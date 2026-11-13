#!/usr/bin/env python3
"""Build the review page: inject the review data (recording, clips, plan) into the page template.

Usage: build_review.py data.json ../templates/review.html "OUT/<CODE> Clip Review.html" [--tokens brand.json]

The page ships with neutral colors and system-safe fonts. --tokens FILE (alias --style, or the BRAND_TOKENS
environment variable) writes a brand's colors and fonts into the light theme: the shared tokens of
docs/BRAND-TOKENS.md (paper, panel, ink, secondary, accent, fonts display, text, inscription; optional
"font_css", the URL of a stylesheet that declares the fonts). The dark theme keeps its neutral values.

data.json: see ../templates/review-data.example.json. For a Claude artifact, each clip's "src" and "poster" are the
URLs returned by the asset upload. For a local review folder, they are paths relative to the HTML file.
Standard library only.
"""
import html, json, os, re, sys
import brand_tokens


def brand_css(path):
    """CSS written at the template's brand marker; empty without a tokens file."""
    if not (path or os.environ.get("BRAND_TOKENS")):
        return "", ""
    t = brand_tokens.resolve(path=path)
    c, f = t["colors"], t["fonts"]
    safe = lambda v: re.sub(r"[^#\w .,()%-]", "", str(v))
    css = (f":root {{ --paper: {safe(c['paper'])}; --panel: {safe(c['panel'])}; --ink: {safe(c['ink'])}; "
           f"--muted: {safe(c['secondary'])}; --signal: {safe(c['accent'])}; "
           f"--display: \"{safe(f['display'])}\", \"Helvetica Neue\", Arial, sans-serif; "
           f"--body: \"{safe(f['text'])}\", \"Helvetica Neue\", Arial, sans-serif; "
           f"--mono: \"{safe(f['inscription'])}\", ui-monospace, Menlo, monospace; }}")
    link = f'<link rel="stylesheet" href="{html.escape(t["font_css"], quote=True)}">\n' if t.get("font_css") else ""
    return css, link


def main():
    tokens = None
    for flag in ("--tokens", "--style"):
        if flag in sys.argv:
            i = sys.argv.index(flag)
            if i + 1 >= len(sys.argv):
                sys.exit(__doc__)
            tokens = sys.argv[i + 1]
            del sys.argv[i:i + 2]
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
    css, link = brand_css(tokens)
    if css and "/*__BRAND__*/" not in out:
        sys.exit("template: the /*__BRAND__*/ marker is missing (brand tokens cannot be applied)")
    out = out.replace("/*__BRAND__*/", css, 1)
    if link:
        out = out.replace("<style>", link + "<style>", 1)
    out = out.replace("<title>Clip Review</title>", f"<title>{html.escape(str(live['code']))} Clip Review</title>", 1)
    with open(sys.argv[3], "w", encoding="utf-8") as f:
        f.write(out)
    print("written", sys.argv[3], len(out), "bytes,", len(data.get("clips", [])), "clips")


if __name__ == "__main__":
    main()
