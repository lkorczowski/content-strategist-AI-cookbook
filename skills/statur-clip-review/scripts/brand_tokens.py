#!/usr/bin/env python3
"""Brand tokens: one JSON shape for every statur-* skill that draws something (docs/BRAND-TOKENS.md).

The brand is a parameter, never a constant in a script. A tokens file comes from the user's private layer:
  {"name", "surface": "paper"|"ink",
   "colors": {paper, panel, ink, ink_drawing, secondary, accent, highlighter, highlighter_pale},
   "fonts": {display, text, inscription, hand, logo},
   "limits": {accent_gestures_per_screen, highlighter_gestures_per_screen, display_weight, radius},
   "banned_markers": [...]}

Order of precedence: tokens written in the spec or layer, then --tokens / --style FILE, then the BRAND_TOKENS
environment variable, then the neutral defaults below (light paper, dark ink, open-license fonts).
This file is the same in every skill that ships it, so each skill still installs alone. Standard library only.

Check a file:  python3 brand_tokens.py [FILE]    prints the resolved tokens and the flat motion tokens.
"""
import json, os, sys

DEFAULTS = {
    "name": "neutral",
    "surface": "paper",
    "colors": {
        "paper": "#F6F3EC", "panel": "#ECE8DE", "ink": "#20262E", "ink_drawing": "#33415C",
        "secondary": "#6F747B", "accent": "#1F6F5C", "highlighter": "#F4D35E", "highlighter_pale": "#FBF0C4",
    },
    "fonts": {
        "display": "Atkinson Hyperlegible", "text": "Atkinson Hyperlegible", "inscription": "IBM Plex Mono",
        "hand": "Caveat", "logo": "Atkinson Hyperlegible",
    },
    "limits": {"accent_gestures_per_screen": 1, "highlighter_gestures_per_screen": 1, "display_weight": 700, "radius": 0},
    "banned_markers": [],
}
FLAT_KEYS = ("ink", "paper", "accent", "muted", "line", "font_display", "weight_display", "font_body",
             "font_mono", "font_serif", "radius")


def is_flat(raw):
    """True for the older flat motion tokens (ink, paper, accent, font_display, ...)."""
    return isinstance(raw, dict) and "colors" not in raw and "fonts" not in raw and any(k in raw for k in FLAT_KEYS)


def _rgba(hexcol, alpha):
    h = hexcol.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{alpha})"


def resolve(inline=None, path=None):
    """Tokens in the shared shape, every key filled. inline: an object found in a spec; path: a --tokens file."""
    raw = inline
    if not raw:
        path = path or os.environ.get("BRAND_TOKENS")
        if path:
            with open(path, encoding="utf-8") as f:
                raw = json.load(f)
    raw = raw or {}
    out = json.loads(json.dumps(DEFAULTS))
    if is_flat(raw):  # older files keep working: read them as a brand on its own dark surface
        c, f, lim = out["colors"], out["fonts"], out["limits"]
        out["surface"] = "ink"
        for src, dst in (("ink", "ink"), ("paper", "paper"), ("accent", "accent"), ("muted", "secondary")):
            if raw.get(src):
                c[dst] = raw[src]
        for src, dst in (("font_display", "display"), ("font_body", "text"), ("font_mono", "inscription"), ("font_serif", "hand")):
            if raw.get(src):
                f[dst] = raw[src]
        if "weight_display" in raw:
            lim["display_weight"] = raw["weight_display"]
        if "radius" in raw:
            lim["radius"] = raw["radius"]
        out["_flat"] = dict(raw)
        out["_given_fonts"] = sorted({raw[k] for k in ("font_display", "font_body", "font_mono", "font_serif") if raw.get(k)})
        return out
    for k in ("colors", "fonts", "limits"):
        out[k].update({a: b for a, b in (raw.get(k) or {}).items() if b not in (None, "")})
    for k in ("name", "surface", "banned_markers", "font_css"):
        if raw.get(k):
            out[k] = raw[k]
    out["_given_fonts"] = sorted({v for v in (raw.get("fonts") or {}).values() if v})
    return out


def flat(tok):
    """The flat tokens the motion templates read. On a paper surface, panels are paper and text is ink."""
    c, f, lim = tok["colors"], tok["fonts"], tok["limits"]
    dark = tok.get("surface") == "ink"
    ground, text = (c["ink"], c["paper"]) if dark else (c["paper"], c["ink"])
    out = {
        "ink": ground, "paper": text, "accent": c["accent"], "muted": c["secondary"], "line": _rgba(text, ".18"),
        "panel": c["panel"], "ink_drawing": c["ink_drawing"], "highlighter": c["highlighter"],
        "highlighter_pale": c["highlighter_pale"],
        "font_display": f["display"], "weight_display": lim.get("display_weight", 700), "font_body": f["text"],
        "font_mono": f["inscription"], "font_serif": f["hand"], "font_logo": f["logo"], "radius": lim.get("radius", 0),
    }
    out.update(tok.get("_flat") or {})  # an older flat file wins key by key
    return out


if __name__ == "__main__":
    t = resolve(path=sys.argv[1] if len(sys.argv) > 1 else None)
    print(json.dumps({"tokens": {k: v for k, v in t.items() if not k.startswith("_")}, "flat": flat(t)}, indent=1))
