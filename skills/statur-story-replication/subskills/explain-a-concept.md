---
name: explain-a-concept
description: Explain one jargon term or mechanism in a spoken script in five steps (term, comic reaction, plain definition, application, three famous examples), and forge vivid analogies. Use whenever a script introduces a technical word or an abstract mechanism.
---

# Explain a concept

## What the move does

A jargon word inside a claim, a beat that gives the viewer permission to be lost, then a plain definition and three examples in one breath. The viewer learns a word and feels smart, and the creator gains authority without losing anyone (FLUENCY, SIGNAL, AUTH).

## How to find it in your source analysis

- `02-map.md`: a unit tagged TERM followed by a MEME or HUMOR unit, then DEFINE, then EXAMPLE units.
- `07-seed.yaml`: moves coded `TERM+DEFINE+EXAMPLE` in the lesson blocks.
- `work/stats.json`: `density_per_10min.terms_defined` and `analogies` give the rate to hold.

## The five-step pattern

1. TERM: say the jargon word inside a claim.
2. CONFUSION BEAT: a one-line meme or reaction from a viewer who did not get it. It gives permission to not know.
3. DEFINE: plain words, under 20 words, no second jargon term.
4. APPLY: apply it to SUBJECT, twice if the term has two sides.
5. EXAMPLES: three famous examples from different domains, said in one breath, then a one-line recap.

Then state the consequence for the viewer in a separate sentence ("This creates two problems").

Invented example, in a video about onboarding:
1. "Our first onboarding had a terrible time to value."
2. `[MEME | blank stare]`
3. "Time to value is how long a new user waits before the product helps them."
4. "For the user, it is the minutes before the first result. For the team, it is the weeks before the user pays."
5. "A light switch, a search box, a vending machine: you act, you get the result. Short time to value."

## Analogy forge

Three kinds:
- Swap analogy: "X, but with Y instead of Z". Pick X = a known risky game, Y = an absurdly bigger stake. Invented: "a coin toss, but with your launch week instead of a coin".
- Incongruity analogy: drop the most iconic heavy thing of universe A into the most iconic simple setting of universe B, then a deflating aftershock. Invented: "an enterprise setup wizard at a lemonade stand. That might slow down the lemonade a little."
- Character analogy: a famous figure with one trait exaggerated. Invented: "a famous detective who refuses to look at any clue until you fill in a form".

## Success criteria

- A 12-year-old who never heard the word can repeat the definition.
- Both universes of an analogy are known to most of the audience (check: blockbuster films, global brands, school myths).
- The analogy carries the scale or the mechanism; decoration alone does not count.
- Define few terms: one per minute is the ceiling, and a long video usually needs only a handful.
