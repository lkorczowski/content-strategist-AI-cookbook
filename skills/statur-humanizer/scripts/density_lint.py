#!/usr/bin/env python3
"""Density lint: find the text a reader skips, before a person has to point at it.

Reads built HTML pages, Markdown or plain text and reports, per page: word count against a
budget, over-long paragraphs and sentences, blocks repeated on the page, facts repeated too
often, defensive notes, signposting, filler, labeled micro-lines stacked in cards, and blocks
copied on many pages. It measures; the judgment (cut, merge, move) stays with the editor.

Usage:
  python3 density_lint.py dist/                      every index.html under dist/
  python3 density_lint.py page.html draft.md         single files
  python3 density_lint.py dist/ --config lint.json   budgets and extra phrases
  python3 density_lint.py draft.md --as /blog/x/ --config lint.json   a draft, with the budget of its future page
  python3 density_lint.py dist/ --json report.json   machine-readable report
  python3 density_lint.py dist/ --strict             exit 1 when a page is over budget
  python3 density_lint.py dist/ --page /pricing/ -v  list every hit of one page

Config (JSON, all keys optional):
  {"budgets": {"/": 900, "/lp/*": 700, "/blog/*": 1800, "*": 4000},
   "max_paragraph": 60, "max_sentence": 28, "max_fact_repeats": 2,
   "ignore_pages": ["/privacy/", "/terms/"], "ignore_selectors": ["pre", "code"],
   "defensive": ["extra regex"], "signpost": ["extra regex"], "filler": ["extra regex"]}
Budgets match the page path with shell wildcards, first match wins, "*" last.
Standard library only. Python 3.8+.
"""
import argparse, collections, fnmatch, glob, json, os, re, sys
from html.parser import HTMLParser

SKIP = {"script", "style", "nav", "footer", "svg", "noscript", "template", "head", "form", "select"}
BLOCK = {"h1", "h2", "h3", "h4", "p", "li", "figcaption", "blockquote", "td", "th", "summary", "small",
         "label", "button", "div", "section", "article", "figure", "ul", "ol", "table", "tr", "details",
         "main", "aside", "dt", "dd", "pre", "header"}
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "wbr", "area", "base", "col", "embed", "track"}

DEFAULTS = {
    "budgets": {"*": 4000},
    "max_paragraph": 60,       # convention (plain-language guides allow more; web pages are scanned)
    "max_sentence": 28,        # convention
    "max_fact_repeats": 2,     # a number may appear twice on a page: once as proof, once as recall
    "ignore_pages": [],
    "ignore_selectors": ["pre", "code"],
    "defensive": [], "signpost": [], "filler": [],
}
DEFENSIVE = [
    r"^\s*(//|\*|note\s*:|nb\s*:|disclaimer)", r"\bfigures? (are )?attributed\b", r"\b(are|is) left out\b",
    r"\bunder nda\b", r"\bresults? (may|will|can) vary\b", r"\bmethodolog", r"\bhow we count", r"\bfor transparency\b",
    r"\bto be clear\b", r"\bit('s| is) (important|worth) (to note|noting)\b", r"\bplease note\b", r"\bkeep in mind\b",
    r"\bnot (a )?guarantee", r"\bself-reported\b", r"\bat the time of writing\b", r"\bas of (this writing|today)\b",
]
SIGNPOST = [
    r"\bin this (guide|playbook|handbook|section|chapter|article|post|essay)\b", r"\b(below|above),? (you('ll| will)|we|i)\b",
    r"\bas (mentioned|said|noted|described|explained|shown) (above|earlier|before|below)\b", r"\bhere('s| is) (what|how|why|the)\b",
    r"\blet('s| us) (dive|look|break|start|walk|unpack)\b", r"\bthis (section|chapter|page|guide|playbook|handbook) (covers|explains|shows|walks|is about|gives)\b",
    r"\bin (short|summary|other words|a nutshell)\b", r"\bto (sum up|recap|summarize)\b", r"\bthe (rest|remainder) of this\b",
    r"\bbefore (we|you) (start|begin|go further)\b", r"\bread on (to|for|and)\b", r"\bthat('s| is) (why|what) this\b",
]
FILLER = [
    r"\b(moreover|additionally|furthermore|importantly|essentially|basically|actually|really|simply|just|very|quite)\b",
    r"\bin order to\b", r"\bthe fact that\b", r"\bat the end of the day\b", r"\bwhen it comes to\b", r"\bit turns out\b",
    r"\b(kind|sort) of\b", r"\bneedless to say\b", r"\bof course\b", r"\bas you (know|can see|might expect)\b",
]
LABEL = re.compile(r"^(format|why|how|what|who|when|where|source|sources|note|result|context|proof|tip|rule|example|takeaway)\s*:", re.I)
NUM = re.compile(r"(?<![\w.])[$€£]?\d[\d.,]*\s?(?:[kKmMbB]\b|%|\+|x\b)?\+?")


