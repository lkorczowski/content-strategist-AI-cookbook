#!/usr/bin/env python3
"""Composite the pro edit: cut A-roll (graded plate), person matte, background layer, layer behind the
speaker, B-roll inserts, motion-design layer on top, then encode the master.

Order per frame:
  1. base     = background layer frame where the plan says "keyed", else the plate itself
  2. under    = motion layer drawn on the base, behind the speaker (text behind the subject)
  3. subject  = plate x matte drawn on top again, so the speaker stays in front of "under"
                (keyed ranges: the subject can be scaled around an anchor, subject_keys)
  4. camera   = punch-ins and moves on the whole picture outside keyed ranges (camera_keys)
  5. inserts  = full-screen or framed B-roll videos and stills
  6. over     = motion layer on top (captions, cards, end card)

Usage:
  composite.py --plate PLATE --matte MATTE.mkv --plan plan.json --layers LAYERDIR --out OUT.mp4
               [--lut grade.cube] [--audio mix.wav] [--crf 16] [--preset medium] [--only 100-200] [--stills DIR]
"""
import argparse, json, math, os, subprocess, sys, time
import numpy as np
import cv2

EASE = {
    "linear": lambda k: k,
    "inOutCubic": lambda k: 4 * k ** 3 if k < 0.5 else 1 - (-2 * k + 2) ** 3 / 2,
    "outCubic": lambda k: 1 - (1 - k) ** 3,
    "outQuint": lambda k: 1 - (1 - k) ** 5,
    "outBack": lambda k: 1 + 2.70158 * (k - 1) ** 3 + 1.70158 * (k - 1) ** 2,
}

def keyed_value(keys, t, field, default):
    """Piecewise keyframes: each key moves the value to key[field] over key['dur'] starting at key['t']."""
    v = default
    for k in keys:
        if field not in k:
            continue
        if t < k["t"]:
            break
        q = min(1.0, (t - k["t"]) / max(k.get("dur", 0.3), 1e-6))
        v = v + (k[field] - v) * EASE.get(k.get("ease", "inOutCubic"), EASE["inOutCubic"])(q)
    return v

def in_ranges(t, rs):
    return any(a <= t < b for a, b in rs)

def cut_stream(src, mapping, fps, tail, pix, vf_extra=""):
    """ffmpeg process that outputs the kept frames of SRC in output order, then holds the last frame for tail s.
    Chronological pieces use one select filter (each frame decoded once). Pieces out of order (a cold open)
    fall back to split + trim, which processes the source once per piece."""
    ranges = [(int(round(m["src_s"] * fps)), int(round((m["src_e"] - m["src_s"]) * fps))) for m in mapping]
    chrono = all(ranges[i][0] + ranges[i][1] <= ranges[i + 1][0] for i in range(len(ranges) - 1))
    if chrono:
        expr = "+".join(f"between(n,{a},{a + n - 1})" for a, n in ranges)
        fc = f"[0:v]fps={fps:g},select='{expr}',setpts=N/FRAME_RATE/TB{(',' + vf_extra) if vf_extra else ''}"
    else:
        parts, labels = [], []
        for i, (a, n) in enumerate(ranges):
            parts.append(f"[v{i}]trim=start_frame={a}:end_frame={a + n},setpts=PTS-STARTPTS[p{i}]")
            labels.append(f"[p{i}]")
        k = len(ranges)
        fc = f"[0:v]fps={fps:g},split={k}" + "".join(f"[v{i}]" for i in range(k)) + ";" + ";".join(parts)
        fc += ";" + "".join(labels) + f"concat=n={k}:v=1:a=0" + (f",{vf_extra}" if vf_extra else "")
    if tail > 0:
        fc += f",tpad=stop_mode=clone:stop_duration={tail:.3f}"
    fc += f",format={pix}[out]"
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-i", src, "-filter_complex", fc, "-map", "[out]", "-f", "rawvideo", "-pix_fmt", pix, "-"]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10 ** 8)

class Layer:
    def __init__(self, d):
        self.d = d; self.ok = bool(d) and os.path.exists(os.path.join(d, "manifest.json"))
        self.frames, self.fmt = set(), "png"
        if self.ok:
            m = json.load(open(os.path.join(d, "manifest.json")))
            self.frames, self.fmt = set(m["frames"]), m["format"]
    def get(self, i):
        if not self.ok or i not in self.frames:
            return None
        im = cv2.imread(os.path.join(self.d, f"{i:06d}.{self.fmt}"), cv2.IMREAD_UNCHANGED)
        if im is None:
            return None
        if im.shape[2] == 4:
            return cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA)
        return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

def over(dst, rgba):
    """Alpha-composite an RGBA uint8 image onto a float32 RGB image in place, only inside the box where
    the layer has pixels (a caption-only frame touches a few percent of the picture)."""
    al = rgba[..., 3]
    x, y, w, h = cv2.boundingRect((al > 0).astype(np.uint8))
    if w == 0 or h == 0:
        return dst
    a = al[y:y + h, x:x + w, None].astype(np.float32) * (1.0 / 255.0)
    roi = dst[y:y + h, x:x + w]
    roi *= (1.0 - a)
    roi += rgba[y:y + h, x:x + w, :3].astype(np.float32) * a
    return dst

