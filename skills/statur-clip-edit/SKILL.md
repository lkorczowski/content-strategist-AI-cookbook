---
name: statur-clip-edit
description: Render a planned clip from one or several long recordings with ffmpeg and no editing software. Cut list from word timestamps, silence trimming, cold open, alternating punch-in on jump cuts, a 9:16 crop or a composed layout (screen share on top, camera bubble in a circle, call thumbnail in a rounded box, blurred background), word-by-word burned captions with the active word highlighted, opening hook box, chapter labels, a small moving watermark, loudness leveled across sources and normalized in two passes, an H.264 master at any length and resolution up to 4K, a light review copy, then a quality check that transcribes the clip again. Use when a clip spec exists (from statur-clip-plan) and the user wants the edited file, a batch of clips, a mix of several recordings, or a simple repeatable edit style for lives, webinars, calls, screen recordings and long videos.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "2.4.0"
  playbook: https://statur.co/clipping/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Clip edit

Part of the clipping playbook (https://statur.co/clipping/). Scripts live in the statur-clipping skill (`../statur-clipping/scripts/`). Spec format: `../statur-clipping/references/spec.md`. Traps and fixes: `../statur-clipping/references/pitfalls.md`.

## Requirements

- ffmpeg 4.4 or newer with libx264 and libass (`ffmpeg -filters | grep -E " ass | subtitles "`). Some default Homebrew builds lack libass: install a full build.
- Python 3.10 or newer. The renderer uses the standard library only; the quality check uses the local transcription model (setup.sh of statur-clipping).
- The caption font in a folder passed with `--fonts`. The family comes from the brand tokens (`fonts.text` for captions, labels and watermark, `fonts.display` for the hook); the neutral default is Atkinson Hyperlegible Bold, installed by setup.sh.
- Optional: a brand tokens file (docs/BRAND-TOKENS.md) passed with `--tokens brand.json` (alias `--style`) or `BRAND_TOKENS`. It sets the default colors and fonts of captions, hook, labels, borders and layout backgrounds. A spec's own `tokens`, `captions`, `hook` and `labels` keys win. No brand is written in the scripts.
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

Outputs per clip: `C01_v1_master.mp4`, `captions.ass`, `captions.srt`, `words_out.json` (the words the edit keeps, on the clip's timeline), `cutlist.json`, `render_report.json` (cut map, loudness), `review/C01_v1_review.mp4` (under 19.3 MiB) and a poster. render_all.py also writes `EXPORTS LIVE01/LIVE01_C01_v1_slug.mp4` and its `.srt`, and moves older versions of that clip to `EXPORTS LIVE01/archives/`, so the root holds only the version ready to post (`--keep-old` disables it). It also writes an upload copy `TRAVAIL LIVE01/upload/LIVE01-C01-v1.mp4` (H.264 4.5 Mbps, about 40 to 70 MB for 1 to 2 minutes): post that file, never the master, which is about 30 Mbps and too heavy for a browser upload. Its name is the video id that distribution tracking uses (`--no-upload-copy` disables it). On a machine that stops long commands, keep `--budget` and re-run until it prints DONE or ALL_DONE.

## Edit style "simple" (default)

- Plays the spec's passages in the given order. Removes pauses longer than 0.30 s between words (padding 0.06 s before, 0.12 s after, never reaching into a removed word) and every `cut` range, exactly: nothing inside a cut range is kept, whatever the word timestamps say.
- With `--audio audio16k.flac`, each cut-in moves back to the real speech onset found on the waveform: speech recognition often places a word's start 50 to 150 ms late.
- Audio pieces are counted in samples to match the video frames exactly, so a clip of 40 pieces keeps lip sync on replays with jittery audio timestamps.
- Every other piece gets a 1.10 punch-in toward the face point, so jump cuts read as intended. 12 ms audio fades on every cut.
- Captions: 3 words or 18 characters per line, active word in the tokens' highlighter color, white text, ink outline, at 70 to 75% of the height, built only from the words kept in the edit.
- Hook box: the first 3 seconds, top of the frame, one sentence on two lines at most.
- Chapter labels from the spec's `screen` fields.
- Watermark: the small moving text `statur.co/clipping`, a new spot every 3.5 to 6.5 seconds, seeded per clip. `--watermark "yourbrand.com"` changes it, `--watermark none` removes it.
- Audio: high-pass 70 Hz, light compression, two-pass loudness normalization to -14 LUFS with a -1.5 dB true peak.
- Master: H.264 CRF 17 at the spec's size and frame rate, any length, 4K when the source allows it. Render where the footage is: a master never travels through a chat tool.

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

In a clip spec: set `captions.active` to the caption color and raise `max_words` and `max_chars` (for example 6 and 32) for quiet sentence captions; `"zoom": {"enabled": false}` when the cuts are few; `"captions": {"enabled": false}` for a long-form YouTube master; no emoji in `hook.text` or `fix`.

## Layouts for screen shares, camera bubbles and calls

A source or a segment can take a composed layout instead of the 9:16 crop (fields: `../statur-clipping/references/spec.md`). Three that worked on real recordings:
- `face`: the camera bubble of a screen recording (Loom) enlarged in a circle over a blurred copy of the screen, captions at 0.75. For talking.
- `react`: the video on screen (the one being analyzed) in the top half, captions in the middle, the bubble below. For moments where the screen matters.
- `meet`: the speaker's call thumbnail enlarged in a rounded box over its own blurred copy, captions at 0.70. The only clean option when the speaker recorded their own call window; it stays soft.

Measure each rectangle on a frame of the recording, render five seconds with `--plan-only` off, look at three frames, then render the clip. Alternate two layouts of the same source (face, then react) to cover a jump cut instead of the punch-in.

## Edit style "podcast split": two cameras and motion design

For a recorded video call (two people, one screen recording) and, when possible, a second camera on the speaker (a phone on a stand). Validated on a 28-minute call: the reviewer approved the result after the four steps below.

1. Sync the second camera on the audio, never on the file clock. Extract both audio tracks at 16 kHz, cross-correlate the energy envelopes to get the offset, then refine with short windows at about ten points across the call: a phone and a screen recorder drift by a few tens of milliseconds over half an hour, so fit a straight line (offset plus drift) and use it per clip.
2. Build the picture before the render, one excerpt per clip (from 6 s before the first passage to 2 s after the last), at 1080x1920 with ffmpeg: a 540 px band on top for the text box, the other person cropped from the call tile in the middle, the second camera at the bottom, both 1080x690, call audio as the only track. Then render the clip from that excerpt with the spec and words shifted to its timeline, with zoom off. Work from the big camera file where it is: copying several gigabytes inside a sandbox that stops long commands leaves a truncated file.
3. Keep every text inside the safe zone of the platforms: top 270 px, bottom 670 px, sides 120 px, and the button column on the right (x above 780) from y 840 down (measured on the TikTok template and the Reels specification). Text box at y 0.15 in lines of 22 characters or fewer, size 52, kept on screen for the whole clip; captions at y 0.625, x 0.42, size 66, 14 characters per line. Draw these zones in red on six frames of every master and look before review.
4. Abstract ideas (a model, a metaphor, a distribution) do not land on a talking head. Replace the listener's panel with motion design while the speaker explains, timed to the words: an HTML page in the brand's colors and fonts with one function `setT(t)` that sets every element for time t (entrances at the word timestamps of the transcript), captured frame by frame with Playwright at 30 fps, encoded to a small `.mkv`, and laid over the panel with `-itsoffset` when the excerpt is built. Reuse the diagrams the brand already publishes so the clip and the site tell the same story. Keep every element inside the panel's safe box (x 120 to 770 under y 840) and give the listener's face back for the reaction at the end.

Packaging rules that came out of the same review: open on the strongest line or the tension (never a hesitation or a chronological setup), move the backstory after it as the explanation, cut stumbles in the middle, and split a caption fix around a cut so its words stay on screen. The on-screen text box and the spoken opening never say the same thing.

Next styles, not in this version: B-roll from a stock library, automatic speaker detection in calls.


## Quality check (always, before review)

```
python3 qa_clip.py "TRAVAIL LIVE01/C01_v1/C01_v1_master.mp4" "TRAVAIL LIVE01/C01_v1/words_out.json" --report qa.json
```

It transcribes the clip again and aligns it with the words the edit meant to keep, then reports loudness, true peak, duration, size and frame rate.
- Expect above 95% of the planned words heard back. Spelling variants of the model are not defects.
- A word heard at a cut that the spec removed: the cut is too loose (or a hidden word, which is expected). A planned word missing at a cut: the cut is too tight.
- A caption that shows words the speaker did not say, or misses words they said: fix the spec. Map a clip time back to the source with `cutlist.json`, read the source words, and when unsure transcribe a 2 to 3 second window alone.
- Look at the first frame after every cut (grey frames, framing, zoom) and at ten moments with captions, hook, labels and watermark burned in.

Captions translated into another language (fixes that replace each phrase): the words_out.json of the render holds the translation, so compare the audio with the source-language words instead: dry-run the same spec with an empty `fix` list (`--plan-only`) and pass that words_out.json to qa_clip.py.

Write what the check found in the spec's `check` list, so the reviewer knows where to look.

## Rules

- Drafts only: the agent never posts or schedules the clip, and never deletes the user's files.
- No passwords, no promised views or results, no invented numbers in hooks or captions.
- Captions say what the speaker said: correct spelling, names and numbers, never rewrite.
- Respect each platform's terms of use and the rights of anyone on screen: guests' consent, no third-party music or footage without rights.
