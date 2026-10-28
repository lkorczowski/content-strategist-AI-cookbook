---
name: statur-broll-find
description: Find, capture and log the pictures a short video shows on top of the speaker (B-roll): the company's own footage and past posts, crisp captures of its own pages, dashboards and repos (including pages only the user's browser can see, through a self-contained page snapshot rendered offline at 2x), stock with a license, and generated media only when the user allows it. Every asset is tied to the sentence it proves and logged with its source and rights. Use when an edit needs screenshots, article or page captures, product screens or B-roll.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/ai-video-editor/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# B-roll find

Part of the AI video editor playbook (https://statur.co/ai-video-editor/). Called by statur-video-editor-pro while it plans the edit.

## 1. From the transcript to a shot list

For each sentence of the planned edit, ask: what would prove this, or make it concrete? Write one line per need: the sentence, what to show, where it lives. A claim with a number needs its source on screen. A claim about a product needs the product. An opinion needs nothing.

## 2. Look in this order

1. The company's own footage: past recordings, lives, b-roll folders, the posters and masters of past clips.
2. Its own pages and documents: site, handbook, docs, repository, dashboards, analytics screens, posts. Use the company's knowledge base to find which page proves which claim.
3. Stock with a license (Pexels API with attribution, the company's paid library). Never for proof.
4. Generated media, only when the user turned the synthetic switch on: label the post, keep the provenance (C2PA or the generator's record).
Third-party pages, posts and articles: only with a reason (commentary, news) and the reviewer's decision.

## 3. Capture

Public page reachable from where the agent runs:

```
python3 scripts/capture.py https://example.com/page out.png --width 1280 --scale 2 [--full] [--selector CSS] [--hide CSS ...] --claim "the sentence"
```

Page only the user's browser can see (signed in, or a cloud sandbox that cannot load its styles): run `scripts/snapshot.js` in that page (an agent with a browser extension executes it; by hand: the DevTools console). It downloads one self-contained HTML file (styles, fonts and images inlined) to the Downloads folder. Then render it offline, crisp, with private parts hidden, and get the boxes to highlight:

```
python3 scripts/render_snapshot.py snapshot.html page.png --width 1100 --scale 2 --hide ".banner" --blur ".email" \
  --find "title=text:Content Strategist AI Cookbook" --boxes boxes.json --claim "the sentence"
```

The boxes are in image pixels, ready for the page_card highlights of statur-motion-design. A snapshot renders the real layout at any size, the network stays off during the render, and nothing leaves the user's computer except the file they chose to save.

Footage from a long recording (a live, a webinar): cut a few seconds with ffmpeg where the file lives, scale it down, and stage only that piece.

## 4. Log

Every capture appends a line to assets.csv: file, kind, source, title, time, owner (own or third-party), license note, the claim it supports. Stock and generated assets get the same line by hand, with their license or provenance. The edit's receipts include this file.

## Rules

- Drafts only: the agent never posts, shares or uploads anything for the user.
- No passwords: captures of signed-in pages happen in the user's own browser; the agent never asks for credentials or cookies.
- Hide or blur personal data before rendering: emails, phone numbers, customer names, private messages.
- Own material first; third-party material only with a reason and the reviewer's decision; licensed stock only; no logos or characters the company does not own.
- No invented numbers: a number on screen comes with its source.
