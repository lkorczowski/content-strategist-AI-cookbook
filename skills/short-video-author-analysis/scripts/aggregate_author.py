#!/usr/bin/env python3
"""Aggregate the per-video maps of one author into an author grammar (short-form videos).

Usage: python3 -I aggregate_author.py <case_dir>
Reads, for every <case_dir>/videos/<NN-id>/ folder:
  meta.json (from short_units.py), card.json (annotator's video card), 01-blocks.md, 02-map.md, 03-loops.md,
  work/units-asr.tsv, work/stats.json (from analyze.py)
card.json fields: group ("top" or "recent"), topic, hook (H-*), end (E-*), turn_t (mm:ss), one_line,
  signature_moves (list of short strings), scores ({"CUR":..,"WEA":..,"CLA":..,"HUM":..,"EMO":..,"AUT":..,"PAY":..,"VOI":..}, out of 20)
Writes: <case_dir>/work/author.json and <case_dir>/10-author-grammar.md
"""
import json, os, re, statistics as st, sys
from collections import Counter, defaultdict

case = sys.argv[1]
vdir = os.path.join(case, 'videos')
def table(path, idpat):
    rows, header = [], None
    if not os.path.exists(path): return rows
    for line in open(path, encoding='utf-8'):
        if not line.startswith('|'): continue
        c = [x.strip() for x in line.strip().strip('|').split('|')]
        if header is None and c and c[0] in ('blk', 'id'): header = c; continue
        if header and re.match(idpat, c[0]): rows.append(dict(zip(header, c)))
    return rows
def secs(t):
    m = re.match(r'^(\d+):(\d\d)$', t.strip()); return int(m.group(1)) * 60 + int(m.group(2)) if m else None
med = lambda xs: round(st.median(xs), 2) if xs else None
num = lambda v: int(re.sub(r'[^\d]', '', str(v)) or 0)

videos = []
for name in sorted(os.listdir(vdir)):
    d = os.path.join(vdir, name)
    if not os.path.isdir(d) or not os.path.exists(os.path.join(d, 'work/stats.json')): continue
    meta = json.load(open(os.path.join(d, 'meta.json'), encoding='utf-8'))
    card = json.load(open(os.path.join(d, 'card.json'), encoding='utf-8'))
    s = json.load(open(os.path.join(d, 'work/stats.json'), encoding='utf-8'))
    blocks = table(os.path.join(d, '01-blocks.md'), r'^B\d\d')
    units = table(os.path.join(d, '02-map.md'), r'^U\d')
    loops = table(os.path.join(d, '03-loops.md'), r'^L\d\d')
    text = [l.split('\t')[5] for l in open(os.path.join(d, 'work/units-asr.tsv'), encoding='utf-8').read().splitlines()[1:]]
    R = s['runtime_s']; mins = R / 60
    beats = [b['beat'] for b in blocks]
    shares = defaultdict(float)
    for b in blocks:
        shares[b['beat']] += (secs(b['end']) - secs(b['start'])) / R
    fn = Counter(s.get('fn_all', {}))
    you = sum(1 for t in text if re.search(r"\byou(r|'re|'ll|'ve)?\b", t, re.I))
    turn = secs(card.get('turn_t', '')) if card.get('turn_t') else None
    v = {
        'name': name, 'group': card.get('group'), 'topic': card.get('topic'), 'views': num(meta.get('views')),
        'date': meta.get('date'), 'runtime_s': R, 'words': s.get('nar_words_total'),
        'wpm': round(s.get('nar_words_total', 0) / mins) if mins else None,
        'beats': ' '.join(beats), 'beat_shares': {k: round(x, 3) for k, x in shares.items()},
        'hook': card.get('hook'), 'end': card.get('end'), 'turn_share': round(turn / R, 2) if turn is not None else None,
        'loops': len(loops), 'loops_per_min': round(len(loops) / mins, 2),
        'humor_per_min': round(fn.get('HUMOR', 0) / mins, 2), 'questions_per_min': round((fn.get('QUESTION', 0) + fn.get('RHETQ', 0)) / mins, 2),
        'evidence_per_min': round(fn.get('EVIDENCE', 0) / mins, 2), 'examples_per_min': round(fn.get('EXAMPLE', 0) / mins, 2),
        'you_share': round(you / max(1, len(text)), 2), 'thread_share': s.get('thread_share'),
        'causal_link_ratio': s.get('causal_link_ratio'), 'tension_mean': s.get('tension', {}).get('mean'),
        'figures': s.get('figures', {}), 'psych': s.get('psych', {}), 'scores': card.get('scores', {}),
        'signature_moves': card.get('signature_moves', []), 'one_line': card.get('one_line'), 'text': text,
    }
    videos.append(v)

