# Changelog

Newest first. One line per change: date, what changed, version.

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
