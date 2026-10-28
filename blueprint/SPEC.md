# EVEREST OS · specification

Version 1.1 · 2026-10-28 · public, by Dr. Louis Korczowski (STATUR). Generic specification of the AI operating system described in this blueprint ([README.md](README.md)). Client manual: [START.md](START.md). Templates for a private repo: [templates/](templates/). It contains no company data. Each private instance keeps its own status table (which requirement passes, which issue tracks a gap) in its own repo and links here instead of copying this text.

Who this is for:
- A company deciding whether to adopt the system: sections 1, 2 and 4 say what it does and what it does not.
- A developer or an agent taking over the build: sections 3, 5, 6 and 7 say how it works, what the platforms allow, and how to test it.
- A reviewer cross-checking an instance: section 7 lists the acceptance tests; every requirement has an ID that the instance's status table reuses.

## 1. Goal

One assistant that knows the company, works the same way in every tool (chat on a phone, a coding session, a scheduled task, ChatGPT or Claude), never forgets an open task, and never acts without a human on what matters. The company owns its knowledge; the method stays public and versioned.

## 2. Principles

| ID | Principle | Why |
|---|---|---|
| P1 | One fact, one home. Every rule or fact has exactly one source of truth; everything else points to it. | A copy reaches only the tools that load it, and drifts at the first edit. |
| P2 | Short entry points. What is pasted into a tool (project instructions, scheduled task prompt, CLAUDE.md) is a few lines that point to the rules file. It never contains a business rule. | The paste is done once by hand; a rule inside it would need the same hand every time it changes. |
| P3 | Configuration in git, live state in a tracker. Rules, knowledge and skills live in a private repo (main branch). Tasks, decisions and blockers live in a tracker the assistant can write to. Neither lives in a chat. | A chat is not searchable by the next session; a file kept by hand goes stale. |
| P4 | Autonomy. A routine runs end to end without a human. A step that needs a human is either removed or put on one action page with the exact text to paste. | A routine that needs its owner adds work instead of saving it. |
| P5 | Fail loudly. When a resource is missing (repo, connector, computer, browser), the run says so on its first line and writes nothing. | A silent "success" that did nothing is the worst failure: nobody looks. |
| P6 | Drafts only. Sending, publishing, paying, deleting, credentials and account settings stay with humans. | The company stays accountable for what goes out in its name. |
| P7 | An agent never has more rights than the human who runs it. | Delegation must not become privilege escalation. |
| P8 | Public method, private data. Generic skills live in this cookbook; a private skill extends a public one by name and never copies it. | Improvements reach every instance; private data reaches none. |
| P9 | English core. The architecture (rules file, entry points, specification) is written in English so one template serves every client; the language used with each person is a rule inside the rules file. | One template, many languages. |

## 3. Architecture

### 3.1 Stores

| Store | Holds | Written by | Read by |
|---|---|---|---|
| Private repo, main branch | rules file (AGENTS.md), knowledge base (kb/), private skills, routine prompts, the instance's status table | agents through branches and pull requests, merged by a human; nobody pushes to main | every session that can attach the repo |
| Tracker (Airtable or similar) | tasks, decisions, blockers, log, a queue of "pending repo writes" | every session, every routine | every session at start |
| This public cookbook | method: skills, playbooks, this specification, START.md | the method owner | every instance |
| Entry points | the short bootstrap of P2 | a human, once | the tool that loads it |
| Caches (project docs, skills saved in an account, assistant memory) | copies of repo files | generated, never edited | tools that cannot read the repo |

### 3.2 Orchestrators and how each reaches the rules

