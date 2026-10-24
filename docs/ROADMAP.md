# Roadmap

Version 1.0, 2026-10-24. Each item names its deliverable and the check that says it is done, so a coding agent can pick it up. Order = priority.

## v1.0 · shipped 2026-10-24

- 14 skills: the Content Testing Loop (3), companions of the four pages already on statur.co (7), two statur.co notes (2), the Format Library (1), the content OS blueprint (1).
- Blueprint of a private AI content OS with templates (knowledge base, project instructions, routine prompt, feedback file, skills registry, git sync for macOS) and the human annotation loop.
- Plugin marketplace file (one plugin per playbook), checks (skill format, private data scan), zip builder.

## v1.1 · shipped 2026-10-24

- STATUR clipping playbook: statur-clipping, clip-plan, clip-edit and clip-review, with scripts, references and the review page template.

## v1.1 · next

| Item | Deliverable | Done when |
|---|---|---|
| First GitHub release | v1.0.0 release with one zip per skill (scripts/build_zips.py) | Every zip uploads in Claude and the skill triggers on a test prompt |
| Repository settings | Description, topics, website link, social preview image (1280x640) | Visible on the repository page |
| Format Library page | Page live on statur.co, card and skill URLs resolve | No 404 from the card or the skill |
| Short-video storytelling playbook | Skills short-video-author-analysis and short-story-replication, guide page on statur.co | Skills pass checks; no third-party quote or private link; acquisition works from transcripts the user provides or exports |
| Long-video storytelling playbook | Skills video-story-analysis and story-replication with their scripts and a small sample case | Same, plus scripts run on the sample in the skill folder |
| Hook stacking | Generic skill hook-stacking: titles, hooks and subject lines with at least three hooks, invented examples | Passes checks; no real client in examples |
| Landing page audit | Generic page audit for founder sites: hero, conversion, navigation, SEO and AI search, copy that sounds generated | Passes checks; public references only |
| Video to essay | Turn a talk, a rant or a video transcript into an independent essay with a fact-check step | Passes checks; independence test included |
| Newsletter essay | Adapt an essay or a handbook into a newsletter issue, with an independent review | Passes checks |
| Plain founder voice | One shared list of AI writing tells and banned constructions, used by every writing skill | Other writing skills name it |

## v1.2

| Item | Deliverable |
|---|---|
| Handbook with an AI layer | Generic skill to publish a handbook page with an Ask your AI bar, per-chapter prompts, a markdown twin and companion skills |
| Strategist hiring scorecard | Skill for the guide on choosing a short-form content strategist |
| Authority before the crash | Skill from the essay on AI SaaS renewals: a 90-day authority plan for AI founders |
| Local search for trades | English skill for a Google Business Profile routine (posts, reviews, keywords) |
| Blueprint: browser methods | Reference of reliable methods for spreadsheets, documents and meeting transcripts through a browser, within each tool's terms |
| Clipping 1.1 | Cut boundaries snapped to the quietest 10 ms near each word edge (word timestamps sit on an 80 ms grid), a crop per speaker for split screens, an audiogram style for audio-only sources |
| Clipping sample case | A short public sample recording in skills/statur-clipping/ with its expected plan and spec, so the chain can be tested end to end in minutes |

## v2

| Item | Deliverable |
|---|---|
| Evals | evals/ per skill: three test prompts, expected behaviors, and a runner |
| Single registry | statur.co reads skill names, descriptions and versions from this repository at build time, pinned to a tag, so the list lives in one place |
| Playbook prose here | If playbooks get contributors or translations, move the page text into playbooks/<slug>/ and render it on statur.co at build |
| Routine library | Blueprint templates for a daily inbox brief, a CRM note sync, an evening meeting recap and a weekly backup, each with its state file and stop rules |
| Data schemas | CSV and Airtable schemas for the video log, snapshots and lessons ledger, with an import guide |
| Client template | A GitHub template repository generated from blueprint/templates ("Use this template") |
| French editions | French versions of the trades handbook skills where the French site publishes the page |

## How to add an item

Open an issue with the deliverable and the check. When the item ships: CHANGELOG.md line, README catalog, playbook card, marketplace.json.
