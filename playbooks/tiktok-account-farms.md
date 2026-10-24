# TikTok account farms: the account network playbook

How startups run dozens to hundreds of TikTok and Instagram accounts to sell apps, what actually works in that playbook, what TikTok, Meta and the FTC allow, and a six-step version that keeps the method (format testing at volume, one person creating, several people publishing) and drops the disguise (fake customers, planted comments, accounts built to look unconnected).

- Page (source of truth): https://statur.co/tiktok-account-farms/
- Markdown for AI assistants: https://statur.co/tiktok-account-farms.md
- Theory (essay): https://louis-korczowski.org/manage-1000-tiktok-accounts-solo
- Version 1.0, 2026-10-24

## Summary

Check the fit first: networks sell products whose value shows on screen in seconds. Scout proven photo-slideshow formats from the last 90 days, produce 40 posts per format with your own images, and test them on two accounts, 20 posts each. Judge each format on its median against each account's own baseline on day 7, and treat outliers as hypotheses. Convert with real proof: the App Store slide, the demo trick, a pinned comment. Scale with people whose accounts say who they work for, and judge the network every month on the cost per customer who stays.

## Skills

| Skill | Use it for |
|---|---|
| [account-network-coach](../skills/account-network-coach/) | Decide if a network fits, scout formats, design and read the two-account test, scale with disclosure, audit a posting-network vendor. |
| [slideshow-maker](../skills/slideshow-maker/) | Render 40 photo slideshows (TikTok, Instagram) or PDF carousels (LinkedIn) from a CSV of slide texts, with a Python script. |

Companion skills from other playbooks: [format-dice-review](../skills/format-dice-review/) to judge the formats, [comment-section-coach](../skills/comment-section-coach/) for the demo trick and replies, [performance-creator-program](../skills/performance-creator-program/) to pay creators who post from their own accounts, [organic-to-paid](../skills/organic-to-paid/) to turn the winners into ads.

## Tools we checked (2026-10-24)

- [Larry](https://clawhub.ai/olliewazza/skills/larry), Oliver Henry's slideshow agent (MIT-0): a reference workflow for slideshows on one account. Before reusing it, render 1080x1920 JPEG, label photorealistic AI images, and keep API keys out of plain-text config files.
- [Postiz](https://github.com/gitroomhq/postiz-app) (AGPL-3.0) and [Upload-Post MCP](https://github.com/Upload-Post/upload-post-mcp) (MIT): publish photo posts through TikTok apps that passed TikTok's audit, with APIs and MCP servers.
- [marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT): hook formulas, App Store optimization and A/B test design that pair well with these skills.
- Avoid: fleets of look-alike accounts, proxies, antidetect browsers, device farms and warm-up bots. They match TikTok's definition of spam.
- Read every third-party skill and its scripts before installing: in February 2026 researchers found 341 malicious skills among 2,857 audited on ClawHub ([The Hacker News](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)).

## Credit

Triggered by a public video by Miles Feldstein, co-founder of Human Post (X, 2026-10-23): https://x.com/MilesFeldstein/status/2113676914279755947. From his protocol we kept the reference bar (photo slideshows above 25,000 views in the last three months), the test size (40 posts, two accounts, 20 posts each), the separation of the person who creates from the people who post, and the App Store proof slide. We changed the winner rule (median against each account's baseline instead of outliers or a fixed 2,000-view bar), replaced planted comments with the demo trick, and replaced accounts built to look unconnected with labelled accounts and disclosed creators. The skills are written from scratch, in our own words.