class Blocks(HTMLParser):
    def __init__(self, ignore):
        super().__init__(); self.skip = 0; self.stack = []; self.buf = []; self.out = []; self.ignore = set(ignore) | SKIP
    def flush(self):
        t = re.sub(r"\s+", " ", "".join(self.buf)).strip(); self.buf = []
        if t:
            tag = next((a for a in reversed(self.stack) if a in BLOCK), "body")
            self.out.append((tag, t))
    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            if tag == "br": self.buf.append(" ")
            return
        if tag in BLOCK: self.flush()
        if tag in self.ignore: self.skip += 1
        self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in VOID or tag not in self.stack: return
        if tag in BLOCK: self.flush()
        while self.stack:
            t = self.stack.pop()
            if t in self.ignore: self.skip -= 1
            if t == tag: break
    def handle_data(self, d):
        if self.skip <= 0: self.buf.append(d)


def read_blocks(path, ignore):
    text = open(path, encoding="utf-8", errors="replace").read()
    if path.endswith((".html", ".htm")):
        p = Blocks(ignore); p.feed(text); p.flush(); return p.out
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)          # YAML front matter is not read by anyone
    text = re.sub(r"```.*?```", "", text, flags=re.S) if "pre" in ignore else text
    text = re.sub(r"\n(?=[ \t]*(?:[-*+]|\d+\.)[ \t])", "\n\n", text)   # one block per list item
    out = []
    for para in re.split(r"\n\s*\n", text):
        t = re.sub(r"\s+", " ", re.sub(r"[#>*_`|]+", " ", para)).strip()
        if t: out.append(("h2" if para.lstrip().startswith("#") else "p", t))
    return out


def sentences(t):
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", t) if len(s.split()) > 2]


def hits(patterns, blocks):
    rx = [re.compile(p, re.I) for p in patterns]; found = []
    for i, (_, t) in enumerate(blocks):
        for r in rx:
            m = r.search(t)
            if m: found.append((i, m.group(0), t)); break
    return found


def lint(blocks, cfg):
    body = [(i, tag, t) for i, (tag, t) in enumerate(blocks)]
    words = sum(len(t.split()) for _, t in blocks)
    r = {"words": words, "blocks": len(blocks)}
    r["long_paragraphs"] = [(i, len(t.split()), t) for i, tag, t in body if len(t.split()) > cfg["max_paragraph"]]
    r["long_sentences"] = [(i, len(s.split()), s) for i, tag, t in body for s in sentences(t) if len(s.split()) > cfg["max_sentence"]]
    seen = collections.defaultdict(list)
    for i, tag, t in body:
        if len(t.split()) >= 8: seen[t.lower()].append(i)
    r["repeated_blocks"] = [(v, k) for k, v in seen.items() if len(v) > 1]
    facts = collections.defaultdict(set)
    for i, tag, t in body:
        for m in NUM.findall(t):
            m = re.sub(r"\s", "", m).rstrip(".,")
            if len(re.sub(r"\D", "", m)) >= 3 or re.search(r"[kKmMbB%x+$€£]", m): facts[m].add(i)
    r["repeated_facts"] = sorted(((len(v), k, sorted(v)) for k, v in facts.items() if len(v) > cfg["max_fact_repeats"]), reverse=True)
    r["defensive"] = hits(DEFENSIVE + cfg["defensive"], blocks)
    r["signpost"] = hits(SIGNPOST + cfg["signpost"], blocks)
    r["filler"] = [(i, m.group(0), t) for i, (_, t) in enumerate(blocks) for p in FILLER + cfg["filler"] for m in re.finditer(p, t, re.I)]
    r["labeled_lines"] = [(i, t) for i, tag, t in body if LABEL.match(t)]
    ws = [len(s.split()) for _, t in blocks for s in sentences(t)]
    r["avg_sentence"] = round(sum(ws) / max(1, len(ws)), 1)
    return r


