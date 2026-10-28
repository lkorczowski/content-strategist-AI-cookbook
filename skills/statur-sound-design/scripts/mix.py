#!/usr/bin/env python3
"""Sound pass of a pro edit: cut voice, voice chain, sound effects on cues, music ducked under the voice,
two-pass loudness normalization. Writes the final mix and a report with the level of each stem.

Inputs
  --source   the recording (any audio ffmpeg reads)        --plan   plan.json (cut mapping, duration)
  --sfx      sfx.json (cues from build_layers.py)            --lib    folder of effect files (sfx_synth.py or licensed)
  --music    music file (music_bed.py or a licensed track)   --rnnoise model file for arnndn (optional)

Levels (defaults, tune per account; no platform publishes a music level, see references/sound.md)
  music under speech: about 18 dB below the voice; music in pauses: about 10 dB below; final -14 LUFS, -1.5 dBTP.

Usage:
  mix.py --source SRC --plan plan.json --sfx sfx.json --lib sfx/ --music music.wav --out mix.wav [--rnnoise sh.rnnn]
"""
import argparse, json, os, re, subprocess, tempfile
import numpy as np
import soundfile as sf

SR = 48000

def decode(path, sr=SR):
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-vn", "-ac", "2", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()

def lufs(path, extra=""):
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-i", path, "-af", f"{extra}ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr); p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    return (float(i[-1]) if i else None, float(p[-1]) if p else None)

