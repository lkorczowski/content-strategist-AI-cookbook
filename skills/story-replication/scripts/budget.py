#!/usr/bin/env python3
"""Word and cue budget per block for a replicated script (story-replication, step 0).

Usage: python3 -I budget.py <source_case_dir> [target_words=7000] [source_wpm=auto] [cue_factor=0.6]

Why: a replication keeps each block's share of runtime. The source mixes narration (spoken at its narrator's pace)
and third-party clips. A replication without footage turns clips into shorter cards (cue_factor x clip time) and
moves the rest of the clip time into narration (retellings). This tool gives, per block, the narration words and
the cue seconds that keep the block shares of the source.
source_wpm=auto computes the narrator's pace from stats.json (narration words / narration seconds).
"""
import json, os, sys

case = sys.argv[1]
W = float(sys.argv[2]) if len(sys.argv) > 2 else 7000.0
s = json.load(open(os.path.join(case, 'work/stats.json')))
if len(sys.argv) > 3 and sys.argv[3] != 'auto':
    wpm = float(sys.argv[3])
else:
    wpm = s['nar_words_total'] / (s['runtime_s'] * s['track_share']['NAR'] / 60)
k = float(sys.argv[4]) if len(sys.argv) > 4 else 0.6
wps = wpm / 60
q = {b['blk']: round(k * b['dur_s'] * b['clip_share']) for b in s['blocks']}
T = W / wps + sum(q.values())
print(f"source narrator pace {wpm:.0f} wpm, cue factor {k}, target narration {W:.0f} words, runtime at that pace {T/60:.1f} min")
print('| block | beat | source words | target words | cue seconds |\n|---|---|---|---|---|')
tot = 0
for b in s['blocks']:
    t = b['dur_s'] * T / s['runtime_s']
    w = max(0, (t - q[b['blk']]) * wps); tot += w
    print(f"| {b['blk']} | {b['beat']} | {b['nar_words']} | {w:.0f} | {q[b['blk']]} |")
print(f"| total | | {s['nar_words_total']} | {tot:.0f} | {sum(q.values())} |")
