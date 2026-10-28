---
name: statur-video-editor-pro
description: Raise the production value of a short vertical video with an AI agent and free local tools, from the basic clipping edit (the default) up to a high-production edit with color grade and HDR fix, voice cleanup, sound design and music, B-roll and captures of your own pages, motion design, background replacement and text behind the speaker. Works on one clip from statur-clipping or on any single recording. Asks the production level and for reference videos, plans every insert from what is said, renders, checks, and refuses what should not ship. Use when someone wants a polished, pro or high-production edit, B-roll, motion graphics, sound design or color on a short video.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/ai-video-editor/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# STATUR video editor pro

Part of the AI video editor playbook (https://statur.co/ai-video-editor/). Read https://statur.co/ai-video-editor.md for the human version, the evidence and the costs when you can open links.

The job: one talking-head recording or one planned clip in, one edit at the production level the user chose out, checked and ready to post. Companion skills, each owning one craft so it can change without touching the others: statur-broll-find (find, capture and log the pictures), statur-motion-design (graphics, captions, cards), statur-sound-design (voice, effects, music, mix), statur-color-grade (HDR to SDR, grade, scopes). The cut itself always comes from statur-clip-edit, so there is one cut logic.

## 0. Read the company context first

Look for kb/01_BRAND.md (blueprint) or .agents/product-marketing.md. The edit needs from it: the visual system (colors, fonts, what the brand never does, e.g. no gradients), the voice, the numbers allowed in public with their source, the names that must never appear, the assets the company owns (site, docs, repos, past posts). Turn the visual system into motion tokens (statur-motion-design references/tokens.md). Ask once for what is missing.

## 1. The production dial

Level 1 is the default and stays exactly what statur-clip-edit renders today. Higher levels add attention control first and polish last, because that is what the evidence rewards (references/levels.md, with sources).

| Level | Adds | Fits | Matte |
|---|---|---|---|
| 1 Basic (default) | statur-clip-edit simple style: cuts, word captions, hook box, punch-ins, loudness | organic clips, lives, volume tests | no |
| 2 Native plus | SDR plate and light grade, voice chain, keyword emphasis in captions, ducked music bed, sound effects on graphic entrances, one or two captures of your own pages | one-message posts, paid feed tests | no |
| 3 Proof and explainer | full-screen cards that prove each claim (captures, lists, stats with source, diagrams), name card, B-roll of your own footage | founder posts with numbers, product proof, B2B explainers | optional |
| 4 Signature | background replacement, text behind the speaker, subject moves, custom motion design matched to a reference video | launches, flagship explainers, brand stories | yes |

A separate switch, off by default, allows synthetic media (generated B-roll, avatars, cloned voices): when it is on, label the post on every platform and keep the provenance (statur-broll-find).

The user sets a ceiling; the agent picks the level per clip from the transcript: a clip with numbers earns a stat card, a product claim earns a capture, a pure opinion stays at 1 or 2. Offer a level 1 and a level 3 version of the same clip as an A/B test when the account has no data yet.

## 2. Intake: ask once

Ask these in one message, with the default the agent will use if the user does not answer:
1. Production level ceiling (default: 2 for a single video, 1 for a clipping batch).
2. Reference videos: links or files of edits they like. With a file they may use, run `scripts/style_probe.py REF.mp4 --out style.json --sheet style.jpg`, look at the sheet, and write the style card (references/intake.md). With a link only, watch it and fill the same card by hand.
3. Assets the edit may show: their site, docs, repo, dashboards, past posts and clips, product screens. Third-party pages only with a reason.
4. Music: their licensed track, the in-app library of the platform at posting time, or the generated bed (default).
5. Platforms, language of captions, deadline.

## 3. Cut, then plan the edit

1. Transcribe and cut with statur-clipping (transcribe.py, then a clip spec, then `clip_render.py --plan-only`): cutlist.json and words_out.json. A single recording uses one segment that covers the whole take; cut false starts with `cut` and fix caption spelling with `fix`.
2. Look at the picture before planning: `statur-color-grade/scripts/scopes.py` (levels, skin on the skin-tone line) and a frame grid with the caption zone drawn. Put captions where the face is not (under the chin, around 73 to 75% of the height when the face sits low).
3. Write the beat sheet: one row per sentence, what the viewer sees. Then the pro spec (references/spec.md), with every time on the source timeline so a new cut keeps graphics on their words.

Planning rules (evidence and practice in references/levels.md):
- Every insert proves or explains something said in that sentence; write the sentence next to it. No decoration.
- Hook: picture, sound and text within the first 1 to 2 seconds. The text hook makes the same promise as the spoken hook in different words.
- Keep the face on screen: back to the face within about 4 seconds after a full-screen card, never more than two cards in a row, or keep the speaker in a card under the panel (explainer split layout, `insets` in references/spec.md) when the explanation runs longer.
- A sound effect only on a visual event (a card enters, a word appears, a number lands).
- Numbers on screen carry their source line. Names follow the company rules.
- Keep the caption zone free on every card; keep text out of the platform UI zones (qa_pro.py checks).

## 4. Assets

Use statur-broll-find. Order: the company's own footage and posts, captures of its own pages (capture.py for public pages, snapshot.js plus render_snapshot.py for pages only the user's browser can see), then stock with a license, then generated media only with the synthetic switch. Every asset goes in assets.csv with its source, owner and the sentence it serves.

