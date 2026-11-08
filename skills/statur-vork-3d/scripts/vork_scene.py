#!/usr/bin/env python3
"""Write the vork scene (scene JSON version 2) of the voice-to-world preset, from the same data.json and
scenario.json as the CPU engine, so both renderers tell the same story on the same timeline.

Usage:
  vork_scene.py --data data.json --scenario scenario.json --out scene.json [--schema scene.schema.json] [--res 720x1280]

Then, on a GPU machine (Apple Silicon with macOS 26, or an NVIDIA GPU with Vulkan ray queries):
  vork render scene.json --profile std/previs --at 9 --out check.png      # stills first
  vork render scene.json --profile std/draft --out silent.mp4             # full movie
The overlay (captions, HUD, end card) and the sound come from the CPU engine pass (make_short.py --overlay-only).

Mapping to vork (how the story is expressed with plain scene data, no custom programs):
- a node switches on by scaling from 0 to 1 at its time (a zero world scale hides geometry, children included);
- glow is OpenPBR emission (emission_color, emission_luminance), animated with material tracks;
- crowds, network nodes and land dots are instanced meshes, batched by switch-on time;
- the camera aims at an "aim" node; both follow keys sampled from the same camera curve as the CPU engine;
- the Earth spin is a rotation track on the "world" node, around the real axis.
"""
import argparse, json, math, sys

import numpy as np

RG = 3000.0  # globe radius in metres, same as shots.js
PAPER, TEAL, WARM, SIG = [0.89, 0.86, 0.80], [0.11, 0.77, 0.58], [1.0, 0.70, 0.45], [0.80, 0.08, 0.01]  # linear Rec.709


def ease(k):
    return 2 * k * k if k < .5 else 1 - (-2 * k + 2) ** 2 / 2


