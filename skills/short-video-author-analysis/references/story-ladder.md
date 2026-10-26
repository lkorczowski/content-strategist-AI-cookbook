# Story ladder and sentence rhythm

Two quick reads that sit on top of the nine-tier map. The map measures everything; these two give a creator a verdict in one line and one thing to fix.

Credit: the five-level story ladder is a framework shared publicly by Kallaway (https://www.tiktok.com/@kallaway.marketing/video/7699869751488564511, 2026-10-23). The short-sentence rhythm trick was shown by ginyboi, who credits the idea to Kallaway (https://www.tiktok.com/@ginyboi/video/7699704871389383967, 2026-10-23). The mapping to the tiers and the checks below are ours.

## 1. The story ladder

Five levels. Each level keeps everything below it and adds one layer. Read the level from the map, then name the next rung.

| Level | What it adds | Where it shows in the map | Check |
|---|---|---|---|
| 1 · Reporter | The core facts, in order | EVIDENCE, ACTION and EXPLAIN units; connectives mostly AND | The story is complete and true |
| 2 · Magician | Hooks inside the story: lean the viewer one way, snap them back | TWIST, REVEAL and SIGNPOST units; an OBJECTION closed by a TURN; the hook code | At least one misdirection in the body, beyond the opening hook |
| 3 · Fortune teller | Stakes: the use, the problem or the desire that makes the viewer feel it is about them | STAKES and ADDRESS in fn2; PERSONAL, LOSS and SOCIAL in psych; the share of sentences with "you" | The viewer can say what they gain or lose |
| 4 · Architect | Arcs and loops: tension that rises and releases, sub-questions that open and close | the tension curve (T) and the loop ledger: mean load, minimum load after the first minute, micro loops per minute | Tension has waves; at least one question is open at every moment after the hook |
| 5 · Maestro | A signature: the way only this creator tells it | the VOI score, signature moves on the card, recurring phrases, the visual equipment | Someone could recognize the creator with the logo hidden |

How to use it:
- Analysis: write the level in the Fiche notes with one line of evidence per rung. A video sits at the highest level whose check passes and whose lower levels all pass.
- Replication: before writing, plan one move per rung (the facts, one misdirection, the stakes in the viewer's words, the loop plan, one signature move). After the self-map, check each rung again.
- Common gap: a script with hooks and loops (levels 2 and 4) but no stakes (level 3). The viewer is curious and does not care.

## 2. Sentence rhythm

Long sentences in a row sound flat when spoken. A short sentence after one or two long ones resets the ear. Short means five words or fewer.

Run `python3 -I scripts/rhythm.py <units.tsv or script>`. It prints the share of short sentences, the share of sentences of 20 words or more, the longest run of sentences of 12 words or more, and every run of three or more long sentences.

Rules of thumb:
- Break any run of three long sentences with a short one, unless the run is a deliberate accumulation (a list that builds).
- Put a short sentence right after a turn or a reveal. The flat answer after a long question is the strongest version.
- Compare the shares with the source creator's own videos, the same way as the other parity rows. Some creators speak in long chains on purpose, and their rhythm comes from pauses and stress. Match the source, then the target voice.
- Captions without punctuation: the script counts each caption cue as a sentence, which overstates the short share. Say so in the notes.
