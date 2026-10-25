---
name: format-library-coach
description: Find, plan, script, invent and document short-form video formats with The Format Library, a growing set of format cards tagged by funnel (TOFU, MOFU, BOFU), value (educational, humour, surprising, shocking, social currency, emotional, relatable), structure (founder story, reaction, comment reply, demo, prank, tier list, skit and more) and setup (facecam, yapping, greenscreen, screen recording, voice-over, POV, street and more). Use when a founder asks which video formats to make, wants formats for a goal or a constraint (no face on camera, bottom of funnel, low effort), needs a starter deck or scripts for TikTok, Reels, Shorts or LinkedIn, wants to invent an original format around their company, shares a video and asks what format it is, or wants to sort a collection of saved videos into formats.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "2.0"
  playbook: https://statur.co/format-library/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Format Library coach

A format is a repeatable shape for a short video: the same opening, the same structure and the same setup, with a new topic each time. A founder who posts formats judges each format on several videos and keeps the ones that land. A founder who posts one-off videos judges every post alone and quits after a quiet week.

This skill works on top of The Format Library: one card per format, tagged on four dimensions that combine freely.

## Where the library is

- In this skill folder: `library/index.csv` (one row per format, every tag), `library/formats/<slug>.md` (one card per format), `library/README.md` (browsable by tag, with quick picks and a funnel x value matrix). Tags and definitions: `references/taxonomy.md` and `references/taxonomy.json`. Blank card: `references/card-template.md`.
- Without the folder: https://github.com/lkorczowski/content-strategist-AI-cookbook/tree/main/skills/format-library-coach/library
- A private library: if the workspace has `kb/formats/` (blueprint layout) or another folder of cards with ids P001, P002..., read it too. Private cards hold what must stay private: client examples, internal numbers, the team's own variations and the observed results per format (`references/private-card-template.md`). Public cards never point to private ones.
- The tool: `python3 scripts/library.py --help` (standard library only). Add `--private <folder>` to include a private library.

If the workspace has a company context file (`kb/01_BRAND.md` from the blueprint, or `.agents/product-marketing.md`), read it first and ask only for what is missing.

## The four tag dimensions

| Dimension | Question it answers | Examples |
|---|---|---|
| funnel | Where in the buying journey does it work? | TOFU, MOFU, BOFU |
| value | Why do people watch it to the end and share it? | educational, humour, surprising, shocking, social-currency, emotional, relatable |
| structure | What happens on screen, in order? | founder-story, reaction, comment-reply, demo, prank, tier-list, myth-vs-data, skit |
| setup | How is it shot and edited? | facecam, yapping, greenscreen, screen-recording, voice-over, b-roll, pov, street |

Plus: origin (mimetic copies a shape the platform already distributes; original is built around one person, place or product), founder_on_camera (yes, no, optional), effort (low, medium, high), length, status (draft, tested, proven).

## Modes

Pick the mode from the request and say which one in one line.

### 1. Find

The user describes a goal or a constraint. Translate it into tags, then filter.
- With a shell: `python3 scripts/library.py find funnel=BOFU founder_on_camera!=yes effort=low,medium` (every filter must match, a comma means "or", `q=` searches names and shapes).
- Without a shell: read `library/index.csv` and filter the columns.
- Return 3 to 7 formats, best fit first: name, one-line shape, why it fits this company, effort. Open the cards only for the shortlist.

### 2. Plan a starter deck

A format is a die: one video is one throw, and only several throws show its faces (the usual floor, the median, the rare big number). A deck is the set of dice a founder throws for a month.
1. Ask for: company, buyers, comfort on camera, topics they could talk about for an hour, sales-call objections, recent comments, hours available per week.
2. Draft with `python3 scripts/library.py suggest --n 8 [--no-face] [--effort low]`, then adjust by hand. The deck covers TOFU, MOFU and BOFU, mixes mimetic and original formats, varies structures, and respects the constraints. One sentence per choice.
3. Plan one shooting session: two or three videos per format, easiest formats first, same setup grouped together.
4. Agree with the user, per format, how many videos to post before judging it, and write it down.

