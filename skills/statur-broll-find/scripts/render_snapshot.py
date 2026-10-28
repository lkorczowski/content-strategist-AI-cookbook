#!/usr/bin/env python3
"""Render a page snapshot (snapshot.js) offline, crisp, with private parts hidden, and locate elements so
the edit can zoom on them or draw a highlight box.

The render blocks every network request: what you see is exactly what the snapshot holds.

Usage:
  render_snapshot.py SNAPSHOT.html OUT.png [--width 1100] [--scale 2] [--hide CSS ...] [--blur CSS ...]
                     [--find "label=CSS or text:Some text" ...] [--boxes boxes.json] [--log assets.csv] [--claim "..."]

--find returns boxes in image pixels (x, y, w, h), ready for the page_card highlights of statur-motion-design.
  "text:Content Strategist" finds the smallest element whose text contains the string.
"""
import argparse, csv, datetime, json, os, pathlib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("snapshot"); ap.add_argument("out")
    ap.add_argument("--width", type=int, default=1100); ap.add_argument("--height", type=int, default=1400)
    ap.add_argument("--scale", type=float, default=2.0)
    ap.add_argument("--hide", nargs="*", default=[]); ap.add_argument("--blur", nargs="*", default=[])
    ap.add_argument("--find", nargs="*", default=[]); ap.add_argument("--boxes", default=None)
    ap.add_argument("--log", default=None); ap.add_argument("--claim", default="")
    ap.add_argument("--owner", choices=["own", "third-party"], default="own"); ap.add_argument("--note", default="")
    a = ap.parse_args()
    from playwright.sync_api import sync_playwright
    p = pathlib.Path(a.snapshot).resolve()
    css = "".join(f"{s}{{display:none!important}}" for s in a.hide) + "".join(f"{s}{{filter:blur(14px)!important}}" for s in a.blur)
    boxes, src = {}, {}
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": a.width, "height": a.height}, device_scale_factor=a.scale)
        pg.route("**/*", lambda r: r.continue_() if r.request.url.startswith(("file:", "data:")) else r.abort())
        pg.goto(p.as_uri(), wait_until="load")
        if css:
            pg.add_style_tag(content=css)
        pg.wait_for_timeout(600)
        for f in a.find:
            label, _, q = f.partition("=")
            if not q:
                label, q = f, f
            boxes[label] = pg.evaluate("""([q, s]) => {
              let el = null;
              if (q.startsWith('text:')) {
                const t = q.slice(5); const all = [...document.querySelectorAll('body *')].filter(e => e.textContent.includes(t));
                all.sort((x, y) => x.textContent.length - y.textContent.length); el = all[0];
              } else el = document.querySelector(q);
              if (!el) return null;
              const r = el.getBoundingClientRect();
              return [Math.round(r.x * s), Math.round((r.y + scrollY) * s), Math.round(r.width * s), Math.round(r.height * s)];
            }""", [q, a.scale])
        src = pg.evaluate("() => { const m = document.querySelector('meta[name=snapshot-source]'); return m ? JSON.parse(m.content) : {}; }")
        pg.screenshot(path=a.out, full_page=True)
        b.close()
    if a.boxes:
        json.dump(boxes, open(a.boxes, "w"), indent=1)
    log = a.log or os.path.join(os.path.dirname(os.path.abspath(a.out)), "assets.csv")
    new = not os.path.exists(log)
    with open(log, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["file", "kind", "source", "title", "captured_at", "owner", "license_note", "claim"])
        w.writerow([os.path.basename(a.out), "page_snapshot", src.get("url", ""), src.get("title", ""), src.get("at", datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")),
                    a.owner, a.note or ("own page" if a.owner == "own" else "THIRD PARTY: reviewer decides"), a.claim])
    print(json.dumps({"status": "DONE", "out": a.out, "boxes": boxes, "source": src}))

if __name__ == "__main__":
    main()
