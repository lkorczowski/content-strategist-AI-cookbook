#!/usr/bin/env python3
"""Scan the public repo for private data before every push.

Usage:
  python3 scripts/leak_scan.py                         generic patterns only
  python3 scripts/leak_scan.py --denylist PATH         plus one regex per line from a private file

The denylist file lives in your PRIVATE repo (client names, internal ids, prices), never here.
Lines starting with # are comments. Exit code 1 when something matches. Standard library only.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "dist", "node_modules"}
TEXT_EXT = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".py", ".js", ".ts", ".mjs", ".sh", ".html"}

GENERIC = [
    ("api key or token", r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,})"),
    ("private key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("Airtable id", r"\b(app|tbl|fld|rec|viw)[A-Za-z0-9]{14}\b"),
    ("Google doc or sheet id in a URL", r"docs\.google\.com/(document|spreadsheets|presentation)/d/[A-Za-z0-9_-]{20,}"),
    ("Google Drive file id in a URL", r"drive\.google\.com/(file/d/|open\?id=)[A-Za-z0-9_-]{20,}"),
    ("IBAN", r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){3,7}\b"),
    ("French SIREN or SIRET", r"\b\d{3} ?\d{3} ?\d{3}(?: ?\d{5})?\b"),
    ("phone number", r"(\+33|\+1)[ .-]?\(?\d{1,3}\)?[ .-]?\d{2,4}[ .-]?\d{2,4}[ .-]?\d{2,4}"),
    ("email address", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    ("local machine path", r"/Users/[A-Za-z0-9_-]+/"),
]
ALLOWED_EMAILS = {"noreply@anthropic.com"}


def files():
    for f in ROOT.rglob("*"):
        if f.is_file() and not (set(f.relative_to(ROOT).parts) & SKIP_DIRS) and f.suffix.lower() in TEXT_EXT:
            yield f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--denylist", help="private file with one regex per line")
    args = ap.parse_args()
    rules = [(label, re.compile(rx)) for label, rx in GENERIC]
    if args.denylist:
        for line in Path(args.denylist).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                rules.append(("denylist", re.compile(line, re.IGNORECASE)))
    hits = []
    for f in files():
        if f.name == "leak_scan.py":
            continue
        for n, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for label, rx in rules:
                for m in rx.finditer(line):
                    if label == "email address" and m.group(0) in ALLOWED_EMAILS:
                        continue
                    hits.append(f"{f.relative_to(ROOT)}:{n}: {label}: {m.group(0)[:60]}")
    print(f"leak_scan: {len(rules)} rules, {len(hits)} hit(s)")
    for h in hits:
        print("  -", h)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
