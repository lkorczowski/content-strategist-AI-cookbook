# Collection routes, best first

Pick, per account, the first route that works and write it in the `route` column of accounts.csv. Every route keeps the user in control: the user signs in, the user approves, the agent reads.

## 1. Official API (route: api)

Stable and within the terms, but each needs a one-time setup by the user.

- YouTube Analytics API (your own channel or a channel you manage): channel and video reports, audience retention (`audienceWatchRatio`), age, gender and country, by day or month. Quota-based. https://developers.google.com/youtube/analytics
- YouTube Data API (any public channel): public view, like and comment counts per video, for the watchlist.
- Instagram and Facebook (Graph API, professional accounts): media insights. Meta renamed the core metric in 2025: `plays` and impressions were deprecated on April 21, 2025 and replaced by `views`. Keep the metric name with every number.
- TikTok: the developer APIs that return public video stats need an approved app; most founders skip this route.

## 2. Native export (route: export)

TikTok Studio, YouTube Studio and Meta Business Suite each have a download button on their analytics screens. The user clicks it and saves the file into `analytics/raw/` under the naming rule. The agent maps the columns to the raw kinds. Ask before any download.

## 3. Reading the analytics screen in the user's own browser (route: studio)

For an owned account with no API set up. The user is signed in in their own browser; a browser agent (Claude in Chrome, or any agent the user runs in their browser) opens the analytics pages the user can already see and reads them, at a human pace, the same pages the user would screenshot by hand. Rules:

- Read only. Never like, follow, comment, post, delete or change a setting.
- Never ask for a password, never copy cookies or tokens out of the browser.
- One account at a time, a few pages per minute. Stop at the first sign-in screen, error page or verification prompt and tell the user.
- What to read, and what we measured in October 2026: TikTok Studio shows account history day by day for up to 365 days, and per video the views of the first 7 days, the retention curve, viewer types, age, gender, locations and traffic sources; the per-video daily chart disappears for videos older than 365 days. YouTube Studio advanced mode lists the top 50 videos of a period and the channel total. Meta Business Suite content insights went back about 18 months on the page we tested, with the `views` metric for content published after July 31, 2025.
- Write what you read into a raw file immediately (one file per collection), then build.

## 4. Public pages (route: public), for the watchlist and for history older than the analytics screen

Public view counts are shown on profile grids (TikTok, Instagram reels tab, YouTube). Read them at a human pace, in the user's browser, for a short watchlist (5 to 20 accounts), once a week or once a month. Respect each platform's terms and robots rules; do not run bulk or parallel collection. Public counts are rounded above a threshold (Instagram shows `318k`), so they serve for comparisons and order of magnitude, not for exact totals.

Dates: a TikTok video id holds its publish time (the id shifted right by 32 bits is a Unix timestamp). An Instagram shortcode decodes to a media id whose top bits hold the time in milliseconds since August 24, 2011 (the id shifted right by 23 bits, plus 1314220021721). Both let you date a video from its link alone.

## X and other text platforms (kind posts)

- X shows per-post analytics (impressions, engagements, profile visits, link clicks, follows) in its analytics screen, and an export where the account has access. On 2026-10-27 the screen of a 20-follower account read "Detailed engagement metrics become available once you reach 50 followers": below that, read the public counts shown on each post (views, replies, reposts, likes, bookmarks) at a human pace, one reading per week.
- A post id on X holds its time: the id shifted right by 22 bits, plus 1288834974657, is a Unix time in milliseconds.
- Profile visits and link clicks carry no ranking weight on X but matter for the business. When the screen does not show them, tag every link with UTM parameters (utm_source=x, utm_content=<post id>) and read the clicks in your site analytics.
- Write one file per reading: `YYYY-MM-DD_x_<handle>_posts.csv`. Label posts (pillar, voice mode, intent reach or revenue, formula) in post_labels.csv: the writing skills fill it.

## 5. Screenshots (route: manual)

The fallback that always works, and the proof you will want anyway. For every video above your viral line at day 7, keep two screenshots: the overview (views, watch time, completion, new followers) and the audience tab. Name them `<video_id>_<tab>_<YYYY-MM-DD>.png` in `proof/<platform>_<handle>/`. `scripts/proof.py` writes a blurred copy for public use.

## Token budget for an agent

- Collect deltas: after the first full pull, read the last 14 days of the daily series and the videos of the last 30 days.
- Build the raw file inside the browser page and read it back in one go, instead of many small reads.
- Keep captions short (45 characters) and retention to about 25 fixed points.
- Two screenshots per viral video, never more. Run the weekly collection with a smaller model.
