# Storytelling annotation taxonomy (v1, 2026-10-23)

Shared vocabulary for tagging a spoken script unit by unit. Every code below was needed at least once on a real long video. Add a code only when a real unit cannot be tagged with the existing ones, and log the addition at the bottom.

The method borrows from linguistic annotation: several independent tiers on the same unit, so that each tier can be counted and plotted on its own. One unit = one spoken sentence (narration), one insert (meme), or one clip beat (a continuous excerpt of third-party footage with one dramatic purpose).

All examples below are invented. They come from one fictional video: a 20-minute explainer in which a founder tells why their first onboarding flow failed (story thread) and explains how onboarding works (lesson thread).

## Tier 0 : unit

| Field | Meaning |
|---|---|
| id | U### for narration and memes (from the ASR segmentation), C## for clip beats, S### for units of a replicated script |
| t | start time mm:ss |
| block | macro block B## (see Tier 2) |

## Tier 1 : TRACK (who speaks, what the viewer sees)

| Code | Definition | Detection cue |
|---|---|---|
| NAR | The creator's own voice, scripted | Main language, creator's register |
| CLIP | Third-party footage that carries dialogue or action the story needs | Other language, other voices, burned-in subtitles, ASR gap |
| MEME | Pop culture insert used as punctuation (film line, TV show, sports crowd, labelled reaction image) | Breaks the creator's register, famous line, 1-5 s |
| CARD | On-screen text that carries information (rule card, title card, definition, "six months later") | Visual only |
| BREATH | Music, black, silence used as a beat | ASR gap with nothing on screen to read |
| META | Channel housekeeping (links to other videos, supporters) | "there is already a video about this on the channel", end card |

Rule of thumb for any video built on foreign-language clips: a line in the other language is CLIP, a gap over 5 s is CLIP or BREATH (check the frame), a line in the main language that breaks the register is MEME, the rest is NAR.

## Tier 2 : BLOCK and BEAT (macro structure)

Blocks are contiguous stretches with one dramatic job. Each block gets one BEAT code.

| Code | Job |
|---|---|
| COLD-OPEN | Start inside the most charged moment or ritual, before any context |
| FLASHBACK | Jump back to the origin of the charged moment |
| REVEAL | Name or show the subject after a delay |
| THESIS | State the creator's stance and the promise of the video |
| LESSON | One teaching unit (a reason, a tip, a rule) |
| STORY | One episode of the story thread |
| DIGRESSION | Announced detour, with a return |
| PIVOT | Change of direction of the argument ("so why do so many teams skip it?") |
| CALLBACK | A block whose main value is to pay off something planted much earlier |
| CRISIS | Lowest point of the story thread |
| CLIMAX | Highest point, the payoff the video has been building toward |
| CODA | Closing, bookend, end card |

## Tier 3 : THREAD (which braid the unit belongs to)

