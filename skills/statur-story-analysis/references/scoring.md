# Scoring rubric v0, calibrated on one long explainer; recalibrate on your own sample

Scores are out of 20, like ability scores in tabletop role-playing games. Modifier = floor((score - 10) / 2). 10 = a competent YouTube explainer in its niche. 18 = the best video you have analyzed in that dimension. Recalibrate after 3 to 5 videos: add each video to the calibration table at the bottom and move the anchors if most videos crowd at one end.

Each score = the anchor that fits the metrics, then plus or minus 2 for what the numbers miss. Write the adjustment in the evidence line.

| Ability | Metrics (from work/stats.json) | 6 | 10 | 14 | 18 |
|---|---|---|---|---|---|
| Curiosity | loops opened per 10 min; min loop load after minute 1; master loops; doors left open | under 1 per 10 min, long stretches with nothing pending | about 2, load drops to 0 between sections | about 4, load never 0, one master loop | 5 or more, load never under 2, 3+ master loops, a cold-open loop closed in the last 15% |
| Weave | thread switches per 10 min; story share; longest stretch without story | one thread | two threads in long alternating blocks, under 5 switches per 10 min | 10+ switches, each lesson section has a story proof or example | 15+ switches, story share 35-55%, longest stretch without story under 8 min |
| Clarity | TERM followed by DEFINE in the next unit; signposts per 10 min; examples per concept; recaps at pivots | jargon undefined | terms defined later or by context | every term defined at once, numbered sections | every term defined at once with 2-3 known examples, a recap at every pivot, one idea per sentence |
| Authority | EVIDENCE and HISTORY per 10 min; sources named and dated; research shown; errors | claims without sources | a few numbers, undated | dated facts and named sources every 2-3 min | dated facts every 2 min, research effort shown, admits what is unknown, no errors found |
| Voice | STANCE, SELF and RANT per 10 min; register; opinions a peer could dispute | neutral narrator | opinions at the start and the end | first-person stance every few minutes, one confession | strong stance, pet peeves, confessions, a register you recognize with the eyes closed |
| Humor | HUMOR tags per 10 min; variety (memes, incongruity, deflation, irony) | under 2 | about 4 | about 8 | about 12 or more, at least 4 different techniques |
| Emotion | mean tension; share of time at 4+; number of 5s; final peak | flat, mean under 1.5 | mean about 2, one peak | mean about 2.5, 20% at 4+, peaks in the last third | mean 3+, 30%+ at 4+, several peaks, the highest at the end |
| Payoff | closed / opened loops; PAYOFF and CALLBACK per 10 min; bookend; longest plant-payoff distance | loops left dangling by accident | most loops closed, no callbacks | callbacks every few minutes, one long setup paid | 85%+ closed, a bookend, a setup paid 20+ min later, doors left open on purpose |

## Custom axes

A creator's own goals become extra axes, each a weighted mix of the core scores or of tag densities, written as a formula so the next analyst can recompute it. Take the goals from the company context file when there is one, or ask the creator for three or four. Example (four axes a creator might ask for): Authority = AUT; Vitality = 0.4 HUM + 0.3 EMO + 0.3 WEA; Clarity = CLA; Fun = 0.7 HUM + 0.3 VOI. Keep the eight core axes on every Fiche so that Fiches stay comparable.

## Calibration table

Add one row per video you analyze, with a one-line note on what makes it a reference.

| Video | CUR | WEA | CLA | AUT | VOI | HUM | EMO | PAY | Note |
|---|---|---|---|---|---|---|---|---|---|