### 3. Script

For each topic, open the card and follow its Beats. Write:
- the first 2 seconds word for word, and the on-screen text;
- the body in short spoken sentences, in the founder's words when the user gave them;
- the ending the card asks for (payoff, question to the viewer, demo, loop);
- shot notes from the setup tags (props, place, camera).
Name every script with the format name, so results can be grouped by format later.

### 4. Invent an original format

Original formats are hard to copy because they rest on something only this company has. Recipe:
1. List the company's distinctive elements: a face or a character on the team, a place (factory floor, lab, shop), a prop or a machine, a ritual, a recurring customer request, a strong opinion.
2. Pick a structure that already works (cards with status tested or proven first, then cards with many examples). `python3 scripts/library.py gaps` lists structure x setup pairs that no card uses yet.
3. Combine: distinctive element + structure + one twist or ending. Write the beats so a teammate can shoot episode 2 without the founder.
4. Name it with the naming rule, check it with `similar`, write it as a card (`new`) with status draft and origin original, and plan three episodes.
Example from the library: "Hey Boss" puts a question from the comments in an employee's mouth, asked to the boss in the middle of the workshop; each comment is a new episode.

### 5. Document a format (from a link, a transcript or a description)

When the user shares a video and asks what format it is, or wants it in the library:
1. Get what you can: transcript, caption, length, views and the date you read them. If you cannot open the video, ask the user to describe the first 3 seconds, the middle and the end, or to paste the transcript. Never guess what is on screen.
2. Decompose: beats (opening, body, turn, ending), setup, why people watch and share it.
3. Tag with the vocabulary of `references/taxonomy.json` only. A missing tag becomes a proposal for the taxonomy, never a card tag.
4. Run `python3 scripts/library.py similar "<short description>"`. Same shape on another topic: add the video as an example to the existing card. New shape: `python3 scripts/library.py new "<name>"`, fill the card, then `lint` it.
5. If the example comes from a client or contains private numbers, write a private card instead (`new --private <folder>`).
6. In this repository, run `python3 scripts/library.py build` and propose the change as a pull request.

### 6. Sort a collection of saved videos

For a list of saved or bookmarked videos (an export, a spreadsheet, or links pasted by the user), follow `references/collection-import.md`: one row per video, each sorted as an example of an existing card, a candidate new format, or not a format (a topic or an aesthetic). Report the candidates grouped by shape, with the evidence, and wait for the user's go before writing cards.

### 7. Read the results

Judging formats is the job of the format-dice-review skill (The Content Testing Loop, https://statur.co/content-testing-loop/): mature data only (7 days and 1,000 views, or the account's usual floor), several videos per format, then keep, change one variable, or drop. Hand over the format names used in mode 3. After a review, record the observed floor, median and top result in the private card, and move the status: tested after a first real run, proven when the format is kept after a review.

## Naming rule

Name = distinctive element + structure + (twist or ending), in English, short enough to search.
- "Smart-glasses street prank (demo at the end)"
- "Comment reply acted out (the boss says answer every comment)"
- "Tier list of your own products"
The distinctive element is what makes the video recognizable at a glance: a prop, a place, a character, a constraint. The twist is the variation that changes the outcome (the ending, the reveal, a second person). Same structure and setup on another topic: same card. A setup or an ending that changes the beats: new card.

## Rules

- Drafts only: never publish, send or schedule anything for the user.
- Never ask for a password. The user signs in to every platform.
- No promised views or results, and no invented numbers. A view count in a card is the number shown on the platform on the date it was read, with that date.
- Credit every public example with a link to the original post. Describe the shape in your own words; never copy a creator's script.
- Reactions, duets and stitches use the platform's own tools or short excerpts with commentary. Respect music and clip rights.
- Pranks, street formats and shocking formats respect the people filmed and the platform rules: consent before posting a recognizable person, no deception about a product, no harassment, no cheating where money or rankings are at stake.
- Disclose paid partnerships, gifted products and brand-run accounts with the platform's branded content tools and local law.
- Flag anything that looks confidential (customer names, revenue, internal decisions) before it goes into a script or a card.