| Orchestrator | Reaches the repo | Notes |
|---|---|---|
| Coding session (Claude Code, Codex, Cursor) started on the repo | yes, from the start | Reads AGENTS.md through CLAUDE.md (`@AGENTS.md`). |
| Scheduled task | yes, if its prompt asks for the repo by name | The stored prompt is the user's request for that run. Observed on Claude cloud scheduled tasks (C08); other platforms: test T12. |
| Chat in a project (Claude, ChatGPT) | only when the user asks for it in a message | See constraint C01. |
| Session linked to a personal computer | through the local clone | Push rules for local clones: the instance's rule 0. |
| Client project without a repo (level 0 below) | no | Uses START.md from this cookbook and uploaded files. |

### 3.3 Adoption levels

| Level | What the company has | What works |
|---|---|---|
| 0 | A ChatGPT or Claude project, the one-line instruction that points to START.md, an engagement brief | Onboarding, intake interview, first knowledge base files, drafts, status from STATE.md (re-uploaded by hand) |
| 1 | + a private repo | Knowledge versioned, shared by every tool, no re-upload |
| 2 | + a tracker | Tasks and decisions survive between sessions; forgotten and blocked tasks resurface |
| 3 | + scheduled tasks | Inbox triage, CRM notes, meeting recaps, analytics collection, without a human in the loop except to approve drafts |

## 4. Feature catalog

| ID | Feature | Level | Status in the method |
|---|---|---|---|
| F01 | Same rules in every tool through one rules file and a short bootstrap | 1 | specified, automatic checks exist (check.py in the reference instance) |
| F02 | Onboarding "Start EVEREST OS" from an engagement brief | 0 | START.md 1.0 online |
| F03 | Session start: open tasks and pending decisions announced, CRITICAL and BLOCKED first | 2 | specified |
| F04 | A task is "done" only when no critical subtask is open | 2 | specified, needs tracker fields (parent, blocked_by, criticality) |
| F05 | A decision postponed in a chat becomes a pending decision with a review date | 2 | specified |
| F06 | Writes from a tool that cannot reach the repo go to a "pending repo write" queue | 1 + 2 | specified |
| F07 | Routines that fail loudly instead of silently | 3 | specified in the routine template |
| F08 | Drafts only: email drafts, post drafts, article drafts | 0 | in every skill's Rules section |
| F09 | Fast answers on a cheap model from a machine index of the knowledge base | 1 | index format specified (key, value, source, date) |
| F10 | Weekly status email draft for the advisor | 0 | START.md section 6 |
| F11 | Skills always at their latest version | 1 | gap: see C03 |
| F12 | Access tiers (contractor, read-only employee, agent with write access, client data split) | 1 + 2 | to design |
| F13 | Real-time client channel | any | out of scope for now |
| F14 | Weekly drift check: rules checks, caches against the main commit, and per-repo branch hygiene (merged, stale, open branches) | 1 | specified (E13) |

## 5. Edge cases

| ID | Case | Expected behavior |
|---|---|---|
| E01 | A task was forgotten | It is announced at the start of the next session on its topic. |
| E02 | A task is believed done but a critical subtask is open | The assistant refuses to close it and names the subtask. |
| E03 | A decision was postponed in a chat | A pending decision row with a review date exists before the chat ends. |
| E04 | The tool cannot reach the repo (phone, plain chat) | It says so in one line, answers only from what it can read, and queues durable writes. |
| E05 | A routine starts while the computer it needs is off | First line "FAILURE REPORTED: <resource> missing", nothing written. |
| E06 | Contractor without repo access | Receives an exported brief; feedback comes back by email, then into the tracker. Never a pasted rule. |
| E07 | Employee with read-only access | Read-only tracker view and exported docs. |
| E08 | Employee or agent with write access | Branch and pull request, never main. |
| E09 | Some people must not see client data | Repos split by sensitivity; the bootstrap does not change. |
| E10 | Quick question on a cheap model | Reads the machine index, then one section, never the whole base. |
| E11 | A client shares documents with the assistant | They stay in the client's project; nothing goes to a public page. |
| E12 | Two tools edit the same file | Branches and pull requests; routine state never lives in git with several writers. |
| E13 | Work branches pile up | A merged branch is deleted at merge. An unmerged branch idle for 7 days without a pull request is kept as a tag `archive/<branch>`, then deleted. A weekly check counts merged, stale and open branches and deletes nothing. |

