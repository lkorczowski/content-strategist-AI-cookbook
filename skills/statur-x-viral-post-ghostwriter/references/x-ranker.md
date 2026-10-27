# What X's ranker counts

Single reference for X ranking facts in this repository. Other skills (statur-x-launch, statur-hook-forensics) link here instead of repeating it. Last checked: 2026-10-27.

## Primary source

X published the code of its For You ranker, built on a Grok-based model, in the repository xai-org/x-algorithm. The file home-mixer/params/param.rs lists the default weight of each predicted action. Each weight multiplies the predicted probability that a viewer takes that action, and the weighted sum ranks the post for that viewer.

- Code: https://github.com/xai-org/x-algorithm
- Weights: https://raw.githubusercontent.com/xai-org/x-algorithm/main/home-mixer/params/param.rs

The file says it mirrors "config feature-switch defaults", so X can change any value without a new commit. Treat the numbers as the published defaults on the reading date.

## Default weights (read 2026-10-27)

| Predicted action | Weight |
|---|---|
| Copy the post's link (share via copy link) | 20.0 |
| Reply | 5.0, plus a 15.0 boost when author and replier follow each other |
| Quote | 5.0 |
| Share via DM | 5.0 |
| Follow the author | 4.0 |
| Share (other) | 2.0 |
| Repost | 1.0 |
| Like | 0.66 |
| Click on the post | 0.3 |
| Open a link | 0.2 |
| Dwell, continuous dwell, click dwell | 0.05, 0.006, 0.4 |
| Profile click | 0.0 |
| Not interested | -52.272 |
| Mute author | -58.8 |
| Block author | -31.2 |
| Report | -234.0 |

The file also notes that the baseline probability of a report is more than 1,000 times lower than a like, so large negative weights act on rare events.

## What it means for a writer

- A post earns reach when it makes people reply, quote, follow or send the link to someone. A like is worth about an eighth of a reply.
- A profile click earns nothing in ranking. A business still needs it, so measure it yourself (statur-social-analytics).
- Conversations with people who follow you back weigh the most: the reply boost for mutual follows is three times the base reply weight.
- One "not interested" costs about as much as 80 likes. Bait that annoys the wrong reader costs reach.
- Opening a link carries a small weight (0.2). The common advice to put the link in the first reply comes from practitioners, not from this file.

## The 2023 code, for comparison

The 2023 release (twitter/the-algorithm-ml, projects/home/recap/README.md) weighted a "good profile click" at 12.0 and a reply engaged by the author at 75.0. Articles that quote those numbers in 2026 describe a ranker X has replaced.

- https://raw.githubusercontent.com/twitter/the-algorithm-ml/main/projects/home/recap/README.md

## Third-party readings

Use them for context, never as the source of a number: they quote the code, sometimes an older version.
- PPC Land: https://ppc.land/xs-algorithm-source-code-drops-what-it-reveals-about-the-platforms-feed-mechanics/
- Buffer: https://buffer.com/library/twitter-timeline-algorithm/
