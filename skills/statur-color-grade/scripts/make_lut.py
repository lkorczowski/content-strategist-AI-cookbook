#!/usr/bin/env python3
"""Write a 3D LUT (.cube) from a few readable grade settings, so a look is a small JSON file in the
brand repo instead of a binary preset with an unknown license.

Order of operations (colorists' order): exposure and white balance, contrast around middle grey,
black and white points, saturation with skin protection, split toning, highlight roll-off.

Usage:
  make_lut.py OUT.cube [--size 33] [--exposure 0.0] [--temp 0.0] [--tint 0.0] [--contrast 1.0] [--pivot 0.42]
              [--black 0.0] [--white 1.0] [--sat 1.0] [--skin-protect 0.5] [--shadows "0,0,0"] [--highlights "0,0,0"]
              [--rolloff 0.0] [--preset name] [--json grade.json]
temp > 0 warms (more red, less blue); tint > 0 adds magenta. shadows/highlights are RGB offsets (-0.05 to 0.05).
"""
import argparse, json
import numpy as np

PRESETS = {
    # natural: keeps skin true, adds a little density; the safe default for founders on camera
    "natural": dict(contrast=1.06, pivot=0.42, black=0.012, sat=1.04, skin_protect=0.6, rolloff=0.15),
    # editorial: denser, slightly warm highlights and cool shadows, for brands with dark interfaces
    "editorial": dict(contrast=1.12, pivot=0.40, black=0.02, sat=0.96, skin_protect=0.7, shadows=[-0.006, 0.004, 0.012],
                      highlights=[0.014, 0.006, -0.01], rolloff=0.25),
}

def srgb_to_lin(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)

def lin_to_srgb(x):
    x = np.clip(x, 0, None)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)

def grade(rgb, p):
    x = srgb_to_lin(rgb) * (2 ** p["exposure"])
    wb = np.array([1 + 0.5 * p["temp"] + 0.25 * p["tint"], 1 - 0.5 * p["tint"], 1 - 0.5 * p["temp"] + 0.25 * p["tint"]])
    x = x * wb
    y = lin_to_srgb(x)
    # contrast: smooth S around the pivot in display space
    c, pv = p["contrast"], p["pivot"]
    y = np.where(y < pv, pv * (y / pv) ** c, 1 - (1 - pv) * ((1 - y) / (1 - pv)) ** c)
    # black and white points
    y = p["black"] + (p["white"] - p["black"]) * y
    # saturation with skin protection (skin hue: red > green > blue, moderate saturation)
    lum = (0.2126 * y[..., 0] + 0.7152 * y[..., 1] + 0.0722 * y[..., 2])[..., None]
    r, g, b = y[..., 0], y[..., 1], y[..., 2]
    skin = np.clip(((r > g) & (g > b)).astype(float) * (1 - np.abs((r - g) / (r - b + 1e-6) - 0.45) * 2), 0, 1)[..., None]
    s = p["sat"] * (1 - p["skin_protect"] * skin) + 1.0 * p["skin_protect"] * skin
    y = lum + (y - lum) * s
    # split toning by luminance
    sh = np.array(p["shadows"]); hi = np.array(p["highlights"])
    w_sh = np.clip(1 - lum / 0.5, 0, 1); w_hi = np.clip((lum - 0.5) / 0.5, 0, 1)
    y = y + w_sh * sh + w_hi * hi
    # highlight roll-off above 0.8
    if p["rolloff"] > 0:
        k = p["rolloff"]; t = 0.8
        y = np.where(y > t, t + (1 - t) * np.tanh((y - t) / (1 - t) * (1 + k)) / np.tanh(1 + k), y)
    return np.clip(y, 0, 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--size", type=int, default=33)
    for k, d in (("exposure", 0.0), ("temp", 0.0), ("tint", 0.0), ("contrast", 1.0), ("pivot", 0.42), ("black", 0.0), ("white", 1.0),
                 ("sat", 1.0), ("skin-protect", 0.5), ("rolloff", 0.0)):
        ap.add_argument("--" + k, type=float, default=None)
    ap.add_argument("--shadows", default=None); ap.add_argument("--highlights", default=None)
    ap.add_argument("--preset", default=None, choices=list(PRESETS)); ap.add_argument("--json", default=None)
    a = ap.parse_args()
    p = dict(exposure=0.0, temp=0.0, tint=0.0, contrast=1.0, pivot=0.42, black=0.0, white=1.0, sat=1.0, skin_protect=0.5,
             shadows=[0, 0, 0], highlights=[0, 0, 0], rolloff=0.0)
    if a.preset:
        p.update(PRESETS[a.preset])
    if a.json:
        p.update(json.load(open(a.json)))
    for k in ("exposure", "temp", "tint", "contrast", "pivot", "black", "white", "sat", "rolloff"):
        v = getattr(a, k)
        if v is not None:
            p[k] = v
    if a.skin_protect is not None:
        p["skin_protect"] = a.skin_protect
    if a.shadows:
        p["shadows"] = [float(v) for v in a.shadows.split(",")]
    if a.highlights:
        p["highlights"] = [float(v) for v in a.highlights.split(",")]
    n = a.size
    g = np.linspace(0, 1, n)
    b, gg, r = np.meshgrid(g, g, g, indexing="ij")      # .cube order: red varies fastest
    rgb = np.stack([r, gg, b], -1).reshape(-1, 3)
    out = grade(rgb, p)
    with open(a.out, "w") as f:
        f.write(f"TITLE \"statur grade\"\n# {json.dumps(p)}\nLUT_3D_SIZE {n}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n")
        for row in out:
            f.write(f"{row[0]:.6f} {row[1]:.6f} {row[2]:.6f}\n")
    print(json.dumps({"status": "DONE", "out": a.out, "settings": p}))

if __name__ == "__main__":
    main()
