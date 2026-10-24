#!/usr/bin/env python3
"""Draw the case diagrams as theme-aware SVG (CSS variables, no fonts embedded).

Usage: python3 -I draw.py <case_dir> <runtime_seconds>
Reads  : 01-blocks.md, 02-map.md, 03-loops.md, 05-graph.json, 06-fiche.json
         (05-graph.json: threads, nodes, edges, chronology and optional real_order, see references/fiche-schema.md)
Writes : work/braid.svg, work/graph.svg, work/chrono.svg, work/radar.svg

CSS variables expected on the host page: --ink --muted --grid --band --card --line
--accent --accent2 --s --l --a --h --x (one color per thread).
"""
import json, math, os, re, sys, html

case, RUNTIME = sys.argv[1], int(sys.argv[2])
esc = lambda s: html.escape(str(s), quote=True)

def secs(t):
    m, s = t.strip().split(':'); return int(m) * 60 + int(s)

def table(path, idpat):
    rows, header = [], None
    for line in open(os.path.join(case, path), encoding='utf-8'):
        if not line.startswith('|'): continue
        c = [x.strip() for x in line.strip().strip('|').split('|')]
        if header is None and c and c[0] in ('blk', 'id'): header = c; continue
        if header and re.match(idpat, c[0]): rows.append(dict(zip(header, c)))
    return rows

blocks = table('01-blocks.md', r'^B\d\d')
units = table('02-map.md', r'^[UCS]\d')
loops = table('03-loops.md', r'^L\d\d')
graph = json.load(open(os.path.join(case, '05-graph.json'), encoding='utf-8'))
fiche = json.load(open(os.path.join(case, '06-fiche.json'), encoding='utf-8'))
for u in units: u['s'] = secs(u['t'])
units.sort(key=lambda u: u['s'])
for i, u in enumerate(units): u['e'] = units[i + 1]['s'] if i + 1 < len(units) else RUNTIME
for b in blocks: b['s'], b['e'] = secs(b['start']), secs(b['end'])
TH = {'S': 'var(--s)', 'L': 'var(--l)', 'A': 'var(--a)', 'H': 'var(--h)', 'X': 'var(--x)'}
NAMES = {'S': 'Story', 'L': 'Lesson', 'A': 'Audience', 'H': 'Host', 'X': 'Channel'}
out = lambda name, svg: open(os.path.join(case, 'work', name), 'w', encoding='utf-8').write(svg)

# ---------------- braid: lanes over time + loop arcs ----------------
W, LEFT, RIGHT = 1000, 118, 12
lanes = ['S', 'L', 'A', 'H', 'X']
TOP = 150
lane_y = {k: TOP + i * 34 for i, k in enumerate(lanes)}
H = TOP + 34 * len(lanes) + 46
x = lambda t: LEFT + (W - LEFT - RIGHT) * t / RUNTIME
p = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Braid of narrative threads over time, with loop arcs">']
for i, b in enumerate(blocks):
    if i % 2 == 0:
        p.append(f'<rect x="{x(b["s"]):.1f}" y="{TOP-18}" width="{x(b["e"])-x(b["s"]):.1f}" height="{34*len(lanes)+4}" fill="var(--band)"/>')
    p.append(f'<text x="{(x(b["s"])+x(b["e"]))/2:.1f}" y="{TOP+34*len(lanes)+2}" font-size="9" text-anchor="middle" fill="var(--muted)">{b["blk"][1:]}</text>')
