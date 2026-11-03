#!/usr/bin/env python3
"""One command for a pro edit: plate, grade, cut list, matte, motion layers, sound, composite, QA.
Each step writes its output in WORK and is skipped on the next run when that output exists, so a change
to the spec re-renders only what it touches (delete a step's output, or pass --redo step,step).

The companion skills must sit next to this one (skills/statur-color-grade, statur-motion-design,
statur-sound-design, statur-clipping), as they do in the cookbook repository.

Usage:
  render_pro.py --spec pro.json --clip-spec clip.json --source SRC.mp4 --words words.json --work WORK
                [--grade natural|editorial|grade.cube] [--music auto|none|track.wav] [--rnnoise model.rnnn]
                [--matte-model rvm_mobilenetv3_fp32.onnx] [--sync sync.json] [--redo layers,sound] [--crf 16]
  --clip-spec: the statur-clip-plan spec (segments, cut, fix, silence) that defines the cut
  --spec:      the pro spec (layers, captions, keys, inserts, sfx), times on the source timeline
"""
import argparse, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.dirname(os.path.dirname(HERE))
P = {
    "plate": os.path.join(SK, "statur-color-grade", "scripts", "plate.py"),
    "lut": os.path.join(SK, "statur-color-grade", "scripts", "make_lut.py"),
    "scopes": os.path.join(SK, "statur-color-grade", "scripts", "scopes.py"),
    "clip_render": os.path.join(SK, "statur-clipping", "scripts", "clip_render.py"),
    "qa_clip": os.path.join(SK, "statur-clipping", "scripts", "qa_clip.py"),
    "motion": os.path.join(SK, "statur-motion-design", "scripts", "motion_render.py"),
    "sfx": os.path.join(SK, "statur-sound-design", "scripts", "sfx_synth.py"),
    "music": os.path.join(SK, "statur-sound-design", "scripts", "music_bed.py"),
    "mix": os.path.join(SK, "statur-sound-design", "scripts", "mix.py"),
    "build": os.path.join(HERE, "build_layers.py"), "matte": os.path.join(HERE, "matte.py"),
    "comp": os.path.join(HERE, "composite.py"), "qa": os.path.join(HERE, "qa_pro.py"),
}

