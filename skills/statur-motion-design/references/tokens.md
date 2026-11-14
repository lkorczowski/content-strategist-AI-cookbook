# Brand tokens

The templates read colors and fonts from one object. The brand is never written in a template or a script: it comes from a tokens file kept in the company's private repo. Shape, keys and precedence: docs/BRAND-TOKENS.md at the root of the cookbook (example: docs/brand-tokens.example.json).

```
python3 scripts/motion_render.py layer.json OUTDIR --tokens brand.json     # or: export BRAND_TOKENS=brand.json
python3 scripts/brand_tokens.py brand.json                                  # print the resolved tokens
```

A layer may also carry its own `tokens` object; it wins over the file. With no tokens at all the renderer uses a neutral look: light paper, dark ink, one quiet accent, open-license fonts.

## What the templates receive

motion_render.py turns the shared tokens into the flat object the templates read as `T`:

| T key | From | Use |
|---|---|---|
| ink | `colors.paper` on a paper surface, `colors.ink` on an ink surface | the ground: panels, card backgrounds, opaque stages |
| paper | the other one | text on panels, boxes that carry text over footage, frames of captures |
| accent | `colors.accent` | emphasis boxes, chips, the active caption word; count the accent elements per frame against `limits.accent_gestures_per_screen` |
| muted, line | `colors.secondary`, the text color at 18% | secondary text, rules |
| panel, ink_drawing, highlighter, highlighter_pale | the same keys of `colors` | for templates you add: a second ground, hand-drawn marks, marker strokes |
| font_display, weight_display | `fonts.display`, `limits.display_weight` | hooks, titles, captions |
| font_body | `fonts.text` | body text |
| font_mono | `fonts.inscription` | labels, data, source lines |
| font_serif | `fonts.hand` | rare quotes, notes |
| radius | `limits.radius` | corner radius of boxes |

The names `ink` and `paper` in `T` mean "ground" and "text on the ground". They are kept so templates written for the older flat tokens still work. A file in the older flat shape (`ink`, `paper`, `accent`, `muted`, `line`, `font_display`, `weight_display`, `font_body`, `font_mono`, `font_serif`, `radius`) still loads as it is.

## Fonts

Fonts load from npm packages (@fontsource/...). The package name is the family in lowercase with hyphens ("IBM Plex Mono" is @fontsource/ibm-plex-mono); add an exception to FONT_PACKAGES in motion_render.py when a package is named differently. Install them next to the scripts (`npm i --prefix fonts @fontsource/<family>`) or point `--fonts-dir` to an @fontsource folder.

A font named in a tokens file must be installed: the renderer stops when it is missing, because the browser would fall back without a word. The neutral defaults are not checked. Use fonts whose license allows video (SIL Open Font License or a license the company holds).

## Bans

Translate the brand's `banned_markers` into template choices before planning: no shadows (templates have none), no gradients (flat panels), no stock photos (use the company's own images), no phone mockups (show captures in a plain frame). Then run the "Avoid the template look" list of SKILL.md on the stills.
