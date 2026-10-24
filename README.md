# Content Strategist AI Cookbook

Open-source AI skills for founder-led short-form content, one set per playbook, by Dr. Louis Korczowski, short-form content strategist for SaaS and AI founders (PhD in machine learning and neuroscience).

Each playbook has two versions. The human version is a page on [statur.co](https://statur.co/playbooks/) that you read and apply. The AI version is here: skills in the open [Agent Skills](https://agentskills.io) format that your assistant runs with you, step by step. The theory behind each method lives in essays on [louis-korczowski.org](https://louis-korczowski.org/ideas).

The repository also contains a [blueprint](blueprint/) to build a private AI content operating system inside a company: knowledge base, routines, state and a human annotation loop. It is the public version of the system I run my own consultancy on.

## Catalog

| Playbook | What it does | Skills |
|---|---|---|
| [The Content Testing Loop](https://statur.co/content-testing-loop/) | Make every short video teach the next one: video log, 7-day rule, passage-by-passage post-mortems, KEEP / CHANGE / CUT edits, format review, monthly lessons ledger. | [video-post-mortem](skills/video-post-mortem/), [format-dice-review](skills/format-dice-review/), [content-learning-session](skills/content-learning-session/) |
| [STATUR clipping](https://statur.co/clipping/) | Turn lives, webinars, long YouTube videos or a Google Drive folder into ready-to-post vertical clips, in French or English: local transcription, clip plan, edit with captions and a moving watermark, quality check, review page with timecoded notes. | [statur-clipping](skills/statur-clipping/), [clip-plan](skills/clip-plan/), [clip-edit](skills/clip-edit/), [clip-review](skills/clip-review/) |
| [The Creative-Led Growth Handbook](https://statur.co/creative-led-growth/) | One primary channel, one hour of founder time a day for five to ten pieces, packaging, share rate first. | [creative-led-growth-coach](skills/creative-led-growth-coach/) |
| [Performance creator programs](https://statur.co/creator-programs/) | Pay UGC creators on performance with a retainer floor: platforms, six steps, eight pitfalls. | [performance-creator-program](skills/performance-creator-program/) |
| [The X launch playbook](https://statur.co/x-launch-playbook/) | A launch week on X judged on business numbers, without renting your reputation. | [x-launch-week](skills/x-launch-week/) |
| [The One-Hour Video Handbook for Tradespeople](https://statur.co/tradespeople-video-handbook/) | One video per job, a five-minute edit, and an AI morning routine that leaves drafts. | [trades-video-coach](skills/trades-video-coach/), [trades-ai-setup](skills/trades-ai-setup/), [trades-morning-routine](skills/trades-morning-routine/), [trades-admin-process](skills/trades-admin-process/) |
| [Comment section strategy](https://statur.co/blog/comment-section-strategy-founders/) | Five comment traps that spread an idea, the line with engagement bait, the demo trick, disclosed founder comments. | [comment-section-coach](skills/comment-section-coach/) |
| [Organic winners as ads](https://statur.co/blog/organic-winners-cheaper-ads/) | Turn proven organic videos into ads with minimal edits and test them against the current best ad. | [organic-to-paid](skills/organic-to-paid/) |
| The Format Library (page coming soon) | Twelve short-form formats for founders and the 48-hour reading rule. | [format-library-coach](skills/format-library-coach/) |
| [Blueprint: AI content OS](blueprint/) | The private half: knowledge base, routines, skills registry, annotation loop. | [content-os-setup](skills/content-os-setup/) |

Playbook cards with links and versions: [playbooks/](playbooks/). What comes next: [docs/ROADMAP.md](docs/ROADMAP.md).

## Install

Pick the way your assistant works.

**Claude (claude.ai, desktop and mobile).** Upload a skill as a zip in the Skills section of Claude's settings (code execution must be on). The zip contains one folder, named like the skill, with SKILL.md inside. Get it from the [releases](https://github.com/lkorczowski/content-strategist-AI-cookbook/releases) page, or download this repository (Code > Download ZIP) and zip the skill folder you want.

**Claude Code.** Add this repository as a plugin marketplace, then install the playbook you need:

```
/plugin marketplace add lkorczowski/content-strategist-AI-cookbook
/plugin install content-testing-loop@content-strategist-ai-cookbook
```

**Any agent that reads Agent Skills** (Claude Code, OpenAI Codex, Cursor, GitHub Copilot, Gemini CLI and others), with the skills CLI:

```
npx skills add lkorczowski/content-strategist-AI-cookbook --skill video-post-mortem
```

Or copy a skill folder into `.agents/skills/` (shared path), `.claude/skills/` (Claude Code) or `~/.gemini/skills/` (Gemini CLI).

**Any chat assistant (ChatGPT, Gemini, Perplexity).** Open the skill's SKILL.md, paste it into the chat or into custom instructions, and ask the assistant to follow it. Each statur.co page also has an "Ask your AI" bar and a prompt per chapter.

**Your company context.** Every skill first looks for a company context file (kb/01_BRAND.md from the [blueprint](blueprint/), or .agents/product-marketing.md) and only asks for what is missing. Write it once, every skill uses it.

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
- docs/: [architecture and responsibilities](docs/ARCHITECTURE.md), [roadmap](docs/ROADMAP.md).

## Author

Dr. Louis Korczowski, short-form content strategist for SaaS and AI founders. PhD in machine learning and neuroscience, ten years of brain-computer interface research, former Head of Growth and board member at Pixminds. Methods at [statur.co](https://statur.co), essays at [louis-korczowski.org](https://louis-korczowski.org).

Issues and suggestions are welcome. License: [MIT](LICENSE).
