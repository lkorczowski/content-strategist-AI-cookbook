#!/usr/bin/env python3
"""Render one motion-design layer (JSON timeline) to numbered frames, with alpha.

A layer is a list of elements (template, start, end, props) on the output timeline. The renderer opens
a headless Chromium page with the engine and the templates, then for every frame where at least one
element is active it calls seek(t) and screenshots the stage. Frames where nothing is active are
skipped: the compositor treats a missing frame as transparent.

Usage:
  motion_render.py LAYER.json OUTDIR [--fps 30] [--workers 2] [--format png|jpg] [--only 120-240]
                   [--fonts-dir node_modules/@fontsource] [--tokens brand.json]

Layer file:
  {"w":1080,"h":1920,"fps":30,"opaque":false,"tokens":{...},"elements":[{"id","type","start","end","props"}]}
  "tokens" is optional: the shared brand tokens (docs/BRAND-TOKENS.md) or the older flat tokens. Without it the
  renderer reads --tokens FILE (alias --style), then the BRAND_TOKENS environment variable, then neutral defaults.
  Image paths in props (keys img, images, posters, src) may be relative to the layer file.

Speed: about 14 frames per second for a 1080x1920 PNG with alpha on 2 vCPUs (measured 2026-10-28).
"""
import argparse, json, os, pathlib, re, sys, time
import brand_tokens
from multiprocessing import Process, Queue

HERE = pathlib.Path(__file__).resolve().parent

FONT_PACKAGES = {}  # family -> fontsource package, only when the package name is not the family in lowercase with hyphens

def font_list(tokens, fonts_dir):
    """Every woff2 file found for the token fonts: <fonts_dir>/<package>/files/<package>-latin-<weight>-<style>.woff2."""
    out, fams = [], {tokens.get(k) for k in ("font_display", "font_body", "font_mono", "font_serif", "font_logo")} - {None}
    for fam in sorted(fams):
        pkg = FONT_PACKAGES.get(fam, re.sub(r"[^a-z0-9]+", "-", fam.lower()).strip("-"))
        for f in sorted((pathlib.Path(fonts_dir) / pkg / "files").glob(f"{pkg}-latin-*.woff2")):
            m = re.fullmatch(rf"{re.escape(pkg)}-latin-(\d+)-(normal|italic)\.woff2", f.name)
            if m:
                out.append({"family": fam, "weight": int(m.group(1)), "style": m.group(2), "src": f.as_uri()})
    return out

def resolve_paths(obj, base):
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k in ("img", "src") and isinstance(v, str) and not v.startswith(("file:", "http", "data:")):
                obj[k] = (base / v).resolve().as_uri()
            elif k in ("images", "posters") and isinstance(v, list):
                obj[k] = [x if str(x).startswith(("file:", "http", "data:")) else (base / x).resolve().as_uri() for x in v]
            else:
                resolve_paths(v, base)
    elif isinstance(obj, list):
        for x in obj:
            resolve_paths(x, base)

def stage_html():
    parts = [(HERE / "engine.js").read_text()]
    for f in sorted((HERE / "templates").glob("*.js")):
        parts.append(f.read_text())
    js = "\n".join(parts)
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'><style>html,body{margin:0;padding:0;background:transparent;overflow:hidden}"
            "#stage{position:absolute;left:0;top:0;overflow:hidden}</style></head><body><div id='stage'></div><script>" + js + "</script></body></html>")

def worker(wid, tl, frames, outdir, fmt, q):
    try:
        _worker(wid, tl, frames, outdir, fmt, q)
    except Exception as e:                      # always report, so the parent never waits forever
        q.put(("error", wid, repr(e)))

