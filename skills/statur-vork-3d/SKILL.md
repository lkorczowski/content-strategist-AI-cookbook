---
name: statur-vork-3d
description: Make short 3D explainer videos and 3D plates for edits from presets written as code, with vork (the headless 3D and VFX engine for agents, github.com/voyager-so/vork) on a GPU machine, or with the statur-motion-3d CPU engine anywhere. Ships the "voice to world" preset - one speaker in a sea of people, a voice that reaches no one, then one listener, a network that compounds over a real-geography dot globe, one opportunity that travels back, and an Earth that keeps turning after the speaker is gone - mapped on the six types of the personal brand scale. Use when someone wants a 3D illustration video for a page, a 3D insert for a pro edit (statur-video-editor-pro motion3d inserts), or wants to try vork for a short video.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "0.1.1"
  playbook: https://statur.co/ai-video-editor/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# vork 3D shorts

Part of the AI video editor playbook (https://statur.co/ai-video-editor/). One preset, two renderers, one timeline: the story lives in the preset (data, camera curve, switch-on times), and each renderer expresses the same story. Sibling skills: statur-motion-3d (the CPU engine this skill reuses), statur-motion-design (2D cards), statur-video-editor-pro (inserts the plates in an edit).

## What vork is, in one paragraph

vork (Voyager rendering kernel, Nullframe Inc.) is a headless 3D and VFX engine written in Rust and Slang. An agent writes a scene as JSON (or with the Python or TypeScript SDK), renders it on the GPU, looks at the image and revises the scene. It has no editor to drive. Scene programs in Slang can change materials, cameras, light paths, simulation and compositing. It was announced on X on 2026-11-06 (https://x.com/ravisparikh/status/2118744950825275680) with a million-bird simulation. Source-available, free during the research preview, including commercial work; it is not open source (read its LICENSE before client work). Rendering needs Apple Silicon with Metal and macOS 26, or an NVIDIA GPU with Vulkan ray queries. Scene authoring and `vork help` need no GPU. Notes and a fact check of the launch claims: references/vork-notes.md.

## Pick the engine

| Machine | Engine | What you get |
|---|---|---|
| Apple Silicon Mac on macOS 26, or NVIDIA RTX Linux or Windows, with vork installed | `vork` | The 3D picture rendered by vork (ray-traced light, denoised). Plate only for now: overlay and sound come from the cpu pass. |
| Anything else (cloud sandbox, Linux VM, older Mac) | `cpu` | statur-motion-3d engine v2: Three.js in headless Chromium with SwiftShader, bloom, brand overlay, synthesized sound. Measured 2026-11-08 on a 2 vCPU cloud machine: 2.3 to 2.8 frames per second at 720x1280, 41 s of video in 7 min. |

`--engine auto` runs `vork setup` and picks vork when it reports a usable GPU. A Docker image does not give a GPU: Docker Desktop on a Mac does not expose Metal to Linux containers, and a Linux VM on a Mac has no Metal either.

## Default path

```
# once: Node 18+, playwright with Chromium, ffmpeg, Python 3 with numpy, scipy and global-land-mask (MIT)
python3 scripts/make_short.py --preset voice-to-world --out short.mp4 --engine cpu --work WORK
# a plate for an edit: no overlay, no sound, a range of the timeline
python3 scripts/make_short.py --preset voice-to-world --plate --from 18.8 --to 22.6 --out insert.mp4
# your own texts and your own city on the globe
python3 scripts/make_short.py --preset voice-to-world --scenario my_scenario.json --city 37.77,-122.42 --out sf.mp4
```

Before a full render, look at stills: `SUB=voice-to-world node ../statur-motion-3d/scripts/render2.js WORK stills 1.5,9,12.5,18,20.5,26,29,34 WORK/stills`, then a contact sheet (`ffmpeg -pattern_type glob -i 'WORK/stills/t*.jpg' -vf scale=300:-1,tile=8x1 sheet.jpg`). make_short.py renders in parts of 14 s that it does not render again, because sandboxes stop long commands.

On a vork machine:

```
python3 scripts/vork_scene.py --data WORK/voice-to-world/data.json --scenario WORK/voice-to-world/scenario.json \
  --out scene.json --schema <vork repo>/packages/ts/scene.schema.json      # prints schema: PASS
vork render scene.json --profile std/previs --at 9 --out check.png            # stills first, look at them
vork render scene.json --profile std/draft --out plate.mp4                    # then the movie
```

## The voice-to-world preset

Files: presets/voice-to-world/ (scenario.json, shots.js for the CPU engine, gen_data.py for the data both engines read). 41 s, 720x1280, 30 fps.

| Time (s) | Picture | Caption | Scale |
|---|---|---|---|
| 0 to 8 | The host speaks in a crowd on their phones; voice rings fade before anyone turns | You speak into a sea of people. Your ideas stay in the room. | Type 0 |
| 8 to 13.2 | One listener turns and lights up, a line joins them, then two, then a cascade | Then one person hears you. Then another. | Type 1 |
| 13.2 to 18.8 | Zoom out: the people become dots, a network spreads over the curve of the Earth | A content strategist makes it compound. Thousands listen. | Type 2 |
| 18.8 to 24.8 | One node glows soft teal and its light travels back along the network to the speaker | One of them comes back to you. A client. A deal. An investor. | Type 2 |
| 24.8 to 30.8 | Whole globe with real coastlines; the land lights up outwards from the speaker's city; arcs cross oceans | Your ideas cross every border. The whole world carries them. | Types 3 and 4 |
| 30.8 to 37 | The Earth spins faster and faster; the speaker's light goes out, the network stays | Years pass. Your ideas outlive you. | Type 5 |
| 37 to 41 | End card | Which type are you today? | |

The types follow the Korczowski scale of https://statur.co/personal-brand-levels/. The HUD shows the type, never a made-up audience number. The speaker's city sets the globe (default: Paris; pass `--city LAT,LON` for your own); the coastlines come from global-land-mask (MIT), sampled on a Fibonacci sphere.

How the CPU engine draws it: the globe radius is 3000 units and the crowd stands on its top, so a single continuous camera curve goes from a close shot of the host to the whole planet; the camera near and far planes follow the distance. Network nodes, land dots and lines are custom shaders that switch on at their own time (attribute aT), so frame N is always the same picture. The static crowd is baked into one vertex-colored mesh (520 people, one draw call); the listeners are live characters.

How the vork scene expresses it (vork_scene.py): switch-on by scaling a node from 0 to 1 (a zero world scale hides geometry), glow as OpenPBR emission with material tracks, crowds, nodes and land dots as instanced meshes batched by switch-on time, the camera aiming at an "aim" node with keys sampled from the same curve, the spin as a rotation track on the world node around the real Earth axis. The scene validates against vork's editor schema (std geometry builders are swapped for a name before validation, as vork expands them in its loader). It has not been rendered yet: the first render on a vork machine goes in references/pitfalls.md.

## Write a new preset

1. Story first: 6 to 12 beats, one caption each, at growing scale, with a twist and an end card (statur-motion-3d references/format.md). Every number on screen needs a source.
2. Data: a script that writes data.json with everything both engines need (positions, times, chains). Seeded random numbers only.
3. CPU engine: shots.js in the statur-motion-3d v2 format; fetch data with `new URL('data.json', import.meta.url)`.
4. vork: a builder like vork_scene.py that reads the same data and the same camera keys. Validate against the schema, then render stills on the GPU machine.
5. Stills, contact sheet, then the full render. Fix what is not readable at phone size.

## Quality gate (refuse to deliver when one fails)

- Every caption readable on its still, the hook frame readable, the HUD never covering the subject.
- Nothing blown out: the subject's face readable in close shots (no spotlight or halo burn), no hard rings on the globe edge.
- Each beat shows its idea without the caption: watch the contact sheet with the captions hidden (`--plate`).
- Duration equals scenario.duration; the file plays with sound; loudness near -16 LUFS for a page, -14 for social.
- Every number on screen has its source; illustrative scales use words (Type 2, millions) and say so.
- Label the post as AI-generated where the platform asks for it.

## Update this skill

New vork release or first GPU render: update references/vork-notes.md and the measured numbers above with the date, add the lesson to references/pitfalls.md, bump metadata.version, add a CHANGELOG.md line, and update the playbook card.

## Rules

- Drafts only: the agent never posts or shares the video.
- No passwords, no account creation; installing vork is the user's call on the user's machine.
- No promised views or results: the scale and the network are an illustration, not a forecast.
- No invented numbers: every figure on screen has a source in the brief, or it is cut.
- Respect licenses and platform terms: vork's preview license, the data licenses (global-land-mask MIT), and the AI-generated label.
