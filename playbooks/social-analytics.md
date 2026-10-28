# STATUR social analytics

Own your short-form analytics: views, retention, audience and daily account stats from TikTok, Instagram, Facebook and YouTube, kept in plain files in your own repository and queried by your AI, without a paid tracking tool.

- Page (human version, source of truth): https://statur.co/blog/own-your-social-media-analytics/
- Markdown for AI assistants: the skill folder below (blog posts have no markdown twin yet)
- Version 1.0, 2026-10-26; skill statur-social-analytics 1.0.0

## Summary

One folder in a private git repository: accounts.csv (owned, client and watched accounts, with your working window and what may be shown in public), raw/ (one CSV per collection, never edited), proof/ (two analytics screenshots per viral video, blurred copies for public use). A script rebuilds a SQLite database from the files, so any AI can answer "which formats win", "which videos crossed 100k at day 7" or "how did this month compare" in SQL. Collection routes, best first: official APIs, native exports, the analytics screen you already see in your own browser read at a human pace, public counts for a short watchlist, screenshots. The skill measures; the Content Testing Loop, the Format Library, Video Script Structure, STATUR clipping and statur-organic-to-paid decide and make, reading the same base.

Built from a real collection on October 25, 2026: a founder TikTok account (238 videos, 365 days of daily stats, retention and audience of two videos above 100k views), a YouTube channel, a Facebook page and Instagram reels.

## Skills

| Skill | Use it for |
|---|---|
| [statur-social-analytics](../skills/statur-social-analytics/) | Set up the base, collect, build, query (sql, dice, winners), proof screenshots, export the video log for the other skills, weekly routine. |
| [statur-share-social-media](../skills/statur-share-social-media/) | Give a strategist access to Instagram, Facebook, TikTok, YouTube and LinkedIn analytics before the first review, without sharing a password in plain text. |

Works with: [statur-video-post-mortem](../skills/statur-video-post-mortem/), [statur-format-review](../skills/statur-format-review/), [statur-content-learning](../skills/statur-content-learning/), [statur-format-library](../skills/statur-format-library/), the Video Script Structure skills, [statur-clipping](../skills/statur-clipping/) and [statur-organic-to-paid](../skills/statur-organic-to-paid/). Who does what: [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md), section 8.
