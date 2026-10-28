#!/usr/bin/env python3
"""Turn a pro edit spec (source times) into render inputs on the output timeline.

The spec places every layer element on the SOURCE timeline (the transcript times), so it survives a new
cut: change the silence settings, re-run statur-clip-edit --plan-only, and every graphic follows its words.
This script reads the cut list (cutlist.json) and the kept words (words_out.json) from statur-clip-edit
--plan-only and writes:
  layers/bg.json, layers/under.json, layers/over.json   inputs of statur-motion-design motion_render.py
  plan.json                                              keyed ranges, subject and camera keys, inserts, captions
  sfx.json                                               sound cues for statur-sound-design mix.py

Usage:
  build_layers.py SPEC.json --cutlist cutlist.json --words words_out.json --out WORKDIR [--tokens brand.json]
"""
import argparse, json, os, re, sys

# sound effects added automatically when an element appears: (name, offset in s, gain dB)
AUTO_SFX = {
    "hook_box": [("whoosh", -0.05, -15)],
    "panel": [("whoosh", -0.04, -13)],
    "card_list": [("swish", 0.0, -16)],
    "chips": [],
    "label_chip": [("pop", 0.0, -19)],
    "lower_third": [("swish", 0.0, -16)],
    "big_text": [("whoosh_low", -0.03, -13)],
    "page_card": [("swish", 0.05, -16)],
    "prompt_box": [],
    "chart_curve": [("riser_soft", 0.3, -22)],
    "loop_diagram": [],
    "timeline_cut": [],
    "end_card": [("whoosh", -0.02, -11), ("chime", 0.35, -15)],
    "footnote": [],
}

class Mapper:
    def __init__(self, cut):
        self.m = cut["mapping"]; self.total = cut["duration"]
    def __call__(self, t):
        for p in self.m:
            if p["src_s"] - 1e-6 <= t < p["src_e"]:
                return round(p["out_s"] + (t - p["src_s"]), 4)
            if t < p["src_s"]:
                return round(p["out_s"], 4)          # inside a removed gap: snap to the next kept piece
        return round(self.total, 4)

def when(item, mp, key="src"):
    if "out" in item:
        return float(item["out"][0]), float(item["out"][1])
    s, e = item[key]
    return mp(float(s)), mp(float(e))

