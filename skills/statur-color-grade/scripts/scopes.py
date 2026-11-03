#!/usr/bin/env python3
"""Measure a few frames of a video: luminance levels, white balance of neutral areas, and the skin hue of
the face against the skin-tone line of a vectorscope. Prints numbers an agent can act on, and writes a
sheet with each frame, its vectorscope and the skin line.

Skin-tone line ("I line"): about 123 degrees on a vectorscope (Cb, Cr plane, 0 degrees = +Cb axis,
counter-clockwise). Healthy skin of any complexion sits within about +-10 degrees of it; saturation varies.

Usage: scopes.py VIDEO --times 2,30,60 [--lut grade.cube] [--sheet scopes.jpg] [--matte MATTE] [--json out.json]
"""
import argparse, json, math, subprocess
import numpy as np
import cv2

def grab(path, t, lut=None, gray=False):
    vf = [f"lut3d=file='{lut}':interp=tetrahedral"] if lut else []
    vf.append("format=" + ("gray" if gray else "rgb24"))
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-vf", ",".join(vf),
                        "-f", "rawvideo", "-"], capture_output=True)
    pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
                        capture_output=True, text=True)
    w, h = [int(v) for v in pr.stdout.strip().split(",")[:2]]
    return np.frombuffer(r.stdout, np.uint8).reshape(h, w) if gray else np.frombuffer(r.stdout, np.uint8).reshape(h, w, 3)

def skin_mask(Y, Cb, Cr, matte=None):
    """Skin-coloured pixels (YCbCr box that holds most complexions), inside the person matte when given,
    restricted to the upper part of the person so hands and arms weigh less."""
    m = (Cr > 0.015) & (Cr < 0.17) & (Cb > -0.16) & (Cb < 0.01) & (Y > 0.18) & (Y < 0.92)
    if matte is not None:
        p = matte > 128
        m &= p
        ys = np.where(p.any(axis=1))[0]
        if len(ys):
            top, bot = ys[0], ys[-1]
            m[int(top + 0.65 * (bot - top)):] = False
    return m

def face_box(img):
    path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml" if hasattr(cv2, "data") else ""
    import os
    if not os.path.exists(path):
        return None
    cc = cv2.CascadeClassifier(path)
    g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    fs = cc.detectMultiScale(g, 1.1, 6, minSize=(160, 160))
    if len(fs) == 0:
        return None
    x, y, w, h = max(fs, key=lambda f: f[2] * f[3])
    return int(x + w * 0.25), int(y + h * 0.45), int(w * 0.5), int(h * 0.3)   # cheeks and nose, away from glasses and hair

def ycc(img):
    f = img.astype(np.float32) / 255.0
    Y = 0.2126 * f[..., 0] + 0.7152 * f[..., 1] + 0.0722 * f[..., 2]
    Cb = (f[..., 2] - Y) / 1.8556; Cr = (f[..., 0] - Y) / 1.5748
    return Y, Cb, Cr

def scope_img(Cb, Cr, size=300):
    im = np.zeros((size, size, 3), np.uint8)
    xs = np.clip((Cb.ravel() * 2 + 0.5) * size, 0, size - 1).astype(int); ys = np.clip((0.5 - Cr.ravel() * 2) * size, 0, size - 1).astype(int)
    acc = np.zeros((size, size), np.float32); np.add.at(acc, (ys, xs), 1)
    acc = np.log1p(acc); acc = (acc / (acc.max() + 1e-9) * 255).astype(np.uint8)
    im[..., 1] = acc; im[..., 0] = acc // 2; im[..., 2] = acc // 3
    c = size // 2; ang = math.radians(123)
    cv2.line(im, (c, c), (int(c + math.cos(ang) * c), int(c - math.sin(ang) * c)), (232, 80, 28), 1)
    cv2.circle(im, (c, c), c - 1, (90, 90, 90), 1)
    return im

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--times", default="2,30,60"); ap.add_argument("--lut", default=None)
    ap.add_argument("--sheet", default=None); ap.add_argument("--json", default=None)
    ap.add_argument("--matte", default=None, help="person matte video (same timeline) to find skin on the speaker only")
    a = ap.parse_args()
    res, tiles = [], []
    for t in [float(x) for x in a.times.split(",")]:
        img = grab(a.video, t, a.lut)
        Y, Cb, Cr = ycc(img)
        r = {"t": t, "y_p2": round(float(np.percentile(Y, 2)), 3), "y_p50": round(float(np.percentile(Y, 50)), 3),
             "y_p98": round(float(np.percentile(Y, 98)), 3), "clipped_pct": round(float((img.max(axis=2) >= 250).mean() * 100), 2)}
        fb = face_box(img)
        mt = grab(a.matte, t, gray=True) if a.matte else None
        sm_ = skin_mask(Y, Cb, Cr, mt)
        if fb is None and sm_.sum() > 2000:
            cb, cr = float(Cb[sm_].mean()), float(Cr[sm_].mean())
            hue = (math.degrees(math.atan2(cr, cb)) + 360) % 360
            r.update({"skin_hue_deg": round(hue, 1), "skin_off_line_deg": round(hue - 123, 1), "skin_sat": round(math.hypot(cb, cr), 4),
                      "skin_y": round(float(Y[sm_].mean()), 3), "skin_px": int(sm_.sum()), "method": "skin mask" + (" in matte" if mt is not None else "")})
            img = img.copy(); img[sm_] = (img[sm_] * 0.5 + np.array([232, 80, 28]) * 0.5).astype(np.uint8)
        if fb:
            x, y, w, h = fb
            cb, cr = float(Cb[y:y + h, x:x + w].mean()), float(Cr[y:y + h, x:x + w].mean())
            hue = (math.degrees(math.atan2(cr, cb)) + 360) % 360
            r.update({"skin_hue_deg": round(hue, 1), "skin_off_line_deg": round(hue - 123, 1), "skin_sat": round(math.hypot(cb, cr), 4),
                      "skin_y": round(float(Y[y:y + h, x:x + w].mean()), 3)})
            cv2.rectangle(img, (x, y), (x + w, y + h), (232, 80, 28), 4)
        res.append(r)
        if a.sheet:
            sm = cv2.resize(img, (300, int(300 * img.shape[0] / img.shape[1])))
            sc = scope_img(Cb, Cr)
            tile = np.zeros((sm.shape[0] + 300, 300, 3), np.uint8); tile[:sm.shape[0]] = sm; tile[sm.shape[0]:] = sc
            tiles.append(tile)
    if a.sheet and tiles:
        cv2.imwrite(a.sheet, cv2.cvtColor(np.concatenate(tiles, axis=1), cv2.COLOR_RGB2BGR))
    out = {"video": a.video, "lut": a.lut, "frames": res}
    if a.json:
        json.dump(out, open(a.json, "w"), indent=1)
    print(json.dumps(out))

if __name__ == "__main__":
    main()
