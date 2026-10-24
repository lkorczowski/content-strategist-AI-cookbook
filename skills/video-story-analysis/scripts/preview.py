#!/usr/bin/env python3
"""Render work/*.svg to PNG with a fixed light palette, for visual checks without a browser.
Usage: python3 -I preview.py <case_dir> <out_dir>   (needs: pip install cairosvg)"""
import re, sys, os, glob
import cairosvg
V = {'--ink': '#1d1b16', '--muted': '#7a7468', '--grid': '#ddd6c8', '--band': '#f3efe6', '--card': '#ffffff',
     '--line': '#8a8478', '--accent': '#e8501c', '--accent2': '#2a6f97', '--s': '#e8501c', '--l': '#2a6f97',
     '--a': '#5b8c3a', '--h': '#9b5de5', '--x': '#888888', '--bg': '#fbf8f2'}
case, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(case, 'work', '*.svg')):
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'var\((--[a-z0-9]+)\)', lambda m: V[m.group(1)], s)
    s = s.replace('<svg ', '<svg font-family="DejaVu Sans" style="background:#fbf8f2" ', 1)
    name = os.path.basename(f).replace('.svg', '.png')
    cairosvg.svg2png(bytestring=s.encode(), write_to=os.path.join(out, name), output_width=700 if 'radar' in f else 1400)
    print(name)
