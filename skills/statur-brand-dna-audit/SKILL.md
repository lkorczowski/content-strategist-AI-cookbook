---
name: statur-brand-dna-audit
description: Build or audit a founder's brand DNA from evidence (their own posts, replies, talks and offer): a refusal list of checkable "I never" lines, a voice mix in percentages with a labelling rubric, content pillars derived from what a buyer must believe before paying, one reader, one outcome and a proof bank of numbers they can show. Writes into the company context file. Use when a founder says their AI content sounds generic, before hiring a ghostwriter or an AI to write for them, when setting up a new channel, or once a month to compare the voice they wrote down with the one they post.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/x-ghostwriter/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Brand DNA audit

Part of The X Ghostwriter Handbook (https://statur.co/x-ghostwriter/), recipes 01 and 02. Platform-neutral: the same brand DNA serves X, LinkedIn, short video and email.

The job: turn a founder's real words into rules a stranger, a ghostwriter or a model can check in five seconds. Adjectives ("authentic, bold") fail that test. Refusals, numbers and named beliefs pass it.

## Single responsibility

This skill writes the brand DNA sections of the company context file and audits them against what the founder actually posts. It never drafts posts (statur-x-viral-post-ghostwriter and the other writing skills do), never collects metrics (statur-social-analytics) and never sets up the knowledge base itself (statur-content-os-setup owns the file layout).

## 0. Read the context first

Read the company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md). Keep what is already decided. This skill fills the gaps and flags contradictions; it never overwrites a decided line without the founder's yes.

## 1. Gather evidence

Ask once, then work with what exists:
- The last 90 days of posts and the replies under them, on the main channel. Under 50 posts, add the founder's other words: transcripts of videos and calls, sales emails, talks, the about page.
- The offer: what is sold, at what stage, to whom.
- The questions people ask before they buy: DMs, sales call notes, replies.
- The numbers the founder can show: dashboards, screenshots, public pages.

Link every finding to the post or document it came from.

## 2. Refusal list

1. From the evidence, list: opening lines used more than twice, phrases the founder shares with five bigger accounts of the niche (name them), posts that drew pushback and why, the founder's existing writing rules.
2. Write 10 to 15 lines that start with "I never", in three groups: words, hooks, moves (framings, claims, behaviour).
3. Each line must be checkable by a stranger in five seconds. "I never sound generic" fails. "I never open with a question" passes.
4. Next to each line, link the post that made you add it. Flag any line the founder's own posts break, so the founder decides.

## 3. Voice mix

1. Define 3 modes. For each: what the first line does, sentence length, the kind of proof, how it ends.
2. Write a labelling rubric: for any post, which mode and why, in one line. The mode is decided by the ending.
3. Label the last 90 days. Show the real split next to the target split, and the three posts that sound least like the written voice.
4. Two people must label the same post the same way. If a label is disputed, tighten the definition.

## 4. Pillars, one reader, one outcome

1. List the 3 or 4 beliefs a buyer must hold before paying. Each belief becomes a pillar, named in four words or less.
2. For each pillar: the kind of post that proves the belief, and the kind that looks related but proves nothing.
3. One reader: one sentence specific enough to exclude people.
4. One outcome: what that reader gets after following the founder for a year.
5. If an analytics base exists, tag past posts by pillar and show which pillar sends people to the offer and which only earns reach.

## 5. Proof bank

Only numbers the founder can screenshot or link, each with its source, its date and who may see it (public, under NDA, client approval pending). Nobody cites a number that is absent from the proof bank, the founder included.

## Output

Write into the company context file, under the voice and proof sections, or propose the diff when the founder decides:

```
## Brand DNA (<date>, evidence: <sources>)
### Refusal list
- I never <...> (evidence: <link>) [broken by <link>: decide]
### Voice mix
Target: <mode A %> / <mode B %> / <mode C %> | Real (<n> posts, <period>): <...>
Rubric: first line / proof / ending per mode
### Pillars
- <pillar>: proves "<belief>" | proof post: <kind> | looks related, proves nothing: <kind>
### One reader / One outcome
### Proof bank
| Number | Source | Date | Visibility |
```

Then a short audit note: the three biggest gaps between the written voice and the posted one, and one change to try next week.

## Rules

- Drafts only: propose changes to the context file; the founder validates each decided line.
- Never ask for a password. Read only what the founder shares or what is public, at a human pace.
- No invented numbers: the proof bank holds only figures with a source. No promised views or results.
- Evidence first: every rule links to the post or document behind it. Quote the founder's words, never a third party's text.
- Personal or sensitive details seen in posts (health, family, private lives of others) stay out of the brand DNA.

## Credit

Method elements from Avid (@Av1dlive), X Article "Personal Brand 101: How to build a brand that makes money with AI" (2026-10-26, labelled on X as a paid partnership with Viktor): https://x.com/Av1dlive/status/2114754937032990945. Taken: the refusal list of "I never" lines, the voice mix in percentages with a rubric, pillars from buyer beliefs, the one reader, the one outcome, the proof bank. Written from scratch in our own words; ranking claims checked against xai-org/x-algorithm.
