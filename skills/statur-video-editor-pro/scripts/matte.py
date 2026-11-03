#!/usr/bin/env python3
"""Person matte (alpha) for every frame of a talking-head video, on a CPU, with no green screen.

Backend: Robust Video Matting (RVM, ONNX export of the MobileNetV3 or ResNet50 model). It is
recurrent: it keeps state from frame to frame, so hair edges stay stable instead of flickering.
The matte is what makes the pro effects possible: background replacement, text behind the speaker,
a cut-out of the speaker over B-roll, a shadow under the speaker.

Output: a grayscale video (FFV1, lossless) with the same size, frame rate and frame count as the input.

Usage:
  matte.py PLATE.mp4 MATTE.mkv --model rvm_mobilenetv3_fp32.onnx [--ratio 0.25] [--preview prev.mp4]

Speed on 2 cloud vCPUs, 1080x1920, ratio 0.25, MobileNetV3: about 3.5 frames per second end to end
(decode, model, encode; the model alone runs near 6). ResNet50 is about 3 times slower with better hair.
License: RVM is GPL-3.0 (code and weights). Running it as a tool is fine; if you redistribute a modified
RVM, follow the GPL. MediaPipe Selfie Segmentation (Apache-2.0) is a lighter fallback with coarser hair.
"""
import argparse, json, subprocess, sys, time
import numpy as np

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                        "stream=width,height,r_frame_rate,nb_read_packets", "-of", "json", path], capture_output=True, text=True)
    s = json.loads(r.stdout)["streams"][0]
    n, d = s["r_frame_rate"].split("/")
    return int(s["width"]), int(s["height"]), float(n) / float(d), int(s.get("nb_read_packets") or 0)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--model", required=True)
    ap.add_argument("--ratio", type=float, default=0.0, help="downsample ratio; 0 = auto (0.25 for HD, 0.4 for SD)")
    ap.add_argument("--threads", type=int, default=0)
    ap.add_argument("--preview", default=None, help="also write a checkerboard preview (speaker over grey) at 540 px wide")
    a = ap.parse_args()
    import onnxruntime as ort
    W, H, fps, n = probe(a.src)
    ratio = a.ratio or (0.25 if max(W, H) >= 1280 else 0.4)
    so = ort.SessionOptions()
    if a.threads:
        so.intra_op_num_threads = a.threads
    sess = ort.InferenceSession(a.model, so, providers=["CPUExecutionProvider"])
    dec = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", a.src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}",
                            "-r", f"{fps:g}", "-i", "-", "-c:v", "ffv1", "-pix_fmt", "gray", a.out], stdin=subprocess.PIPE)
    prev = None
    if a.preview:
        pw, ph = 540, int(round(540 * H / W / 2) * 2)
        prev = subprocess.Popen(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{pw}x{ph}",
                                 "-r", f"{fps:g}", "-i", "-", "-c:v", "libx264", "-crf", "26", "-pix_fmt", "yuv420p", a.preview],
                                stdin=subprocess.PIPE)
    rec = [np.zeros((1, 1, 1, 1), np.float32)] * 4
    dr = np.array([ratio], np.float32)
    fsz = W * H * 3
    i, t0 = 0, time.time()
    while True:
        buf = dec.stdout.read(fsz)
        if len(buf) < fsz:
            break
        img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        src = (img.astype(np.float32) / 255.0).transpose(2, 0, 1)[None]
        fgr, pha, *rec = sess.run(None, {"src": src, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3], "downsample_ratio": dr})
        alpha = np.clip(pha[0, 0] * 255.0 + 0.5, 0, 255).astype(np.uint8)
        enc.stdin.write(alpha.tobytes())
        if prev:
            import cv2
            small = cv2.resize(img, (pw, ph), interpolation=cv2.INTER_AREA).astype(np.float32)
            al = cv2.resize(alpha, (pw, ph), interpolation=cv2.INTER_AREA).astype(np.float32)[..., None] / 255.0
            comp = small * al + np.array([60, 200, 90], np.float32) * (1 - al)
            prev.stdin.write(comp.astype(np.uint8).tobytes())
        i += 1
        if i % 150 == 0:
            el = time.time() - t0
            print(json.dumps({"frames": i, "of": n, "fps": round(i / el, 2)}), flush=True)
    for p in (enc, prev):
        if p:
            p.stdin.close(); p.wait()
    dec.wait()
    print(json.dumps({"status": "DONE", "frames": i, "ratio": ratio, "seconds": round(time.time() - t0, 1), "out": a.out}))

if __name__ == "__main__":
    main()
