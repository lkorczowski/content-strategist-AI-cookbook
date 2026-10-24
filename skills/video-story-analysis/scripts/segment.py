#!/usr/bin/env python3
"""Segment a timed ASR transcript ([mm:ss] text, one line per caption) into sentence units.
Usage: python3 -I segment.py transcript-raw.txt [meme_times.txt] [clip_lang] > work/units-asr.tsv
- Joins the lines and cuts on . ? ! (closing quotes stay with their sentence).
- Track: CLIP if the sentence looks mostly English (for a video in another language with English clips),
  MEME if its start time is listed in meme_times.txt (one mm:ss line per insert), NAR otherwise.
- clip_lang: "en" (default) or "none" to switch off the language check, for example on an English-language video.
TSV output: id, start, end, track, words, text
"""
import re, sys

def secs(t):
    m, s = t.split(':'); return int(m) * 60 + int(s)

def fmt(s):
    return f"{s//60:02d}:{s%60:02d}"

# Common English function words: a short line is English when more than 35% of its words are in this list.
EN = set("the and you he she it is are was were what did got i'm i of to a an my your with this that just like how do don't want "
         "can will would have has had not no yes oh okay right wait all on in at for from so but".split())
CHECK_LANG = (sys.argv[3] if len(sys.argv) > 3 else 'en') != 'none'

def is_english(txt):
    if not CHECK_LANG: return False
    w = re.findall(r"[a-zA-Z']+", txt.lower())
    if not w: return False
    return sum(x in EN for x in w) / len(w) > 0.35

rows = []
for line in open(sys.argv[1], encoding='utf-8'):
    m = re.match(r'\[(\d\d:\d\d)\] (.*)', line.rstrip('\n'))
    if m: rows.append((secs(m.group(1)), m.group(2).strip()))
memes = set()
if len(sys.argv) > 2 and sys.argv[2] != '-':
    memes = {secs(l.strip()) for l in open(sys.argv[2]) if re.match(r'\d\d:\d\d', l.strip())}

units, cur, cur_t, last_t = [], [], None, None
for i, (t, txt) in enumerate(rows):
    lang_en = is_english(txt)
    # forced cut on a language change or a gap over 5 s
    if cur and (t - last_t > 5 or lang_en != is_english(' '.join(cur))):
        units.append((cur_t, last_t, ' '.join(cur))); cur = []
    if not cur: cur_t = t
    parts = re.split(r'(?<=[.?!])\s+(?=[A-ZÀ-ÖØ-Ý"«])', txt)
    for j, p in enumerate(parts):
        if not cur: cur_t = t
        cur.append(p)
        if j < len(parts) - 1 or re.search(r'[.?!]["»]?$', p):
            units.append((cur_t, t, ' '.join(cur))); cur = []
    last_t = t
if cur: units.append((cur_t, last_t, ' '.join(cur)))

print("id\tstart\tend\ttrack\twords\ttext")
for k, (a, b, txt) in enumerate(units, 1):
    tr = 'CLIP' if is_english(txt) else ('MEME' if a in memes else 'NAR')
    print(f"U{k:03d}\t{fmt(a)}\t{fmt(b)}\t{tr}\t{len(txt.split())}\t{txt}")
