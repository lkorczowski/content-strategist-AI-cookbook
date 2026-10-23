---
name: video-post-mortem
description: Compare short-form videos passage by passage (retention curve, spoken words, on-screen text, saves and shares) against the creator's own comparable videos, then return KEEP, CHANGE or CUT edit instructions labelled as tests. Use when someone asks why a TikTok, Reel or Short underperformed, which sentence made viewers leave, how two versions compare, or how to re-edit a video.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0"
  playbook: https://statur.co/content-testing-loop/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Video post-mortem

Part of The Content Testing Loop (https://statur.co/content-testing-loop/). Read https://statur.co/content-testing-loop.md for the full method and its sources when you can open links.

The job: find the passage that lost viewers, read what was said and shown at that moment, propose one precise edit, and say how sure you are. One video compared with nothing teaches nothing. Every judgment is made against the creator's own archive.

## What to ask for

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing.

Ask once, then work with what the user gives you. Accept a pasted table, a CSV (use templates/video-log.csv as the expected shape) or screenshots of the analytics screen.

For each video under review:
- Platform, publish date, the date the numbers were read, and whether it ran in the main feed, as a test post or as an ad.
- Transcript with timestamps, and the on-screen text by segment. If there is no transcript, ask for the script or the caption file.
- Retention: percent of viewers still watching by second, or at least at 3 s, 10 s and the end. Average watch time and length.
- Views, likes, comments, saves, shares, new followers.

For the comparison set: 10 to 20 earlier videos from the same account, same platform, same format and a similar length, with the same metrics. Fewer than 5 means the comparison is descriptive only, and you say so.

## Evidence rules

1. Maturity gate. A video is early data until it is at least 7 days old, has passed 1,000 views and its numbers carry a reading date. Early videos get a description, never a verdict.
2. Own archive only. Compare with the creator's comparable videos. Industry averages are context, never the yardstick.
3. Keep the signals apart. Retention says whether people stayed. Saves say they want to come back. Shares say they want someone else to see it. Comments and follows are separate again. Never merge them into one score.
4. Passage loss. For each window of 1 to 3 seconds, compute the drop in percent still watching, then compare it with the usual drop of the comparison set in the same window. The first 2 seconds always lose the most: judge them against the comparison set, never against the rest of the video.
5. Archive test. An explanation counts as supported only when the same pattern shows up in at least two other videos and you looked for counterexamples. Otherwise it is a hunch, and you write the word hunch.
6. Limits. End with what the data cannot tell (sample size, a news event, a change in distribution, a different posting hour).

## Steps

1. Check the inputs. List missing fields and the maturity status of each video. Stop at a description if everything is early data.
2. Cut each video into windows: 0-2 s, 2-5 s, then 2 to 3 second windows aligned on sentences.
3. Build the passage table: window, percent remaining, spoken words, on-screen text, what is visible, raw loss, usual loss, verdict (better, usual, worse, or uncertain when the gap is within a few points).
4. Name the worst reliable passage and the best one. Read the context: promise made and not paid, a slow setup, a joke that needs prior knowledge, a jump in topic, on-screen text that contradicts the voice, a loop closed too early.
5. Test each explanation against the archive. Keep supported ones, label the rest as hunches.
6. Write the edit plan with timecodes: KEEP (what works and must survive the re-edit), CHANGE (exact replacement line or visual), CUT (exact start and end). One to three changes, never a full rewrite.
7. Write the test: re-edit against the original, published in comparable conditions (the same hour and weekday, or a platform test feature such as Instagram Trial Reels where available), with the metric that decides and the reading date.

## Output

```
POST-MORTEM · <video> vs <comparison set, n=, dates>
Status: mature | early data (descriptive only)
Signals: retention at 3 s / 10 s / end, saves per 1,000 views, shares per 1,000 views, each vs the set median
Passage table: <window | remaining | spoken | on screen | raw loss | usual loss | verdict>
Worst reliable passage: <window> because <reason> (supported | hunch)
Best passage: <window> because <reason>
Edit plan:
- KEEP <window>: <why>
- CHANGE <window>: "<new line or visual>"
- CUT <window>: <start-end>
Test: <version A vs B, where, decision metric, reading date>
What the data cannot tell: <limits>
Lessons to log: <0 to 2 lines for the lessons ledger, with status>
```

## Rules

- Drafts only. Never publish, delete, schedule or re-upload anything for the user.
- Never ask for a password and never sign in for the user. Work from exports, screenshots or numbers the user provides, or from official platform APIs the user has connected. Respect each platform's terms of use.
- No promised views or results. No invented numbers: every figure comes from the user's data or a source the user can open.
- Flag anything confidential (customer names, revenue, internal decisions) before it goes into a script.
