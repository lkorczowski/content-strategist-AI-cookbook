# Architecture and responsibilities

Version 2.0, 2026-10-26 (section 8 added; section 0 naming and statur- prefix, cookbook v2.0.0). Read this before changing the structure of this repository, of a site that links to it, or of a private instance built from it. Written for humans and for coding agents (Claude Code, Codex, Cursor).

## 0. Names: the lab and the instances

Public skills are the output of a marketing lab, STATUR: generic methods, tested on real accounts, published here under the statur- prefix. A private instance (Louis's own, or one per client) is where those methods run with a company's tone, ideas, nuances, taste, proofs and data. Its private skills extend public ones by name and carry the instance's own prefix. Running the public skills inside an instance is what builds the instance's knowledge base over time; a lesson that holds across several cases comes back here as a new version of the generic skill, without the company's data.

Naming rules: main skill of a playbook = statur-<playbook>; sub-skill = statur-<object>-<action>; plugin = statur-<playbook> or statur-<role>. Renames of 2026-10-26: CHANGELOG v2.0.0 and scripts/rename_skills.py.

## 1. The system in one picture

```
                    louis-korczowski.org            statur.co                     French site
                    essays: the why                 handbooks: the how            French versions
                         |  "theory behind it"           |  links, prompts, install       |
                         +-------------------------------+--------------------------------+
                                                         |
                                                         v
            PUBLIC   lkorczowski/content-strategist-AI-cookbook   (this repo: method layer)
                     skills/  playbooks/  blueprint/  scripts/  docs/
                                                         |
                          installed by version, never copied (one-way: public -> private)
                                                         v
            PRIVATE  Louis's own instance            PRIVATE  <client>-os (one per client)
                     Louis's instance                               built from blueprint/templates
                     kb, routines, data, private skills             kb, routines, data, private skills
```

Three layers, three jobs:

| Layer | Repository or site | Single responsibility | Audience |
|---|---|---|---|
| Method | this repo | Executable method: skills, playbook cards, blueprint templates, tooling | Anyone's AI assistant, Louis's clients, Louis |
| Surfaces | statur.co, louis-korczowski.org, the French site | Human-readable pages: handbooks (how), essays (why), French versions | Founders, search engines, LLM crawlers |
| Instances | Louis's private instance, one private repo per client | Company-specific knowledge, routines, data and private skills | One company's team and its agents |

## 2. Source of truth for every artifact

One artifact, one owner. Every other place links to the owner and never holds a copy.

| Artifact | Owner (source of truth) | Consumers | Never |
|---|---|---|---|
| Public skill (SKILL.md, templates, scripts) | this repo, skills/<name>/ | statur.co pages (links, install command), clients' assistants, private instances | copied into a site, a zip on a site, or a private repo |
| Handbook or dossier prose | statur.co repo (page source), with its markdown twin /<slug>.md generated at build | playbook card here, AI assistants via the Ask your AI bar and llms.txt | pasted here in full |
| Page version and changelog note | statur.co src/lib/hbkit.ts (HANDBOOKS) | the page footer, the markdown twin | maintained twice: the skill version lives here, the page version lives there |
| Essay (theory, story) | louis-korczowski.org (WordPress) | statur.co "theory behind it" link, playbook card | rewritten on statur.co |
| Playbook card (summary, links, skills list) | this repo, playbooks/<slug>.md | README catalog, Claude Code marketplace | containing client data |
| Blueprint (structure of a private instance) | this repo, blueprint/ | statur-content-os-setup skill, every private instance | containing a real company's data |
| Brand, offer, prices, proofs, voice of Louis | Louis's private instance, kb/01 | Louis's private skills, routines, site copy decisions | appearing in this repo |
| Routines, their prompts and their state | the private instance that runs them | that instance only | published (they contain ids and personal data) |
| Leak denylist (client names, ids, prices) | each private instance | scripts/leak_scan.py --denylist <private path> | committed here |
| Client data, CRM, transcripts, meetings | the private instance | that instance only | anywhere public |

## 3. Who decides what

| Decision | Decider | Where it is written |
|---|---|---|
| A method changes (new rule, new step) | Louis | skill + CHANGELOG.md here, then the page on statur.co |
| A page is published or updated | Louis (GO) | statur.co BUILD-LOG |
| A private skill becomes public | Louis, after the promotion checklist (blueprint/README.md) | CHANGELOG.md here + skills registry of the private repo |
| A client adopts a public skill | the client | the client's kb/04_OPERATIONS.md (skill, version) |
| Repository structure | Louis, with this document updated in the same commit | this file |

## 4. Flows

1. New method. Louis records an idea or a rant. The essay goes to louis-korczowski.org (skill tiktok-rant-to-blog, private). The handbook goes to statur.co (skill statur-handbook, private). The companion skills go here. The page links to the skills; the skills link to the page.
2. Improving a skill. Change it here first, bump metadata.version, add a CHANGELOG.md line, update the playbook card, then bump the page version on statur.co if the method on the page changed.
3. Using a skill privately. A private instance never edits a public skill. It either installs it (claude.ai zip from a release, Claude Code plugin pinned with #tag, or `npx skills add ... --copy` into its own repo, updated on purpose with `npx skills update`), and it supplies the company context through its kb/01 file, which every public skill reads first. A private need that the context file cannot express goes into a separately named private skill that calls the public one by name.
4. Promoting a private skill. Follow the checklist in blueprint/README.md. The public version replaces the generic part of the private one; the private repo keeps only its overlay.
5. Working with a client. Create the client's private repo from blueprint/templates, install the public skills they need, fill their kb with them. Their data never comes back here. A generic improvement found with a client is promoted like any private skill.

## 5. Why a repository and no gists

- Skills are folders (SKILL.md, templates, scripts). Gists are flat lists of files.
- Install tools expect a repository: Claude Code plugin marketplaces, the skills CLI, release zips for claude.ai.
- One repository gives one changelog, one license, issues and pull requests, and one place for crawlers and LLMs to cite.
- Sites link to files here and render their own prompt boxes. No gist is needed for embedding, and a gist would become a second copy to keep in sync.

## 6. Decisions behind this design (2026-10-24)

| Question | Decision | Why |
|---|---|---|
| Repository or gists? | One public repository, no gists | Skills are folders; gists hold one flat level of files and cannot carry .claude-plugin/. Releases, issues and one changelog live in a repository. |
| Where does the playbook text live? | On statur.co, with a generated markdown twin | One owner for the prose. The repository keeps short cards. If playbooks get contributors or translations, move the prose here and render it at build (roadmap v2). |
| How do pages show skills? | Links, install commands and per-chapter prompts | No copy to keep in sync. The page owns its prompts; the skill owns the full method. |
| How does a private instance customize a skill? | Company context file + optional private skill by another name | No fork, no drift. Matches the context-file pattern used by the largest public marketing skills repositories. |
| Frontmatter fields | name, description, license, metadata only | Extra fields break claude.ai uploads. |
| License | MIT for everything | Ecosystem norm for skills; the cards are short. Page prose stays on statur.co under its own terms. |
| Leak guard | scripts/leak_scan.py with a private denylist passed as an argument | Zero dependency, runs anywhere. gitleaks with a custom rule file kept outside the repo is an equivalent option. |

## 7. Layout

```
README.md                    catalog: playbooks -> skills, install, author
CLAUDE.md                    rules for agents working here (public repo: never commit private data)
CHANGELOG.md                 one line per change, newest first
LICENSE                      MIT
.claude-plugin/marketplace.json   one plugin per playbook, pointing at skills/
playbooks/<slug>.md          short cards: summary, page URL, markdown URL, essay URL, skills
skills/<name>/SKILL.md       Agent Skills format, plus templates/ or references/ when needed
blueprint/README.md          how to build a private AI content OS
blueprint/templates/         skeleton of a private instance (kb, routines, skills registry, ops)
scripts/check_skills.py      frontmatter and style checks
scripts/leak_scan.py         private data scan, with a private denylist passed as an argument
scripts/build_zips.py        one zip per skill for claude.ai upload and GitHub releases
docs/ARCHITECTURE.md         this file
docs/ROADMAP.md              what comes next
```

## 8. Skill responsibilities: one job per skill

The skills form one loop. Each step has one owner; the next step reads what the previous one wrote instead of asking the user again.

```
  MEASURE                     DIAGNOSE                    DECIDE                       MAKE
  statur-social-analytics ->  statur-video-post-mortem -> statur-format-review     ->  statur-format-library (pick, script)
  (collect, store,            (one video)                 (keep, change, drop)         storytelling skills (write)
   query, proof)                                          statur-content-learning      statur-clipping (cut long recordings)
                                                          (monthly)                    statur-organic-to-paid (winners into ads)
        ^                                                                                      |
        +---------------------------------------- published videos ----------------------------+
```

| Step | Skill | Single responsibility | Reads | Writes | Never |
|---|---|---|---|---|---|
| Measure | statur-social-analytics | Collect metrics of owned, client and watched accounts; store every reading; answer data questions; keep proof screenshots | platforms (API, export, the user's own analytics screen, public pages) | accounts.csv, raw/, analytics.db, TOTALS.md, proof/ | decides what to post |
| Diagnose | statur-video-post-mortem | Explain one video passage by passage, KEEP / CHANGE / CUT | video_log, retention | post-mortem notes, test plan | collects data, judges a format |
| Decide | statur-format-review | Keep, change one variable or drop each format on mature data | dice table, video_log | format decisions, next production plan | scripts videos |
| Decide | statur-content-learning | Monthly ledger of lessons with evidence, next three tests | video_log (whole history), post-mortems | lessons ledger, coaching brief | judges a single video |
| Make | statur-format-library | Find, plan and script formats; name the format of a video | the library, winners | formats.csv lines, scripts | keeps or kills a format (that is statur-format-review) |
| Make | statur-story-analysis, statur-author-analysis, statur-story-replication, statur-short-story-replication | Map how a winning video holds attention, then write a script on the same beats | winners (own or watched) | story sheets, scripts | collect metrics |
| Make | statur-clipping, statur-clip-plan, statur-clip-edit, statur-clip-review | Turn a long recording into clips | the account's winning formats and hooks | clips, specs, review pages | collect metrics |
| Make | statur-organic-to-paid | Move organic winners into ads and test them | winners with saves and shares | ad test plan | collect metrics |
| Decide (paid) | statur-meta-ads-scaling | Diagnose a Meta account and run it: structure, live ads per budget, test lane, partnership share, offers and statics, weekly and monthly reads | ad exports or a read-only Meta connector, store numbers | diagnosis, structure plan, test plan, weekly and monthly tables | launch or edit ads, recruit creators (statur-creator-program), pick organic winners (statur-organic-to-paid) |
| Define | statur-brand-dna-audit | Write and audit the brand DNA from evidence: refusal list, voice mix, pillars from buyer beliefs, one reader, one outcome, proof bank | the founder's posts, transcripts, offer, buyer questions | the brand DNA sections of kb/01_BRAND.md (proposed, the founder validates) | drafts posts, collects metrics |
| Study | statur-hook-forensics | Read viral text posts and X Articles case by case and keep the hook formula file | public posts with their counts | case files, formula table | drafts the founder's posts, maps a controversy (statur-idea-war-map) |
| Make (X) | statur-x-viral-post-ghostwriter | Draft and score X posts, replies, quotes and Articles; weekly mix; cold-start mode; 30-day goal and scorecard; owner of X ranking facts (references/x-ranker.md) | brand DNA, formula file, post_log | drafts with a score line, reply targets, scorecard | posts or replies for the user, collects metrics, plans a launch week (statur-x-launch) |
| Launch (X) | statur-x-launch | One launch week on X judged on business numbers | launch asset, champions, offers | launch plan, contract review | runs the weekly X rhythm after day 14 (statur-x-viral-post-ghostwriter) |

Short names used on statur.co and in talks: "format library" = statur-format-library; "storytelling OS" = the four Video Script Structure skills; "clipping" = the four STATUR clipping skills; "social analytics" = statur-social-analytics.

Shared definitions (one owner each, used by every skill):

| Definition | Value | Owner |
|---|---|---|
| Post log columns (X, LinkedIn) | the `post_log` view of statur-social-analytics: posts joined with post_labels.csv (pillar, voice mode, intent, formula) | statur-social-analytics (references/schema.md) |
| X ranking weights | references/x-ranker.md, dated, primary source only | statur-x-viral-post-ghostwriter |
| Brand DNA (refusal list, voice mix, pillars, one reader, one outcome, proof bank) | sections 03, 07 and 08 of kb/01_BRAND.md | statur-brand-dna-audit |
| Video log columns | the `video_log` view of statur-social-analytics; templates/video-log.csv in statur-video-post-mortem is the manual fallback with the same columns | statur-social-analytics (references/schema.md) |
| Early signal | a reading at 48 hours, used to boost, reply in comments or test an ad; never a verdict | statur-format-review |
| Mature data | at least 7 days live and 1,000 views (or the account's usual floor if smaller); the only data a verdict uses | statur-format-review |
| Viral line | 100,000 views at day 7 by default, set per account | statur-social-analytics |

Known overlap to remove: statur-format-library 1.0 also asks to decide after 48 hours which formats to keep. Version 2.0 (pull request #3) drops it; until it merges, statur-format-review is the decider.

## 9. Checks before every push

1. `python3 scripts/check_skills.py` reports zero problems.
2. `python3 scripts/leak_scan.py --denylist <private denylist>` reports zero hits.
3. Every new skill appears in README.md, in its playbook card and in .claude-plugin/marketplace.json.
4. CHANGELOG.md has a line for the change.
