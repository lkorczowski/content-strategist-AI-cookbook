---
name: statur-motion-design
description: Motion design for short vertical videos with an AI agent and no After Effects: deterministic HTML and CSS templates (hook box, word captions with emphasis, chips, name card, list card, page capture card with zoom and highlight, prompt box, curve chart, loop diagram, recording cut into clips, big text behind the speaker, poster wall and grid backgrounds, end card, moving watermark) rendered frame by frame with headless Chromium into transparent layers, in the brand's colors and fonts. Use when an edit needs graphics, kinetic text, animated captions, cards or an end card, or when someone wants to add or change a motion template.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.1.0"
  playbook: https://statur.co/ai-video-editor/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Motion design

Part of the AI video editor playbook (https://statur.co/ai-video-editor/). Called by statur-video-editor-pro, usable alone for any motion piece (a demo, an end card, a text animation).

## How it works

A layer is a JSON list of elements, each with a template, a start, an end and props. `scripts/motion_render.py` opens one Chromium page with `engine.js` and every file in `templates/`, then for each frame where an element is active it calls `seek(t)` and screenshots the stage: PNG with alpha for layers that go over or under the speaker, JPEG for opaque backgrounds. Frames with nothing active are skipped; the compositor treats them as transparent.

Every template computes its look from the time it is given (no CSS animation, no transition), so frame 812 always renders the same picture, frames can render in any order and on several workers, and a change to one element re-renders only its frames.

```
python3 scripts/motion_render.py layer.json OUTDIR [--tokens brand.json] [--workers 2] [--frames 30,90,150] [--duration 91.0]
```

Install once: Playwright with Chromium, and the fonts named in the tokens file as npm packages next to the scripts (the neutral defaults shown here):

```
npm i --prefix fonts @fontsource/atkinson-hyperlegible @fontsource/ibm-plex-mono @fontsource/caveat
```

Speed on 2 vCPUs, 1080x1920: 12 to 14 frames per second with alpha, 7 for full backgrounds with many images.

## Brand tokens

No brand is written in this skill. Colors, fonts, limits and bans come from one tokens file kept in the company's private repo (shape: docs/BRAND-TOKENS.md, example: docs/brand-tokens.example.json), built once from the company context file. Pass it with `--tokens brand.json` (alias `--style`), set `BRAND_TOKENS`, or write a `tokens` object in the layer. With none of them the templates render in a neutral look: light paper, dark ink, one quiet accent. How the tokens reach the templates, fonts and the older flat shape: references/tokens.md.

## Avoid the template look

Viewers recognize the default output of AI design and editing tools at a glance, and trust the video less. Check the plan, then every still, against this list. The tokens file may add the brand's own `banned_markers`.

Avoid:
- A near-black ground with one neon or amber accent.
- Word-by-word bold captions with one colored keyword.
- A zoom on every sentence.
- A whoosh or a riser on every cut.
- Fake terminal or desktop windows around text.
- Hero numbers that count up.
- The same spring on every element.
- Background grids and particles.
- Glows, glass cards, gradient text.
- Emoji in captions.

Prefer:
- Sentence-case captions on a quiet band, with one underlined key word at most.
- A title card that reads like paper: flat ground, ink text, no effect.
- The annotated image: freeze the frame, draw a circle and an arrow by hand, add a short note, resume.
- Hard cuts. Motion only where it explains something.
- Real assets: the company's own pages, photos, screens and documents.
- Long-form YouTube videos: no burned subtitles. Upload a caption file.

In this skill that means: use `ink_grid`, the `counter` of `big_text`, `prompt_box` and the accent box of `captions` only when the brand asks for them, never by default. Vary entrances (a cut, a fade, one spring) instead of one helper everywhere. Count accent elements per still against `limits.accent_gestures_per_screen`.

## Templates

Catalog with every prop: references/templates.md. In short:
- Text: hook_box, captions, chips, label_chip, lower_third, big_text (with counter or word swaps, meant for the layer behind the speaker), footnote, end_card, watermark.
- Cards: panel (full-screen backdrop), card_list, page_card (a capture in a frame that pans, zooms and draws highlight boxes), prompt_box.
- Diagrams: chart_curve, loop_diagram, timeline_cut.
- Backgrounds: poster_wall, ink_grid.

## Design rules that keep it native

- One idea per card, readable in the time of its sentence. Look at a still of every card before the full render.
- Text in the safe area of TikTok and Reels on a 1080x1920 frame: y 269 to 1248, x 120 to 960 above y 840 and x 120 to 780 below it; keep the caption zone free on cards. Full-screen panels may cover the zones, their text may not.
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
