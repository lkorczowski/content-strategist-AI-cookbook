---
name: statur-motion-3d
description: Make full 3D motion-design short videos in code, with no AI video model and no 3D software, such as the viral "What if X disappeared for 5 seconds?" format - a procedural low-poly world (park, skyline, crowd, hands, Earth, Moon) drawn in day, wireframe, glow and point-cloud modes, a ticking HUD clock, serif captions, a loop end card and a synthesized sound bed, rendered frame by frame on a CPU with Three.js, headless Chromium and ffmpeg. Version 2 adds bloom and shadows, animated characters and a host mascot, a brand overlay, a 2D editorial stage and a synthesized music bed. Use when someone wants a faceless 3D explainer or what-if video, a 3D background for a talking-head video, or to reproduce or adapt a 3D short format.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "0.2.0"
  playbook: https://statur.co/ai-video-editor/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Motion 3D

Part of the AI video editor playbook (https://statur.co/ai-video-editor/). Sibling of statur-motion-design (2D templates and layers): this skill draws whole 3D scenes. Both render a deterministic web page frame by frame, so they share the same habits: stills first, then the full render.

## When it fits

- Faceless what-if and "how it works" explainers: one premise, a chain of consequences at growing scale, real numbers.
- A 3D plate behind or between talking-head shots (founder explains, the world reacts).
- A test of a viral format: rebuild it with the same structure to learn what carries it, then write your own script.

## Intake (ask once, then use the defaults)

1. Premise and script: the question (title), the place the viewer stands in, 6 to 12 consequences, the twist, the end-card fact. Default: none, the script is required. Every number needs a source line in the brief.
2. Visual arc: which kit modes in which order. Default: the park-to-space arc of examples/kit-tour (day, event, wireframe, glow, white-out, Earth, Moon, point cloud, loop card).
3. Voice: none (default, works muted and in any language), or a voice track the user supplies; then time captions to it.
4. Format: 720x1280 at 30 fps (default, fastest on a CPU) or 1080x1920.
5. Brand: default serif look (EB Garamond, Inter, JetBrains Mono). A private layer may swap the fonts and colors in index.html.

## Default path

```
bash scripts/setup_project.sh <project>              # engine + example + Three.js + fonts
# edit <project>/scenario.json (texts, clock, captions, sound) and <project>/shots.js (cameras, modes, effects)
node scripts/render.js <project> stills 0.3,7,10,18,22,26,34,38,46,50,54,60,65,70,77 <project>/stills
# look at every still: one per caption, the hook frame, every mode switch
node scripts/render.js <project> video <project>/silent.mp4
python3 scripts/sound.py <project>/scenario.json <project>/sound.wav
ffmpeg -i <project>/silent.mp4 -i <project>/sound.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart <project>/final.mp4
```

Install once: Node 18+, `npm i playwright` with its Chromium, ffmpeg, Python 3 with numpy and scipy. No GPU needed: Chromium renders WebGL with SwiftShader.

Measured on a 2 vCPU cloud machine (2026-10-30): 15 stills in under 10 s; 80 s at 720x1280 30 fps (2,405 frames) in 8 to 10 min (3.8 to 5.8 frames per second); sound in 4 s.

## How it works

- `engine/kit.js` builds the world once, from seeded random numbers: skyline boxes with window textures, low-poly trees, block people (sitting, standing, dress), picnic blankets, POV hands, stars, dust, sand sparks, falling streaks, glow sprites, Earth (cloud texture), Moon, and a point-cloud copy of every surface. Each object has four looks: `day`, `wire` (black fill, white edges, window grids, speckled ground, stars), `glow` (wire plus light), and `points`. Modes switch per frame with `K.mode()`.
- `shots.js` (one per project) lists the shots: `{from, to, run(t, k)}`. A shot picks a mode, moves the camera with `K.path()`, and calls kit effects (`K.hands`, `K.dust`, `K.sand`, `K.streaks`, `K.outshine`, `K.pointCloud`, `K.space`). It may draw 2D light on the overlay canvas `O.fx`, or fade the frame to white with `O.white()`.
- `scenario.json` holds every text and time: title (keyword in `<hl>`), HUD segments (label, clock, sub-line, including an interpolated number), captions, end card, sound cues. Schema: references/scenario-schema.md.
- `core.js` exposes `window.renderAt(t)`. Nothing depends on the wall clock, so frame 812 always renders the same picture, stills match the video, and any range can be re-rendered.
- `scripts/sound.py` synthesizes the sound bed from the cues: ticks on the countdown, a boom at the event, a drone, crackles and swells, impacts, a space pad, silence before the end card. No samples, so there is no license to clear.

## Engine v2 (production value)

The first engine (engine/) reproduces a format. Engine v2 (engine2/) is for original videos that must look produced. Same principle (deterministic `renderAt(t)`, stills first), more craft:

- Stage: `scenario.engine` is `3d` (Three.js with ACES tone mapping, UnrealBloom, optional soft shadows) or `2d` (a canvas the shots draw on). Workspace layout: one folder per video (`<workspace>/<video>/scenario.json` and `shots.js`), engine files at the workspace root. Setup: `bash scripts/setup_project2.sh <workspace>`.
- Kit (`engine2/lib3d.js`): articulated people with poses (walk, march with a sign, cheer, phone, type, shrug, look up, point), a host mascot (`host()`, `hostPose()`), robots, city blocks with lit windows, streets, cars, lamps, facade screens, signs with text, aircraft, star fields, camera paths with handheld shake.
- Overlay (`engine2/core2.js` + `index.html`): brand tag and site, title with a colored keyword (`*word*`), HUD readout (label, value, progress bar), punchy captions (scale-in, keyword in the signal color), a source line under any caption that carries a number, end card with a question, film grain and vignette. Light backgrounds: `"ui": "light"`; move the HUD with `"hud_top"`.
- Sound (`scripts/sound2.py`): music bed by sections (pulse, drop, build, drive, wide, hold, end) in a mood (tense minor, bright or playful major), plus SFX on cuts (whoosh, blackout, thud, hit, pop, ding, crowd). Still no samples and no license to clear.
- Render: `SUB=<video> node scripts/render2.js <workspace> stills 1,4,9 <out>` then `SUB=<video> node scripts/render2.js <workspace> video <out.mp4>`; mux with ffmpeg. Measured 2026-10-31 on 2 vCPU at 720x1280 30 fps: 3D with bloom about 2.2 frames per second (52 s in 10 to 11 min), 2D about 6 frames per second (52 s in 4 min).

## Production value rules (learned from a 6/10 review)

- No dead air: a caption on screen at all times after the title; gaps under 0.5 s; 2.5 to 3.5 s per caption; 45 to 60 s total.
- Something moves in every frame: the camera (path plus light shake) and the characters (walk, react, cheer). A static crowd reads as a bug.
- Cut every 1 or 2 captions to a new place or scale; each cut gets a whoosh and the HUD moves.
- One signature across every video: the same tag, HUD, caption style and end card, and, when the brand has one, the host mascot in the hook and the last beat.
- Light the characters: at night add a soft fill light that follows the camera; keep bloom under the level that turns domes and skies into white blobs.
- Every number on screen carries its source line; every story beat survives a "really?" in the comments.
- Before the full render, a contact sheet of one still every 2 to 3 s; fix every shot where the subject is not readable at phone size.

## Format recipe (what to keep from viral what-if shorts)

Details, evidence grades and the beat-by-beat reference: references/format.md. In short:
- The question is the title on frame 1, with the keyword in color.
- The viewer is placed in a real place, in the second person.
- One number ticks the whole video (countdown, then a slowed game clock, then a growing measure).
- One consequence per caption, under 10 words, at growing scale: body, place, planet, beyond.
- A twist at the end, then a black beat, then a loop card that repeats the title with one sourced fact.
- Real numbers with a source: comment sections check them.
- Label the post as AI-generated where the platform asks for it.

## Quality gate (refuse to deliver when one fails)

- Every caption readable on its still, including over white frames (the overlay has a dark halo for that).
- No still shows the wrong world (a park inside a space shot, a wall of buildings filling the sky).
- The HUD clock reaches its target value at the right second; the sub-line matches the scale on screen.
- Fonts loaded: render.js stops with "missing fonts" otherwise.
- Every number on screen has its source in the brief.
- The final file plays from start to end with sound; duration equals scenario.duration.

## Extend the kit

Add an object or an effect in `engine/kit.js` as a function on K, built from seeded random numbers, with a look for every mode it appears in. Add a shot in shots.js. Keep geometry merged per material (thousands of objects stay fast on a CPU). Pitfalls met so far: references/pitfalls.md.

## Update this skill

When a render, a platform rule or a tool changes: update the measured numbers above with the date, add the lesson to references/pitfalls.md, bump metadata.version, add a CHANGELOG.md line. Revisit the CPU-only choice when a GPU machine is available (bloom and higher resolution get cheap).

## Rules

- Drafts only: the agent never posts or shares the video.
- No passwords, no account creation.
- No promised views or results: the reference numbers describe other accounts.
- No invented numbers: every figure on screen has a source in the brief, or it is cut.
- Never publish another creator's script: rebuild a format to learn from it, then write your own text. Credit format inspirations with a link.
- Respect platform terms, including the AI-generated content label.
