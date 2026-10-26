#!/usr/bin/env python3
"""Assemble the Fiche (character-sheet style analysis page) as one self-contained HTML file.

Usage: python3 -I build_fiche.py <case_dir> <out_html>
Reads  : 06-fiche.json, work/stats.json, 01-blocks.md, 03-loops.md, 05-graph.json (thread labels),
         07-seed.yaml (optional, to count moves), work/{graph,braid,chrono,radar,tension,loops}.svg
The SVGs use CSS variables (see scripts/draw.py); this page defines them for light and dark themes.
Page title, eyebrow and the explanatory notes come from 06-fiche.json (page_title, eyebrow, notes) or stay generic.
"""
import json, os, re, sys, html

case, out = sys.argv[1], sys.argv[2]
E = lambda s: html.escape(str(s), quote=True)
J = lambda f: json.load(open(os.path.join(case, f), encoding='utf-8'))
fiche, st = J('06-fiche.json'), J('work/stats.json')
graph = J('05-graph.json') if os.path.exists(os.path.join(case, '05-graph.json')) else {}
svg = {k: open(os.path.join(case, 'work', k + '.svg'), encoding='utf-8').read() for k in ('graph', 'braid', 'chrono', 'radar', 'tension', 'loops')}
notes = fiche.get('notes', {})
page_title = fiche.get('page_title') or 'Story Fiche'
eyebrow = fiche.get('eyebrow') or 'FICHE · STORY ANALYSIS'

def table(path, idpat):
    rows, header = [], None
    for line in open(os.path.join(case, path), encoding='utf-8'):
        if not line.startswith('|'): continue
        c = [x.strip() for x in line.strip().strip('|').split('|')]
        if header is None and c and c[0] in ('blk', 'id'): header = c; continue
        if header and re.match(idpat, c[0]): rows.append(dict(zip(header, c)))
    return rows
blocks = {b['blk']: b for b in table('01-blocks.md', r'^B\d\d')}
loops = table('03-loops.md', r'^L\d\d')

idt = fiche['identity']; plat = idt.get('platforms', {}); yt = plat.get('youtube', {}); tt = plat.get('tiktok', {})
mod = lambda s: f"{'+' if (s - 10) // 2 >= 0 else ''}{(s - 10) // 2}"
fmt = lambda s: f"{int(s)//60}:{int(s)%60:02d}"
runtime_min = round(idt['runtime_s'] / 60)
published = yt.get('published') or tt.get('published') or ''
byline = ' · '.join(x for x in [E(idt.get('creator', '')), f'published {E(published)}' if published else '',
                                  f'runtime {fmt(idt["runtime_s"])}', E(idt.get('format', ''))] if x)
chips = []
if yt.get('views_d7'):
    chips.append(f"YouTube {yt['views_d7']:,} views in 7 days")
    if yt.get('subscribers'): chips.append(f"{yt['views_d7'] / yt['subscribers']:.1f}× subscribers")
if tt.get('plays_d7'):
    chips.append(f"TikTok {tt['plays_d7']:,} plays in 7 days")
    if tt.get('likes'): chips.append(f"{tt['likes'] / tt['plays_d7'] * 100:.1f}% likes per play")
    if tt.get('saves'): chips.append(f"{tt['saves']:,} saves")
chips_html = ''.join(f'<span class="chip">{E(c)}</span>' for c in chips)
NAMES = {'S': 'Story', 'L': 'Lesson', 'A': 'Audience', 'H': 'Host'}
thr = graph.get('threads', {})
legend = ''.join(f'<span><i style="background:var(--{k.lower()})"></i>{E(thr.get(k, {}).get("label", NAMES[k]))}</span>' for k in ('S', 'L', 'A', 'H'))
seed_path = os.path.join(case, '07-seed.yaml')
n_moves = sum(1 for line in open(seed_path, encoding='utf-8') if re.match(r'\s+- \[', line)) if os.path.exists(seed_path) else 0
clip_pct = st['track_share'].get('CLIP', 0) * 100
structure_note = notes.get('structure') or ('Story beats sit on the left in screen-time order, lessons on the right. Each grey arrow shows which story beat proves which lesson. '
                                            'The dashed arcs jump back up: a later moment pays a plant set earlier in the video.')