| Code | Thread |
|---|---|
| S | Story thread: the chronological real-world story (example: the startup's first six months, from launch to relaunch) |
| L | Lesson thread: the subject explained (example: what onboarding is, why it fails, how to fix it) |
| H | Host thread: the creator as a character (opinions, confessions, research effort, jokes about themselves) |
| A | Audience thread: the viewer's own life and work ("your users", "imagine you launch tomorrow") |
| X | Channel thread: references to other videos of the channel, supporters |

A unit can carry two threads (primary first). A thread switch is counted each time the primary thread changes between two consecutive NAR or CLIP units.

## Tier 4 : FUNCTION (what the unit does in the narrative)

One primary function, up to three secondary ones. Families:

### A. Curiosity and attention
| Code | Definition | Example (invented) |
|---|---|---|
| HOOK | A claim or image built to stop the scroll | Every new user clicked the same button, then left |
| TEASE | Mention without naming, or name without explaining | "a strange screen we will talk about today" |
| QUESTION | Explicit question asked to the viewer or the story | "Did they ship it anyway?" |
| OPEN | Opens a loop (question, promise, mystery, setup) that is not closed in the same unit | The day the founder calls the worst of the company, left unnamed |
| CLOSE | Closes a loop opened earlier | The relaunch turns out to be the day from the opening |
| CLIFF | Cuts away from a thread at a peak, before the outcome | The first user opens the app, cut to the dashboard |
| REVEAL | Delivers withheld information | "a plain five-step welcome tour" |
| TWIST | Reverses an expectation | The fix worked, for about a week |

### B. Navigation
| Code | Definition | Example (invented) |
|---|---|---|
| PROMISE | Announces what the video will deliver | Tell the story, explain why it failed, show how to fix yours |
| SIGNPOST | Numbered or explicit marker of position | "Third reason", "fifth and last tip" |
| RECAP | Summarizes what was covered | "OK, we saw why the tour looked great on paper" |
| BRIDGE | Transition between threads or blocks | "Which brings us back to launch night" |
| DETOUR | Announces a digression | "before the fix, a quick side note" |
| RETURN | Comes back from a digression | "And that is what makes onboarding so fragile" |
| TIMEJUMP | Ellipsis or jump in time | "Six months later" |

### C. Story mechanics
| Code | Definition | Example (invented) |
|---|---|---|
| SCENE | Sets place and time | A shared office, the night before launch |
| CHAR | Introduces or characterizes a person | The cofounder who never reads a checklist |
| STAKES | States what can be won or lost | A bad first week can sink the next round |
| ESCAL | Raises the stakes | The biggest prospect signs up that same night |
| PLANT | Setup meant to be paid later | The founder promises to never launch on a Friday |
| PAYOFF | Pays a plant | The relaunch happens on a Friday, on purpose |
| CALLBACK | Explicit reference to an earlier element of the video | The opening screenshot shown again |
| IRONY | Dramatic irony: viewer knows more than the character | "Nothing can go wrong with a tour this simple" |
| ACTION | Narrates what happens | The founder walks through the signup flow, click by click |
| CLIMAX | Peak event | The first user finishes the flow live, on stream |
| POV | Puts the viewer in a character's shoes | "Put yourself in the founder's place for two seconds" |
| DESCRIBE | Sensory or vivid description | The silence in the room while the counter stays at zero |

### D. Pedagogy
| Code | Definition | Example (invented) |
|---|---|---|
| TERM | Introduces a jargon term | activation, time to value |
| DEFINE | Defines a term in plain words, right after TERM | time to value = how long a new user waits before the product helps them |
| EXPLAIN | Explains a mechanism or rule | Each step you add, some users leave before the next one |
| EXAMPLE | Concrete instance | A calendar app that asks for your whole team before it shows a single slot |
| ANALOGY | Maps the subject onto a known domain | A restaurant that asks for your life story before it shows the menu |
| HYPO | Second-person simulation of a situation | "Imagine you signed up for your own product today" |
| CONTRAST | Opposes two cases | Short tour, users stay; long tour, users leave |
| LIST | Enumeration with announced count | "three reasons", "two possibilities" |
| TIP | Actionable advice | Cut every step that does not lead to the first result |
| EVIDENCE | Dated fact, number, source | A dated figure from a named public report |
| HISTORY | Origin and evolution of the subject | From the first product tours to today's checklists |
| NUANCE | Concession or exception that keeps the claim honest | "Some products do need a long setup" |

### E. Persona and relationship
| Code | Definition | Example (invented) |
|---|---|---|
| STANCE | Opinion stated in first person | "I think most product tours should be deleted" |
| SELF | Self-disclosure, confession | A whole weekend spent redesigning a button nobody clicked |
| RANT | Emotional diatribe on a pet peeve | Pop-ups that ask for a rating after ten seconds |
| HUMOR | Joke, absurd image, comic timing | A tour so long it needs its own tour |
| ASIDE | Quick side remark addressed to the viewer | "yes, I know, not the catchiest name" |
| OBJECTION | Voices the viewer's objection, then answers | "You might think a longer tour teaches more. Quite the opposite." |
| CONCEDE | Validates the other side | "Some teams love long setups, and that is legitimate" |
| RESEARCH | Shows the work behind the video | "I could find no public data on this" |
| ADDRESS | Direct address (you) | "your users", "your team" |
| INGROUP | Shared culture reference that rewards insiders | A joke only product managers get |

### F. Emotion and crowd
| Code | Definition | Example (invented) |
|---|---|---|
| PROOF | Social proof (views, crowd size, "most watched") | The most shared post in the company's history |
| AUTHORITY | Status of a source or of the creator | A veteran product designer, "seasoned teams say" |
| FEAR | Loss aversion, threat | You lose the user in one second |
| AWE | Scale, wonder, hyperbole | One screen decides the fate of the company |
| CATHARSIS | Release after long tension | The counter finally moves |
| NOSTALGIA | Evokes the past of the viewer or of the community | The first app you ever loved |
| TRIBE | Sorts the audience into camps | Teams who love checklists vs teams who hate them |
| RITUAL | Repeated phrase or gesture of the community | A catchphrase the community repeats at every launch |

## Tier 5 : FIGURE (rhetorical figures, optional, can be several)

ANAPHORA (repeated opening), TRICOLON (three parallel items), ACCUM (accumulation, list for effect), ANTITHESIS, HYPERBOLE, MEIOSIS (comic understatement), LITOTE (understatement by negation), IRONY (verbal), RHETQ (rhetorical question), HYPOPHORA (question then own answer), PROLEPSIS (anticipated objection), APOSIOPESIS (sentence cut off), METAPHOR, SIMILE, PERSONIF, INCONGRUITY (mixing two universes for comedy), DEFLATION (big build, small fall), REGISTER (deliberate drop to slang or vulgarity), REPETITION (keyword hammered), CHIASMUS, APOPHASIS (says it by saying they will not say it: "I will skip the pricing page, which is a mess"), COUNTERFACTUAL ("that day exists only because..."), PRIAMEL ("forget X, forget Y, the worst is Z"), PARALLELISM (same structure repeated across sentences).

Definitions and more figures: Silva Rhetoricae, https://rhetoric.byu.edu/ (consult when a figure is unclear).

## Tier 6 : PSYCH (mechanism that makes it work on a crowd)

| Code | Mechanism | Reference to consult |
|---|---|---|
| GAP | Information gap curiosity | Loewenstein 1994, https://stafforini.com/works/loewenstein-1994-psychology-curiosity-review/ and https://www.pbs.org/wgbh/nova/article/how-to-stimulate-curiosity/ |
| ZEIG | Unfinished tasks and open loops stay in memory | https://en.wikipedia.org/wiki/Zeigarnik_effect |
| TRANSPORT | Narrative transportation, absorption in a story | Green and Brock 2000, https://en.wikipedia.org/wiki/Transportation_theory_(psychology) |
| PEAKEND | Experience judged by its peak and its end | https://en.wikipedia.org/wiki/Peak%E2%80%93end_rule |
| LOSS | Loss aversion | https://en.wikipedia.org/wiki/Loss_aversion |
| SOCIAL | Social proof | Cialdini, https://en.wikipedia.org/wiki/Social_proof |
| AUTH | Authority bias | https://en.wikipedia.org/wiki/Authority_bias |
| PARA | Parasocial bond with the host | Horton and Wohl 1956, https://en.wikipedia.org/wiki/Parasocial_interaction |
| INGRP | In-group identity | https://en.wikipedia.org/wiki/In-group_favoritism |
| VAR | Variable reward, unpredictable payoff | https://en.wikipedia.org/wiki/Reinforcement |
| ANTIC | Anticipation of a known reward | |
| VICAR | Vicarious emotion through people on screen | https://en.wikipedia.org/wiki/Emotional_contagion |
| IRONY | Pleasure of knowing more than the character | https://en.wikipedia.org/wiki/Irony#Dramatic_irony |
| FLUENCY | Ease of processing (plain words, one idea per sentence) | https://en.wikipedia.org/wiki/Fluency_heuristic |
| SIGNAL | Signaling principle: cues that show structure help learning | Mayer, 12 principles of multimedia learning, https://lucidea.com/blog/mayers-12-principles-of-multimedia-learning and Mayer 2020 PDF https://ugc.futurelearn.com/uploads/files/7d/d6/7dd6188d-c343-4311-b064-ac98d2c95abc/Multimedia_Principles._R._E._Mayer__2020.pdf |
| PERSONAL | Personalization principle: conversational style helps learning | same source |
| SURPRISE | Prediction error, pattern break | |
| CATHAR | Release of accumulated tension | |

## Tier 7 : OBJECTIVE (why the creator needs this unit)

| Code | Objective |
|---|---|
| RETAIN | Keep the viewer watching (curiosity, cliffhanger, pace) |
| TEACH | Make the viewer understand or able to do something |
| MOVE | Make the viewer feel (tension, awe, laughter, catharsis) |
| FUN | Entertain, comic relief |
| TRUST | Build credibility (facts, nuance, research) |
| BRAND | Build the creator's persona and taste (personal branding) |
| BELONG | Make the viewer feel part of a community |
| ACT | Give something to use right away |
| GROW | Grow the channel (links to other videos, rabbit hole, comments bait) |

## Tier 8 : TENSION (0 to 5) and LOOPS

- TENSION: how much the viewer wants the next sentence. 0 = pure information, nothing pending. 1 = mild interest. 2 = a question is pending. 3 = stakes are stated and pending. 4 = an outcome is imminent. 5 = peak, the payoff is happening.
- LOOPS: each OPEN gets an id L## in the loop ledger with its opening unit, its closing unit and its lifetime. "Loop load" at time t = number of loops open at t.

## Tier 9 : CONNECTIVE (optional, sentence-initial)

Tags the logical link with the previous unit, following the "but / therefore" test used by screenwriters (Trey Parker and Matt Stone at NYU, https://www.firstwriter.com/articles/?GUID=3831 and https://thehustle.co/the-storytelling-secrets-that-netted-matt-stone-and-trey-parker-600-million-dollars): AND (and then, also), BUT (but, yet, except that), THEREFORE (so, therefore, that is why), BECAUSE (because), SO-WHAT (and the thing is). Use the equivalent words in the video's language. A high share of BUT and THEREFORE links is a marker of causal storytelling over listing.

## Changelog

- v1 2026-10-23: created. Codes added while tagging the first videos, after finding units with no fitting code: function RESEARCH; figures INCONGRUITY, COUNTERFACTUAL, PRIAMEL, PARALLELISM, APOPHASIS.
