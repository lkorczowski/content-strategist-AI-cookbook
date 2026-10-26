# Blueprint: build a private AI content operating system in your company

This blueprint is how I set up an AI copilot for marketing and content inside a company. It is the public, generic version of the system I run my own consultancy on. The method lives here, in public. Your company's knowledge, data and routines live in a private repository that you own.

Author: Dr. Louis Korczowski, short-form content strategist (https://statur.co, https://louis-korczowski.org).

## The three layers

```
PUBLIC  method     this cookbook: skills, playbooks, blueprint, scripts       (shared, versioned)
PUBLIC  surfaces   your website pages, essays, handbooks                       (human readers)
PRIVATE instance   your company repo: knowledge base, routines, data, skills   (your team only)
```

- The method is generic. It never contains a client, a price or an id. You install it, you never fork it.
- The instance is specific. It holds what makes your company yours: brand voice, offers, proofs, customers, routine state.
- Information flows one way, from public to private. A private improvement goes back to the public layer only after it has been made generic (see "Promote a private skill" below).

## What the private instance contains

```
<company>-os/                     private git repository
  README.md                       one paragraph: what this repo is, where to start
  CLAUDE.md                       rules for any agent working here (start, end, guardrails)
  kb/                             knowledge base, one subject per file
    00_INDEX.md                   who is the source of truth for what (read first)
    01_BRAND.md                   positioning, audience, offer, proofs with canonical numbers, voice, visuals
    02_SALES-PLAYBOOK.md          routing of inbound requests, email templates, CRM note format
    03_ROUTINES.md                scheduled tasks, their scope, and lessons learned on tools
    04_OPERATIONS.md              tools, people and roles, index of external resources
    05_TODO.md                    decisions to take and tasks for humans
  routines/
    prompts/<routine>.md          one file per scheduled task: header (schedule, model, folder) + prompt
    data/                         small state files (config, rules, state, feedback); personal data gitignored
    .secrets/                     gitignored, never read by the agent
  skills/                         private skills (brand voice, internal processes) + README.md registry
  content/                        drafts and research for your public pages
  clients/                        one folder per client or project, if you are an agency
  archive/<date>-<subject>/       everything replaced, never deleted in place
```

Templates for every file above are in templates/, plus templates/PROJECT-INSTRUCTIONS.md for the assistant's project instructions. The shared memory between routine runs is described in [annotation-loop.md](annotation-loop.md).

## Seven rules that keep the system healthy

1. One fact, one home. Every subject has exactly one source of truth, listed in kb/00_INDEX.md. Everything else links to it.
2. Fresh copy first. Every session and every routine starts from the latest version of the private repo (git pull without error, or a fresh clone) and pushes its changes before it ends.
3. One routine, one scope. A scheduled task owns one perimeter (inbox, CRM, meetings, backup). Two routines never write to the same system.
4. Drafts only. The agent prepares emails, posts and articles as drafts. A human sends and publishes. Passwords, payments and account creation stay with humans.
5. A human annotation loop. Each routine leaves a short digest. The human annotates it (done, do this, ignore that) and the next run reads the annotations first. That is the shared memory between runs.
6. Archive what is outdated. A document that is out of date moves to archive/ with a date. The knowledge base stays small enough to be read at the start of every session.
7. Public method, private data. Generic skills come from this cookbook by version. Private skills add your context on top and name the public skill they extend.

## Set it up in a company (about one day)

1. Create a private repository from templates/ and fill kb/00_INDEX.md first.
2. Write kb/01_BRAND.md with the team: audience, offer, canonical proofs (named, dated, with sources), voice rules, banned phrases.
3. Install the public skills the team needs (README of this cookbook, "Install").
4. Add one routine at a time, starting with the one that saves the most hours. Check it runs without a human for a week before adding the next.
5. Connect the human annotation loop: where the digest lands, how the human answers.
6. Add the content testing loop (playbooks/content-testing-loop.md) once videos are published every week.

The skill statur-content-os-setup walks an assistant through these steps with the team.

## Promote a private skill to the public cookbook

1. The skill solves a problem other companies have.
2. Remove every client name, number, price, id, path and voice rule specific to your brand. Replace them with questions the skill asks the user.
3. Run scripts/check_skills.py and scripts/leak_scan.py with your private denylist.
4. Publish it in the cookbook with a version and a CHANGELOG line.
5. In the private repo, keep only what is private: a thin skill that names the public one and adds your context, or nothing at all.