def _worker(wid, tl, frames, outdir, fmt, q):
    from playwright.sync_api import sync_playwright
    html = pathlib.Path(outdir).resolve() / f".stage_{wid}.html"
    html.write_text(stage_html())
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--allow-file-access-from-files", "--disable-web-security"])
        pg = b.new_page(viewport={"width": tl["w"], "height": tl["h"]}, device_scale_factor=1)
        pg.goto(html.as_uri())
        pg.evaluate("async (tl) => await init(tl)", tl)
        n = 0
        for i in frames:
            t = i / tl["fps"]
            pg.evaluate("async (t) => await seek(t)", t)
            path = os.path.join(outdir, f"{i:06d}.{fmt}")
            if fmt == "png":
                pg.screenshot(path=path, type="png", omit_background=not tl.get("opaque"))
            else:
                pg.screenshot(path=path, type="jpeg", quality=93)
            n += 1
            if n % 150 == 0:
                q.put(("progress", wid, n))
        b.close()
    html.unlink()
    q.put(("done", wid, n))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("layer"); ap.add_argument("outdir")
    ap.add_argument("--fps", type=float, default=0)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--format", default=None, choices=["png", "jpg"])
    ap.add_argument("--only", default=None, help="frame range a-b (inclusive) for tests")
    ap.add_argument("--frames", default=None, help="comma-separated frame numbers (previews)")
    ap.add_argument("--allow-system-fonts", action="store_true", help="render even when a token font is missing (fallback font)")
    ap.add_argument("--fonts-dir", default=str(HERE.parent / "fonts" / "node_modules" / "@fontsource"))
    ap.add_argument("--tokens", "--style", dest="tokens", default=None, help="brand tokens JSON (docs/BRAND-TOKENS.md); the layer's own tokens win")
    ap.add_argument("--duration", type=float, default=0, help="timeline length in seconds (default: last element end)")
    a = ap.parse_args()
    lp = pathlib.Path(a.layer).resolve()
    tl = json.load(open(lp))
    tl.setdefault("w", 1080); tl.setdefault("h", 1920)
    tl["fps"] = a.fps or tl.get("fps", 30)
    resolve_paths(tl["elements"], lp.parent)
    brand = brand_tokens.resolve(tl.get("tokens"), a.tokens)
    tl["tokens"] = brand_tokens.flat(brand)
    tl["fonts"] = font_list(tl["tokens"], a.fonts_dir)
    # a missing brand font never fails in the browser: it silently falls back to a system font. Stop here instead.
    # Only fonts named in a tokens file are checked: the neutral defaults may fall back to system fonts.
    missing = sorted(f for f in brand["_given_fonts"] if f not in {x["family"] for x in tl["fonts"]})
    if missing and not a.allow_system_fonts:
        sys.exit(f"fonts not found in {a.fonts_dir}: {', '.join(missing)}. Install them (npm i --prefix fonts @fontsource/<family>), "
                 "point --fonts-dir to the @fontsource folder, or add the family to FONT_PACKAGES. --allow-system-fonts renders anyway.")
    fmt = a.format or ("jpg" if tl.get("opaque") else "png")
    dur = a.duration or max(e["end"] for e in tl["elements"])
    nfr = int(round(dur * tl["fps"]))
    frames = [i for i in range(nfr) if any(e["start"] <= i / tl["fps"] < e["end"] for e in tl["elements"])]
    all_frames = list(frames)
    if a.only:
        lo, hi = [int(x) for x in a.only.split("-")]
        frames = [i for i in frames if lo <= i <= hi]
    if a.frames:
        want = {int(x) for x in a.frames.split(",") if x.strip()}
        frames = [i for i in frames if i in want]
    a.outdir = os.path.abspath(a.outdir)
    os.makedirs(a.outdir, exist_ok=True)
    t0 = time.time()
    W = max(1, min(a.workers, len(frames)))
    q, procs = Queue(), []
    for k in range(W):
        part = frames[k::W]
        pr = Process(target=worker, args=(k, tl, part, a.outdir, fmt, q)); pr.start(); procs.append(pr)
    done, failed = 0, False
    while done < W:
        kind, wid, n = q.get()
        if kind == "error":
            sys.stderr.write(f"worker {wid} failed: {n}\n"); done += 1; failed = True
        elif kind == "done":
            done += 1
        else:
            print(json.dumps({"worker": wid, "frames": n}), flush=True)
    for pr in procs:
        pr.join()
    # the manifest lists every frame of this timeline that exists on disk, so a partial re-render (--only, --frames)
    # patches a layer without hiding the frames rendered before
    on_disk = [i for i in all_frames if os.path.exists(os.path.join(a.outdir, f"{i:06d}.{fmt}"))]
    json.dump({"layer": tl.get("layer", lp.stem), "fps": tl["fps"], "w": tl["w"], "h": tl["h"], "format": fmt,
               "opaque": bool(tl.get("opaque")), "frames": on_disk}, open(os.path.join(a.outdir, "manifest.json"), "w"))
    el = time.time() - t0
    if failed:
        sys.exit(1)
    print(json.dumps({"status": "DONE", "layer": str(lp.name), "frames": len(frames), "seconds": round(el, 1),
                      "fps": round(len(frames) / max(el, 1e-6), 2)}))

if __name__ == "__main__":
    main()
