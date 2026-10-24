---
name: short-story-replication
description: Take an author Fiche and its short seed (from short-video-author-analysis) and write a short talking-head script (60 s to 7 min) on a new subject that replays one of the author's templates beat for beat, in the target creator's own voice, with sourced facts, then check parity with the author's medians. Use when a creator wants a TikTok, Short or Reel script that follows the structure of a creator they analyzed.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/video-script-structure/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Short story replication · from an author Fiche to a short script

Part of the Video Script Structure playbook (https://statur.co/video-script-structure/, page coming soon). Read https://statur.co/video-script-structure.md for the full method once it is published and you can open links.

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing. It supplies the target voice: register, banned constructions, and the proofs the creator may cite.

The promise: the same template, the same beat shares, the same density of loops, jokes and facts per minute as the author's median video, on a new subject, in the target creator's voice. A short video has no room for padding, so every beat has one job and the last line closes the first loop.

## Inputs

| Input | Where | Default |
|---|---|---|
| Author grammar and seed | case folder `10-author-grammar.md`, `11-templates.md`, `07-seed-short.yaml` | required, from `short-video-author-analysis` |
| Gold and example videos | case folder `videos/` | read 3 videos of the chosen template before writing |
| Subject | the request | required |
| Facts | a research dossier, one fact per line: `F## \| date \| claim \| value \| source` (reuse one if it exists) | every factual sentence carries [F##] |
| Target voice | the company context file or the creator's own style rules | the creator's register and banned constructions |
| Length | the template's median length and the author's median words per minute, from `10-author-grammar.md` | required |

## Outputs (folder `script-<slug>-short/`)

1. `00-brief.md`: subject, template chosen and why, length, voice rules.
2. `01-plan.md`: the template's beats with target shares and times, and for each beat the move, the fact ids and the loop it opens or closes.
3. `02-script.md`: the script with one note line per beat (`> B02 TURN · F12`), production cues on their own lines (`[IMAGE | ...]`, `[SCREENSHOT | ...]`, `[TEXT | ...]`), fact ids.
4. `03-selfmap/`: the script tagged like a case video (blocks, map, loops, card) and `04-parity.md` against the author's medians.
5. `05-factcheck.md`: from a separate agent when the facts are new; a re-check of the ids when the dossier was already checked.

## Process

### Step 1 · Pick the template
Pick the template from YOUR author analysis (`11-templates.md`) whose shape fits the subject. Shapes vary by author. Invented illustrations: a mystery with a solution, a strange fact that becomes a lesson, an assumption to knock down. Write in `00-brief.md` why this template fits this subject, and which videos of the template you read.

### Step 2 · Find the five things a short needs (sub-skill `find-the-turn`)
1. The hook fact: one strange, true, dated sentence the viewer cannot scroll past.
2. The viewer's assumption: what most people believe about the subject, stated fairly. It plays the part of the author's voiced objection.
3. The turn: the true fact that breaks the assumption.
4. The build: 2 to 4 escalating details, each with a source.
5. The button: a last line that returns to the hook image or flips the moral (sub-skill `write-the-button`).
Start writing once all five have a fact id or are marked as the creator's opinion.

### Step 3 · Plan the beats
Copy the template's beats and shares into `01-plan.md`, convert shares to seconds and words at the target pace, and place every loop: a hook loop opened in the first 3 seconds and closed by the last line, plus one or two micro loops per minute.

### Step 4 · Write
Spoken style, one idea per sentence, sentences under 25 words except one long accumulation in the build. Respect the target voice. When the author's signature figure clashes with it, use the affirmative equivalent from `subskills/voice-adaptation.md`. Example: a reversal built on two opposed halves clashes with a voice that bans negation-based framing.

### Step 5 · Self-map and parity
Turn the script into timed units: `python3 -I scripts/script_units.py 02-script.md work/ <author_wpm>`. Write those sentences as a transcript with cue times (a `duration_s:` header line, then one line per sentence, `[mm:ss.s] text`), then run `python3 -I scripts/short_units.py work/transcript.txt selfmap`. Tag the units with the author analysis method (blocks, map, loops, card), run `python3 -I scripts/analyze.py selfmap <runtime_s>`, and compare with the template's videos: `python3 -I scripts/parity_short.py <author_case_dir> selfmap <video prefixes of the template>`. Check the hook loop row by hand from `03-loops.md`.

| Metric | Tolerance |
|---|---|
| Length | within 15% of the template median |
| Beat shares | each within 8 points |
| Turn position | within 0.15 of the template median |
| Loops per minute | within 30% |
| Jokes per minute | within 40% |
| Facts per minute | within 40% |
| Sentences with "you" | within 10 points |
| Hook loop | opened by second 3, closed in the last 10% |

Explain every row marked FIX in `04-parity.md`: fix it, or state why the gap is deliberate. A deliberate gap is fine when the target voice asks for it, for example a creator who cites more sourced numbers than the author.

### Step 6 · Fact-check and deliver
Check every [F##] against the dossier (separate agent if the facts are new), date the script and save it. Deliver to the user as a draft: the script, the template used, the parity verdict and the runtime.

## Calibration
Every target comes from your own author analysis: medians from `10-author-grammar.md`, the template from `11-templates.md`, the beats and moves from `07-seed-short.yaml`. Copy no number from another author or from an example.

## Sub-skills
- `subskills/find-the-turn.md`: finding the assumption and the fact that breaks it.
- `subskills/write-the-hook.md`: the hook types the author uses most, with a test for each.
- `subskills/write-the-button.md`: endings that close the hook loop.
- `subskills/voice-adaptation.md`: moving the author's figures into another creator's voice.

## Errors to avoid
- Copying the author's topics or sentences. The template is the contract; the subject, the facts and the voice are yours.
- A button that summarizes. Strong endings return to an image or flip the moral; a summary closes nothing.
- Facts without dates in a short video: the viewer has no time to check, so a wrong number costs more trust than in a long one.
- Reusing an undefined term. A word coined in another script (a nickname for a company, a running metaphor) reads as noise in a short where it was never introduced. Define it in the script or use the plain name.
- Leaving the viewer out. Compare the share of sentences with "you" with the author's median. Small rewrites inside existing sentences ("the tool you might be using right now") close the gap without adding a sentence.
- A setup that implies a false end state. "Company A resold Company B's model until Company B launched its own app" suggests Company A stopped. Split the sentence and state only what the source says.

## Rules
- Drafts only: never publish, send or schedule anything for the user.
- Never ask for a password. The user signs in to every platform.
- No promised views or results, and no invented numbers. Every fact in a script carries a source the user can open.
- Respect each platform's terms of use.
- Transcripts of other people's videos stay private: use them for analysis, write your own words, and credit the creator when you borrow a structure.
