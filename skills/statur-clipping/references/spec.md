# The clip spec

One JSON file per clip version. clip-plan writes it, clip-edit renders it, clip-review changes it. Times are seconds on the transcript timeline (the times of words.json). Example: templates/clip-spec.example.json.

## Content

| Field | Meaning |
|---|---|
| `id`, `version`, `slug` | `C05`, `2`, `wolf-pack-funnel`. The master is named `<CODE>_<id>_v<version>_<slug>.mp4`. Bump `version` for every change the reviewer will see. |
| `title` | Working title, for the review page. |
| `hook` | `{"text": "...", "dur": 3.2, "size": 90}`. One natural sentence of ten words or fewer, in the speaker's voice, shown in a box at the top for `dur` seconds. `|` forces a line break. Optional: `y` (0.15), `box`, `text_color`, `font`, `margin`, `pad`, `max_chars` (0 = wrap only on `|`). |
| `segments` | Passages in play order: `{"s": 3612.5, "e": 3619.0, "label": "the claim", "screen": "Part 1/3"}`. Chronological or not: a cold open is a short segment placed first and removed from the later one with `cut`. `label` is for humans; `screen` shows a chapter label at the top (consecutive segments with the same `screen` share it; groups longer than 15 s show it for 4 s). |
| `cut` | `[[s, e], ...]`: an exact time range, removed from the audio and the picture whatever the word timestamps say; words whose middle falls inside it leave the captions. |
| `fix` | Caption corrections: `{"s": 3713.3, "e": 3713.6, "text": "coût"}` replaces the words that START inside [s, e) with the text, timed over the same span. A fix never changes the audio. An empty text hides the words from the captions and keeps them in the clip. To remove audio, use `cut`. |
| `changelog` | One line per version: what changed and why. Shown on the review page. |

## Picture and sound

| Field | Default | Meaning |
|---|---|---|
| `frame` | `{"w": 1080, "h": 1920, "fps": 30}` | Output size and frame rate. Phone lives: `"fps": 25`. 4K vertical: `"w": 2160, "h": 3840` when the source allows it. |
| `frame.crop_x`, `frame.crop_y` | 0.5, 0.5 | Center of the 9:16 crop in the source, as a fraction of its width and height. A selfie live often needs `crop_y` 0.6 to put the face high in the frame. |
| `frame.face_x`, `frame.face_y` | 0.5, 0.42 | Point the punch-in zooms toward, inside the crop. |
| `zoom` | `{"enabled": true, "factor": 1.10}` | Every other piece is punched in, so jump cuts read as intended. |
| `captions` | font Archivo Black, size 78, 3 words or 18 characters per line, `y` 0.70, white, active word `#E8501C`, outline `#0E0E0C` | Word-by-word captions with the active word highlighted. Put `y` under the chin and above the platform's bottom text (0.70 to 0.75). `"enabled": false` for no captions. |
| `labels` | size 58, white on `#E8501C`, `y` 0.155 | Style of the `screen` chapter labels. |
| `watermark` | `{"text": "statur.co/clipping", "size": 30, "opacity": 0.55, "min": 3.5, "max": 6.5, "enabled": true}` | Small moving watermark: a new spot every `min` to `max` seconds among seven safe spots, slight drift, seeded per clip. |
| `silence` | `{"min_gap": 0.30, "pad_in": 0.06, "pad_out": 0.12, "max_keep_gap": 0.20, "bleed": 0.02}` | Pauses longer than `min_gap` are cut. Padding never reaches into a removed neighbor word beyond `bleed`. |
| `audio` | `{"lufs": -14, "tp": -1.5, "lra": 11, "highpass": 70}` | Two-pass loudness normalization. |
| `encode` | `{"crf": 17, "preset": "veryfast"}` | H.264 master. No size or length limit. |

## Several recordings in one clip

A clip can mix passages of several recordings (a supercut of the same idea told in three sessions), or a series can share one project folder. List the recordings once and give each segment its source.

| Field | Meaning |
|---|---|
| `sources` | `{"V1": {"file": "RUSHS WEB01/WEB01_V1_source.mp4", "words": "TRAVAIL WEB01/V1/asr/words.json", "audio": "TRAVAIL WEB01/V1/audio16k.flac", "sync": null, "layout": "v1_face", "size": [2464, 1300]}, ...}`. Paths are relative to the project folder (`--root`). `layout` is the default layout of that source. `size` forces the true frame size when a download stores the picture on a stretched grid (the renderer also corrects a sample aspect ratio other than 1:1 by itself). |
| `segments[].src` | The source of the segment. Times are that source's own transcript times. |
| `cut` | In a mix, write each cut with its source: `[s, e, "V2"]` or `{"s": .., "e": .., "src": "V2"}`. A cut without a source applies to the first source. |
| `fix[].src` | Same rule for caption corrections. |
| `audio.level_sources` | `true` by default: each source is measured on its own pieces and leveled to the mean of the sources before the two-pass normalization, so a quiet video call next to a loud solo recording does not jump. |

