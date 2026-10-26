---
name: figures-cookbook
description: Recipes for rhetorical and comic devices of story-led explainers (deflation beat, priamel, voiced objection, second-person loss, perspective shift, aposiopesis completed by a clip, reveal by deflation, counterfactual tease, meme placement, register drop, meiosis) with templates, invented examples and target-voice constraints. Use while drafting any block of a replicated script.
---

# Figures cookbook

Each recipe: what it does, the template, an invented example, the constraint for the target voice.

## How to find these in your source analysis

- `work/stats.json`: `figures` counts every Tier 5 figure; `density_per_10min` gives humor, memes and questions per 10 minutes. Hold the same rates.
- `02-map.md`: the `fig` column shows where each figure sits; read the gloss of two or three units per figure before you write your own.
- `07-seed.yaml`: moves list the figure codes block by block.

## Deflation beat
Does: comic reversal of a virtue. Template: "[Subject] kept [virtue]. [Pause.] For about [short time]." Invented: "The team kept its no-Friday-launch rule... for about a month." Voice: spoken with a pause marker `...`; avoid choppy fragment pairs in written copy.

## Priamel
Does: builds to an unexpected small detail that becomes the worst. Template for a voice that bans "not X" framing: "The worst thing about [place]? Forget [big item 1]. Forget [big item 2]. The worst is [small item]." Then one sentence of sensory escalation. Invented: "The worst thing about our first onboarding? Forget the long form. Forget the slow server. The worst was a grey button on a grey background."

## Voiced objection
Does: says what the viewer thinks, then refutes it in a few words. Template: "You might think: [reasonable assumption]. [Short reversal]." The reversal must be shorter than the objection. Invented: "You might think a longer tour teaches users more. Quite the opposite."

## Second-person loss
Does: makes the viewer feel the stakes through loss aversion. Template: 3 sentences of building in second person (time, effort, a sentimental object), 1 short sentence of the draw, 1 accumulation of every lost item naming the sentimental object again, 1 image of the result. Invented: "Imagine two years on your product. From a weekend prototype to a real team. The first customer's thank-you note pinned above your desk. Then one update ships broken. You lose the reviews, the referrals, the renewals, and the thank-you note now reads like a joke. You are back at day one."

## Perspective shift before payoff
Does: transfers the stakes to the viewer right before the climax. Template: "Before I show you the rest, put yourself in [hero]'s shoes." Then ONE long sentence stacking: time since, crowd, humiliation just before, what they get back, why it is personal (the origin). Then the payoff. Invented: "Months after the failed launch, on a stage in front of the investors who passed, after a morning of demos that crashed, the founder opens the very first prototype she ever built."

## Aposiopesis completed by a clip
Does: lets the source finish the narrator's sentence, a joke on timing. Template: cut your sentence on a relative pronoun, cut to the quote or clip that completes it. Without footage, cut to an on-screen quote card. Invented: "...and the person in charge of the launch checklist was the cofounder who..." then a card with the cofounder's public post saying they read only the important parts.

## Reveal by deflation
Does: names the subject by contrast with grandiose rivals. Template: three big rivals, then "[plain small noun] that [humble description]". Invented: "AI copilots, six-figure redesigns, growth hacks... none of them came close to this plain little checklist."

## Counterfactual tease
Does: opens the subject loop without naming it. Template for a voice that bans double negation: "[Famous moment] exists only because, [time] earlier, [master] [did something with an unnamed thing]." Invented: "That relaunch exists only because, two years earlier, the founder kept a strange file nobody else wanted to open."

## Meme placement
Read the source's meme rate (`density_per_10min.memes`) and match it. Place a meme right after a punchline or a technical word, never in the middle of a story beat. In a script, write `[MEME | description | emotion]` with the emotion it carries (confusion, horror, triumph). Prefer original reactions or licensed clips; a meme never carries information.

## Register drop
Count the REGISTER figures in the source and keep the rate. Use the target creator's own register: a founder brand usually stays professional-casual.

## Meiosis (comic understatement)
Invented: "a small detour through three months of rewrites", "that might change the roadmap a little". Allowed even when the creator bans litotes: it is an understatement by size, without negation. Keep it rare: match the source's MEIOSIS count per 10 minutes.
