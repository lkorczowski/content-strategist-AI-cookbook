---
name: statur-video-to-essay
description: Turn a short video that worked (your own talk, rant or explainer, or a third-party video you react to) into a standalone, sourced English blog essay in the author's voice, with an argument table, open questions answered by research, an idea database, an SEO and AI-search review, a WordPress block draft and an image concept. Use when someone asks to turn a TikTok, Reel, Short, Loom or podcast clip into a blog post or essay.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/playbooks/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Video to essay

A video that worked proved its idea. The essay turns it into an evergreen, sourced asset. Golden rule: the essay stands alone. The video is raw material, never the subject; the blog reader has not seen it and does not need to.

## Context: what this skill loads, and when

| File | Where | Read it |
|---|---|---|
| `kb/context/statur-video-to-essay.md` | the author's private repo or project documents | At the start of every run, when it exists |
| The brand file it names (voice, proof table, visual rules, client confidentiality) | same place | Before step 7 and step 11 |
| The idea database it names | same place | At step 4 |

The context file holds the brand goal, where the inputs come from, the site's categories and storage folders, the author's voice markers and banned formulas, the publishing procedure, and the journal of past essays with the author's corrections. No context file: ask for the voice sample, the proof the author allows, and the site, and say so in one line.

## Inputs

- The raw transcript (often an automatic one, full of errors).
- The on-screen hook text: it made people stop, so the H1 reuses it as closely as possible.
- Stats and comments: they serve the analysis in the dossier, never the body of the essay.

## Pipeline

1. Clean transcript in the source language: remove fillers and repeats, fix transcription errors and proper names, keep the spoken tone, flag inaudible parts.
2. Argument table: `# | argument | strength | what the essay does with it`. Name the main logical gap between the premises and the conclusion.
3. Open questions: the 3 to 5 questions a demanding reader asks after the video and that it leaves open. Each becomes a section, fed by research.
4. Idea database: one row per idea with the original wording, a status (CORE, SUPPORT, TO FIX, OFF-BRAND), the fix or the source, and where it is reused. New rows continue the numbering.
5. Dossier only: summary, strengths, weaknesses, rates (likes, saves, shares, saves per like), comment clusters, real audience against the target reader. Say plainly if the comments serve the positioning.
6. Plan: the essay's own goals (brand, thesis, search, distribution), then the logical path section by section. The essay's thesis may go beyond the video's.
7. Draft v1, already written as a standalone essay.
8. Review: the site's SEO and AI-search gate if it has one, TL;DR, FAQ, internal links, the original video in an annex, sources checked by web search, thinkers and quotes, one proof from the brand's proof table, what to cut, the independence test. Then run statur-humanizer on the draft.
9. Draft v2: the review and the answers to the open questions. This version goes to the site.
10. Draft on the site (procedure below).
11. Image concept (below).
12. Hand-over: dossier and v2 to the author, files stored, idea database updated.

## Writing rules

- Independence: no platform stats in the body (views, saves, comments, shares), no story of the video or its follow-ups ("in my video"). The community can appear when it brings a precise idea ("the most common objection was..."). Test: remove every mention of the platform and the essay still stands.
- Go further than the video: facts, counter-arguments and answers it did not have.
- Keep the meaning the author gives to their own examples. Never bend an example to fit the thesis.
- Facts: every market claim, number or quote is checked and linked, primary source first. A number from the video with no source is removed or reworded. When research contradicts the author, the essay gives the right number. Platform data must be recent and specific to short-form video.
- Steelman: quote a contradicted expert with their exact, sourced position. Attack ideas, never people. Describe what a named person said and did, never a motive they did not give.
- Comments: paraphrased or translated, never with the handle.
- One canonical proof per essay, worded as in the brand file.
- Opinion essay: no call to action in the body, a dry last line (one thesis sentence), the site link in the author bio.
- When the transcript holds a how-to, the essay ends with a "How to..." section that keeps and enriches those steps. No invented metrics.
- When a third-party example carries the argument, embed it in the paragraph that describes it.
- Sensitive personal content said on video (health, family, other people's private lives) never goes in the essay; flag it in the dossier.
- Shape: hook (credibility + fact or tension + the question the essay settles), bold TL;DR (5 bullets), H2 sections (one per open question), the community's main objection when it is critical, the how-to when there is one, a question back to the reader, the thesis line, FAQ (3 to 4 questions), "Annex: the original video" (one sentence + embed), bio.
- Length: 1,500 to 2,400 words without the FAQ.
- A third-party video: the essay stays the author's (their practice, their thesis); the video is credited in its paragraph, with no annex and no stats.

## Title and search

- H1: the closest translation of the on-screen hook. It must not carry an idea the body corrects.
- SEO title, slug and meta: the site's gate, or a keyword-led title under 60 characters and a meta of 140 to 155 characters.
- When the topic also has a practical page on another site: pick the two main keywords before writing any title (autocomplete and the results page, no paid tool). The essay takes the opinion or definition query ("Do X work?", "what is X"), the practical page the how-to query. Neither puts the other's main keyword in a title or an H2. One link from the essay to the practical page, in the bio.

## WordPress draft (block editor)

- The author signs in. Default status: draft. Never publish or schedule without the author's yes.
- Before editing an existing draft, check through the API (`modified`, revisions) that the author did not edit it. If they did, propose the changes instead.
- In the editor page: `wp.blocks.rawHandler({ HTML })` to build the blocks, replace each marker paragraph with `wp.blocks.createBlock('core/embed', { url, providerNameSlug, type: 'rich' })`, `resetBlocks`, `editPost({ title, slug, excerpt, categories, status: 'draft' })`, `savePost()`. Tags through `wp.apiFetch('/wp/v2/tags')`. With Yoast: `setFocusKeyword`, `updateData({ title, description })`, then save.
- Read back through `/wp/v2/posts/{id}?context=edit` and open the preview. Give the author the edit link.
- Never retype an image as base64 in a tool call: it corrupts the file. Hand files to the browser with the methods of blueprint/references/tool-methods.md.

## Image

Follow the brand's visual rules. Options: a frame of the video, retouched, on the brand's background (continuity from video to blog); a reusable series layout with a diagram that carries the thesis (statur-codex-diagram); a public-domain artwork tied to the topic, credited. Always write the alt text. The skill writes the retouch prompt; it never alters a real face.

## Improvement loop

After each essay, add a line to the journal in the context file: date, video, what the author changed before publishing, the lesson. A lesson that holds for any author comes back here in generic words.

## Rules

- Drafts only: the author publishes.
- No passwords, no accounts: the author signs in.
- No promised views or results.
- No invented numbers, quotes or anecdotes.
- Respect each platform's terms and the clients' confidentiality.
