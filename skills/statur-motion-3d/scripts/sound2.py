#!/usr/bin/env python3
"""STATUR SIM sound v2: a synthesized music bed (kick, bass, hats, pad, arpeggio) by sections, plus SFX on cuts.
Reads scenario.json keys "music" {bpm, key, mood, sections[[from,to,name]]} and "sfx" [[type, time]].
Moods: tense (minor), bright (major), playful (major, plucky). No samples, no voice.
Usage: sound2.py scenario.json out.wav"""
import json, sys, wave
import numpy as np
from scipy.signal import lfilter

S = json.load(open(sys.argv[1])); SR = 44100; DUR = float(S['duration']); N = int(SR * DUR); t = np.arange(N) / SR
rng = np.random.default_rng(3); L = np.zeros(N); Rr = np.zeros(N)
M = S.get('music', {}); bpm = M.get('bpm', 100); beat = 60 / bpm; mood = M.get('mood', 'tense')
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}; root = 38 + NOTE.get(M.get('key', 'D'), 2)  # MIDI around D2
def hz(m): return 440 * 2 ** ((m - 69) / 12)
prog = [[0, 3, 7], [-4, 0, 3], [3, 7, 10], [-2, 2, 5]] if mood == 'tense' else [[0, 4, 7], [-3, 0, 4], [5, 9, 12], [7, 11, 14]]
def lp(x, c): k = np.exp(-2 * np.pi * c / SR); return lfilter([1 - k], [1, -k], x)
def hp(x, c): return x - lp(x, c)
def add(x, g=1.0, pan=0.0, at=0):
    i = int(at * SR); n = min(len(x), N - i)
    if n > 0: L[i:i + n] += x[:n] * g * (1 - pan); Rr[i:i + n] += x[:n] * g * (1 + pan)
def env(n, a, r): e = np.ones(n); ai = max(1, int(a * SR)); e[:ai] = np.linspace(0, 1, ai) if ai < n else 1; e *= np.exp(-np.arange(n) / SR / max(r, 1e-3)); return e
def kick(): n = int(.35 * SR); tt = np.arange(n) / SR; f = 50 + 90 * np.exp(-tt * 30); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9)
def hat(): n = int(.05 * SR); return hp(rng.standard_normal(n), 7000) * np.exp(-np.arange(n) / SR * 80)
def snare(): n = int(.2 * SR); return (hp(rng.standard_normal(n), 1500) * .7 + np.sin(2 * np.pi * 190 * np.arange(n) / SR) * .4) * np.exp(-np.arange(n) / SR * 22)
def tone(f, d, kind='sine', a=.005, r=.3):
    n = int(d * SR); tt = np.arange(n) / SR
    if kind == 'saw': x = 2 * ((f * tt) % 1) - 1; x = lp(x, 1800)
    elif kind == 'pluck': x = (2 * ((f * tt) % 1) - 1); x = lp(x, 2600) * np.exp(-tt * 9)
    else: x = np.sin(2 * np.pi * f * tt)
    return x * env(n, a, r)
sec_of = lambda x: next((s[2] for s in M.get('sections', []) if s[0] <= x < s[1]), 'none')
nb = int(DUR / beat) + 1
for b in range(nb):
    tb = b * beat; sec = sec_of(tb); bar = b // 4; chord = prog[bar % 4]; pos = b % 4
    if sec in ('pulse', 'build', 'wide', 'drive'):
        if sec != 'wide' or pos in (0, 2): add(kick(), .9 if sec != 'pulse' else .6, 0, tb)
        add(tone(hz(root + chord[0] - 12), beat * .9, 'sine', .005, beat * .6), .55, 0, tb)
        if sec in ('build', 'drive'):
            add(tone(hz(root + chord[0] - 12), beat * .45, 'sine', .005, .15), .35, 0, tb + beat / 2)
            if pos in (1, 3): add(snare(), .35, .1, tb)
        for h in (0, .5): add(hat(), .12 if sec != 'pulse' else .07, .3, tb + h * beat)
        if sec in ('build', 'wide', 'drive') or mood == 'playful':
            for k in range(4):
                n = root + 12 + chord[k % 3] + (12 if k == 3 else 0)
                add(tone(hz(n), beat / 4 * .95, 'pluck'), .16 if mood != 'playful' else .22, (-.4 if k % 2 else .4), tb + k * beat / 4)
    if sec in ('pulse', 'build', 'wide', 'hold', 'drive', 'end') and pos == 0:
        for k, iv in enumerate(chord):
            f = hz(root + 12 + iv); d = beat * 4.05
            add(tone(f, d, 'saw', .4, 2.5) * .5 + tone(f * 1.003, d, 'saw', .4, 2.5) * .5, .07 if sec != 'end' else .1, (k - 1) * .3, tb)
    if sec == 'hold' and pos in (0, 1): add(kick() * .7, .5, 0, tb)
    if sec == 'drop' and pos == 0: add(lp(rng.standard_normal(int(beat * 4 * SR)), 120) * env(int(beat * 4 * SR), .3, 2), .5, 0, tb)
# SFX
for kind, at in S.get('sfx', []):
    if kind == 'whoosh':
        n = int(.45 * SR); x = rng.standard_normal(n); x = lp(x, 900) * np.sin(np.linspace(0, np.pi, n)) ** 2; add(x, .5, -.3, at - .25)
    elif kind == 'blackout':
        n = int(1.6 * SR); tt = np.arange(n) / SR; x = np.sin(2 * np.pi * np.cumsum(120 * np.exp(-tt * 2) + 30) / SR) * np.exp(-tt * 1.5) + (np.sign(np.sin(2 * np.pi * 50 * tt)) * .15 * np.exp(-tt * 6)); add(x, .9, 0, at)
    elif kind in ('thud', 'hit'):
        add(kick() * (1.3 if kind == 'hit' else 1), 1.0, 0, at); add(lp(rng.standard_normal(int(.6 * SR)), 300) * env(int(.6 * SR), .001, .25), .5, 0, at)
    elif kind == 'pop':
        add(tone(880, .12, 'sine', .001, .05) + tone(1320, .12, 'sine', .001, .04), .35, .2, at)
    elif kind == 'ding':
        add(tone(1568, .8, 'sine', .001, .35) + .5 * tone(2349, .8, 'sine', .001, .3), .25, .2, at)
    elif kind == 'crowd':
        n = int(2.5 * SR); x = lp(rng.standard_normal(n), 700) * (1 + .5 * np.sin(np.arange(n) / SR * 9)) * env(n, .3, 1.2); add(x, .45, 0, at)
mix = np.stack([L, Rr], 1); mix = np.tanh(mix / (np.max(np.abs(mix)) + 1e-9) * 1.4) * .9
with wave.open(sys.argv[2], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('sound written', sys.argv[2])
