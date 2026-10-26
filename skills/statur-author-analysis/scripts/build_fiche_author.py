#!/usr/bin/env python3
"""Assemble an author Fiche (many short videos of one creator) as one self-contained HTML page.

Usage: python3 -I build_fiche_author.py <case_dir> <out_html>
Reads  : <case_dir>/06-fiche.json (narrative fields written by the analyst) and <case_dir>/work/author.json
         (scripts/aggregate_author.py). The radar and the beat strips are drawn here as inline SVG with CSS variables.
06-fiche.json fields: title, eyebrow, creator, handle, period, class{name,why}, background{name,why},
  alignment{name,why}, formula, abilities[{code,name,evidence}], templates[{name,skeleton,share_of_videos,when,beats[[beat,share]]}],
  feats[{name,how,where}], equipment[], flaws[], custom_axes[{name,formula,score}], notes[]
"""
import html, json, math, os, sys

case, out = sys.argv[1], sys.argv[2]
E = lambda s: html.escape(str(s), quote=True)
F = json.load(open(os.path.join(case, '06-fiche.json'), encoding='utf-8'))
A = json.load(open(os.path.join(case, 'work/author.json'), encoding='utf-8'))
vids = A['videos']; sc = A['scores']
mod = lambda s: f"{'+' if (s - 10) // 2 >= 0 else ''}{int((s - 10) // 2)}"

# radar: mean polygon plus min-max band
order = ['CUR', 'WEA', 'CLA', 'AUT', 'VOI', 'HUM', 'EMO', 'PAY']
names = {a['code']: a['name'] for a in F['abilities']}
cx, cy, R = 210, 200, 150
def pt(i, v):
    ang = -math.pi / 2 + i * 2 * math.pi / len(order)
    return cx + R * v / 20 * math.cos(ang), cy + R * v / 20 * math.sin(ang)
poly = lambda vals: ' '.join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, v) for i, v in enumerate(vals)))
grid = ''.join(f'<polygon points="{poly([r]*8)}" fill="none" stroke="var(--grid)" stroke-width="1"/>' for r in (5, 10, 15, 20))
axes = ''.join(f'<line x1="{cx}" y1="{cy}" x2="{pt(i,20)[0]:.1f}" y2="{pt(i,20)[1]:.1f}" stroke="var(--grid)"/>' for i in range(8))
labels = ''
for i, c in enumerate(order):
    x, y = pt(i, 23.5); anchor = 'middle' if abs(x - cx) < 20 else ('start' if x > cx else 'end')
    labels += f'<text x="{x:.1f}" y="{y+4:.1f}" text-anchor="{anchor}" class="rl">{E(names.get(c, c))} {sc[c]["mean"]:.0f}</text>'
band_max = poly([sc[c]['max'] for c in order]); band_min = poly([sc[c]['min'] for c in order]); mean = poly([sc[c]['mean'] for c in order])
radar = (f'<svg viewBox="-70 -10 560 420" role="img" aria-label="Ability radar: mean of {len(vids)} videos with the range from lowest to highest video">'
         f'{grid}{axes}<polygon points="{band_max}" fill="var(--accent)" fill-opacity=".10" stroke="var(--accent)" stroke-opacity=".35" stroke-dasharray="3 3"/>'
         f'<polygon points="{band_min}" fill="var(--paper)" fill-opacity=".85" stroke="var(--accent)" stroke-opacity=".35" stroke-dasharray="3 3"/>'
         f'<polygon points="{mean}" fill="var(--accent)" fill-opacity=".22" stroke="var(--accent)" stroke-width="2.5"/>{labels}</svg>')

BEATC = {'HOOK': 'var(--b1)', 'FRAME': 'var(--b2)', 'SETUP': 'var(--b3)', 'STORY': 'var(--b4)', 'TURN': 'var(--b5)', 'BUILD': 'var(--b6)',
         'PAYOFF': 'var(--b7)', 'BUTTON': 'var(--b8)', 'ASIDE': 'var(--b9)', 'CTA': 'var(--b9)'}
def strip(beats):
    x, segs = 0.0, ''
    for b, s in beats:
        w = s * 600
        segs += f'<rect x="{x:.1f}" y="0" width="{max(w-1.5,1):.1f}" height="34" rx="3" fill="{BEATC.get(b, "var(--b9)")}"/>'
        if w > 46: segs += f'<text x="{x+w/2:.1f}" y="22" text-anchor="middle" class="bl">{E(b)}</text>'
        x += w
    return f'<svg viewBox="0 0 600 34" role="img" aria-label="{E(" ".join(b for b, _ in beats))}">{segs}</svg>'

