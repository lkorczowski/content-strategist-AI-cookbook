# Changelog

Newest first. One line per change: date, what changed, version.

## 2026-11-03 · v2.16.0

- statur-format-library 3.0.0: The Format Library becomes a library of 150 format cards (one file per format in skills/statur-format-library/library/formats/), tagged on four dimensions (funnel, value, structure, setup) with a controlled taxonomy (references/taxonomy.json, 3 + 7 + 41 + 24 tags) and a naming rule. Modes: find, plan a starter deck, script, invent an original format, document a format, sort a collection of saved videos, hand over the results. New tool scripts/library.py (build, check, lint, find, suggest, similar, new, gaps) with --private for a private library of cards. New references: card-template.md, private-card-template.md (with observed results per format) and collection-import.md. The twelve formats of version 2.0.0 are kept as cards. 16 cards (F135 to F150) and the status of 13 cards come from real programs, anonymized. CI runs library.py check.
- Same release, issue #12: the skill no longer reads results or decides which formats to keep (the 48-hour reading step of 2.0.0 is gone). statur-format-review decides on mature data, statur-content-learning runs the monthly lessons; this skill only copies a review decision into a private card. ARCHITECTURE section 8: Make row updated, known overlap removed. Playbook card format-library: library version 0.1.
- Ported from draft pull request #3 (format-library-coach 2.0, 2026-10-25, written before the statur- rename): paths moved under skills/statur-format-library/, skill links renamed (statur-comment-section, statur-format-review). Marketplace 2.15.0.

## 2026-11-03 · v2.15.0

