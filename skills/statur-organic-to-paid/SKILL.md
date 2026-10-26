---
name: statur-organic-to-paid
description: Turn proven organic short-form videos into ads. Shortlist winners at 48 hours against each format's usual results, check they fit paid (cold viewer, offer, claims, rights), keep the hook and make minimal edits, test each winner against the current best ad on cost per new customer, then feed the ad results into the next production day. Use when someone asks which TikToks, Reels or Shorts to boost, how to turn organic content into ad creatives, how to handle creative fatigue or how to connect organic and paid.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "2.0.0"
  playbook: https://statur.co/blog/organic-winners-cheaper-ads/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Organic to paid

Part of Organic winners make your ads cheaper (https://statur.co/blog/organic-winners-cheaper-ads/).

The job: let the platform test hooks for free in organic, then give the ad budget to videos whose hook already held strangers. Every organic post is a free experiment: the algorithm shows it to a small audience, measures how long people stay and decides whether to push further. An ad made from scratch carries none of that proof, so the budget pays to find out. This skill runs organic and paid as one pipeline: volume, a data loop that spots winners, a handoff to paid, and ad data back into the next production day.

## What to ask for

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing.

Ask once, then work with what the user gives you. Accept a pasted table, a CSV or screenshots.
- Organic, one row per video: format, platform, publish date, reading date, views, retention at 3 s, average watch time, saves, shares, comments, new followers.
- The format's usual results: the same metrics for earlier videos of the same format on the same account.
- Paid: the current best ad over a stated period (spend, impressions, CPM, clicks, new customers, cost per new customer), the audience, the optimization event and the budget available for a test.
- Rights: who appears on screen, who owns the posting account, the music and any third-party footage.
- The offer and the page the ad sends to.

## Steps

1. Check the volume. One video teaches nothing. Patterns show when the account has a batch of the same format, and one production day a month gives a full batch. With fewer than 5 comparable videos, the shortlist is descriptive only, and you say so.
2. Read at 48 hours. Compare each video with its own format on the same account: views on a log scale against the format's median and 25th to 75th percentile range, retention at 3 s and watch time against the format median, saves and shares per 1,000 views. Keep each signal apart.
3. Shortlist.
   - CANDIDATE: views above the format's range and retention at 3 s at or above the format median. The hook held strangers.
   - WATCH: views above the range with weak retention, or a spike from one outside share. Read again at 7 days.
   - SKIP: inside or below the range.
4. Check paid fit for each candidate.
   - Cold viewer: the video makes sense to someone who has never seen the account.
   - Offer: the product, or the problem it solves, is visible or one step away.
   - Claims: every claim is true and allowed under the platform's ad policies.
   - Rights: written consent from everyone on screen for paid use, the creator's authorization when the post is theirs, music and footage cleared for ads.
5. Prepare minimal edits. Keep the first 3 seconds identical: that is the proven part. Allowed edits: burned-in captions, a crop that respects the platform's safe zones, one call to action at the end, a cut of an inside joke that needs the account's history, a swap of audio that is not cleared for ads. List every edit. Where the platform allows it, run the original post as the ad (for example TikTok Spark Ads, or an existing post selected in Meta Ads Manager) so its likes and comments stay visible.
6. Design the test. A is the current best ad, B the organic winner. Same audience, optimization event, placements and budget split, launched the same day. Use the platform's split test feature where available. The decision metric is cost per new customer, or the cost of the event that matters to the business. Click-through rate and cost per view are diagnostics only. Write the minimum spend or number of conversions and the reading date before launch.
7. Decide at the reading date.
   - SCALE: B beats A on the decision metric after the planned spend. Raise the budget in steps and keep A as the control.
   - EXTEND ONCE: the gap is small or the conversions are few. Run once more with the same rules.
   - STOP: B loses after the planned spend. Note what the paid audience rejected.
   Fatigue: track frequency and cost per new customer week by week. When the cost rises, the next organic winner takes the slot.
8. Feed the loop. Log each ad with its format, its opening line, its organic numbers and its ad numbers. Organic shows which hooks hold attention. Paid shows which hooks convert. Bring both into the next production day: more of the winning formats, variations of the winning hook.

Optional estimate: organic views / 1,000 x the account's own CPM gives what the same reach would have cost in ads. Use the user's CPM only. Without it, leave a placeholder.

## Output

```
ORGANIC TO PAID · <account> · <period> · videos read: <n> · comparable per format: <n>
Shortlist at 48 h:
<video | format | views vs format range | 3 s retention vs median | saves/1k | shares/1k | CANDIDATE, WATCH or SKIP | reason>
Paid fit: <video | cold viewer | offer visible | claims allowed | rights: people, creator, music, footage>
Edits for paid: <video | first 3 s unchanged yes/no | edits>
Test: A <current best ad> vs B <organic winner> | audience | event | budget split | minimum spend or conversions | reading date
Decision metric: cost per new customer | A: <value> | B: <after reading>
Decision: SCALE | EXTEND ONCE | STOP · <reason>
Reach value (optional): <views> / 1,000 x <user CPM> = <value>
Back to production: <formats and hooks to produce more of, variations to try>
What the data cannot tell: <limits>
```

## Rules

- Drafts only. Never launch, boost, publish, send, comment, reply, edit a live ad, change a budget or spend money for the user. Spend starts only after the user's explicit go.
- Never ask for a password and never sign in for the user. Work from exports, screenshots or numbers the user provides, or from official platform APIs the user has connected.
- Respect each platform's terms of use, ad policies and disclosure rules. Content made by a creator or a customer runs only with their written consent and the platform's paid partnership label or authorization flow.
- No promised views, costs or results. An organic winner raises the odds. The test decides.
- No invented numbers: every figure comes from the user's data or a source the user can open. Unknown values stay placeholders.
- Flag anything confidential (customer names, revenue, internal decisions) before it goes into an ad.
