# Quality gate

`qa_pro.py MASTER --plan plan.json --layers frames --words cut/words_out.json --qa-clip ../statur-clipping/scripts/qa_clip.py`

## Hard checks (REFUSE when one fails)

- H.264 yuv420p, BT.709 tags, the planned size.
- Loudness -15 to -13 LUFS integrated, true peak at most -1.0 dBTP.
- No black stretch over 0.5 s before the end card.
- At least 90% of the planned words heard back (re-transcription).
- An audio track.

## Notes (PASS_WITH_NOTES)

- Duration off the plan by more than 0.25 s.
- Frozen stretches (a still card can be intended: check it).
- Graphics in a platform UI zone on several sampled frames. The gate checks the hard UI zones (top 240 px, right column x 960 to 1080 for y 840 to 1700, bottom below y 1700); the target area for text is tighter (references/levels.md, safe areas).

## What the agent looks at, every time

The contact sheet of 16 frames, plus stills around each card, each cut to the room and the end card:
- the hook frame: text readable in one glance, face visible;
- captions never on the mouth or the eyes, never cut by the frame;
- every card fully visible (not hidden by its own panel), no text cut, no overlap with captions;
- keyed frames: hair edges clean, no halo, the speaker not floating;
- numbers on screen match their source line;
- the end card URL is live.

## Decisions for a human (mark them on the review page)

- Realistic synthetic people or scenes.
- Captures of third-party pages or posts.
- Music whose license the manifest cannot prove.

## Refusal

An edit that fails a hard check, or that a reviewer would not post (a claim without proof, a name the company forbids, a wrong number), goes back with the reason. Saying "this clip should not ship" is part of the job.
