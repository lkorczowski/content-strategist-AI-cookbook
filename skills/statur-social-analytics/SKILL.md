---
name: statur-social-analytics
description: Build and run your own short-form analytics base in plain files that your AI can query, without a paid tracking tool. Collect views, retention, audience and daily account stats from TikTok, Instagram, Facebook and YouTube (official APIs, native exports, or the analytics screens you already see in your browser), keep every reading in git, watch competitor accounts, keep proof screenshots of your viral videos, and answer questions in SQL (which formats win, which videos crossed 100k at day 7, how a month compares). Use when someone wants to track their own short-form metrics, monitor accounts, count total views across accounts, keep analytics screenshots, or feed their format review, post-mortems and clip plans with real data.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/blog/own-your-social-media-analytics/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# STATUR social analytics

A paid tracking tool keeps your history in its database, breaks when a platform renames a metric and stops when the card expires. This skill keeps your numbers where you keep your code: CSV files in a private git repository, rebuilt into a SQLite database your AI can query. The platforms stay the source; your repository becomes the memory.

This skill has one job: measure and store. It never decides what to post. It hands its data to the skills that decide (see "Hand-offs").

## 0. Read the context first

Look for a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md). Read which accounts are owned, which are clients, which names may appear in public, and which numbers are allowed in public. Ask once for what is missing.

## 1. Set up the base (once, 15 minutes)

1. Pick the folder: `content/analytics/` in the company's private repository (blueprint layout), or any private folder under version control.
2. `python3 scripts/analytics.py init content/analytics` creates `accounts.csv`, `formats.csv`, `raw/` and `proof/`.
3. Fill accounts.csv with the user, one row per account: owned accounts, client accounts and a short watchlist (5 to 20 accounts). For each, the route (references/routes.md), the working window and the attribution. Columns: references/schema.md.
4. Ask which route the user accepts for each platform, best first: official API, native export, reading the analytics screen in the user's own browser, public pages for the watchlist, screenshots. Write it in the `route` column.

## 2. Collect

One collection = one raw file, named `YYYY-MM-DD_<platform>_<handle>_<kind>.csv`, kind `videos`, `daily`, `retention` or `audience`. Columns: references/schema.md. Never edit a raw file afterwards: the next reading is a new file, and the database keeps the latest reading of each video while the raw table keeps the whole history.

- First pull per owned account: every video, 365 days of daily stats where the platform shows them, and for each video above the viral line, its first 7 days, retention and audience.
- Then weekly: the last 14 days of daily stats and the videos of the last 30 days. Daily granularity does not need a daily run when the platform returns the history day by day.
- Watchlist: public counts once a week or once a month, at a human pace (references/routes.md, route 4).
- Then `python3 scripts/analytics.py build content/analytics`, and commit with a message like `analytics 2026-W44`.

## 3. Proof screenshots

The viral line defaults to 100,000 views at day 7 (agree another line with small accounts). For each video above it, keep two screenshots of the platform's own analytics: the overview and the audience tab, in `proof/<platform>_<handle>/<video_id>_<tab>_<YYYY-MM-DD>.png`. `python3 scripts/proof.py IN OUT --box x0,y0,x1,y1` blurs the caption, thumbnail and handle for a copy you can show without naming the account. Keep both. A screenshot taken months later shows a different number, so take it once the video is 7 days old.

## 4. Ask questions

- `python3 scripts/analytics.py sql content/analytics "<query>"` runs any read-only SQL. Ready questions: references/queries.md.
- `python3 scripts/analytics.py dice content/analytics --account <key>`: per format, on mature videos, the floor, the 25th percentile, the median, the 75th percentile and the top, plus saves and shares per 1,000 views and 3-second retention.
- `python3 scripts/analytics.py winners content/analytics --account <key>`: each mature video against its own format's median, top and bottom of the list.
- `TOTALS.md`: views counted per account and in total, with the views still waiting for a window decision. Watchlist accounts are listed and never counted.

Answer with the query and its result, in plain words, and say which data is immature, rounded or missing.

## 5. Hand-offs (single responsibility)

This skill measures. Each decision belongs to one other skill, which reads this base instead of asking for numbers again:

| Question | Skill | What it reads here |
|---|---|---|
| Why did this video lose people, and how to re-edit it? | video-post-mortem | `export-log` output, the video's retention rows |
| Which formats do I keep, change or drop? | format-dice-review | the `dice` table and `video_log` with the format column |
| What has my history taught me this month? | content-learning-session | `video_log` over the whole history |
| Which format is this winner, and what do I script next? | format-library-coach | winners and their captions; it writes the format into formats.csv |
| Which moments of my live or long video become clips? | statur-clipping, clip-plan | the winning formats and hooks of the account |
| How do I write a script that replays a winner's structure? | video-story-analysis, short-video-author-analysis, story-replication, short-story-replication | the winners list (own or watched) as the videos to analyse |
| Which organic winners go into ads? | organic-to-paid | the winners list with saves and shares |

Install the others from the same repository. A private instance may add its own collectors in a separately named private skill that extends this one; it never forks it.

## 6. Weekly routine (optional)

A scheduled task on the user's computer, with the browser the user signed in to: collect (section 2), take the missing proof screenshots (section 3), build, commit, then write a five-line digest as a draft: total counted, videos that crossed the line this week, accounts that need a new sign-in. Test it once with the user before scheduling, and only schedule it if it runs without the user.

## Rules

- Drafts only: the assistant never sends, posts, schedules or deletes anything for the user. It never likes, follows or comments while reading a page.
- No passwords: the user signs in in their own browser. Never ask for a password, never copy cookies or tokens.
- No promised views or results, and no invented numbers: every figure comes from a raw file with its reading date and source. Rounded public counts stay labelled as rounded.
- Respect each platform's terms of use: official APIs and exports first, human pace on any page, no bulk or parallel collection, a short watchlist only.
- Client numbers and screenshots stay in the private repository. Public proof uses blurred copies and only accounts marked `named` or `anonymous` in accounts.csv.
