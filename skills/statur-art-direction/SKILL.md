---
name: statur-art-direction
description: Build an art direction that does not look AI-made, starting from 5 to 15 images the owner loves (tattoos, posters, engravings, photos, packaging). Read the images, list the AI design tells to refuse, turn the images into tokens (palette, type, one signature gesture, real texture), write DESIGN.md and tokens.json, build a one-page specimen with real blocks, then test it. Use before building a website, a deck or a social template, when a site "looks like every Claude site", or when the owner says the visuals feel generic.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/tradespeople-video-handbook/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Art direction from images you love

The job: give a business a visual identity that reads as theirs, not as the default look of an AI tool. The raw material is not a style name ("modern, clean"). It is a handful of images the owner already loves, plus the real texture of their trade (their photos, their handwriting, their materials). The output is a short written direction and a token file that every later tool reads: the website (statur-trades-site), carousels, quotes, thumbnails.

Method used to rebuild the statur.co identity in November 2026: tattoo flash and old engravings as references, a written list of refused AI tells, then one signature gesture. It took one session.

## Single responsibility

This skill writes the art direction (DESIGN.md, tokens.json, specimen.html) and audits pages against it. It never builds the site (statur-trades-site does), never writes the copy, never picks the business positioning (read it from the company context file).

## 0. Read the context first

Read the company context file (kb/01_BRAND.md, kb/01_ENTREPRISE.md or .agents/product-marketing.md): trade, ideal client, tone, logo if any, what the owner already decided. Keep what is decided. If a DESIGN.md exists, audit it instead of starting over.

## 1. Collect the images (owner, 10 minutes)

Ask once, in plain words:
- "Send me 5 to 15 images you love, not necessarily from your trade: a tattoo, a poster, a label, an old drawing, a photo, a shop front. What matters is that they make you stop."
- "Send 5 to 10 of your own photos: jobs, tools, materials, hands at work, before and after."
- "Do you have a logo or colours you want to keep?"

Ask where the images can be read (a Drive folder, the chat, a local folder). Media stays in the owner's Drive or local folder, never in a public repository. The reference images are inspiration only: never trace, copy or reproduce an artist's work, and never put it on the site.

## 2. Read every image (assistant)

For each image, write 4 short lines in a notes file (design/notes.md):
- Line: thick or fine, steady or shaky, dotted, hatched, engraved, brush.
- Light and texture: paper, grain of the material, flat colour, shadow, halo.
- Colour: the 2 or 3 colours that carry it, with an approximate hex. Say "approximate".
- The motif or gesture that makes you remember it (a circle drawn by hand, a stamp, a dotted bust, a hand-lettered word).

Then write a 5-line synthesis: what the images share. Show it to the owner and ask "is that what you like in them?". Their correction is worth more than your reading.

## 3. Write down what to refuse

Copy this list into DESIGN.md as "Refused". These are the most cited tells of AI-made sites in 2025-2026 (research of 2026-11-13, sources in the statur.co Brand Carnet notes). A page may break one rule only if the owner's images clearly ask for it.

1. One warm accent (terracotta, rust, orange) on a near-black or cream background.
2. One word of the headline in colour, italic or bold.
3. Small spaced capitals above every heading (eyebrow labels).
4. Monospace used for labels, navigation, footers.
5. A pill with a dot above the main title.
6. Grid lines or dot patterns fading on a dark hero.
7. Decorative numbering 01 / 02 / 03 on content that is not a sequence.
8. Centred hero: eyebrow, title, subtitle, two buttons, screenshot.
9. Inter, Geist, Space Grotesk, Instrument Serif, Space Mono, Bricolage Grotesque as the signature font.
10. Cream background plus big contrasted serif as the "human" fix (it is the other Claude look).
11. Three equal cards with an icon; the same card radius and shadow everywhere.
12. A band of giant numbers with small labels and no source.
13. Bento grids, frosted glass, purple-blue gradients, glows, fake grain.
14. Section order hero, logos, 3 features, steps, stats, testimonials, pricing, FAQ, CTA.
15. Headlines in paired fragments ("Built to last. Priced to win.") and "not X, it's Y".

## 4. Turn the images into tokens

Decide, and write each decision in one line with the image it comes from:
- Background and ink: taken from the references or the trade (paper, plaster, slate, wood), never pure white plus pure black by default.
- One accent colour, used for function only (what to remember, the call to act). Rule: at most two accent gestures per screen.
- Type: one display face that carries the character of the images, one text face that reads well, both free to use (OFL / Google Fonts). Check the licence. Avoid the fonts in rule 9. Good starting pool: IM Fell, Junicode, Cardo, Libre Caslon, EB Garamond, Cormorant, Marcellus SC, Redaction for display; Newsreader, Source Serif, Atkinson Hyperlegible, Public Sans for text. Fraunces and Newsreader are common in AI sites: fine for text, weak as a signature.
- One signature gesture, drawn from the images and repeated everywhere: a hand-drawn circle around the key number, a highlighter stroke, a stamp, a dotted outline, an engraved frame. One, not five.
- Real texture only: the owner's photos, a scan of real paper, their handwriting (a font can be made from a page of their letters later). No generated grain or fake patterns.
- Layout: built on the argument of each page, asymmetric splits allowed, the trade photos large.

Write tokens.json with the exact values (colours, fonts with their URLs, sizes, radius, spacing, the gesture rules). Every other tool reads this file; no tool keeps its own hex codes.

## 5. Build the specimen (assistant)

One HTML page, design/specimen.html, using only tokens.json, that shows the real blocks the site will need: header with logo, a hero with a real photo and the real promise, a service block, a before / after block, a review block (empty placeholder if there are no real reviews), the contact block with the phone, the footer. Real words from the context file, never lorem ipsum, never invented reviews or numbers ("to confirm" instead).

## 6. Test before showing

- Screenshot at 1280 px and 390 px wide (Playwright or Chrome). Look at both.
- Scan the HTML for the refused list: eyebrow labels, mono outside code, pills, 01/02 numbering, gradients, more than two accent gestures per screen.
- Competitor test: put the competitor's name in place of the owner's. If the page still works, it is too generic. Change the photo, the promise or the gesture.
- AI test: ask a fresh assistant "who made this page, a designer or an AI tool, and why?" with only the screenshot. Fix what it names.

## 7. Owner validation

Show the specimen (preview link or screenshots on the phone) with three questions: "do you recognise your images in it?", "would your best client trust this?", "what would you remove?". Apply, then mark DESIGN.md "validated on <date>". Only then does statur-trades-site start building.

## Files written

- design/notes.md: reading of each image and the synthesis.
- DESIGN.md: refused list, decisions with their source image, the signature gesture, do and don't examples.
- tokens.json: values read by every tool.
- design/specimen.html and its two screenshots.

## Rules

- Drafts only: nothing goes public without the owner's yes.
- Reference images are inspiration, never reproduced; no artist's work, logo or character on the site.
- No invented reviews, numbers, clients or certifications.
- Free fonts only unless the owner buys a licence; check every licence.
- No passwords; accounts are created by the owner.
