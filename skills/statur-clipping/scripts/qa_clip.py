#!/usr/bin/env python3
"""Quality check of a rendered clip.
- Re-transcribes the clip (same local model) and aligns it with the words the edit meant to keep.
  Words lost or mangled near a cut show up as gaps: the usual sign of a cut placed too tight.
- Measures integrated loudness and true peak, duration, resolution and frame rate.
Usage: qa_clip.py CLIP.mp4 words_out.json [--report qa.json]
"""
import argparse, difflib, json, os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

def norm(w):
    w = w.lower()
    w = re.sub(r"[^\w'’-]+", "", w)
    return w.replace("’", "'")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("clip"); ap.add_argument("words_out"); ap.add_argument("--report")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run([sys.executable, os.path.join(HERE, "transcribe.py"), a.clip, td, "--max-speech", "15"],
                           capture_output=True, text=True)
        if r.returncode:
            print(r.stderr[-2000:]); sys.exit(1)
        heard = json.load(open(os.path.join(td, "words.json")))
    meant = [w for w in json.load(open(a.words_out)) if norm(w["w"])]   # punctuation-only tokens carry no sound
    heard = [w for w in heard if norm(w["w"])]
    A = [norm(w["w"]) for w in meant]; B = [norm(w["w"]) for w in heard]
    sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
    issues = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        t = meant[i1]["s"] if i1 < len(meant) else (meant[-1]["e"] if meant else 0)
        issues.append({"at": round(t, 2), "type": tag, "meant": " ".join(x["w"] for x in meant[i1:i2]),
                       "heard": " ".join(x["w"] for x in heard[j1:j2])})
    ratio = sm.ratio()
    lr = subprocess.run(["ffmpeg", "-nostdin", "-v", "info", "-i", a.clip, "-af", "ebur128=peak=true", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", lr); TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", lr)
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", a.clip],
                                   capture_output=True, text=True).stdout)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    rep = {"match_ratio": round(ratio, 3), "issues": issues, "lufs": float(I[-1]) if I else None,
           "true_peak": float(TP[-1]) if TP else None, "duration": float(pr["format"]["duration"]),
           "size": [v["width"], v["height"]], "fps": v.get("avg_frame_rate")}
    if a.report:
        json.dump(rep, open(a.report, "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: rep[k] for k in ("match_ratio", "lufs", "true_peak", "duration", "size", "fps")}, ensure_ascii=False))
    for x in issues[:40]:
        print(f"  {x['at']:7.2f}s {x['type']:8s} meant: {x['meant'][:60]!r} | heard: {x['heard'][:60]!r}")

if __name__ == "__main__":
    main()
