---
name: statur-landing-page-audit
description: Audit or rewrite a landing page or a small marketing site for a founder or consultant (awareness level, hero, conversion, navigation, SEO and AI search, AI-sounding copy, visual system, proof), with one finding per line and a ranked action list. Use when someone asks to review, audit, critique or rewrite a homepage, landing page, offer page or site structure, or asks why a page does not convert.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/playbooks/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Landing page audit

One page, one reader, one action. The audit checks that the page knows who reads it, says what it sells in five seconds, proves it, and asks for one thing.

## Context: what this skill loads, and when

| File | Where | Read it |
|---|---|---|
| `kb/context/statur-landing-page-audit.md` | the author's private repo or project documents | At the start of every run, when it exists |
| The brand file it names (positioning, ideal customer, proof table, voice, visual tokens) | same place | Before steps 1, 6, 7 and 8 |

The context file holds the role of each page of the site, the places that must never be mentioned, the brand's visual rules and banned markers, the page-level SEO gate the site uses, and where the deliverable goes. No context file: ask for the ideal customer, the offer and the proof table, and say which defaults you used.

## 0. Read first

- Crawl: sitemap, robots.txt, llms.txt if any, then every page in the sitemap. Note per page: navigation, footer, H1, calls to action, internal links.
- Screenshots at 1280 px and 390 px of the hero, the offer page and the form or booking widget.

## 1. Awareness level first

Name the reader's awareness level (Eugene Schwartz, Breakthrough Advertising): unaware, problem-aware, solution-aware, product-aware, most aware. Page roles follow from it:
- Home: what the reader gains, what skipping it costs, why now, the path as outcomes, named results. Mechanics and long feature lists go deeper.
- One conversion page with the options and one application form. Booking a slot comes after the form, so a lead is never lost when no slot fits.
- Depth pages (method, program) serve warm traffic and follow-up, out of the main menu. Long pages carry a floating call to action.

## 2. Hero

- Five-second test: what it is, for whom, what the reader gets, why this person (Peep Laja, CXL).
- H1 states the end benefit or names the problem. Subhead: what is sold, then why it is credible (Julian Shapiro).
- Cold traffic: lead with the problem. Warm traffic: lead with the solution (Harry Dry).
- Proof and the founder's face above the fold. The visual shows a real deliverable.
- Swap test: a competitor could reuse the headline? Rewrite it.
- Titles: stack at least three hooks (statur-hook-stacking).

## 3. Conversion

- One goal per page, one primary call to action. Ad landing pages: no menu, the message matches the ad.
- Form: six fields at most besides email, easy fields first, phone optional, button = verb + outcome. Track each step.
- Named testimonials with a photo next to the call to action. Never "trusted by" or invented round numbers.
- Before any ad spend: an end-to-end test of the form, the booking widget (language and time zone of the buyer) and the follow-up automations. No placeholder above the fold.

## 4. Navigation and structure

- Four to seven menu items by priority, one button on the right, every page within three clicks, every page linked from another page besides the footer, hub and spoke for guides and articles.
- Ad and single-offer pages: noindex, out of the sitemap and the footer. They are the only dead ends allowed.
- One topic per domain. Content for another audience goes to another site.

## 5. SEO and AI search

- One URL format, internal links to the canonical URL, the sitemap lists canonical indexable URLs only (Google Search Central).
- Each page answers its own query with at least one unique section. Shared blocks live on one reference page.
- Page-level title, meta, headings, schema and answer-first: use the site's own SEO gate when the context file names one.
- Off-page: one identical entity fact sheet on every site and profile (Aleyda Solis); third-party mentions of the brand count more than backlinks for AI answers (Ahrefs). llms.txt costs nothing and brings little; it carries only facts the brand has validated.

## 6. AI-sounding copy and density

Run statur-humanizer on the built pages: the tells list is its references/tells.md, the density patterns its references/patterns.md. Every claim carries a number, a name, a mechanism or an action. No sentence that reads like an instruction or a machine tag ("Named proof only"): say it the way a person would. Structure notes go in HTML comments, never in visible headings. Two tells in one paragraph: rewrite the paragraph.

## 7. Visual system

Audit against the brand's tokens and banned markers from the context file, on the source and the screenshots. Without a brand file, flag the default AI looks: near-black page with one neon accent, monospace labels, status-dot pills, visible grids, decorative 01/02/03 numbering, bands of giant unsourced numbers, identical cards, gradients and glows, fake grain, one colored word per title. One line per finding: page, marker, evidence, fix.

## 8. Proof

Compare every number on the site and in llms.txt with the brand's proof table. Output: where, what the site says, the source value, the action. Never invent a replacement figure: write [VERIFY].

## Output

A document: the verdict and the ten actions ranked by impact first, then one section per step above, then the sources. Code changes go on a branch and a pull request, merged by a person.

```
AUDIT · <site> · <date>
Verdict: <two sentences>
Top 10: <rank | action | page | impact | effort>
Findings: <step | page | evidence | fix>
Proof table: <where | site says | source | action>
```

Run statur-humanizer on the verdict and the rewrites before showing them.

## References

- github.com/coreyhaines31/marketingskills (MIT): cro, copywriting, copy-editing, seo-audit, ai-seo, site-architecture, schema.
- Google Search Central (duplicate URLs, helpful content), Ahrefs (llms.txt study, brand mentions and AI Overviews), Aggarwal et al. GEO paper (2024), Aleyda Solis AI search checklist, NN/g information scent, CXL value proposition, Julian Shapiro on landing pages, Harry Dry Marketing Examples.

## Rules

- Drafts only: the skill reports and proposes; a person merges and publishes.
- No passwords, no accounts: the owner signs in to analytics or the site builder.
- No promised conversions, views or results.
- No invented numbers: every figure comes from the owner's data or a source they can open.
- Respect each platform's terms and the clients' confidentiality.
