# Lead generation ads: the Meta and TikTok playbook

From the ad objective to a call in five minutes: a VIP list, an instant form or one landing page per buyer profile, a form that qualifies, pitches and plays, a Google Sheet router with row numbers, the follow-up sequence, the five-minute call, quality feedback to Meta and TikTok, and list hygiene. US rules, with an end note for France and the EU.

- Page (human version, source of truth): https://statur.co/lead-generation-ads/
- Markdown for AI assistants: https://statur.co/lead-generation-ads.md
- Version 1.0, 2026-11-10; skill statur-lead-gen-ads 1.0.0

## Summary

Ask the platform for leads: it optimizes the event you buy. Build a VIP list with a real privilege before a big campaign. Start with a Higher intent instant form with three questions (qualify, pitch, play); build one landing page per buyer profile, tracked with pixel plus Conversions API, when the budget and a long pitch justify it. Route every lead to a Google Sheet you own, use the row number as its ID, create the phone contact, alert the caller, start the sequence in minutes, call within five minutes. Mark lead quality every week and send the stages back to the platform. Keep the list clean and consented.

## Skills

| Skill | Use it for |
|---|---|
| [statur-lead-gen-ads](../skills/statur-lead-gen-ads/) | The twelve recipes: objective, VIP list, route, form, landing pages, AI setup, router (templates), sequence, five-minute call, playful forms, quality feedback, hygiene. |
| [statur-meta-ads-scaling](../skills/statur-meta-ads-scaling/) | The creative and the weekly read of the Meta account that feeds the campaign. |

## Templates

- [lead-sheet-template.csv](../skills/statur-lead-gen-ads/templates/lead-sheet-template.csv): the sheet columns.
- [make-lead-router.blueprint.json](../skills/statur-lead-gen-ads/templates/make-lead-router.blueprint.json): the Make scenario, without any private ID.