braid_note = notes.get('braid') or (f"The longest stretch without a story unit lasts {fmt(st['longest_without_story_s'])}, from {st['longest_without_story_from']}. "
                                    'Check what carries it (host lane, memes, numbered signposts): it is the riskiest stretch of the video.')
edit_note = notes.get('edit') or ('A talking-head version keeps the structure and loses the proof shots, '
                                  'so every clip needs a precise retelling or a quote on screen.')
method_note = notes.get('method') or 'Files: the case folder (map, loops, blocks, stats, graph, seed). Third-party transcript kept private, for analysis only.'

abil = ''.join(f'''<div class="ab"><div class="ab-name">{E(a["name"])}</div><div class="ab-score">{a["score"]}</div><div class="ab-mod">{mod(a["score"])}</div><p class="ab-ev">{E(a["evidence"])}</p></div>''' for a in fiche['abilities'])
custom = ''.join(f'<tr><td>{E(x["name"])}</td><td class="mono">{E(x["formula"])}</td><td class="num">{x["score"]}</td></tr>' for x in fiche['custom_axes_example']['axes'])
feats = ''.join(f'<li><h4>{E(f["name"])}</h4><p>{E(f["how"])}</p><p class="where mono">{E(f["where"])}</p></li>' for f in fiche['feats'])
equip = ''.join(f'<li>{E(x)}</li>' for x in fiche['equipment'])
flaws = ''.join(f'<li>{E(x)}</li>' for x in fiche['flaws'])
signals = ''.join(f'<li>{E(x)}</li>' for x in fiche['audience_signals'])
beat_rows = ''
for b in st['blocks']:
    job = blocks.get(b['blk'], {}).get('job', '')
    beat_rows += (f'<tr><td class="mono">{b["blk"]}</td><td class="mono">{b["start"]}</td><td class="num">{b["share"]*100:.1f}%</td>'
                  f'<td><span class="beat">{E(b["beat"])}</span></td><td><strong>{E(b["title"])}</strong><br><span class="job">{E(job)}</span></td>'
                  f'<td class="num">{b["nar_words"]}</td><td class="num">{b["clip_share"]*100:.0f}%</td><td class="num">{b["T_mean"]}</td></tr>')
loop_rows = ''.join(f'<tr><td class="mono">{E(L["id"])}</td><td class="mono">{E(L["open_t"])}</td><td class="mono">{E(L["close_t"])}</td><td>{E(L["scale"])}</td><td>{E(L["description"])}</td></tr>' for L in loops if L['scale'] in ('MASTER', 'OPEN'))
def bars(d, n=12):
    items = list(d.items())[:n]
    if not items: return ''
    mx = max(v for _, v in items)
    return ''.join(f'<div class="bar"><span class="bar-l mono">{E(k)}</span><span class="bar-t"><span class="bar-f" style="width:{v/mx*100:.0f}%"></span></span><span class="bar-v num">{v}</span></div>' for k, v in items)
