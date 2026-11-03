# Rules for Claude Code and other agents working in this repository

CLAUDE.md imports this file (@AGENTS.md): one source for the rules of this repo, read by Claude Code, Codex and Cursor.

This repository is PUBLIC. Everything committed here is readable by anyone, forever (git history included).

## What this repo is

The public method layer of Dr. Louis Korczowski's short-form content work: skills in the Agent Skills format, playbook cards that point to the human-readable pages on statur.co, and a blueprint to build a private AI content operating system in any company. Architecture and responsibilities: docs/ARCHITECTURE.md. Roadmap: docs/ROADMAP.md.

## Never commit

- Client names, client numbers, prices, quotes, contracts, revenue, salaries.
- Personal data of anyone: emails, phone numbers, addresses, family details.
- Internal ids: Airtable bases, Google Drive or Sheet ids, CRM location ids, API keys, tokens.
- Paths of a private machine (/Users/...), private repo paths, private routine prompts.
- Text copied from a third party (prompts shown in someone's video, book passages). Write the method in your own words and credit the idea with a link.

Before every push: `python3 scripts/check_skills.py` and `python3 scripts/leak_scan.py --denylist <path to the private denylist>`. Both must report zero problems. Install the pre-push hook once per clone: `COOKBOOK_DENYLIST=<path> bash scripts/install_hooks.sh`. CI runs the skill checks and the generic scan on every push.

## Git

- GitHub main is the source of truth. Agents work on a branch (agent/<machine>/<yyyymmdd>-<task>) and open a pull request; nobody pushes to main directly. A private instance may add its own rule for machines and clones.

## One source of truth per artifact

- A skill lives only in skills/<name>/. Never copy it into a site or into a private repo: link to it, or install it from here.
- The long human-readable text of a playbook lives on its web page (statur.co). playbooks/<slug>.md is a short card: summary, links, skills, version. Never paste the full page here.
- Private context (brand voice, proofs, prices, client data, routine state) lives in the private instance repo of each company. A private skill may extend a public one by name; it never forks it.

## Conventions

- Skill folder name = frontmatter name, lowercase and hyphens, always prefixed statur-. Main skill of a playbook: statur-<playbook>. Sub-skill: statur-<object>-<action>. Plugins: statur-<playbook> or statur-<role>. Frontmatter: name, description (what it does and when to use it), license MIT, metadata author, version, playbook URL.
- Every skill ends with a "## Rules" section: drafts only, no passwords, no promised views or results, no invented numbers, respect platform terms.
- English, short sentences, no em dash, no emoji.
- Any change to a skill: bump metadata.version, add a CHANGELOG.md line, update the playbook card and, if the version changed, the HANDBOOKS registry on statur.co (src/lib/hbkit.ts in the site repo).
- New skill: add it to README.md (catalog), to its playbook card and to .claude-plugin/marketplace.json.
