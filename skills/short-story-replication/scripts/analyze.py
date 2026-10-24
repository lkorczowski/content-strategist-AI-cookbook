#!/usr/bin/env python3
"""Compute storytelling metrics for one case folder.

Usage: python3 -I analyze.py <case_dir> <runtime_seconds>
Reads  : 01-blocks.md, 02-map.md, 03-loops.md, work/units-asr.tsv (optional, for word counts)
Writes : work/stats.json, 04-stats.md, work/tension.svg, work/loops.svg

All tables are Markdown pipe tables whose first column is an id (B##, U###, C##, L##).
"""
import json, re, sys, os
from collections import Counter, defaultdict

case = sys.argv[1]
RUNTIME = int(sys.argv[2])

def secs(t):
    t = t.strip()
    if not re.match(r'^\d+:\d\d$', t):
        return None
    m, s = t.split(':'); return int(m) * 60 + int(s)

def fmt(s):
    return f"{int(s)//60:02d}:{int(s)%60:02d}"

def table(path, idpat):
    rows, header = [], None
    for line in open(os.path.join(case, path), encoding='utf-8'):
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if header is None and cells and cells[0] in ('blk', 'id'):
            header = cells; continue
        if header and re.match(idpat, cells[0]):
            rows.append(dict(zip(header, cells)))
    return rows

def split(v):
    return [] if v in ('', '-') else [x.strip() for x in v.split(',') if x.strip()]

blocks = table('01-blocks.md', r'^B\d\d')
units = table('02-map.md', r'^[UCS]\d')
loops = table('03-loops.md', r'^L\d\d')

for b in blocks:
    b['s'], b['e'] = secs(b['start']), secs(b['end'])
for u in units:
    u['s'] = secs(u['t'])
units.sort(key=lambda u: u['s'])
for i, u in enumerate(units):
    u['e'] = units[i + 1]['s'] if i + 1 < len(units) else RUNTIME
    u['dur'] = max(0, u['e'] - u['s'])
    u['T'] = int(u['T'])

# words per unit from the ASR segmentation (NAR and MEME only)
words = {}
asr = os.path.join(case, 'work/units-asr.tsv')
if os.path.exists(asr):
    for line in open(asr, encoding='utf-8'):
        p = line.rstrip('\n').split('\t')
        if p[0].startswith('U'):
            words[int(p[0][1:])] = int(p[4])
swords = {}
sasr = os.path.join(case, 'work/units-script.tsv')
if os.path.exists(sasr):
    for line in open(sasr, encoding='utf-8'):
        p = line.rstrip('\n').split('\t')
        if p[0].startswith('S') and p[0][1:].isdigit():
            swords[int(p[0][1:])] = int(p[5])
def unit_words(uid):
    ms = re.match(r'S(\d+)[a-z]?(?:-S?(\d+))?', uid)
    if ms:
        a = int(ms.group(1)); b = int(ms.group(2)) if ms.group(2) else a
        return sum(swords.get(k, 0) for k in range(a, b + 1))
    m = re.match(r'U(\d+)[a-z]?(?:-(\d+))?', uid)
    if not m: return 0
    a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
    return sum(words.get(k, 0) for k in range(a, b + 1))

stats = {'runtime_s': RUNTIME, 'units': len(units)}

# track time shares
track_time = Counter()
for u in units: track_time[u['trk']] += u['dur']
stats['track_share'] = {k: round(v / RUNTIME, 3) for k, v in track_time.most_common()}

# thread time shares (primary thread)
thread_time = Counter()
for u in units: thread_time[u['thr'].split(',')[0]] += u['dur']
stats['thread_share'] = {k: round(v / RUNTIME, 3) for k, v in thread_time.most_common()}

# thread switches among NAR/CLIP units
seq = [u['thr'].split(',')[0] for u in units if u['trk'] in ('NAR', 'CLIP', 'CARD')]
switches = sum(1 for a, b in zip(seq, seq[1:]) if a != b)
stats['thread_switches'] = switches
stats['thread_switches_per_10min'] = round(switches / (RUNTIME / 600), 1)

# longest stretch without a story-thread unit (S)
last_s, longest, longest_at = 0, 0, 0
for u in units:
    if u['thr'].split(',')[0] == 'S':
        gap = u['s'] - last_s
        if gap > longest: longest, longest_at = gap, last_s
        last_s = u['e']
if RUNTIME - last_s > longest: longest, longest_at = RUNTIME - last_s, last_s
has_story = any(u['thr'].split(',')[0] == 'S' for u in units)
stats['has_story_units'] = has_story
stats['longest_without_story_s'] = longest
stats['longest_without_story_from'] = fmt(longest_at)

