#!/usr/bin/env python3
"""Generate a calm, license-free music bed that sits under a voice: pad, pluck arpeggio, sub bass,
soft kick, hats and claps, with a sidechain pump. Seeded, so the same settings give the same track.

It is a fallback that is always available. A licensed track from the user's library is better when
the brand has one (see references/sound.md); mix.py accepts either.

Usage:
  music_bed.py OUT.wav --duration 92 [--bpm 100] [--key A] [--drops 36.2,49.4] [--outro 1.6] [--seed 3]
  --drops: "33.5-35.9,60" windows (or single times = one bar) where the drums stop: a breath before a reveal
"""
import argparse, json
import numpy as np
from scipy import signal
import soundfile as sf

SR = 48000
PROG = {  # chord tones as semitones above the key root (natural minor feel): i7, VImaj7, IIImaj7, VII
    "minor": [[0, 3, 7, 10], [-4, 0, 3, 7], [3, 7, 10, 14], [-2, 2, 5, 10]],
}
ROOTS = {"C": 48, "C#": 49, "D": 50, "D#": 51, "E": 52, "F": 53, "F#": 54, "G": 55, "G#": 56, "A": 45, "A#": 46, "B": 47}

def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)

def saw(f, n, det=0.0, ph=0.0):
    t = np.arange(n) / SR
    return 2 * ((t * f * 2 ** (det / 1200) + ph) % 1.0) - 1

def adsr(n, a, d, s, r, sus_len=None):
    t = np.arange(n) / SR; T = n / SR
    e = np.where(t < a, t / max(a, 1e-4), np.where(t < a + d, 1 - (1 - s) * (t - a) / max(d, 1e-4), s))
    rel = np.clip((T - t) / max(r, 1e-4), 0, 1)
    return e * rel

def ir(seconds, rng, damp=5000):
    n = int(SR * seconds)
    x = rng.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR / (seconds / 6))[:, None]
    sos = signal.butter(2, damp, "lowpass", fs=SR, output="sos")
    x = signal.sosfilt(sos, x, axis=0)
    return x / np.sqrt((x ** 2).sum(axis=0, keepdims=True))

