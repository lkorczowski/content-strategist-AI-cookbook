#!/usr/bin/env python3
"""Turn one short-video transcript into units and an empty map, so every annotator starts from the same units.

Usage: python3 -I short_units.py <transcript.txt> <video_dir>

Input: a transcript file with a header block ("key: value" lines, the first line may start with "#") followed by
cue lines "[mm:ss.s] text" (caption cues, as written by the acquisition step; see references/acquisition.md).
Output in <video_dir>:
  meta.json            header fields (url, date, duration_s, views, likes, comments, shares, saves, caption, track)
  work/units-asr.tsv   id, start, end, track, words, text   (format read by scripts/analyze.py)
  02-map.md            the map table with ids, times and incipits filled and every tag column set to "?"

Units: cue words get times spread evenly over their cue; the text is split into sentences at . ? ! (and at a
quote-closing mark after them). A sentence over 28 words is split at the cue boundary closest to its middle.
Captions without punctuation fall back to cue boundaries: one cue per unit, cues under 5 words joined to the next.
"""
import json, os, re, sys

src, out = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(out, 'work'), exist_ok=True)
meta, cues = {}, []
for raw in open(src, encoding='utf-8'):
    line = raw.rstrip('\n')
    m = re.match(r'^\[(\d+):(\d+(?:\.\d+)?)\]\s*(.*)$', line)
    if m:
        cues.append((int(m.group(1)) * 60 + float(m.group(2)), m.group(3).strip()))
        continue
    if line.startswith('#'):
        meta['title'] = line.lstrip('# ').strip(); continue
    m = re.match(r'^([a-z_]+):\s*(.*)$', line)
    if m and not cues:
        k, v = m.group(1), m.group(2)
        if k == 'views' and '|' in v:
            first, *rest = v.split('|')
            meta['views'] = first.strip()
            for part in rest:
                kk, _, vv = part.strip().partition(':')
                meta[kk.strip()] = vv.strip()
        else:
            meta[k] = v
dur = float(meta.get('duration_s') or (cues[-1][0] + 3 if cues else 0))
json.dump(meta, open(os.path.join(out, 'meta.json'), 'w'), indent=1, ensure_ascii=False)

# word list with times and cue boundaries
words = []
for i, (t, txt) in enumerate(cues):
    t2 = cues[i + 1][0] if i + 1 < len(cues) else dur
    ws = txt.split()
    for j, w in enumerate(ws):
        words.append({'w': w, 't': t + (t2 - t) * j / max(1, len(ws)), 'cue_start': j == 0})
punct = sum(1 for w in words if re.search(r'[.?!]["”\')]*$', w['w']))
units, cur = [], []
def push():
    if cur: units.append(list(cur)); cur.clear()
for k, w in enumerate(words):
    cur.append(w)
    if punct >= max(3, len(words) // 60):
        if re.search(r'[.?!]["”\')]*$', w['w']): push()
    else:
        nxt = words[k + 1] if k + 1 < len(words) else None
        if len(cur) >= 5 and (nxt is None or nxt['cue_start']): push()
push()
final = []
for u in units:
    if len(u) <= 28:
        final.append(u); continue
    cut = min((i for i in range(8, len(u) - 8) if u[i]['cue_start']), key=lambda i: abs(i - len(u) / 2), default=len(u) // 2)
    final += [u[:cut], u[cut:]]
fmt = lambda s: f"{int(s)//60:02d}:{int(s)%60:02d}"
with open(os.path.join(out, 'work/units-asr.tsv'), 'w', encoding='utf-8') as f:
    f.write('id\tstart\tend\ttrack\twords\ttext\n')
    for i, u in enumerate(final, 1):
        end = final[i][0]['t'] if i < len(final) else dur
        f.write(f"U{i:03d}\t{fmt(u[0]['t'])}\t{fmt(end)}\tNAR\t{len(u)}\t{' '.join(x['w'] for x in u)}\n")
with open(os.path.join(out, '02-map.md'), 'w', encoding='utf-8') as f:
    f.write(f"# {meta.get('title', os.path.basename(out))} · unit map\n\n")
    f.write('Columns as in taxonomy.md (plus `beat` from taxonomy-short.md in 01-blocks.md). Replace every "?".\n\n')
    f.write('| id | t | blk | trk | thr | fn | fn2 | fig | psy | obj | T | loop | cx | incipit | gloss |\n')
    f.write('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n')
    for i, u in enumerate(final, 1):
        inc = ' '.join(x['w'] for x in u[:8]).replace('|', '/')
        f.write(f"| U{i:03d} | {fmt(u[0]['t'])} | ? | NAR | ? | ? | ? | ? | ? | ? | ? | ? | ? | {inc} | ? |\n")
print(f"{len(cues)} cues, {len(words)} words, punctuation marks {punct}, {len(final)} units, duration {dur:.0f}s, {len(words) / max(1, dur) * 60:.0f} wpm")
