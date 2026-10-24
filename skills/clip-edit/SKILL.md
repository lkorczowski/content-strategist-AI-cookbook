---
name: clip-edit
description: Render a planned clip from one or several long recordings with ffmpeg and no editing software. Cut list from word timestamps, silence trimming, cold open, alternating punch-in on jump cuts, a 9:16 crop or a composed layout (screen share on top, camera bubble in a circle, call thumbnail in a rounded box, blurred background), word-by-word burned captions with the active word highlighted, opening hook box, chapter labels, a small moving watermark, loudness leveled across sources and normalized in two passes, an H.264 master at any length and resolution up to 4K, a light review copy, then a quality check that transcribes the clip again. Use when a clip spec exists (from clip-plan) and the user wants the edited file, a batch of clips, a mix of several recordings, or a simple repeatable edit style for lives, webinars, calls, screen recordings and long videos.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.1.0"
  playbook: https://statur.co/clipping/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Clip edit

Part of the clipping playbook (https://statur.co/clipping/). Scripts live in the statur-clipping skill (`../statur-clipping/scripts/`). Spec format: `../statur-clipping/references/spec.md`. Traps and fixes: `../statur-clipping/references/pitfalls.md`.

## Requirements

- ffmpeg 4.4 or newer with libx264 and libass (`ffmpeg -filters | grep -E " ass | subtitles "`). Some default Homebrew builds lack libass: install a full build.
- Python 3.10 or newer. The renderer uses the standard library only; the quality check uses the local transcription model (setup.sh of statur-clipping).
- The caption font in a folder passed with `--fonts` (Archivo Black by default).
- The sync map of the source (`sync.json` from sync_check.py) when the sync check reported an offset.

## Run

Always a dry run first, then read the captions of every passage you touched:

```
python3 clip_render.py --source RUSH.mp4 --words words.json --spec C01.json --out "TRAVAIL LIVE01/C01_v1" --sync sync.json --plan-only
```

One clip:

```
python3 clip_render.py --source RUSH.mp4 --words words.json --spec C01.json --out "TRAVAIL LIVE01/C01_v1" \
  --sync sync.json --audio audio16k.flac --fonts FONTS_DIR --review --tmp /tmp/clips [--budget 150] [--watermark "yourbrand.com"]
```

A batch, with masters copied to EXPORTS and clips skipped when their spec has not changed:

```
python3 render_all.py --project "$HOME/Clips/2026-10-24 LIVE01 Title" --code LIVE01 --source RUSH.mp4 --words words.json \
  --sync sync.json --audio audio16k.flac --fonts FONTS_DIR --tmp /tmp/clips [--budget 150] specs/C01.json specs/C05.json ...
```

A mix of several recordings, or a project with one folder for several recordings: the spec lists its `sources` (paths relative to the project folder), and no `--source` or `--words` is needed:

```
python3 clip_render.py --spec "TRAVAIL WEB01/specs/C02_v1.json" --root "$HOME/Clips/2026-10-25 WEB01 Title" --out "TRAVAIL WEB01/C02_v1" --fonts FONTS_DIR --review --tmp /tmp/clips
python3 render_all.py --project "$HOME/Clips/2026-10-25 WEB01 Title" --code WEB01 --fonts FONTS_DIR --tmp /tmp/clips --budget 150 specs/C0*_v1.json
```

Outputs per clip: `C01_v1_master.mp4`, `captions.ass`, `captions.srt`, `words_out.json` (the words the edit keeps, on the clip's timeline), `cutlist.json`, `render_report.json` (cut map, loudness), `review/C01_v1_review.mp4` (under 19.3 MiB) and a poster. render_all.py also writes `EXPORTS LIVE01/LIVE01_C01_v1_slug.mp4` and its `.srt`, and moves older versions of that clip to `EXPORTS LIVE01/archives/`, so the root holds only the version ready to post (`--keep-old` disables it). On a machine that stops long commands, keep `--budget` and re-run until it prints DONE or ALL_DONE.

## Edit style "simple" (default)

- Plays the spec's passages in the given order. Removes pauses longer than 0.30 s between words (padding 0.06 s before, 0.12 s after, never reaching into a removed word) and every `cut` range, exactly: nothing inside a cut range is kept, whatever the word timestamps say.
- With `--audio audio16k.flac`, each cut-in moves back to the real speech onset found on the waveform: speech recognition often places a word's start 50 to 150 ms late.
- Audio pieces are counted in samples to match the video frames exactly, so a clip of 40 pieces keeps lip sync on replays with jittery audio timestamps.
- Every other piece gets a 1.10 punch-in toward the face point, so jump cuts read as intended. 12 ms audio fades on every cut.
- Captions: 3 words or 18 characters per line, active word in the accent color, white text, dark outline, at 70 to 75% of the height, built only from the words kept in the edit.
- Hook box: the first 3 seconds, top of the frame, one sentence on two lines at most.
- Chapter labels from the spec's `screen` fields.
- Watermark: the small moving text `statur.co/clipping`, a new spot every 3.5 to 6.5 seconds, seeded per clip. `--watermark "yourbrand.com"` changes it, `--watermark none` removes it.
- Audio: high-pass 70 Hz, light compression, two-pass loudness normalization to -14 LUFS with a -1.5 dB true peak.
- Master: H.264 CRF 17 at the spec's size and frame rate, any length, 4K when the source allows it. Render where the footage is: a master never travels through a chat tool.

## Layouts for screen shares, camera bubbles and calls

A source or a segment can take a composed layout instead of the 9:16 crop (fields: `../statur-clipping/references/spec.md`). Three that worked on real recordings:
- `face`: the camera bubble of a screen recording (Loom) enlarged in a circle over a blurred copy of the screen, captions at 0.75. For talking.
- `react`: the video on screen (the one being analyzed) in the top half, captions in the middle, the bubble below. For moments where the screen matters.
- `meet`: the speaker's call thumbnail enlarged in a rounded box over its own blurred copy, captions at 0.70. The only clean option when the speaker recorded their own call window; it stays soft.

Measure each rectangle on a frame of the recording, render five seconds with `--plan-only` off, look at three frames, then render the clip. Alternate two layouts of the same source (face, then react) to cover a jump cut instead of the punch-in.

Next styles, not in this version: B-roll from a stock library, motion design with a programmatic tool (check the license threshold of each tool for companies), automatic speaker detection in calls.

## Quality check (always, before review)

```
python3 qa_clip.py "TRAVAIL LIVE01/C01_v1/C01_v1_master.mp4" "TRAVAIL LIVE01/C01_v1/words_out.json" --report qa.json
```

It transcribes the clip again and aligns it with the words the edit meant to keep, then reports loudness, true peak, duration, size and frame rate.
- Expect above 95% of the planned words heard back. Spelling variants of the model are not defects.
- A word heard at a cut that the spec removed: the cut is too loose (or a hidden word, which is expected). A planned word missing at a cut: the cut is too tight.
- A caption that shows words the speaker did not say, or misses words they said: fix the spec. Map a clip time back to the source with `cutlist.json`, read the source words, and when unsure transcribe a 2 to 3 second window alone.
- Look at the first frame after every cut (grey frames, framing, zoom) and at ten moments with captions, hook, labels and watermark burned in.

Write what the check found in the spec's `check` list, so the reviewer knows where to look.

## Rules

- Drafts only: the agent never posts or schedules the clip, and never deletes the user's files.
- No passwords, no promised views or results, no invented numbers in hooks or captions.
- Captions say what the speaker said: correct spelling, names and numbers, never rewrite.
- Respect each platform's terms of use and the rights of anyone on screen: guests' consent, no third-party music or footage without rights.
