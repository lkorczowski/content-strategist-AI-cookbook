#!/usr/bin/env python3
"""Synthesize a small sound-effect library from scratch (no sample, no license to track).

Every effect is generated from noise, sines and filters with a fixed seed, so the same command gives
the same files on any machine. The set covers what motion design needs: whoosh, whoosh_low, swish,
swish_out, pop, tick, click, key (6 variants), snip, impact, riser_soft, chime.
Replace any file with a licensed sample of the same name to change the sound (see references/sound.md).

Usage: sfx_synth.py OUTDIR [--sr 48000]
"""
import argparse, json, os
import numpy as np
from scipy import signal
import soundfile as sf

SR = 48000

def noise(n, rng, pink=False):
    x = rng.standard_normal(n)
    if pink:   # 1/f spectrum shaped in the frequency domain
        X = np.fft.rfft(x); f = np.arange(len(X), dtype=float); f[0] = 1.0
        x = np.fft.irfft(X / np.sqrt(f), n)
    return x / (np.abs(x).max() + 1e-9)

def sweep_filter(x, f_start, f_mid, f_end, kind="bandpass", q=1.2, block=256):
    """Filter whose cutoff glides start -> mid -> end (log scale), processed block by block with state kept."""
    n = len(x); out = np.zeros(n); zi = None; nb = int(np.ceil(n / block))
    for b in range(nb):
        k = b / max(nb - 1, 1)
        f = np.exp(np.interp(k, [0, 0.5, 1], np.log([f_start, f_mid, f_end])))
        f = min(f, SR / 2 * 0.9)
        if kind == "bandpass":
            lo, hi = f / (1 + 1 / (2 * q)), f * (1 + 1 / (2 * q))
            sos = signal.butter(2, [lo, min(hi, SR / 2 * 0.95)], btype="bandpass", fs=SR, output="sos")
        else:
            sos = signal.butter(2, f, btype=kind, fs=SR, output="sos")
        if zi is None or zi.shape[0] != sos.shape[0]:
            zi = signal.sosfilt_zi(sos) * 0
        seg = x[b * block:(b + 1) * block]
        y, zi = signal.sosfilt(sos, seg, zi=zi)
        out[b * block:b * block + len(seg)] = y
    return out

def env(n, attack, release, shape=2.0):
    t = np.arange(n) / SR; T = n / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1) ** shape
    r = np.clip((T - t) / max(release, 1e-4), 0, 1) ** shape
    return np.minimum(a, r)

def expdec(n, tau):
    return np.exp(-np.arange(n) / SR / tau)

def fade_tail(x, ms=6.0):
    m = min(len(x), int(SR * ms / 1000))
    if m > 1:
        x = x.copy(); x[-m:] *= np.linspace(1, 0, m)
    return x

def reverb(x, rng, seconds=0.8, mix=0.2, damp=4000):
    x = fade_tail(x)
    n = int(SR * seconds)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / (seconds / 5))
    ir = signal.sosfilt(signal.butter(2, damp, "lowpass", fs=SR, output="sos"), ir)
    ir /= np.sqrt((ir ** 2).sum()) + 1e-9
    wet = signal.fftconvolve(x, ir)
    dry = np.concatenate([x, np.zeros(len(wet) - len(x))])
    return (1 - mix) * dry + mix * wet * 0.6

def stereo(x, pan_from=0.0, pan_to=0.0, width_ms=0.0):
    x = fade_tail(x, 8.0)
    n = len(x); p = np.linspace(pan_from, pan_to, n)
    l = x * np.cos((p + 1) * np.pi / 4); r = x * np.sin((p + 1) * np.pi / 4)
    if width_ms:
        d = int(SR * width_ms / 1000); r = np.concatenate([np.zeros(d), r[:-d]]) if d else r
    return np.stack([l, r], axis=1)

def norm(x, peak_db=-1.0):
    return x / (np.abs(x).max() + 1e-9) * 10 ** (peak_db / 20)

def tone(n, f0, f1=None, kind="sine"):
    f = np.geomspace(f0, f1 or f0, n) if f1 else np.full(n, f0)
    ph = 2 * np.pi * np.cumsum(f) / SR
    if kind == "tri":
        return 2 / np.pi * np.arcsin(np.sin(ph))
    return np.sin(ph)