for m in range(0, RUNTIME // 60 + 1, 5):
    p.append(f'<text x="{x(m*60):.1f}" y="{H-8}" font-size="9" text-anchor="middle" fill="var(--muted)">{m} min</text>')
share = {k: graph.get('threads', {}).get(k, {'share': 0, 'objectives': []}) for k in lanes}
for k in lanes:
    y = lane_y[k]
    p.append(f'<line x1="{LEFT}" x2="{W-RIGHT}" y1="{y}" y2="{y}" stroke="var(--grid)"/>')
    p.append(f'<text x="{LEFT-8}" y="{y-2}" font-size="11" text-anchor="end" fill="var(--ink)" font-weight="600">{NAMES[k]}</text>')
    p.append(f'<text x="{LEFT-8}" y="{y+10}" font-size="9" text-anchor="end" fill="var(--muted)">{share[k]["share"]:.0%} · {"/".join(share[k]["objectives"][:2])}</text>')
for u in units:
    k = u['thr'].split(',')[0]; T = int(u['T']); hgt = 4 + T * 3.2
    p.append(f'<rect x="{x(u["s"]):.1f}" y="{lane_y[k]-hgt/2:.1f}" width="{max(1.2, x(u["e"])-x(u["s"])-0.4):.1f}" height="{hgt:.1f}" rx="1.5" fill="{TH[k]}"><title>{esc(u["id"])} {esc(u["t"])} {esc(u["fn"])}: {esc(u["gloss"])}</title></rect>')
# loop arcs above the lanes
for L in loops:
    o = secs(L['open_t']); c = secs(L['close_t']) if L['close_t'] != '-' else RUNTIME
    if L['scale'] == 'MICRO': continue
    x1, x2 = x(o), x(c); hgt = min(118, 18 + (c - o) / RUNTIME * 120)
    col = 'var(--accent)' if L['scale'] == 'MASTER' else 'var(--muted)'
    sw = 2 if L['scale'] == 'MASTER' else 1
    dash = ' stroke-dasharray="4 3"' if L['close_t'] == '-' else ''
    p.append(f'<path d="M{x1:.1f},{TOP-20} C{x1:.1f},{TOP-20-hgt:.1f} {x2:.1f},{TOP-20-hgt:.1f} {x2:.1f},{TOP-20}" fill="none" stroke="{col}" stroke-width="{sw}"{dash}><title>{esc(L["id"])}: {esc(L["description"])}</title></path>')
    if L['scale'] == 'MASTER':
        p.append(f'<text x="{(x1+x2)/2:.1f}" y="{TOP-20-hgt*0.75-3:.1f}" font-size="9" text-anchor="middle" fill="var(--accent)">{esc(L["id"])}</text>')
p.append(f'<text x="{LEFT}" y="14" font-size="11" fill="var(--ink)">Loops: arcs from opening to closing (bold = master loops, dashed = left open). Bars: one per unit, height = tension.</text>')
p.append('</svg>')
out('braid.svg', ''.join(p))

# ---------------- graph: story column vs lesson column, y = screen time ----------------
W2, H2 = 1000, 980
colx = {'S': 110, 'R': 600}
NW = {'S': 330, 'R': 372}
ytime = lambda t: 70 + (H2 - 120) * secs(t) / RUNTIME
nodes = [n for n in graph['nodes'] if n['thr'] != 'X']
pos = {}
for col in ('S', 'R'):
    ns = sorted([n for n in nodes if (n['thr'] == 'S') == (col == 'S')], key=lambda n: secs(n['t']))
    last = -99
    for n in ns:
        y = max(ytime(n['t']), last + 44)
        pos[n['id']] = (colx[col], y, NW[col]); last = y
g = [f'<svg viewBox="0 0 {W2} {H2}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Narrative graph: story episodes on the left, lessons on the right, edges show which story beat proves which lesson">']
g.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--line)"/></marker>'
         '<marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--accent)"/></marker></defs>')