def onepole(x, a_up, a_down):
    y = np.empty_like(x); v = 0.0
    for i, s in enumerate(x):
        c = a_up if s > v else a_down
        v = v + c * (s - v); y[i] = v
    return y

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True); ap.add_argument("--plan", required=True)
    ap.add_argument("--sfx", required=True); ap.add_argument("--lib", required=True)
    ap.add_argument("--music", default=None); ap.add_argument("--out", required=True)
    ap.add_argument("--rnnoise", default=None)
    ap.add_argument("--music-db", type=float, default=-12.0, help="music gain in pauses, relative to its own level")
    ap.add_argument("--duck-db", type=float, default=-8.0, help="extra music gain while the voice speaks")
    ap.add_argument("--sfx-db", type=float, default=0.0, help="trim on every effect")
    ap.add_argument("--lufs", type=float, default=-14.0); ap.add_argument("--tp", type=float, default=-1.5)
    ap.add_argument("--voice-chain", default=None, help="override the ffmpeg voice filter chain")
    a = ap.parse_args()
    P = json.load(open(a.plan)); fps = P["fps"]; spf = SR / fps
    work = tempfile.mkdtemp(prefix="mix_")
    # 1. voice cut, sample accurate (each piece is a whole number of frames), 5 ms crossfades at joins
    src = decode(a.source)
    pieces = []
    for m in P["mapping"]:
        s = int(round(round(m["src_s"] * fps) * spf)); n = int(round(round((m["src_e"] - m["src_s"]) * fps) * spf))
        seg = src[s:s + n].copy()
        if len(seg) < n:
            seg = np.concatenate([seg, np.zeros((n - len(seg), 2), np.float32)])
        f = int(0.005 * SR); ramp = np.linspace(0, 1, f, dtype=np.float32)[:, None]
        seg[:f] *= ramp; seg[-f:] *= ramp[::-1]
        pieces.append(seg)
    voice = np.concatenate(pieces + [np.zeros((int(round(P["tail"] * SR)), 2), np.float32)])
    total = int(round(P["duration"] * SR))
    voice = voice[:total] if len(voice) >= total else np.concatenate([voice, np.zeros((total - len(voice), 2), np.float32)])
    vr = os.path.join(work, "voice_raw.wav"); sf.write(vr, voice, SR, subtype="FLOAT")
    # 2. voice chain
    chain = a.voice_chain or ("highpass=f=80," + (f"arnndn=m='{a.rnnoise}':mix=0.65," if a.rnnoise else "afftdn=nf=-50:nr=8,") +
                              "equalizer=f=250:t=q:w=1.2:g=-2,equalizer=f=4200:t=q:w=1.0:g=2,deesser=i=0.3," +
                              "acompressor=threshold=-22dB:ratio=2.5:attack=8:release=160:makeup=2")
    vp = os.path.join(work, "voice.wav")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", vr, "-af", chain, "-c:a", "pcm_f32le", vp], check=True)
    voice = decode(vp)[:total]
    if len(voice) < total:
        voice = np.concatenate([voice, np.zeros((total - len(voice), 2), np.float32)])
    # 3. effects on cues
    cues = json.load(open(a.sfx))["cues"]
    fx = np.zeros((total, 2), np.float32); cache = {}; kn = 0
    rng = np.random.default_rng(5)
    for c in cues:
        name = c["name"]
        if name == "key":
            kn += 1; name = f"key_{(kn % 6) + 1}"
        if name not in cache:
            p = os.path.join(a.lib, name + ".wav")
            if not os.path.exists(p):
                print(json.dumps({"warning": f"missing effect {name}"})); cache[name] = None; continue
            cache[name] = decode(p)
        x = cache[name]
        if x is None:
            continue
        g = 10 ** ((c.get("gain_db", -14) + a.sfx_db + (rng.uniform(-1.5, 1.5) if name.startswith(("tick", "key")) else 0)) / 20)
        i = int(round(c["t"] * SR)); j = min(total, i + len(x))
        if i < total and i >= 0:
            fx[i:j] += x[: j - i] * g
    # 4. music ducked under the voice
    mus = np.zeros((total, 2), np.float32)
    if a.music:
        m = decode(a.music)[:total]
        mus[: len(m)] = m
        hop = int(0.01 * SR)
        rms = np.sqrt(np.convolve((voice ** 2).mean(axis=1), np.ones(hop * 3) / (hop * 3), mode="same") + 1e-12)
        db = 20 * np.log10(rms[::hop] + 1e-9)
        act = np.clip((db + 48) / 14, 0, 1)
        act = onepole(act, 0.35, 0.025)                  # fast attack, slow release (per 10 ms step)
        gdb = a.music_db + a.duck_db * act
        g = np.repeat(10 ** (gdb / 20), hop)[:total]
        if len(g) < total:
            g = np.concatenate([g, np.full(total - len(g), g[-1])])
        mus *= g[:, None]
    pre = voice + fx + mus
    pp = os.path.join(work, "pre.wav"); sf.write(pp, pre, SR, subtype="FLOAT")
    # 5. two-pass loudness normalization
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", pp, "-af", f"loudnorm=I={a.lufs}:TP={a.tp}:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    mj = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)[-1])
    ln = (f"loudnorm=I={a.lufs}:TP={a.tp}:LRA=11:measured_I={mj['input_i']}:measured_TP={mj['input_tp']}:measured_LRA={mj['input_lra']}:"
          f"measured_thresh={mj['input_thresh']}:offset={mj['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", pp, "-af", ln + f",aresample={SR}", "-c:a", "pcm_s16le", a.out], check=True)
    # report: stems relative to the final mix
    gain = 10 ** ((a.lufs - float(mj["input_i"])) / 20)
    rep = {}
    for nm, x in (("voice", voice), ("sfx", fx), ("music", mus)):
        p = os.path.join(work, nm + ".wav"); sf.write(p, x * gain, SR, subtype="FLOAT")
        rep[nm] = dict(zip(("lufs", "peak_dbfs"), lufs(p)))
    rep["final"] = dict(zip(("lufs", "peak_dbfs"), lufs(a.out)))
    if rep["voice"]["lufs"] is not None and rep["music"]["lufs"] is not None:
        rep["voice_minus_music_db"] = round(rep["voice"]["lufs"] - rep["music"]["lufs"], 1)
    rep.update({"status": "DONE", "out": a.out, "cues": len(cues), "chain": chain})
    json.dump(rep, open(os.path.splitext(a.out)[0] + "_report.json", "w"), indent=1)
    print(json.dumps(rep))

if __name__ == "__main__":
    main()
