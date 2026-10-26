#!/usr/bin/env python3
"""Build the review page: inject the review data (recording, clips, plan) into the page template.

Usage: build_review.py data.json ../templates/review.html "OUT/<CODE> Clip Review.html"

data.json: see ../templates/review-data.example.json. For a Claude artifact, each clip's "src" and "poster" are the
URLs returned by the asset upload. For a local review folder, they are paths relative to the HTML file.
Standard library only.
"""
import html, json, sys


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    tpl = open(sys.argv[2], encoding="utf-8").read()
    live = data.get("live") or {}
    missing = [k for k in ("code", "title", "date", "duration") if k not in live]
    if missing:
        sys.exit(f"data.json: live is missing {missing}")
    for c in data.get("clips", []):
        for k in ("id", "v", "title", "dur"):
            if k not in c:
                sys.exit(f"data.json: clip {c.get('id', '?')} is missing '{k}'")
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    if "/*__DATA__*/" not in tpl:
        sys.exit("template: the /*__DATA__*/ marker is missing")
    out = tpl.replace("/*__DATA__*/", "window.__REVIEW_DATA__ = " + blob + ";")
    out = out.replace("<title>Clip Review</title>", f"<title>{html.escape(str(live['code']))} Clip Review</title>", 1)
    with open(sys.argv[3], "w", encoding="utf-8") as f:
        f.write(out)
    print("written", sys.argv[3], len(out), "bytes,", len(data.get("clips", [])), "clips")


if __name__ == "__main__":
    main()
