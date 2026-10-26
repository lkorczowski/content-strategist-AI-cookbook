---
name: statur-trades-setup
description: One-time install of the morning AI routine from The One-Hour Video Handbook for Tradespeople. Check the prerequisites, collect the business profile, audit the video channel and the website, create a scheduled task at 7am that turns each new video into a website article draft, post texts and a carousel in an email draft, then run a first test. Use when a tradesperson asks to set up the AI routine, automate posts from their videos, or connect their assistant to their channel, email and website.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "2.0.0"
  playbook: https://statur.co/tradespeople-video-handbook/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Trades AI setup

Part of The One-Hour Video Handbook for Tradespeople (https://statur.co/tradespeople-video-handbook/). Read https://statur.co/tradespeople-video-handbook.md for the full method and its sources when you can open links.

The job: install, once, a routine that works overnight so the tradesperson finds drafts every morning. The user talks on camera. The assistant writes. Everything stays a draft until the user posts it. The setup takes about 90 minutes with the user, then the routine needs no daily input beyond reading the brief.

This skill is written for any assistant that can run scheduled tasks, use a browser and create email drafts (for example Claude with Claude in Chrome and Gmail). Adapt the steps to the tools available, and say plainly when a step cannot be done.

## What to ask for

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing.

Ask once, one short question at a time, then work with what the user gives you.
- Trade, services, towns covered, and the contact line to end every post (phone or website, as the user wants it written).
- The learning channel and its link, and the other apps where the user reposts.
- The website address and how it is edited (website builder or CMS), and whether it can save an article as a draft.
- The inbox where the morning brief should land.
- Tone: three words the user would use to describe how they talk, and one past post or caption they like.

## Prerequisites (check before anything else)

1. An assistant plan that runs scheduled tasks while the user is away.
2. A computer that stays on overnight, if the assistant works through the user's own browser.
3. The user signed in, by themselves, to the channel, the email and the website in that browser. Never ask for a password. If a sign-in is missing, tell the user where to sign in and wait.
4. The videos have speech. A video without words gives the assistant nothing to write. Check that the channel offers transcripts or automatic captions.

If one prerequisite fails, stop, say which one and what the user can do, and continue only when it is fixed.

## Setup steps

1. Profile. Write a one-page business profile from the answers: trade, services, towns, tone, contact line, channel links. Show it to the user and ask for corrections.
2. Channel audit. Check the channel against the handbook rules: named after the person then the trade, face as profile photo, description with trade, towns, phone and website. List the fixes in order with the exact text to paste. The user makes the changes.
3. Website audit. List the existing pages by service and by town. Mark which jobs and towns are covered and which are missing. Confirm that a new article can be saved as a draft without being published. Change nothing on the website.
4. Routine draft. Write the routine instructions (below), filled with the profile. Show them to the user.
5. Scheduled task. Ask the user before creating it. Then create one task at 7:00 local time, every day, that runs the routine. Name it clearly so the user can find, pause or delete it.
6. Autonomy check. Read the routine step by step and confirm that no step needs the user during the night. The only allowed interruption is a sign-in that expired, which the brief reports.
7. First test. With the user present, run the routine once on the latest video. Open every draft together: the website article, the post texts, the carousel, the email brief. Collect the user's corrections and add them to the routine instructions.
8. Handover. Tell the user in four lines: where the brief lands, how to give feedback (reply to the brief or edit the instructions), how to pause the task, what to do when the brief says a sign-in expired.

## Routine instructions (to fill and save in the scheduled task)

If the statur-trades-morning-routine skill is installed, the task can simply run it. Otherwise save these instructions:

```
Every day at 7:00:
1. Open <channel link>. Find videos published since the last run. None: go to step 7.
2. Get the transcript or automatic captions of each new video. No speech: note it in the brief.
3. Check <website> for a page about this job and this town.
4. Write one website article (title with service and town, 300 to 600 words, the job as told in the video, contact line at the end). Save it as a DRAFT on the website. Never publish.
5. Write post texts for <other apps>, 80 to 150 words each, in the user's tone, contact line at the end.
6. Create a 5 to 7 slide carousel: the problem, why it mattered, the result, the delay given in the video, the contact.
7. Create an email DRAFT titled "Morning brief <date>" in <inbox>: links to the drafts, the texts, the carousel, and anything that needs the user (a sign-in that expired, a fact to confirm, an idea to retell an old job when no new video exists).
Never send, publish, delete or edit a published page. Never invent a price, a delay, a town or a review. Ask in the brief before any other change.
Profile: <one-page business profile>
```

## Output

```
AI SETUP · <trade> · <towns> · <date>
Prerequisites: scheduled tasks <ok|missing> | computer on <ok|missing> | signed in: channel <ok>, email <ok>, website <ok> | speech in videos <ok|missing>
Profile: <summary, confirmed by the user>
Channel fixes: <ordered list with text to paste>
Website coverage: <service x town covered | missing> | draft saving <ok|not possible>
Scheduled task: <name, time, created after the user said yes>
Autonomy check: <ok | the step that needs the user>
First test: <drafts created and where> | corrections added: <list>
Handover: <brief location | feedback | pause | expired sign-in>
```

## Rules

- Drafts only. The routine creates a website draft and an email draft. It never sends an email, never publishes, never schedules a post and never deletes anything.
- Ask before any change: before creating the scheduled task, before any change to the channel, the website or the email settings. The user makes channel and profile changes themselves.
- Never ask for a password and never sign in for the user. If a site signs the user out, the brief says where to sign in again.
- Respect each platform's terms of use. Use official features (studio apps, captions, website drafts) and never scrape other people's content.
- No promised views or results. No invented numbers: every figure comes from the user or a source the user can open.
- Privacy: no customer names, faces, addresses or number plates in drafts without consent. Flag anything confidential.
- Companion skills: statur-trades-morning-routine (the daily run), statur-trades-video (scripts and feedback).
