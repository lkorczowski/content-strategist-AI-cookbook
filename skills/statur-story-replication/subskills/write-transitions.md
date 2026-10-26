---
name: write-transitions
description: Write the transitions of a long spoken script so that every block exit opens or closes a loop and sentence links run on but/therefore rather than and-then. Use when joining blocks or threads in a replicated script.
---

# Write transitions

## What the move does

A story-led explainer can switch thread every half minute and still feel smooth. Its transitions are short, spoken, and almost always open or close something. A transition that opens a loop gives the viewer a reason to stay through the next block (ZEIG).

## How to find it in your source analysis

- `02-map.md`: units tagged BRIDGE, DETOUR, RETURN, RECAP, QUESTION or TEASE on the first or last unit of a block; the `cx` column at block boundaries.
- `03-loops.md`: which loop opens or closes at each block exit.
- `work/stats.json`: `thread_switches_per_10min` and `causal_link_ratio` give the rates to hold.

## Catalog of transition templates

| Transition | Job | Where |
|---|---|---|
| "And the thing is, that moment exists only because..." | Counterfactual tease, opens the subject loop | end of cold open |
| "This moment matters for three reasons." | Announces a list, micro loop | after a clip |
| "Yet in this field, [impressive things] are everywhere..." | BUT link into the reveal | lesson entry |
| "Which raises two questions." | Opens loops addressed to the viewer | end of reveal |
| "Before explaining that, a quick side note." | Announced detour (the viewer forgives it because it is announced) | inside a lesson |
| "And that is what makes [SUBJECT] exceptional." | Return from the detour | after a rant |
| "And that always makes a good story." | Bridge from lesson to story | end of a lesson block |
| "So we saw why [SUBJECT] is great. Why do so many people refuse it?" | Recap plus pivot question | midpoint |
| "That is why most experts say [rule]. It is exactly what happened in [date]." | THEREFORE link from tip to story proof | before the sandbox |
| "There is a way to make it work, though." | Nuance that opens the tips | after the sandbox |
| "So how did it end?" | Question that reopens the saga after a long lesson | end of tips |
| "For now, the experts' advice is [rule]. And precisely, [return to the opening venue]." | Deferral then landing on the cold-open venue | before the payoff |
| "Before I show you the rest, put yourself in [HERO]'s shoes." | POV shift before payoff | climax entry |

## Invented example

End of a lesson block on onboarding tips: "So the fix is simple: cut every step before the first result. And that is exactly what the founder did, six months in. So why did she put the old tour back a month later?" The block closes the tip loop and opens a new one that the next story block pays.

## Rules

- Every block exit opens a loop or closes one. If a block ends with nothing pending, add a question, a tease or a cliffhanger.
- Sentence-initial links: aim for at least half BUT or THEREFORE. Replace "and then" by "but" or "so" when the logic allows.
- Announce detours. An announced detour is a promise; an unannounced one is a drift.
- When you return to the saga after a long lesson, ask a question about it ("So what did they do next?", "So how did it end?").
- Respect the target creator's banned constructions. Example of such rules: no "X, not Y" framing, no litote by negation, no em dash. Rewrite "the worst is not X, not Y, it is Z" as "Forget X. Forget Y. The worst is Z."
