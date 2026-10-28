# Changelog

Newest first. One line per change: date, what changed, version.

## 2026-10-28 · v2.6.0

- blueprint/SPEC.md 1.0: specification of EVEREST OS (goal, nine principles, stores, orchestrators, adoption levels, feature catalog, edge cases, dated platform constraints, acceptance tests T01 to T14). Instances keep their status table in their own repo and link here.

## 2026-10-28 · v2.5.0

- New playbook card x-ghostwriter (The X Ghostwriter Handbook, https://statur.co/x-ghostwriter/) and three skills: statur-x-viral-post-ghostwriter 1.0.0 (drafts and score lines for X posts, replies, quotes and Articles, weekly mix, cold-start mode, 30-day contract and scorecard, references/x-ranker.md as the single owner of X ranking facts), statur-brand-dna-audit 1.0.0 (refusal list, voice mix, pillars from buyer beliefs, one reader, one outcome, proof bank, written from evidence) and statur-hook-forensics 1.0.0 (case files and hook formula file for text posts and X Articles). Built from Avid's paid-partnership X Article of 2026-10-26, checked against X's published code, tested on a 20-follower account.
- statur-social-analytics 2.1.0: kind `posts` for X and LinkedIn, post_labels.csv, views `posts` and `post_log`, X route notes (analytics locked under 50 followers, UTM for link clicks, date from the post id).
- statur-x-launch 2.1.0: ranking facts now cite X's published weights through references/x-ranker.md; hand-over to statur-x-viral-post-ghostwriter after day 14.
- Blueprint 01_BRAND.md: brand DNA slots (one reader, one outcome, pillars, proof bank, refusal list, voice mix). ARCHITECTURE section 8: rows and shared definitions for the X skills.
- Plugin statur-x-ghostwriter; statur-content-strategist gains the three new skills. Marketplace 2.5.0.
- .gitattributes: LF line endings in every clone.

## 2026-10-27 · v2.4.0

- New skill statur-share-social-media 1.0.0 (STATUR social analytics): give a content advisor access to Instagram, Facebook Page, TikTok, YouTube and LinkedIn analytics with the least access, without a password in plain text (Meta business portfolio invite, password manager share for personal TikTok accounts, YouTube Viewer role).

## 2026-10-27 · v2.3.0

- blueprint/START.md 1.0: public operating manual for client projects in ChatGPT or Claude. A one-line project instruction points to it. "Start EVEREST OS" runs the onboarding: brief, pre-onboarding checklist, intake interview, knowledge base files, email draft to the advisor. Every later conversation starts from STATE.md with its CRITICAL and BLOCKED items. New template blueprint/templates/STATE.md.

## 2026-10-27 · v2.1.0

- New skill statur-idea-war-map 1.0.0 and playbook card how-ideas-go-viral: map the ideas of an online controversy (implied ideas, concepts, camps, third parties, quote duels, Elo). Worked example: the French vs Japanese war on X, October 2026.

## 2026-10-26 · v2.0.0

- Breaking: every public skill now starts with statur-. Folder, frontmatter name and links renamed, every skill at version 2.0.0. Old paths keep a README-only folder that points to the new name until 2027-01-31 (no SKILL.md, so no tool loads them). Renames:
  - video-post-mortem -> statur-video-post-mortem
  - format-dice-review -> statur-format-review
  - content-learning-session -> statur-content-learning
  - video-story-analysis -> statur-story-analysis
  - story-replication -> statur-story-replication
  - short-video-author-analysis -> statur-author-analysis
  - short-story-replication -> statur-short-story-replication
  - clip-plan -> statur-clip-plan
  - clip-edit -> statur-clip-edit
  - clip-review -> statur-clip-review
  - creative-led-growth-coach -> statur-creative-led-growth
  - performance-creator-program -> statur-creator-program
  - organic-to-paid -> statur-organic-to-paid
  - format-library-coach -> statur-format-library
  - comment-section-coach -> statur-comment-section
  - x-launch-week -> statur-x-launch
  - trades-video-coach -> statur-trades-video
  - trades-ai-setup -> statur-trades-setup
  - trades-morning-routine -> statur-trades-morning-routine
  - trades-admin-process -> statur-trades-admin
  - content-os-setup -> statur-content-os-setup
  - meta-ads-scaling-coach -> statur-meta-ads-scaling
  - statur-clipping and statur-social-analytics keep their names.
  - On unmerged branches: account-network-coach -> statur-account-networks, slideshow-maker -> statur-slideshow-maker.
- Plugins renamed statur-<playbook> (statur-content-testing-loop, statur-storytelling, statur-tradespeople...) and two role bundles added: statur-content-strategist and statur-creative-strategist. Marketplace version 2.0.0.
- scripts/rename_skills.py: the same rename for any branch or private instance (idempotent).
- README: naming section. CLAUDE.md: naming convention.

## 2026-10-26 · v1.5

- New playbook: Scale Meta ads without cost inflation (https://statur.co/scale-meta-ads/), with the skill meta-ads-scaling-coach 1.0.0: diagnosis (creative, offer, page), one purchase campaign, live ads sized to the budget, creative test lane, partnership ad share, offers and statics, weekly 7-day read, monthly contribution after ad spend, limited-time sale lane. US rules, France and EU end note. docs/ARCHITECTURE.md section 8: paid row added.

## 2026-10-26 · v1.4

- Video Script Structure 1.1: video-story-analysis, story-replication, short-video-author-analysis and short-story-replication 1.1.0. New reference story-ladder.md (five levels mapped to the nine tiers, credited to Kallaway) and new scripts/rhythm.py (share of short sentences, longest run of long sentences, runs to fix; the short-sentence trick credited to ginyboi and Kallaway). Analysis skills place videos and templates on the ladder; replication skills plan one move per rung and check rhythm before and after the self-map.

## 2026-10-26 · v1.3

- New playbook: STATUR social analytics (https://statur.co/blog/own-your-social-media-analytics/), with the skill statur-social-analytics 1.0.0: analytics base in plain files (accounts.csv, raw collections, proof screenshots), collection routes ranked from official APIs to screenshots, analytics.py (init, build into SQLite, sql, dice, winners, export-log, TOTALS.md), proof.py (blurred copies), ready SQL questions and an invented sample.
- docs/ARCHITECTURE.md 1.1: section 8, one job per skill (measure, diagnose, decide, make), shared definitions (video log columns, early signal at 48 hours, mature data at 7 days, viral line) and the known overlap of format-library-coach 1.0.
- video-post-mortem 1.0.2, format-dice-review 1.0.1, content-learning-session 1.0.2: read the analytics base when it exists instead of asking for numbers.

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
