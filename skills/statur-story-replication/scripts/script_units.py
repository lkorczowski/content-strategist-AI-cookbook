#!/usr/bin/env python3
"""Split a replicated script into timed units, for self-mapping and parity checks.

Usage: python3 -I script_units.py 03-script.md <out_dir> [words_per_minute=150]

Script conventions:
- Block headers: lines starting with "## B" followed by two digits (e.g. "## B07 · Reason 3 ...").
- Production cues on their own line in square brackets: [CLIP | ... | 8s], [CARD | ... | 4s], [MEME | ... | 2s],
  [B-ROLL | ...], [TITLE CARD | ... | 2s], [CUT TO BLACK | 2s], [RETELLING]. A trailing "| Ns" sets the cue duration
  (default 3 s for CLIP/CARD/MEME/TITLE CARD, 0 for B-ROLL and RETELLING, which play under narration).
- Fact ids [F12] and [HYPO] at the end of sentences are ignored in word counts.
- Lines starting with ">" or "#" other than block headers are notes and are ignored.

Writes <out_dir>/units-script.tsv (id, start, end, block, track, words, text) and prints per-block word counts and
the estimated runtime.
"""
import re, sys, os

src, out = sys.argv[1], sys.argv[2]
WPM = float(sys.argv[3]) if len(sys.argv) > 3 else 150.0
os.makedirs(out, exist_ok=True)
fmt = lambda s: f"{int(s)//60:02d}:{int(s)%60:02d}"
TAG = re.compile(r'\s*\[(?:F\d+(?:,\s*F\d+)*|HYPO)\]')
units, block, t = [], None, 0.0
per_block = {}
for raw in open(src, encoding='utf-8'):
    line = raw.strip()
    if not line:
        continue
    m = re.match(r'^##\s+(B\d\d)\b', line)
    if m:
        block = m.group(1); per_block.setdefault(block, [0, t, t]); continue
    if line.startswith('#') or line.startswith('>') or block is None:
        continue
    c = re.match(r'^\[([A-Z][A-Z \-]+?)(?:\s*\|(.*))?\]$', line)
    if c:
        kind = c.group(1).strip(); rest = c.group(2) or ''
        d = re.search(r'\|\s*(\d+(?:\.\d+)?)s\s*$', '|' + rest)
        dur = float(d.group(1)) if d else (3.0 if kind in ('CLIP', 'CARD', 'MEME', 'TITLE CARD', 'CUT TO BLACK') else 0.0)
        track = {'CLIP': 'CLIP', 'CARD': 'CARD', 'MEME': 'MEME', 'TITLE CARD': 'CARD', 'CUT TO BLACK': 'BREATH'}.get(kind, 'CUE')
        if kind == 'B-ROLL':
            track = 'BREATH' if 'music only' in rest.lower() else 'CARD'
        if dur > 0:
            units.append([None, t, t + dur, block, track, 0, line]); t += dur
        continue
    # narration paragraph: split into sentences
    text = TAG.sub('', line).replace('**', '')
    for s in re.split(r'(?<=[.?!])\s+(?=[A-Z"“(\[])', text):
        w = len(re.findall(r"[A-Za-z0-9$%'’\-]+", s))
        if not w: continue
        d = w / WPM * 60
        units.append([None, t, t + d, block, 'NAR', w, s]); t += d
        per_block[block][0] += w
    per_block[block][2] = t
for i, u in enumerate(units, 1):
    u[0] = f"S{i:03d}"
with open(os.path.join(out, 'units-script.tsv'), 'w', encoding='utf-8') as f:
    f.write('id\tstart\tend\tblock\ttrack\twords\ttext\n')
    for u in units:
        f.write(f"{u[0]}\t{fmt(u[1])}\t{fmt(u[2])}\t{u[3]}\t{u[4]}\t{u[5]}\t{u[6]}\n")
total = sum(v[0] for v in per_block.values())
print(f"total narration words {total}, estimated runtime {fmt(t)} at {WPM:.0f} wpm, units {len(units)}")
for b, (w, s, e) in sorted(per_block.items()):
    print(f"{b} start {fmt(s)} words {w} dur {fmt(e - s)}")