def collapse(seq):
    out = []
    for x in seq.split():
        if not out or out[-1] != x: out.append(x)
    return out
def skeleton(seq):
    core = [x for x in collapse(seq) if x not in ('ASIDE', 'CTA')]
    return ' '.join(core)
ORDER = ['HOOK', 'FRAME', 'SETUP', 'STORY', 'TURN', 'BUILD', 'PAYOFF', 'BUTTON']
def core(seq):
    seen = []
    for x in seq.split():
        if x in ORDER and x not in seen: seen.append(x)
    return ' '.join(seen)
def length_class(r): return 'short (under 90 s)' if r < 90 else ('mid (90 to 240 s)' if r <= 240 else 'long (over 240 s)')
for v in videos:
    v['core'] = core(v['beats']); v['turns'] = v['beats'].split().count('TURN'); v['length_class'] = length_class(v['runtime_s'])
tmpl = Counter(skeleton(v['beats']) for v in videos)
cores = Counter(v['core'] for v in videos)
by_len = {}
for v in videos:
    by_len.setdefault(v['length_class'], []).append(v)

metrics = ['runtime_s', 'words', 'wpm', 'turn_share', 'loops_per_min', 'humor_per_min', 'questions_per_min', 'evidence_per_min', 'examples_per_min', 'you_share', 'causal_link_ratio', 'tension_mean']
def medians(vs): return {m: med([v[m] for v in vs if v.get(m) is not None]) for m in metrics}
groups = {g: [v for v in videos if v['group'] == g] for g in ('top', 'recent')}
abil = ['CUR', 'WEA', 'CLA', 'HUM', 'EMO', 'AUT', 'PAY', 'VOI']
score_stats = {a: {'mean': round(st.mean([v['scores'][a] for v in videos if a in v['scores']]), 1) if videos else None,
                   'min': min((v['scores'][a] for v in videos if a in v['scores']), default=None),
                   'max': max((v['scores'][a] for v in videos if a in v['scores']), default=None)} for a in abil}
fig_videos = Counter(); psy_videos = Counter()
for v in videos:
    fig_videos.update(k for k, c in v['figures'].items() if c); psy_videos.update(k for k, c in v['psych'].items() if c)
# signature phrases: 3- to 5-grams present in at least 4 videos
STOP = set('the a an and or of to in on is it that this i you we they he she was be for with as at but so just like'.split())
ngram_videos = defaultdict(set)
for v in videos:
    toks = re.findall(r"[a-z']+", ' '.join(v['text']).lower())
    for n in (3, 4, 5):
        for i in range(len(toks) - n + 1):
            g = toks[i:i + n]
            if sum(1 for w in g if w not in STOP) >= 1:
                ngram_videos[' '.join(g)].add(v['name'])
phr = sorted(((g, len(s)) for g, s in ngram_videos.items() if len(s) >= 4), key=lambda x: (-x[1], -len(x[0])))
seen, phrases = set(), []
for g, c in phr:
    if any(g in p for p in seen): continue
    seen.add(g); phrases.append((g, c))
    if len(phrases) >= 25: break

beat_share_med = {}
for b in ORDER:
    xs = [v['beat_shares'].get(b, 0) for v in videos]
    beat_share_med[b] = med(xs)