## Layouts

The default layout is the 9:16 crop above. A composed layout places rectangles of the source on the vertical frame: a screen share on top, a camera bubble in a circle, a call thumbnail in a rounded box, a blurred background. Define layouts once in `layouts`, then set `layout` on a source, on a segment, or on the whole spec.

```json
"layouts": {
  "face": {"captions_y": 0.75, "layers": [
    {"rect": [0, 0, 1, 1], "blur": 20, "dim": 0.4},
    {"rect": [0.0145, 0.6775, 0.153, 0.29], "to": [0.148, 0.2917, 0.7037, 0.3958], "mask": "circle", "border": {"w": 8}, "punch": true}]},
  "react": {"captions_y": 0.545, "layers": [
    {"rect": [0.2409, 0, 0.2956, 1], "to": [0, 0, 1, 0.5], "anchor_y": 0.3},
    {"rect": [0.0145, 0.6775, 0.153, 0.29], "to": [0.259, 0.578, 0.4815, 0.2708], "mask": "circle", "border": {"w": 6}, "punch": true}]}
}
```

| Layer field | Default | Meaning |
|---|---|---|
| `rect` | required | `[x, y, w, h]` in fractions of the source frame. Measure it on a frame of the recording (contact sheet or screenshot). |
| `to` | `[0, 0, 1, 1]` | Where the layer goes, in fractions of the output frame. A circle needs a square in pixels: on 1080x1920, `w` 0.4815 goes with `h` 0.2708. |
| `fit` | `cover` | `cover` cuts the rectangle to the target's shape (centered, or `anchor_x` / `anchor_y` from 0 to 1); `stretch` squeezes it. |
| `blur`, `dim` | none | Background treatment: blur strength (20 to 30 for a background), brightness factor (0.35 to 0.85). |
| `mask`, `radius`, `border` | none | `circle` or `round` (rounded box, `radius` in px at 1080 wide); `border` `{"w": 6, "color": "#E8501C"}`. |
| `sharpen` | none | 0.4 to 0.8 for an enlarged call thumbnail. |
| `punch` | false | This layer takes the alternating punch-in (`zoom`); put it on the face. |
| layout `captions_y` | `captions.y` | Caption height for the pieces of this layout. |
| layout `background` | `#0E0E0C` | Color behind the layers. |

`watermark.spots` (`[[x, y], ...]`, fractions) replaces the seven default spots when a layout puts a face where a spot would be.

## Planning before the download

A plan can be written on a rough transcript (the platform's captions, Loom's transcript, YouTube's) before the video arrives. Give each segment the first and last words as read there, and each cut the words to remove:

```json
{"src": "V3", "s": 62.6, "e": 75.5, "from": "aujourd'hui les gens qui regardent", "to": "une fonctionnalité qui est incroyable"}
{"src": "V3", "s": 65.8, "e": 70.8, "text": "voilà vraiment les gens qui regardent ne sont pas abonnés"}
```

After the local transcription, `snap_segments.py SPEC --root PROJECT` moves every edge onto the matching words (search window 8 s) and reports a score per edge. Under 0.6, read the passage with `words_range.py` and set it by hand.

## Publishing brief (read by the review page and the delivery step)

`caption`, `hashtags` (list), `pinned` (pinned comment), `objective` (`{"stage": "MOFU", "goals": ["authority"], "why": "..."}`), `format` (from the company's format library), `score` (the six scores and the total), `why` (one line on why this clip), `check` (list of things the reviewer should look at).

## Workflow rules

- Dry run first: `clip_render.py --plan-only` writes the cut list, the captions and words_out.json without video. Read the captions of every passage you touched before rendering.
- Place segment boundaries and cuts in pauses. Read the words with `words_range.py words.json START END`.
- One fix per phrase, never across a pause. Correct only what the speaker said: spelling, proper names, numbers, punctuation. Never rewrite the words a speaker said; if a sentence must change, cut it.
- A new version gets a new file (`C05_v2.json`) and keeps the old one: the reviewer compares versions.