dens = st['density_per_10min']
vital = [
    ('Open loops at any time', f"{st['loops']['mean_load']:.1f} on average, never under {st['loops']['min_load_after_60s']} after minute 1"),
    ('Loops opened', f"{st['loops']['count']} ({dens['loops_opened']} per 10 min), {st['loops']['left_open']} left open on purpose"),
    ('Longest loop', fmt(st['loops']['max_lifetime_s'])),
    ('Thread switches', f"{st['thread_switches']} ({st['thread_switches_per_10min']} per 10 min)"),
    ('Story share of runtime', f"{st['thread_share'].get('S',0)*100:.0f}%"),
    ('Clips share of runtime', f"{clip_pct:.0f}%"),
    ('Humor', f"{dens['humor_units']} tagged units per 10 min" + (f", about one every {600/dens['humor_units']:.0f} s" if dens['humor_units'] else '')),
    ('Tension', f"mean {st['tension']['mean']} / 5, {st['tension']['share_ge4']*100:.0f}% of time at 4 or 5"),
    ('Causal links', f"{st['causal_link_ratio']*100:.0f}% of sentence links are but / therefore"),
    ('Narration', f"{st['nar_words_total']:,} words ({idt.get('language', '')}, ASR count)"),
]
vital_html = ''.join(f'<div class="vs"><dt>{E(k)}</dt><dd>{E(v)}</dd></div>' for k, v in vital)

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(page_title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya+SC:wght@500;700;800&family=Alegreya+Sans:ital,wght@0,400;0,500;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: a role-playing character sheet. Boxed fields on paper, ability scores in a column, one violet accent. */
:root {{
  --bg: #f4f4f6; --paper: #ffffff; --ink: #17151f; --muted: #6b6878; --rule: #cfcdd8; --grid: #e2e0ea; --band: #f0eef6;
  --card: #ffffff; --line: #8b8799; --accent: #5a3cc4; --accent2: #b07d1e;
  --s: #c2410c; --l: #1d4ed8; --a: #2f7d32; --h: #9333ea; --x: #8b8799;
  --f-display: "Alegreya SC", "Palatino Linotype", Georgia, serif;
  --f-body: "Alegreya Sans", "Gill Sans", "Segoe UI", sans-serif;
  --f-mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #121118; --paper: #1b1a23; --ink: #ecebf2; --muted: #a3a0b2; --rule: #3a3848; --grid: #2c2a38; --band: #201f2a;
  --card: #1f1e28; --line: #8d899f; --accent: #a58bff; --accent2: #e0b458;
  --s: #fb8a4c; --l: #79a7ff; --a: #7bc47f; --h: #c58cff; --x: #8d899f; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #121118; --paper: #1b1a23; --ink: #ecebf2; --muted: #a3a0b2; --rule: #3a3848; --grid: #2c2a38; --band: #201f2a;
  --card: #1f1e28; --line: #8d899f; --accent: #a58bff; --accent2: #e0b458;
  --s: #fb8a4c; --l: #79a7ff; --a: #7bc47f; --h: #c58cff; --x: #8d899f; color-scheme: dark; }}
body {{ background: var(--bg); color: var(--ink); font-family: var(--f-body); font-size: 16px; line-height: 1.5; }}
.wrap {{ max-width: 1120px; margin: 0 auto; padding-block: 28px 64px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 22px; }}
h1, h2, h3, h4 {{ font-family: var(--f-display); text-wrap: balance; margin: 0; }}
h2 {{ font-size: 1.35rem; letter-spacing: .02em; display: flex; align-items: baseline; gap: 10px; }}
h2 small {{ font-family: var(--f-body); font-size: .85rem; color: var(--muted); letter-spacing: 0; }}
p {{ margin: 0; }}
.mono {{ font-family: var(--f-mono); font-size: .82em; }}
.num {{ font-variant-numeric: tabular-nums; text-align: right; white-space: nowrap; }}
.sheet {{ background: var(--paper); border: 1.5px solid var(--ink); border-radius: 4px; padding: 18px; display: grid; gap: 14px; min-width: 0; }}
.label {{ font-family: var(--f-display); font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }}
header.sheet {{ border-width: 2px; }}
.top {{ display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: 18px; align-items: end; }}
.eyebrow {{ font-family: var(--f-display); color: var(--accent); letter-spacing: .2em; font-size: .8rem; }}
h1 {{ font-size: clamp(1.5rem, 3.2vw, 2.25rem); line-height: 1.15; font-weight: 700; }}
.byline {{ color: var(--muted); }}
.fields {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }}
.field {{ border-bottom: 1px solid var(--rule); padding-bottom: 4px; display: grid; gap: 2px; }}
.field b {{ font-weight: 600; }}
.formula {{ border: 1px dashed var(--accent); border-radius: 4px; padding: 10px 12px; font-size: 1.05rem; }}
.formula .label {{ color: var(--accent); }}
.stats {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.chip {{ border: 1px solid var(--rule); border-radius: 999px; padding: 2px 10px; font-size: .85rem; font-variant-numeric: tabular-nums; }}
.core {{ display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 22px; align-items: start; }}
.abils {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }}
.ab {{ border: 1.5px solid var(--ink); border-radius: 10px 10px 18px 18px; padding: 10px 12px 12px; display: grid; grid-template-columns: auto 1fr; grid-template-areas: "name name" "score ev" "mod ev"; column-gap: 12px; row-gap: 2px; background: var(--card); }}
.ab-name {{ grid-area: name; font-family: var(--f-display); letter-spacing: .1em; text-transform: uppercase; font-size: .8rem; color: var(--muted); }}
.ab-score {{ grid-area: score; font-family: var(--f-display); font-size: 2.2rem; line-height: 1; font-weight: 800; text-align: center; min-width: 2.4ch; }}
.ab-mod {{ grid-area: mod; border: 1px solid var(--accent); color: var(--accent); border-radius: 999px; text-align: center; font-weight: 700; font-size: .9rem; }}
.ab-ev {{ grid-area: ev; font-size: .84rem; color: var(--muted); line-height: 1.4; }}
.radar svg {{ width: 100%; height: auto; display: block; }}
.vitals {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 8px 18px; margin: 0; }}
.vs {{ border-left: 3px solid var(--accent2); padding-left: 10px; }}
.vs dt {{ font-family: var(--f-display); font-size: .78rem; letter-spacing: .08em; color: var(--muted); text-transform: uppercase; }}
.vs dd {{ margin: 0; font-variant-numeric: tabular-nums; }}
.fig {{ overflow-x: auto; }}
.fig svg {{ display: block; width: 100%; min-width: 760px; height: auto; }}
.fig.narrow svg {{ min-width: 0; max-width: 560px; }}
.legend {{ display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: .85rem; color: var(--muted); }}
.legend i {{ display: inline-block; width: 12px; height: 12px; border-radius: 2px; vertical-align: -1px; margin-right: 6px; }}
.note {{ color: var(--muted); font-size: .9rem; max-width: 72ch; }}
table {{ border-collapse: collapse; width: 100%; font-size: .9rem; }}
th {{ text-align: left; font-family: var(--f-display); font-weight: 700; letter-spacing: .06em; font-size: .75rem; text-transform: uppercase; color: var(--muted); border-bottom: 1.5px solid var(--ink); padding: 6px 8px; }}
td {{ border-bottom: 1px solid var(--grid); padding: 7px 8px; vertical-align: top; }}
.tscroll {{ overflow-x: auto; }}
.tscroll table {{ min-width: 720px; }}
.beat {{ font-family: var(--f-mono); font-size: .72rem; border: 1px solid var(--rule); border-radius: 3px; padding: 1px 5px; white-space: nowrap; }}
.job {{ color: var(--muted); font-size: .86rem; }}
.two {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 22px; }}
.feats {{ list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }}
.feats li {{ border-top: 2px solid var(--accent); padding-top: 8px; display: grid; gap: 4px; align-content: start; }}
.feats h4 {{ font-size: 1.02rem; }}
.where {{ color: var(--muted); }}
ul.plain {{ margin: 0; padding-left: 1.1em; display: grid; gap: 6px; }}
.bars {{ display: grid; gap: 4px; }}
.bar {{ display: grid; grid-template-columns: 9.5em 1fr 2.4em; gap: 8px; align-items: center; font-size: .85rem; }}
.bar-t {{ height: 9px; background: var(--grid); border-radius: 5px; overflow: hidden; }}
.bar-f {{ display: block; height: 100%; background: var(--accent); border-radius: 5px; }}
.seed code {{ font-family: var(--f-mono); font-size: .85em; background: var(--band); padding: 1px 5px; border-radius: 3px; }}
@media (max-width: 760px) {{ .top, .core, .two {{ grid-template-columns: minmax(0, 1fr); }} .abils {{ grid-template-columns: minmax(0, 1fr); }} .fields {{ grid-template-columns: minmax(0, 1fr); }} }}
</style>
</head><body>
<div class="wrap">
<header class="sheet">
  <div class="top">
    <div style="display:grid;gap:8px;min-width:0">
      <div class="eyebrow">{E(eyebrow)}</div>
      <h1>{E(idt["title"])}</h1>
      <p class="byline">{byline}</p>
      <div class="stats">{chips_html}</div>
    </div>
    <div class="fields">
      <div class="field"><span class="label">Class</span><b>{E(fiche["class"]["name"])}</b><span class="job">{E(fiche["class"]["why"])}</span></div>
      <div class="field"><span class="label">Background</span><b>{E(fiche["background"]["name"])}</b><span class="job">{E(fiche["background"]["why"])}</span></div>
      <div class="field"><span class="label">Alignment</span><b>{E(fiche["alignment"]["name"])}</b><span class="job">{E(fiche["alignment"]["why"])}</span></div>
      <div class="field"><span class="label">Niche</span><b>{E(idt["niche"])}</b><span class="job">Language: {E(idt["language"])}</span></div>
    </div>
  </div>
  <div class="formula"><span class="label">Formula</span><br>{E(fiche["formula"])}</div>
