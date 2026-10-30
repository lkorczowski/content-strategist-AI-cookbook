#!/usr/bin/env python3
"""Synthesize the sound bed of a statur-motion-3d video from the "sound" cues of scenario.json.

No samples, no voice, no license to clear: every sound is generated (numpy + scipy).
Cue types: ambience, ticks, riser, boom, drone, crackle, swell, noise, pad, rumble, shimmer, note.
Usage: sound.py scenario.json out.wav [--seed 7]
"""
import argparse, json, wave
import numpy as np
from scipy.signal import lfilter

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('scenario'); ap.add_argument('out'); ap.add_argument('--seed', type=int, default=7)
args = ap.parse_args()
S = json.load(open(args.scenario))
SR, DUR = 48000, float(S['duration'])
N = int(SR * DUR); t = np.arange(N) / SR
rng = np.random.default_rng(args.seed)
L = np.zeros(N); Rt = np.zeros(N)

def env(a, b, attack=.05, release=.3):
    e = np.zeros(N); i0, i1 = int(a * SR), min(N, int(b * SR)); seg = t[i0:i1] - a; ln = b - a
    e[i0:i1] = np.clip(seg / max(attack, 1e-3), 0, 1) * np.clip((ln - seg) / max(release, 1e-3), 0, 1); return e
def lowpass(x, cut):
    k = np.exp(-2 * np.pi * cut / SR); return lfilter([1 - k], [1, -k], x)
def noise(): return rng.standard_normal(N)
def add(x, gain=1.0, pan=0.0):
    global L, Rt
    L += x * gain * (1 - pan); Rt += x * gain * (1 + pan)
def boom(at, size=1.0, freq=48):
    i = int(at * SR); seg = t[:N - i]; x = np.zeros(N)
    x[i:] = np.sin(2 * np.pi * freq * seg * (1 - .3 * np.clip(seg, 0, 1))) * np.exp(-seg * 1.6 / size) * .9
    x[i:] += lowpass(noise()[:N - i], 400) * np.exp(-seg * 3 / size) * .6
    return x

for c in S.get('sound', []):
    ty, g = c['type'], c.get('gain', .5); a, b = c.get('from', 0), c.get('to', DUR)
    if ty == 'ambience': add(lowpass(noise(), c.get('cut', 900)) * env(a, b, 1.0, .05), g)
    elif ty == 'ticks':
        k = 0
        while a + k * c.get('every', 1) < b:
            i = int((a + k * c.get('every', 1)) * SR); n = int(.03 * SR); x = np.zeros(N)
            if i + n < N: x[i:i + n] = np.sin(2 * np.pi * 2400 * t[:n]) * np.exp(-t[:n] * 180)
            add(x, g, .2 if k % 2 else -.2); k += 1
    elif ty == 'riser': add(np.sin(2 * np.pi * (110 + 220 * np.clip((t - a) / (b - a), 0, 1) ** 2) * t) * env(a, b, (b - a) * .85, .02), g)
    elif ty == 'boom': add(boom(c['at'], c.get('size', 1.0), c.get('freq', 48)), g)
    elif ty == 'drone': add((np.sin(2 * np.pi * 41.2 * t) + .5 * np.sin(2 * np.pi * 61.7 * t) + .25 * np.sin(2 * np.pi * 82.4 * t + 1)) * env(a, b, 2.0, .2), g)
    elif ty == 'crackle':
        x = np.zeros(N)
        for _ in range(int(75 * (b - a))):
            at = rng.uniform(a, b); i = int(at * SR); n = int(.012 * SR)
            if i + n < N: x[i:i + n] += rng.standard_normal(n) * np.exp(-np.arange(n) / (n / 4)) * rng.uniform(.2, 1) * ((at - a) / (b - a))
        add(x, g, float(rng.uniform(-.5, .5)))
    elif ty == 'swell': add(lowpass(noise(), c.get('cut', 1500)) * env(a, b, b - a, .05) * np.clip((t - a) / (b - a), 0, 1) ** 2, g)
    elif ty == 'noise': add(lowpass(noise(), c.get('cut', 8000)) * env(a, b, .01, (b - a) * .9), g)
    elif ty == 'pad':
        pad = sum(np.sin(2 * np.pi * f * t + p) for f, p in [(110, 0), (164.8, 1), (220.5, 2), (329.6, .5)]) / 4 * (1 + .3 * np.sin(2 * np.pi * .2 * t))
        add(pad * env(a, b, 2.5, .3), g)
    elif ty == 'rumble': add(lowpass(noise(), c.get('cut', 120)) * env(a, b, 1, .3), g)
    elif ty == 'shimmer': add(sum(np.sin(2 * np.pi * f * t) for f in (880, 1318.5, 1760, 2637)) / 4 * env(a, b, .3, 1), g)
    elif ty == 'note': add(np.sin(2 * np.pi * c.get('freq', 55) * t) * env(a, b, 1.5, 2), g)
    else: raise SystemExit(f'unknown cue type: {ty}')

mix = np.stack([L, Rt], 1); peak = np.max(np.abs(mix)) or 1
pcm = (mix / peak * .89 * 32767).astype(np.int16)
with wave.open(args.out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('sound written to', args.out)