- statur-clipping 2.4.0, statur-clip-edit 2.3.0, statur-clip-plan 2.2.0: several recordings in one clip or one project (spec `sources`, segment `src`, cuts and fixes per source, loudness leveled across sources), composed layouts for screen recordings and calls (camera bubble in a circle over a blurred screen, screen on top with the bubble below, call thumbnail in a rounded box, caption height per layout, watermark spots per spec), stretched downloads brought back to square pixels (sample aspect ratio, source `size`), planning on the platform's own transcript before the download (`snap_segments.py`), local transcription of chosen windows only (`transcribe.py --ranges`, `--append`), `prep_source.sh` with `SRCID`, and a mix spec template (`templates/clip-spec.mix.example.json`). Keeps 2.3.0's always-on pre-scale (now per source: `size`, then the source's `norm` or `frame.norm`, then the probed size), `captions.x`, `frame.zoom` (also per crop layout) and `--audio-preroll`. Ported from draft PR #2 (written 2026-10-24 as statur-clipping 1.1.0 from three Loom recordings mixed into five clips).

## 2026-11-03 · v2.14.1

- statur-clipping 2.3.1: `qa_clip.py --max-speech` (chunk length of the second reading, default 15 s) and the pitfall "a quality check that translates" for accented English, found on a real English live. Written as v2.7.1 / 2.1.1, renumbered at merge.

## 2026-10-28 · v2.14.0

- Playbook card statur-clipping: 34-second demo video of the second run (docs/media), page version 1.3.
- statur-clipping 2.3.0: section 1 rewritten as a one-message setup checklist (working folder, Downloads, browser extension on the computer that holds the footage, Drive, tools, the routine approved once).
- statur-clip-plan 2.1.0: captions in another language than the speech, one fix per phrase that never crosses a pause, a cut or a segment, checked against the original cut list.
- statur-clip-edit 2.2.0 and statur-clipping render_all.py: an upload copy per clip (TRAVAIL <code>/upload/<code>-<id>-v<version>.mp4, 4.5 Mbps), named with the video id used to track posts. Found while posting six LIVE02 clips on TikTok and YouTube (issue #17).
- statur-clip-review 2.1.0: the review page shows only the latest version of each clip when it is an improvement; two versions only when they are options to choose from.
- Versions renumbered at merge (written on 2026-10-28 as v2.5.1 and v2.6.0, skills statur-clipping 2.0.1 and 2.1.0, statur-clip-edit 2.1.0): main had reached statur-clipping 2.2.0 and statur-clip-edit 2.1.0 in between.

## 2026-10-28 · v2.13.0

- statur-clipping 2.3.0 (first part): Downloads folder connected once at setup (an agent cannot grant itself folder access, a night run has no one to approve it), two connected browsers (select the one on the computer that holds the footage, by device id, kept in a machine file), captions above the head on walking selfie lives. Found on the first unattended run of a TikTok live, 2026-10-28.

## 2026-10-31 · v2.12.0

- statur-motion-3d 0.2.0: engine v2 (bloom, soft shadows, ACES), animated people and a host mascot, robots and city kit, brand overlay with HUD, keyword captions and source lines, 2D editorial stage, synthesized music bed with SFX (sound2.py), production value rules from a 6/10 review, minimal 3D and 2D examples, new pitfalls.

## 2026-10-30 · v2.11.0

- New skill statur-motion-3d 0.1.0: 3D motion-design shorts in code (Three.js scene kit with day, wireframe, glow and point-cloud modes, scenario.json for texts, HUD clock, captions and sound cues, deterministic CPU render with Chromium and ffmpeg, synthesized sound bed), format recipe of viral what-if shorts, pitfalls from the first real test.

## 2026-10-29 · v2.10.0

- New skill statur-personal-brand-scale 1.0.0 and playbook card personal-brand-levels: the Korczowski scale of personal branding (Type 0 to Type 4), 16-line evidence score with decimals, trap per type, 90-day plan to the next type. Page: https://statur.co/personal-brand-levels/.

## 2026-10-28 · v2.9.0

- New playbook card ai-video-editor (The AI video editor, https://statur.co/ai-video-editor/) and five skills, one craft each: statur-video-editor-pro 1.0.0 (four-level production dial with level 1 = the statur-clip-edit render unchanged, intake with reference videos and style_probe.py, pro spec on the source timeline, build_layers.py, composite.py with person matte, subject and camera keys, inserts and grain, render_pro.py, qa_pro.py quality gate with refusal), statur-motion-design 1.0.0 (deterministic HTML templates rendered with alpha by motion_render.py: hook box, captions with emphasis, chips, name card, list card, page capture card with pan and highlights, prompt box, curve chart, loop diagram, recording cut into clips, big text behind the speaker, poster wall and grid backgrounds, end card, moving watermark), statur-sound-design 1.0.0 (generated effect library, generated music bed with drum drops, mix.py: voice chain, cues, ducking, two-pass loudness, stem report), statur-color-grade 1.0.0 (plate.py HDR to SDR, make_lut.py readable grades, scopes.py skin line and levels) and statur-broll-find 1.0.0 (capture.py, snapshot.js and render_snapshot.py for pages only the user's browser can see, assets.csv). Built from a level 4 edit of a 97-second iPhone HDR selfie on 2026-10-28.
- Plugin statur-ai-video-editor; statur-content-strategist gains the five skills. ARCHITECTURE section 8: Make row. Marketplace 2.9.0.
- Same release, after the second and third versions of the test edit: speaker card under full-screen panels (explainer split layout, `insets`, drawn after the overlays, head found in the matte), caption `y_keys` that carry any caption prop, soft plate edges for a scaled speaker (`--edge-feather`), motion_render.py stops when a brand font is missing and keeps every rendered frame in the manifest after a partial render, an "Update this skill" section (new tools, new evidence, expert rules, traps), seven new pitfalls, layouts and proof devices in the reference style card.
- Same release, after an independent fact-check: levels.md scopes the 2.5x emoji result to direct-response ads, marks which agent times were measured (levels 1 and 4) and which are estimates, gives level 4 as 35 to 45 minutes like SKILL.md and the playbook card, and links pip-and-pop to its DOI; the text safe area (y 269 to 1248, x 120 to 960 above y 840, x 120 to 780 below) is now the same in levels.md, statur-motion-design and the handbook, and qa.md says the gate checks the looser hard UI zones; SKILL.md says the matte covers the whole recording (range matting on the roadmap).

## 2026-10-31 · v2.8.0

- statur-clipping 2.2.0: `frame.norm` scales every frame before the crop (TikTok replays switch resolution mid-stream, which moved the crop off the face), `frame.zoom` for a tighter base crop (without `frame.norm`, frames still scale to the probed size as in 2.1.1); pitfalls updated (captions at 0.625, resolution switches).

## 2026-10-31 · v2.7.1

- statur-clipping 2.1.1: clip_render.py scales every frame to the probed size before the crop, so a replay that switches resolution mid-stream no longer fails some pieces. New pitfall. Found on a 1 h 51 TikTok replay.

## 2026-10-30 · v2.6.4

- statur-idea-war-map 1.1.0: ideas become beliefs. Step 3 names beliefs with a four-question test ("I believe that", any packaging, support and attack, no format word), every post gets a stance, idea_map.py counts support against attack inside a belief, templates/concepts.csv becomes templates/beliefs.csv (1.0 annotation files with a concept column still run).

## 2026-10-30 · v2.7.0

- statur-clip-edit 2.1.0: edit style "podcast split" (second camera synced on the audio, stacked split built per clip, safe zones of TikTok and Reels, motion design from an HTML page captured frame by frame for abstract ideas) and the packaging rules from the same review. statur-clipping 2.1.0: `captions.x` in clip_render.py, the watermark never takes a spot on the caption line, `hook.dur` longer than the clip keeps the text box on screen.

## 2026-10-29 · v2.6.3

- statur-clipping 2.0.1 and statur-clip-edit 2.0.1: `--audio-preroll` in clip_render.py and render_all.py (audio decoded from its own short seek when a corrupt AAC stretch silences the start of a piece), new pitfall, quality check of translated captions against the source-language words. Found on a 2 h 15 TikTok replay.

## 2026-10-28 · v2.6.2

- AGENTS.md holds the repo rules; CLAUDE.md only imports it, so every coding agent reads the same file.

## 2026-10-28 · v2.6.1

- blueprint/SPEC.md 1.1: independent review. Links to README, START.md and templates; private repo merged by a human, nobody pushes to main; C08 (cloud scheduled task read and push observed), C09 (shallow clones fetch one branch); C10 (cloud git proxy: no tag push, no branch deletion; local merges skip auto-delete); F14 and E13 (branch hygiene); acceptance tests reused by ID, not copied (P1); T06 machine file only on a personal computer. Templates: CLAUDE.md ends with branch and pull request, git-sync.sh never pushes main.

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
