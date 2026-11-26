---
name: statur-newsletter-essay
description: Write or adapt a full newsletter essay (Substack, Beehiiv, Ghost, LinkedIn newsletter) from an article, a talk or a video, with a coverage table of the source, a mechanism before the study, claim headings, honest limits and one reply-based call to action, then an independent review before the author sees it. Use when someone asks for a newsletter issue, a Substack post, an essay version of an article, or says a draft reads like AI.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/playbooks/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Newsletter essay

A newsletter issue is a full essay, never a teaser. Readers stay in the app, and the networks reward complete posts. The goal: a reader in the target audience reads to the end, then replies or subscribes.

## Context: what this skill loads, and when

| File | Where | Read it |
|---|---|---|
| `kb/context/statur-newsletter-essay.md` | the author's private repo or project documents | At the start of every run, when it exists |
| The brand file it names (voice, proof table, client confidentiality) | same place | Steps 0, 2 and 3 |

The context file holds the publication and its audience, the author's offer line for the P.S., how drafts reach the platform, browser notes, and the author's feedback journal. No context file: ask for the publication, the audience and the call to action, and say so in one line.

## Step 0: material

1. Read the source in full (the page text, not a summary) and list every idea, example, number and source in a coverage table.
2. Open every primary source behind each number. Note who did it, what they did in one clause, the exact number, and what it does not show. Never cite a study you have not opened. Unknown fact: [SOURCE].
3. Check every outbound link. Report a dead link and leave it out.
4. Check client confidentiality before naming anyone.

## Step 1: title and subtitle

- Title with statur-hook-stacking: a claim or a finding, three hooks or more, about 12 words. The title claims only what the evidence measured.
- Subtitle: what the reader gets, plus a named proof (a study, a company, the author's own case).

## Step 2: structure (1,400 to 2,200 words; one flagship of 3,000+ a month)

1. Hook, 3 to 5 sentences: a specific scene or a claim against what the audience believes, the stakes for them, what the post delivers. Credentials in one clause at most.
2. Mechanism: why it happens, with one everyday analogy and one coined term in bold, defined once. It comes before the study.
3. First proof, introduced with the research rule below.
4. Three to five numbered sections. Each: claim, evidence, a real example (named or anonymized), what to do this week.
5. Field note: a specific case from the author's own work, real numbers only. A slightly unflattering detail is the strongest human marker: ask the author for one, never invent it.
6. "What this does not prove": 3 to 5 sentences of honest limits.
7. Close: a challenge for this week, then one reply-based call to action. The offer goes in a P.S. only.

## Research rule

Adapted from how Adam Mastroianni explains studies in Experimental History. Introduce a study in this order: who (names and institution, linked), what they did in one clause, the number, what it means for the reader, what it does not show. Never "research shows". Two or three studies at most per essay, each one changing what the reader does. Re-read every sentence that leans on a source against the source.

## Headings

Full sentences with a verb and a specific noun, readable as a summary when skimmed. Numbered for frameworks.
- Good: "How to use your comment section as a retention trap", "One fake up-vote changed what the next reader thought".
- Weak: "Five comment traps", "Key takeaways", "Conclusion", a single abstract noun.

## Rhythm

- Paragraphs of 1 to 4 sentences. Long and short sentences alternate. A question at the turns.
- First person, "you" for the reader, contractions.
- Merge two parallel short sentences into one sentence with "while" or a semicolon.
- Tells to avoid: statur-humanizer references/tells.md.

## What strong human essays never do

- Open with a definition, "today's landscape" or a generic question.
- "Research shows" with no named study, or a number with no source.
- A number followed straight by advice, with no mechanism in between.
- Abstract-noun headings, sections of equal length, triads everywhere.
- Even, medium-length sentences, no questions, no contractions.
- Vague anecdotes ("a client once..."), no coined term, the same hedge everywhere.
- A summary ending that repeats the headings, stacked calls to action, random bold.

## Reference posts (studied 2026-10-22)

Lenny's Newsletter (Kristen Lowe, "How to make people care about your startup"), Growth Unhinged (Kyle Poyar, "One year as a solopreneur"), Elena Verna ("So, you want to be a content creator?"), MKT1 (Emily Kramer, "I analyzed 1,100+ marketing job posts"), Experimental History (Adam Mastroianni), SparkToro (Amanda Natividad, "Creating and Promoting Were Never the Same Decision"), Not Boring ("An Ode to Counter-Positioning"). Read them for structure; never copy their wording.

## Step 3: review before the author sees it

1. Run statur-humanizer on the first draft and note in one line what it changed.
2. A separate reviewer that did not write the draft checks: the coverage table (every idea kept, changed or dropped, with a reason); every number and source-based sentence against its source; the structure above; the list of what strong essays never do; the author's past feedback (context file).
3. Fix, then deliver the essay with a short review: coverage, fixes, points for the author to decide.

## Step 4: draft on the platform

Save the essay as a draft on the platform, in the author's signed-in browser or through the platform's draft API. After a write through an API, close any editor tab that shows an older version: its autosave can overwrite the new draft.

## Output

```
ESSAY · <title> · <date>
Subtitle: <line>
Words: <n>
Coverage: <idea | kept / changed / dropped | reason>
Sources checked: <n> | dead links: <list>
Review: <fixes | points to decide>
Draft: <where it was saved>
```

## Rules

- Drafts only: never publish or send without the author's yes.
- No passwords, no accounts: the author signs in.
- No promised views, subscribers or results.
- No invented numbers, quotes or anecdotes: every one comes from the author or a source they can open.
- Respect each platform's terms and the clients' confidentiality.