## 6. Platform constraints (observed, dated, may change)

These are facts about the tools, not choices. Each was observed on the date given; re-check before relying on it.

| ID | Constraint (observed 2026-10-28 unless noted) | Consequence |
|---|---|---|
| C01 | In a Claude chat running in auto permission mode, attaching a GitHub repo is refused unless the user's own message asks for it. Instructions of the project do not count as a request. | A chat reads the repo only after the user writes a short request such as "attach the repo". |
| C02 | Declaring trusted repos for the auto mode classifier is done in organization managed settings (Team and Enterprise plans, Owner role) or in a settings file on the user's machine. Cowork sessions do not read the managed settings from the admin console. | On other plans, a cloud chat cannot be pre-authorized. |
| C03 | A skill saved in a Claude account is a snapshot. It does not follow the repo. | Either re-save after each change, or save a stub that reads the skill file from the repo (stub never changes). |
| C04 | A Claude project can sync files from GitHub into its knowledge, but the sync is manual ("Sync now"). | Useful for reading, but it is a cache that drifts until someone clicks. |
| C05 | Creating a scheduled task from a session needs an explicit request from the user in that session. | Routines are created on a human's request, then run alone. |
| C06 | A git client inside a sandboxed view of a personal computer can read but should not commit (no credentials, lock files left behind). | Push from a cloud clone or from the computer's own terminal. |
| C07 | Files an assistant writes in a ChatGPT or Claude project conversation are not added to the project's knowledge. | At level 0, STATE.md and kb files are re-uploaded by hand. |
| C08 | A Claude cloud scheduled task whose stored prompt names the repo attached it, read the rules file and pushed a test branch with no human, in under a minute. | Level 3 routines can run in the cloud. Creating the task still needs C05. |
| C09 | `git clone --depth 1` implies `--single-branch`: the clone fetches only the default branch (git documentation). | Before branching, add the fetch refspec `+refs/heads/*:refs/remotes/origin/*`, or a pushed branch has no remote ref and checks report false "unpushed commit" alerts. Judge whether a branch is merged on full history. |

## 7. Acceptance tests

An instance reuses these IDs in its own tests file (P1: it links here and does not copy the text) and records date, result and link for each.

| ID | Test | Pass when |
|---|---|---|
| T01 | Rules file at the repo root, CLAUDE.md imports it | Automatic check passes |
| T02 | Bootstrap identical in every entry point, under 1,500 characters, no business rule | Automatic check passes |
| T03 | No machine path in any routine prompt | Automatic check passes |
| T04 | Phone chat, question on a canonical fact | Answer cites the source file, invents nothing, says which copy or repo it read |
| T05 | Same question in ChatGPT and in Claude | Same facts, same sources |
| T06 | Coding session on the repo | Reads the rules file, and on a personal computer the machine identity file, before any edit |
| T07 | Forgotten task (E01) | Announced first |
| T08 | Blocked task (E02) | Refused, subtask named |
| T09 | Postponed decision (E03) | Pending row with review date |
| T10 | Routine with a missing resource (E05) | FAILURE REPORTED line, nothing written |
| T11 | Cheap model with the index only (E10) | Correct file and section |
| T12 | Scheduled task attaches the repo, reads the rules, pushes a test branch | Read OK and push OK, or the exact refusal recorded |
| T13 | Every skill linked from a public page exists in this cookbook | Automatic check passes |
| T14 | Skill used in a session matches the repo version | Same content as main, or the stub loaded the repo file |

## 8. Change process

Change the method here through a pull request, bump the version line, add a CHANGELOG line. An instance updates its status table, never this file. A finding that is specific to one company stays in its private repo.