author = {'cores': cores.most_common(), 'beat_share_median': beat_share_med,
          'length_classes': {k: {'n': len(vs), 'median_runtime': med([x['runtime_s'] for x in vs]), 'median_turns': med([x['turns'] for x in vs]),
                                 'cores': Counter(x['core'] for x in vs).most_common(), 'medians': medians(vs)} for k, vs in by_len.items()},
          'videos': [{k: v[k] for k in v if k != 'text'} for v in videos], 'templates': tmpl.most_common(),
          'medians_all': medians(videos), 'medians_top': medians(groups['top']), 'medians_recent': medians(groups['recent']),
          'hooks': Counter(v['hook'] for v in videos).most_common(), 'ends': Counter(v['end'] for v in videos).most_common(),
          'hooks_top': Counter(v['hook'] for v in groups['top']).most_common(), 'ends_top': Counter(v['end'] for v in groups['top']).most_common(),
          'figures_in_videos': fig_videos.most_common(), 'psych_in_videos': psy_videos.most_common(),
          'phrases': phrases, 'scores': score_stats}
os.makedirs(os.path.join(case, 'work'), exist_ok=True)
json.dump(author, open(os.path.join(case, 'work/author.json'), 'w'), indent=1, ensure_ascii=False)

L = [f"# Author grammar · {os.path.basename(case)}\n", f"Generated by scripts/aggregate_author.py from {len(videos)} video maps. Medians, counts and shares only; a sample of this size is small, read differences as tendencies.\n",
     '## Videos\n', '| video | group | views | runtime | words | wpm | hook | end | turn at | loops/min | jokes/min | beats |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
for v in sorted(videos, key=lambda v: -v['views']):
    L.append(f"| {v['name']} | {v['group']} | {v['views']:,} | {v['runtime_s']}s | {v['words']} | {v['wpm']} | {v['hook']} | {v['end']} | {v['turn_share']} | {v['loops_per_min']} | {v['humor_per_min']} | {v['beats']} |")
L += ['\n## Medians\n', '| metric | all | top 10 | recent 10 |', '|---|---|---|---|']
for m in metrics:
    L.append(f"| {m} | {author['medians_all'][m]} | {author['medians_top'][m]} | {author['medians_recent'][m]} |")
L += ['\n## Templates (beat skeletons, ASIDE and CTA removed)\n', '| skeleton | videos |', '|---|---|']
L += [f"| {k} | {c} |" for k, c in tmpl.most_common()]
L += ['\n## Core skeletons (first occurrence of each beat, in order)\n', '| core | videos |', '|---|---|'] + [f"| {k} | {c} |" for k, c in cores.most_common()]
L += ['\n## Length classes\n', '| class | videos | median runtime | median turns | most common core |', '|---|---|---|---|---|']
for k, x in author['length_classes'].items():
    L.append(f"| {k} | {x['n']} | {x['median_runtime']} | {x['median_turns']} | {x['cores'][0][0] if x['cores'] else ''} |")
L += ['\n## Median share of runtime per beat (0 when absent)\n'] + [f"- {b}: {beat_share_med[b]}" for b in ORDER]
L += ['\n## Hooks and endings\n', f"- Hooks, all: {author['hooks']}", f"- Hooks, top 10: {author['hooks_top']}", f"- Endings, all: {author['ends']}", f"- Endings, top 10: {author['ends_top']}"]
L += ['\n## Figures and mechanisms (number of videos using each)\n', f"- Figures: {fig_videos.most_common(15)}", f"- Psych: {psy_videos.most_common(12)}"]
L += ['\n## Recurring phrases (3 to 5 words, in at least 4 videos)\n'] + [f"- \"{g}\" ({c} videos)" for g, c in phrases]
L += ['\n## Ability scores across videos (out of 20)\n', '| ability | mean | min | max |', '|---|---|---|---|'] + [f"| {a} | {x['mean']} | {x['min']} | {x['max']} |" for a, x in score_stats.items()]
open(os.path.join(case, '10-author-grammar.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(f"{len(videos)} videos aggregated; {len(tmpl)} skeletons; top skeleton: {tmpl.most_common(1)}")