</header>

<section class="sheet">
  <h2>Ability scores <small>out of 20, modifier as in a tabletop role-playing game</small></h2>
  <div class="core">
    <div class="abils">{abil}</div>
    <div style="display:grid;gap:14px;min-width:0">
      <div class="radar">{svg["radar"]}</div>
      <div><div class="label">Custom axes (example of a creator overlay)</div>
      <table><thead><tr><th>Axis</th><th>Formula</th><th class="num">Score</th></tr></thead><tbody>{custom}</tbody></table>
      <p class="note" style="margin-top:6px">Any creator goal can be added as a weighted mix of the eight core scores or of tag densities. The core sheet stays comparable across videos.</p></div>
    </div>
  </div>
</section>

<section class="sheet">
  <h2>Vital statistics <small>what keeps {runtime_min} minutes alive</small></h2>
  <dl class="vitals">{vital_html}</dl>
</section>

<section class="sheet">
  <h2>Narrative structure <small>story and lesson branches, braided</small></h2>
  <div class="legend">{legend}<span><i style="background:var(--accent)"></i>Payoff arcs</span></div>
  <div class="fig">{svg["graph"]}</div>
  <p class="note">{E(structure_note)}</p>
  <div class="fig">{svg["chrono"]}</div>
</section>

<section class="sheet">
  <h2>The braid over time <small>one bar per unit, height = tension</small></h2>
  <div class="fig">{svg["braid"]}</div>
  <div class="fig">{svg["tension"]}</div>
  <div class="fig">{svg["loops"]}</div>
  <p class="note">{E(braid_note)}</p>
