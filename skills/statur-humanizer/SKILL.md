---
name: statur-humanizer
description: Cut the text a reader skips, on a web page, playbook, landing page, essay or post, before a person has to point at it. A density pass in three steps (measure with a script, classify each weak block into one of ten patterns, cut or merge or move it), then an AI-tell pass, then a read-aloud check. Use before publishing any page or long document written with an AI, when someone says a text is verbose, too long, heavy, padded or sounds like AI, and as a gate in a site build.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "0.1.0"
  playbook: https://statur.co/playbooks/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Humanizer: every block earns its place

Text written with an AI fails in two ways. It uses the phrases people now recognize as machine made, and it says too much: notes nobody asked for, the same proof three times, a sentence that announces the next one. Public humanizer skills cover the first failure well (see Credits). This one starts with the second, because a reader forgives a stiff phrase and leaves a page that wastes their time.

The reader scans. In the Nielsen Norman Group studies of 1997, 79 percent of test users scanned a new page and 16 percent read word by word; a concise version of the same page scored 58 percent higher on measured usability, and a concise, scannable and objective version 124 percent higher (51 users, five versions of one site). The studies are old and small. Treat them as direction, and measure your own pages.

## Intake (ask once, then use the defaults)

1. What is the text and who reads it: a cold visitor on a landing page, a buyer comparing, a practitioner using a reference playbook?
2. What must survive every cut: the proof with its source, the legal lines, a commitment written by the author. Default: every number keeps its source, quotes and legal text are never touched.
3. How far to go: `report` (list the weak blocks, change nothing, the default for a whole site), `propose` (list with a rewrite for each), `apply` (edit the files, one commit per page).
4. Budgets per page type. Defaults below; the author's own numbers win.

## Default path

```
python3 scripts/density_lint.py dist/                         # every built page, one line each
python3 scripts/density_lint.py dist/ --page /pricing/ -v     # every hit of one page
python3 scripts/density_lint.py draft.md -v                   # a Markdown or text draft
python3 scripts/density_lint.py dist/ --config lint.json --strict   # build gate: exit 1 over budget
python3 scripts/density_lint.py --help
```

The script needs Python 3.8 and nothing else. It reads the visible text only (navigation, footer, forms, code blocks and scripts are left out) and counts, per page: words against the budget, paragraphs over 60 words, sentences over 28 words, blocks repeated on the page, numbers stated in more than two blocks, defensive notes, signposting, filler words, labeled micro-lines, and blocks copied on three pages or more. It finds candidates. It cannot tell a paragraph that teaches from one that pads, so step 2 is read by a person or a model.

### Step 1. Measure

Run the lint on the built pages, not on the source: templates and shared components hide most of the repetition. Sort by words over budget. Start with the pages a cold visitor sees first.

Default budgets (convention, set from the first audit; change them in `lint.json`):

| Page | Visible words |
|---|---|
| Home | 900 |
| Ad landing page | 600 |
| Offer or program page | 1,200 |
| Proof or cases page | 700 |
| Blog post | 1,500 |
| Playbook or handbook | 3,500 |

### Step 2. Classify each weak block

Read the page top to bottom as the reader named in the intake. For every block ask: if this disappeared, would that reader miss it? When the answer is no, name the pattern. The ten patterns, the test for each and the fix are in `references/patterns.md`. Short form:

| Code | Pattern | Fix |
|---|---|---|
| V1 | Defensive note: how we count, what is left out, a caveat nobody asked for | Cut, or keep three words next to the number, or move behind a link |
| V2 | Repetition: the same proof, number or idea again on the page | Keep the strongest instance |
| V3 | Announce, recap, comment: a sentence about the text | Cut |
| V4 | Stacked layers: a card with a description, a label line, a second label line, a source | One sentence per card, the rest behind a click |
| V5 | Over-long block: one idea in more than 60 words, or a 28-word sentence | Split, or cut the qualifiers |
| V6 | Over-explanation: what the reader sees or knows already | Cut |
| V7 | Process talk: how the page was made, version notes, machine labels | Move to a comment, a changelog or the end |
| V8 | Too many items: twelve entries where five are read | Keep the best, link the rest |
| V9 | Boilerplate: the same block copied on many pages | One reference page, a one-line link elsewhere |
| V10 | Second definition: a term explained again each time it returns | Define once, link back |

