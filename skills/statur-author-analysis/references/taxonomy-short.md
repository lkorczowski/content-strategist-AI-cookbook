# Taxonomy addendum · short talking-head videos

Everything in `taxonomy.md` still applies (tracks, threads, function codes, figures, psych mechanisms, objectives, tension, loops, connectives). This file adds what a short video needs and a long one hides: the opening second, the turn, the last line, and the comparison across many videos of one author.

All examples below are invented to show the shape of each code.

## 1. Unit

One unit = one spoken sentence or clause that does one job, usually 2 to 6 seconds. Automatic caption cues are cut by time, not by meaning: merge or split cues so each unit is a full thought. Keep the cue timestamp of the first word.

## 2. Short beats (column `beat` in 01-blocks.md)

| Beat | Job | Typical place |
|---|---|---|
| HOOK | the first line: a claim, a question or an image that makes the viewer stay for line 2 | 0 to 5 s |
| FRAME | says what this is about and why the viewer should care (often "so", "here's the thing") | right after the hook |
| SETUP | the facts, the story or the premise needed for the turn | first third |
| TURN | the reframe: the moment the video says the obvious reading is wrong or incomplete | around 35 to 65% |
| BUILD | examples, escalation or a second turn that makes the new reading feel inevitable | after the turn |
| PAYOFF | the insight stated plainly | last quarter |
| BUTTON | the last line: a joke, a twist, an image or a callback that closes the video | last 5 s |
| STORY | an anecdote or a historical episode told as a scene | anywhere |
| ASIDE | an announced digression or a joke outside the line of argument | anywhere |
| CTA | an ask (follow, comment, buy, link) | usually last or first |

A video is a sequence of beats, written as a string: `HOOK FRAME STORY TURN BUILD PAYOFF BUTTON`. Templates are recurring sequences across the author's videos.

## 3. Hook types (column `hook` in the video header)

| Code | Hook | Invented example |
|---|---|---|
| H-CLAIM | a bold or strange statement of fact | "This is the most expensive spreadsheet in the company." |
| H-CONTRA | contradicts what the viewer believes ("everyone is wrong about") | "Inbox zero is a trap." |
| H-QUESTION | asks the viewer something | "Why does every onboarding email sound the same?" |
| H-SCENE | starts inside a story or an image | "It's 2 a.m. and the dashboard is green." |
| H-NEWS | reacts to a current event or a post | "This post is everywhere today. Let's read it." |
| H-REPLY | answers a comment or a viewer question | "Someone asked why I never post on Mondays." |
| H-STAKES | says what the viewer stands to lose or gain | "This one setting decides who sees your next video." |
| H-LIST | announces a number of items | "Three questions to ask before you hire an agency." |
| H-CONFESS | the creator admits something about themselves | "I deleted my best-performing video last week." |

## 4. Ending types (column `end`)

| Code | Ending | Invented example |
|---|---|---|
| E-JOKE | a punchline | "So yes, the spreadsheet has its own budget line." |
| E-MORAL | a short rule or aphorism | "Fix the habit, and the tool follows." |
| E-CALLBACK | returns to the image or line of the hook | "And the dashboard is still green." |
| E-SINCERE | drops the irony and says what the creator really believes | "I think this is the best job in the world." |
| E-QUESTION | asks the viewer | "Which one would you pick?" |
| E-OPEN | cliffhanger or "part 2" | "What they did next is part 2." |
| E-CTA | ends on an ask | "Comment 'guide' and I'll send it." |
| E-FACT | ends on a dated fact, no button line | "The rule changed in March 2024." |

## 5. Per-video metrics (computed by scripts/analyze.py plus scripts/aggregate_author.py)

- words, duration, words per minute
- time to first loop, time to the turn (share of runtime), number of turns
- loops opened per minute, min load after 5 s, open at the end
- humor units per minute, questions per minute, second-person share (sentences with "you")
- evidence per minute (numbers, names, dates), analogies per minute
- thread shares (S story, L lesson, A audience, H host, X meta)
- but/therefore share of links
- tension curve: start, turn, end; peak position

## 6. Author-level layer (10-author-grammar.md)

- template frequencies (beat strings clustered), with the median share of each beat
- hook and ending distributions, overall and for the 10 most-viewed vs the 10 most recent videos
- signature moves: recurring phrases and figures, with counts across videos
- medians and ranges of the per-video metrics
- what separates the most-viewed videos from the rest, stated only when the difference holds in most pairs (20 videos is a small sample: say "tendency", never "law")

## 7. Errors to avoid

- Tagging the author's irony as sincerity. Many talking-head creators state a view in order to knock it down: tag the turn where the knock-down happens.
- Counting caption fragments as units: rhythm metrics then measure the caption tool's cue length.
- Comparing views across years without saying so: the audience and the algorithm change.

## Changelog

- v1: created while analyzing a talking-head creator across about 20 short videos of 1 to 6 minutes. Added E-FACT here and the figure APOPHASIS in `taxonomy.md` after finding units with no fitting code.
