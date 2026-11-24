---
name: statur-trial-reels
description: Test reel hooks on Instagram with trial reels (shown to non-followers first), publish them from Claude through the STATUR connector, compare the versions after 24-72 hours and pick the winner to share with followers. Use when someone wants to post a trial reel, A/B test a hook, test a video on non-followers, schedule reels for themselves or a client, or read which reel version won.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "0.1.0"
  playbook: https://statur.co/content-testing-loop/
  connector: https://mcp.statur.co/mcp
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Trial reels: test the hook on strangers, ship the winner

Part of the Content Testing Loop (https://statur.co/content-testing-loop/). A trial reel is shown first to people who don't follow the account. Your followers don't see a weak version, and the numbers tell you which hook works on cold traffic, which is the audience that grows an account. This skill turns that into a weekly routine: same body, several hooks, one winner.

Works best with the STATUR connector for Claude (`https://mcp.statur.co/mcp`, access key included with the STATUR cookbook offer; tools `publish_reel`, `list_reels`, `reel_insights` and others), which publishes through the official Instagram API. Without it, follow the same method by hand in the Instagram app (create a reel, then turn on "Trial" before sharing) and ask the user for the numbers.

## 1. Before posting

Ask once:
- Which account (own or a client's)? If several are connected, call `list_accounts` and confirm.
- What is being tested? Change **one thing** between versions: the hook (first 1-3 seconds, on-screen text, first sentence). Keep the body, length, sound and caption the same, or the result means nothing.
- How many versions (2 to 4) and when to post. Space versions at least 1 hour apart, in the account's usual posting window.
- Graduation: **MANUAL** by default, so the user decides after reading the numbers. Use **SS_PERFORMANCE** only if the user wants Instagram to share automatically with followers when a reel performs well.

The account must be a Professional account (Creator or Business). Video: MP4 or MOV, 9:16, 3 s to 15 min.

## 2. Publish

For each version:
1. Get the file. With a shell, call `create_upload_link` and run its curl command on the local file. Otherwise give the user the `upload_page` and wait for "uploaded". A public https URL also works.
2. Show the user a summary: account, version label (A, B, C), hook, caption, time, trial and graduation. **Publish only after an explicit yes.**
3. Call `publish_reel` with `trial: true`. Use `publish_at` for the next versions (ISO 8601 with time zone).
4. Call `get_job` until it says `published`, then give the permalink.

Keep a small table in the conversation, or in the project's content log if it has one: version, hook, job_id, media_id, posted at.

## 3. Read the result (24 to 72 hours later)

Call `list_reels` (or `reel_insights` per media_id). Compare the versions on:

| Signal | Metric | Why it matters |
|---|---|---|
| Distribution | `views`, `reach` | Did Instagram keep pushing it to strangers? |
| Hook holds | `ig_reels_avg_watch_time` ÷ video length | People stayed past the first seconds |
| Worth sending | `shares` ÷ `reach` | The strongest growth signal on cold traffic |
| Worth keeping | `saved` ÷ `reach` | Value, for educational content |

Rules:
- Compare versions posted in the same window. If one version has under ~300 views after 48 hours, say the test is not readable yet. Don't crown a winner on noise.
- Pick the winner on watch-time ratio and shares per reach first, then views. Say the margin plainly ("B kept people 1.4× longer, with twice the shares per reach").
- Then tell the user how to graduate it: in the Instagram app, from the trial reel's menu, share it with followers. The API can't do it. Leave the losers as trials.
- Write down the lesson as a sentence about hooks ("a question on screen beat a bold claim for this audience"). That sentence is the real output; reuse it in the next brief.

## 4. For agencies

Each client connects their own account through a link from `connect_account_link` (valid 7 days, works once). Always name the account in summaries, and never cross-post between accounts without the user saying so.

## Limits

- 100 API posts per account per 24 hours (`publishing_limit`).
- Uploaded videos are kept 3 days, so schedule uploaded files within 70 hours.
- Instagram decides who sees a trial reel and can change the feature. If results look odd, check in the app that the reel is marked as a trial.

## Credit

The trial-reel A/B test of a hook comes from a public workflow shared by Angus Sewell (Angus the Nontechnical, TikTok, 2026-10-22), credited on the Content Testing Loop card. Written here from scratch, in our own words.

## Rules

- Publish only after the user approved each post: account, video, caption, time, trial and graduation. Never publish on an account the user did not name.
- Never ask for a password and never sign in for the user. Accounts are connected by their owner through Instagram's own login. Respect Instagram's terms and community guidelines.
- No promised views or results. No invented numbers: every figure comes from the account's insights or numbers the user provides.
- Flag anything confidential (customer names, revenue, internal decisions) before it goes into a caption.
