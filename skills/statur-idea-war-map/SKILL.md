---
name: statur-idea-war-map
description: Map the ideas fighting in an online controversy (a meme war, a political clash, a brand crisis) from its most viewed posts. Reads each post with its image or video, writes the implied idea, induces the contested concepts, assigns each post a camp and a community, measures quote duels with the reach ratio and an Elo rating, and outputs a map of ideas with third parties made visible. Use when someone asks why an idea went viral, which side is winning a war of ideas, who the third parties are, or how a trend spread across languages.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/how-ideas-go-viral/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Idea war map

Part of the dossier How Ideas Go Viral on Social Media (https://statur.co/how-ideas-go-viral/). Read https://statur.co/how-ideas-go-viral.md for the worked example and its sources when you can open links.

The job: turn a few hundred viral posts into a short list of ideas in conflict, show which camp each idea serves, which ideas win when they answer each other, and who else joined the fight. Views decide what counts. The hidden meaning of each post decides where it goes.

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

## Step 3 · Induce the concepts

1. Read all the implied ideas and propose concepts: contested grounds that both camps can hold ideas about ("who owns anime", "who started it"). A concept is not a camp.
2. Write each concept as a short label and one inclusion rule.
3. Assign every post to one concept. Merge concepts with fewer than 3 posts, split concepts that mix two arguments.
4. Show the list to the human and apply their edits before measuring anything.

Expect 15 to 25 concepts for a few hundred posts. Plan for surprises: in the worked example, the spectators' verdict, auto-translation and old grudges were not in the first hypothesis list.

## Step 4 · Label camp, community, register and relation

Use templates/annotations.csv. For each post:
- side: the camp the idea serves (one code per camp, plus NEU for neutral, confused or meta posts).
- community: who posts, from language and self-identification (FR, JA, EN, AR...). A post in one language can serve another camp. Someone can post in French while being an English speaker who says so.
- register: humor, insult, argument, info, testimony, meta.
- rel, for quotes only: rebut (another idea against the original), amplify (same camp, new angle), verdict (a spectator judging the fight), restate.

The camp is a reading of the post. Never infer or state the ethnicity, religion or nationality of a person.

## Step 5 · Measure

Run `python3 scripts/idea_map.py templates/annotations.csv templates/concepts.csv --out map.json`. It computes:
- Reach of each concept: sum of the views of its posts, and the share serving each camp.
- Duels: for every rebuttal, ratio = views of the answer / views of the original. Above 1, the answer won.
- Elo of each concept: every rebuttal between two concepts is a match, in date order, K = 32, start 1,500. The answer wins the match when its ratio is above 1.
- Third-party share: views posted by communities outside the main camps.

Read the numbers before writing anything:
- An idea with high reach and a low Elo travels but loses when answered.
- A small idea with a high Elo is a correction or a counter that people trust.
- A concept owned by a third party is the outsider to watch.

## Step 6 · Map and report

1. Place each concept on a "battle lines" axis: the share of its views serving each camp (left camp left, right camp right, neutral in the middle). Size by reach.
2. Optional "idea space": embed the implied ideas with a sentence model, average them per concept, and place the concepts by metric MDS on cosine distance (the intertopic map of LDAvis).
3. Report in this order: who won the attention, which ideas carried it, the biggest duels, the third parties, the origin of the conflict, the method and its limits.

Automation note from the worked example: clustering raw post text with a sentence model recovers almost none of the concepts (adjusted Rand index 0.11). Clustering the implied ideas reaches about 0.2. The jump to clean concepts needs the reading of Step 2 and the human check of Step 3. Keep both.

## Rules

- Drafts only. Never post, reply, quote or send on the user's behalf.
- No passwords: the user signs in to the platform and to any API console.
- No promised views or results. A map explains what happened; it predicts nothing.
- No invented numbers: every view count comes from the platform, with its reading date.
- Never publish post text, slurs or private individuals' data. Paraphrase ideas neutrally, count insults without linking them.
- Respect the platform's terms: read with the user's own account at a human pace, and keep raw data private.