def make(name, rng):
    if name == "whoosh":
        n = int(0.55 * SR); x = sweep_filter(noise(n, rng, True), 280, 2600, 700, q=0.9)
        x *= env(n, 0.28, 0.27, 1.6); return stereo(norm(reverb(x, rng, 0.6, 0.18)), -0.6, 0.6)
    if name == "whoosh_low":
        n = int(0.65 * SR); x = sweep_filter(noise(n, rng, True), 140, 900, 180, kind="lowpass")
        x = norm(x) * env(n, 0.3, 0.35, 1.5) + 0.5 * tone(n, 95, 48) * env(n, 0.05, 0.5, 1.2)
        return stereo(norm(reverb(x, rng, 0.7, 0.15)), -0.3, 0.3, 6)
    if name == "swish":
        n = int(0.24 * SR); x = sweep_filter(noise(n, rng), 1800, 6500, 3000, q=1.4)
        x *= env(n, 0.09, 0.15, 1.8); return stereo(norm(reverb(x, rng, 0.35, 0.1)), 0.3, -0.3)
    if name == "swish_out":
        n = int(0.28 * SR); x = sweep_filter(noise(n, rng, True), 3200, 1200, 380, q=1.0)
        x *= env(n, 0.04, 0.24, 1.4); return stereo(norm(x), 0.4, -0.4)
    if name == "pop":
        n = int(0.11 * SR); x = tone(n, 950, 420) * expdec(n, 0.035)
        x[:int(0.002 * SR)] += rng.standard_normal(int(0.002 * SR)) * 0.3
        return stereo(norm(reverb(x, rng, 0.25, 0.08)), 0, 0, 2)
    if name == "tick":
        n = int(0.035 * SR); x = signal.sosfilt(signal.butter(2, [2500, 6000], "bandpass", fs=SR, output="sos"), rng.standard_normal(n)) * expdec(n, 0.004)
        x += 0.4 * tone(n, 2400) * expdec(n, 0.006); return stereo(norm(x, -3))
    if name == "click":
        n = int(0.07 * SR); x = np.zeros(n)
        for off, g in ((0, 1.0), (0.026, 0.6)):
            i = int(off * SR); m = int(0.012 * SR)
            x[i:i + m] += signal.sosfilt(signal.butter(2, [1200, 5000], "bandpass", fs=SR, output="sos"), rng.standard_normal(m)) * expdec(m, 0.0025) * g
        return stereo(norm(x, -2))
    if name.startswith("key"):
        n = int(0.06 * SR); f = 1500 + rng.random() * 1800
        x = signal.sosfilt(signal.butter(2, [f * 0.6, f * 1.6], "bandpass", fs=SR, output="sos"), rng.standard_normal(n)) * expdec(n, 0.006)
        x += 0.25 * tone(n, 180 + rng.random() * 60) * expdec(n, 0.012)
        return stereo(norm(x, -2 - rng.random() * 4), rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3))
    if name == "snip":
        n = int(0.14 * SR); x = np.zeros(n)
        for off in (0.0, 0.045):
            i = int(off * SR); m = int(0.03 * SR)
            b = signal.sosfilt(signal.butter(4, [4200, 8800], "bandpass", fs=SR, output="sos"), rng.standard_normal(m)) * expdec(m, 0.005)
            b += 0.5 * tone(m, 6200) * expdec(m, 0.01)
            x[i:i + m] += b
        return stereo(norm(reverb(x, rng, 0.2, 0.06), -2))
    if name == "impact":
        n = int(1.0 * SR)
        sub = tone(n, 62, 36) * expdec(n, 0.28)
        hit = signal.sosfilt(signal.butter(2, 1400, "lowpass", fs=SR, output="sos"), rng.standard_normal(n)) * expdec(n, 0.06)
        x = 0.9 * sub + 0.6 * norm(hit)
        return stereo(norm(reverb(x, rng, 1.0, 0.18, 2500)), 0, 0, 8)
    if name == "riser_soft":
        n = int(1.4 * SR); x = sweep_filter(noise(n, rng, True), 400, 1600, 6000, q=1.1)
        g = (np.arange(n) / n) ** 2.2; x = norm(x) * g + 0.15 * tone(n, 300, 900) * g
        x *= env(n, 0.05, 0.06, 1.0); return stereo(norm(reverb(x, rng, 0.6, 0.2)), -0.5, 0.5, 5)
    if name == "chime":
        n = int(1.6 * SR); f = 880.0; x = np.zeros(n)
        for ratio, g, tau in ((1, 1, 0.9), (2.0, 0.35, 0.5), (2.76, 0.25, 0.35), (5.4, 0.12, 0.18)):
            x += g * tone(n, f * ratio) * expdec(n, tau)
        x *= env(n, 0.004, 0.2, 1.0); return stereo(norm(reverb(x, rng, 1.2, 0.3, 6000), -3), 0, 0, 7)
    raise ValueError(name)

NAMES = ["whoosh", "whoosh_low", "swish", "swish_out", "pop", "tick", "click", "snip", "impact", "riser_soft", "chime"] + [f"key_{i}" for i in range(1, 7)]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("outdir"); a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    rng = np.random.default_rng(2026)
    man = {}
    for nm in NAMES:
        x = make(nm, rng)
        sf.write(os.path.join(a.outdir, nm + ".wav"), x.astype(np.float32), SR, subtype="FLOAT")
        man[nm] = {"seconds": round(len(x) / SR, 3), "license": "generated by sfx_synth.py, no third-party material"}
    json.dump(man, open(os.path.join(a.outdir, "manifest.json"), "w"), indent=1)
    print(json.dumps({"status": "DONE", "files": len(man), "dir": a.outdir}))

if __name__ == "__main__":
    main()
