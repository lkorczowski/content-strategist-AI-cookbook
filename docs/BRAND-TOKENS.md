# Brand tokens

One JSON file describes a brand to every skill that draws something: videos, captions, motion design, 3D overlays, review pages. The public skills hold no brand. They read this file, or fall back to a neutral look.

Example with neutral values: [brand-tokens.example.json](brand-tokens.example.json). Keep your real file in your private repo, next to kb/01_BRAND.md. Do not commit it here.

## Shape

```json
{
  "name": "neutral",
  "surface": "paper",
  "colors": {"paper": "", "panel": "", "ink": "", "ink_drawing": "", "secondary": "", "accent": "", "highlighter": "", "highlighter_pale": ""},
  "fonts": {"display": "", "text": "", "inscription": "", "hand": "", "logo": ""},
  "limits": {"accent_gestures_per_screen": 1, "highlighter_gestures_per_screen": 1, "display_weight": 700, "radius": 0},
  "banned_markers": []
}
```

| Key | Meaning |
|---|---|
| `name` | Short brand name. Shown in a tag or an end line only when a skill has one. `neutral` shows nothing. |
| `surface` | `paper` (default): grounds and panels are paper, text is ink. `ink`: the reverse, for a brand that lives on a dark ground. |
| `colors.paper` | The ground: title cards, panels, the hook box, the review page. |
| `colors.panel` | A second ground, slightly darker or lighter than paper: side panels, table rows. |
| `colors.ink` | Text and outlines. |
| `colors.ink_drawing` | Lines of diagrams and hand-drawn marks (circle, arrow, note) when they differ from the text ink. |
| `colors.secondary` | Secondary text, rules, borders. |
| `colors.accent` | The one color of emphasis: a chip, a border, a label box. |
| `colors.highlighter` | A marker stroke behind or under a key word. The active caption word. |
| `colors.highlighter_pale` | The same marker at low strength, for a large area. |
| `fonts.display` | Titles and hooks. |
| `fonts.text` | Captions, body, labels. |
| `fonts.inscription` | Small technical lines: sources, dates, data. |
| `fonts.hand` | Hand notes and annotations, rare quotes. |
| `fonts.logo` | The wordmark, when it is set in type. |
| `limits.accent_gestures_per_screen` | How many accent elements one frame may hold. The agent checks it on stills. |
| `limits.highlighter_gestures_per_screen` | Same for highlighter strokes. |
| `limits.display_weight`, `limits.radius` | Weight of the display font, corner radius of boxes in px. |
| `banned_markers` | What this brand never shows, in plain words. The agent reads the list before planning and checks every still against it. Scripts do not enforce it. |
| `font_css` (optional) | URL of a stylesheet that declares the fonts, for HTML pages such as the review page. |
| `site` (optional) | Domain shown where a skill prints one. |

Fonts are family names. Renderers that need files find them by package or folder; each skill says how. Use fonts whose license allows video.

## How a skill receives it

Order of precedence, the same everywhere:

1. `tokens` written inside the spec, the layer or the scenario (`brand` in a statur-motion-3d scenario).
2. `--tokens FILE` on the command line (alias `--style FILE`).
3. The `BRAND_TOKENS` environment variable (a path).
4. The neutral defaults: light paper, dark ink, one quiet accent, open-license fonts.

Every script runs with no tokens file. Keys left out take the neutral value. The older flat motion tokens (`ink`, `paper`, `accent`, `muted`, `font_display`, ...) still load: they are read as a brand on its own dark surface.

| Skill | Entry point | What the tokens drive |
|---|---|---|
| statur-motion-design | `motion_render.py --tokens`, layer `tokens` | every template: grounds, text, accent, fonts, radius |
| statur-video-editor-pro | `build_layers.py --tokens`, spec `tokens` | the layers it writes for statur-motion-design, speaker card border and dot |
| statur-clipping, statur-clip-edit | `clip_render.py --tokens`, `render_all.py --tokens`, spec `tokens` | caption, hook, label and watermark fonts; active word, outline, hook box, label box, layout background, border |
| statur-clip-review | `build_review.py ... --tokens` | colors and fonts of the review page (light theme) |
| statur-motion-3d (engine v2) | `setup_project2.sh <workspace> [tokens.json]`, scenario `brand` | overlay colors, the three font slots, tag, site and end line |

`brand_tokens.py` is the loader. The same file sits in the `scripts/` folder of each Python skill above, so a skill still installs alone. Change it in one place, then copy it to the others. `python3 brand_tokens.py FILE` prints the resolved tokens.

## Avoid the template look

A brand file is not enough. Viewers recognize the default output of AI design and editing tools at a glance, whatever the colors. Each video skill carries the same check list ("Avoid the template look"): no near-black ground with one neon accent, no word-by-word caption pack with a colored keyword, no zoom on every sentence, no whoosh on every cut, no fake terminal or desktop window, no counting hero number, no single spring on every element, no background grid or particles, no glow, glass card or gradient text, no emoji in captions. Put the items your brand refuses in `banned_markers`, in your own words.
