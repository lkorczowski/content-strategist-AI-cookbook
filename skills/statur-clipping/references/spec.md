# The clip spec

One JSON file per clip version. clip-plan writes it, clip-edit renders it, clip-review changes it. Times are seconds on the transcript timeline (the times of words.json). Example: templates/clip-spec.example.json.

## Content

| Field | Meaning |
|---|---|
| `id`, `version`, `slug` | `C05`, `2`, `wolf-pack-funnel`. The master is named `<CODE>_<id>_v<version>_<slug>.mp4`. Bump `version` for every change the reviewer will see. |
| `title` | Working title, for the review page. |
| `hook` | `{"text": "...", "dur": 3.2, "size": 90}`. One natural sentence of ten words or fewer, in the speaker's voice, shown in a box at the top for `dur` seconds. `|` forces a line break. Optional: `y` (0.15), `box`, `text_color`, `font`, `margin`, `pad`, `max_chars` (0 = wrap only on `|`). |
| `segments` | Passages in play order: `{"s": 3612.5, "e": 3619.0, "label": "the claim", "screen": "Part 1/3"}`. Chronological or not: a cold open is a short segment placed first and removed from the later one with `cut`. `label` is for humans; `screen` shows a chapter label at the top (consecutive segments with the same `screen` share it; groups longer than 15 s show it for 4 s). |
| `cut` | `[[s, e], ...]`: words whose middle falls inside a range are removed from the audio, the picture and the captions. |
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

## Publishing brief (read by the review page and the delivery step)

`caption`, `hashtags` (list), `pinned` (pinned comment), `objective` (`{"stage": "MOFU", "goals": ["authority"], "why": "..."}`), `format` (from the company's format library), `score` (the six scores and the total), `why` (one line on why this clip), `check` (list of things the reviewer should look at).

## Workflow rules

- Dry run first: `clip_render.py --plan-only` writes the cut list, the captions and words_out.json without video. Read the captions of every passage you touched before rendering.
- Place segment boundaries and cuts in pauses. Read the words with `words_range.py words.json START END`.
- One fix per phrase, never across a pause. Correct only what the speaker said: spelling, proper names, numbers, punctuation. Never rewrite the words a speaker said; if a sentence must change, cut it.
- A new version gets a new file (`C05_v2.json`) and keeps the old one: the reviewer compares versions.