abil = ''
for a in F['abilities']:
    s = sc[a['code']]
    abil += (f'<div class="ab"><div class="ab-name">{E(a["name"])}</div><div class="ab-score">{s["mean"]:.0f}</div><div class="ab-mod">{mod(round(s["mean"]))}</div>'
             f'<p class="ab-ev"><span class="mono">range {s["min"]}-{s["max"]}</span> · {E(a["evidence"])}</p></div>')
ma, mt, mr = A['medians_all'], A['medians_top'], A['medians_recent']
labels_m = {'runtime_s': 'Length (s)', 'words': 'Words', 'wpm': 'Words per minute', 'turn_share': 'Turn position (share of runtime)', 'loops_per_min': 'Loops opened per minute',
            'humor_per_min': 'Jokes per minute', 'questions_per_min': 'Questions per minute', 'evidence_per_min': 'Facts per minute', 'examples_per_min': 'Examples per minute',
            'you_share': 'Sentences with "you"', 'causal_link_ratio': 'But / therefore links', 'tension_mean': 'Mean tension (0-5)'}
med_rows = ''.join(f'<tr><td>{E(labels_m[k])}</td><td class="num">{ma[k]}</td><td class="num">{mt[k]}</td><td class="num">{mr[k]}</td></tr>' for k in labels_m)
tmpl = ''.join(f'<div class="tp"><div class="tp-h"><h4>{E(t["name"])}</h4><span class="chip">{E(t["share_of_videos"])}</span></div><div class="fig">{strip(t["beats"])}</div>'
               f'<p class="mono sk">{E(t["skeleton"])}</p><p>{E(t["when"])}</p></div>' for t in F['templates'])
def bars(pairs):
    pairs = [(k, v) for k, v in pairs if k]; mx = max((v for _, v in pairs), default=1)
    return ''.join(f'<div class="bar"><span class="bar-l mono">{E(k)}</span><span class="bar-t"><span class="bar-f" style="width:{v/mx*100:.0f}%"></span></span><span class="bar-v num">{v}</span></div>' for k, v in pairs)
feats = ''.join(f'<li><h4>{E(f["name"])}</h4><p>{E(f["how"])}</p><p class="where mono">{E(f["where"])}</p></li>' for f in F['feats'])
equip = ''.join(f'<li>{E(x)}</li>' for x in F['equipment']); flaws = ''.join(f'<li>{E(x)}</li>' for x in F['flaws'])
custom = ''.join(f'<tr><td>{E(x["name"])}</td><td class="mono">{E(x["formula"])}</td><td class="num">{x["score"]}</td></tr>' for x in F['custom_axes'])
phr = ''.join(f'<li><span class="q">{E(g)}</span> <span class="num muted">{c} videos</span></li>' for g, c in A['phrases'][:14])
vrows = ''
for v in sorted(vids, key=lambda v: v['name']):
    s = v['scores']; tot = sum(s.get(c, 0) for c in order)
    vrows += (f'<tr><td class="mono">{E(v["name"][:2])}</td><td>{E(v["topic"])}</td><td>{E(v["group"])}</td><td class="num">{v["views"]/1e6:.1f}M</td><td class="num">{v["runtime_s"]}s</td>'
              f'<td class="mono">{E(v["hook"])}</td><td class="mono">{E(v["end"])}</td><td class="num">{v["turn_share"]}</td><td class="num">{tot}</td></tr>')
notes = ''.join(f'<li>{E(x)}</li>' for x in F.get('notes', []))

