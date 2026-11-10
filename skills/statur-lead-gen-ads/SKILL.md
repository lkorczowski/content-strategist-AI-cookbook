---
name: statur-lead-gen-ads
description: Plan, build and run lead generation ads on Meta and TikTok for a founder or small business. Chooses between a native instant form and one landing page per buyer profile, drafts a form that qualifies, pitches and plays, sets up a lead router to a Google Sheet with the row number as ID (Make template), writes the follow-up sequence, measures time to first call against the five-minute rule, and sets up lead quality feedback to the platform (Meta Conversions API for CRM, TikTok CRM events). Use when someone asks how to get leads from Facebook, Instagram or TikTok ads, instant form vs landing page, why their leads are bad or never answer, how to connect lead ads to a sheet or CRM, or how fast to call a lead.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/lead-generation-ads/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Lead generation ads

Part of Lead generation ads: the Meta and TikTok playbook (https://statur.co/lead-generation-ads/). Read https://statur.co/lead-generation-ads.md for the full method and its sources when you can open links.

The job: every paid lead follows the same path in minutes (row in a sheet the business owns, row number as ID, phone contact, internal alert, automatic email, call), and the platform learns each week which leads were good. Twelve recipes, numbered as on the page.

Hand-offs:
- The creative that feeds the campaign and the weekly read of a Meta account: statur-meta-ads-scaling.
- Creators paid on results whose posts run as ads: statur-creator-program.

Rules are written for US advertisers. When the user sells in France or the EU, add the page's end note (CNIL consent rules for email, prior consent for phone canvassing since August 11, 2026) and tell them to have a lawyer check consent texts.

## What to ask for

If the workspace has a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md), read it first and ask only for what is missing.
- Offer in one sentence, price range, B2B or B2C, who calls the leads and when.
- The one condition that makes a lead worth calling (role, company size, project date, area). Keep money out of the form: budget belongs to the call.
- Current campaigns: objective, optimization event, daily budget, results of the last 14 days.
- Customers: who bought, why, what they said (10 to 30 if possible).
- Where leads land today (Leads Center, CRM, sheet, email) and the lead sheet export if one exists.

## Steps

1. Objective (recipe 01). Check every campaign optimizes leads or qualified leads. Flag boosted posts, traffic or landing page view goals used to get contacts. Size ad sets so each can reach about 50 leads a week; propose fewer ad sets when the budget is short.
2. List (recipe 02). For a big campaign (Black Friday, a launch), propose a VIP list: a name, a one-line privilege, a date. Author's rule to state as a rule: 5 to 10% of the campaign's ad budget on building the list before it starts.
3. Route (recipe 03). Build the buyer profile x pain x solution grid from real customers (or competitor reviews if none). Recommend an instant form first unless the offer is high-ticket with a long pitch or several distinct profiles. Compare routes on cost per qualified lead, never cost per lead alone.
4. Form (recipe 04). Draft an instant form, Higher intent for services and B2B, More volume for a first test of a VIP list: intro card (2 lines), one qualifying multiple-choice question where one option disqualifies, one pitch question that teaches the value, one playful question (quiz or small prize draw; official rules needed), prefilled contact fields, SMS phone verification only when fake numbers pass about a quarter of leads (author's rule: each step raises the cost per lead), open sharing, tracking parameters with campaign, ad set and ad names, a completion screen that promises the callback time. Give the click list; the user clicks Publish after a test with Meta's Lead Ads Testing Tool (a published form cannot be edited, only copied).
5. Landing pages (recipe 05), only when step 3 says so: one outline per profile, the same filter question, an optional VSL outline (3 minutes or more), pixel plus Conversions API with a shared event ID. Author's rule: about 3,000 euros minimum per campaign before landing pages pay.
6. Router (recipe 07). Set up templates/lead-sheet-template.csv and templates/make-lead-router.blueprint.json (see templates/README.md). Row number in the contact name ("83 Jane Doe"). Keep the sheet even with a CRM. If the Make MCP server is connected, read the scenario first, propose changes, apply only after the user says yes.
7. Sequence (recipe 08). Plain text, one link per email: L1 instant, L2 +1 hour if not booked, L3 day 1, L4 day 3, L5 day 7; no-show N1 +1 hour, N2 day 1. CAN-SPAM footer. WhatsApp only with an opt-in that names the business; templates outside the 24-hour window.
8. Call (recipe 09). From the sheet, compute median minutes to first call, share within 5 minutes and within 1 hour, qualification rate per group. Write an opener that starts from the qualifying answer. Author's rule: above about 100,000 euros of monthly revenue, one person whose only job is to call new leads within five minutes.
9. Feedback (recipe 11). Define 2 to 3 stages reached within 28 days with a 1 to 40% rate each, map the user's statuses, and give the Zapier or Make steps for Meta Conversions API for CRM (Meta lead ID, daily upload) or TikTok CRM events (TikTok recommends more than 50 signals in 14 days). Then switch Meta's goal to conversion leads.
10. Hygiene (recipe 12). Duplicates by email then last 9 phone digits, rows without owner or next step, rows without consent source; a 20-minute weekly checklist.

## Pitfalls

1. Judging instant forms on cost per lead: in Meta's own A/B tests and one independent test, cost per qualified lead was lower on instant forms. No high-ticket B2B test exists; say so.
2. "The pixel loses half the events": no reputable source supports a general number. Recommend pixel plus Conversions API and measuring the gap in the user's own account.
3. Quoting speed-to-lead studies wrongly: HBR 2011 compared replies within an hour against later ones (nearly 7x more likely to qualify, figures read in secondary copies); the 100x and 21x figures come from a vendor-run InsideSales study comparing 5 and 30 minutes. Neither measured closed sales.
4. Giveaways that ask people to share or tag to enter: against Meta's Pages policy.
5. Leads left only in Leads Center or in a CRM the business may stop paying for.

## Rules

- Drafts only: never publish an ad, change a budget, send an email or message a lead.
- No passwords: the user signs in to Meta, TikTok, Make and Google.
- No promised cost per lead, lead volume or revenue. Label vendor data and the author's rules as such.
- Never invent a number. Use the page's figures with their sources, or ask.
