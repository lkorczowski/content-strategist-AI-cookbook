#!/usr/bin/env python3
"""Compare a short replicated script with the author's template medians (short-story-replication, step 5).

Usage: python3 -I parity_short.py <author_case_dir> <selfmap_dir> <template_video_prefixes>
Example: python3 -I parity_short.py case-NN-<slug> script-<slug>-short/selfmap 02,05,07,11,14
Reads <author_case_dir>/work/author.json and <selfmap_dir>/{01-blocks.md, 03-loops.md, card.json, work/stats.json, work/units-asr.tsv}.
Prints a Markdown table: length, beat shares, turn position, loops, jokes, facts, second person.
The hook loop row of the parity check (opened by second 3, closed in the last 10%) is read by hand from 03-loops.md.
"""
import json, os, re, statistics as st, sys

case, sm, ids = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
A = json.load(open(os.path.join(case, 'work/author.json')))
vs = [v for v in A['videos'] if v['name'][:2] in ids]
med = lambda k: st.median([v[k] for v in vs if v.get(k) is not None])
ORDER = ['HOOK', 'FRAME', 'SETUP', 'STORY', 'TURN', 'BUILD', 'PAYOFF', 'BUTTON']
t_sh = {b: st.mean([v['beat_shares'].get(b, 0) for v in vs]) for b in ORDER}
s = json.load(open(os.path.join(sm, 'work/stats.json'))); R = s['runtime_s']; mins = R / 60
card = json.load(open(os.path.join(sm, 'card.json')))
secs = lambda t: int(t.split(':')[0]) * 60 + int(t.split(':')[1])
sh = {}
for l in open(os.path.join(sm, '01-blocks.md')):
    if l.startswith('| B'):
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        sh[c[3]] = sh.get(c[3], 0) + (secs(c[2]) - secs(c[1])) / R
loops = [l for l in open(os.path.join(sm, '03-loops.md')) if re.match(r'^\| L\d\d', l)]
text = [l.split('\t')[5] for l in open(os.path.join(sm, 'work/units-asr.tsv')).read().splitlines()[1:]]
you = sum(1 for t in text if re.search(r"\byou(r|'re|'ll|'ve)?\b", t, re.I)) / max(1, len(text))
fn = s.get('fn_all', {})
rows = []
def add(n, a, b, ok, tol): rows.append((n, a, b, tol, 'ok' if ok else 'FIX'))
add('Length (s)', med('runtime_s'), R, abs(R - med('runtime_s')) / med('runtime_s') <= 0.15, 'within 15%')
worst = max(((b, abs(sh.get(b, 0) - x)) for b, x in t_sh.items()), key=lambda t: t[1])
add('Beat shares (worst gap)', worst[0], f"{worst[1]*100:.1f} points", worst[1] <= 0.08, 'each within 8 points')
turn = secs(card['turn_t']) / R
add('Turn position', round(med('turn_share'), 2), round(turn, 2), abs(turn - med('turn_share')) <= 0.15, 'within 0.15')
for name, key, val, tol in [('Loops per minute', 'loops_per_min', len(loops) / mins, 0.3), ('Jokes per minute', 'humor_per_min', fn.get('HUMOR', 0) / mins, 0.4),
                            ('Facts per minute', 'evidence_per_min', fn.get('EVIDENCE', 0) / mins, 0.4)]:
    m = med(key); add(name, m, round(val, 2), abs(val - m) / m <= tol, f'within {int(tol*100)}%')
add('Sentences with "you"', f"{med('you_share'):.0%}", f"{you:.0%}", abs(you - med('you_share')) <= 0.10, 'within 10 points')
print('| Metric | Template median | Script | Tolerance | Verdict |\n|---|---|---|---|---|')
for r in rows: print('| ' + ' | '.join(str(x) for x in r) + ' |')
