#!/usr/bin/env python3
"""Re-transcribe one passage of a long recording with short chunks and splice the result into words.json.

Why: on a bilingual speaker, long ASR chunks can switch language mid-sentence (French heard as English)
and blur word boundaries. A clip only needs a few minutes to be right: re-running those minutes with
6-second chunks fixes most of it, at a small cost.

Usage:
  refine_span.py words.json AUDIO START END [--max-speech 6] [--pad 0.6]
START and END are seconds or H:MM:SS on the transcript timeline. The original file is kept once as
words.orig.json. Needs transcribe.py next to this script (same model environment variables).
"""
import argparse, json, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))

def secs(x):
    if ":" in str(x):
        p = [float(v) for v in str(x).split(":")]
        return sum(v * 60 ** i for i, v in enumerate(reversed(p)))
    return float(x)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words"); ap.add_argument("audio"); ap.add_argument("start"); ap.add_argument("end")
    ap.add_argument("--max-speech", type=float, default=6.0); ap.add_argument("--pad", type=float, default=0.6)
    a = ap.parse_args()
    S, E = secs(a.start), secs(a.end)
    A = max(0.0, S - a.pad)
    orig = a.words.replace(".json", ".orig.json")
    if not os.path.exists(orig):
        shutil.copy(a.words, orig)
    words = json.load(open(a.words))
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "span.wav")
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{A:.3f}", "-i", a.audio, "-t", f"{E + a.pad - A:.3f}",
                        "-ac", "1", "-ar", "16000", wav], check=True)
        r = subprocess.run([sys.executable, os.path.join(HERE, "transcribe.py"), wav, td, "--max-speech", str(a.max_speech)],
                           capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stderr[-2000:])
        new = json.load(open(os.path.join(td, "words.json")))
    new = [{"w": w["w"], "s": round(w["s"] + A, 3), "e": round(w["e"] + A, 3)} for w in new]
    mid = lambda w: (w["s"] + w["e"]) / 2
    new = [w for w in new if S <= mid(w) <= E]
    before = [w for w in words if mid(w) < S]
    after = [w for w in words if mid(w) > E]
    old = [w for w in words if S <= mid(w) <= E]
    json.dump(before + new + after, open(a.words, "w"), ensure_ascii=False)
    print(json.dumps({"span": [S, E], "old_words": len(old), "new_words": len(new)}))
    print("OLD:", " ".join(w["w"] for w in old)[:600])
    print("NEW:", " ".join(w["w"] for w in new)[:600])

if __name__ == "__main__":
    main()
