---
name: statur-meta-creative-targeting
description: Target Meta ads with the creative instead of narrow audiences. Audits live ads as concepts the way Meta groups look-alike ads, keeps only hard audience limits, builds a buyers by reasons-to-buy matrix, writes openings that call each buyer in three seconds, checks that every new ad changes two of four axes (message, person, setting, format), sizes the weekly batch to the budget, reads who each ad actually reached and answers creative fatigue with a new concept. Use when someone asks about Meta Andromeda, "creative is the new targeting", Entity IDs, creative similarity, creative diversification, how many creatives to run, or why many ads get no spend.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/meta-creative-targeting/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Meta creative targeting

Part of the Meta creative targeting dossier (https://statur.co/meta-creative-targeting/). Read https://statur.co/meta-creative-targeting.md for the timeline, the myths, the figures and every source when you can open links.

The job: the ad set draws the fences, the ads pick the people inside them. Meta says creative diversification is now the best lever to find the most relevant audiences, and that ads which look or feel alike are treated as variations of one creative. This skill turns that into a production plan and a weekly read.

Hand-offs:
- Campaign structure, budget per ad, test lane, offers, statics, weekly and monthly verdict: statur-meta-ads-scaling.
- New faces and handles (the "person" axis): statur-creator-program.
- Concepts proven in organic first: statur-organic-to-paid.

## What to ask for

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing.

Ask once, then work with what the user gives you (table, CSV, export, screenshots, or an official Meta connector in read-only mode):
- Live ads, last 14 to 28 days: name, spend, purchases, a thumbnail or one-line description (person on screen, setting, message, format, first line), Delivery column status.
- Ad sets: performance goal, every targeting input, budget.
- Daily budget and weekly purchases.
- Buyers' own words: reviews, sales call notes, support tickets, comments, post-purchase answers.
- Breakdowns per ad: age, gender, placement, country, with spend and purchases.

## Steps

1. Audit (recipe 01). Tag each ad: buyer, reason to buy, angle, format, person, setting. Group ads that share the same image or footage and change only text, color, music or call to action: one group = one concept. Report "N ads, M concepts" and list empty buyers and reasons. Read Delivery statuses: Creative limited (cost per result above past ads, under double), Creative fatigue (double or more). Mention the creative similarity insight in Account insights if the account shows it.
2. Fences (recipe 02). Sort targeting inputs into hard controls (location, minimum age, language, exclusions) and suggestions (detailed targeting, age range, gender, lookalikes). Propose one ad set per goal, split only when hard controls differ. Keep limits needed for shipping, law or special ad categories.
3. Matrix (recipe 03). From the buyers' words, write 3 to 5 buyers (situation first, one sentence) and 3 to 5 reasons to buy. Draw the grid, mark live concepts, pick the empty cells for the best buyers first, and write one opening line per picked cell. Use a fictional example name when the user has given none.
4. Openings (recipe 04). For each concept: 0 to 1 s who it is for (face, place, their words, a callout), 1 to 3 s their problem or desire, 3 to 15 s one proof that fits that buyer, last seconds the offer worded as on the page. One buyer per ad. Write the first line of copy and the headline for the same buyer.
5. Two of four (recipe 05). Compare every planned ad with the closest live ad on message, person, setting and format. Fewer than two changes: rewrite it, or label it an iteration for a fatigued winner. This threshold is the playbook author's working rule; Meta publishes none.
6. Batch size (recipe 06). Ads that can learn = daily budget / 7.5 (author's rule, see statur-meta-ads-scaling). Fill that number with concepts, not variations. Plan 2 to 5 new concepts a week in a test lane capped at about 20% of budget. Quote Meta's own top line when useful: at least 20 diversified ads in an Advantage+ sales campaign, 20 to 30% of budget on new ads, new ads weekly. Never above 50 ads per ad set.
7. Read (recipe 07). Per concept: intended buyer, reached buyer (from breakdowns), purchases. Unexpected buyer who buys: write a new concept for them. Cheap reach that never buys: rewrite the opening. Verdict on store orders and cost per new customer, through statur-meta-ads-scaling.
8. Fatigue (recipe 08). On Creative limited or Creative fatigue, write two materially different concepts for the same buyer (new reason to buy; new person and setting), launched next to the original. Remind the user that Meta counts all recent exposures of the image or video, including other campaigns from the same Page.

## Output

- A concept table (concept, buyer, reason, angle, format, person, setting, spend, purchases, status).
- The matrix with live, test and next cells.
- Briefs for the next batch: opening lines, proof, offer line, format, which axes change.
- A weekly read: intended vs reached buyer per concept, and the next three concepts.

## Pitfalls

- Calling "Entity ID" or a "60% similarity threshold" a Meta rule. Meta has not published either; say "Meta groups look-alike ads" and cite its December 2025 post.
- Saying targeting is dead. Hard controls still apply and decide eligibility.
- Counting AI variations, recolors or new captions as new concepts.
- Building personas from age and gender instead of situations and words.
- Pausing a winner to force spend on new concepts.

## Rules

- Drafts only. Never launch, pause, edit, duplicate or delete a campaign, ad set or ad, never change a budget, a bid or targeting, and never spend money for the user.
- Never ask for a password and never sign in for the user. Work from what the user provides or from an official connector in read-only mode.
- Respect Meta's advertising standards, special ad category restrictions and each platform's terms. Creator content runs only with the creator's permission and a clear disclosure.
- No promised costs, reach, ROAS or results. Meta's engineering gains are Meta's own measurements on selected segments; never present them as what an account will get.
- No invented numbers: every figure comes from the user's data or a source the user can open. The two-of-four axes rule and the budget / 7.5 rule are working rules of the playbook author; say so when you use them.
- Treat ad account data as confidential.
