#!/usr/bin/env python3
"""Local FR/EN transcription with word timestamps (sherpa-onnx + NVIDIA Parakeet TDT 0.6B v3 + Silero VAD).
Usage: transcribe.py INPUT_MEDIA OUT_DIR [--threads N] [--max-speech 20]
(--max-speech: longest chunk in seconds; 6 or less for a second reading of a bilingual passage)
Outputs in OUT_DIR: words.json, segments.json, transcript.txt (timestamped), transcript.srt, speech.json (VAD speech spans)
"""
import sys, os, json, time, subprocess, argparse
import numpy as np, sherpa_onnx

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.environ.get("ASR_MODEL_DIR", os.path.join(HERE, "..", "models", "sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8"))
VAD = os.environ.get("VAD_MODEL", os.path.join(HERE, "..", "models", "silero_vad.onnx"))
SR = 16000

def load_audio(path):
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()

def fmt(t, srt=False):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    if srt:
        return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}".replace(",1000", ",999")
    return f"{h:d}:{m:02d}:{s:05.2f}" if h else f"{m:02d}:{s:05.2f}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input"); ap.add_argument("out")
    ap.add_argument("--threads", type=int, default=max(1, os.cpu_count() or 2))
    ap.add_argument("--max-speech", type=float, default=20.0)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    samples = load_audio(a.input)
    total = len(samples) / SR
    print(f"audio {total/60:.1f} min loaded in {time.time()-t0:.1f}s", flush=True)

    rec = sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=f"{M}/encoder.int8.onnx", decoder=f"{M}/decoder.int8.onnx",
        joiner=f"{M}/joiner.int8.onnx", tokens=f"{M}/tokens.txt",
        num_threads=a.threads, model_type="nemo_transducer", decoding_method="greedy_search")

    cfg = sherpa_onnx.VadModelConfig()
    cfg.silero_vad.model = VAD
    cfg.silero_vad.threshold = 0.45
    cfg.silero_vad.min_silence_duration = 0.30
    cfg.silero_vad.min_speech_duration = 0.20
    cfg.silero_vad.max_speech_duration = a.max_speech
    cfg.sample_rate = SR
    vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=180)
    win = cfg.silero_vad.window_size

    spans = []
    def drain():
        while not vad.empty():
            seg = vad.front
            spans.append((seg.start, np.array(seg.samples, dtype=np.float32)))
            vad.pop()
    for i in range(0, len(samples), win):
        vad.accept_waveform(samples[i:i+win]); drain()
    vad.flush(); drain()
    print(f"VAD: {len(spans)} speech spans in {time.time()-t0:.1f}s", flush=True)

    words, segments = [], []
    t1 = time.time()
    for k, (start, chunk) in enumerate(spans):
        off = start / SR
        pad = np.zeros(int(0.15 * SR), dtype=np.float32)   # small padding helps the last token
        st = rec.create_stream(); st.accept_waveform(SR, np.concatenate([chunk, pad]))
        rec.decode_stream(st); r = st.result
        toks, ts = list(r.tokens), list(r.timestamps)
        durs = list(r.durations) if hasattr(r, "durations") else [0.08] * len(toks)
        cur = None
        seg_words = []
        for tok, t, d in zip(toks, ts, durs):
            if tok.startswith(" ") or cur is None:
                if cur: seg_words.append(cur)
                cur = {"w": tok.strip(), "s": round(off + t, 3), "e": round(off + t + max(d, 0.04), 3)}
            else:
                cur["w"] += tok
                cur["e"] = round(off + t + max(d, 0.04), 3)
        if cur: seg_words.append(cur)
        seg_end = off + len(chunk) / SR
        for w in seg_words:
            w["e"] = min(w["e"], round(seg_end + 0.05, 3))
        words.extend(seg_words)
        segments.append({"i": k, "s": round(off, 3), "e": round(seg_end, 3), "text": r.text.strip()})
        if k % 50 == 0:
            done = seg_end / total
            el = time.time() - t1
            print(f"  {k}/{len(spans)} spans, {done*100:.0f}% audio, {el:.0f}s elapsed", flush=True)

    json.dump(words, open(os.path.join(a.out, "words.json"), "w"), ensure_ascii=False)
    json.dump(segments, open(os.path.join(a.out, "segments.json"), "w"), ensure_ascii=False, indent=0)
    json.dump([[round(s/SR,3), round(s/SR + len(c)/SR,3)] for s, c in spans], open(os.path.join(a.out, "speech.json"), "w"))
    with open(os.path.join(a.out, "transcript.txt"), "w") as f:
        for s in segments:
            if s["text"]: f.write(f"[{fmt(s['s'])}] {s['text']}\n")
    with open(os.path.join(a.out, "transcript.srt"), "w") as f:
        n = 0
        for s in segments:
            if not s["text"]: continue
            n += 1
            f.write(f"{n}\n{fmt(s['s'], True)} --> {fmt(s['e'], True)}\n{s['text']}\n\n")
    el = time.time() - t0
    print(f"DONE {len(words)} words, {len(segments)} segments, {el/60:.1f} min total, RTF {el/total:.3f}", flush=True)

if __name__ == "__main__":
    main()
