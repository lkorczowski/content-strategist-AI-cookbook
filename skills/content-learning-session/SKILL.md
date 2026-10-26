---
name: content-learning-session
description: Run a monthly learning session over a creator's or founder's whole short-form history, re-test the lessons already saved, add new ones only with examples and counterexamples, keep them in a lessons ledger, and write a short coaching brief with the next three tests. Use when someone wants to know what their content data has taught them, to update a content playbook, or to plan next month's tests.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.2"
  playbook: https://statur.co/content-testing-loop/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Content learning session

Part of The Content Testing Loop (https://statur.co/content-testing-loop/). Read https://statur.co/content-testing-loop.md for the full method and its sources when you can open links.

Credit: the structure of this skill (re-test saved lessons first, examples and counterexamples, REFUTED lines kept in the ledger, a coaching brief at the end) comes from a public workflow shared by Angus Sewell (https://www.tiktok.com/@angusthenontechnical/video/7699512206605421838). The instructions are written from scratch.

A post-mortem explains one video. A learning session decides what the whole archive has proven. Its output is a ledger of lessons with their evidence, and a short list of tests for next month. Run it once a month, or after every 20 new videos.

## What to ask for

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing.

If the workspace has an analytics base built with statur-social-analytics (a folder with accounts.csv, raw/ and analytics.db, usually content/analytics/), read the `video_log` view over the whole history (`export-log` writes it as video-log.csv) instead of asking for numbers. That skill owns collection and the data schema; this one only reads it.

- The history: one row per video with these columns (the same as video-log.csv in the video-post-mortem skill): video_id, platform, publish_date, read_date, days_live, distribution (main_feed, test, ad), format, hook_type, length_s, views, likes, comments, saves, shares, new_followers, avg_watch_s, ret_3s_pct, ret_10s_pct, ret_end_pct, notes.
- The current lessons ledger (templates/lessons-ledger.csv). Empty is fine for a first session.
- The post-mortems written since the last session, if any.

## Evidence rules

1. Separate before you compare. Split by platform, and by distribution period when something changed (paid boost, a new format, a long pause, a platform update the user knows about). Never mix organic and paid results.
2. Old lessons first. Re-test every saved lesson on the new videos before adding anything. Each lesson ends the session as confirmed, weakened or refuted. A refuted lesson stays in the ledger with the word REFUTED, so nobody learns it twice.
3. Examples and counterexamples. Every finding lists the videos that support it and the videos that contradict it.
4. Status ladder. Hunch: seen once or twice. Supported: seen in at least 5 videos across at least 2 topics, with fewer counterexamples than examples. Confirmed: still supported after one dedicated test where only that variable changed.
5. Principles over topics. Keep lessons that hold across different topics and formats ("a number in the first 2 seconds lifts 3-second retention"). A lesson that only describes one viral video is a hunch.
6. Mature data only. Videos younger than 7 days or under 1,000 views stay out of verdicts.

## Steps

1. Load and clean the history. Report gaps and the number of mature videos per platform.
2. Re-test the ledger. One line per lesson: new examples, new counterexamples, new status.
3. Look for new patterns by format, hook type, first on-screen words, length, topic family, posting time and call to action. Compare medians, never single videos.
4. Write new ledger rows (hunch or supported) with their evidence.
5. Pick the next three tests. Each test changes one variable, names the metric that decides and the number of videos needed.
6. Write the coaching brief: 300 to 500 words, spoken style, second person, in this order: what worked, what stopped working, the three tests, one thing to stop doing. It can be read aloud, or pasted into an audio tool such as NotebookLM to get a short audio overview.

## Output

```
LEARNING SESSION · <account> · <period> · mature videos per platform: <n>
Ledger changes: <lesson id | old status -> new status | evidence | counterexamples>
New lessons: <rows>
Next three tests: <variable | hypothesis | metric | videos needed>
Coaching brief: <text>
```

Return the updated ledger as CSV so the user can paste it back into their sheet.

## Rules

- Drafts only. Never publish, send or schedule anything.
- Never ask for a password or sign in for the user. Respect each platform's terms of use.
- No promised views or results. No invented numbers: every figure comes from the user's data or a source the user can open.
- Say plainly when the archive is too small to conclude.
