# The pro spec

One JSON file per edit version, next to the clip spec of statur-clip-plan. The clip spec decides the cut; the pro spec decides everything the viewer sees and hears on top of it. Every time is a SOURCE time (the times of words.json), so when the cut changes, graphics stay on their words. `build_layers.py` maps them to the output timeline with cutlist.json. Example: templates/pro-spec.example.json.

## Top level

| Field | Meaning |
|---|---|
| `id`, `version`, `code` | Same as the clip spec (`C01`, `1`, `VID01`). |
| `level` | 1 to 4 (section 1 of SKILL.md). |
| `fps`, `w`, `h` | Output frame. Default 30, 1080, 1920. |
| `tail` | Seconds added after the last word (end card, music ring-out). |
| `tokens` | Brand tokens for motion design (statur-motion-design references/tokens.md). |
| `keyed` | Source ranges where the background is replaced (needs the person matte). |
| `bg`, `under`, `over` | Motion layers. `bg`: opaque backgrounds for keyed ranges. `under`: drawn behind the speaker (text behind the subject). `over`: on top (cards, chips, end card). Each element: `{"id", "type", "src": [s, e] or "out": [s, e], "z", "props", "sfx": true}`. Types and props: statur-motion-design references/templates.md. |
| `captions` | `props` (y, size, max_width, max_chars, lines), `emph_src` (source windows whose words get the accent box) or `emph_words`, optional `y_keys` to move captions for a while. Words come from words_out.json. |
| `watermark` | Moving text, `from_src`, `to_src`, size, opacity; hidden automatically during panels, inserts and the end card. |
| `subject_keys` | Keyed ranges only: scale and move the speaker (`s`, `ax`, `ay` anchor, `dx`, `dy`, `dur`, `ease`). |
| `camera_keys` | Outside keyed ranges: punch-ins and pushes on the whole picture (`z`, `fx`, `fy` focus, `ox`, `oy` where the focus lands, `dur`, `ease`). A key holds until the next one. |
| `inserts` | B-roll files: `file`, `src`, `rect` ("full" or [x, y, w, h]), `ken_burns`, `transition` (slide or fade), `seek`, `focus_y`. |
| `sfx` | Manual cues: `src`, `name`, `gain_db`, `why`. Template entrances add their own cues (build_layers.py AUTO_SFX). |
| `music` | `bpm`, `key`, `drops_out` (output-time windows without drums: a breath before a reveal). |

Local times inside props (a chip appears, a counter starts, a highlight draws) can be given as `t_src` (source time); build_layers.py converts them.

## Planning sheet (write it before the spec)

| Source time | Sentence | Viewer sees | Proves or explains | Sound |
|---|---|---|---|---|
| 0.3 to 3.2 | Personal brand won't be the same after this hack | speaker over a wall of the account's own clips, text hook | the account posts many clips | impact, whoosh on the hook |
| 3.3 to 7.5 | I'm posting more than 10 times a day | full-screen list of today's scheduled posts from the tracking file | the number said | ticks per row |

## Rules

- One insert per claim, in the sentence that makes the claim.
- Keep the speaker's face on screen most of the time; cards last the length of their sentence.
- Never put a number on screen without its source line.
- Version every change (`_v2.pro.json`), keep the old one, write a changelog line.