def conv_st(x, h):
    return np.stack([signal.fftconvolve(x[:, c], h[:, c])[: len(x)] for c in range(2)], axis=1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--bpm", type=float, default=100); ap.add_argument("--key", default="A")
    ap.add_argument("--drops", default=""); ap.add_argument("--outro", type=float, default=1.6)
    ap.add_argument("--seed", type=int, default=3); ap.add_argument("--intro", type=float, default=2.4)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    beat = 60.0 / a.bpm; bar = 4 * beat
    N = int((a.duration + 2.0) * SR)
    pad = np.zeros((N, 2)); pl = np.zeros((N, 2)); bass = np.zeros(N); kick = np.zeros(N); perc = np.zeros((N, 2))
    kick_env = np.zeros(N)
    root = ROOTS.get(a.key, 45)
    chords = PROG["minor"]
    drops = []   # windows [s, e): a bar whose start falls inside is played without drums
    for x in a.drops.split(","):
        x = x.strip()
        if not x:
            continue
        if "-" in x[1:]:
            s0, e0 = x.split("-", 1) if not x.startswith("-") else (x, x)
            drops.append((float(s0), float(e0)))
        else:
            drops.append((float(x), float(x) + bar))
    nbars = int(np.ceil(a.duration / bar)) + 1
    lp_pad = signal.butter(2, 1400, "lowpass", fs=SR, output="sos")
    for b in range(nbars):
        t0 = b * bar; i0 = int(t0 * SR)
        if i0 >= N: break
        ch = chords[b % len(chords)]
        # pad: 4 voices, 3 detuned saws each, filtered
        n = min(int(bar * SR * 1.15), N - i0)
        v = np.zeros(n)
        for st in ch:
            f = hz(root + 12 + st)
            for det in (-8, 0, 7):
                v += saw(f, n, det, rng.random()) / 3
        v = signal.sosfilt(lp_pad, v) * adsr(n, 0.35, 0.4, 0.8, 0.5) * 0.16
        pad[i0:i0 + n, 0] += v; pad[i0:i0 + n, 1] += np.roll(v, 90)
        # pluck arpeggio, eighth notes
        pat = [0, 2, 1, 3, 2, 1, 3, 2]
        for k, idx in enumerate(pat):
            ts = t0 + k * beat / 2; j = int(ts * SR)
            if j >= N: break
            m = min(int(0.5 * SR), N - j)
            f = hz(root + 24 + ch[idx])
            tt = np.arange(m) / SR
            note = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt / 0.18) * 0.11
            pan = 0.3 if k % 2 else -0.3
            pl[j:j + m, 0] += note * np.cos((pan + 1) * np.pi / 4); pl[j:j + m, 1] += note * np.sin((pan + 1) * np.pi / 4)
        # bass: root on 1 and on the "and" of 2
        for ts, ln in ((t0, beat * 1.4), (t0 + 1.5 * beat, beat * 1.0), (t0 + 2.5 * beat, beat * 1.2)):
            j = int(ts * SR); m = min(int(ln * SR), N - j)
            if m <= 0: continue
            f = hz(root - 12 + ch[0]); tt = np.arange(m) / SR
            bass[j:j + m] += np.tanh(1.6 * np.sin(2 * np.pi * f * tt)) * adsr(m, 0.01, 0.15, 0.6, 0.12) * 0.22
        # drums (skipped during the intro, the drops and the outro)
        in_drop = any(s0 - 0.05 <= t0 + 0.01 < e0 for s0, e0 in drops) or t0 < a.intro or t0 > a.duration - a.outro - bar * 0.25
        if not in_drop:
            for kb in (0, 2):  # kick, half time
                j = int((t0 + kb * beat) * SR); m = min(int(0.32 * SR), N - j)
                tt = np.arange(m) / SR
                f = 52 + 70 * np.exp(-tt / 0.03)
                kick[j:j + m] += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.12) * 0.55
                kick_env[j:j + int(0.25 * SR)] = np.maximum(kick_env[j:j + int(0.25 * SR)], np.exp(-np.arange(min(int(0.25 * SR), N - j)) / SR / 0.09))
            for k in range(8):  # hats on off-beats
                if k % 2 == 0: continue
                j = int((t0 + k * beat / 2) * SR); m = min(int(0.05 * SR), N - j)
                h = signal.sosfilt(signal.butter(2, 8000, "highpass", fs=SR, output="sos"), rng.standard_normal(m)) * np.exp(-np.arange(m) / SR / 0.012) * 0.05
                perc[j:j + m, 0] += h * 0.8; perc[j:j + m, 1] += h
            for kb in (1, 3):  # soft clap
                j = int((t0 + kb * beat) * SR); m = min(int(0.2 * SR), N - j)
                cl = signal.sosfilt(signal.butter(2, [900, 2600], "bandpass", fs=SR, output="sos"), rng.standard_normal(m)) * np.exp(-np.arange(m) / SR / 0.05) * 0.07
                perc[j:j + m, 0] += cl; perc[j:j + m, 1] += cl * 0.9
    # delay on the plucks (dotted eighth), sidechain pump on pad and bass
    d = int(0.75 * beat * SR)
    for _ in range(3):
        pl[d:] += 0.32 * pl[:-d][:, ::-1]
    pump = 1 - 0.35 * signal.lfilter([1], [1, -0.0], kick_env)
    pad *= pump[:, None]; bass *= pump
    h = ir(2.0, rng)
    wet = conv_st(pad + pl, h) * 0.35
    mix = pad + pl + wet + np.stack([bass, bass], 1) + np.stack([kick, kick], 1) + perc
    # intro filter opening and outro: let the last chord ring
    t = np.arange(N) / SR
    open_k = np.clip(t / max(a.intro, 0.1), 0, 1)
    lp = signal.butter(2, 600, "lowpass", fs=SR, output="sos")
    mix = mix * open_k[:, None] + signal.sosfilt(lp, mix, axis=0) * (1 - open_k[:, None])
    end = int(a.duration * SR)
    fade = np.ones(N); fade[end:] = 0
    tail_n = int(0.8 * SR); fade[end - tail_n:end] = np.linspace(1, 0, tail_n) ** 1.5
    mix *= fade[:, None]
    mix = np.tanh(mix * 1.3) / 1.3
    mix = mix[:end]
    mix *= 10 ** (-3 / 20) / (np.abs(mix).max() + 1e-9)
    sf.write(a.out, mix.astype(np.float32), SR, subtype="FLOAT")
    print(json.dumps({"status": "DONE", "out": a.out, "seconds": round(len(mix) / SR, 2), "bpm": a.bpm, "key": a.key,
                      "license": "generated by music_bed.py, no third-party material"}))

if __name__ == "__main__":
    main()
