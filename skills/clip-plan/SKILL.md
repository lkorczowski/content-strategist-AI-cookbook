---
name: clip-plan
description: Read the full transcript of a live, a webinar, a call, a podcast or a long video, or of several recordings on one subject, and plan the clips worth editing. Builds a topic map with viewer questions and scattered answers, scores every candidate of 60 seconds or more on hook, clarity, value, payoff, delivery and fit after hard gates, gives each one a funnel stage (TOFU, MOFU, BOFU), goals and a format, proposes a series and mixes across recordings, then writes the edit spec of each chosen clip. Works on the platform's own transcript before the video is downloaded. Use after transcribing a long recording, or when someone asks which moments of a live, a webinar, a call or a video should become clips.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.2"
  playbook: https://statur.co/clipping/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Clip plan

Part of the clipping playbook (https://statur.co/clipping/). Scripts live in the statur-clipping skill (`../statur-clipping/scripts/`); the spec format is in `../statur-clipping/references/spec.md`.

## Inputs

- The transcript with word timestamps (`words.json` from `transcribe.py`) and a block view: `transcript_blocks.py words.json > blocks.txt`.
- The company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md): buyers, positioning, voice, canonical numbers, names that must never appear, the price policy, the format library, the clip length floor. Without it, ask once for the missing parts. A plan made without the company's own knowledge picks entertaining moments; a plan made with it picks the moments that sell the company's ideas.
- Optional: contact sheets of the video, the live comments, the platform's analytics of the live.

## Method

1. Read everything, block by block. Never sample: a strong answer can sit in the last 20 minutes, and a question asked at minute 12 can be answered at minute 47.
2. Topic map: one line per topic with its time ranges, in order of appearance. Mark viewer questions (who asked is never shown), stories, numbers, strong claims, jokes and noise (greetings, gifts, trolls, reading names, technical fixes).
3. Candidates: every passage that can stand alone for 60 seconds or more. Stitch the scattered parts of one answer. Overlaps are allowed: a long answer can give a deep dive and a short cut with another hook, and the same question asked to several guests makes a supercut.
4. Score with references/rubric.md. Apply the hard gates first.
5. Check each candidate against the context file: numbers allowed, client names allowed, prices allowed, claims the speaker can defend, third parties named on air.
6. Rank. Show the plan to the user as one table, then write the spec of the first clip. After the user's review of that clip, write the specs of the others.

## Several recordings on one subject

Read every recording, then map the topics across them: the same idea told in two sessions, an example in one and the method in another. Two kinds of clips come out:
- a series: the best standalone passage of each recording;
- a mix: one clip that strings passages of several recordings (a supercut). Keep one idea per mix, open with the strongest line wherever it comes from, and keep numbers consistent: two sessions can quote different figures for the same thing, so use one passage or cut the figures.

Check the picture before choosing: a passage where the speaker is only a thumbnail (their own call window) makes an audio-led clip. Note the layout of each segment in the plan.

## Planning on the platform's transcript

Loom, YouTube and TikTok show a transcript in the page. Plan on it before the download: same method, same gates. Write each segment with the first and last words as read there (`from`, `to`) and each cut with the words to remove (`text`). Its times are per phrase and its words are approximate: after the local transcription of the chosen windows, `snap_segments.py` moves every edge onto the word timestamps.

## Before writing a spec: clean the words of each passage

Multilingual speech recognition sometimes hears a French phrase as English (or the reverse), and long chunks blur word boundaries. For every passage a clip uses:

```
refine_span.py words.json audio16k.flac START END        # second reading with 6-second chunks
merge_best.py words.orig.json words.json START END        # keep, phrase by phrase, the reading in the right language
words_range.py words.json START END                       # read the result with timestamps
```

When one word stays doubtful, transcribe a 2 to 3 second window alone (`transcribe.py` on a short extract with `--max-speech 2.5`). Still doubtful: cut the word, or ask the user to listen.

Then place segment boundaries in pauses, list the words to remove (`cut`) and the caption corrections (`fix`, one per phrase, never across a pause). A fix corrects spelling, names, numbers and punctuation; it never rewrites what was said and never changes the audio.

## Spec of a clip (input of clip-edit)

```json
{"id": "C05", "version": 1, "slug": "wolf-pack-funnel",
 "title": "...",
 "hook": {"text": "One natural sentence, 10 words max|optional line break", "dur": 3.2, "size": 90},
 "segments": [
   {"s": 3612.5, "e": 3619.0, "label": "the claim", "screen": "Part 1/3"},
   {"s": 3665.7, "e": 3671.2, "label": "the example"}
 ],
 "cut": [[3646.1, 3649.9]],
 "fix": [{"s": 3713.3, "e": 3713.6, "text": "coût"}],
 "frame": {"fps": 25, "crop_y": 0.6, "face_y": 0.75},
 "captions": {"y": 0.75},
 "caption": "...", "hashtags": ["..."], "pinned": "...",
 "objective": {"stage": "MOFU", "goals": ["authority"]}, "format": "..."}
```

- Segments play in the order given: chronological or not. A cold open is a short segment placed first and removed from the later one with `cut`.
- `screen` shows a chapter label at the top (consecutive segments with the same label share it); long groups show it for 4 seconds.
- Every field and its default: `../statur-clipping/references/spec.md`.
- Dry-run every spec with `clip_render.py --plan-only` and read the captions before any render.

## Hooks

- The on-screen hook is one natural sentence in the speaker's voice, often first person and descriptive: "Je démonte 4 pitchs de SaaS en live TikTok" ("I tear down 4 SaaS pitches live on TikTok"). A two-sentence punchline ("4 startup pitches. 1 question kills them.") reads as AI-written; the founder rejected it on the first real run.
- Use a hook-writing skill when one exists (hook stacking: a clear topic keyword plus a stake), then cut to 10 words.
- Organic clips carry no call to action. The pinned comment restates the tension and invites an answer.

## Rules

- Drafts only: the plan is a proposal; the user decides what gets edited and posted.
- No passwords, no promised views or results, no invented numbers: every figure in a hook or caption comes from the recording or the context file.
- Never show a viewer's name or handle without a reason and their consent; get guests' consent before clipping them.
- Respect each platform's terms of use, including rules on reposted and templated content.
