#!/usr/bin/env python3
"""Make the picture plate of a recording: decode, tone map HDR to SDR when needed, apply a grade LUT,
and write an SDR BT.709 file that every later step reads (matting, compositing, review).

Phones record HDR by default (iPhone: HEVC 10 bit, BT.2020, HLG). Platforms show an HDR upload in HDR
on some phones and badly tone-mapped on others, and every overlay (captions, screenshots, motion design)
is designed in SDR. So the plate is SDR, made once, with a known tone map.

Usage:
  plate.py SRC OUT.mp4 [--lut grade.cube] [--tonemap mobius|hable|reinhard|none] [--npl 203]
           [--w 1080 --h 1920] [--fps 30] [--crf 12] [--start S --dur D]
Prints a JSON line with what it detected and did.
"""
import argparse, json, subprocess, sys

def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,pix_fmt,color_transfer,color_primaries,color_space,r_frame_rate",
                        "-of", "json", path], capture_output=True, text=True)
    return json.loads(r.stdout)["streams"][0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--lut", default=None, help=".cube 3D LUT applied after the tone map (statur-color-grade make_lut.py)")
    ap.add_argument("--tonemap", default="mobius", choices=["mobius", "hable", "reinhard", "none"])
    ap.add_argument("--npl", type=float, default=203.0, help="nominal peak luminance; 203 = HDR reference white (ITU-R BT.2408)")
    ap.add_argument("--param", type=float, default=0.3, help="tone map parameter (mobius: knee, reinhard: contrast)")
    ap.add_argument("--w", type=int, default=0); ap.add_argument("--h", type=int, default=0)
    ap.add_argument("--fps", type=float, default=0)
    ap.add_argument("--crf", type=int, default=12)
    ap.add_argument("--preset", default="veryfast")
    ap.add_argument("--start", type=float, default=0); ap.add_argument("--dur", type=float, default=0)
    ap.add_argument("--no-audio", action="store_true")
    a = ap.parse_args()
    s = probe(a.src)
    trc = s.get("color_transfer", "")
    hdr = trc in ("arib-std-b67", "smpte2084")
    chain = []
    if hdr and a.tonemap != "none":
        prim = s.get("color_primaries", "bt2020")
        chain += [f"zscale=t=linear:npl={a.npl:g}", "format=gbrpf32le", "zscale=p=bt709",
                  f"tonemap={a.tonemap}:desat=0" + (f":param={a.param:g}" if a.tonemap in ("mobius", "reinhard") else ""),
                  "zscale=t=bt709:m=bt709:r=tv", "format=gbrp"]
    elif hdr:
        chain += ["zscale=t=bt709:m=bt709:p=bt709:r=tv", "format=gbrp"]
    if a.lut:
        chain.append(f"lut3d=file='{a.lut}':interp=tetrahedral")
    if a.w and a.h:
        chain.append(f"scale={a.w}:{a.h}:flags=lanczos")
    if a.fps:
        chain.append(f"fps={a.fps:g}")
    chain += ["format=yuv420p"]
    cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error"]
    if a.start:
        cmd += ["-ss", f"{a.start:.3f}"]
    cmd += ["-i", a.src]
    if a.dur:
        cmd += ["-t", f"{a.dur:.3f}"]
    cmd += ["-vf", ",".join(chain), "-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]
    cmd += ["-an"] if a.no_audio else ["-c:a", "pcm_s16le", "-ar", "48000"]
    out = a.out
    if not a.no_audio and out.endswith(".mp4"):
        out = out[:-4] + ".mov"          # PCM audio needs MOV/MKV
    r = subprocess.run(cmd + [out], capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stderr[-3000:]); sys.exit(1)
    print(json.dumps({"status": "DONE", "out": out, "hdr_in": hdr, "transfer_in": trc, "tonemap": a.tonemap if hdr else None,
                      "lut": a.lut, "size": [s["width"], s["height"]]}))

if __name__ == "__main__":
    main()
