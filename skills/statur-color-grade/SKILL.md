---
name: statur-color-grade
description: Picture finishing for short videos with an AI agent: convert phone HDR (iPhone HLG, BT.2020) to a clean SDR BT.709 plate with a known tone map, write the brand's grade as a small readable LUT, check skin against the skin-tone line and the levels with numbers and a scope sheet, sharpen lightly. Use before any overlay or edit on phone footage, when a video looks washed out, burnt or grey after upload, or when someone wants a consistent look across videos.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/ai-video-editor/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Color grade

Part of the AI video editor playbook (https://statur.co/ai-video-editor/). Called by statur-video-editor-pro; useful alone before statur-clip-edit when the recording comes from a phone in HDR.

## 1. Plate: one SDR file every later step reads

```
python3 scripts/plate.py RAW.mp4 plate.mov [--tonemap mobius] [--npl 203]
```

It reads the transfer of the source. HLG or PQ (HDR) is tone mapped to SDR BT.709 (zscale + tonemap, reference white 203 nits after ITU-R BT.2408), SDR passes through. Captions, cards and captures are designed in SDR: an HDR plate under them makes white text look grey on some phones and burnt on others. The audio is kept in PCM. Measured: 22 frames per second at 1080x1920 on 2 vCPUs.

## 2. Measure before grading

```
python3 scripts/scopes.py plate.mov --times 2,30,60 --matte matte.mkv --sheet scopes.jpg
```

Numbers per frame: luminance at 2%, 50% and 98%, share of clipped pixels, and the skin hue of the speaker against the skin-tone line (about 123 degrees on a vectorscope; healthy skin of any complexion sits within about 10 degrees of it). With a person matte the skin is measured on the speaker only. Look at scopes.jpg.

## 3. Grade as a LUT

```
python3 scripts/make_lut.py grade.cube --preset natural          # or editorial, or your own settings
python3 scripts/make_lut.py grade.cube --preset editorial --exposure -0.1
```

Settings are readable numbers in the colorists' order: exposure and white balance (temp, tint), contrast around middle grey, black and white points, saturation with skin protection, split toning of shadows and highlights, highlight roll-off. The LUT carries its settings in a comment line, so a look is a small text file kept in the brand repo. Presets: natural (safe default, skin kept true), editorial (denser, warm highlights, cool shadows). Apply with ffmpeg `lut3d`, then a light `cas` sharpening (0.3 to 0.4).

Rules of thumb: fix white balance only when skin is off the line by more than about 10 degrees; keep skin luminance near 0.6 to 0.7; do not crush the clothes to black; check the measure again after the grade.

## Rules

- Drafts only: the agent never posts or shares the result.
- Keep the speaker real: no skin smoothing, no face reshaping, no relighting that changes who they are.
- Generate LUTs instead of downloading packs whose license is unclear.
- Never overwrite the original recording: the plate is a new file.