# tag counts
def count(field, primary_only=False):
    c = Counter()
    for u in units:
        vals = split(u[field])
        if primary_only: vals = vals[:1]
        c.update(vals)
    return dict(c.most_common())
stats['fn_primary'] = count('fn', True)
fn_all = Counter()
for u in units: fn_all.update(split(u['fn']) + split(u['fn2']))
stats['fn_all'] = dict(fn_all.most_common())
stats['figures'] = count('fig')
stats['psych'] = count('psy')
stats['objective'] = count('obj')
stats['connectives'] = count('cx')
cx = stats['connectives']
causal = cx.get('BUT', 0) + cx.get('THEREFORE', 0) + cx.get('BECAUSE', 0) + cx.get('SO-WHAT', 0)
stats['causal_link_ratio'] = round(causal / max(1, causal + cx.get('AND', 0)), 2)

# densities per 10 minutes
per10 = lambda n: round(n / (RUNTIME / 600), 1)
def n(code): return fn_all.get(code, 0)
dens = {
  'loops_opened': per10(len(loops)),
  'questions': per10(n('QUESTION')),
  'humor_units': per10(n('HUMOR')),
  'memes': per10(sum(1 for u in units if u['trk'] == 'MEME')),
  'terms_defined': per10(n('TERM')),
  'analogies': per10(n('ANALOGY')),
  'examples': per10(n('EXAMPLE')),
  'evidence': per10(n('EVIDENCE') + n('HISTORY')),
  'stance_self_rant': per10(n('STANCE') + n('SELF') + n('RANT')),
  'payoff_callback': per10(n('PAYOFF') + n('CALLBACK')),
  'tips': per10(n('TIP')),
  'direct_address': per10(n('ADDRESS') + n('HYPO') + n('POV')),
}
stats['density_per_10min'] = dens

# loops: lifetimes and load curve
lt = []
for L in loops:
    o = secs(L['open_t']); c = secs(L['close_t']) if L['close_t'] != '-' else None
    L['o'], L['c'] = o, c
    if c is not None: lt.append(c - o)
stats['loops'] = {
    'count': len(loops), 'left_open': sum(1 for L in loops if L['c'] is None),
    'mean_lifetime_s': round(sum(lt) / len(lt)) if lt else 0,
    'max_lifetime_s': max(lt) if lt else 0,
    'by_scale': dict(Counter(L['scale'] for L in loops)),
    'by_type': dict(Counter(L['type'] for L in loops)),
}
load = []
for t in range(0, RUNTIME + 1, 10):
    load.append(sum(1 for L in loops if L['o'] <= t and (L['c'] is None or t < L['c'])))
stats['loops']['min_load_after_60s'] = min(load[6:]) if len(load) > 6 else 0
stats['loops']['mean_load'] = round(sum(load) / len(load), 2)

# tension curve, per 10 s, value of the unit playing at t
tension = []
for t in range(0, RUNTIME + 1, 10):
    cur = 0
    for u in units:
        if u['s'] <= t < u['e'] or (u['s'] <= t and u is units[-1]):
            cur = u['T']
    tension.append(cur)
stats['tension'] = {'mean': round(sum(tension) / len(tension), 2),
                    'share_ge4': round(sum(1 for x in tension if x >= 4) / len(tension), 3),
                    'peaks_5': [fmt(u['s']) for u in units if u['T'] == 5]}

# per block
pb = []
for b in blocks:
    us = [u for u in units if b['s'] <= u['s'] < b['e']]
    w = sum(unit_words(u['id']) for u in us if u['trk'] in ('NAR',))
    clip_t = sum(u['dur'] for u in us if u['trk'] in ('CLIP', 'CARD'))
    pb.append({'blk': b['blk'], 'beat': b['beat'], 'title': b['title'], 'start': b['start'], 'end': b['end'],
               'dur_s': b['e'] - b['s'], 'share': round((b['e'] - b['s']) / RUNTIME, 3),
               'units': len(us), 'nar_words': w, 'clip_share': round(clip_t / max(1, b['e'] - b['s']), 2),
               'T_mean': round(sum(u['T'] for u in us) / max(1, len(us)), 1),
               'T_max': max([u['T'] for u in us] or [0]),
               'threads': dict(Counter(u['thr'].split(',')[0] for u in us))})
stats['blocks'] = pb
stats['nar_words_total'] = sum(x['nar_words'] for x in pb)

json.dump(stats, open(os.path.join(case, 'work/stats.json'), 'w'), indent=1, ensure_ascii=False)

