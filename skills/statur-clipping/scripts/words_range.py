#!/usr/bin/env python3
"""Print words between two times with their timestamps, one line per pause-separated run.
Usage: words_range.py words.json START END   (H:MM:SS or seconds)"""
import json, sys
def t(x):
    if ":" in x:
        p = [float(v) for v in x.split(":")]
        return sum(v * 60 ** i for i, v in enumerate(reversed(p)))
    return float(x)
ws = json.load(open(sys.argv[1])); a, b = t(sys.argv[2]), t(sys.argv[3])
run, prev = [], None
for w in ws:
    if w["e"] < a or w["s"] > b:
        continue
    if prev is not None and w["s"] - prev > 0.35:
        print(f"{run[0][0]:8.2f}-{prev:8.2f} | " + " ".join(r[1] for r in run)); run = []
    run.append((w["s"], w["w"])); prev = w["e"]
if run:
    print(f"{run[0][0]:8.2f}-{prev:8.2f} | " + " ".join(r[1] for r in run))