class Insert:
    def __init__(self, spec, fps, W, H):
        self.s = spec; self.fps = fps; self.W, self.H = W, H
        self.cap = None; self.still = None; self.last = None; self.idx = -1
        f = spec["file"]
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            im = cv2.imread(f, cv2.IMREAD_COLOR); self.still = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        else:
            self.cap = cv2.VideoCapture(f); self.src_fps = self.cap.get(cv2.CAP_PROP_FPS) or fps
            self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
    def frame(self, lt):
        if self.still is not None:
            return self.still
        want = int((lt + self.s.get("seek", 0)) * self.src_fps)
        want = min(max(0, want), self.n - 1)
        while self.idx < want:
            ok, im = self.cap.read()
            if not ok:
                break
            self.idx += 1; self.last = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        return self.last
    def draw(self, dst, t):
        lt = t - self.s["start"]; dur = self.s["end"] - self.s["start"]
        img = self.frame(lt)
        if img is None:
            return dst
        r = self.s.get("rect", "full")
        x, y, w, h = (0, 0, self.W, self.H) if r == "full" else r
        ih, iw = img.shape[:2]
        sc = max(w / iw, h / ih) * self.s.get("zoom", 1.0)
        kb = self.s.get("ken_burns", 0.0)                       # slow push-in over the insert
        sc *= 1.0 + kb * (lt / max(dur, 1e-6))
        rw, rh = int(math.ceil(iw * sc)), int(math.ceil(ih * sc))
        res = cv2.resize(img, (rw, rh), interpolation=cv2.INTER_LANCZOS4 if sc > 1 else cv2.INTER_AREA)
        ox, oy = (rw - w) // 2, int((rh - h) * self.s.get("focus_y", 0.5))
        tile = res[oy:oy + h, ox:ox + w].astype(np.float32)
        tin, tout = self.s.get("in", 0.25), self.s.get("out", 0.2)
        k = 1.0
        mode = self.s.get("transition", "slide")
        if mode == "fade":
            k = min(1.0, lt / max(tin, 1e-6), (dur - lt) / max(tout, 1e-6))
            k = max(0.0, k)
            dst[y:y + h, x:x + w] = dst[y:y + h, x:x + w] * (1 - k) + tile * k
        else:  # slide up in, cut out
            q = EASE["outQuint"](min(1.0, max(0.0, lt / max(tin, 1e-6))))
            off = int(round((1 - q) * h))
            if off < h:
                dst[y + off:y + h, x:x + w] = tile[:h - off]
        return dst

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", required=True); ap.add_argument("--matte", required=True)
    ap.add_argument("--plan", required=True); ap.add_argument("--layers", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--lut", default=None)
    ap.add_argument("--audio", default=None); ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--only", default=None, help="a-b output frames: write JPG stills to --stills instead of a video")
    ap.add_argument("--stills", default=None)
    ap.add_argument("--frames", default=None, help="comma-separated output frames to write as stills (previews)")
    ap.add_argument("--segment", default=None, help="a-b: render only these output frames into OUT (a part, no audio); see --join")
    ap.add_argument("--join", nargs="*", default=None, help="parts to concatenate in order, muxed with --audio into --out")
    ap.add_argument("--sharpen", type=float, default=0.0, help="contrast-adaptive sharpening amount on the plate (0 to 1)")
    ap.add_argument("--grain", type=float, default=0.0, help="film grain strength in 8-bit levels (2 to 4 is subtle); also hides banding on flat panels")
    a = ap.parse_args()
    P = json.load(open(a.plan)); fps, W, H = P["fps"], P["w"], P["h"]
    if a.join is not None:
        lst = a.out + ".parts.txt"
        with open(lst, "w") as f:
            for part in a.join:
                f.write(f"file '{os.path.abspath(part)}'\n")
        cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst]
        if a.audio:
            cmd += ["-i", a.audio, "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-shortest"]
        subprocess.run(cmd + ["-c:v", "copy", "-movflags", "+faststart", a.out], check=True)
        os.remove(lst)
        print(json.dumps({"status": "DONE", "out": a.out, "parts": len(a.join)})); return
    N = int(round(P["duration"] * fps))
    vf = []
    if a.lut:
        vf.append(f"lut3d=file='{a.lut}':interp=tetrahedral")
    if a.sharpen > 0:
        vf.append(f"cas=strength={a.sharpen:g}")
    plate = cut_stream(a.plate, P["mapping"], fps, P["tail"], "rgb24", ",".join(vf))
    matte = cut_stream(a.matte, P["mapping"], fps, P["tail"], "gray")
    L = {k: Layer(os.path.join(a.layers, k)) for k in ("bg", "under", "over")}
    ins = [Insert(x, fps, W, H) for x in P.get("inserts", [])]
    lo, hi = (0, N - 1)
    seg = None
    if a.segment:
        lo, hi = [int(x) for x in a.segment.split("-")]; hi = min(hi, N - 1); seg = True
        a.audio = None
    pick = None
    if a.frames:
        pick = sorted({int(x) for x in a.frames.split(",") if x.strip()})
        lo, hi = pick[0], pick[-1]; pick = set(pick)
        a.only = f"{lo}-{hi}"
    if a.only and not seg:
        lo, hi = [int(x) for x in a.only.split("-")]
        os.makedirs(a.stills, exist_ok=True)
    enc = None
    if not a.only or seg:
        cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", f"{fps:g}", "-i", "-"]
        if a.audio:
            cmd += ["-i", a.audio]
        cmd += ["-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
                "-profile:v", "high", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
                "-movflags", "+faststart"]
        if a.audio:
            cmd += ["-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-shortest"]
        cmd += [a.out]
        enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    fsz, msz = W * H * 3, W * H
    t0 = time.time()
    ink = np.array([14, 14, 12], np.float32)
    for i in range(N):
        pb = plate.stdout.read(fsz); mb = matte.stdout.read(msz)
        if len(pb) < fsz or len(mb) < msz:
            sys.stderr.write(f"stream ended at frame {i} of {N}\n"); break
        if i < lo:
            continue
        if i > hi:
            break
        if pick is not None and i not in pick:
            continue
        t = i / fps
        A = np.frombuffer(pb, np.uint8).reshape(H, W, 3).astype(np.float32)
        M = np.frombuffer(mb, np.uint8).reshape(H, W, 1).astype(np.float32) / 255.0
        keyed = in_ranges(t, P["keyed"])
        und = L["under"].get(i)
        if keyed:
            bg = L["bg"].get(i)
            base = bg[..., :3].astype(np.float32) if bg is not None else np.broadcast_to(ink, (H, W, 3)).copy()
            if und is not None:
                over(base, und)
            s = keyed_value(P["subject_keys"], t, "s", 1.0)
            ax = keyed_value(P["subject_keys"], t, "ax", W / 2); ay = keyed_value(P["subject_keys"], t, "ay", H)
            dx = keyed_value(P["subject_keys"], t, "dx", 0.0); dy = keyed_value(P["subject_keys"], t, "dy", 0.0)
            if abs(s - 1) > 1e-3 or abs(dx) > 0.5 or abs(dy) > 0.5:
                Mt = np.float32([[s, 0, ax * (1 - s) + dx], [0, s, ay * (1 - s) + dy]])
                As = cv2.warpAffine(A, Mt, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
                Ms = cv2.warpAffine(M[..., 0], Mt, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)[..., None]
            else:
                As, Ms = A, M
            frame = base * (1 - Ms) + As * Ms
        else:
            frame = A.copy()
            if und is not None:
                over(frame, und)
                frame = frame * (1 - M) + A * M
            z = keyed_value(P["camera_keys"], t, "z", 1.0)
            if abs(z - 1) > 1e-3:
                fx = keyed_value(P["camera_keys"], t, "fx", W / 2); fy = keyed_value(P["camera_keys"], t, "fy", H / 2)
                ox = keyed_value(P["camera_keys"], t, "ox", fx); oy = keyed_value(P["camera_keys"], t, "oy", fy)
                # keep the picture covering the frame: clamp the translation for this zoom
                tx = ox - z * fx; ty = oy - z * fy
                tx = min(0.0, max(W - z * W, tx)); ty = min(0.0, max(H - z * H, ty))
                Mt = np.float32([[z, 0, tx], [0, z, ty]])
                frame = cv2.warpAffine(frame, Mt, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        for x in ins:
            if x.s["start"] <= t < x.s["end"]:
                x.draw(frame, t)
        ov = L["over"].get(i)
        if ov is not None:
            if ov.shape[2] == 4:
                over(frame, ov)
            else:
                frame = ov[..., :3].astype(np.float32)
        if a.grain > 0:
            g = np.random.default_rng(i).standard_normal((H // 2, W // 2)).astype(np.float32) * a.grain
            frame += cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
        out = np.clip(frame + 0.5, 0, 255).astype(np.uint8)
        if enc:
            enc.stdin.write(out.tobytes())
        else:
            cv2.imwrite(os.path.join(a.stills, f"{i:06d}.jpg"), cv2.cvtColor(out, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
        if i % 150 == 0:
            el = time.time() - t0
            print(json.dumps({"frame": i, "of": N, "fps": round((i - lo + 1) / max(el, 1e-6), 2)}), flush=True)
    for p in (plate, matte):
        p.stdout.close(); p.kill()
    if enc:
        enc.stdin.close(); enc.wait()
    print(json.dumps({"status": "DONE", "frames": N, "seconds": round(time.time() - t0, 1), "out": a.out if enc else a.stills}))

if __name__ == "__main__":
    main()
