---
name: video-story-analysis
description: Map the storytelling of a long video (YouTube, TikTok, podcast) sentence by sentence on nine tiers and produce a Fiche, a character-sheet style analysis with ability scores, a spider chart, a non-linear narrative graph, a loop ledger, a beat sheet and a replication seed. Use when someone shares a long video and asks how its story works, why it holds attention, to tag or map it, or to make a Fiche of it before replaying its structure with story-replication.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.1.0"
  playbook: https://statur.co/video-script-structure/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Video story analysis · from a link to a Fiche

Part of the Video Script Structure playbook (https://statur.co/video-script-structure/, page coming soon). Read https://statur.co/video-script-structure.md for the full method once it is published and you can open links.

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing. It supplies the creator's goals, which become custom axes on the Fiche (see `references/scoring.md`).

## What you produce

One case folder `case-<slug>/` containing, in this order:

1. `source/`: transcript, clip log, coverage and visual layer, audience signals (raw material, private)
2. `01-blocks.md`: macro blocks (beat sheet)
3. `02-map.md`: every unit tagged on 9 tiers (the core of the work)
4. `03-loops.md`: the loop ledger
5. `04-stats.md` + `work/stats.json`: generated metrics
6. `05-graph.json`: narrative graph (story and lesson nodes, "proves" and "pays" edges, chronology)
7. `06-fiche.json`: scores, class, feats, equipment, flaws, audience signals
8. `07-seed.yaml`: domain-agnostic beat skeleton, the input of the `story-replication` skill
9. `fiche.html`: the Fiche page

The vocabulary for every tag is `references/taxonomy.md`. Read it before tagging. Scripts are in `scripts/`. Data formats: `references/fiche-schema.md`.

## Why it is done this way

- Several independent tiers on the same unit (track, thread, function, figure, psych, objective, tension, loops) make each layer countable. A single "label" per sentence hides the fact that one sentence can teach, joke and open a loop at once.
- Narration and clips are tagged as separate units. In a clip-heavy video, third-party footage can fill a large share of the runtime and carry most of the payoffs. An analysis of the narration alone misses the engine.
- The loop ledger is separate from the map because loops are relations between two moments. Loop load over time is the best single explanation of why a long video does not feel long.
- The seed is abstracted (HERO, SUBJECT, MASTER, RITUAL) so the structure can be replayed on any subject.

## Parallel plan (for several agents)

Acquisition needs the user's browser or files, so it runs first and in sequence. Everything after the blocks can fan out.

| Stage | Who | Input | Output |
|---|---|---|---|
| 1 Acquire | lead | link, files the user provides | source/*, work/units-asr.tsv |
| 2 Audience signals | agent S (parallel to 3) | link | source/audience-signals.md |
| 3 Blocks | lead | units, clip log | 01-blocks.md |
| 4 Tag | agents T1..Tn, one per 3 to 5 blocks | taxonomy, blocks, their units plus 3 units of context on each side | map-Bxx.md fragments |
| 5 Merge | lead | fragments | 02-map.md with harmonized codes; loop ids assigned centrally |
| 6 Loops, graph, scores, seed, Fiche | lead | map | 03 to 07, fiche.html |
| 7 Verify | blind agent | taxonomy, transcript, 30 random units | list of disagreements |

Tag agents propose loops as `?open:<short name>` and `?close:<short name>`; the lead replaces them by L## ids. Ask every agent to use only codes from the taxonomy and to list any unit it could not tag.

## Step 1 · Acquire the material

Use only sources that respect the platform's terms. Detail and snippets: `references/acquisition.md`.

1a. Transcript. In this order of preference:
- a transcript the user pastes;
- a transcript or caption file that the user or the creator owns (exported from the creator studio or the editing tool);
- the transcript or captions the platform shows to any viewer (for example YouTube's "Show transcript" panel), copied by the user or read on the page;
- a local speech-to-text run on a video the user has the right to download, such as their own.

Long reposts on short-video platforms often have no captions: look for the original upload, which often has a transcript panel. Normalize to `[mm:ss] text` lines and save the result in `source/transcript-raw.txt` with a header saying it is third-party content for private analysis. Transcripts of other people's videos are for private analysis (commentary and education); never republish them, and quote at most a short phrase with credit.

1b. Coverage. `python3 -I scripts/coverage.py source/transcript-raw.txt <runtime_s>` lists every gap over 6 s and the share of runtime without main-language speech. Gaps are usually foreign-language clips that the ASR dropped, memes, cards and music.

1c. Clip layer. Burned-in subtitles are invisible to ASR. Read them from what the player shows: inside each gap over 5 s, one look every 2 s at the subtitle strip, by watching or with screenshots. On a file the user owns, build contact sheets with ffmpeg (`references/acquisition.md`). Write `source/clip-log.md`: one bullet per clip beat with time range, track (CLIP, MEME, CARD, BREATH) and the dialogue paraphrased or quoted short.

1d. Visual layer. One frame every 30 s, from screenshots of the player or from a contact sheet of a file the user owns. Count host on camera, third-party footage, art, cards, memes, title cards. Never claim a video has "no editing" before this count: a video that feels like a talking head can show the host on camera only a small fraction of the time.

1e. Audience signals. Read what the page shows any viewer, within the site's terms: scroll the comments, read the pinned comment first (creators often correct a simplification or answer the question the video left open there), and look at the "Most replayed" graph above the progress bar if the platform shows it. In the first days it may be absent: note it and check later. Write a paraphrased summary grouped by mechanism. Never copy comments or keep commenter names.

## Step 2 · Segment

`python3 -I scripts/segment.py source/transcript-raw.txt work/meme_times.txt > work/units-asr.tsv`

The script marks lines that look English as CLIP, for a video in another language with English clips. On an English-language video, add `none` as a third argument to switch that check off. `meme_times.txt` lists the start time of every main-language line that breaks the host's register (film or TV lines): you find them while reading the transcript and checking the frames. Then decide by hand:
- Replace dense foreign-language clip regions by clip beats from the clip log (the word-list language detector misclassifies short lines).
- Merge consecutive ASR sentences that form one gesture (an enumeration, a two-line joke) into one unit `U092-095`.
- Split a sentence that carries two functions (`U253a`, `U253b`).

## Step 3 · Macro blocks

Cut a new block when the job changes (new reason, new story episode, pivot, payoff). Give each block one beat code from the taxonomy, a title, threads and a one-sentence job. Plan 15 to 25 blocks for 45 minutes. Write `01-blocks.md` with the machine table first (columns blk, start, end, beat, threads, title, job; the scripts parse it), then reading notes: what is braided with what, what breaks chronology and why.

## Step 4 · Tag the map

Write `02-map.md` as a pipe table with these columns: id, t, blk, trk, thr, fn, fn2, fig, psy, obj, T, loop, cx, incipit, gloss.

Rules that keep a map consistent:
- One primary function per unit, up to three secondary. If you want five, split the unit.
- Tension 0 to 5 follows the definitions in the taxonomy. Story blocks sit at 3 to 5, teaching at 1 to 2. A clip of the payoff is 5 only if the viewer has been waiting for it.
- Loops: write `L##o` where a loop opens and `L##c` where it closes, in the same row as the unit.
- Connective (`cx`): read the first words of the sentence (but, yet, so, because, and, or their equivalent in the video's language). It feeds the but/therefore ratio.
- `incipit` = first words of the original (private use). `gloss` = what the unit does, in English, in your own words. The gloss is what the replication skill reads, so describe the move, not just the content.
- Tag figures only when they are really there. A simile is not a metaphor; a comic understatement is MEIOSIS, an understatement by negation is LITOTE.
- When no code fits, add one to the taxonomy changelog with the kind of unit that needed it.

## Step 5 · Loop ledger

`03-loops.md`: id, open_t, open_u, close_t, close_u, type (Q, TEASE, PROMISE, PLANT, LIST, DETOUR, OBJ), scale (MASTER over half the runtime, ARC, MICRO under a minute, OPEN never closed), description. Then three reading notes: master loops, the keystone (the return that reveals the shape), the doors left open.

## Step 6 · Metrics

`python3 -I scripts/analyze.py <case_dir> <runtime_s>` writes `04-stats.md`, `work/stats.json` and the tension and loop-load curves. Read it against the map: the longest stretch without a story unit, blocks with low tension and no host thread, the causal-link ratio. Every number you put in the Fiche comes from this file. Add the sentence rhythm with `python3 -I scripts/rhythm.py work/units-asr.tsv`: share of short sentences, longest run of long ones, runs to fix.

## Step 7 · Graph

`05-graph.json`: nodes for story episodes (with the real date when known), lesson sections, host and audience moments; edges `proves` (story beat illustrates lesson), `pays` (later node pays an earlier plant), `leads`; a `chronology` list with the order told and the real order, plus `real_order`. Then `python3 -I scripts/draw.py <case_dir> <runtime_s>` draws braid, graph, chronology and radar. Check them with `python3 scripts/preview.py <case_dir> <png_dir>` (needs `pip install cairosvg`; use it when no headless browser is available) and look at the PNGs once.

## Step 8 · Scores

Eight core abilities out of 20 (Curiosity, Weave, Clarity, Authority, Voice, Humor, Emotion, Payoff) with the role-playing modifier. Use the anchors in `references/scoring.md` and write one evidence line per score with the numbers from stats. Add the creator's own axes as weighted mixes of the core scores (`custom_axes_example` in the JSON); take the goals from the company context file when there is one. Also fill class, background, alignment (a one-line joke grounded in data), the one-sentence formula, 8 to 12 feats (how and where), equipment (assets the format needs), flaws and audience signals.

Then place the video on the story ladder (`references/story-ladder.md`): the highest level whose check passes with all levels below it, one evidence line per rung, and the next rung as the first improvement.

## Step 9 · Seed

`07-seed.yaml`: per block, share of runtime, narration words, clip share, purpose, ordered moves `[codes, abstract instruction, source example]`, loops, research needs, asset needs, plus the saga requirements and rhythm rules at the top. Write instructions with placeholders (SUBJECT, HERO, MASTER, RITUAL, TRIBE). Check that shares sum to 1.0 and words to the narration total (`python3 -c "import yaml..."`).

Invented example of one move: `[HYPO+FEAR, "Make the viewer imagine losing what HERO built in one moment", "the founder pictures the launch dashboard stuck at zero"]`.

## Step 10 · Fiche page

`python3 -I scripts/build_fiche.py <case_dir> <case_dir>/fiche.html`. Open it in a browser, look at it once, fix in one pass and rebuild. The page title and eyebrow come from `06-fiche.json` (default "Story Fiche"). Describe diagram elements by line style, never by color: the page has a dark theme where colors change. The Fiche is a draft for the user; the user decides whether to share it.

## Step 11 · Verify and store

- 30 random units checked against the transcript and the taxonomy by a separate agent that did not tag them.
- Every date, number and name in the Fiche traced to the transcript, the clip log or a source. Remove what is not: a year with no source slips into a note easily.
- Reference URLs verified with a search, never recalled from memory.
- Keep the case folder in a private folder or repository: it holds third-party material.

## Errors seen while building the method, and the fix

| What went wrong | Why | Fix now in the method |
|---|---|---|
| No captions on a long repost | Long reposts on short-video platforms often lack captions | Find the original upload and its transcript panel |
| The transcript panel will not load | Pages and panels fail sometimes | Ask the user to paste it, or run local speech-to-text on a file the user has the right to use |
| A large share of the runtime missing from the transcript | ASR in the main language drops foreign clips; burned-in subtitles are images | Read the clip layer from what the player shows |
| Screenshots from the wrong timestamps | Two capture runs overlapped | One capture run at a time; redo any sheet whose subtitle lines do not follow each other |
| "No editing" assumption | The brief said so | Count the visual layer before agreeing |
| An unverified URL in the taxonomy | Recalled from memory | Search, then cite |
| Arcs called by their color in captions | The page theme changes colors | Name line styles |

## Copyright and privacy

The transcript, clip log and comments are third-party content: keep them private. The Fiche and any public guide use paraphrase and at most one short quote per source, under 15 words, with credit. Comments are summarized by mechanism, never copied with names.

## External resources

- Taxonomy and psych references with URLs: `references/taxonomy.md`
- Rhetorical figures: https://rhetoric.byu.edu/
- But/therefore rule: https://www.firstwriter.com/articles/?GUID=3831
- Curiosity gap: https://stafforini.com/works/loewenstein-1994-psychology-curiosity-review/
- Multimedia learning principles (signaling, personalization): https://lucidea.com/blog/mayers-12-principles-of-multimedia-learning

## Sample

`sample/01-sample-checklist/` is an invented short video, already split into units and tagged on the nine tiers (all names, numbers and events invented). Run `python3 -I scripts/analyze.py sample/01-sample-checklist 58` to check your setup, and use its files as a format reference. See `sample/README.md`.

## Rules

- Drafts only: never publish, send or schedule anything for the user.
- Never ask for a password. The user signs in to every platform.
- No promised views or results, and no invented numbers. Every fact in a script carries a source the user can open.
- Respect each platform's terms of use.
- Transcripts of other people's videos stay private: use them for analysis, write your own words, and credit the creator when you borrow a structure.
