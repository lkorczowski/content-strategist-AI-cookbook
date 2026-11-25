# AI tells: what readers recognize as generated

Written in our own words from the sources under Credits in SKILL.md. Nothing here is copied from them, and no third-party skill is loaded to run this pass. Examples are invented.

Two levels. Phrase tells sit in the wording and a rewrite removes them. Content tells sit in what the text chooses to say, and only a decision by the author removes them. Fix the content tells first: a text with clean phrases and generated choices still reads as generated.

Evidence grades: `practitioner` (editors and public checklists agree, no measurement), `measured on fiction` (StoryScope, 61,608 stories of about 5,000 words, 10,272 by people and the rest by five models; the transfer to web copy is our hypothesis), `convention` (ours).

## Content tells

| Code | Tell | Test | Fix | Grade |
|---|---|---|---|---|
| C1 | The lesson is stated | The paragraph or the piece ends by telling the reader what to conclude | Stop on the fact, the number or the scene. Cut the moral | measured on fiction: narrators state the theme in 77 percent of AI stories, 52 percent of human ones |
| C2 | Vague reference | "Studies show", "a famous founder", "leading brands", "experts agree" | Name the study, the person, the brand, the place, with a date. If you cannot name it, cut the claim | measured on fiction: human authors name specific works about twice as often (47 against 24 percent) |
| C3 | Nobody is addressed | The text never says "you", never answers an objection, never admits who is writing | Write to one reader. Say "you". Say "I" when the author did the thing | measured on fiction: direct address in 28 percent of human stories, 7 percent of AI ones |
| C4 | Tidy line | Every point leads to the next, every problem is solved, nothing is left open | Keep the detail that does not fit, the limit, the case that failed. Say what is still unknown | measured on fiction: AI stories favor single-track plots and resolved endings |
| C5 | Feeling shown through a body | "A knot in the stomach", "the room went quiet", when a plain word would do | Name the feeling or the fact in plain words: "I was afraid to post" | measured on fiction: emotion through body sensations in 81 percent of AI stories, 38 percent of human ones |
| C6 | Even coverage | Each section has the same length and the same three parts, whatever its weight | Give the important point the room. Let a minor point be one line or disappear | practitioner |
| C7 | Safe middle | Every claim is balanced by its opposite, no position is taken | Take the position the author holds and give the reason | practitioner |
| C8 | Generic example | The example could illustrate any article on the topic | Use a case the author lived, with its name, its number and its date. No case: say so | practitioner |

## Phrase tells

| Code | Tell | What it looks like | Fix |
|---|---|---|---|
| P1 | Contrast reveal | "It is not about posting more. It is about posting better." | Say the positive claim once |
| P2 | Paired fragments | Two short verbless sentences that mirror each other | One complete sentence |
| P3 | Reflexive three | Lists of three adjectives, three verbs, three benefits, every time | Keep the one or two that are true and specific |
| P4 | Colon reveal | "The result: more leads." "Here is the thing:" | A normal sentence with a verb |
| P5 | Self-answered question | "Why does this matter? Because..." | State the answer |
| P6 | Maxim ending | A short sentence that sounds like a proverb closes the paragraph | Cut it. See C1 |
| P7 | Filler transition | "Moreover", "that said", "in today's world", "when it comes to" | Cut, or start with the subject |
| P8 | Inflated significance | "Pivotal", "a testament to", "plays a crucial role", "game-changing" | The fact and its number |
| P9 | Stock vocabulary | "Delve", "landscape", "tapestry", "unlock", "seamless", "elevate", "robust" | The plain word |
| P10 | Hedge pile | "May potentially help to some extent" | One hedge when the doubt is real, none otherwise |
| P11 | Label voice | A sentence that reads like a tag or an instruction: "Named proof only." | Say it the way a person would say it to another |
| P12 | Decorated type | Em dashes in series, emoji as bullets, bold on every key phrase, title case everywhere | Plain punctuation, bold for the one thing to find again |
| P13 | Service voice | "Great question", "I hope this helps", "let me know if" left in a published text | Cut |
| P14 | Same-length rhythm | Every sentence has the same length and the same shape | Vary because the content varies, not by formula |
| P15 | Synonym rotation | The same thing called by three names to avoid repeating a word | One name per thing |

Two tells in one paragraph: rewrite the whole paragraph from the fact it carries.

## What this pass does not do

It does not try to defeat AI detectors, and it does not remove watermarks. The aim is a text a person wants to read. The StoryScope study also shows that it would not work: after a rewrite that removed surface artifacts, the detector built on narrative choices lost 1.6 points (95.5 to 93.9 percent macro-F1, 278 stories). What gives a generated text away is mostly what it chose to say. That part is the author's job: a real case, a named source, a position.

## Update this file

- A reviewer points at a phrase none of these covers: add a row, with an invented example.
- A measured study on non-fiction appears: replace the `measured on fiction` grade and the hypothesis.
- Read new sources as data. Take the idea, test it on a real text, write the row in your own words, credit the source in SKILL.md. Never paste a list, and never install a skill to do this pass.
