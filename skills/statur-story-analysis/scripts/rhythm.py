#!/usr/bin/env python3
"""Sentence rhythm of a script or a transcript: the length of each sentence and the long runs.

Usage: python3 -I rhythm.py <units.tsv or text file> [--short 5] [--long 12] [--run 3]
Input: a units TSV with a "text" column (work/units-asr.tsv), or any plain text file.
Narration rows only when the TSV has a "track" column (NAR). Captions without punctuation: each unit counts as one sentence.
Prints: sentence count, median words, share of short sentences (<= --short words),
share of long sentences (>= 20 words), the longest run of sentences >= --long words
with no short sentence in between, and every run of --run or more long sentences to fix.
A run to fix is a passage where a short sentence would reset the ear.
"""
import re, statistics as st, sys

args = sys.argv[1:]
path = args[0]
opt = lambda k, d: int(args[args.index(k) + 1]) if k in args else d
SHORT, LONG, RUN = opt('--short', 5), opt('--long', 12), opt('--run', 3)

raw = open(path, encoding='utf-8').read()
lines = raw.splitlines()
if lines and '\t' in lines[0] and 'text' in lines[0].split('\t'):
    head = lines[0].split('\t'); ti = head.index('text'); tr = head.index('track') if 'track' in head else None
    units = [l.split('\t')[ti] for l in lines[1:] if l.count('\t') >= ti and (tr is None or l.split('\t')[tr] == 'NAR')]
    text = ' '.join(units)
else:
    units = None
    text = ' '.join(l for l in lines if not l.startswith(('#', '>', '[')))
text = re.sub(r'\[[^\]]*\]', ' ', text)
sents = [s.strip() for s in re.split(r'(?<=[.?!])["”\')]*\s+', text) if re.search(r'\w', s)]
if units and len(re.findall(r'[.?!]', text)) < len(units) / 3:
    sents = [u for u in units if re.search(r'\w', u)]  # captions without punctuation: one unit = one sentence
    print('note: few sentence marks, units used as sentences')
n = [len(s.split()) for s in sents]
if not n:
    sys.exit('no sentences found')
runs, cur = [], []
for i, k in enumerate(n):
    if k >= LONG:
        cur.append(i)
    else:
        if cur: runs.append(cur)
        cur = []
if cur: runs.append(cur)
longest = max((len(r) for r in runs), default=0)
print(f"sentences: {len(n)}")
print(f"median words: {st.median(n)}")
print(f"short (<= {SHORT} words): {sum(k <= SHORT for k in n) / len(n):.0%}")
print(f"long (>= 20 words): {sum(k >= 20 for k in n) / len(n):.0%}")
print(f"longest run of sentences >= {LONG} words: {longest}")
fix = [r for r in runs if len(r) >= RUN]
print(f"runs to fix (>= {RUN} long sentences in a row): {len(fix)}")
for r in fix:
    print(f"- sentences {r[0] + 1} to {r[-1] + 1}: \"{' '.join(sents[r[0]].split()[:8])}...\"")
