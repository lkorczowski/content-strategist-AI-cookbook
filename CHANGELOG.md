# Changelog

Newest first. One line per change: date, what changed, version.

## Unreleased · Format Library 0.1 (branch format-library-v2)

- format-library-coach 2.0: The Format Library becomes a library of 150 format cards (one file per format in skills/format-library-coach/library/formats/), tagged on four dimensions (funnel, value, structure, setup) with a controlled taxonomy (references/taxonomy.json, 3 + 7 + 41 + 24 tags) and a naming rule. New modes: find, plan a starter deck, script, invent an original format, document a format, sort a collection of saved videos, read the results. New tool scripts/library.py (build, check, lint, find, suggest, similar, new, gaps) with --private for a private library of cards. New references: private-card-template.md (with observed results per format) and collection-import.md. The twelve formats of version 1.0 are all kept as cards. 16 cards (F135 to F150) and the status of 13 cards (tested or proven) come from real client programs, anonymized. CI checks the cards and the generated index.

## 2026-10-24 · v1.2

- New playbook: Video Script Structure (https://statur.co/video-script-structure/, page coming soon), with four skills: video-story-analysis 1.0.0 (nine-tier sentence map of a long video, story sheet, structure diagram, replication seed), story-replication 1.0.0 (word budget, beat map, self-map, parity and fact-check), short-video-author-analysis 1.0.0 (one creator across about twenty short videos, templates, medians, author sheet) and short-story-replication 1.0.0 (short talking-head script from one template, with sub-skills for the turn, the hook, the last line and voice adaptation). Acquisition uses only transcripts a platform shows to viewers, files the user owns or a local transcription, within each platform's terms. Examples are invented.

## 2026-10-24 · v1.1.2

- statur-clipping 1.0.2 and clip-edit 1.0.1: the root of EXPORTS keeps only the latest version of each clip; render_all.py moves older versions to EXPORTS/archives/ (--keep-old to disable), and a dropped clip goes to archives/ too.

## 2026-10-24 · v1.1.1

- statur-clipping 1.0.1 (references/sources.md: YouTube archive, replay audio and file size worded as their sources say) and clip-plan 1.0.1 (one overstatement removed), after the independent fact-check of statur.co/clipping 1.1.

## 2026-10-24 · v1.1

- New playbook: STATUR clipping (https://statur.co/clipping/), with four skills: statur-clipping 1.0 (sources: live replays, long YouTube videos, Google Drive files and folders, local files and folders; install, queue, watermark, routine; every script), clip-plan 1.0 (with the clip rubric), clip-edit 1.0 (renderer with exact cut ranges, cut-ins moved back to the speech onset with --audio, audio counted in samples against lip-sync drift) and clip-review 1.0 (review page template with a local mode, page builder). Built from a real run on a 1:40 TikTok live.

## 2026-10-24 · v1.0.1

- video-post-mortem 1.0.1 and content-learning-session 1.0.1: credit for the public workflow of Angus Sewell that shaped their structure, two rules reworded. Playbook card of The Content Testing Loop: full credit and essay link.

## 2026-10-24 · v1.0

- First public release of the cookbook: 14 skills.
- New playbook: The Content Testing Loop, with three skills: video-post-mortem 1.0 (with video log and retention curve templates), format-dice-review 1.0, content-learning-session 1.0 (with the lessons ledger template).
- Companion skills for the pages already on statur.co: creative-led-growth-coach 1.0, performance-creator-program 1.0, x-launch-week 1.0, trades-video-coach 1.0, trades-ai-setup 1.0, trades-morning-routine 1.0, trades-admin-process 1.0, format-library-coach 1.0.
- Skills for two statur.co notes: comment-section-coach 1.0 and organic-to-paid 1.0.
- Blueprint of a private AI content operating system (templates for the knowledge base, project instructions, routines, skills registry, git sync, and the human annotation loop) and its skill content-os-setup 1.0.
- Every skill reads a company context file first (kb/01_BRAND.md or .agents/product-marketing.md).
- Checks: pre-push hook installer and CI workflow.
- Tooling: scripts/check_skills.py, scripts/leak_scan.py, scripts/build_zips.py. Architecture and roadmap in docs/.
