#!/usr/bin/env python3
"""List gaps over 6 s in an ASR transcript ([mm:ss] lines) and the share of runtime they cover.
Usage: python3 -I coverage.py transcript-raw.txt [runtime_s]"""
import re,sys
L=[l for l in open(sys.argv[1],encoding='utf-8') if l.startswith('[')]
def s(t):m,x=t.split(':');return int(m)*60+int(x)
rows=[(s(re.match(r'\[(\d\d:\d\d)\]',l).group(1)),l[8:].strip()) for l in L]
END=int(sys.argv[2]) if len(sys.argv)>2 else (rows[-1][0]+3 if rows else 0)  # runtime_s, default: last caption + 3 s
gaps=[]
for i,(t,txt) in enumerate(rows):
    nxt=rows[i+1][0] if i+1<len(rows) else END
    # approx duration of line: ~2.2s
    if nxt-t>6: gaps.append((t,nxt,nxt-t-2,txt))
tot=sum(g[2] for g in gaps)
print('lines',len(rows),'gaps>6s',len(gaps),'approx non-speech seconds',tot, 'share %.1f%%'%(100*tot/max(1,END)))
for a,b,d,txt in gaps: print(f'{a//60:02d}:{a%60:02d} -> {b//60:02d}:{b%60:02d}  ~{d:3d}s  after: {txt[:60]}')
words=sum(len(t.split()) for _,t in rows)
print('words',words)
