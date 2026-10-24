---
name: story-replication
description: Take a Fiche and its seed (from video-story-analysis) and write a complete script of the same size on a different subject, replaying the same blocks, twists, figures, loops and research moves one for one, then check parity with the source metrics and fact-check every claim. Use when someone wants to apply the storytelling structure of a long video they analyzed to their own topic, or asks to turn a Fiche or a seed into a new script.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/video-script-structure/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Story replication · from a Fiche to a new script

Part of the Video Script Structure playbook (https://statur.co/video-script-structure/, page coming soon). Read https://statur.co/video-script-structure.md for the full method once it is published and you can open links.

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing. It supplies the target creator's voice rules: register, language, banned constructions, proofs allowed.

The promise: same skeleton, new flesh. The new script has the same blocks in the same order, the same share of runtime per block, the same moves inside each block, the same loops opened and closed at the same places, the same density of jokes, questions and payoffs. Only the subject, the hero and the facts change. Every fact is real and sourced.

## Inputs

| Input | Where | Default |
|---|---|---|
| Fiche data | case folder `06-fiche.json` | required |
| Seed | case folder `07-seed.yaml` | required |
| Map and loops | `02-map.md`, `03-loops.md` | read for examples of each move |
| Target subject or question | the request | required |
| Target voice | the company context file, or the creator's style rules | the creator's own register and banned constructions |
| Target length | narration words | same as the source narration (`nar_words_total` in the source `work/stats.json`) |
| Production | footage available or not | assume no licensed footage: clip slots become quote cards or retellings |

## Outputs (folder `script-<slug>/`)

1. `00-brief.md`: target, audience, promise, voice rules, length budget.
2. `research/dossier.md`: every fact as `F## | date | claim | value | source | confidence`.
3. `01-casting.md`: the casting table (SUBJECT, HERO, MASTER, RITUAL, TRIBE, the draws, the stranger, the callback, the worst draw, the payoff venue, the deck of outcomes) with fact ids.
4. `02-beatmap.md`: block by block, move by move, source move then target move then fact ids.
5. `03-script.md`: the script, with production cues.
6. `selfmap/` (01-blocks.md, 02-map.md, 03-loops.md, generated 04-stats.md) and `05-parity.md`: the new script tagged with the same taxonomy and its metrics compared with the source.
7. `06-factcheck.md`: the verification table from a separate agent.

## Sub-skills

Recipes in `subskills/`, each with how to find the move in your source analysis, how to transpose it and an invented example:
- `find-ritual-opening.md`: the cold open that is secretly the payoff, and the bookend.
- `cast-the-saga.md`: the real hero and the dated episodes of the story thread.
- `build-the-deck.md`: a spectrum of named outcomes for an unpredictable subject.
- `explain-a-concept.md`: jargon in five steps, and the analogy forge.
- `clip-beats.md`: clip slots as footage cues, quote cards or retellings.
- `write-transitions.md`: block exits that open or close a loop, but/therefore links.
- `figures-cookbook.md`: rhetorical and comic devices with templates.
- `fact-check.md`: the dossier format and the separate verification pass.

## Process

### Step 0 · Brief
Write `00-brief.md`: the question the video answers, who it is for, the one-sentence formula transposed ("Explain SUBJECT through the multi-year saga of HERO..."), the voice rules, the length.
Length budget: run `python3 -I scripts/budget.py <source_case_dir> <target_words>`. It computes the source narrator's pace in words per minute, turns each block's clip time into shorter cards (0.6 of the clip time by default) and gives the narration words and cue seconds per block that keep the block shares of the source. Clip-heavy story blocks get more narration (retellings) than the seed's word count; lesson blocks get slightly less.

### Step 1 · Cast (sub-skills `find-ritual-opening`, `cast-the-saga`, `build-the-deck`)
Research before writing. Use several research agents in parallel (one per slot family) when available: ritual and payoff, hero timeline, deck of outcomes, domain facts for the lessons. Every fact goes to the dossier. Fill the casting table and score it with the cast-the-saga grid. Start writing at 14/18 or above.

### Step 2 · Beat map
For each block of the seed, copy the moves and write the target move next to each one, with the fact ids. This is the one-for-one contract. Keep:
- the order of blocks and moves,
- the loop openings and closings (same ids, renamed descriptions),
- the "proves" pairing: each lesson block is followed by the story beat that proves it,
- the non-linear moves: cold open from the payoff, the callback pulled forward next to its setup, the bookend.

Allowed changes: content, examples, jokes, names, numbers. A move with no fitting real material is rewritten with the same function and flagged `[ADAPTED: reason]`.

Faster in practice: write the script directly with one note line before each move, `> B07.6 TERM+DEFINE+EXAMPLE x3 · F164 F163`, then generate the beat map with `python3 -I scripts/build_beatmap.py <seed.yaml> 03-script.md > 02-beatmap.md`. It lists every seed move next to the first words of its target text and flags MISSING or EXTRA moves. Aim for zero of each. Notes start with ">" so the unit splitter and the clean reading copy ignore them.

### Step 3 · Lesson content (sub-skill `explain-a-concept`)
For each lesson block, read the seed's purpose and moves, and keep the role of each reason, fear and tip (for example a tangible reason, a reason that divides the audience, a reason explained with jargon, a reason delayed by a host rant). Find the domain's equivalent for each role. Each needs real facts.

### Step 4 · Draft block by block
Write `03-script.md` in the target voice. Production cues on their own lines: `[CLIP | ...]`, `[CARD | ...]`, `[MEME | emotion]`, `[B-ROLL | ...]`, `[RETELLING]`, `[TITLE CARD | ...]`, `[CUT TO BLACK]` (sub-skill `clip-beats`). Fact ids at the end of each factual sentence `[F07]`.

Rhythm targets come from the seed's rhythm rules and the source stats: spoken words per joke, per new loop and per thread switch. Hold them (sub-skills `write-transitions`, `figures-cookbook`). Rule of thumb: at least half of sentence-initial links are but or therefore.

Draft in passes of about a quarter of the blocks. After each pass, re-read the loop ledger and check that every open loop is still pending or closed where planned, and count words per block with `python3 -I scripts/script_units.py 03-script.md work/ <source_wpm>`. A first draft written from the beat map tends to run short, mostly in the lesson blocks and the crisis. Expand with real facts (a second example, a counter-case, a callback), never with filler.

### Step 5 · Self-map and parity
Freeze the script first: write `03-script-clean.md` (the script without note lines) and `work/units-script.tsv`, then give both to a separate agent. Any later edit that adds or removes a sentence shifts the unit ids S###; edit inside sentences, or change cue durations, until the map is done. Regenerating the units file after the mapper has started forces a round of corrections.

Tag the new script unit by unit with the taxonomy in `selfmap/` (same file names and formats as a case folder: `01-blocks.md`, `02-map.md` with glosses only, `03-loops.md`), give each unit an estimated start time from the word count (150 words per minute plus cue durations), then run `python3 -I <video-story-analysis>/scripts/analyze.py <script_folder>/selfmap <estimated_runtime_s>` and `python3 -I scripts/parity.py <source_case_dir> <script_folder>/selfmap > 05-parity.md`. Tolerances:

| Metric | Tolerance vs source |
|---|---|
| Narration words | within 10% |
| Block shares | each within 2 points |
| Thread shares | each within 7 points |
| Loops | count within 20%, same master loops, min load after minute 1 at least 2 |
| Humor per 10 min | within 25% |
| But/therefore share | at least 50% |
| Tension | peaks at 5 in the same blocks as the source |

Fix the script until parity holds, then score the new script with the rubric of the analysis skill and put both radars side by side.

### Step 6 · Fact-check (sub-skill `fact-check`)
A separate agent checks every `[F##]` sentence against its source and searches for newer figures. Apply every fix. Put the check date at the top of the script.

### Step 7 · Voice and copy pass
Apply the voice rules from the company context file. Example of a creator's rules: no em dash, no litote by negation, no "X, not Y" framing, no choppy fragment pairs in written copy, no invented numbers, proofs named and dated, no promised results. Spoken rhythm beats grammar: read it aloud in your head; split sentences over 35 words except the one long POV sentence before the payoff.

### Step 8 · Deliver
Hand the folder and the script to the user as drafts. Report: the casting in five lines, the parity verdict, the open questions (facts that need the user's call), and the estimated runtime.

## Decisions and their reasons

- Research before writing: the structure depends on real events (a callback years later needs a real person who really came back years later). Writing first and finding facts later produces fiction dressed as documentary.
- Same word count as the source narration, not the same runtime: clips and cards add runtime that depends on production. Report both.
- Clip slots become quote cards or retellings by default: most creators have no licensed footage, and long third-party excerpts are a rights risk.
- The audience thread (A) is the only place for hypotheticals; the story thread (S) contains only documented events.

## Errors to avoid (seen while building the method)

- Keeping a source figure that clashes with the target voice. The priamel ("the worst is not X, not Y, it is Z") breaks a ban on "X, not Y" framing: rewrite it as "Forget X. Forget Y. The worst is Z."
- Forcing a one-to-one content match. The function is the contract, the content is free. A lucky bystander in the source becomes whatever real person got lucky from the hero's move in the new domain.
- Facts about fast-moving companies age in weeks: date the script and re-run the fact-check before recording.
- Color details invented in retellings. A draft slips in "the whole forum catches fire", "thousands of users", "two founders in hoodies" with no source. Every concrete detail of a retelling (place, crowd, clothes, numbers) needs a fact id, or it goes.
- Causation read into dates. A startup's revenue jumps in the six months around a new model release; no source says the release caused it. Write the coincidence of dates ("in the six months around that release") and let the viewer connect it.
- Double negation in the target voice ("that day would never have existed if the lab had not..."). Search the draft for not, never, nobody, nothing, no, n't and rewrite the ones that stack ("that day exists only because...").
- Parallel research agents can share one web search budget. Give late agents known URLs to fetch, and keep a list of what is still unverified.
- The ritual can be a question the community keeps asking its masters (for example the question every podcast in the niche asks its guests) when no line spoken by the master fits the payoff. It still has to open and close the video.

## Scripts

`scripts/` holds the tools of this skill: `budget.py` (step 0), `build_beatmap.py` (step 2), `script_units.py` (steps 4 and 5), `parity.py` (step 5). They read the case folder format of the video-story-analysis skill.

## Rules

- Drafts only: never publish, send or schedule anything for the user.
- Never ask for a password. The user signs in to every platform.
- No promised views or results, and no invented numbers. Every fact in a script carries a source the user can open.
- Respect each platform's terms of use.
- Transcripts of other people's videos stay private: use them for analysis, write your own words, and credit the creator when you borrow a structure.
