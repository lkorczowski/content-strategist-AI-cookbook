#!/usr/bin/env python3
"""Group a word-timestamped transcript into readable blocks for analysis.
A new block starts after a pause longer than --gap seconds or when a block exceeds --max seconds.
Usage: transcript_blocks.py words.json [--gap 1.2] [--max 50] > blocks.txt
Each line: [H:MM:SS-H:MM:SS] text
"""
import argparse, json

def hms(t):
    t = int(t); return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}"

ap = argparse.ArgumentParser()
ap.add_argument("words"); ap.add_argument("--gap", type=float, default=1.2); ap.add_argument("--max", type=float, default=50)
a = ap.parse_args()
ws = sorted(json.load(open(a.words)), key=lambda w: w["s"])
blk, out = [], []
for w in ws:
    if blk and (w["s"] - blk[-1]["e"] > a.gap or w["e"] - blk[0]["s"] > a.max):
        out.append(blk); blk = []
    blk.append(w)
if blk:
    out.append(blk)
for b in out:
    print(f"[{hms(b[0]['s'])}-{hms(b[-1]['e'])}] " + " ".join(x["w"] for x in b))
