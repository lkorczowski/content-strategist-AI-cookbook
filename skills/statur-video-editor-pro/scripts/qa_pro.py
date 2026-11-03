#!/usr/bin/env python3
"""Quality gate of a pro edit. Measures what a reviewer would check, writes a contact sheet the agent must
look at, and returns PASS, PASS_WITH_NOTES or REFUSE with reasons. An edit that fails a hard check is not
delivered as ready to post.

Checks
  file       H.264, yuv420p, BT.709 tags, expected size and frame rate, duration
  loudness   integrated -15 to -13 LUFS, true peak at most -1.0 dBTP
  picture    black or frozen stretches longer than 0.5 s outside the planned end card
  safe areas over-layer pixels (text, cards) in the platform UI zones, outside full-screen panels:
             top 0-240 px, right column x 960-1080 for y 840-1700, bottom y over 1700 (1080x1920 frame);
             these are the hard UI zones, looser than the target area for text in references/levels.md
  speech     optional: words heard back (qa_clip.py of statur-clipping) at 90% or more
  sheet      16 frames with their times, for the agent to look at

Usage: qa_pro.py MASTER.mp4 --plan plan.json --layers LAYERDIR [--words words_out.json] [--qa-clip PATH] [--out qa.json]
"""
import argparse, json, os, re, subprocess, sys
import numpy as np
import cv2

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("master"); ap.add_argument("--plan", required=True); ap.add_argument("--layers", required=True)
    ap.add_argument("--words", default=None); ap.add_argument("--qa-clip", default=None, help="path to statur-clipping qa_clip.py")
    ap.add_argument("--out", default=None); ap.add_argument("--sheet", default=None)
    a = ap.parse_args()
    P = json.load(open(a.plan)); fps = P["fps"]; W, H = P["w"], P["h"]
    rep = {"master": a.master, "hard": [], "notes": []}
    pr = json.loads(sh(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", a.master]).stdout)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    au = next((s for s in pr["streams"] if s["codec_type"] == "audio"), None)
    dur = float(pr["format"]["duration"])
    rep["file"] = {"codec": v["codec_name"], "pix_fmt": v["pix_fmt"], "size": [v["width"], v["height"]], "fps": v["r_frame_rate"],
                   "color": [v.get("color_primaries"), v.get("color_transfer"), v.get("color_space")], "duration": round(dur, 2),
                   "audio": au["codec_name"] if au else None, "mb": round(os.path.getsize(a.master) / 1e6, 1)}
    if v["codec_name"] != "h264" or v["pix_fmt"] != "yuv420p":
        rep["hard"].append("video is not H.264 yuv420p")
    if [v["width"], v["height"]] != [W, H]:
        rep["hard"].append(f"size {v['width']}x{v['height']} differs from the plan {W}x{H}")
    if v.get("color_transfer") not in ("bt709", None):
        rep["hard"].append(f"transfer {v.get('color_transfer')} (expected bt709 SDR)")
    if abs(dur - P["duration"]) > 0.25:
        rep["notes"].append(f"duration {dur:.2f} s, plan {P['duration']:.2f} s")
    if not au:
        rep["hard"].append("no audio track")
    else:
        e = sh(["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-i", a.master, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
        i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1]); tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])
        rep["loudness"] = {"lufs": i, "true_peak": tp}
        if not -15.0 <= i <= -13.0:
            rep["hard"].append(f"loudness {i} LUFS outside -15 to -13")
        if tp > -1.0:
            rep["hard"].append(f"true peak {tp} dBTP above -1.0")
    e = sh(["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-i", a.master, "-an", "-vf", "blackdetect=d=0.5:pix_th=0.06,freezedetect=n=-55dB:d=0.8", "-f", "null", "-"]).stderr
    blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", e)
    freezes = re.findall(r"freeze_start: ([\d.]+)", e)
    tail0 = P["duration"] - P.get("tail", 0) - 0.1
    blacks = [(float(s), float(t)) for s, t in blacks if float(s) < tail0]
    freezes = [float(s) for s in freezes if float(s) < tail0]
    rep["picture"] = {"black": blacks, "frozen_starts": freezes}
    if blacks:
        rep["hard"].append(f"black stretches at {blacks}")
    if freezes:
        rep["notes"].append(f"frozen stretches start at {freezes} (check: a still card can be intended)")
    # safe areas, from the over layer frames
    od = os.path.join(a.layers, "over"); viol = []
    if os.path.exists(os.path.join(od, "manifest.json")):
        man = json.load(open(os.path.join(od, "manifest.json")))
        for i in man["frames"][::int(fps // 2) or 1]:
            im = cv2.imread(os.path.join(od, f"{i:06d}.png"), cv2.IMREAD_UNCHANGED)
            if im is None or im.shape[2] < 4:
                continue
            al = im[..., 3]
            if (al > 250).mean() > 0.85:
                continue                      # full-screen panel: the platform UI covers it like any picture
            zones = {"top": al[:240, :], "right_column": al[840:1700, 960:], "bottom": al[1700:, :]}
            for k, z in zones.items():
                cov = float((z > 128).mean())
                if cov > 0.004:
                    viol.append({"t": round(i / fps, 2), "zone": k, "coverage": round(cov, 4)})
    rep["safe_areas"] = {"violations": len(viol), "examples": viol[:12]}
    if len(viol) > 6:
        rep["notes"].append(f"{len(viol)} sampled frames put graphics in a platform UI zone (see examples)")
    # speech heard back
    if a.words and a.qa_clip and os.path.exists(a.qa_clip):
        q = sh([sys.executable, a.qa_clip, a.master, a.words, "--report", os.path.splitext(a.master)[0] + "_speech_qa.json"])
        try:
            sq = json.load(open(os.path.splitext(a.master)[0] + "_speech_qa.json"))
            hr = sq.get("match_ratio")
            rep["speech"] = {"match_ratio": hr, "issues": len(sq.get("issues", [])), "examples": sq.get("issues", [])[:8]}
            if hr is not None and hr < 0.9:
                rep["hard"].append(f"only {hr:.0%} of planned words heard back")
        except Exception as ex:
            rep["notes"].append(f"speech check not run: {ex} {q.stderr[-300:]}")
    # contact sheet
    sheet = a.sheet or os.path.splitext(a.master)[0] + "_qa_sheet.jpg"
    ts = np.linspace(0.6, dur - 0.4, 16)
    tiles = []
    for t in ts:
        r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.2f}", "-i", a.master, "-frames:v", "1", "-vf", "scale=270:480",
                            "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True)
        if len(r.stdout) == 270 * 480 * 3:
            im = np.frombuffer(r.stdout, np.uint8).reshape(480, 270, 3).copy()
            cv2.putText(im, f"{t:.1f}s", (6, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (28, 80, 232), 2)
            tiles.append(im)
    if tiles:
        rows = [np.concatenate(tiles[k:k + 8], axis=1) for k in range(0, len(tiles), 8) if len(tiles[k:k + 8]) == 8]
        cv2.imwrite(sheet, np.concatenate(rows, axis=0), [cv2.IMWRITE_JPEG_QUALITY, 88])
        rep["sheet"] = sheet
    rep["status"] = "REFUSE" if rep["hard"] else ("PASS_WITH_NOTES" if rep["notes"] else "PASS")
    out = a.out or os.path.splitext(a.master)[0] + "_qa.json"
    json.dump(rep, open(out, "w"), indent=1)
    print(json.dumps({k: rep[k] for k in ("status", "hard", "notes")} | {"loudness": rep.get("loudness"), "sheet": rep.get("sheet")}))

if __name__ == "__main__":
    main()
