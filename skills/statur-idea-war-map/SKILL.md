---
name: statur-idea-war-map
description: Map the beliefs fighting in an online controversy (a meme war, a political clash, a brand crisis) from its most viewed posts. Reads each post with its image or video, writes the implied idea, names the beliefs people hold (never the joke format), tags each post as supporting or attacking its belief, assigns a camp and a community, measures quote duels with the reach ratio and an Elo rating, and outputs a map with third parties made visible. Use when someone asks why an idea went viral, which side is winning a war of ideas, who the third parties are, or how a trend spread across languages.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.1.0"
  playbook: https://statur.co/how-ideas-go-viral/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Belief war map

Part of the dossier How Ideas Go Viral on Social Media (https://statur.co/how-ideas-go-viral/). Read https://statur.co/how-ideas-go-viral.md for the worked example and its sources when you can open links.

The job: turn a few hundred viral posts into a short list of beliefs in conflict, show which camp each belief serves, whether its supporters or its attackers won, which beliefs win when they answer each other, and who else joined the fight. Views decide what counts. The hidden meaning of each post decides where it goes.

The core rule: an idea is what people believe ("The Japanese are suicidal", "It's a Muslim invasion"). A joke, an argument, a testimony, a statistic or a politician's statement is only the packaging. The same belief can travel in every one of them, and a fact-check that attacks it belongs to it too.

## What to ask for

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing.

Ask once, then work with what the user gives you:
- The controversy in one sentence, its start date, and the camps as the user sees them (two or more).
- The platform (X, TikTok, Instagram, YouTube) and the languages involved.
- A seed list: links to the most viewed posts the user knows, or permission to search the platform in their logged-in browser.
- A view threshold for the corpus (default 500,000 views; 250,000 for third-party languages; 100,000 for a dense map).
- A budget if an API is used. Reading in the browser costs nothing; an API usually bills per post read.

## Step 1 · Collect the corpus

1. Seeds: the user's links, plus the most viewed posts found by searching each language. On X, the search operators `min_faves:`, `since:` and `lang:` with the Top tab surface viral posts without an API.
2. Duels: for the 10 to 15 most viewed seeds, open the Quotes tab and keep the most viewed quotes. A quote is someone answering a post with their own idea.
3. Third parties: search the controversy in every language that shows up in the quotes (English, Arabic, Spanish, Portuguese, Thai, Korean, Chinese in our worked example).
4. Keep for each post: id, handle, language, views, likes, date, media type, the post it quotes, and a local copy of its image or a frame of its video.
5. Exclude posts that mention the camps without the controversy (a travel anecdote, unrelated news). Log every exclusion with its reason.

Raw text and media stay in a private folder. They never go in a public file.

## Step 2 · Read each post with its picture

The joke often lives in the image or the video. For every post:
1. Look at the media. For a batch, build contact sheets (9 images per sheet, labelled with handle and views) and read them sheet by sheet. For the top videos, open the post and capture two or three frames.
2. Write a literal caption: what is said and shown.
3. Write the implied idea in one neutral sentence: the claim the post makes, including the meaning of the joke. "His feet do not touch the ground" is a suicide joke. "Vegeta eats a whole pig" is an argument about Islam.
4. Give a confidence from 1 to 3. Every 1 goes to the human review list.

## Step 3 · Name the beliefs

1. Read all the implied ideas and group them into beliefs: something a person can hold, written as a short sentence ("The Japanese are suicidal", "The media hide the truth"). Never name a belief after its format ("Suicide jokes", "The spectators' verdict").
2. Test every label with four questions. Rewrite it until all four answers are yes:
   - Can someone say "I believe that ..." before it?
   - Can a joke, a serious argument, a debunk and a politician's statement all be about it?
   - Can one post support it and another attack it?
   - Is it free of format words (joke, meme, verdict, question)?
3. Give each belief an owner: the camp whose voice it serves. Posts with no belief (pure questions, "why are they fighting?", insults with no claim) go to an X bucket with no owner and stay off the rope.
4. Assign every post to one belief. A correction is not a belief of its own: official arrest data that answers "It's a Muslim invasion" is the attacking side of that belief. Merge beliefs with fewer than 3 posts, split a belief whose posts defend two different claims.
5. Show the list to the human and apply their edits before measuring anything.

Expect 15 to 20 beliefs for a few hundred posts. Plan for surprises: in the worked example, "France won the meme war" and "Auto-translation turned X into a battlefield" were not in the first hypothesis list.

## Step 4 · Label stance, camp, community, register and relation

Use templates/annotations.csv. For each post:
- stance: supports, attacks or neutral toward the post's belief. A Japanese post citing arrest statistics attacks "It's a Muslim invasion"; a joke about the same rioters supports it.
- side: the camp the post serves (one code per camp, plus NEU for neutral, confused or meta posts).
- community: who posts, from language and self-identification (FR, JA, EN, AR...). A post in one language can serve another camp. Someone can post in French while being an English speaker who says so.
- register, the packaging: humor, insult, argument, info, testimony, meta. Keep it apart from the belief.
- rel, for quotes only: rebut (another idea against the original), amplify (same camp, new angle), verdict (a spectator judging the fight), restate.

The camp is a reading of the post. Never infer or state the ethnicity, religion or nationality of a person.

## Step 5 · Measure

Run `python3 scripts/idea_map.py templates/annotations.csv templates/beliefs.csv --out map.json`. It computes:
- Reach of each belief: sum of the views of its posts, the share serving each camp, and the views that support or attack it.
- Duels inside a belief: when a supporter and an attacker quote each other, which one reached more people.
- Duels: for every rebuttal, ratio = views of the answer / views of the original. Above 1, the answer won.
- Elo of each belief: every rebuttal between two beliefs is a match, in date order, K = 32, start 1,500. The answer wins the match when its ratio is above 1.
- Third-party share: views posted by communities outside the main camps.

Read the numbers before writing anything:
- A belief with high reach and a low Elo travels but loses when answered.
- Attackers who win the duels inside a belief while supporters keep most of the views: the facts won the argument and lost the reach. Report both numbers.
- Compare the registers inside one belief: if it reaches as much with jokes as with arguments, the joke is only its vehicle.
- A belief owned by a third party is the outsider to watch.

## Step 6 · Map and report

1. Place each belief on a "battle lines" axis: the share of its views serving each camp (left camp left, right camp right, neutral in the middle). Size by reach.
2. Optional "idea space": embed the implied ideas with a sentence model, average them per belief, and place the beliefs by metric MDS on cosine distance (the intertopic map of LDAvis).
3. Report in this order: who won the attention, which beliefs carried it and with which packaging, supporters against attackers, the biggest duels, the third parties, the origin of the conflict, the method and its limits.

Automation note from the worked example: clustering raw post text with a sentence model recovers almost none of the beliefs (adjusted Rand index 0.11). Clustering the implied ideas reaches about 0.2. The jump to clean beliefs needs the reading of Step 2 and the human check of Step 3. Keep both.

## Rules

- Drafts only. Never post, reply, quote or send on the user's behalf.
- No passwords: the user signs in to the platform and to any API console.
- No promised views or results. A map explains what happened; it predicts nothing.
- No invented numbers: every view count comes from the platform, with its reading date.
- Never publish post text, slurs or private individuals' data. Paraphrase ideas neutrally, count insults without linking them.
- Respect the platform's terms: read with the user's own account at a human pace, and keep raw data private.