def norm(w):
    return re.sub(r"[^\w']", "", w.lower())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("--cutlist", required=True); ap.add_argument("--words", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--tokens", default=None)
    a = ap.parse_args()
    spec = json.load(open(a.spec)); cut = json.load(open(a.cutlist)); words = json.load(open(a.words))
    base = os.path.dirname(os.path.abspath(a.spec))
    mp = Mapper(cut)
    fps = spec.get("fps", 30); W, H = spec.get("w", 1080), spec.get("h", 1920)
    tail = float(spec.get("tail", 0.0))
    dur = round(cut["duration"] + tail, 4)
    tokens = spec.get("tokens") or (json.load(open(a.tokens)) if a.tokens else {})
    os.makedirs(os.path.join(a.out, "layers"), exist_ok=True)

    sfx = []
    def add_sfx(t, name, gain, src=""):
        if t is not None and 0 <= t <= dur:
            sfx.append({"t": round(t, 3), "name": name, "gain_db": gain, "why": src})

    def resolve(v):  # image paths relative to the spec
        if isinstance(v, str) and not v.startswith(("/", "file:", "http", "data:")):
            return os.path.join(base, v)
        return v

    def build(layer_name, items, opaque=False):
        els = []
        for k, it in enumerate(items):
            s, e = when(it, mp)
            props = json.loads(json.dumps(it.get("props", {})))
            for key in ("img", "src"):
                if key in props: props[key] = resolve(props[key])
            for key in ("images", "posters"):
                if key in props: props[key] = [resolve(x) for x in props[key]]
            # local times given in source seconds (t_src) become local output seconds
            for key in ("items", "highlights", "markers"):
                for x in props.get(key, []) or []:
                    if isinstance(x, dict) and "t_src" in x:
                        x["t"] = round(mp(float(x.pop("t_src"))) - s, 3)
            if isinstance(props.get("counter"), dict) and "t_src" in props["counter"]:
                props["counter"]["t"] = round(mp(float(props["counter"].pop("t_src"))) - s, 3)
            if isinstance(props.get("swap"), list):
                for x in props["swap"]:
                    if "t_src" in x: x["t"] = round(mp(float(x.pop("t_src"))) - s, 3)
            for key in ("type_from", "enter_at", "fly"):
                if isinstance(props.get(key + "_src"), (int, float)):
                    props[key] = round(mp(float(props.pop(key + "_src"))) - s, 3)
            el = {"id": it.get("id", f"{layer_name}{k}"), "type": it["type"], "start": s, "end": e, "z": it.get("z", k), "props": props}
            els.append(el)
            if it.get("sfx", True):
                for name, off, g in AUTO_SFX.get(it["type"], []):
                    add_sfx(s + off, name, g, f"{it['type']} in")
                tp = it["type"]
                if tp == "panel" and it.get("sfx_out", True):
                    add_sfx(e - 0.12, "swish_out", -20, "panel out")
                if tp == "chips":
                    for x in props.get("items", []):
                        add_sfx(s + x.get("t", 0), "pop", -17, "chip")
                if tp == "card_list":
                    first, st = props.get("first", 0.35), props.get("stagger", 0.16)
                    for i in range(len(props.get("rows", []))):
                        add_sfx(s + first + i * st, "tick", -21, "row")
                if tp == "big_text" and isinstance(props.get("counter"), dict):
                    c = props["counter"]; t0 = s + c.get("t", 0); d = c.get("dur", 1.0)
                    n = int(d / 0.07)
                    for i in range(n):
                        add_sfx(t0 + i * 0.07 * (1 + i / n), "tick", -26, "counter")
                    add_sfx(t0 + d, "impact", -12, "counter end")
                if tp == "big_text" and isinstance(props.get("swap"), list):
                    for x in props["swap"][1:]:
                        add_sfx(s + x.get("t", 0) - 0.02, "whoosh_low", -16, "swap")
                if tp == "page_card":
                    for h in props.get("highlights", []):
                        add_sfx(s + h.get("t", 0), "click", -17, "highlight")
                if tp == "prompt_box":
                    tf, td = props.get("type_from", 0.3), props.get("type_dur", 1.6)
                    n = max(1, int(len(props.get("text", "")) * 0.55))
                    for i in range(n):
                        add_sfx(s + tf + td * i / n, "key", -24, "typing")
                    ent = props.get("enter_at", tf + td + 0.15)
                    add_sfx(s + ent, "click", -14, "enter")
                    for i in range(len(props.get("lines", []))):
                        add_sfx(s + ent + 0.25 + i * props.get("line_stagger", 0.32), "pop", -18, "result line")
                if tp == "chart_curve":
                    d0, d1 = props.get("draw", [0.4, 2.6])
                    xm = props.get("xmax", 300)
                    for m in props.get("markers", []):
                        add_sfx(s + d0 + d1 * (m["x"] / xm) ** 0.75, "pop", -17, "marker")
                if tp == "loop_diagram":
                    d0, d1 = props.get("draw", [0.3, 1.6]); n = len(props.get("nodes", []))
                    for i in range(n):
                        add_sfx(s + d0 + d1 * i / max(n, 1), "pop", -18, "node")
                if tp == "timeline_cut":
                    sc0, sc1 = props.get("scan", [0.3, 1.5])
                    for cu in props.get("cuts", []):
                        add_sfx(s + sc0 + sc1 * cu["s"], "snip", -15, "cut")
                    fly, fs = props.get("fly", 2.0), props.get("fly_stagger", 0.12)
                    for i in range(len(props.get("posters", []))):
                        add_sfx(s + fly + i * fs, "swish", -21, "clip out")
        json.dump({"layer": layer_name, "w": W, "h": H, "fps": fps, "opaque": opaque, "tokens": tokens, "elements": els},
                  open(os.path.join(a.out, "layers", f"{layer_name}.json"), "w"), indent=1)
        return els

    bg = build("bg", spec.get("bg", []), opaque=True)
    under = build("under", spec.get("under", []))
    over_items = list(spec.get("over", []))

    # captions from the kept words, with emphasis on chosen words (by source time window or by text)
    cap = spec.get("captions", {})
    if cap.get("enabled", True):
        emph_src = [tuple(x) for x in cap.get("emph_src", [])]
        emph_txt = {norm(x) for x in cap.get("emph_words", [])}
        inv = cut["mapping"]
        cw = []
        for w in words:
            src_t = None
            for p in inv:       # map back to source time to test the emphasis windows
                if p["out_s"] - 1e-6 <= w["s"] < p["out_e"]:
                    src_t = p["src_s"] + (w["s"] - p["out_s"]); break
            em = (src_t is not None and any(a0 <= src_t <= b0 for a0, b0 in emph_src)) or norm(w["w"]) in emph_txt
            cw.append({"w": w["w"], "s": w["s"], "e": w["e"], "emph": bool(em)})
        props = dict(cap.get("props", {})); props["words"] = cw
        over_items.insert(0, {"id": "captions", "type": "captions", "out": [0, dur], "props": props, "z": 50, "sfx": False})
        # caption height can move for a while (e.g. when the speaker is scaled down)
        for k, yk in enumerate(cap.get("y_keys", [])):
            s, e = when(yk, mp)
            over_items.append({"id": f"captions_y{k}", "type": "captions", "out": [s, e], "z": 51, "sfx": False,
                               "props": dict(props, y=yk["y"], words=[x for x in cw if s - 0.05 <= x["s"] < e])})
    wm = spec.get("watermark")
    if wm and wm.get("enabled", True):
        s0 = mp(float(wm.get("from_src", 0)))
        # the watermark hides while a full-screen panel, an insert or the end card is on screen
        mute = [list(when(x, mp)) for x in spec.get("over", []) if x["type"] in ("panel", "end_card")]
        mute += [list(when(x, mp)) for x in spec.get("inserts", [])]
        wm = dict(wm, mute=mute)
        over_items.append({"id": "watermark", "type": "watermark", "out": [s0, mp(float(wm.get("to_src", 1e9))) if "to_src" in wm else cut["duration"]],
                           "props": {k: v for k, v in wm.items() if k not in ("from_src", "to_src", "enabled")}, "z": 60, "sfx": False})
    over = build("over", over_items)
    # captions with y_keys: hide the main caption element during those windows
    ov = json.load(open(os.path.join(a.out, "layers", "over.json")))
    ykw = [(x["start"], x["end"]) for x in ov["elements"] if x["id"].startswith("captions_y")]
    for x in ov["elements"]:
        if x["id"] == "captions" and ykw:
            x["props"]["words"] = [w for w in x["props"]["words"] if not any(s - 0.05 <= w["s"] < e for s, e in ykw)]
    json.dump(ov, open(os.path.join(a.out, "layers", "over.json"), "w"), indent=1)

    for x in spec.get("sfx", []):
        t = mp(float(x["src"])) if "src" in x else float(x["out"])
        add_sfx(t + x.get("offset", 0), x["name"], x.get("gain_db", -14), x.get("why", "manual"))
    sfx.sort(key=lambda x: x["t"])
    json.dump({"duration": dur, "cues": sfx}, open(os.path.join(a.out, "sfx.json"), "w"), indent=1)

    def keys(lst, fields):
        out = []
        for k in lst:
            t = mp(float(k["src"])) if "src" in k else float(k["out"])
            out.append(dict({f: k[f] for f in fields if f in k}, t=t, dur=k.get("dur", 0.3), ease=k.get("ease", "inOutCubic")))
        return sorted(out, key=lambda x: x["t"])
    plan = {"fps": fps, "w": W, "h": H, "duration": dur, "speech_duration": cut["duration"], "tail": tail,
            "keyed": [list(when({"src": r}, mp)) for r in spec.get("keyed", [])],
            "subject_keys": keys(spec.get("subject_keys", []), ["s", "ax", "ay", "dx", "dy"]),
            "camera_keys": keys(spec.get("camera_keys", []), ["z", "fx", "fy", "ox", "oy"]),
            "inserts": [dict(x, start=when(x, mp)[0], end=when(x, mp)[1], file=resolve(x["file"])) for x in spec.get("inserts", [])],
            "music": dict({k: v for k, v in spec.get("music", {}).items() if k not in ("drop_src", "drops_out")},
                          drops=[f"{round(mp(float(x)), 3)}" for x in spec.get("music", {}).get("drop_src", [])]
                                + [f"{w[0]}-{w[1]}" for w in spec.get("music", {}).get("drops_out", [])]),
            "mapping": cut["mapping"]}
    json.dump(plan, open(os.path.join(a.out, "plan.json"), "w"), indent=1)
    print(json.dumps({"status": "DONE", "duration": dur, "bg": len(bg), "under": len(under), "over": len(over), "sfx": len(sfx)}))

if __name__ == "__main__":
    main()
