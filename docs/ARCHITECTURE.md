# Architecture and responsibilities

Version 1.0, 2026-10-24. Read this before changing the structure of this repository, of a site that links to it, or of a private instance built from it. Written for humans and for coding agents (Claude Code, Codex, Cursor).

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
| Format cards (one file per format) and their generated index | this repo, skills/format-library-coach/library/ | the skill, statur.co /format-library (rendered at build), private instances | edited in the generated README.md or index files, or copied into a site |
| Playbook card (summary, links, skills list) | this repo, playbooks/<slug>.md | README catalog, Claude Code marketplace | containing client data |
| Blueprint (structure of a private instance) | this repo, blueprint/ | content-os-setup skill, every private instance | containing a real company's data |
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
| Where does a library of entries live (the Format Library)? (2026-10-25, to validate) | Inside its skill folder: skills/format-library-coach/library/, one card per entry, index generated by scripts/library.py | A library is data the skill reads, so it travels with the skill zip and the plugin. One file per entry makes pull requests and reviews small. statur.co renders the page from library/index.json at build time and never holds a copy. Private entries (client examples, numbers) live in the private instance with P-ids. |

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

## 8. Checks before every push

1. `python3 scripts/check_skills.py` reports zero problems.
2. `python3 scripts/leak_scan.py --denylist <private denylist>` reports zero hits.
3. Every new skill appears in README.md, in its playbook card and in .claude-plugin/marketplace.json.
4. CHANGELOG.md has a line for the change.
