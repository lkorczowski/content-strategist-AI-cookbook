# Schema of the analytics base

Plain CSV files are the source of truth. `scripts/analytics.py build` turns them into `analytics.db` (SQLite) for queries. Delete the database at any time: it is rebuilt from the files.

## Folder

```
analytics/
  accounts.csv        one row per account you track or watch (the only file you edit by hand)
  formats.csv         video_id -> format, hook_type (written during the format review)
  raw/                one file per collection, named YYYY-MM-DD_<platform>_<handle>_<kind>.csv, never edited
  proof/              analytics screenshots, <platform>_<handle>/<video_id>_<tab>_<YYYY-MM-DD>.png
  proof_anon/         blurred copies safe to show in public
  analytics.db        generated
  TOTALS.md           generated
```

Put the folder in a private git repository (the blueprint's `content/analytics/`): every collection becomes a commit, so the history survives any tool, subscription or account change.

## accounts.csv

| Column | Values | Meaning |
|---|---|---|
| key | short id | used everywhere else (e.g. `me-tiktok`) |
| owner | text | person or company behind the account |
| platform | tiktok, instagram, facebook, youtube, linkedin, x | |
| handle | without @ | must match the handle in raw file names |
| relation | own, client, watch | own and client accounts can be counted; watch accounts never are |
| access | owner, manager, editor, business-suite, none | what the analytics screen lets you see |
| route | studio, api, export, public, manual | how the numbers are collected (references/routes.md) |
| window_start, window_end | YYYY-MM-DD | the period you worked on the account; empty end = ongoing |
| attribution | full, window, tbd, none | full = all videos count; window = only videos published in the window; tbd = waiting for your decision; none = never counted |
| publish | named, anonymous, none | whether the account may be named in public proof |
| notes | text | |

## Raw kinds

`videos`: video_id, posted, length_s, views, likes, comments, shares, saves, new_followers, avg_watch_s, ret_3s_pct, ret_10s_pct, ret_end_pct, views_d7, caption, url. Missing columns are allowed. Rounded counts such as `318k` or `1.2M` are read as numbers and stay marked as rounded in your notes.

`daily`: date, views, profile_views, likes, comments, shares, followers, reached. One row per day of the account.

`retention`: video_id, second, pct_remaining. A few fixed points are enough (0 to 6, 8, 10, 12, 15, 20, 30 seconds, then every 15 to 30 seconds, and the last second).

`audience`: video_id, dimension (age, gender, country, traffic), label, pct. Leave video_id empty for account-level audience.

## Views in analytics.db

- `videos`: the latest reading of each video, with `days_live` computed from the reading date.
- `daily`, `retention`, `audience`: the latest reading of each row.
- `raw_videos`: every reading, so you can follow a video from day 1 to day 30.
- `video_log`: the exact columns of `video-log.csv` read by video-post-mortem, format-dice-review and content-learning-session.
- `formats`, `accounts`: the two hand-made files.