def run(step, cmd):
    t = time.time()
    print(json.dumps({"step": step, "cmd": " ".join(str(c) for c in cmd)[:300]}), flush=True)
    r = subprocess.run([str(c) for c in cmd])
    if r.returncode:
        print(json.dumps({"step": step, "status": "FAILED"})); sys.exit(1)
    print(json.dumps({"step": step, "status": "DONE", "seconds": round(time.time() - t, 1)}), flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True); ap.add_argument("--clip-spec", required=True)
    ap.add_argument("--source", required=True); ap.add_argument("--words", required=True); ap.add_argument("--work", required=True)
    ap.add_argument("--grade", default="natural"); ap.add_argument("--music", default="auto"); ap.add_argument("--rnnoise", default=None)
    ap.add_argument("--matte-model", default=None); ap.add_argument("--sync", default=None)
    ap.add_argument("--redo", default=""); ap.add_argument("--crf", type=int, default=16); ap.add_argument("--sharpen", type=float, default=0.3)
    ap.add_argument("--grain", type=float, default=2.0, help="film grain in 8-bit levels, 0 to turn off")
    ap.add_argument("--out", default=None, help="master path (default WORK/master.mp4)")
    a = ap.parse_args()
    W = os.path.abspath(a.work); os.makedirs(W, exist_ok=True)
    redo = set(x for x in a.redo.split(",") if x)
    need = lambda step, path: step in redo or not os.path.exists(path)
    py = sys.executable
    spec = json.load(open(a.spec))
    # 1. plate (SDR, tone mapped when the source is HDR)
    plate = os.path.join(W, "plate.mov")
    if need("plate", plate):
        run("plate", [py, P["plate"], a.source, plate])
    # 2. grade
    lut = a.grade if a.grade.endswith(".cube") else os.path.join(W, f"grade_{a.grade}.cube")
    if not a.grade.endswith(".cube") and need("grade", lut):
        run("grade", [py, P["lut"], lut, "--preset", a.grade])
    graded = os.path.join(W, "plate_graded.mp4")
    if need("grade", graded):
        vf = f"lut3d=file='{lut}':interp=tetrahedral" + (f",cas=strength={a.sharpen:g}" if a.sharpen > 0 else "")
        run("grade", ["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", plate, "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", "-an", graded])
        run("scopes", [py, P["scopes"], graded, "--times", "1,5,10", "--sheet", os.path.join(W, "scopes.jpg"), "--json", os.path.join(W, "scopes.json")])
    # 3. cut list (one cut logic: statur-clip-edit --plan-only)
    cutdir = os.path.join(W, "cut")
    if need("cut", os.path.join(cutdir, "cutlist.json")):
        cmd = [py, P["clip_render"], "--source", plate, "--words", a.words, "--spec", a.clip_spec, "--out", cutdir, "--plan-only"]
        if a.sync:
            cmd += ["--sync", a.sync]
        run("cut", cmd)
    # 4. matte, only when the spec uses it (keyed ranges or a layer behind the speaker)
    matte = os.path.join(W, "matte.mkv")
    if (spec.get("keyed") or spec.get("under")) and need("matte", matte):
        if not a.matte_model:
            sys.exit("the spec needs a person matte: pass --matte-model (see statur-video-editor-pro references/slots.md)")
        run("matte", [py, P["matte"], plate, matte, "--model", a.matte_model])
    elif not os.path.exists(matte):
        # no effect needs the speaker cut out: an all-white matte keeps the compositor simple
        run("matte", ["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", plate, "-vf", "format=gray,geq=lum=255", "-c:v", "ffv1", "-an", matte])
    # 5. layers
    lay = os.path.join(W, "layers")
    if need("layers", os.path.join(W, "plan.json")) or "layers" in redo:
        run("build", [py, P["build"], a.spec, "--cutlist", os.path.join(cutdir, "cutlist.json"), "--words", os.path.join(cutdir, "words_out.json"), "--out", W])
        plan = json.load(open(os.path.join(W, "plan.json")))
        for L in ("bg", "under", "over"):
            run(f"motion_{L}", [py, P["motion"], os.path.join(lay, f"{L}.json"), os.path.join(W, "frames", L), "--duration", plan["duration"]])
    plan = json.load(open(os.path.join(W, "plan.json")))
    # 6. sound
    lib = os.path.join(W, "sfx")
    if need("sound", os.path.join(lib, "manifest.json")):
        run("sfx", [py, P["sfx"], lib])
    music = None
    if a.music == "auto":
        music = os.path.join(W, "music.wav")
        if need("sound", music):
            m = plan.get("music", {})
            run("music", [py, P["music"], music, "--duration", plan["duration"], "--bpm", m.get("bpm", 100), "--key", m.get("key", "A"),
                          "--drops", ",".join(str(x) for x in m.get("drops", []))])
    elif a.music != "none":
        music = a.music
    mix = os.path.join(W, "mix.wav")
    if need("sound", mix):
        cmd = [py, P["mix"], "--source", a.source, "--plan", os.path.join(W, "plan.json"), "--sfx", os.path.join(W, "sfx.json"), "--lib", lib, "--out", mix]
        if music:
            cmd += ["--music", music]
        if a.rnnoise:
            cmd += ["--rnnoise", a.rnnoise]
        run("mix", cmd)
    # 7. composite
    master = a.out or os.path.join(W, "master.mp4")
    if need("composite", master):
        # parts of 300 frames: a stopped run resumes where it stopped, and no single command runs for long
        parts_dir = os.path.join(W, "parts"); os.makedirs(parts_dir, exist_ok=True)
        n = int(round(plan["duration"] * plan["fps"])); parts = []
        for lo in range(0, n, 300):
            part = os.path.join(parts_dir, f"p{lo:05d}.mp4"); parts.append(part)
            if "composite" in redo or not os.path.exists(part):
                run(f"composite {lo}", [py, P["comp"], "--plate", graded, "--matte", matte, "--plan", os.path.join(W, "plan.json"),
                                        "--layers", os.path.join(W, "frames"), "--out", part, "--crf", a.crf, "--preset", "fast",
                                        "--grain", a.grain, "--segment", f"{lo}-{min(n, lo + 300) - 1}"])
        run("join", [py, P["comp"], "--plate", graded, "--matte", matte, "--plan", os.path.join(W, "plan.json"), "--layers", os.path.join(W, "frames"),
                     "--audio", mix, "--out", master, "--join"] + parts)
        up = os.path.splitext(master)[0] + "_upload.mp4"
        run("upload copy", ["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", master, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                            "-maxrate", "4500k", "-bufsize", "9000k", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                            "-colorspace", "bt709", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", up])
    # 8. quality gate
    run("qa", [py, P["qa"], master, "--plan", os.path.join(W, "plan.json"), "--layers", os.path.join(W, "frames"),
               "--words", os.path.join(cutdir, "words_out.json"), "--qa-clip", P["qa_clip"]])
    print(json.dumps({"status": "DONE", "master": master, "qa": os.path.splitext(master)[0] + "_qa.json"}))

if __name__ == "__main__":
    main()