def norm(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


# camera keys copied from shots.js: [t, target, direction, distance]
CAM = [(0, (0, RG + .6, 0), (.12, .36, 1), 12), (7.6, (0, RG + .6, 0), (.45, .45, 1), 14.5),
       (13.2, (0, RG + .5, 0), (.35, .9, .8), 46), (18.8, (0, RG, 0), (.25, 1, .55), 1700),
       (22.6, (0, RG, 0), (.18, 1, .5), 2300), (30.8, (0, 0, 0), (.18, .82, .62), 15800), (41, (0, 0, 0), (.18, .82, .62), 15800)]


def cam_at(t):
    i = 0
    while i < len(CAM) - 2 and t > CAM[i + 1][0]:
        i += 1
    ta, A, dA, la = CAM[i]
    tb, B, dB, lb = CAM[i + 1]
    k = ease(min(1, max(0, (t - ta) / (tb - ta))))
    tgt = np.asarray(A) + (np.asarray(B) - np.asarray(A)) * k
    d = norm(norm(dA) + (norm(dB) - norm(dA)) * k)
    dist = math.exp(math.log(la) + (math.log(lb) - math.log(la)) * k)
    return tgt + d * dist, tgt


def quat_axis(axis, ang):
    a = norm(axis) * math.sin(ang / 2)
    return [float(a[0]), float(a[1]), float(a[2]), math.cos(ang / 2)]


def mat(color, rough=.6, emit=None, lum=0.0):
    inp = {"base_color": color, "specular_roughness": rough}
    if emit is not None:
        inp.update({"emission_color": emit, "emission_luminance": lum})
    return {"program": "std/openpbr", "inputs": inp}


def inst(points):
    pts = [[round(float(x), 3) for x in p] for p in points]
    return {"attributes": {"TRANSLATION": {"type": "vec3", "data": pts}}}


def build(data, scen, res):
    dur = float(scen["duration"])
    nodes, tracks, materials = [], [], {}
    materials.update({
        "ground": mat([0.012, 0.012, 0.014], .9), "globe": mat([0.006, 0.007, 0.009], .8),
        "crowd": mat([0.08, 0.09, 0.12], .7), "speaker": mat([0.85, 0.83, 0.78], .5, WARM, 0.0),
        "ring": mat([0, 0, 0], .9, PAPER, 0.0), "node": mat([0, 0, 0], .9, PAPER, 6.0),
        "teal": mat([0, 0, 0], .9, TEAL, 0.0), "land_dim": mat([0.03, 0.03, 0.03], .9, PAPER, 0.15),
        "land_lit": mat([0, 0, 0], .9, PAPER, 4.0),
        "camera-optics": {"program": "std/camera", "inputs": {"lens": 35.0, "clip_end": 80000}},
    })
    tracks.append({"path": ["materials", "speaker", "inputs", "emission_luminance"], "keys": [[0, 0.4], [13, 0.4], [18, 6], [22.4, 6], [22.6, 30], [24, 8], [33, 8], [35, 0], [dur, 0]]})
    tracks.append({"path": ["materials", "teal", "inputs", "emission_luminance"], "keys": [[0, 0], [18.9, 0], [19.2, 40], [29, 40], [31, 0], [dur, 0]]})
    world = {"type": "node", "name": "world", "children": []}
    W = world["children"]
    top = [0, RG, 0]
    # globe and ground
    W.append({"type": "mesh", "name": "globe", "geometry": {"std": "sphere", "radius": RG - 1.2, "segments": 192, "rings": 128}, "materials": ["globe"]})
    W.append({"type": "mesh", "name": "ground", "translation": top, "geometry": {"std": "grid", "size": [180, 180]}, "materials": ["ground"]})
    # speaker: body and head, glowing after the opportunity comes back
    W.append({"type": "mesh", "name": "speaker", "translation": [0, RG + .9, 0], "geometry": {"std": "capsule", "radius": .32, "height": 1.8}, "materials": ["speaker"],
              "children": [{"type": "mesh", "name": "speaker-head", "translation": [0, 1.15, 0], "geometry": {"std": "sphere", "radius": .3}, "materials": ["speaker"]}]})
    # crowd: one instanced capsule mesh (same seeded layout idea as shots.js, not the same people)
    rng = np.random.default_rng(11)
    crowd = []
    while len(crowd) < 520:
        r, a = 2.6 + math.sqrt(rng.random()) * 26, rng.random() * 2 * math.pi
        x, z = math.cos(a) * r, math.sin(a) * r
        if abs(x) < 3 and 0 < z < 14:
            continue
        crowd.append([x, RG + .85, z])
    W.append({"type": "mesh", "name": "crowd", "geometry": {"std": "capsule", "radius": .25, "height": 1.7}, "materials": ["crowd"], "instances": inst(crowd)})
    # listeners: light up at their time
    LIST = [(8.3, (2.2, -3.2)), (10.8, (-4.8, -2.6)), (11.9, (4.6, 2.2))] + [(12.3 + i * .07, (math.cos(a) * r, math.sin(a) * r)) for i, (a, r) in enumerate(zip(rng.random(14) * 6.28, 6 + rng.random(14) * 16))]
    for i, (t0, (x, z)) in enumerate(LIST):
        m = f"listener-{i}"
        materials[m] = mat([0.08, 0.09, 0.12], .7, PAPER, 0.0)
        tracks.append({"path": ["materials", m, "inputs", "emission_luminance"], "keys": [[0, 0], [t0, 0], [t0 + .3, 12], [t0 + 1.5, 3], [dur, 3]]})
        W.append({"type": "mesh", "name": m, "translation": [x, RG + .85, z], "geometry": {"std": "capsule", "radius": .26, "height": 1.7}, "materials": [m]})
    # voice rings: torus scaled out from the speaker every 1.3 s until 13.6 s
    for i in range(8):
        name = f"ring-{i}"
        keys, lum = [[0, [0, 0, 0]]], [[0, 0.0]]
        t = i * 1.3
        while t < 13.6:
            reach = 9 if t < 8 else 16
            life = (reach - .4) / 5.5
            keys += [[round(t, 3), [.4, .4, .4]], [round(t + life, 3), [reach, reach, reach]], [round(t + life + .01, 3), [0, 0, 0]]]
            t += 1.3 * 8
        keys.append([dur, [0, 0, 0]])
        materials[name] = mat([0, 0, 0], .9, PAPER, 1.5)
        W.append({"type": "mesh", "name": name, "translation": [0, RG + 1.7, 0], "scale": [0, 0, 0], "geometry": {"std": "torus", "radius": 1, "tube": .015, "segments": 96, "rings": 6}, "materials": [name]})
        tracks.append({"path": ["nodes", name, "scale"], "keys": keys})
    # network nodes in 12 batches by switch-on time
    P = np.asarray(data["nodes"]).reshape(-1, 3) * (RG + 1.5)
    tn = 12.6 + 6.0 * np.log(np.asarray(data["d"]) / 0.004) / math.log(0.42 / 0.004)
    edges = np.linspace(tn.min() - 1e-3, tn.max() + 1e-3, 13)
    for b in range(12):
        sel = (tn >= edges[b]) & (tn < edges[b + 1])
        if not sel.any():
            continue
        name = f"nodes-{b}"
        W.append({"type": "mesh", "name": name, "scale": [0, 0, 0], "geometry": {"std": "sphere", "radius": 1.0, "segments": 8, "rings": 4}, "materials": ["node"], "instances": inst(P[sel])})
        t0 = float(edges[b + 1])
        tracks.append({"path": ["nodes", name, "scale"], "keys": [[0, [0, 0, 0]], [t0, [0, 0, 0]], [t0 + .01, [1, 1, 1]], [dur, [1, 1, 1]]]})
    # opportunity: teal pulse that travels the chain back to the speaker between 19.4 and 22.5 s
    chain = [P[i] for i in data["chain"]] + [np.array([0, RG + 2.1, 0])]
    keys = [[0, chain[0].round(3).tolist()]]
    for s, p in enumerate(chain):
        keys.append([round(19.4 + 3.1 * s / (len(chain) - 1), 3), p.round(3).tolist()])
    keys.append([dur, chain[-1].round(3).tolist()])
    W.append({"type": "mesh", "name": "opportunity", "geometry": {"std": "sphere", "radius": 6.0}, "materials": ["teal"]})
    tracks.append({"path": ["nodes", "opportunity", "translation"], "keys": keys})
    trail = []
    for s in range(len(chain) - 1):
        for k in range(12):
            trail.append(chain[s] + (chain[s + 1] - chain[s]) * k / 12 + np.array([0, 2, 0]))
    W.append({"type": "mesh", "name": "trail", "scale": [0, 0, 0], "geometry": {"std": "sphere", "radius": 2.5, "segments": 8, "rings": 4}, "materials": ["teal"], "instances": inst(trail)})
    tracks.append({"path": ["nodes", "trail", "scale"], "keys": [[0, [0, 0, 0]], [19.4, [0, 0, 0]], [19.41, [1, 1, 1]], [dur, [1, 1, 1]]]})
    # land dots: always-dim layer plus lit layer in 8 batches from the speaker outwards (24.0 to 30.5 s)
    LP = np.asarray(data["land"]).reshape(-1, 3) * (RG + 2)
    ang = np.asarray(data["land_ang"])
    W.append({"type": "mesh", "name": "land-dim", "geometry": {"std": "sphere", "radius": 7.0, "segments": 6, "rings": 3}, "materials": ["land_dim"], "instances": inst(LP)})
    for b in range(8):
        sel = (ang >= math.pi * b / 8) & (ang < math.pi * (b + 1) / 8 + 1e-9)
        if not sel.any():
            continue
        name = f"land-{b}"
        t0 = 24.0 + 6.5 * (b + 1) / 8
        W.append({"type": "mesh", "name": name, "scale": [0, 0, 0], "geometry": {"std": "sphere", "radius": 7.5, "segments": 6, "rings": 3}, "materials": ["land_lit"], "instances": inst(LP[sel])})
        tracks.append({"path": ["nodes", name, "scale"], "keys": [[0, [0, 0, 0]], [t0, [0, 0, 0]], [t0 + .01, [1, 1, 1]], [dur, [1, 1, 1]]]})
    # light over the speaker, low sky light everywhere
    W.append({"type": "light", "name": "key", "shape": "spot", "translation": [3, RG + 14, 6], "target": top, "energy": 9000, "color": [1, .89, .77], "spot_size": 1.0})
    nodes.append(world)
    nodes.append({"type": "light", "name": "moon", "shape": "sun", "rotation": {"euler": [-1.0, .4, 0]}, "energy": .6, "color": [.75, .8, 1]})
    # camera, aim node, keys sampled every 0.25 s from the same curve as the CPU engine
    nodes.append({"type": "node", "name": "aim", "translation": [0, RG + .6, 0]})
    nodes.append({"type": "camera", "name": "cam", "translation": [0, RG + 5, 12], "target": "aim", "material": "camera-optics"})
    ck, ak = [], []
    for i in range(int(dur * 4) + 1):
        t = i / 4
        p, g = cam_at(t)
        ck.append([t, [round(float(x), 3) for x in p]])
        ak.append([t, [round(float(x), 3) for x in g]])
    tracks += [{"path": ["nodes", "cam", "translation"], "keys": ck}, {"path": ["nodes", "aim", "translation"], "keys": ak}]
    # Earth spin around the real axis, faster and faster after 30.8 s (same law as shots.js)
    north = data["north"]
    rk = []
    for i in range(int(dur * 10) + 1):
        t = i / 10
        u = max(0, t - 30.8)
        rk.append([t, quat_axis(north, .02 * u + .09 * u ** 3)])
    tracks.append({"path": ["nodes", "world", "rotation"], "keys": rk})
    w, h = res
    return {"version": 2, "materials": materials, "nodes": nodes, "animation": [{"tracks": tracks}],
            "render": {"resolution": [w, h], "fps": int(scen.get("fps", 30)), "duration": dur, "camera": "cam", "background": [0.002, 0.002, 0.003]}}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--data", required=True)
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--schema", help="vork editor schema (packages/ts/scene.schema.json in the vork repo) to validate against")
    ap.add_argument("--res", default="720x1280")
    a = ap.parse_args()
    res = [int(x) for x in a.res.lower().split("x")]
    scene = build(json.load(open(a.data)), json.load(open(a.scenario)), res)
    json.dump(scene, open(a.out, "w"), separators=(",", ":"))
    print(f"scene written to {a.out}: {len(scene['animation'][0]['tracks'])} tracks")
    if a.schema:
        import jsonschema
        # the editor schema describes expanded scenes; std builders ({"std": ...}) expand in vork's loader first,
        # so they are swapped for a resource name before validation (the official first-scene.json needs the same)
        def strip(o):
            if isinstance(o, dict):
                return {k: ("std-geometry" if k == "geometry" and isinstance(v, dict) and "std" in v else strip(v)) for k, v in o.items()}
            return [strip(x) for x in o] if isinstance(o, list) else o
        errs = sorted(jsonschema.Draft202012Validator(json.load(open(a.schema))).iter_errors(strip(scene)), key=lambda e: list(e.path))
        for e in errs[:20]:
            print("SCHEMA", "/".join(map(str, e.path)), e.message[:200])
        print("schema:", "PASS" if not errs else f"FAIL ({len(errs)} errors)")
        sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
