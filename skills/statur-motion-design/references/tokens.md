# Brand tokens

The templates read colors and fonts from one object. Fill it from the company context file (kb/01_BRAND.md, visual system), keep it in the private repo, pass it in the layer or the pro spec as `tokens`.

```json
{
  "ink": "#0E0E0C",
  "paper": "#F2EFE8",
  "accent": "#E8501C",
  "muted": "#8A8780",
  "line": "rgba(242,239,232,.18)",
  "font_display": "Archivo",
  "weight_display": 900,
  "font_body": "Archivo",
  "font_mono": "JetBrains Mono",
  "font_serif": "Cormorant",
  "radius": 0
}
```

| Token | Use |
|---|---|
| ink | panels, card backgrounds, text on light boxes |
| paper | text on panels, hook box, frames of captures |
| accent | active caption word, emphasis boxes, highlights, chips, the one dot; keep it under 10% of the frame |
| muted, line | secondary text, rules, grids |
| font_display, weight_display | hooks, titles, captions |
| font_mono | labels, data, source lines |
| font_serif | rare quotes |
| radius | corner radius of boxes (0 for a brutalist system) |

Fonts load from npm packages (@fontsource/...) found by motion_render.py (`--fonts-dir`); add a family to FONT_FILES in motion_render.py when the brand uses another one. Use fonts whose license allows video (SIL Open Font License or a license the company holds).

Translate the brand's bans into template choices: no shadows (templates have none), no gradients (flat panels; the grid is drawn with hard lines), no stock photos (use the company's own images), no phone mockups (show captures in a plain frame).
