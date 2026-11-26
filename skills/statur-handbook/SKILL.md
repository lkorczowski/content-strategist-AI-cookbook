---
name: statur-handbook
description: Build or update a handbook (a recipe book the reader executes) or a dossier (a sourced investigation that ends in a playbook) on a website, with its AI layer, the "Ask your AI" bar, a ready prompt per chapter, a markdown twin for AI engines, an llms.txt line and companion skills on GitHub. Use when someone asks to write a handbook, playbook, guide or dossier page, to add an AI layer to an existing guide, or to publish the skills that go with a page.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/playbooks/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Handbook with an AI layer

A handbook is a recipe book the reader executes. Each handbook has a twin for AI: the same method written as skills and kept up to date on GitHub, plus a button that hands the page to the reader's own assistant.

## Context: what this skill loads, and when

| File | Where | Read it |
|---|---|---|
| `kb/context/statur-handbook.md` | the author's private repo or project documents | At the start of every run, when it exists |
| The brand file it names (voice, proof table, visual rules) | same place | Steps 2, 7 and 8 |

The context file holds the site's components and registry, the skills repository and its checks, the second-language edition, the visual checklist, the pre-push checks and the journal of past pages. No context file: build the page with the site's own components and say which parts of the AI layer are missing.

## 1. Pick the format

- Handbook: an actionable method (steps, routines, rules). No client case data in the body.
- Dossier: a sourced investigation of a phenomenon, with third-party cases and numbers, ending in a playbook.
- Essay: the story and the theory, on the author's personal site (statur-video-to-essay). Named client cases live there, with the client's consent and checked numbers.
- One topic often gives all three: the essay tells, the dossier proves, the handbook makes the reader do it. Each links to the others.

## 2. Page structure

Benchmarked on Shape Up, Julian Shapiro's guides, the GitLab handbook, Mintlify docs and coreyhaines31/marketingskills (2026-10-23).
1. Hero: concrete result + audience. Titles with statur-hook-stacking.
2. "Ask your AI" bar.
3. TL;DR.
4. The method on one screen: one diagram (statur-codex-diagram) or one table, then the list of recipes with time and frequency.
5. The recipes or chapters.
6. Skills block, honest expectations, link to the essay, FAQ (3 to 5), version footer, call to action.

## 3. A recipe

In this order, readable in three minutes on a phone:
- Title = verb + result, then a quick card (time, frequency).
- The rule in one sentence, boxed.
- What you need (3 to 5 bullets), when useful.
- Numbered steps, one action each. For a video, cut by time segment (0-2 s, 2-10 s...).
- Why: 1 to 3 sentences, a primary source if a fact is claimed.
- Avoid: 3 bullets at most.
- Today: one action to do today.
- A folded "For your AI" block: a copy-ready prompt with [placeholders], and the companion skill.

## 4. The AI layer

- A registry of pages (slug, title, version, date, change note, skills with one-line descriptions) drives the "Ask your AI" bar, the skills block and the version footer, so a page never lists its skills by hand.
- "Ask your AI" opens the reader's assistant (ChatGPT, Claude, Perplexity) with a prompt that points to the markdown twin of the page.
- The markdown twin (`/slug.md`) is generated at build from the page, never written by hand. The page declares it as an alternate.
- llms.txt: one line per page with its markdown and skills links.
- Each content update: version +0.1, date, change note in the registry and in the skills repository changelog.

## 5. Companion skills

- A companion skill lives only in its public repository: the site links to it, private instances install it, nobody copies it.
- Agent Skills format: `skills/<name>/SKILL.md`, frontmatter limited to name (same as the folder, lowercase and hyphens), description (what and when), license, metadata (author, version, playbook URL, repository). Other fields break some uploaders. Body under 500 lines.
- Each skill reads the company's context file first, and points to the page's markdown twin for detail and sources.
- Rules in every skill: drafts only, no passwords, no promised views or results, no invented numbers.
- A playbook card per page in the repository, an entry in the catalog and in the plugin marketplace.

## 6. A second-language edition

For another audience (local trades, another country): a standalone page in that language, same structure, the brand's visual system, diagram labels translated, an "Ask your AI" bar that points to the translated page. The skills stay in English; the assistant answers in the reader's language.

## 7. Content rules

- Voice, proof and banned phrases: the brand file. No client case in a handbook.
- Every market fact is sourced from a primary source you opened. Say what the source says ("platforms demote watermarked reposts"), never more ("platforms penalize schedulers").
- A fictional first name in examples ("Marc the electrician") until the real person agrees.
- Pick the slug and main keyword by research (autocomplete, results page) before building. The practical page takes the how-to query, the essay the opinion query; the essay's term appears once in the dossier body, linked to the essay, never in a title or an H2.
- Vendor numbers: labelled self-reported, recalculated (cost per post, cost per 1,000 views at a given threshold), compared with a sourced paid benchmark.
- When a page reuses a third party's structure, the credit names each element reused.

## 8. Checks before push

1. Independent fact-check: every URL opened, every number against its source, style rules, tone toward named people.
2. The site's SEO and AI-search gate if it has one.
3. Build: pages and markdown twins generated; check at 1280 and 390 px for overflow; "For your AI" blocks present.
4. "Ask your AI" test bench when the prompt changes or a new page ships: incognito or temporary chats in at least two assistants, fixed questions, no answer with a number absent from the page.
5. Visual checklist of the brand.
6. statur-humanizer on the first draft, then on the built page: one opening (no subtitle, TL;DR and table that say the same thing), the copy-prompt and install command once per page, FAQ answers in one or two sentences, no number repeated more than twice.
7. Every link to GitHub answers before the page ships.

## 9. Distribution

Once live, the page follows the usual flow: essay (statur-video-to-essay), newsletter (statur-newsletter-essay), carousel and posts, X posts and Article (statur-x-viral-post-ghostwriter). This skill does not redefine those steps.

## Rules

- Drafts only: pages ship through a branch and a pull request merged by a person.
- No passwords, no accounts.
- No promised views or results.
- No invented numbers: every figure comes from the author's data or a source they can open.
- Respect each platform's terms and the clients' confidentiality.
