#!/usr/bin/env python3
"""Measure the editing style of a reference video the user likes, so the edit can match its pace with
numbers instead of adjectives. Needs a file the user is allowed to use (their own export, a video they
saved with the platform's own download, a client's master). Without a file, watch the video, step
through it, and fill the same style card by hand.

Measures: cut and scene changes (count, per 10 s, median shot length), visual change rate, share of
frames where a face fills the frame (talking head vs inserts), loudness and loudness range, words per
second when a transcript is given. Writes a contact sheet of the frame after each change so the agent can
name what each insert is (screen capture, stock, motion graphic, caption style).

Usage: style_probe.py REF.mp4 --out style.json [--sheet style_sheet.jpg] [--threshold 0.32] [--words words.json]
"""
import argparse, json, re, subprocess
import numpy as np
import cv2

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ref"); ap.add_argument("--out", required=True); ap.add_argument("--sheet", default=None)
    ap.add_argument("--threshold", type=float, default=0.32); ap.add_argument("--words", default=None)
    a = ap.parse_args()
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", a.ref], capture_output=True, text=True).stdout)
    dur = float(pr["format"]["duration"])
    # scene changes with ffmpeg's scdet score
    e = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", a.ref, "-an", "-vf", f"scale=270:-2,scdet=threshold={a.threshold * 100:g}", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    cuts = [float(x) for x in re.findall(r"lavfi\.scd\.time: ([\d.]+)", e)]
    shots = np.diff([0.0] + cuts + [dur]) if dur else np.array([])
    # visual change rate and face share on small frames, 5 per second
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", a.ref, "-vf", "fps=5,scale=108:192", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    fr = np.frombuffer(r.stdout, np.uint8).reshape(-1, 192, 108, 3).astype(np.float32)
    diff = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2, 3)) if len(fr) > 1 else np.array([0.0])
    events = int((diff > 18).sum())
    f = fr / 255.0
    Y = 0.2126 * f[..., 0] + 0.7152 * f[..., 1] + 0.0722 * f[..., 2]
    Cb = (f[..., 2] - Y) / 1.8556; Cr = (f[..., 0] - Y) / 1.5748
    skin = ((Cr > 0.015) & (Cr < 0.17) & (Cb > -0.16) & (Cb < 0.01) & (Y > 0.18) & (Y < 0.92)).mean(axis=(1, 2))
    talking = float((skin > 0.08).mean()) if len(skin) else 0.0
    lo = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-i", a.ref, "-vn", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", lo); LRA = re.findall(r"LRA:\s+([\d.]+) LU", lo)
    style = {"file": a.ref, "duration": round(dur, 2), "cuts": len(cuts), "cuts_per_10s": round(len(cuts) / max(dur, 1e-6) * 10, 2),
             "median_shot_s": round(float(np.median(shots)), 2) if len(shots) else None,
             "visual_changes_per_10s": round(events / max(dur, 1e-6) * 10, 2), "face_frame_share": round(talking, 2),
             "lufs": float(I[-1]) if I else None, "lra": float(LRA[-1]) if LRA else None, "cut_times": [round(c, 2) for c in cuts]}
    if a.words:
        w = json.load(open(a.words))
        if w:
            style["words_per_s"] = round(len(w) / max(w[-1]["e"] - w[0]["s"], 1e-6), 2)
    if a.sheet:
        ts = ([0.3] + [c + 0.15 for c in cuts])[:40]
        tiles = []
        for t in ts:
            rr = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.2f}", "-i", a.ref, "-frames:v", "1", "-vf", "scale=180:320", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True)
            if len(rr.stdout) == 180 * 320 * 3:
                im = np.frombuffer(rr.stdout, np.uint8).reshape(320, 180, 3).copy()
                cv2.putText(im, f"{t:.1f}", (4, 312), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (28, 80, 232), 2); tiles.append(im)
        while len(tiles) % 10:
            tiles.append(np.zeros((320, 180, 3), np.uint8))
        if tiles:
            cv2.imwrite(a.sheet, np.concatenate([np.concatenate(tiles[k:k + 10], axis=1) for k in range(0, len(tiles), 10)], axis=0))
            style["sheet"] = a.sheet
    style["read_me"] = ("Look at the sheet and write the style card: hook layout, caption style (size, position, emphasis), "
                        "insert types and how often, motion design vocabulary, sound effects you can see as visual events, music, color look. "
                        "Then pick the production level and the parameters that match (cuts per 10 s, inserts per minute).")
    json.dump(style, open(a.out, "w"), indent=1)
    print(json.dumps({k: style[k] for k in style if k not in ("cut_times", "read_me")}))

if __name__ == "__main__":
    main()
