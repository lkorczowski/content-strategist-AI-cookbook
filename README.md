# Content Strategist AI Cookbook

Open-source AI skills for founder-led short-form content, one set per playbook, by Dr. Louis Korczowski, short-form content strategist for SaaS and AI founders (PhD in machine learning and neuroscience).

Each playbook has two versions. The human version is a page on [statur.co](https://statur.co/playbooks/) that you read and apply. The AI version is here: skills in the open [Agent Skills](https://agentskills.io) format that your assistant runs with you, step by step. The theory behind each method lives in essays on [louis-korczowski.org](https://louis-korczowski.org/ideas).

The repository also contains a [blueprint](blueprint/) to build a private AI content operating system inside a company: knowledge base, routines, state and a human annotation loop. It is the public version of the system I run my own consultancy on.

## Catalog

| Playbook | What it does | Skills |
|---|---|---|
| [How Ideas Go Viral on Social Media](https://statur.co/how-ideas-go-viral/) | Map the ideas of an online controversy from its most viewed posts: implied ideas, contested concepts, camps, third parties, quote duels and an Elo rating per idea. | [statur-idea-war-map](skills/statur-idea-war-map/) |
| [The Content Testing Loop](https://statur.co/content-testing-loop/) | Make every short video teach the next one: video log, 7-day rule, passage-by-passage post-mortems, KEEP / CHANGE / CUT edits, format review, monthly lessons ledger. | [statur-video-post-mortem](skills/statur-video-post-mortem/), [statur-format-review](skills/statur-format-review/), [statur-content-learning](skills/statur-content-learning/) |
| [STATUR social analytics](https://statur.co/blog/own-your-social-media-analytics/) | Own your short-form analytics without a paid tool: views, retention, audience and daily stats in plain files in your repo, a watchlist, proof screenshots, SQL your AI can run. Feeds the Content Testing Loop, the Format Library, clipping and scripts. | [statur-social-analytics](skills/statur-social-analytics/) |
| Video Script Structure (page coming soon) | Script founder videos people finish, from 2 minutes to 40: map any video sentence by sentence on nine tiers, name a creator's templates across twenty short videos, then write your own script on the same beats and check parity before you film. | [statur-story-analysis](skills/statur-story-analysis/), [statur-story-replication](skills/statur-story-replication/), [statur-author-analysis](skills/statur-author-analysis/), [statur-short-story-replication](skills/statur-short-story-replication/) |
| [STATUR clipping](https://statur.co/clipping/) | Turn lives, webinars, long YouTube videos or a Google Drive folder into ready-to-post vertical clips, in French or English: local transcription, clip plan, edit with captions and a moving watermark, quality check, review page with timecoded notes. | [statur-clipping](skills/statur-clipping/), [statur-clip-plan](skills/statur-clip-plan/), [statur-clip-edit](skills/statur-clip-edit/), [statur-clip-review](skills/statur-clip-review/) |
| [The Creative-Led Growth Handbook](https://statur.co/creative-led-growth/) | One primary channel, one hour of founder time a day for five to ten pieces, packaging, share rate first. | [statur-creative-led-growth](skills/statur-creative-led-growth/) |
| [Performance creator programs](https://statur.co/creator-programs/) | Pay UGC creators on performance with a retainer floor: platforms, six steps, eight pitfalls. | [statur-creator-program](skills/statur-creator-program/) |
| [The X launch playbook](https://statur.co/x-launch-playbook/) | A launch week on X judged on business numbers, without renting your reputation. | [statur-x-launch](skills/statur-x-launch/) |
| [The X Ghostwriter Handbook](https://statur.co/x-ghostwriter/) | Grow on X from zero with an AI that drafts in your voice: refusal list and voice mix from your own posts, pillars from buyer beliefs, hook forensics, X's published ranking weights, a reply routine for cold accounts, a 30-day goal and scorecard. | [statur-x-viral-post-ghostwriter](skills/statur-x-viral-post-ghostwriter/), [statur-brand-dna-audit](skills/statur-brand-dna-audit/), [statur-hook-forensics](skills/statur-hook-forensics/) |
| [The One-Hour Video Handbook for Tradespeople](https://statur.co/tradespeople-video-handbook/) | One video per job, a five-minute edit, and an AI morning routine that leaves drafts. | [statur-trades-video](skills/statur-trades-video/), [statur-trades-setup](skills/statur-trades-setup/), [statur-trades-morning-routine](skills/statur-trades-morning-routine/), [statur-trades-admin](skills/statur-trades-admin/) |
| [Comment section strategy](https://statur.co/blog/comment-section-strategy-founders/) | Five comment traps that spread an idea, the line with engagement bait, the demo trick, disclosed founder comments. | [statur-comment-section](skills/statur-comment-section/) |
| [Scale Meta ads without cost inflation](https://statur.co/scale-meta-ads/) | The creative strategist handbook: one purchase campaign fed by organic winners, creators paid on results run as partnership ads, offers and statics; live ads sized to the budget, a test lane, weekly and monthly reads. | [statur-meta-ads-scaling](skills/statur-meta-ads-scaling/) |
| [Organic winners as ads](https://statur.co/blog/organic-winners-cheaper-ads/) | Turn proven organic videos into ads with minimal edits and test them against the current best ad. | [statur-organic-to-paid](skills/statur-organic-to-paid/) |
| The Format Library (page coming soon) | Twelve short-form formats for founders and the 48-hour reading rule. | [statur-format-library](skills/statur-format-library/) |
| [Blueprint: AI content OS](blueprint/) | The private half: knowledge base, routines, skills registry, annotation loop. | [statur-content-os-setup](skills/statur-content-os-setup/) |

Playbook cards with links and versions: [playbooks/](playbooks/). What comes next: [docs/ROADMAP.md](docs/ROADMAP.md).

## Install

Pick the way your assistant works.

**Claude (claude.ai, desktop and mobile).** Upload a skill as a zip in the Skills section of Claude's settings (code execution must be on). The zip contains one folder, named like the skill, with SKILL.md inside. Get it from the [releases](https://github.com/lkorczowski/content-strategist-AI-cookbook/releases) page, or download this repository (Code > Download ZIP) and zip the skill folder you want.

**Claude Code.** Add this repository as a plugin marketplace, then install the playbook you need, or a whole role (statur-content-strategist, statur-creative-strategist):

```
/plugin marketplace add lkorczowski/content-strategist-AI-cookbook
/plugin install statur-content-testing-loop@content-strategist-ai-cookbook
```

**Any agent that reads Agent Skills** (Claude Code, OpenAI Codex, Cursor, GitHub Copilot, Gemini CLI and others), with the skills CLI:

```
npx skills add lkorczowski/content-strategist-AI-cookbook --skill statur-video-post-mortem
```

Or copy a skill folder into `.agents/skills/` (shared path), `.claude/skills/` (Claude Code) or `~/.gemini/skills/` (Gemini CLI).

**Any chat assistant (ChatGPT, Gemini, Perplexity).** Open the skill's SKILL.md, paste it into the chat or into custom instructions, and ask the assistant to follow it. Each statur.co page also has an "Ask your AI" bar and a prompt per chapter.

**Your company context.** Every skill first looks for a company context file (kb/01_BRAND.md from the [blueprint](blueprint/), or .agents/product-marketing.md) and only asks for what is missing. Write it once, every skill uses it.

## Naming

Every public skill starts with statur-, the name of the marketing lab that publishes them. One main skill per playbook carries the playbook's name (statur-clipping, statur-social-analytics, statur-format-library, statur-meta-ads-scaling). Sub-skills name the object, then the action (statur-clip-plan, statur-video-post-mortem, statur-format-review). Plugins group skills by playbook (statur-content-testing-loop) or by role (statur-content-strategist, statur-creative-strategist).

A private instance (a company's own knowledge base and skills) extends these skills by name and never copies them. Its own skills use its own prefix. Skills renamed on 2026-10-26 keep a README at their old path that points to the new one: see CHANGELOG v2.0.0.

## Rules every skill follows

- Drafts only: the assistant never sends, publishes, schedules or deletes anything for you.
- No passwords: you sign in yourself, the assistant never asks for one.
- No promised views or results, and no invented numbers: every figure comes from your data or from a source you can open.
- Respect each platform's terms of use.

## How this repository is organized

- skills/: one folder per skill, Agent Skills format (SKILL.md, plus templates/, references/ and scripts/ when the skill needs them).
- playbooks/: short cards that link each page, its markdown version, its essay and its skills. The page on statur.co is the source of truth for the text.
- blueprint/: how to build a private AI content OS, with templates.
- scripts/: checks run before every change (skill format, private data scan) and the zip builder for releases.
- docs/: [architecture and responsibilities](docs/ARCHITECTURE.md) (section 8: which skill does what), [roadmap](docs/ROADMAP.md).

## Author

Dr. Louis Korczowski, short-form content strategist for SaaS and AI founders. PhD in machine learning and neuroscience, ten years of brain-computer interface research, former Head of Growth and board member at Pixminds. Methods at [statur.co](https://statur.co), essays at [louis-korczowski.org](https://louis-korczowski.org).

Issues and suggestions are welcome. License: [MIT](LICENSE).