def budget_for(url, budgets):
    for pat, n in budgets.items():
        if pat != "*" and fnmatch.fnmatch(url, pat): return n
    return budgets.get("*", 10 ** 9)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+"); ap.add_argument("--config"); ap.add_argument("--json")
    ap.add_argument("--strict", action="store_true"); ap.add_argument("--page"); ap.add_argument("--as", dest="as_url", help="page path a single draft will be published at, to pick its budget, e.g. /blog/my-post/"); ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    cfg = dict(DEFAULTS)
    if a.config: cfg.update(json.load(open(a.config, encoding="utf-8")))
    files = []
    for p in a.paths:
        if os.path.isdir(p):
            for f in sorted(glob.glob(os.path.join(p, "**", "index.html"), recursive=True)):
                rel = os.path.relpath(os.path.dirname(f), p); files.append(("/" if rel == "." else "/" + rel + "/", f))
        else: files.append((a.as_url if a.as_url and len(a.paths) == 1 else p, p))
    files = [(u, f) for u, f in files if not any(fnmatch.fnmatch(u, i) for i in cfg["ignore_pages"])]
    pages = {u: read_blocks(f, cfg["ignore_selectors"]) for u, f in files}
    cross = collections.defaultdict(set)
    for u, bl in pages.items():
        for _, t in bl:
            if len(t.split()) >= 12: cross[t].add(u)
    shared = sorted(((len(v) * len(k.split()), len(v), k) for k, v in cross.items() if len(v) >= 3), reverse=True)
    report, over = {}, 0
    print(f"{'page':44} {'words':>6} {'budget':>6} {'long¶':>5} {'longS':>5} {'rep':>4} {'fact':>4} {'def':>4} {'sign':>4} {'fill':>4} {'lab':>4}")
    for u in sorted(pages, key=lambda k: -sum(len(t.split()) for _, t in pages[k])):
        r = lint(pages[u], cfg); b = budget_for(u, cfg["budgets"]); r["budget"] = b; r["over_budget"] = r["words"] > b
        over += r["over_budget"]; report[u] = r
        print(f"{u[:44]:44} {r['words']:6} {b if b < 10**9 else '-':>6} {len(r['long_paragraphs']):5} {len(r['long_sentences']):5} "
              f"{len(r['repeated_blocks']):4} {len(r['repeated_facts']):4} {len(r['defensive']):4} {len(r['signpost']):4} {len(r['filler']):4} {len(r['labeled_lines']):4}"
              + ("  OVER" if r["over_budget"] else ""))
    if shared:
        print(f"\nBlocks copied on 3+ pages: {len(shared)} ({sum(s[0] for s in shared)} words served in total)")
        for w, n, t in shared[:10]: print(f"  x{n:<3} {t[:110]}")
    for u, r in report.items():
        if not (a.verbose and (not a.page or a.page == u)): continue
        print(f"\n== {u}")
        for i, n, t in r["long_paragraphs"]: print(f"  long paragraph #{i} ({n}w): {t[:140]}")
        for i, n, t in r["long_sentences"]: print(f"  long sentence #{i} ({n}w): {t[:140]}")
        for idx, t in r["repeated_blocks"]: print(f"  repeated {idx}: {t[:120]}")
        for n, k, idx in r["repeated_facts"]: print(f"  fact {k} in {n} blocks {idx}")
        for key in ("defensive", "signpost"):
            for i, m, t in r[key]: print(f"  {key} #{i} [{m}]: {t[:140]}")
        for i, t in r["labeled_lines"]: print(f"  labeled line #{i}: {t[:100]}")
    if a.json:
        json.dump({"pages": report, "shared": shared}, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{len(report)} page(s), {sum(r['words'] for r in report.values())} words, {over} over budget")
    sys.exit(1 if (a.strict and over) else 0)


if __name__ == "__main__":
    main()
