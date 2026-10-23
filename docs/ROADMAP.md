# Roadmap

Version 1.0, 2026-10-24. Each item names its deliverable and the check that says it is done, so a coding agent can pick it up. Order = priority.

## v1.0 · shipped 2026-10-24

- 12 skills: the Content Testing Loop (3), companions of the four pages already on statur.co (7), the Format Library (1), the content OS blueprint (1).
- Blueprint of a private AI content OS with templates (knowledge base, routine prompt, feedback file, skills registry, git sync for macOS).
- Plugin marketplace file (one plugin per playbook), checks (skill format, private data scan), zip builder.

## v1.1 · next

| Item | Deliverable | Done when |
|---|---|---|
| First GitHub release | v1.0.0 release with one zip per skill (scripts/build_zips.py) | Every zip uploads in claude.ai and the skill triggers on a test prompt |
| Repository settings | Description, topics (agent-skills, claude-skills, content-strategy, short-form-video, tiktok, founder-led-marketing), website link, social preview image | Visible on the repository page |
| Format Library page | Page live on statur.co, card and skill URLs resolve | No 404 from the card or the skill |
| Short-video storytelling playbook | Skills short-video-author-analysis and short-story-replication, page on statur.co | Skills pass checks; acquisition step works from transcripts the user provides |
| Long-video storytelling playbook | Skills video-story-analysis and story-replication with their scripts, page on statur.co | Same, plus scripts run on the sample in the skill folder |
| Hook stacking | Generic skill hook-stacking (titles, hooks, subject lines with at least three hooks) | Passes checks; no brand-specific examples |
| Video to essay | Generic skill that turns a talk, a rant or a video transcript into an independent essay | Passes checks; independence test and fact-check steps included |

## v1.2

| Item | Deliverable |
|---|---|
| Founder site audit | Generic version of a page audit for founder sites (UX, conversion, SEO, AI search, copy that sounds generated) |
| Strategist hiring scorecard | Skill for the guide on choosing a short-form content strategist |
| Newsletter adaptation | Skill that adapts an essay or a handbook into a newsletter issue |
| Local search for trades | English skill for a Google Business Profile routine (posts, reviews, keywords) |

## v2

| Item | Deliverable |
|---|---|
| Evals | evals/ per skill: three test prompts, expected behaviors, and a runner |
| CI | GitHub Action that runs check_skills.py and the generic leak scan on every pull request |
| Routine library | Blueprint templates for a daily inbox brief, a CRM note sync, an evening meeting recap and a weekly backup, each with its state file and stop rules |
| Data schemas | CSV and Airtable schemas for the video log, snapshots and lessons ledger, with an import guide |
| Client template | A GitHub template repository generated from blueprint/templates ("Use this template") |
| French editions | French versions of the trades handbook skills where the French site publishes the page |

## How to add an item

Open an issue with the deliverable and the check. When the item ships: CHANGELOG.md line, README catalog, playbook card, marketplace.json.
