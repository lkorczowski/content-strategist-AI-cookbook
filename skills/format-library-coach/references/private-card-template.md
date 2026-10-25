# Private format card (template)

A private card lives in a company's private repository (blueprint layout: `kb/formats/`), never in this public repository. It holds what a public card cannot: client examples, internal numbers, the team's own variations and the results observed per format. Ids are P001, P002... The file name is the slug of the name, like public cards, so `scripts/library.py --private kb/formats` can read it.

Two kinds of private cards:
- **Overlay**: a public format run in your program. Set `public_id` to the public card (F0xx) and keep the public name. Fill only what is yours.
- **Private format**: a format you do not want to publish yet. Fill every section of `card-template.md`, plus the sections below.

```
---
id: P001
name: Same name as the public card, or the private format name
public_id: F079
funnel: TOFU
value: humour
structure: comment-reply, skit
setup: on-site, two-shot
origin: original
founder_on_camera: optional
effort: low
length: 30-60 s
status: tested
added: YYYY-MM-DD
---

# Same name as the public card

## Shape
(one line, or "see the public card")

## Beats
(only if they differ from the public card)

## Make it yours
(how this team runs it: who is on camera, where, which props)

## Examples
- [account, views (read YYYY-MM-DD)](URL): what to look at. Client accounts are allowed here.

## Dice
| Account | Videos posted | Floor | Median | Top | Window | Read on | Source |
|---|---|---|---|---|---|---|---|
| client or own account | 6 | 1.2k | 4k | 210k | 7 days | YYYY-MM-DD | analytics export, dashboard |

Floor, median and top are views (or the metric the account judges on) after the same window for every video. They describe the die; they promise nothing.

## Decisions
- YYYY-MM-DD: keep, change one variable (which one) or drop, and why (from format-dice-review).

## For your AI
(the public prompt, with the company context already filled)
```