## 5. Render

One command runs every step and skips what is already done:

```
python3 scripts/render_pro.py --spec pro.json --clip-spec clip.json --source RAW.mp4 --words words.json --work WORK \
  --grade natural --music auto --rnnoise models/sh.rnnn --matte-model models/rvm_mobilenetv3_fp32.onnx
```

The steps, if you run them by hand: plate and grade (statur-color-grade: plate.py, make_lut.py, scopes.py), cut list (statur-clip-edit --plan-only), person matte (`scripts/matte.py`, only when the spec has keyed ranges or a layer behind the speaker), layers (`scripts/build_layers.py`, then statur-motion-design motion_render.py for bg, under and over), sound (statur-sound-design: sfx_synth.py, music_bed.py, mix.py), picture (`scripts/composite.py`), quality gate (`scripts/qa_pro.py`). Setup and speeds: references/slots.md.

Render where the footage is. On a cloud machine of 2 vCPUs a 90-second level 4 edit took about 35 minutes of compute (matte 15, layers 6, picture 12, sound 1): render a few stills first (`--frames` on motion_render.py and composite.py) and look at them before the full pass. Sandboxes stop long background jobs: render the picture in parts of 300 frames in the foreground (`composite.py --segment 0-299 --out parts/p0000.mp4`, then the next range), then `composite.py --join parts/*.mp4 --audio mix.wav --out master.mp4`. A part that exists is not rendered again.

## 6. Quality gate (always)

`qa_pro.py` measures the file, loudness (-15 to -13 LUFS, true peak at most -1 dBTP), black or frozen stretches, text in the platform UI zones, and the words heard back against words_out.json. It writes a contact sheet: look at it, frame by frame, before saying the edit is ready. It returns PASS, PASS_WITH_NOTES or REFUSE. A REFUSE is not delivered as ready to post: fix and render again, or explain to the user why this clip should not ship. Three decisions always go to a human, marked on the review page: realistic synthetic people or scenes, third-party captures, music whose license the manifest cannot prove. Checklist: references/qa.md.

## 7. Deliver

Masters keep the clipping names (`<CODE>_<clip>_v<N>_<slug>.mp4`) in the EXPORTS folder, older versions in EXPORTS/archives/, an upload copy when the master is large, and next to each master its receipts: the spec, assets.csv, the mix report and the QA report. Review on the statur-clip-review page. The user posts, or the company's posting skill does after their go.

## 8. Technology slots

Each craft is a slot with a default that runs on a CPU, a license, and alternatives (references/slots.md): tone mapping, grade, matte, voice denoise, music, effects, motion renderer, captions, B-roll source, assembly, hand-off to a human editor. When a better tool appears, change the slot and its companion skill; the spec format and the other skills stay the same.

## 9. Where it breaks

Traps met on the first real run (HDR phone footage, captions on the mouth, cards hidden behind their own panel, a word the transcript missed, a slow first render): references/pitfalls.md. Read it before the first render.

## 10. Update this skill

New tools, new evidence and expert advice change this skill through three doors, so a later reader can tell what changed and why:
- A new tool: change its slot (references/slots.md) and the companion skill that owns the craft; the spec format stays. Record the license and a measured speed.
- New evidence or an expert's rule: add it to the parameter table of references/levels.md with its evidence level (measured, platform guidance, practitioner, vendor, convention) and its source link. Change a default only for a higher evidence level, or for results measured on the account itself; otherwise keep the default and note the alternative.
- A trap met on a real run: one row in references/pitfalls.md with the fix.
Then bump metadata.version, add a CHANGELOG line, and update the playbook card and the handbook page.

## Rules

- Drafts only: the agent never posts, schedules, deletes or shares anything for the user.
- No passwords: the user signs in; captures of signed-in pages happen in the user's own browser.
- No promised views or results and no invented numbers: every number on screen comes from the recording, the company context or a source the user can open, with its source line.
- Respect each platform's terms and the rights of anyone shown: own footage and pages first, third-party material only with a reason the user approves, licensed music only, consent of every person on screen.
- Synthetic media stays off unless the user turns it on, and is then labeled on every platform.
