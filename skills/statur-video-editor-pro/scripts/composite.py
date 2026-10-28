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

def edge_mask(W, H, F, sides):
    """Soft ramps (smoothstep, F px) on the given sides of the source frame. Used when the speaker is scaled or
    moved on a keyed background: the plate ends at the frame edge, so a shoulder or a hand would otherwise end
    on a hard straight line inside the picture."""
    x = np.ones(W, np.float32); y = np.ones(H, np.float32)
    r = np.linspace(0.0, 1.0, F, dtype=np.float32); r = r * r * (3 - 2 * r)
    if "l" in sides: x[:F] = np.minimum(x[:F], r)
    if "r" in sides: x[-F:] = np.minimum(x[-F:], r[::-1])
    if "t" in sides: y[:F] = np.minimum(y[:F], r)
    if "b" in sides: y[-F:] = np.minimum(y[-F:], r[::-1])
    return y[:, None] * x[None, :]

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

class Inset:
    """The speaker in a card over a full-screen panel (explainer split layout, as in many produced explainers):
    the plate frame cropped around the head found in the matte, drawn after the overlay layer so the panel stays
    a full-screen stage and the face never leaves the screen. Spec: rect [x, y, w, h] on the output frame,
    head_pad (px above the head top), delay and fade (s), border and dot colors (hex), radius (px)."""
    def __init__(self, spec, W, H):
        self.s = spec; self.W, self.H = W, H; self.cy = None
        x, y, w, h = spec.get("rect", [60, 1250, 960, 610])
        self.rect = (int(x), int(y), int(w), int(h))
        r = int(spec.get("radius", 0))
        self.mask = None
        if r > 0:
            m = np.zeros((int(h), int(w)), np.uint8)
            cv2.rectangle(m, (r, 0), (int(w) - r - 1, int(h) - 1), 255, -1); cv2.rectangle(m, (0, r), (int(w) - 1, int(h) - r - 1), 255, -1)
            for cx_, cy_ in ((r, r), (int(w) - r - 1, r), (r, int(h) - r - 1), (int(w) - r - 1, int(h) - r - 1)):
                cv2.circle(m, (cx_, cy_), r, 255, -1, lineType=cv2.LINE_AA)
            self.mask = (m.astype(np.float32) / 255.0)[..., None]
    @staticmethod
    def rgb(hexs):
        hexs = hexs.lstrip("#"); return np.array([int(hexs[i:i + 2], 16) for i in (0, 2, 4)], np.float32)
    def draw(self, dst, A, M, t):
        lt = t - self.s["start"]; dur = self.s["end"] - self.s["start"]
        kin = min(1.0, max(0.0, (lt - self.s.get("delay", 0.12)) / max(self.s.get("fade", 0.25), 1e-6)))
        kout = min(1.0, max(0.0, (dur - lt) / 0.18))
        k = min(kin, kout)
        if k <= 0:
            return dst
        x, y, w, h = self.rect
        cw = self.W; ch = int(round(cw * h / w))
        if ch > self.H:
            ch = self.H; cw = int(round(ch * w / h))
        # head top: first row where the matte is wider than a hand
        rows = np.where((M[..., 0] > 0.5).sum(axis=1) > self.s.get("head_min_px", 160))[0]
        top = float(rows.min()) if len(rows) else self.H * 0.2
        want = max(0.0, min(float(self.H - ch), top - self.s.get("head_pad", 60)))
        self.cy = want if self.cy is None else self.cy + (want - self.cy) * 0.12   # smooth, no jitter
        cy = int(round(self.cy)); cx = (self.W - cw) // 2
        tile = cv2.resize(A[cy:cy + ch, cx:cx + cw], (w, h), interpolation=cv2.INTER_AREA)
        yy = y + int(round((1 - EASE["outCubic"](kin)) * 40))   # rises 40 px while it fades in
        hh = min(h, self.H - yy)
        if hh <= 0:
            return dst
        a = k if self.mask is None else self.mask[:hh] * k
        reg = dst[yy:yy + hh, x:x + w]
        reg[:] = reg * (1 - a) + tile[:hh] * a
        if self.s.get("border"):
            col = self.rgb(self.s["border"])
            for (y0, y1, x0, x1) in ((yy, yy + 2, x, x + w), (yy + hh - 2, yy + hh, x, x + w), (yy, yy + hh, x, x + 2), (yy, yy + hh, x + w - 2, x + w)):
                dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - k) + col * k
        if self.s.get("dot"):
            col = self.rgb(self.s["dot"]); d = 7
            dst[max(0, yy - d):yy + d, max(0, x - d):x + d] = dst[max(0, yy - d):yy + d, max(0, x - d):x + d] * (1 - k) + col * k
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
    ap.add_argument("--edge-feather", type=int, default=72, help="px of soft edge on the sides of a scaled or moved speaker (0: hard edge)")
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
    cards = [Inset(x, W, H) for x in P.get("insets", [])]
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
        # write under a temporary name and rename at the end: a killed run never leaves a part that looks finished
        tmp_out = os.path.splitext(a.out)[0] + ".partial" + os.path.splitext(a.out)[1]
        cmd += [tmp_out]
        enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    fsz, msz = W * H * 3, W * H
    t0 = time.time()
    ink = np.array([14, 14, 12], np.float32)
    edge_cache = {}
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
                Msrc = M[..., 0]
                if a.edge_feather > 0:
                    # feather only the sides of the moved plate that now fall inside the picture
                    x0 = ax * (1 - s) + dx; y0 = ay * (1 - s) + dy; x1 = x0 + s * W; y1 = y0 + s * H
                    sides = ("l" if x0 > 0.5 else "") + ("r" if x1 < W - 0.5 else "") + ("t" if y0 > 0.5 else "") + ("b" if y1 < H - 0.5 else "")
                    if sides:
                        key = (sides,)
                        if key not in edge_cache:
                            edge_cache[key] = edge_mask(W, H, int(a.edge_feather), sides)
                        Msrc = Msrc * edge_cache[key]
                Ms = cv2.warpAffine(Msrc, Mt, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)[..., None]
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
        for c in cards:
            if c.s["start"] <= t < c.s["end"]:
                c.draw(frame, A, M, t)
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
        if enc.returncode != 0:
            sys.exit(f"encoder failed with code {enc.returncode}; {tmp_out} left for inspection")
        os.replace(tmp_out, a.out)
    print(json.dumps({"status": "DONE", "frames": N, "seconds": round(time.time() - t0, 1), "out": a.out if enc else a.stills}))

if __name__ == "__main__":
    main()
