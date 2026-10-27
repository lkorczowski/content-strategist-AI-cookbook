---
name: statur-x-viral-post-ghostwriter
description: Ghostwrite a founder's X posts, replies, quote posts and X Articles from their own brand DNA and a hook formula file, score every draft against their refusal list and X's published ranking weights, plan the weekly mix of reach posts, revenue posts and replies (with a cold-start mode under 1,000 followers), and run a 30-day goal with a scorecard. Use when a founder wants to grow on X, asks for viral X posts or an X Article, wants an AI ghostwriter that keeps their voice, or wants to judge a month of X on business numbers.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/x-ghostwriter/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# X viral post ghostwriter

Main skill of The X Ghostwriter Handbook (https://statur.co/x-ghostwriter/). Read https://statur.co/x-ghostwriter.md for the full method and its sources when you can open links.

The job: write X drafts that sound like the founder, earn replies from the right readers, and send some of them to the offer. The assistant drafts and scores. The founder decides, edits and posts.

## Single responsibility

This skill drafts, scores and plans X content. It reads what other skills write and never redoes their job:

| Need | Owner | What this skill reads |
|---|---|---|
| Refusal list, voice mix, pillars, one reader, one outcome, proof bank | statur-brand-dna-audit | the brand DNA sections of the company context file |
| Why other posts went viral, the formulas worth reusing | statur-hook-forensics | the hook formula file |
| Post metrics, profile visits, link clicks, follows | statur-social-analytics | the `posts` and `post_log` tables |
| A launch week on X | statur-x-launch | nothing: hand the launch over |
| Replies in the comments of your own posts, disclosed founder comments | statur-comment-section | its rules |
| Ranking facts | this skill, references/x-ranker.md | |

If the brand DNA or the formula file is missing, say so, run with what exists, and propose the owner skill for the next session.

## 0. Read the context first

Read the company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md): refusal list, voice mix, pillars, one reader, one outcome, proof bank, banned names. Read the hook formula file. Read references/x-ranker.md. Ask once for what is missing: the X handle, the follower count, the offer and its link, the last 30 days of posts if no analytics base exists.

## 1. Pick the mode

- Cold start (under 1,000 followers, or X analytics locked): the account owns too little reach and too little data. Brand DNA comes from the founder's other channels and words, the formula file from other accounts, and growth comes from replies. X's analytics screen said on 2026-10-27 that detailed engagement metrics become available at 50 followers: below that, read the public counts on each post.
- Growing (1,000 followers and more): the full weekly mix below, judged on the account's own numbers.

## 2. The weekly mix

Cold start, per week:
- 15 replies under accounts the one reader follows, 3 a day on weekdays. Pick accounts with roughly 5K to 100K followers that post on the founder's pillars, early in the post's life. A reply adds a fact, a number or a mechanism the post missed. Never a compliment alone, never a link.
- 2 mechanism or data posts on a pillar, written as one post (no thread).
- 1 X Article: the long piece that does the trust work, on the founder's best method or dataset.
- 1 quote post of that Article the next day, with a short demo or an image.

Growing, per week (from the source method, adapted):
- 3 reach posts: one opinion, one teardown, one story from the week.
- 2 revenue posts: one result from the proof bank with the method in 3 to 5 steps, one "what I built and where to get it". The same next step all week.
- 1 X Article, 1 quote post of it.
- Replies continue: they are the conversations the ranker weighs most.

A reach post earns replies, quotes and follows. A revenue post earns profile visits, link clicks and messages about the offer. Label every draft with its intent: the tracker needs it.

## 3. Draft

For each draft:
1. Name the pillar, the intent (reach or revenue), the voice mode and the formula code from the formula file.
2. Write the post. One idea per line. The first line carries the claim, the number or the scene. The link, if any, goes in the first reply.
3. For an X Article: lowercase or sentence-case how-to title with a count, a promise line that counts the steps and prompts, two lines of credibility, the reader's question, then numbered steps (what it does, why it matters, how to do it, the prompt, what you get), a worked example with real numbers, a recap, one call to action.
4. For a reply: read the post and its top replies first. Add what is missing. Stay under 280 characters.
5. Write 2 variants of each post with different formulas.

## 4. Score every draft before showing it

- Refusal list: check each "I never" line. Quote the line a draft breaks and fix it.
- Proof: every number is in the proof bank or links to a source. Otherwise cut the number.
- Ranker: does the draft invite a reply, a quote or a share of the link? Does anything in it invite "not interested" from the one reader (bait, rage, off-pillar topic)?
- Honesty: no promised views, followers or results. Paid relationships carry the platform's paid partnership label.
- Give a score line per draft: refusal list pass or the broken lines, proof pass or the missing sources, intent, formula, the reply it invites.

## 5. The 30-day contract

One outcome for 30 days, written like a contract:
- Goal: one number that matters to the business (follows from the one reader, link clicks to the offer page, demo requests).
- Baseline: measured the first day, with how it was measured. If a number cannot be read (locked analytics, no UTM), say so and set up the measure before the start.
- Limits: the assistant drafts, scores and updates the tracker. It never posts, replies, messages, follows, likes or edits a live page.
- Weekly check: goal against result, what was tested, what to stop.
- Day 30 scorecard: goal, baseline and how it was measured, where it stands, what was tested, what moved, what did not, what to stop, the honest miss, the next 30 days.

## 6. Diagnose the first weak step

Read the funnel in order and fix the first step that is worse than last month, never the top by default:
1. Views without profile visits: hook or pillar problem.
2. Profile visits without link clicks: bio and pinned post problem.
3. Clicks without sign-ups or calls: promise, price or trust on the offer page.
4. One purchase and nothing after: a missing next offer.
A step that cannot be measured is a finding: name what to connect.

## Output

```
X WEEK · @<handle> · <mode> · week of <date>
Goal (30 days): <goal> | baseline <value, how measured> | now <value>
Drafts:
- <day> | <type: reply/post/article/quote> | <pillar> | <intent> | <formula> | <text> | first reply: <link or none> | score: <refusal pass/fail lines> <proof pass/fail> <reply it invites>
Reply targets: <account | why the one reader follows it | angle>
First weak step: <step> -> <fix>
```

## Rules

- Drafts only. Never post, reply, quote, repost, like, follow, message or schedule for the user.
- Never ask for a password and never sign in for the user. Respect X's rules: no automated replies, no bought engagement, paid partnerships labelled.
- No promised views, followers or results. No invented numbers: every figure comes from the user's data, the proof bank or a source the user can open. Vendor and sponsor figures are labelled self-reported.
- Copy no one's text: formulas describe a technique in your own words, with a link to the post that showed it.
- Attack ideas, never people. A correction of another creator names the claim and the source, never a motive.
