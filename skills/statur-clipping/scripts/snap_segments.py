#!/usr/bin/env python3
"""Snap a clip spec planned on a rough transcript (a platform's captions, Loom or YouTube cues, notes)
to the word timestamps of the local transcription.

Each segment may carry "from" and "to": the first and last words of the passage, as read in the rough
transcript. Each cut may carry "text": the words to remove. The script finds those words in words.json
near the planned times and moves s and e onto them, so the plan can be written before the video is
downloaded and the edit still lands on word boundaries.

Usage:
  snap_segments.py SPEC.json [--root PROJECT] [--words words.json] [--window 8] [--out SPEC_snapped.json]
  (--words for a one-source spec; a mix reads each source's words from the spec's "sources")
Prints one line per segment and cut: the matched words, the old and new times, a score from 0 to 1.
A score under 0.6 means the words were not found: read the passage with words_range.py and set it by hand.
"""
import argparse, difflib, json, os, re, sys, unicodedata

def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9']+", " ", t).replace("'", " ").split()

def flat(words):
    """Tokens of the words list, each tied to the index of its word."""
    toks, idx = [], []
    for i, w in enumerate(words):
        for t in norm(w["w"]):
            toks.append(t); idx.append(i)
    return toks, idx

def find(words, toks, idx, phrase, near, window, prefer="start"):
    """Best match of the phrase's tokens in the words within [near - window, near + window].
    Returns (first word index, last word index, score)."""
    q = norm(phrase)
    if not q:
        return None
    lo, hi = near - window, near + window
    cand = [k for k, i in enumerate(idx) if lo <= words[i]["s"] <= hi]
    if not cand:
        return None
    best = None
    n = len(q)
    for k in cand:
        for L in (n - 1, n, n + 1):
            if L < 1 or k + L > len(toks):
                continue
            sm = difflib.SequenceMatcher(None, q, toks[k:k + L]).ratio()
            dist = abs(words[idx[k]]["s"] - near) / max(window, 1)
            score = sm - 0.05 * dist
            if best is None or score > best[2]:
                best = (idx[k], idx[k + L - 1], score, sm)
    return best

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("--root", default=None); ap.add_argument("--words", default=None)
    ap.add_argument("--window", type=float, default=8.0, help="seconds around the planned time to search")
    ap.add_argument("--out", default=None, help="default: overwrite the spec (a .bak copy is kept)")
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    base = os.path.abspath(a.root or os.path.dirname(os.path.abspath(a.spec)))
    srcs = spec.get("sources") or {"main": {"words": a.words}}
    if not spec.get("sources") and not a.words:
        raise SystemExit("one-source spec: give --words")
    default = spec.get("default_src") or next(iter(srcs))
    cache = {}
    def load(sid):
        if sid not in cache:
            p = srcs[sid]["words"]
            p = p if os.path.isabs(p) else os.path.join(base, p)
            ws = sorted(json.load(open(p)), key=lambda w: w["s"])
            cache[sid] = (ws,) + flat(ws)
        return cache[sid]
    report, low = [], 0
    for k, seg in enumerate(spec["segments"]):
        sid = seg.get("src", default)
        ws, toks, idx = load(sid)
        old = (seg["s"], seg["e"])
        first = len(report)
        if seg.get("from"):
            m = find(ws, toks, idx, seg["from"], float(seg["s"]), a.window)
            if m and m[3] >= 0.6:
                i0 = m[0]
                prev_e = ws[i0 - 1]["e"] if i0 > 0 else ws[i0]["s"] - 0.3
                seg["s"] = round(max(prev_e, ws[i0]["s"] - 0.08), 3)
            report.append({"seg": k, "src": sid, "edge": "from", "text": seg["from"], "score": round(m[3], 2) if m else 0,
                           "found": " ".join(w["w"] for w in ws[m[0]:m[1] + 1]) if m else None})
            low += (not m or m[3] < 0.6)
        if seg.get("to"):
            m = find(ws, toks, idx, seg["to"], float(seg["e"]), a.window)
            if m and m[3] >= 0.6:
                i1 = m[1]
                next_s = ws[i1 + 1]["s"] if i1 + 1 < len(ws) else ws[i1]["e"] + 0.3
                seg["e"] = round(min(next_s, ws[i1]["e"] + 0.15), 3)
            report.append({"seg": k, "src": sid, "edge": "to", "text": seg["to"], "score": round(m[3], 2) if m else 0,
                           "found": " ".join(w["w"] for w in ws[m[0]:m[1] + 1]) if m else None})
            low += (not m or m[3] < 0.6)
        for r in report[first:]:
            r.update({"old": old, "new": (seg["s"], seg["e"])})
    for c in spec.get("cut", []):
        if not isinstance(c, dict) or not c.get("text"):
            continue
        sid = c.get("src", default)
        ws, toks, idx = load(sid)
        m = find(ws, toks, idx, c["text"], float(c["s"]), a.window)
        if m and m[3] >= 0.6:
            i0, i1 = m[0], m[1]
            prev_e = ws[i0 - 1]["e"] if i0 > 0 else ws[i0]["s"] - 0.2
            next_s = ws[i1 + 1]["s"] if i1 + 1 < len(ws) else ws[i1]["e"] + 0.2
            # the cut covers the words and half of the pauses around them
            c["s"] = round((prev_e + ws[i0]["s"]) / 2, 3); c["e"] = round((ws[i1]["e"] + next_s) / 2, 3)
        report.append({"cut": c["text"], "src": sid, "score": round(m[3], 2) if m else 0,
                       "found": " ".join(w["w"] for w in ws[m[0]:m[1] + 1]) if m else None, "new": (c["s"], c["e"])})
        low += (not m or m[3] < 0.6)
    out = a.out or a.spec
    if out == a.spec:
        open(a.spec + ".bak", "w").write(open(a.spec).read())
    json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
    for r in report:
        print(json.dumps(r, ensure_ascii=False))
    print(json.dumps({"status": "SNAPPED" if not low else "CHECK", "low_scores": low, "out": out}))

if __name__ == "__main__":
    main()
