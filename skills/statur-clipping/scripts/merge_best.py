#!/usr/bin/env python3
"""Merge two transcriptions of the same passage, keeping, phrase by phrase, the one in the expected language.

Multilingual ASR sometimes hears a French phrase as English (or the reverse), and which phrases go
wrong depends on how the audio was chunked. refine_span.py gives a second reading with short chunks;
this tool cuts the passage into phrases (pauses of the first reading) and keeps, for each phrase,
the reading with fewer words of the wrong language.

Usage:
  merge_best.py words.orig.json words.json START END [--lang fr] [--out words.json]
"""
import argparse, json, re

EN = set("the it's is my for so and you that this what with are but don't do we they it i i've i'm your be "
         "have was not can just like very bad good there their them he she his her our if then than "
         "because about would could should".split())
FR = set("le la les un une des du de et est je tu il elle on nous vous ils elles que qui ça c'est pas mais "
         "donc parce en au aux ce cette mon ma mes ton ta tes son sa ses leur avec pour sur dans faut "
         "fait ont sont avoir être va vais bah euh ouais voilà alors".split())

def norm(w):
    return re.sub(r"[^\w'’-]", "", w.lower()).replace("’", "'")

def wrong_ratio(ws, lang):
    if not ws:
        return 1.0
    bad = EN if lang == "fr" else FR
    return sum(1 for w in ws if norm(w["w"]) in bad) / len(ws)

def secs(x):
    if ":" in str(x):
        p = [float(v) for v in str(x).split(":")]
        return sum(v * 60 ** i for i, v in enumerate(reversed(p)))
    return float(x)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("orig"); ap.add_argument("new"); ap.add_argument("start"); ap.add_argument("end")
    ap.add_argument("--lang", default="fr"); ap.add_argument("--out", default=None)
    a = ap.parse_args()
    S, E = secs(a.start), secs(a.end)
    A = json.load(open(a.orig)); B = json.load(open(a.new))
    mid = lambda w: (w["s"] + w["e"]) / 2
    a_in = [w for w in A if S <= mid(w) <= E]
    b_in = [w for w in B if S <= mid(w) <= E]
    # windows: split at the pauses (> 0.35 s) of the first reading
    cuts = [S]
    for x, y in zip(a_in, a_in[1:]):
        if y["s"] - x["e"] > 0.35:
            cuts.append((x["e"] + y["s"]) / 2)
    cuts.append(E + 1e-6)
    out, picks = [], []
    for lo, hi in zip(cuts, cuts[1:]):
        wa = [w for w in a_in if lo <= mid(w) < hi]
        wb = [w for w in b_in if lo <= mid(w) < hi]
        ra, rb = wrong_ratio(wa, a.lang), wrong_ratio(wb, a.lang)
        keep_a = wa and ra < rb
        out.extend(wa if keep_a else wb)
        if keep_a:
            picks.append(f"{lo:.1f}-{hi:.1f} first reading: " + " ".join(w["w"] for w in wa)[:120])
    merged = [w for w in B if mid(w) < S] + sorted(out, key=lambda w: w["s"]) + [w for w in B if mid(w) > E]
    json.dump(merged, open(a.out or a.new, "w"), ensure_ascii=False)
    print(f"{len(picks)} phrase(s) taken from the first reading")
    for p in picks:
        print("  " + p)

if __name__ == "__main__":
    main()
