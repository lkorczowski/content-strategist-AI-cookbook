---
name: statur-clip-review
description: Run the review loop of edited clips with a human. Publishes light review copies on a private review page where the reviewer plays each clip, pauses, writes notes stamped at the exact frame, gives a verdict per clip and votes on the rest of the clip plan, then reads the notes back, turns each one into a spec change, renders the next version and answers the note. Works as a private Claude artifact, as a local page opened from disk, or with Frame.io when the team already uses it. Use after a first edit, when a founder or a client must approve clips, or when someone wants a Frame.io-like review without a paid tool.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "2.1.0"
  playbook: https://statur.co/clipping/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Clip review

Part of the clipping playbook (https://statur.co/clipping/). The page template is templates/review.html, the data format templates/review-data.example.json, the builder scripts/build_review.py. Renders come from the statur-clip-edit skill.

## Surfaces

| Surface | Cost | The agent reads the notes | Use it when |
|---|---|---|---|
| Private Claude artifact built from templates/review.html | included in Claude | yes, from the page's data store | the reviewer uses Claude; review copies under 20 MB each |
| The same page opened from disk (local mode) | free | the reviewer clicks Copy notes and pastes them in the chat | any assistant, no account needed |
| Frame.io | paid seats | yes, through its MCP server (public beta) or comment webhooks | the team or the client already reviews there |
| Google Drive comments | included | no reliable way | a quick look, weak for a loop |

The page: a 9:16 player with frame stepping and speed control, notes stamped at the player's time (or a range with I and O), tags (cut, pace, captions, hook, audio, image, other), a verdict per clip version (ready to post, needs changes, drop it), the clip brief (hook, goal, format, scores, caption, hashtags, pinned comment, what to check), the passages used in the source, and the whole clip plan with a vote per candidate. French and English interface.

## Build the page

1. Render review copies with statur-clip-edit (`--review`): a 720x1280 MP4 under 19.3 MiB and a poster per clip version.
2. Write data.json (shape: templates/review-data.example.json): the recording (code, title, date, duration in seconds), one entry per clip version (id, v, title, dur, fps, src, poster and the brief), and the plan. Show only the latest version of each clip when it improves on the previous one (a fix, a better hook, captions moved): the reviewer judges what will be posted, and the changelog of the brief says what changed. Keep two versions side by side only when they are two options the reviewer must choose between. Older masters stay in EXPORTS/archives. `start` picks the version shown first; `lang` is fr or en.
3. Claude artifact: upload each review copy and poster as an asset of the artifact, put the returned URLs in `src` and `poster`, build with `python3 scripts/build_review.py data.json templates/review.html "<CODE> Clip Review.html"` and publish it private, with the capabilities db, user and assets. Share the link only with the reviewers.
4. Local mode: build the page into the folder that holds the review copies, with `src` and `poster` as file names, and open it in a browser. Notes stay in that browser until the reviewer clicks Copy notes.

## The loop

1. Send the link with one line per clip: what it is and what to check. Ask for a verdict on every clip.
2. The reviewer pauses at the moment, picks a tag, writes the note, optionally marks a range, then gives a verdict.
3. Read the notes. Artifact: collections `notes` (clip, v, t, t2, tag, text, state), `verdicts` (one per clip version) and `planvotes`. Local mode: the JSON the reviewer pasted.
4. Map each note to a spec change: move a cut, remove a passage, add a cold open, fix a caption word, change the hook, change the framing. Change only what the note asks for. Write the change in the spec's `changelog`, bump `version`, dry-run, render, run the quality check.
5. Answer each note on the page: set `state` to `done` and `reply` to one line ("Fixed in v2: hook in one sentence"). In local mode, answer in the chat.
6. Replace the clip's entry in data.json with the new version (its changelog lists every change), upload its review copy, rebuild and republish the same page. Tell the reviewer what changed, clip by clip.
7. Stop when every clip has a verdict. "Ready to post" means the master in EXPORTS is the one to publish; "Drop it" removes the clip from the batch. Plan votes decide which candidates are edited next.

## Rules

- Drafts only: nothing is posted, scheduled or shared by the agent beyond the reviewers the user names.
- No passwords: reviewers sign in to their own accounts; the agent never asks for credentials.
- No promised views or results, no invented numbers in the brief.
- Review copies can show people who did not consent to be published: keep the page private and the link with the reviewers.
- Respect each platform's terms of use when the approved clips are posted.
