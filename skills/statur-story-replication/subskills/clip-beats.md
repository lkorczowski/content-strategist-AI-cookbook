---
name: clip-beats
description: Write the clip beats of a replicated script, the share of runtime the source gives to third-party footage, as precise cues when footage exists or as retellings and quote cards when it does not. Use when a seed block has a clip share above zero.
---

# Clip beats

## What the move does

In a clip-heavy source, the narrator sets up a moment and lets third-party footage land it. Clips often carry the proof and the payoffs: the viewer sees the event instead of hearing about it (VICAR). A replication must keep their function even when the footage is not available or not licensed.

## How to find it in your source analysis

- `07-seed.yaml`: blocks with `clip_share` above zero, and moves whose codes include CLIP.
- `02-map.md`: units with track CLIP or CARD, and the loops (`L##c`) that close on them.
- `work/stats.json`: `track_share.CLIP` for the whole video, `blocks[].clip_share` per block.

## Three ways to fill a clip slot

1. FOOTAGE: a real public clip (interview, keynote, demo, livestream, podcast). Write the cue as:
   `[CLIP | source title, channel, date | from mm:ss to mm:ss | what we see | on-screen subtitle under 15 words]`
   Keep each excerpt short and commented. Check the platform's rights; a long unedited excerpt is not commentary.
2. QUOTE CARD: a text card with a short public quote or post (under 15 words), attributed and dated, over a neutral background or a screenshot of the public post.
   `[CARD | "quote under 15 words" | author, outlet or platform, date]`
3. RETELLING: the narrator tells the scene precisely, in the present tense, with one detail of setting, who says what (paraphrased), and the reaction. Use it when no footage or quote exists. Mark it `[RETELLING]` so the editor knows to use B-roll.

## Invented example

Setup: "Watch the counter in the corner of the screen." Then `[RETELLING]`: "Launch night. The founder refreshes the dashboard. The counter reads zero. Her cofounder says, more or less, that zero is also a number." Reaction within two sentences: "Nobody laughs. Not yet." In a real script, every detail of the scene carries a fact id.

## Rules

- A clip beat always follows a setup that tells the viewer what to watch for, and is followed by a reaction or an explanation within 2 sentences.
- Put narration between two clips, except at the climax.
- Every fact in a clip beat has a research id `[F##]` like the narration.
- Budget: when the seed block has clip share c and duration d, the clip slot is about c × d seconds; a retelling of that slot at 150 words per minute adds words to the script. Report the estimated runtime separately from the narration word count.
