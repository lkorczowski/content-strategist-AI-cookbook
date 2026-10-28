---
name: statur-motion-design
description: Motion design for short vertical videos with an AI agent and no After Effects: deterministic HTML and CSS templates (hook box, word captions with emphasis, chips, name card, list card, page capture card with zoom and highlight, prompt box, curve chart, loop diagram, recording cut into clips, big text behind the speaker, poster wall and grid backgrounds, end card, moving watermark) rendered frame by frame with headless Chromium into transparent layers, in the brand's colors and fonts. Use when an edit needs graphics, kinetic text, animated captions, cards or an end card, or when someone wants to add or change a motion template.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/ai-video-editor/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Motion design

Part of the AI video editor playbook (https://statur.co/ai-video-editor/). Called by statur-video-editor-pro, usable alone for any motion piece (a demo, an end card, a text animation).

## How it works

A layer is a JSON list of elements, each with a template, a start, an end and props. `scripts/motion_render.py` opens one Chromium page with `engine.js` and every file in `templates/`, then for each frame where an element is active it calls `seek(t)` and screenshots the stage: PNG with alpha for layers that go over or under the speaker, JPEG for opaque backgrounds. Frames with nothing active are skipped; the compositor treats them as transparent.

Every template computes its look from the time it is given (no CSS animation, no transition), so frame 812 always renders the same picture, frames can render in any order and on several workers, and a change to one element re-renders only its frames.

```
python3 scripts/motion_render.py layer.json OUTDIR [--workers 2] [--frames 30,90,150] [--duration 91.0]
```

Install once: Playwright with Chromium, and the fonts as npm packages next to the scripts:

```
npm i --prefix fonts @fontsource/archivo @fontsource/jetbrains-mono @fontsource/cormorant
```

Speed on 2 vCPUs, 1080x1920: 12 to 14 frames per second with alpha, 7 for full backgrounds with many images.

## Brand tokens

Colors, fonts and the brand's bans come from the company context file. Map them once to tokens (references/tokens.md): ink, paper, accent, muted, line, font_display, weight_display, font_body, font_mono, font_serif, radius. A brand that bans shadows and gradients gets flat panels and thin rules: the templates have no shadow by default.

## Templates

Catalog with every prop: references/templates.md. In short:
- Text: hook_box, captions, chips, label_chip, lower_third, big_text (with counter or word swaps, meant for the layer behind the speaker), footnote, end_card, watermark.
- Cards: panel (full-screen backdrop), card_list, page_card (a capture in a frame that pans, zooms and draws highlight boxes), prompt_box.
- Diagrams: chart_curve, loop_diagram, timeline_cut.
- Backgrounds: poster_wall, ink_grid.

## Design rules that keep it native

- One idea per card, readable in the time of its sentence. Look at a still of every card before the full render.
- Text in the safe area: no text in the top 240 px, nothing in the right column (x over 960) below y 840 on a 1080x1920 frame; keep the caption zone free on cards.
- Motion has a reason: an element enters when its word is said, a highlight draws when the claim is made, a number counts while it is spoken.
- Every entrance is a visual event that may carry a sound effect (statur-sound-design); quiet exits.
- Numbers on screen carry their source line (footnote template).

## Add a template

Copy the pattern of an existing one in `templates/`: `STATUR.register('name', {create(e, root, T, c) {... return {update(lt, dur, t) {...}}}})`. Build the DOM in create, set styles from the local time lt in update, use the helpers in `STATUR.util` (prog, spring, env, lerp, rng). Images: call `waitImg(img)` so frames wait for decoding. Then document the props in references/templates.md and bump the version. Another renderer (Lottie, Rive, HyperFrames, a 3D tool) fits as a template that draws into its root at time lt.

## Rules

- Drafts only: the agent never posts or shares the rendered video.
- No passwords; no invented numbers on screen, every figure with its source.
- Fonts and images with a license that allows video (SIL Open Font License fonts, the company's own images); no logos or characters the company does not own.
- Respect each platform's terms: no other platform's logo or handle on a video meant for a different platform.
