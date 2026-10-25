# The Format Library

A growing library of short-form video formats for founders: one card per format, tagged on four dimensions that combine freely. **Funnel** (TOFU, MOFU, BOFU), **value** (why people watch and share: educational, humour, surprising, shocking, social currency, emotional, relatable), **structure** (what happens, in order) and **setup** (how it is shot and edited). Every card gives the shape, the beats by second, how a SaaS or AI founder makes it their own, variations, what to watch out for, public examples with the date their numbers were read, and a prompt for your AI.

- Browse the library: [skills/format-library-coach/library/](../skills/format-library-coach/library/README.md) (quick picks, funnel x value matrix, every format by tag)
- Tags, definitions and naming rule: [taxonomy](../skills/format-library-coach/references/taxonomy.md)
- Page (human version): https://statur.co/format-library/ (publication pending)
- Library version 0.1, 2026-10-25 (skill format-library-coach 2.0)

## How to use it

1. Filter by goal or constraint (BOFU, no face on camera, low effort), or ask the skill for a starter deck of six to eight formats.
2. Script each video with the beats of its card and name it with the format name.
3. Shoot two or three videos per format in one sitting.
4. Judge formats on mature data with [format-dice-review](../skills/format-dice-review/) (The Content Testing Loop): 7 days and 1,000 views, several videos per format, then keep, change one variable or drop.
5. Invent your own original formats from a proven structure and something only your company has.
6. Spot a new format in your feed, or sit on hundreds of saved videos? Document them with the same skill and add them by pull request.

## Skills

| Skill | Use it for |
|---|---|
| [format-library-coach](../skills/format-library-coach/) | Find formats by tag, plan a starter deck, script with the beats, invent an original format, document a format from a video, sort a collection of saved videos. |
| [format-dice-review](../skills/format-dice-review/) | Read the results per format and decide keep, change or drop. |

## The tool

`python3 skills/format-library-coach/scripts/library.py` (standard library only): `find`, `suggest`, `similar`, `new`, `gaps`, `lint`, `build`, `check`. Add `--private <folder>` to include a private library of cards (ids P001...) with client examples and observed results, kept in your own repository.

## Contribute

A new format is a pull request with one card in `skills/format-library-coach/library/formats/`, created with `library.py new "<name>"` from `references/card-template.md`, tags from `references/taxonomy.json` only, at least one public example link with the date its numbers were read (or the line "No public example in this card yet."). Run `python3 skills/format-library-coach/scripts/library.py build` before opening the pull request; CI runs `library.py check`.