</section>

<section class="sheet">
  <h2>Beat sheet <small>{len(st["blocks"])} blocks, durations and word budgets</small></h2>
  <div class="tscroll"><table><thead><tr><th>Block</th><th>Start</th><th class="num">Share</th><th>Beat</th><th>Title and job</th><th class="num">Words</th><th class="num">Clips</th><th class="num">T</th></tr></thead><tbody>{beat_rows}</tbody></table></div>
</section>

<section class="sheet">
  <h2>Master loops and doors left open</h2>
  <div class="tscroll"><table><thead><tr><th>Loop</th><th>Opens</th><th>Closes</th><th>Scale</th><th>What the viewer waits for</th></tr></thead><tbody>{loop_rows}</tbody></table></div>
</section>

<section class="sheet">
  <h2>Feats <small>signature techniques, reusable</small></h2>
  <ul class="feats">{feats}</ul>
</section>

<section class="sheet two">
  <div style="display:grid;gap:10px;min-width:0"><h3>Rhetorical figures</h3><div class="bars">{bars(st["figures"])}</div></div>
  <div style="display:grid;gap:10px;min-width:0"><h3>Crowd psychology</h3><div class="bars">{bars(st["psych"])}</div>
  <p class="note">GAP information gap, VICAR emotion through people on screen, AUTH authority, LOSS loss aversion, INGRP in-group, SIGNAL structure cues, TRANSPORT absorption in story, PARA bond with the host, ANTIC anticipation, VAR variable reward.</p></div>
</section>

<section class="sheet two">
  <div style="display:grid;gap:10px;min-width:0"><h3>Equipment</h3><ul class="plain">{equip}</ul>
  <h3 style="margin-top:8px">What depends on the edit</h3>
  <p>Clips carry {clip_pct:.0f}% of the runtime. {E(edit_note)}</p></div>
  <div style="display:grid;gap:10px;min-width:0"><h3>Flaws</h3><ul class="plain">{flaws}</ul>
  <h3 style="margin-top:8px">What the audience said</h3><ul class="plain">{signals}</ul></div>
</section>

<section class="sheet seed">
  <h2>Seed for replication</h2>
  <p>This Fiche ships with a machine-readable seed: <code>07-seed.yaml</code> ({len(st["blocks"])} blocks, {n_moves} moves, word budgets, loops, research and asset needs). The skill <code>statur-story-replication</code> takes it and writes a script of the same size on another subject. The analysis that produced this sheet is the skill <code>statur-story-analysis</code>.</p>
  <p class="note">{E(method_note)}</p>
</section>
</div>
</body></html>
'''
open(out, 'w', encoding='utf-8').write(page)
print('written', out, len(page))
