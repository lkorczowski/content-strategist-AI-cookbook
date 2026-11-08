# The Format Library

A growing library of short-form video formats for founders: one card per format, tagged on four dimensions that combine freely. **Funnel** (TOFU, MOFU, BOFU), **value** (why people watch and share: educational, humour, surprising, shocking, social currency, emotional, relatable), **structure** (what happens, in order) and **setup** (how it is shot and edited). Every card gives the shape, the beats by second, how a SaaS or AI founder makes it their own, variations, what to watch out for, public examples with the date their numbers were read, and a prompt for your AI.

- Browse the library: [skills/statur-format-library/library/](../skills/statur-format-library/library/README.md) (quick picks, funnel x value matrix, every format by tag)
- Tags, definitions and naming rule: [taxonomy](../skills/statur-format-library/references/taxonomy.md)
- Page (human version): https://statur.co/format-library/ (publication pending)
- Library version 0.1, 2026-11-03 (skill statur-format-library 3.0.0)

## How to use it

1. Filter by goal or constraint (BOFU, no face on camera, low effort), or ask the skill for a starter deck of six to eight formats.
2. Script each video with the beats of its card and name it with the format name.
3. Shoot two or three videos per format in one sitting.
4. Judge formats elsewhere: [statur-format-review](../skills/statur-format-review/) (The Content Testing Loop) decides keep, change one variable or drop on mature data (7 days and 1,000 views, several videos per format). This library never decides; it records the decision in your private card.
5. Invent your own original formats from a proven structure and something only your company has.
6. Spot a new format in your feed, or sit on hundreds of saved videos? Document them with the same skill and add them by pull request.

## Skills

| Skill | Use it for |
|---|---|
| [statur-format-library](../skills/statur-format-library/) | Find formats by tag, plan a starter deck, script with the beats, invent an original format, document a format from a video, sort a collection of saved videos. |
| [statur-format-review](../skills/statur-format-review/) | Read the results per format and decide keep, change or drop (not part of this playbook: The Content Testing Loop). |
| [statur-content-learning](../skills/statur-content-learning/) | Monthly lessons across the whole history (The Content Testing Loop). |

## The tool

`python3 skills/statur-format-library/scripts/library.py` (standard library only): `find`, `suggest`, `similar`, `new`, `gaps`, `lint`, `build`, `check`. Add `--private <folder>` to include a private library of cards (ids P001...) with client examples and observed results, kept in your own repository.

## Contribute

A new format is a pull request with one card in `skills/statur-format-library/library/formats/`, created with `library.py new "<name>"` from `references/card-template.md`, tags from `references/taxonomy.json` only, at least one public example link with the date its numbers were read (or the line "No public example in this card yet."). Run `python3 skills/statur-format-library/scripts/library.py build` before opening the pull request; CI runs `library.py check`.
