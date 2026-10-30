#!/usr/bin/env python3
"""Render one short clip from a long recording (live, webinar, podcast).

What it does, in order:
1. Builds the cut list from word timestamps: keeps the requested segments (in the
   order given, chronological or not), removes silences and hesitations longer than
   min_gap, and any extra ranges listed in "cut".
2. Renders each kept piece with an accurate seek, a 9:16 crop and an alternating
   punch-in zoom that hides jump cuts, with 12 ms audio fades against clicks.
3. Joins the pieces, burns word-by-word captions (active word highlighted) and the
   opening hook, normalizes loudness in two passes (default -14 LUFS), and writes
   the master (H.264, 1080x1920 by default, any length, 4K if asked).
4. Optionally writes a light review proxy as HLS (fMP4 segments) for a review page.

Usage:
  clip_render.py --source SRC --words words.json --spec clip.json --out OUTDIR
                 [--fonts DIR] [--proxy] [--keep-temp]

Works with ffmpeg 4.4 or newer (libx264, libass). No other dependency.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, math, time

PREROLL = 5.0   # seconds decoded before each cut point (covers a 2-4 s keyframe interval)

def run(cmd, quiet=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write("FAILED: " + " ".join(cmd) + "\n" + r.stderr[-3000:] + "\n")
        raise SystemExit(1)
    return r

def probe(path):
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path])
    j = json.loads(r.stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    fr = v.get("avg_frame_rate", "30/1")
    num, den = (fr.split("/") + ["1"])[:2]
    fps = float(num) / float(den) if float(den) else 30.0
    return {"w": int(v["width"]), "h": int(v["height"]), "fps": fps,
            "dur": float(j["format"]["duration"]), "has_audio": a is not None}

# ---------------------------------------------------------------- cut list
def speech_onset(audio, lo, s0):
    """Start of the speech burst that holds s0, searched back to lo on the transcript audio (16 kHz).
    ASR word starts often land 50 to 150 ms after the real onset (a plosive, a soft first syllable).
    Returns None when no silence separates the word from what comes before (connected speech)."""
    if not audio or s0 - lo < 0.03:
        return None
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{lo:.3f}", "-i", audio, "-t", f"{s0 + 0.12 - lo:.3f}",
                        "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True)
    raw = r.stdout
    n = len(raw) // 2
    if n < 480:
        return None
    vals = memoryview(raw).cast("h")
    hop = 160                       # 10 ms frames
    db = []
    for i in range(0, n - hop + 1, hop):
        acc = 0
        for v in vals[i:i + hop]:
            acc += v * v
        db.append(10 * math.log10(acc / hop + 1e-9) - 90.3)
    k0 = min(len(db) - 1, int((s0 - lo) / 0.01))
    floor, peak = min(db), max(db[k0:]) if db[k0:] else max(db)
    if peak - floor < 15:
        return None
    th = floor + 0.25 * (peak - floor)
    j = k0
    while j >= 0 and db[j] >= th:
        j -= 1
    if j < 0:
        return None
    return lo + (j + 1) * 0.01

def keep_intervals(words, spec, audio=None):
    """Kept intervals [src_s, src_e, segment_index], in the order of spec["segments"].
    A run of words breaks on a pause longer than min_gap or when a removed word sits in between.
    Padding never reaches into a neighbouring word, so a removed word never bleeds into the cut.
    A cut is an exact time range: whatever the word timestamps say, nothing inside [a, b] is kept
    (ASR word boundaries can be 50 to 100 ms off; a cut placed on the waveform wins)."""
    sil = {"min_gap": 0.30, "pad_in": 0.06, "pad_out": 0.12, "max_keep_gap": 0.20, "bleed": 0.02}
    sil.update(spec.get("silence", {}))
    cuts = [(float(c[0]), float(c[1])) for c in spec.get("cut", [])]
    def in_cut(w):
        mid = (w["s"] + w["e"]) / 2
        return any(a <= mid <= b for a, b in cuts)
    n = len(words)
    out = []
    kept = set()      # indexes of the words that stay in the clip (captions use only these)
    for k, seg in enumerate(spec["segments"]):
        S, E = float(seg["s"]), float(seg["e"])
        keep = [i for i, w in enumerate(words) if w["e"] > S + 0.02 and w["s"] < E - 0.02 and not in_cut(w)]
        if not keep:
            continue
        runs, cur = [], [keep[0]]
        for i in keep[1:]:
            gap = words[i]["s"] - words[cur[-1]]["e"]
            if gap > sil["min_gap"] or i != cur[-1] + 1:
                runs.append(cur); cur = [i]
            else:
                cur.append(i)
        runs.append(cur)
        for r in runs:
            kept.update(r)
        ivs = []   # [a, b, first_index, last_index]
        for r in runs:
            i0, i1 = r[0], r[-1]
            s0, e1 = words[i0]["s"], words[i1]["e"]
            prev_e = words[i0 - 1]["e"] if i0 > 0 else -1e9
            next_s = words[i1 + 1]["s"] if i1 + 1 < n else 1e9
            a = max(S, s0 - sil["pad_in"], min(prev_e, s0) - sil["bleed"])
            lo = max(S, min(prev_e, s0) - sil["bleed"], s0 - 0.30)
            on = speech_onset(audio, lo, s0)
            if on is not None:
                a = min(a, max(lo, on - 0.02))
            b = min(E, e1 + sil["pad_out"], max(next_s, e1) + sil["bleed"])
            if ivs and ivs[-1][3] + 1 == i0 and a - ivs[-1][1] <= sil["max_keep_gap"]:
                ivs[-1][1] = max(ivs[-1][1], b); ivs[-1][3] = i1
            else:
                ivs.append([a, b, i0, i1])
        frags = []
        for a, b, _, _ in ivs:
            parts = [(a, b)]
            for ca, cb in cuts:
                nxt = []
                for x, y in parts:
                    if cb <= x or ca >= y:
                        nxt.append((x, y))
                    else:
                        if ca > x:
                            nxt.append((x, ca))
                        if cb < y:
                            nxt.append((cb, y))
                parts = nxt
            frags.extend(parts)
        out.extend([round(a, 3), round(b, 3), k] for a, b in frags if b - a >= 0.12)
    keep_intervals.kept = kept
    return out

def join_punct(words):
    out = []
    for w in words:
        t = w["w"].strip()
        if out and t and re.fullmatch(r"[?!.,;:…»)\]]+", t) and w["s"] - out[-1]["e"] < 0.5:
            sep = " " if t[0] in "?!:;»" else ""      # French spacing before ? ! : ;
            out[-1] = dict(out[-1], w=out[-1]["w"] + sep + t, e=max(out[-1]["e"], w["e"]))
        else:
            out.append(dict(w))
    return out

def apply_fixes(words, fixes):
    """Caption corrections. Replace the words starting in [s, e) by the given text; timing is spread over
    the replaced span in proportion to the length of each new word. A fix never changes the audio:
    an empty text hides the words from the captions and keeps them in the edit (use "cut" to remove audio)."""
    for f in fixes:
        s0, e0 = float(f["s"]), float(f["e"])
        idx = [i for i, w in enumerate(words) if s0 <= w["s"] < e0]
        if not idx:
            continue
        a, b = words[idx[0]]["s"], words[idx[-1]]["e"]
        toks = f["text"].split()
        if not toks:
            words = words[:idx[0]] + [dict(words[i], hide=True) for i in idx] + words[idx[-1] + 1:]
            continue
        tot = sum(len(t) + 1 for t in toks) or 1
        new, t = [], a
        for tk in toks:
            d = (b - a) * (len(tk) + 1) / tot
            new.append({"w": tk, "s": round(t, 3), "e": round(t + d, 3)}); t += d
        words = words[:idx[0]] + new + words[idx[-1] + 1:]
    return words

def load_sync(path):
    """Piecewise-linear map from transcript time to media time (sync_check.py output).
    None or "none" = same timeline. A number = constant offset in seconds."""
    if not path or path == "none":
        return lambda t: t
    try:
        off = float(path)
        return lambda t: t + off
    except ValueError:
        pass
    pts = sorted(json.load(open(path))["points"])
    if len(pts) == 1:
        d = pts[0][1] - pts[0][0]
        return lambda t: t + d
    def f(t):
        if t <= pts[0][0]:
            (x0, y0), (x1, y1) = pts[0], pts[1]
        elif t >= pts[-1][0]:
            (x0, y0), (x1, y1) = pts[-2], pts[-1]
        else:
            i = next(i for i in range(1, len(pts)) if pts[i][0] >= t)
            (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        return y0 + (y1 - y0) * (t - x0) / (x1 - x0)
    return f

# ---------------------------------------------------------------- captions
def ass_time(t):
    t = max(0.0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    cs = int(round((s - int(s)) * 100))
    if cs == 100:
        cs = 99
    return f"{h:d}:{m:02d}:{int(s):02d}.{cs:02d}"

def hexcol(rgb, alpha="00"):
    rgb = rgb.lstrip("#")
    r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
    return f"&H{alpha}{b}{g}{r}".upper()

def clean_word(w, keep_punct="?!"):
    w = w.strip()
    w = re.sub(r"^[\"'«»“”(\[]+", "", w)
    w = re.sub(r"[\"'«»“”)\]]+$", "", w)
    w = re.sub(r"[,;:.…]+$", "", w) if True else w
    return w

def build_ass(words_out, spec, W, H, total, mapping=None):
    cap = {"font": "Archivo Black", "size": 78, "max_words": 3, "max_chars": 18,
           "y": 0.70, "color": "#FFFFFF", "active": "#E8501C", "outline": "#0E0E0C",
           "outline_w": 6, "uppercase": False, "enabled": True}
    cap.update(spec.get("captions", {}))
    hook = spec.get("hook") or {}
    hk = {"font": "Archivo Black", "size": 100, "text_color": "#0E0E0C", "box": "#F2EFE8",
          "y": 0.15, "dur": 3.0, "max_chars": 0, "margin": 80, "pad": 22}
    hk.update({k: v for k, v in hook.items() if k != "text"})
    lb = {"font": "Archivo Black", "size": 58, "text_color": "#FFFFFF", "box": "#E8501C", "y": 0.155, "pad": 12,
          "max_group": 15.0, "short": 4.0}
    lb.update(spec.get("labels", {}))
    # default watermark: the playbook this pipeline comes from (change it with --watermark or the spec)
    wm = {"text": "statur.co/clipping", "font": "Archivo Black", "size": 30, "color": "#FFFFFF", "opacity": 0.55,
          "min": 3.5, "max": 6.5, "enabled": True}
    wm.update(spec.get("watermark", {}))
    wm_alpha = f"{int(round((1 - float(wm['opacity'])) * 255)):02X}"
    scale = H / 1920.0
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
        "WrapStyle: 2", "ScaledBorderAndShadow: yes", "YCbCr Matrix: TV.709", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Cap,{cap['font']},{int(cap['size']*scale)},{hexcol(cap['color'])},{hexcol(cap['color'])},{hexcol(cap['outline'])},&H00000000,0,0,0,0,100,100,0,0,1,{cap['outline_w']*scale:.1f},0,5,40,40,0,1",
        f"Style: Label,{lb['font']},{int(lb['size']*scale)},{hexcol(lb['text_color'])},{hexcol(lb['text_color'])},{hexcol(lb['box'])},{hexcol(lb['box'])},0,0,0,0,100,100,2,0,3,{lb['pad']*scale:.1f},0,8,80,80,{int(lb['y']*H)},1",
        f"Style: Hook,{hk['font']},{int(hk['size']*scale)},{hexcol(hk['text_color'])},{hexcol(hk['text_color'])},{hexcol(hk['box'])},{hexcol(hk['box'])},0,0,0,0,100,100,0,0,3,{hk['pad']*scale:.1f},0,8,{int(hk['margin']*scale)},{int(hk['margin']*scale)},{int(hk['y']*H)},1",
        f"Style: WM,{wm['font']},{int(wm['size']*scale)},{hexcol(wm['color'], wm_alpha)},{hexcol(wm['color'], wm_alpha)},{hexcol('#0E0E0C', wm_alpha)},&H00000000,0,0,0,0,100,100,1,0,1,{1.6*scale:.1f},0,7,0,0,0,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    # hook: wrap to lines of max_chars
    if hook.get("text"):
        hl = []
        for part in hook["text"].split("|"):          # "|" forces a line break
            if not hk["max_chars"]:
                hl.append(part.strip()); continue
            cur = ""
            for w in part.split():
                if cur and len(cur) + 1 + len(w) > hk["max_chars"]:
                    hl.append(cur); cur = w
                else:
                    cur = (cur + " " + w).strip()
            if cur:
                hl.append(cur)
        txt = "\\N".join(hl)
        lines.append(f"Dialogue: 2,{ass_time(0)},{ass_time(min(total, hk['dur']))},Hook,,0,0,0,,{{\\q0\\fad(0,180)}}{txt}")
    # segment labels ("Pitch 1/4"...), shown from the segment start (after the hook) to its end
    if mapping:
        hook_end = min(total, hk["dur"]) if hook.get("text") else 0
        groups = []   # [label, [segment indexes]]
        for k, seg in enumerate(spec["segments"]):
            lab = seg.get("screen")
            if groups and lab and groups[-1][0] == lab:
                groups[-1][1].append(k)
            else:
                groups.append([lab, [k]])
        for lab, ks in groups:
            ms = [m for m in mapping if m["seg"] in ks]
            if not lab or not ms:
                continue
            st = max(ms[0]["out_s"], hook_end + 0.05); en = ms[-1]["out_e"]
            if en - st > lb["max_group"]:
                en = st + lb["short"]
            if en - st > 0.3:
                lines.append(f"Dialogue: 3,{ass_time(st)},{ass_time(en)},Label,,0,0,0,,{{\\fad(120,120)}}{lab.upper()}")
    # watermark: small, semi-transparent, and it jumps between safe spots every few seconds with a slow
    # drift, so it cannot be removed with one crop or one blur box. Spots avoid the captions, the hook,
    # the chapter labels and the platform's buttons and caption area.
    if wm["enabled"] and wm["text"]:
        import random
        spots = [(0.05, 0.095), (0.58, 0.095), (0.05, 0.35), (0.55, 0.35), (0.05, 0.53), (0.30, 0.45), (0.05, 0.62)]
        spots = [p for p in spots if abs(p[1] - float(cap["y"])) > 0.06] or spots   # never on the caption line
        rng = random.Random(str(spec.get("id", "clip")) + wm["text"])
        t, last = 0.0, None
        while t < total - 0.2:
            d = rng.uniform(float(wm["min"]), float(wm["max"]))
            i = rng.randrange(len(spots))
            if i == last:
                i = (i + 1 + rng.randrange(len(spots) - 1)) % len(spots)
            last = i
            x, y = spots[i]
            dx, dy = rng.choice([(40, 0), (-40, 0), (0, 30), (0, -30)])
            x1, y1 = int(x * W), int(y * H)
            x2, y2 = x1 + int(dx * scale), y1 + int(dy * scale)
            if x2 < int(0.03 * W):
                x2 = x1 + int(abs(dx) * scale)
            end = min(total, t + d)
            lines.append(f"Dialogue: 0,{ass_time(t)},{ass_time(end)},WM,,0,0,0,,"
                         f"{{\\move({x1},{y1},{x2},{y2})\\fad(250,250)}}{wm['text']}")
            t = end
    if cap["enabled"] and words_out:
        # group words into chunks
        chunks, cur = [], []
        for i, w in enumerate(words_out):
            disp = clean_word(w["w"])
            if not disp:
                continue
            ww = dict(w, d=disp.upper() if cap["uppercase"] else disp)
            if cur:
                gap = ww["s"] - cur[-1]["e"]
                chars = sum(len(x["d"]) + 1 for x in cur) + len(ww["d"])
                if len(cur) >= cap["max_words"] or chars > cap["max_chars"] or gap > 0.35:
                    chunks.append(cur); cur = []
            cur.append(ww)
            if re.search(r"[.?!…]$", w["w"].strip()):
                chunks.append(cur); cur = []
        if cur:
            chunks.append(cur)
        y = int(cap["y"] * H)
        act = hexcol(cap["active"])[2:]  # &HBBGGRR without alpha for \c
        act = "&H" + hexcol(cap["active"])[4:] + "&"
        base = "&H" + hexcol(cap["color"])[4:] + "&"
        for ci, ch in enumerate(chunks):
            c_end = ch[-1]["e"]
            nxt = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else total
            c_end = min(max(c_end, ch[-1]["s"] + 0.25), nxt)
            for k, w in enumerate(ch):
                st = w["s"] if k else ch[0]["s"]
                en = ch[k + 1]["s"] if k + 1 < len(ch) else c_end
                if en - st < 0.03:
                    continue
                parts = []
                for j, x in enumerate(ch):
                    t = x["d"].replace("{", "(").replace("}", ")")
                    parts.append(f"{{\\c{act}}}{t}{{\\c{base}}}" if j == k else t)
                lines.append(f"Dialogue: 1,{ass_time(st)},{ass_time(en)},Cap,,0,0,0,,{{\\an5\\pos({int(float(cap.get('x', 0.5)) * W)},{y})}}" + " ".join(parts))
    return "\n".join(lines) + "\n"

def write_srt(words_out, path, max_chars=42):
    chunks, cur = [], []
    for w in words_out:
        cur.append(w)
        txt = " ".join(x["w"] for x in cur)
        if len(txt) >= max_chars or re.search(r"[.?!]$", w["w"]):
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    def ts(t):
        h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
        ms = int(round((s - int(s)) * 1000)); ms = min(ms, 999)
        return f"{h:02d}:{m:02d}:{int(s):02d},{ms:03d}"
    with open(path, "w") as f:
        for i, c in enumerate(chunks, 1):
            f.write(f"{i}\n{ts(c[0]['s'])} --> {ts(c[-1]['e'])}\n{' '.join(x['w'] for x in c)}\n\n")

# ---------------------------------------------------------------- geometry
def crop_box(src_w, src_h, W, H, frame, zoom):
    """Base crop at the target aspect ratio, then an optional punch-in around the face point."""
    target = W / H
    if src_w / src_h > target:      # source wider: crop width
        ch = src_h; cw = int(round(src_h * target))
    else:                            # source taller: crop height
        cw = src_w; ch = int(round(src_w / target))
    cw -= cw % 2; ch -= ch % 2
    cy = frame.get("crop_y", 0.5) * src_h
    cx = frame.get("crop_x", 0.5) * src_w
    x0 = int(min(max(cx - cw / 2, 0), src_w - cw)); y0 = int(min(max(cy - ch / 2, 0), src_h - ch))
    if zoom and zoom > 1.0:
        zw = int(round(cw / zoom)); zh = int(round(ch / zoom)); zw -= zw % 2; zh -= zh % 2
        fx = frame.get("face_x", 0.5); fy = frame.get("face_y", 0.42)   # face point inside the base crop
        x1 = int(round(x0 + (cw - zw) * fx)); y1 = int(round(y0 + (ch - zh) * fy))
        return zw, zh, x1 - x1 % 2, y1 - y1 % 2
    return cw, ch, x0 - x0 % 2, y0 - y0 % 2

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True); ap.add_argument("--words", required=True)
    ap.add_argument("--spec", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--fonts", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts"))
    ap.add_argument("--review", action="store_true", help="also write a light MP4 review copy and a poster")
    ap.add_argument("--hls", action="store_true", help="also write an HLS proxy (very long clips)")
    ap.add_argument("--keep-temp", action="store_true")
    ap.add_argument("--threads", type=int, default=0)
    ap.add_argument("--tmp", default=None, help="work folder for pieces (default OUT/_tmp); keep it off synced folders")
    ap.add_argument("--budget", type=float, default=0, help="stop cleanly after about N seconds and resume on the next run (0 = no limit)")
    ap.add_argument("--force", action="store_true", help="re-render everything")
    ap.add_argument("--plan-only", action="store_true", help="write the cut list, captions and words, then stop (no video)")
    ap.add_argument("--watermark", default=None, help="watermark text (creator handle or domain); the spec's watermark.text wins; 'none' disables")
    ap.add_argument("--audio", default=None, help="transcript audio (audio16k.flac): moves each cut-in back to the real speech onset")
    ap.add_argument("--audio-preroll", type=float, default=None, help="seconds of audio decoded before each cut, from a second, shorter seek (default: same as the video pre-roll); use about 0.8 when a corrupt audio stretch silences the start of a piece")
    ap.add_argument("--sync", default=None, help="sync map from sync_check.py (or a constant offset in seconds) when the transcript audio does not follow the video's timeline")
    a = ap.parse_args()
    t_start = time.time()
    def out_of_time(need):
        return a.budget > 0 and (time.time() - t_start + need) > a.budget

    spec = json.load(open(a.spec)); words = json.load(open(a.words))
    words.sort(key=lambda w: w["s"])
    if a.watermark and not (spec.get("watermark") or {}).get("text"):
        if a.watermark.lower() == "none":
            spec["watermark"] = dict(spec.get("watermark") or {}, enabled=False)
        else:
            spec["watermark"] = dict(spec.get("watermark") or {}, text=a.watermark)
    words = apply_fixes(words, spec.get("fix", []))
    words = join_punct(words)
    info = probe(a.source) if not a.plan_only else {"w": 1080, "h": 1920, "fps": 30, "dur": 0, "has_audio": True}
    fr = {"w": 1080, "h": 1920, "fps": 30}; fr.update(spec.get("frame", {}))
    W, H, FPS = int(fr["w"]), int(fr["h"]), float(fr["fps"])
    enc = {"crf": 17, "preset": "veryfast"}; enc.update(spec.get("encode", {}))
    au = {"lufs": -14, "tp": -1.5, "lra": 11, "highpass": 70}; au.update(spec.get("audio", {}))
    zm = {"enabled": True, "factor": 1.10}; zm.update(spec.get("zoom", {}))

    os.makedirs(a.out, exist_ok=True)
    ivs = keep_intervals(words, spec, a.audio)
    kept_words = keep_intervals.kept
    fp = hashlib.sha1(json.dumps([[iv[:2] for iv in ivs], fr, zm, PREROLL, a.audio_preroll, info["w"], info["h"], str(a.sync), 3], sort_keys=True).encode()).hexdigest()[:10]
    tmp = os.path.join(a.tmp or os.path.join(a.out, "_tmp"), f"{spec.get('id', 'clip')}_v{spec.get('version', 1)}_{fp}")
    if a.force:
        shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp, exist_ok=True)
    if not ivs:
        raise SystemExit("no interval kept: check segments and words")

    # output timeline mapping and caption words; each piece lasts a whole number of frames so that
    # audio (48 kHz) and video stay aligned across the concat
    to_media = load_sync(a.sync)
    words_out, mapping, o = [], [], 0.0
    captioned = set()
    for i, (s, e, k) in enumerate(ivs):
        e = round(s + max(1, round((e - s) * FPS)) / FPS, 4)
        ms_ = to_media(s)
        mapping.append({"src_s": s, "src_e": e, "media_s": round(ms_, 4), "out_s": round(o, 4), "out_e": round(o + e - s, 4), "seg": k,
                        "zoom": zm["factor"] if (zm["enabled"] and i % 2 == 1) else 1.0})
        # a kept word is captioned in the piece that holds most of it; ASR start and end times can be a
        # little off, so a word that runs past the piece (a cut placed on the waveform) is still shown,
        # clamped to the piece, while a word that only grazes the piece is not
        for wi, w in enumerate(words):
            ov = min(e, w["e"]) - max(s, w["s"])
            if (wi in kept_words and (wi, k) not in captioned and not w.get("hide")
                    and ov >= min(0.12, 0.5 * max(w["e"] - w["s"], 0.02))):
                captioned.add((wi, k))
                ws_ = max(0.0, w["s"] - s)
                words_out.append({"w": w["w"], "s": round(ws_ + o, 3),
                                  "e": round(max(ws_ + 0.04, min(e, w["e"]) - s) + o, 3)})
        o += e - s
    total = o

    if a.plan_only:
        with open(os.path.join(a.out, "captions.ass"), "w") as f:
            f.write(build_ass(words_out, spec, W, H, total, mapping))
        write_srt(words_out, os.path.join(a.out, "captions.srt"))
        json.dump(words_out, open(os.path.join(a.out, "words_out.json"), "w"), ensure_ascii=False)
        json.dump({"id": spec.get("id"), "version": spec.get("version", 1), "duration": round(total, 2),
                   "pieces": len(mapping), "mapping": mapping}, open(os.path.join(a.out, "cutlist.json"), "w"), indent=1)
        print(json.dumps({"status": "PLAN", "duration": round(total, 2), "pieces": len(mapping)})); return

    # stage A: render pieces
    pieces = []
    for i, m in enumerate(mapping):
        dur = m["src_e"] - m["src_s"]
        cw, ch, cx, cy = crop_box(info["w"], info["h"], W, H, fr, m["zoom"])
        fade = min(0.012, dur / 4)
        p = os.path.join(tmp, f"p{i:03d}.mkv")
        pieces.append(p)
        if os.path.exists(p + ".done"):
            continue
        if out_of_time(dur * 0.8 + 3):
            print(json.dumps({"status": "INCOMPLETE", "stage": "pieces", "done": i, "of": len(mapping)})); sys.exit(3)
        # seek a few seconds early, then decode forward and trim inside the filter graph: live recordings
        # (HEVC/TS, long GOPs) give grey frames when decoding starts on a non-keyframe, and the trims keep
        # audio and video cut at the same sample-accurate point
        start = m["media_s"]
        pre = min(PREROLL, start)
        nfr = max(1, round(dur * FPS))
        sp = round(pre * FPS)          # after the fps filter, one pts unit is one frame
        ns = round(nfr * 48000 / FPS)  # audio samples of the piece: exactly the length of its video
        # audio: the start is found on timestamps, the length is counted in samples. Live replays carry
        # jittery audio timestamps, so a duration measured on timestamps gives pieces a few ms too long
        # or too short, and the error adds up over the concat (up to 0.1 s of lip-sync drift on a 1 min clip)
        apre = pre if a.audio_preroll is None else min(a.audio_preroll, start)
        fc = (f"[0:v]fps={FPS:g},trim=start_pts={sp}:end_pts={sp + nfr},setpts=PTS-STARTPTS,"
              f"crop={cw}:{ch}:{cx}:{cy},scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p[v];"
              f"[{0 if apre == pre else 1}:a]atrim=start={apre:.4f}:duration={dur + 0.25:.4f},asetpts=PTS-STARTPTS,aresample=48000,asetpts=N/SR/TB,"
              f"aformat=sample_fmts=s16:channel_layouts=stereo,apad=whole_len={ns},atrim=end_sample={ns},"
              f"afade=t=in:st=0:d={fade:.3f},afade=t=out:st={max(0, dur - fade):.4f}:d={fade:.3f}[a]")
        cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", f"{start - pre:.4f}", "-i", a.source]
        if apre != pre:  # audio from its own, shorter seek: a corrupt AAC stretch inside the video pre-roll can silence the decoder
            cmd += ["-ss", f"{start - apre:.4f}", "-i", a.source]
        cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "ultrafast",
               "-crf", "10", "-c:a", "pcm_s16le"]
        if a.threads:
            cmd += ["-threads", str(a.threads)]
        run(cmd + [p])
        open(p + ".done", "w").write("ok")
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        for p in pieces:
            f.write(f"file '{os.path.abspath(p)}'\n")

    # captions and hook
    ass_path = os.path.join(a.out, "captions.ass")
    with open(ass_path, "w") as f:
        f.write(build_ass(words_out, spec, W, H, total, mapping))
    write_srt(words_out, os.path.join(a.out, "captions.srt"))

    # loudness pass 1 (cached)
    af_pre = f"highpass=f={au['highpass']},acompressor=threshold=-21dB:ratio=2.5:attack=5:release=150:makeup=1.5"
    loud = os.path.join(tmp, "loud.json")
    if os.path.exists(loud):
        mj = json.load(open(loud))
    else:
        r = run(["ffmpeg", "-nostdin", "-v", "info", "-f", "concat", "-safe", "0", "-i", lst, "-vn",
                 "-af", f"{af_pre},loudnorm=I={au['lufs']}:TP={au['tp']}:LRA={au['lra']}:print_format=json",
                 "-f", "null", "-"])
        mj = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)[-1])
        json.dump(mj, open(loud, "w"))
    ln = (f"loudnorm=I={au['lufs']}:TP={au['tp']}:LRA={au['lra']}:measured_I={mj['input_i']}:"
          f"measured_TP={mj['input_tp']}:measured_LRA={mj['input_lra']}:measured_thresh={mj['input_thresh']}:"
          f"offset={mj['target_offset']}:linear=true")

    # final master
    fontsdir = os.path.abspath(a.fonts)
    ass_esc = os.path.abspath(ass_path).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    master = os.path.join(a.out, f"{spec.get('id', 'clip')}_v{spec.get('version', 1)}_master.mp4")
    cmd = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
           "-filter_complex", f"[0:v]ass='{ass_esc}':fontsdir='{fontsdir}'[v];[0:a]{af_pre},{ln},aresample=48000[a]",
           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", enc["preset"], "-crf", str(enc["crf"]),
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", f"{FPS:g}", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart"]
    if a.threads:
        cmd += ["-threads", str(a.threads)]
    fkey = hashlib.sha1((open(ass_path).read() + json.dumps([au, enc, FPS, master])).encode()).hexdigest()
    fdone = os.path.join(tmp, "final.done")
    if not (os.path.exists(fdone) and open(fdone).read() == fkey and os.path.exists(master)):
        if out_of_time(total * 0.9 + 5):
            print(json.dumps({"status": "INCOMPLETE", "stage": "final", "done": len(mapping), "of": len(mapping)})); sys.exit(3)
        run(cmd + [master])
        open(fdone, "w").write(fkey)

    # review copy: one progressive MP4 kept under ~19 MiB (artifact asset cap is 20 MiB) + a poster frame
    review = None
    if a.review:
        rdir = os.path.join(a.out, "review"); os.makedirs(rdir, exist_ok=True)
        rv = os.path.join(rdir, f"{spec.get('id', 'clip')}_v{spec.get('version', 1)}_review.mp4")
        budget_kbps = 0.93 * 19 * 8 * 1024 / max(total, 1.0)          # whole file, kbit/s
        a_kbps = 96 if budget_kbps > 700 else 64
        v_kbps = int(max(250, min(2400, budget_kbps - a_kbps)))
        rh = 1280 if v_kbps >= 700 else 960
        rw = int(round(rh * W / H / 2) * 2)
        for attempt in range(3):
            run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", master, "-vf", f"scale={rw}:{rh}:flags=bicubic",
                 "-c:v", "libx264", "-preset", "veryfast", "-b:v", f"{v_kbps}k", "-maxrate", f"{int(v_kbps*1.4)}k",
                 "-bufsize", f"{int(v_kbps*2)}k", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", f"{a_kbps}k",
                 "-movflags", "+faststart", rv])
            if os.path.getsize(rv) <= 19.3 * 1024 * 1024:
                break
            v_kbps = int(v_kbps * 0.8)
        poster = os.path.join(rdir, f"{spec.get('id', 'clip')}_v{spec.get('version', 1)}_poster.jpg")
        run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", f"{min(1.5, total/2):.2f}", "-i", master,
             "-frames:v", "1", "-vf", f"scale={rw}:{rh}", "-q:v", "4", poster])
        review = {"video": os.path.abspath(rv), "poster": os.path.abspath(poster),
                  "bytes": os.path.getsize(rv), "video_kbps": v_kbps, "size": [rw, rh]}

    # optional HLS proxy for very long clips (fMP4 segments named .mp4 so any uploader sees video/mp4)
    proxy = None
    if a.hls:
        pdir = os.path.join(a.out, "proxy"); os.makedirs(pdir, exist_ok=True)
        run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", master, "-vf", "scale=720:1280:flags=bicubic",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-g", str(int(FPS * 2)),
             "-keyint_min", str(int(FPS * 2)), "-sc_threshold", "0", "-c:a", "aac", "-b:a", "128k",
             "-f", "hls", "-hls_time", "6", "-hls_playlist_type", "vod", "-hls_segment_type", "fmp4",
             "-hls_fmp4_init_filename", "init.mp4", "-hls_segment_filename", os.path.join(pdir, "seg_%03d.mp4"),
             os.path.join(pdir, "proxy.m3u8")])
        proxy = pdir

    report = {"id": spec.get("id"), "version": spec.get("version", 1), "source": os.path.abspath(a.source),
              "source_info": info, "duration": round(total, 2), "pieces": len(pieces),
              "kept_ratio": round(total / sum(float(s["e"]) - float(s["s"]) for s in spec["segments"]), 3),
              "loudness_input": mj, "master": os.path.abspath(master), "review": review, "proxy": proxy,
              "mapping": mapping}
    json.dump(report, open(os.path.join(a.out, "render_report.json"), "w"), indent=1)
    json.dump(words_out, open(os.path.join(a.out, "words_out.json"), "w"), ensure_ascii=False)
    if not a.keep_temp:
        shutil.rmtree(tmp, ignore_errors=True)
    report["status"] = "DONE"
    print(json.dumps({k: report[k] for k in ("status", "id", "version", "duration", "pieces", "kept_ratio", "master", "review", "proxy")}))

if __name__ == "__main__":
    main()
