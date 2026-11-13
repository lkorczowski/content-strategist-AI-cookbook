#!/usr/bin/env python3
"""Make a short 3D video, or a 3D plate for an edit, from a preset, with the best renderer this machine has.

Engines:
  cpu   statur-motion-3d engine v2 (Three.js in headless Chromium, SwiftShader, ffmpeg). Runs anywhere, with the
        brand overlay (tag, title, HUD, captions, end card) and a synthesized sound bed.
  vork  vork (github.com/voyager-so/vork) on Apple Silicon with macOS 26, or on an NVIDIA GPU with Vulkan ray
        queries. Writes the vork scene of the preset and renders the 3D picture; the overlay and the sound
        still come from the cpu pass, composited on top. Pass --engine vork only on such a machine.
  auto  vork when `vork --version` answers and `vork setup` reports a usable GPU, else cpu.

Usage:
  make_short.py --preset voice-to-world --out short.mp4 [--work DIR] [--engine auto|cpu|vork]
                [--from S --to S] [--plate] [--scenario my.json] [--city LAT,LON] [--part 14]
  --plate     no overlay and no sound: a picture to insert in an edit (statur-video-editor-pro, motion3d inserts)
  --from/--to a range of the preset timeline, in seconds (default: the whole scenario)
  --scenario  a scenario.json that replaces the preset texts (captions, HUD, end card, music, sfx)
  --city      the speaker's city for the globe (default: Paris 48.86,2.35)
"""
import argparse, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
M3D = os.path.join(os.path.dirname(SKILL), "statur-motion-3d")
PLATE_CSS = "<style>#tag,#site,#title,#hud,#cap,#src,#end{display:none!important}</style>"


def sh(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd)[:240], flush=True)
    r = subprocess.run([str(c) for c in cmd], **kw)
    if r.returncode:
        sys.exit(f"failed: {cmd[0]} (exit {r.returncode})")


def vork_ready():
    if not shutil.which("vork"):
        return False
    try:
        out = subprocess.run(["vork", "setup"], capture_output=True, text=True, timeout=900)
        return out.returncode == 0
    except Exception:
        return False


def workspace(work, plate):
    """statur-motion-3d v2 workspace, created once; plate mode gets its own index page without overlay."""
    if not os.path.exists(os.path.join(work, "node_modules", "three")):
        sh(["bash", os.path.join(M3D, "scripts", "setup_project2.sh"), work])
    html = open(os.path.join(M3D, "engine2", "index.html")).read()
    page = "plate.html" if plate else "index.html"
    if plate:
        html = html.replace("</head>", PLATE_CSS + "</head>")
    open(os.path.join(work, page), "w").write(html)
    return page


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--preset", default="voice-to-world")
    ap.add_argument("--out", required=True)
    ap.add_argument("--work", default=os.path.expanduser("~/.cache/statur-vork-3d"))
    ap.add_argument("--engine", default="auto", choices=["auto", "cpu", "vork"])
    ap.add_argument("--from", dest="t0", type=float, default=0.0)
    ap.add_argument("--to", dest="t1", type=float, default=None)
    ap.add_argument("--plate", action="store_true")
    ap.add_argument("--scenario", default=None)
    ap.add_argument("--city", default=None, help="LAT,LON of the speaker")
    ap.add_argument("--part", type=float, default=14.0, help="seconds per render part (sandboxes stop long commands)")
    a = ap.parse_args()

    pdir = os.path.join(SKILL, "presets", a.preset)
    if not os.path.isdir(pdir):
        sys.exit(f"unknown preset {a.preset}: " + ", ".join(sorted(os.listdir(os.path.join(SKILL, 'presets')))))
    work = os.path.abspath(a.work); os.makedirs(work, exist_ok=True)
    page = workspace(work, a.plate)
    sub = os.path.join(work, a.preset); os.makedirs(sub, exist_ok=True)
    shutil.copy(os.path.join(pdir, "shots.js"), sub)
    shutil.copy(a.scenario or os.path.join(pdir, "scenario.json"), os.path.join(sub, "scenario.json"))
    data = os.path.join(sub, "data.json")
    if not os.path.exists(data) or a.city:
        city = a.city.split(",") if a.city else []
        sh([sys.executable, os.path.join(pdir, "gen_data.py"), data] + city)
    S = json.load(open(os.path.join(sub, "scenario.json")))
    t1 = a.t1 if a.t1 is not None else float(S["duration"])
    engine = a.engine if a.engine != "auto" else ("vork" if vork_ready() else "cpu")
    print(json.dumps({"engine": engine, "preset": a.preset, "range": [a.t0, t1], "plate": a.plate}), flush=True)

    render2 = os.path.join(M3D, "scripts", "render2.js")
    env = dict(os.environ, SUB=a.preset, PAGE=page)
    parts, t = [], a.t0
    pdir_out = os.path.join(work, "parts", a.preset + ("-plate" if a.plate else "")); os.makedirs(pdir_out, exist_ok=True)
    out = os.path.abspath(a.out)
    if engine == "vork":
        scene = os.path.join(sub, "scene.json")
        sh([sys.executable, os.path.join(HERE, "vork_scene.py"), "--data", data, "--scenario", os.path.join(sub, "scenario.json"), "--out", scene])
        f0, f1 = int(round(a.t0 * S.get("fps", 30))), int(round(t1 * S.get("fps", 30))) - 1
        plate3d = os.path.join(sub, "vork_plate.mp4")
        sh(["vork", "render", scene, "--profile", "std/draft", "--frame-start", f0, "--frame-end", f1, "--out", plate3d])
        if a.plate:
            shutil.copy(plate3d, out); print(json.dumps({"status": "DONE", "out": out})); return
        sys.exit("vork full shorts need the overlay compositing step, not built yet: use --plate with vork, or --engine cpu")
    while t < t1 - 1e-6:
        e = min(t1, t + a.part)
        p = os.path.join(pdir_out, f"p{t:07.2f}-{e:07.2f}.mp4")
        if not os.path.exists(p):
            sh(["node", render2, work, "video", p, t, e], env=env)
        parts.append(p); t = e
    lst = os.path.join(pdir_out, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    silent = os.path.join(pdir_out, "silent.mp4")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])
    if a.plate:
        shutil.copy(silent, out)
    else:
        wav = os.path.join(pdir_out, "sound.wav")
        sh([sys.executable, os.path.join(M3D, "scripts", "sound2.py"), os.path.join(sub, "scenario.json"), wav])
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-ss", a.t0, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out])
    print(json.dumps({"status": "DONE", "out": out, "engine": engine}))


if __name__ == "__main__":
    main()
