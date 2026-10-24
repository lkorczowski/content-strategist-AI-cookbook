#!/usr/bin/env python3
"""Compare the metrics of a replicated script with its source case (story-replication, step 5).

Usage: python3 -I parity.py <source_case_dir> <script_selfmap_dir> > 05-parity.md
Both dirs must hold work/stats.json (written by video-story-analysis/scripts/analyze.py). Prints a Markdown table with the tolerance and a verdict.
"""
import json, os, sys

a = json.load(open(os.path.join(sys.argv[1], 'work/stats.json')))
b = json.load(open(os.path.join(sys.argv[2], 'work/stats.json')))
rows = []
def add(name, va, vb, ok, tol):
    rows.append((name, va, vb, tol, 'ok' if ok else 'FIX'))

wa, wb = a['nar_words_total'], b['nar_words_total']
add('Narration words', wa, wb, abs(wb - wa) / wa <= 0.10, 'within 10%')
for k in ('S', 'L', 'A', 'H'):
    va, vb = a['thread_share'].get(k, 0), b['thread_share'].get(k, 0)
    add(f'Thread share {k}', f'{va:.0%}', f'{vb:.0%}', abs(va - vb) <= 0.07, 'within 7 points')
la, lb = a['loops']['count'], b['loops']['count']
add('Loops', la, lb, abs(lb - la) / la <= 0.20, 'within 20%')
add('Master loops', a['loops']['by_scale'].get('MASTER', 0), b['loops']['by_scale'].get('MASTER', 0),
    b['loops']['by_scale'].get('MASTER', 0) >= a['loops']['by_scale'].get('MASTER', 0) - 1, 'same, minus 1 at most')
add('Min loop load after minute 1', a['loops']['min_load_after_60s'], b['loops']['min_load_after_60s'], b['loops']['min_load_after_60s'] >= 2, 'at least 2')
ha, hb = a['density_per_10min']['humor_units'], b['density_per_10min']['humor_units']
add('Humor per 10 min', ha, hb, abs(hb - ha) / ha <= 0.25, 'within 25%')
add('But/therefore share', f"{a['causal_link_ratio']:.0%}", f"{b['causal_link_ratio']:.0%}", b['causal_link_ratio'] >= 0.5, 'at least 50%')
ba = {x['blk']: x['share'] for x in a['blocks']}; bb = {x['blk']: x['share'] for x in b['blocks']}
worst = max(((k, abs(ba[k] - bb.get(k, 0))) for k in ba), key=lambda t: t[1])
add('Block shares (worst gap)', f'{worst[0]}', f'{worst[1]*100:.1f} points', worst[1] <= 0.02, 'each within 2 points')
pa = {x['blk'] for x in a['blocks'] if x['T_max'] == 5}; pb = {x['blk'] for x in b['blocks'] if x['T_max'] == 5}
add('Blocks with a tension peak (5)', ', '.join(sorted(pa)), ', '.join(sorted(pb)), pa <= pb, 'same blocks peak')
print('| Metric | Source | Script | Tolerance | Verdict |\n|---|---|---|---|---|')
for r in rows:
    print('| ' + ' | '.join(str(x) for x in r) + ' |')
