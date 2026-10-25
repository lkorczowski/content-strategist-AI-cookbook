# Sorting a collection of saved videos into formats

Most creators and founders already have a format library without knowing it: hundreds of saved or bookmarked videos, grouped in collections that mix three logics. Some collections are a shape (yapping, reaction videos), some are a value (humour, educational), some are a sector or a client (fitness, a customer's industry). The job is to pull the formats out of that pile.

## Input

One row per video. A CSV with these columns works with any assistant:

| Column | Required | Notes |
|---|---|---|
| url | yes | the post link |
| collection | no | the name of the collection or folder it was saved in |
| caption | no | the post text |
| transcript | no | the platform's own captions or a transcript the user owns; the first 300 characters are enough to sort |
| views, likes, shares, saves | no | as shown on the platform |
| read_on | yes if numbers are given | the date the numbers were read |
| duration_s | no | length in seconds; 0 often means a photo post |

How to get it: use the platform's own data export or collection view, or paste links in batches. Respect each platform's terms: no scraping tools that the terms forbid, no collection of other people's personal data beyond what is needed to describe a public post.

## Sorting rules

For each row, decide one of three outcomes, using only the caption, the transcript and the numbers. When neither is enough to see the shape, mark it "unclear" and ask the user.

1. **Example of an existing card**: same structure and setup as a card (`python3 scripts/library.py similar "<one-line description>"` scores above 0.5, or the shape matches the card's Shape section). Record the card id.
2. **Candidate new format**: a repeatable shape that no card covers. Write a one-line shape, the tags, and a proposed name with the naming rule.
3. **Not a format**: the video was saved for its topic, its aesthetic, a product or a person. Record the reason in two words ("topic: nutrition").

Then group the candidates: several rows with the same shape make one candidate format with several examples. A candidate with one example only stays a candidate until a second example appears.

## Output

- A table: url, collection, outcome (card id, candidate name, not a format, unclear), one-line reason.
- The candidate formats, each with its examples, proposed name and tags.
- Collections that turned out to be pure formats (most rows map to one card): suggest renaming the collection after the format.

Write no card before the user validates the candidates. Then use `new` for each, fill it, `lint`, `build`.
