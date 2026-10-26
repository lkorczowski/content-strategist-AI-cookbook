---
name: format-dice-review
description: Review short-form video formats as dice (the dice system by Dr. Louis Korczowski): group videos by format, read each format's median and spread on mature data, then decide keep, change one variable or drop, and plan the next production day. Use for a weekly or monthly format review, when someone asks which video formats to keep, or how to plan the next batch of videos.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.1"
  playbook: https://statur.co/content-testing-loop/
  method: https://statur.co/method/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Format dice review

Part of The Content Testing Loop (https://statur.co/content-testing-loop/). The theory: https://statur.co/method/ and https://louis-korczowski.org/board-game-theory-viral-short-form-video.

A video is a throw and a format is the die. One throw tells you almost nothing. A format is good when it lands high on average with a small spread. This review judges dice, never single throws, and sits above the video post-mortem: the post-mortem fixes a video, the dice review decides which formats get produced next.

## What to ask for

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing.

If the workspace has an analytics base built with statur-social-analytics (a folder with accounts.csv, raw/ and analytics.db, usually content/analytics/), run `python3 scripts/analytics.py dice <dir>` from that skill and read the `video_log` view instead of asking for numbers. That skill owns collection and the data schema; this one only reads it.

- One row per video: format name, platform, publish date, reading date, views, saves, shares, retention at 3 s and 10 s (the columns of video-log.csv in the video-post-mortem skill).
- For each format: how many videos were planned before judging it, and the result agreed for it (the target), if any.
- The production capacity of the next session (how many videos).

## Rules of the review

1. Mature data only: videos at least 7 days old and above 1,000 views, or the account's usual floor if it is smaller. Younger videos are listed apart.
2. Read views on a log scale. Report each format's median, its typical range (25th to 75th percentile) and its floor.
3. Judge each signal apart: views, saves per 1,000 views, shares per 1,000 views, 3-second retention.
4. Respect the planned repetitions. A format is never dropped before it has run the number of videos planned for it. Keep judging it, keep improving it.
5. Two kinds of dice. Mimetic formats copy what already performs on the platform. Original formats are built around one person, their face and their way of talking. A healthy set keeps both.

## Decisions

- KEEP: median above the account median and range acceptable. Make it a template (fixed opening, structure, length) and produce variations.
- CHANGE ONE VARIABLE: median close to the account median, or a wide range. Change only the hook, the length or the setting, then judge again after the same number of videos.
- DROP: below the account floor on the planned repetitions, after at least one change. Replace it with a new die, mimetic or original, to keep the balance.
- WATCH: not enough mature videos yet.

## Steps

1. Group videos by format and count mature videos per format.
2. Compute median, range and floor per format and per signal.
3. Assign KEEP, CHANGE, DROP or WATCH with one sentence of justification and the evidence.
4. Propose new dice when a format is dropped or when the set lacks mimetic or original formats.
5. Plan the next session: number of videos per format, most proven formats first, one slot for a new die.

## Output

```
DICE REVIEW · <account> · <period> · mature videos: <n>
<format | type mimetic/original | n | median views | range | saves/1k | shares/1k | 3 s retention | decision | reason>
New dice: <format | type | why>
Next session plan: <format | videos | variable to change, if any>
```

## Rules

- Drafts only. Never publish, send or schedule anything.
- Never ask for a password or sign in for the user. Respect each platform's terms of use.
- No promised views or results. No invented numbers.
- When the data is too thin, say so and plan more throws.