### Step 3. Cut, merge, move

Apply in this order, because each step is cheaper than the next:

1. Cut the block. Most V1, V3, V6 findings end here.
2. Merge two sentences when the second only specifies the first.
3. Move depth behind a click (a details element, a linked reference page, a footnote) when a minority of readers needs it. A source stays visible; its commentary does not.
4. Rewrite shorter. One idea per sentence. Keep the number, the name, the mechanism or the action; drop the adjective.

Never change a number, a name, a quote or a legal sentence. Never invent a figure to replace a vague phrase: write a placeholder and ask.

### Step 4. AI-tell pass

After the cuts, read what is left for the phrases readers recognize as generated: contrast reveals ("Not X. Y."), paired fragments, reflexive lists of three, colon reveals, questions the text answers itself, maxim endings, filler transitions, inflated significance, text that reads like a label or an instruction. Rewrite the whole paragraph when it holds two of them. The full lists live in the sources under Credits; this skill does not copy them.

### Step 5. Read aloud, then lint again

Read the page aloud once, or have the model read it as the intake reader with five seconds per screen. Anything the voice rushes through is a candidate. Run the lint again and record the before and after counts in the change description.

## Keep it from coming back

- Build gate: run the lint with `--strict` and a `lint.json` in the site build. A page over its budget fails the build; the author raises the budget on purpose or cuts.
- Writing rule for the drafting model, to paste in the project instructions: "Before you add a note, a caveat or a how-we-count line, ask who asked for it. A number carries its source in a few words and nothing else. State each proof once per page. No sentence about the text itself."
- Templates: when a component prints a block on every page (a commitment, a rules box, a FAQ), count it once in the design review. The lint lists the blocks copied on three pages or more.
- Review habit: the person who reviews marks what to shorten and strikes what to delete. Log each struck block with its pattern code; a pattern struck twice becomes a lint phrase in `lint.json`.

## Output

For `report` and `propose`: one table per page (block, pattern code, why, fix, rewrite when asked, severity 1 to 3), a site summary (words before, estimated words after, the five patterns that cost the most) and the list of decisions that belong to the author (a proof to drop, a section to remove). For `apply`: one commit per page with the before and after lint line.

## Pitfalls

See `references/pitfalls.md`. The three that matter most: cutting a source along with its commentary; shortening a reference playbook as if it were a landing page; trusting the lint counts without reading the page.

## Update this skill

- Add a pattern when a reviewer points at a block none of the ten covers. Give it a code, a test and a fix in `references/patterns.md`.
- Add a phrase to the `defensive`, `signpost` or `filler` lists (in `lint.json` for one site, in the script when it holds on two).
- Revisit the budgets when you have reading data (scroll depth, time on page) for your own pages: the defaults are conventions.
- Revisit the AI-tell pass when the sources under Credits change; they move faster than this file.

## Credits

- blader/humanizer (MIT), github.com/blader/humanizer: 26 patterns of AI writing in six groups.
- Corey Haines, marketingskills, copywriting reference "AI tells", github.com/coreyhaines31/marketingskills.
- Wikipedia, "Signs of AI writing" (CC BY-SA 4.0), en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing.
- Morkes and Nielsen, "Concise, Scannable, and Objective: How to Write for the Web", 1997, nngroup.com; Nielsen, "How Users Read on the Web", 1997.
- US plain language guidelines, "Clear and short", digital.gov/guides/plain-language.

## Rules

- Drafts only: the skill proposes or edits files in a branch; a person publishes.
- No passwords, no accounts: you sign in yourself.
- No promised results: shorter text is easier to read, and nothing here promises conversions or views.
- No invented numbers. Every figure, name, quote and source in the text survives unchanged, or the cut is flagged for the author.
- Legal pages and verbatim commitments are never edited.