story_obj = ', '.join(share['S']['objectives'][:3])
rest_share = sum(share[k]['share'] for k in ('L', 'A', 'H'))
g.append(f'<text x="{colx["S"]}" y="30" font-size="13" font-weight="700" fill="var(--s)">STORY BRANCH ({share["S"]["share"]:.0%} of runtime){" · " + story_obj if story_obj else ""}</text>')
g.append(f'<text x="{colx["R"]}" y="30" font-size="13" font-weight="700" fill="var(--l)">LESSON + AUDIENCE + HOST BRANCHES ({rest_share:.0%})</text>')
g.append(f'<text x="{colx["S"]}" y="48" font-size="10" fill="var(--muted)">Vertical axis = screen time, top to bottom. Small grey text = when it really happened.</text>')
for m in range(0, RUNTIME // 60 + 1, 5):
    y = ytime(f'{m}:00')
    g.append(f'<line x1="505" x2="535" y1="{y:.1f}" y2="{y:.1f}" stroke="var(--grid)"/><text x="520" y="{y-3:.1f}" font-size="9" text-anchor="middle" fill="var(--muted)">{m}\'</text>')
def anchor(nid, side):
    x0, y0, w = pos[nid]; return (x0 + (w if side == 'r' else 0), y0 + 17)
for e in graph['edges']:
    a, b = e['from'], e['to']
    if a not in pos or b not in pos: continue
    if e['type'] == 'proves' or e['type'] == 'leads':
        (x1, y1), (x2, y2) = anchor(a, 'r'), anchor(b, 'l')
        if pos[a][0] > pos[b][0]: (x1, y1), (x2, y2) = anchor(a, 'l'), anchor(b, 'r')
        mx = (x1 + x2) / 2
        g.append(f'<path d="M{x1:.1f},{y1:.1f} C{mx:.1f},{y1:.1f} {mx:.1f},{y2:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="var(--line)" stroke-width="1.2" marker-end="url(#ar)"/>')
        g.append(f'<text x="{mx:.1f}" y="{(y1+y2)/2-4:.1f}" font-size="8.5" text-anchor="middle" fill="var(--muted)">{esc(e["note"])}</text>')
    else:  # pays: arc on the outer left side of the story column
        (x1, y1), (x2, y2) = anchor(a, 'l'), anchor(b, 'l')
        bend = 10 + abs(y1 - y2) * 0.05
        g.append(f'<path d="M{x1:.1f},{y1:.1f} C{x1-bend*2:.1f},{y1:.1f} {x2-bend*2:.1f},{y2:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="var(--accent)" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#ar2)"><title>{esc(e["note"])}</title></path>')
for n in nodes:
    x0, y0, w = pos[n['id']]
    col = TH[n['thr']]
    g.append(f'<rect x="{x0}" y="{y0:.1f}" width="{w}" height="34" rx="6" fill="var(--card)" stroke="{col}" stroke-width="1.5"/>')
    g.append(f'<rect x="{x0}" y="{y0:.1f}" width="5" height="34" rx="2" fill="{col}"/>')
    g.append(f'<text x="{x0+12}" y="{y0+14:.1f}" font-size="11" font-weight="600" fill="var(--ink)">{esc(n["t"])} {esc(n["label"])}</text>')
    sub = ('real: ' + n['when'] + ' · ' if n.get('when') else NAMES[n['thr']] + ' · ') + ' '.join(n['obj'])
    g.append(f'<text x="{x0+12}" y="{y0+27:.1f}" font-size="9" fill="var(--muted)">{esc(sub)}</text>')
g.append(f'<text x="{colx["S"]}" y="{H2-14}" font-size="10" fill="var(--accent)">Dashed arcs = payoffs that jump back in screen time to the plant they pay.</text>')
g.append('</svg>')
out('graph.svg', ''.join(g))

# ---------------- chrono: order told vs real order ----------------
ch = graph['chronology']
# real_order: the distinct 'real' values of the chronology, in the order the events happened.
# Without it, keep the order of first appearance (no crossing lines).
real_order = graph.get('real_order') or list(dict.fromkeys(r['real'] for r in ch))
real_order = list(dict.fromkeys(list(real_order) + [r['real'] for r in ch]))
W3, H3 = 1000, 210
c = [f'<svg viewBox="0 0 {W3} {H3}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Order in which events are told versus the order in which they happened">']
c.append('<text x="20" y="34" font-size="11" font-weight="600" fill="var(--ink)">Told</text><text x="20" y="178" font-size="11" font-weight="600" fill="var(--ink)">Happened</text>')
xs = lambda i, n: 130 + i * (W3 - 230) / max(1, n - 1)
for i, r in enumerate(ch):
    xt = xs(i, len(ch)); xr = xs(real_order.index(r['real']), len(real_order))
    c.append(f'<line x1="{xt:.1f}" y1="52" x2="{xr:.1f}" y2="150" stroke="var(--accent)" stroke-width="1.4" opacity="0.8"/>')
for i, r in enumerate(ch):
    xt = xs(i, len(ch))
    c.append(f'<circle cx="{xt:.1f}" cy="46" r="6" fill="var(--s)"/><text x="{xt:.1f}" y="24" font-size="9" text-anchor="middle" fill="var(--ink)">{esc(r.get("short", r["label"]))}</text>')
for i, rr in enumerate(real_order):
    xr = xs(i, len(real_order))
    c.append(f'<circle cx="{xr:.1f}" cy="156" r="6" fill="var(--l)"/><text x="{xr:.1f}" y="178" font-size="10" text-anchor="middle" fill="var(--muted)">{esc(rr)}</text>')
c.append('<text x="110" y="200" font-size="9" fill="var(--muted)">Crossing lines = non-linear telling: events told in a different order from the one in which they happened.</text>')
c.append('</svg>')
out('chrono.svg', ''.join(c))

# ---------------- radar ----------------
ab = fiche['abilities']; n = len(ab)
W4, H4 = 560, 440; cx, cy, R = W4 / 2, H4 / 2 + 4, 150
pt = lambda i, v: (cx + R * v / 20 * math.sin(2 * math.pi * i / n), cy - R * v / 20 * math.cos(2 * math.pi * i / n))
r = [f'<svg viewBox="0 0 {W4} {H4}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Ability scores out of 20">']
for ring in (5, 10, 15, 20):
    pts = ' '.join(f'{pt(i, ring)[0]:.1f},{pt(i, ring)[1]:.1f}' for i in range(n))
    r.append(f'<polygon points="{pts}" fill="none" stroke="var(--grid)"/>')
    r.append(f'<text x="{cx+3}" y="{cy - R*ring/20 + 10:.1f}" font-size="8" fill="var(--muted)">{ring}</text>')
for i, a in enumerate(ab):
    x2, y2 = pt(i, 20); r.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="var(--grid)"/>')
    lx, ly = pt(i, 23.4)
    anchor_ = 'middle' if abs(lx - cx) < 20 else ('start' if lx > cx else 'end')
    r.append(f'<text x="{lx:.1f}" y="{ly+4:.1f}" font-size="11" font-weight="600" text-anchor="{anchor_}" fill="var(--ink)">{esc(a["name"])} {a["score"]}</text>')
pts = ' '.join(f'{pt(i, a["score"])[0]:.1f},{pt(i, a["score"])[1]:.1f}' for i, a in enumerate(ab))
r.append(f'<polygon points="{pts}" fill="var(--accent)" fill-opacity="0.22" stroke="var(--accent)" stroke-width="2"/>')
for i, a in enumerate(ab):
    x2, y2 = pt(i, a['score']); r.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="3.5" fill="var(--accent)"/>')
r.append('</svg>')
out('radar.svg', ''.join(r))
print('ok', [f for f in os.listdir(os.path.join(case, 'work')) if f.endswith('.svg')])