page = f'''<title>{E(F["title"])}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya+SC:wght@500;700;800&family=Alegreya+Sans:ital,wght@0,400;0,500;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Author character sheet: same sheet system as the long-video Fiche, teal accent for a many-videos sheet. */
:root {{ --bg:#f3f5f4; --paper:#ffffff; --ink:#141a19; --muted:#5e6b68; --rule:#cbd5d2; --grid:#dfe7e4; --card:#ffffff; --accent:#0f766e; --accent2:#b45309;
  --b1:#0f766e; --b2:#2a9d8f; --b3:#8aa8a1; --b4:#c2410c; --b5:#7c3aed; --b6:#a78bfa; --b7:#b45309; --b8:#141a19; --b9:#cbd5d2; --bt:#ffffff;
  --f-display:"Alegreya SC","Palatino Linotype",Georgia,serif; --f-body:"Alegreya Sans","Gill Sans","Segoe UI",sans-serif; --f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#0f1312; --paper:#171d1c; --ink:#e7eeec; --muted:#9fb0ac; --rule:#33403d; --grid:#26302e; --card:#1b2221; --accent:#5eead4; --accent2:#f59e0b;
  --b1:#14b8a6; --b2:#2dd4bf; --b3:#5b7a73; --b4:#fb923c; --b5:#a78bfa; --b6:#7c5fd6; --b7:#f59e0b; --b8:#e7eeec; --b9:#33403d; --bt:#0f1312; color-scheme:dark; }} }}
:root[data-theme="dark"] {{ --bg:#0f1312; --paper:#171d1c; --ink:#e7eeec; --muted:#9fb0ac; --rule:#33403d; --grid:#26302e; --card:#1b2221; --accent:#5eead4; --accent2:#f59e0b;
  --b1:#14b8a6; --b2:#2dd4bf; --b3:#5b7a73; --b4:#fb923c; --b5:#a78bfa; --b6:#7c5fd6; --b7:#f59e0b; --b8:#e7eeec; --b9:#33403d; --bt:#0f1312; color-scheme:dark; }}
body {{ background:var(--bg); color:var(--ink); font-family:var(--f-body); font-size:16px; line-height:1.5; }}
.wrap {{ max-width:1120px; margin:0 auto; padding-block:28px 64px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); display:grid; gap:22px; }}
h1,h2,h3,h4 {{ font-family:var(--f-display); text-wrap:balance; margin:0; }} p {{ margin:0; }}
h2 {{ font-size:1.35rem; letter-spacing:.02em; display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; }} h2 small {{ font-family:var(--f-body); font-size:.85rem; color:var(--muted); }}
.mono {{ font-family:var(--f-mono); font-size:.82em; }} .num {{ font-variant-numeric:tabular-nums; text-align:right; white-space:nowrap; }} .muted {{ color:var(--muted); }}
.sheet {{ background:var(--paper); border:1.5px solid var(--ink); border-radius:4px; padding:18px; display:grid; gap:14px; min-width:0; }}
.label {{ font-family:var(--f-display); font-size:.72rem; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); }}
.top {{ display:grid; grid-template-columns:minmax(0,1.5fr) minmax(0,1fr); gap:18px; align-items:end; }}
.eyebrow {{ font-family:var(--f-display); color:var(--accent); letter-spacing:.2em; font-size:.8rem; }}
h1 {{ font-size:clamp(1.5rem,3.2vw,2.25rem); line-height:1.15; }}
.fields {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; }} .field {{ border-bottom:1px solid var(--rule); padding-bottom:4px; display:grid; gap:2px; min-width:0; }}
.formula {{ border:1px dashed var(--accent); border-radius:4px; padding:10px 12px; font-size:1.05rem; }} .formula .label {{ color:var(--accent); }}
.core {{ display:grid; grid-template-columns:minmax(0,1.25fr) minmax(0,1fr); gap:22px; align-items:start; }}
.abils {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; }}
.ab {{ border:1.5px solid var(--ink); border-radius:10px 10px 18px 18px; padding:10px 12px 12px; display:grid; grid-template-columns:auto 1fr; grid-template-areas:"name name" "score ev" "mod ev"; column-gap:12px; row-gap:2px; background:var(--card); min-width:0; }}
.ab-name {{ grid-area:name; font-family:var(--f-display); letter-spacing:.1em; text-transform:uppercase; font-size:.8rem; color:var(--muted); }}
.ab-score {{ grid-area:score; font-family:var(--f-display); font-size:2.2rem; line-height:1; font-weight:800; text-align:center; min-width:2.4ch; }}
.ab-mod {{ grid-area:mod; border:1px solid var(--accent); color:var(--accent); border-radius:999px; text-align:center; font-weight:700; font-size:.9rem; }}
.ab-ev {{ grid-area:ev; font-size:.84rem; color:var(--muted); line-height:1.4; min-width:0; }}
.radar svg {{ width:100%; height:auto; display:block; }} .rl {{ font-family:var(--f-body); font-size:12px; fill:var(--ink); }}
.legend {{ font-size:.85rem; color:var(--muted); }}
.tps {{ display:grid; gap:16px; }} .tp {{ display:grid; gap:6px; }} .tp-h {{ display:flex; gap:10px; align-items:baseline; flex-wrap:wrap; }}
.chip {{ border:1px solid var(--rule); border-radius:999px; padding:2px 10px; font-size:.85rem; }}
.fig {{ overflow-x:auto; }} .fig svg {{ display:block; width:100%; min-width:480px; height:auto; }} .bl {{ font-family:var(--f-mono); font-size:10px; fill:var(--bt); }}
.sk {{ color:var(--muted); }}
.two {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:22px; }}
.bar {{ display:grid; grid-template-columns:110px 1fr 36px; gap:8px; align-items:center; font-size:.9rem; }} .bar-t {{ height:10px; background:var(--grid); border-radius:6px; overflow:hidden; }} .bar-f {{ display:block; height:100%; background:var(--accent); }}
ul.feats {{ list-style:none; padding:0; margin:0; display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:12px; }}
ul.feats li {{ border:1px solid var(--rule); border-radius:6px; padding:10px 12px; display:grid; gap:4px; }} .where {{ color:var(--muted); }}
ul.plain {{ margin:0; padding-left:1.1em; display:grid; gap:4px; }} .q {{ font-style:italic; }}
.tbl {{ overflow-x:auto; }} table {{ border-collapse:collapse; width:100%; font-size:.9rem; }} th,td {{ border-bottom:1px solid var(--rule); padding:6px 8px; text-align:left; vertical-align:top; }} th {{ font-family:var(--f-display); font-size:.75rem; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); }}
@media (max-width:760px) {{ .top,.core,.two {{ grid-template-columns:1fr; }} .abils,.fields {{ grid-template-columns:1fr; }} }}
</style>
<div class="wrap">
<header class="sheet"><div class="top"><div style="display:grid;gap:8px;min-width:0"><div class="eyebrow">{E(F["eyebrow"])}</div><h1>{E(F["creator"])}</h1><p class="muted">{E(F["handle"])} · {E(F["period"])} · {len(vids)} videos analyzed</p></div>
<div class="fields"><div class="field"><span class="label">Class</span><b>{E(F["class"]["name"])}</b><span class="muted">{E(F["class"]["why"])}</span></div>
<div class="field"><span class="label">Background</span><b>{E(F["background"]["name"])}</b><span class="muted">{E(F["background"]["why"])}</span></div>
<div class="field"><span class="label">Alignment</span><b>{E(F["alignment"]["name"])}</b><span class="muted">{E(F["alignment"]["why"])}</span></div>
<div class="field"><span class="label">Median video</span><b>{ma["runtime_s"]:.0f} s, {ma["words"]:.0f} words</b><span class="muted">{ma["wpm"]:.0f} words per minute</span></div></div></div>
<div class="formula"><span class="label">Formula</span><p>{E(F["formula"])}</p></div></header>
<section class="sheet"><h2>Ability scores <small>mean of {len(vids)} videos, out of 20, with the range</small></h2><div class="core"><div class="abils">{abil}</div>
<div class="radar">{radar}<p class="legend">Solid shape: mean. Dashed band: lowest to highest video on each axis.</p></div></div></section>
<section class="sheet"><h2>Templates <small>beat sequences that recur across the {len(vids)} videos</small></h2><div class="tps">{tmpl}</div></section>
<section class="sheet two"><div style="display:grid;gap:10px;min-width:0"><h2>Hooks</h2>{bars(A["hooks"])}<p class="label">Top 10 only</p>{bars(A["hooks_top"])}</div>
<div style="display:grid;gap:10px;min-width:0"><h2>Endings</h2>{bars(A["ends"])}<p class="label">Top 10 only</p>{bars(A["ends_top"])}</div></section>
<section class="sheet"><h2>Vital statistics <small>medians</small></h2><div class="tbl"><table><tr><th>Measure</th><th>All {len(vids)}</th><th>Top 10</th><th>Recent 10</th></tr>{med_rows}</table></div></section>
<section class="sheet"><h2>Feats <small>signature moves you can reuse</small></h2><ul class="feats">{feats}</ul></section>
<section class="sheet two"><div style="display:grid;gap:10px;min-width:0"><h2>Recurring phrases</h2><ul class="plain">{phr}</ul></div>
<div style="display:grid;gap:10px;min-width:0"><h2>Equipment</h2><ul class="plain">{equip}</ul><h2>Flaws</h2><ul class="plain">{flaws}</ul></div></section>
<section class="sheet"><h2>Custom axes <small>weighted mixes of the core scores</small></h2><div class="tbl"><table><tr><th>Axis</th><th>Formula</th><th>Score</th></tr>{custom}</table></div></section>
<section class="sheet"><h2>The {len(vids)} videos</h2><div class="tbl"><table><tr><th>#</th><th>Topic</th><th>Group</th><th>Views</th><th>Length</th><th>Hook</th><th>End</th><th>Turn</th><th>Score /160</th></tr>{vrows}</table></div>
<ul class="plain muted">{notes}</ul></section>
</div>'''
open(out, 'w', encoding='utf-8').write(page)
print('wrote', out, len(page), 'bytes')
