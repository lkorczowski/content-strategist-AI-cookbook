#!/usr/bin/env python3
"""Render every clip spec of a live, one after the other, and copy each master to EXPORTS.

Resumable: run it again until it prints ALL_DONE (machines that cap command time stop it midway;
each clip_render.py run resumes where it stopped). A clip is skipped when its spec has not changed
since its last successful export.

Usage:
  render_all.py --project "2026-10-24 LIVE01 Title" --code LIVE01 --source RUSH --words words.json
                [--sync sync.json] [--audio audio16k.flac] [--fonts DIR] [--tmp /tmp/clips] [--budget 150] SPEC [SPEC ...]
Outputs: TRAVAIL <code>/<id>_v<version>/ (master, captions, review copy) and
         EXPORTS <code>/<code>_<id>_v<version>_<slug>.mp4 + .srt
The root of EXPORTS keeps only the newest version of each clip: older versions (.mp4 and .srt) move to
EXPORTS <code>/archives/ (moved, never deleted). Move a clip you drop to archives/ yourself. --keep-old disables it.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, time

def archive_older(exports, code, cid):
    """Keep only the highest version of clip <cid> at the root of EXPORTS; move the others to EXPORTS/archives/."""
    pat = re.compile(r"^" + re.escape(code) + "_" + re.escape(cid) + r"_v(\d+)_.+\.(mp4|srt)$")
    found = [(int(m.group(1)), n) for n in os.listdir(exports) for m in [pat.match(n)] if m]
    if not found:
        return []
    top = max(v for v, _ in found)
    arch = os.path.join(exports, "archives")
    moved = []
    for v, n in found:
        if v < top:
            os.makedirs(arch, exist_ok=True)
            dst = os.path.join(arch, n)
            if os.path.exists(dst):                      # never overwrite an archived file
                base, ext = os.path.splitext(n)
                dst = os.path.join(arch, f"{base}_{time.strftime('%Y%m%d-%H%M%S')}{ext}")
            shutil.move(os.path.join(exports, n), dst)
            moved.append(n)
    return moved
HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True); ap.add_argument("--code", required=True)
    ap.add_argument("--source", required=True); ap.add_argument("--words", required=True)
    ap.add_argument("--sync", default=None); ap.add_argument("--fonts", default=os.path.join(HERE, "..", "fonts"))
    ap.add_argument("--audio", default=None, help="transcript audio (audio16k.flac): each cut-in moves back to the real speech onset")
    ap.add_argument("--tmp", default="/tmp/clips"); ap.add_argument("--budget", type=float, default=0)
    ap.add_argument("--watermark", default=None, help="default watermark text for every clip (a spec's own text wins)")
    ap.add_argument("--keep-temp", action="store_true", help="keep the rendered pieces (faster re-renders, more disk)")
    ap.add_argument("--keep-old", action="store_true", help="leave older versions at the root of EXPORTS (default: move them to EXPORTS/archives/)")
    ap.add_argument("specs", nargs="+")
    a = ap.parse_args()
    t0 = time.time()
    work = os.path.join(a.project, f"TRAVAIL {a.code}"); exports = os.path.join(a.project, f"EXPORTS {a.code}")
    os.makedirs(exports, exist_ok=True)
    pending = 0
    words = json.load(open(a.words))
    for sp in a.specs:
        spec = json.load(open(sp))
        # the hash covers the spec and only the words inside its passages: refining another passage
        # of the transcript does not re-render this clip
        used = [w for w in words if any(float(g["s"]) - 1 <= w["s"] <= float(g["e"]) + 1 for g in spec["segments"])]
        sha = hashlib.sha1(open(sp, "rb").read() + json.dumps(used, sort_keys=True).encode()
                           + str(a.watermark).encode() + open(os.path.join(HERE, "clip_render.py"), "rb").read()).hexdigest()[:12]
        cid, v = spec.get("id", "clip"), spec.get("version", 1)
        slug = spec.get("slug", "clip")
        out = os.path.join(work, f"{cid}_v{v}")
        marker = os.path.join(out, ".exported")          # holds the hash of the last exported spec
        if os.path.exists(marker) and open(marker).read().strip() == sha:
            print(json.dumps({"clip": f"{cid}_v{v}", "status": "SKIP"})); continue
        left = a.budget - (time.time() - t0) if a.budget else 0
        if a.budget and left < 20:
            pending += 1; print(json.dumps({"clip": f"{cid}_v{v}", "status": "WAITING"})); continue
        cmd = [sys.executable, os.path.join(HERE, "clip_render.py"), "--source", a.source, "--words", a.words,
               "--spec", sp, "--out", out, "--fonts", a.fonts, "--review", "--tmp", a.tmp]
        if a.sync:
            cmd += ["--sync", a.sync]
        if a.audio:
            cmd += ["--audio", a.audio]
        if a.watermark:
            cmd += ["--watermark", a.watermark]
        if a.keep_temp:
            cmd += ["--keep-temp"]
        if a.budget:
            cmd += ["--budget", f"{left:.0f}"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 3:      # out of time: finish this clip on the next run before starting another one
            pending += 1; print(json.dumps({"clip": f"{cid}_v{v}", "status": "INCOMPLETE"}))
            t0 = -1e9; continue
        if r.returncode != 0:
            print(json.dumps({"clip": f"{cid}_v{v}", "status": "FAILED", "error": r.stderr[-800:]})); pending += 1; continue
        name = f"{a.code}_{cid}_v{v}_{slug}"
        shutil.copy(os.path.join(out, f"{cid}_v{v}_master.mp4"), os.path.join(exports, name + ".mp4"))
        shutil.copy(os.path.join(out, "captions.srt"), os.path.join(exports, name + ".srt"))
        open(marker, "w").write(sha)
        archived = [] if a.keep_old else archive_older(exports, a.code, cid)
        rep = json.load(open(os.path.join(out, "render_report.json")))
        print(json.dumps({"clip": f"{cid}_v{v}", "status": "DONE", "duration": rep["duration"], "export": name + ".mp4", "archived": archived}))
    print("ALL_DONE" if pending == 0 else f"PENDING {pending}: run again")

if __name__ == "__main__":
    main()
