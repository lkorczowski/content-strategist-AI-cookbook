#!/usr/bin/env python3
"""Check that the transcript timeline matches the video file, and write a sync map if it does not.

Why: live recordings (TikTok replays, HLS downloads, MPEG-TS) often start the audio a second or two
after the video, and drift by a few tens of milliseconds over an hour. Word timestamps come from an
audio file extracted for transcription; if that file does not follow the video's timeline, every cut
lands early or late. This tool cross-correlates the audio the renderer will actually decode (same
pre-roll seek as clip_render.py) with the transcript audio at N points and reports the offsets.

Usage:
  sync_check.py MEDIA TRANSCRIPT_AUDIO [--every 300] [--out sync.json]
Exit code 0 when in sync (all offsets under 40 ms), 2 when a map was written and must be passed to
clip_render.py with --sync.
Needs numpy and ffmpeg.
"""
import argparse, json, subprocess, sys
import numpy as np

SR = 16000
PREROLL = 5.0

def probe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def dec(path, start, dur, preroll=None):
    if preroll is None:
        cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{max(0, start):.3f}", "-i", path, "-t", f"{dur:.3f}",
               "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    else:
        pre = min(preroll, start)
        cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{start - pre:.3f}", "-i", path,
               "-filter_complex", f"[0:a]atrim=start={pre:.3f}:duration={dur:.3f},asetpts=PTS-STARTPTS[a]",
               "-map", "[a]", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, dtype=np.float32).copy()

def measure(media, ref, t, win=6.0, search=4.0):
    """Offset d such that the media audio at time t + d equals the transcript audio at time t."""
    a = dec(ref, t, win)                                   # transcript audio, the pattern
    b = dec(media, t - search, win + 2 * search, PREROLL)  # media audio around the same time
    if len(a) < SR * win * 0.9 or len(b) < len(a) or np.std(a) < 1e-4:
        return None, 0.0
    a = a - a.mean(); b = b - b.mean()
    n = len(a) + len(b); N = 1 << (n - 1).bit_length()
    c = np.fft.irfft(np.fft.rfft(b, N) * np.conj(np.fft.rfft(a, N)), N)[: len(b) - len(a) + 1]
    k = int(np.argmax(c))
    corr = float(c[k] / (np.linalg.norm(a) * np.linalg.norm(b[k:k + len(a)]) + 1e-9))
    return k / SR - search, corr

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("media"); ap.add_argument("transcript_audio")
    ap.add_argument("--every", type=float, default=300.0, help="seconds between measure points")
    ap.add_argument("--out", default="sync.json")
    ap.add_argument("--tolerance", type=float, default=0.04)
    a = ap.parse_args()
    dur = min(probe_dur(a.media), probe_dur(a.transcript_audio))
    ts = list(np.arange(30.0, dur - 15.0, a.every)) + [dur - 15.0]
    pts = []
    for t in ts:
        off, corr = None, 0.0
        for shift in (0.0, 20.0, -20.0, 40.0):             # move off silent or noisy windows
            tt = t + shift
            if 10 < tt < dur - 12:
                off, corr = measure(a.media, a.transcript_audio, tt)
                if off is not None and corr >= 0.8:
                    t = tt; break
        if off is None or corr < 0.8:
            print(f"t={t:8.1f}  no reliable match (corr {corr:.2f})"); continue
        pts.append([round(float(t), 3), round(float(t + off), 4), round(corr, 3)])
        print(f"t={t:8.1f}  media = transcript {off * 1000:+8.1f} ms   corr {corr:.2f}")
    if len(pts) < 2:
        sys.exit("not enough reliable points")
    offs = np.array([p[1] - p[0] for p in pts])
    out = {"media": a.media, "transcript_audio": a.transcript_audio,
           "points": [[p[0], p[1]] for p in pts], "corr": [p[2] for p in pts],
           "offset_ms": {"min": round(float(offs.min() * 1000), 1), "max": round(float(offs.max() * 1000), 1)}}
    in_sync = bool(np.all(np.abs(offs) < a.tolerance))
    out["in_sync"] = in_sync
    json.dump(out, open(a.out, "w"), indent=1)
    if in_sync:
        print(f"IN SYNC: all offsets under {a.tolerance * 1000:.0f} ms. No map needed.")
        sys.exit(0)
    print(f"OUT OF SYNC: offsets from {out['offset_ms']['min']} to {out['offset_ms']['max']} ms. "
          f"Map written to {a.out}: pass it to clip_render.py with --sync.")
    sys.exit(2)

if __name__ == "__main__":
    main()