# ---------- SVG charts ----------
W, H, PADL, PADB = 960, 220, 40, 34
def x(t): return PADL + (W - PADL - 10) * t / RUNTIME
def svg_curve(values, step, vmax, color, title, ylab):
    pts = ' '.join(f"{x(i*step):.1f},{(H-PADB) - (H-PADB-20) * v / vmax:.1f}" for i, v in enumerate(values))
    shade = []
    for i, b in enumerate(blocks):
        if i % 2 == 0:
            shade.append(f'<rect x="{x(b["s"]):.1f}" y="20" width="{x(b["e"])-x(b["s"]):.1f}" height="{H-PADB-20}" fill="var(--band)"/>')
        shade.append(f'<text x="{(x(b["s"])+x(b["e"]))/2:.1f}" y="{H-PADB+12}" font-size="9" text-anchor="middle" fill="var(--muted)">{b["blk"][1:]}</text>')
    ticks = ''.join(f'<text x="{x(m*60):.1f}" y="{H-4}" font-size="9" text-anchor="middle" fill="var(--muted)">{m}\'</text>' for m in range(0, RUNTIME // 60 + 1, 5))
    grid = ''.join(f'<line x1="{PADL}" x2="{W-10}" y1="{(H-PADB)-(H-PADB-20)*v/vmax:.1f}" y2="{(H-PADB)-(H-PADB-20)*v/vmax:.1f}" stroke="var(--grid)"/><text x="{PADL-6}" y="{(H-PADB)-(H-PADB-20)*v/vmax+3:.1f}" font-size="9" text-anchor="end" fill="var(--muted)">{v}</text>' for v in range(0, vmax + 1))
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title}">'
            f'<text x="{PADL}" y="12" font-size="11" fill="var(--ink)">{title}</text>{"".join(shade)}{grid}'
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.6"/>{ticks}</svg>')
open(os.path.join(case, 'work/tension.svg'), 'w').write(svg_curve(tension, 10, 5, 'var(--accent)', 'Tension (0-5), every 10 s, blocks shaded', 'T'))
open(os.path.join(case, 'work/loops.svg'), 'w').write(svg_curve(load, 10, max(load) + 1, 'var(--accent2)', 'Open loops at each moment', 'n'))

# ---------- Markdown report ----------
L = []
L.append('# Case stats (generated by scripts/analyze.py, do not edit by hand)\n')
L.append(f"- Runtime {fmt(RUNTIME)}, {len(units)} units, {stats['nar_words_total']} narration words (ASR count)")
L.append(f"- Track share of time: " + ', '.join(f"{k} {v:.0%}" for k, v in stats['track_share'].items()))
L.append(f"- Thread share of time (primary): " + ', '.join(f"{k} {v:.0%}" for k, v in stats['thread_share'].items()))
L.append(f"- Thread switches: {switches} ({stats['thread_switches_per_10min']} per 10 min). Longest stretch without a story unit: {(str(longest) + ' s from ' + fmt(longest_at)) if has_story else 'the whole video (no story units)'}")
L.append(f"- Loops: {len(loops)} total, {stats['loops']['left_open']} left open, mean lifetime {stats['loops']['mean_lifetime_s']} s, max {stats['loops']['max_lifetime_s']} s, mean load {stats['loops']['mean_load']}, min load after the first minute {stats['loops']['min_load_after_60s']}")
L.append(f"- Tension: mean {stats['tension']['mean']}, share of time at 4+ {stats['tension']['share_ge4']:.0%}, peaks at 5: {', '.join(stats['tension']['peaks_5'])}")
L.append(f"- Causal links (BUT, THEREFORE, BECAUSE, SO-WHAT) vs AND: {stats['causal_link_ratio']:.0%}")
L.append('\n## Densities per 10 minutes\n')
L.append('| metric | per 10 min |\n|---|---|')
for k, v in dens.items(): L.append(f'| {k} | {v} |')
L.append('\n## Blocks\n')
L.append('| blk | beat | start | dur | share | units | NAR words | clip share | T mean | T max | threads |\n|---|---|---|---|---|---|---|---|---|---|---|')
for b in pb:
    L.append(f"| {b['blk']} | {b['beat']} | {b['start']} | {b['dur_s']} s | {b['share']:.1%} | {b['units']} | {b['nar_words']} | {b['clip_share']:.0%} | {b['T_mean']} | {b['T_max']} | {', '.join(f'{k}:{v}' for k, v in b['threads'].items())} |")
for name in ('fn_primary', 'fn_all', 'figures', 'psych', 'objective', 'connectives'):
    L.append(f'\n## {name}\n')
    L.append(', '.join(f'{k} {v}' for k, v in stats[name].items()))
open(os.path.join(case, '04-stats.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(open(os.path.join(case, '04-stats.md'), encoding='utf-8').read())
