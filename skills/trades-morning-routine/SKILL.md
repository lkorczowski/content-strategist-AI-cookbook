---
name: trades-morning-routine
description: Run the daily 7am routine from The One-Hour Video Handbook for Tradespeople. Find the new video and its transcript, check if the website covers that job and town, write a website article saved as a draft, post texts for each app and a 5 to 7 slide carousel, then leave everything in an email draft called Morning brief. Use as the instructions of a scheduled task, or when a tradesperson asks to turn today's video into an article, posts and a carousel.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0"
  playbook: https://statur.co/tradespeople-video-handbook/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Trades morning routine

Part of The One-Hour Video Handbook for Tradespeople (https://statur.co/tradespeople-video-handbook/). Read https://statur.co/tradespeople-video-handbook.md for the full method and its sources when you can open links.

The job: every morning, turn the tradesperson's new video into a website article draft, post texts and a carousel, and leave everything in one email draft. The user reads it over coffee in 10 to 15 minutes, corrects a few words and posts by hand. Nothing is sent or published by the assistant.

This skill is written for any assistant that can run scheduled tasks, use a browser and create email drafts (for example Claude with Claude in Chrome and Gmail). The routine runs unattended: it never waits for an answer during the run. Anything that needs the user goes into the brief.

## What it needs (set once, usually by the trades-ai-setup skill)

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing.

- A business profile: trade, services, towns covered, tone, contact line, channel links, website address, inbox for the brief.
- The user signed in, by themselves, to the channel, the email and the website in the browser the assistant uses.
- A record of the last run date, so the same video is never processed twice.

Run by hand: ask once for the profile items that are missing, or for the video link and transcript, then work with what the user gives you.

## Steps

1. Find new videos. Open the learning channel. List videos published since the last run. None: skip to step 7 and suggest an old job to retell (film an old before photo from the screen, tell it from a new angle).
2. Get the words. Read the transcript or automatic captions of each new video. No speech: say so in the brief and suggest talking to camera next time. Never guess what was said.
3. Check the website. Look for an existing page about this job and this town. Covered: plan an article that adds the new case and links to that page. Missing: plan a new article for the service and the town.
4. Website article. Title with the service and the town. 300 to 600 words, plain words, in the order Problem, Agitation, Solution as told in the video. Facts only from the transcript and the profile. Contact line at the end. Save it as a DRAFT on the website. If drafts cannot be saved, paste the article in the brief.
5. Post texts. One text per app (for example Facebook, Instagram, LinkedIn), 80 to 150 words, in the user's tone, contact line at the end. Remind the user to upload the clean video file in each app by hand, without another app's watermark.
6. Carousel. 5 to 7 slides: the customer's question, the problem, why it mattered, the result, the delay given in the video, the contact. Give the slide text and one image idea per slide (frames from the video, or the before and after photos the user already has). Create the images if the assistant can, and attach or link them.
7. Morning brief. Create an email DRAFT titled "Morning brief <date>" in the user's inbox, in this order: what to post today, links to the drafts, the texts ready to paste, the carousel, then "Needs you" (expired sign-ins, facts to confirm, questions).
8. Log. Save the run date and the videos processed. Read any feedback the user left (a reply to yesterday's brief, notes in the instructions) and apply it from the next run.

## Writing rules

- Short sentences, the words a customer uses, no jargon.
- Never invent a price, a delay, a town, a brand or a review. Missing fact: write [to confirm] and list it under "Needs you".
- No customer names, faces, addresses or number plates unless the user said the customer agreed.
- One contact line, the same everywhere, exactly as written in the profile.

## Failure handling

- A site signed the user out: stop that step, keep going with the others, and write in the brief which site and where to sign in again. Never ask for a password.
- The website or channel layout changed and a step fails: describe what was seen in one line in the brief. Never click buttons that publish, delete or change settings to work around it.
- Something is unclear: choose the safest option (keep it as a draft, change nothing) and ask the question in the brief.

## Output

```
Subject: Morning brief <date>

POST TODAY
- <video title> on <learning channel>: done by the user | to repost on <apps>

WEBSITE
- Article draft: "<title>" saved at <draft link> | covers <service> in <town> | existing page: <link or none>

POST TEXTS
- <app 1>: <text>
- <app 2>: <text>

CAROUSEL (5 to 7 slides)
1. <text> | image: <idea or file>
...

NEEDS YOU
- <expired sign-in, fact to confirm marked [to confirm], question>
- No new video? Idea to retell: <old job, new angle>
```

## Rules

- Drafts only. The routine saves a website draft and an email draft. It never sends an email, never publishes, never schedules a post and never deletes anything.
- Ask before any change other than creating those drafts: write the question in the brief and wait for the user's answer on a later run.
- Never ask for a password and never sign in for the user.
- Respect each platform's terms of use. Use official features (captions, studio apps, website drafts) and only the user's own content.
- No promised views or results. No invented numbers: every figure comes from the user, the transcript or a source the user can open.
- Flag anything confidential (customer details, prices, addresses) before it goes into a draft.
- Companion skills: trades-ai-setup (installs this routine), trades-video-coach (scripts and feedback).
