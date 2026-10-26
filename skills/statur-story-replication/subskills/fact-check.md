---
name: fact-check
description: Verify every fact of a replicated script against its research dossier and live sources before delivery, with a separate agent, and fix or remove what fails. Use as the last step of statur-story-replication or on any script with numbers, dates and quotes.
---

# Fact-check

## Dossier format (research/dossier.md)

One line per fact: `F## | YYYY-MM-DD | claim | value | [source](url) | confidence high/medium/low | used in blocks`.
Quotes: under 15 words, in quotation marks, with the exact source. Everything else paraphrased.

## In the script

Every sentence that carries a number, a date, a name in a factual role, or a quote ends with its ids: `[F07]` or `[F07, F12]`. Sentences in the audience thread (hypotheticals) carry `[HYPO]`. Opinions of the host carry nothing.

## Verification pass (separate agent, did not write the script)

1. Extract every `[F##]` sentence.
2. For each, open the source and check: the number, the date, the wording of quotes, the direction of the claim (a forecast is not a fact, a reported figure is "reported by").
3. Search for a newer figure when the claim is about the present (valuations, revenue run-rates, user counts move monthly).
4. Output a table: id, verdict (ok, fix, remove), correction, source.

## Rules

- A low-confidence fact never carries a turning point of the story.
- Reported numbers are attributed ("according to Reuters"), estimates are called estimates.
- Superlatives ("fastest", "biggest") need a source that says it, or become a number.
- Never present a hypothetical, a composite or a forecast as an event.
- The date of the last check goes at the top of the script: facts about fast-moving companies age in weeks.
