---
name: slideshow-maker
description: Render photo slideshows for TikTok and Instagram (carousels) and PDF carousels for LinkedIn from a CSV of slide texts, with a bundled Python script (Pillow). Fits text inside the platform safe zones, reuses your own backgrounds, flags slides with too many words, and writes contact sheets and a manifest for your video log. Use when someone asks to make TikTok slideshows or Instagram carousels at volume, to produce the 40 posts of a format test, or to turn a list, a script or a thread into carousel images.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0"
  playbook: https://statur.co/PLAYBOOK_SLUG/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Slideshow maker

Part of PLAYBOOK_TITLE (https://statur.co/PLAYBOOK_SLUG/). Works for any playbook that needs carousel images.

The job: turn one format (the structure of a slideshow that already works) into many posts. The assistant writes the slide texts in a CSV, the script renders every slide in one command, and the user reviews the contact sheets and publishes by hand or through their own scheduler.

## What to ask for

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing.

- The format: links or screenshots of three to five reference slideshows, or a description. Slide count, role of each slide, words per slide, image style, last slide.
- The images: the user's own photos and product screenshots, or images they have the right to use. Put them in one folder next to the CSV.
- Platform and size: 1080x1920 (9:16, TikTok photo mode full screen), 1080x1350 (4:5, Instagram and TikTok feed), 1080x1080 (square), PDF for LinkedIn.
- How many posts, and the variable to test (the hook first).
- Fonts and colors if the brand has them (a bold .ttf or .otf file).

## Steps

1. Write the format card: number of slides, the job of each slide (hook, items, payoff, call to action), the maximum words per slide (8 to 15 reads in about two seconds), and which slide changes between variants.
2. Write the variants in a CSV, one row per slide: post_id, slide, text, image, bg, position. Use templates/slideshow-spec.csv as the model. Name posts by format and variant (habits-hook-a-01) so the video log can group them later.
3. Change one variable at a time. For a format test, keep slides 2 to the end fixed and test the hook, then the last slide.
4. Check every line before rendering. First-person claims must be true for the account that will post them. Numbers, ratings and results must come from the user's data or a source they can open.
5. Render:
   ```
   python3 scripts/make_slideshows.py posts.csv --out slideshows --size 1080x1920 --sheet
   python3 scripts/make_slideshows.py posts.csv --out carousels --size 1080x1350 --style band
   python3 scripts/make_slideshows.py posts.csv --out linkedin --size 1080x1350 --pdf
   ```
   Options: --style outline, band or plain; --font path; --darken 0 to 0.6 for photos; --format jpg, png or webp (jpg by default); --safe top,right,bottom,left margins in pixels for a 1920 px slide.
6. Review the contact sheets (contact-sheet.jpg in each post folder). Fix every warning in manifest.csv: "text does not fit" means shorten the text, more than 30 words means split the slide.
7. Hand over: the post folders, the manifest, and a caption draft per post. Copy the manifest rows into the video log so the format can be judged on day 7 (skill format-dice-review).

## Requirements

Python 3.9 or later and Pillow (`pip install Pillow`). No network access needed. The script finds a bold system font on macOS, Linux and Windows, or takes one with --font.

## Platform notes

PLATFORM_NOTES

## Rules

- Drafts only. Never publish, schedule or upload anything for the user.
- Never ask for a password and never sign in for the user.
- Respect each platform's terms of use: the user's own or licensed images only, no reposts of other creators' content, an AI-generated label where the platform asks for one, and the paid partnership label when someone is paid to post.
- No fake testimonials, fake reviews, invented ratings or results on a slide.
- No promised views or results. No invented numbers: every figure on a slide comes from the user's data or a source the user can open.
