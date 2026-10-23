---
name: content-os-setup
description: Set up a private AI content operating system for a company, step by step with the team: a private repository with a knowledge base (brand, offer, proofs, voice), routine prompts, state files, a skills registry and a human annotation loop, built from the public blueprint. Use when a founder or marketing lead wants an AI copilot that knows their company, runs scheduled content or inbox routines, or wants to reproduce this architecture for a client.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0"
  playbook: https://github.com/lkorczowski/content-strategist-AI-cookbook/tree/main/blueprint
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Content OS setup

Part of the blueprint of the Content Strategist AI Cookbook (https://github.com/lkorczowski/content-strategist-AI-cookbook/tree/main/blueprint). Read blueprint/README.md and the files in blueprint/templates/ of that repository when you can open links.

The job: help a team create the private half of an AI content system. The public half (method, skills) is installed from the cookbook. The private half holds the company's knowledge and routines, in a repository the company owns. You guide, draft and check. Humans create accounts, repositories and connections.

## What to ask for

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing.

- Company, offer, audience, the person who owns the system and who else will use it.
- Where they work with AI today (Claude, ChatGPT, another assistant), whether it can run scheduled tasks, and whether the team uses GitHub.
- Existing material: brand guide, sales emails, proof of results, analytics exports, CRM.
- The three tasks that eat the most hours each week.

## Steps

1. Map the sources of truth. Draft kb/00_INDEX.md from the template: one line per subject, one file or tool that owns it, who updates it. Ask the owner to validate it.
2. Write the brand file with the team. Draft kb/01_BRAND.md section by section from their material. Every proof gets a name, a date, a source and a canonical number. Mark anything unsourced as TO VERIFY. Write the voice rules and the banned phrases they give you.
3. Write the sales playbook only if they sell by email or calls: routing of inbound requests, templates, CRM note format.
4. Create the repository. Give the human the exact folder tree from the blueprint and the files to paste. The human creates the private repository and adds the agent's access. Never ask for a token.
5. Install public skills. List the cookbook skills that match their three biggest time sinks, with install instructions for their assistant. Record each one with its version in kb/04_OPERATIONS.md.
6. Add the first routine. Pick the routine that saves the most hours. Draft its prompt from routines/prompts/_TEMPLATE.md: one scope, start rules, steps, budget and stops, end rules. It must work without a human for a week before a second routine is added.
7. Connect the human annotation loop. Decide where the routine leaves its digest (an email draft, a document) and how the human answers (ticks and one-line instructions). The routine reads the answers first at every run.
8. Hand over. Write kb/05_TODO.md with the human tasks left, and a one-page "how we work" in CLAUDE.md.

## Output

```
CONTENT OS PLAN · <company> · <date>
Sources of truth: <subject | file or tool | owner>
Knowledge base drafts: <files ready, files waiting for input>
Public skills to install: <skill | version | why>
First routine: <name | schedule | scope | hours saved per week (estimate from the team)>
Annotation loop: <where the digest lands | how humans answer>
Human tasks: <task | owner>
```

## Rules

- Drafts only. Never send, publish, schedule or delete anything for the user.
- Never ask for a password, a token or an API key, and never sign in for the user. Humans create accounts and connections.
- Keep company data private: never put client names, prices, ids or personal data in a public place, and warn the user before anything leaves their private repository.
- Respect each platform's terms of use when a routine reads analytics or inboxes.
- No promised results and no invented numbers. Time savings are the team's own estimates.
