---
name: statur-trades-site
description: Build and launch a tradesperson's website with Astro, GitHub and Cloudflare Pages, step by step and as automatic as possible: prerequisites, content brief from the company file, art direction from images the owner loves (statur-art-direction), pages, contact form, tests, free hosting, own domain without breaking email, local SEO, then a daily upkeep task. Use when a tradesperson asks for a website, a client asks them "do you have a site?", or an existing site must be moved off an agency.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/tradespeople-video-handbook/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Trades website with Astro

Part of The One-Hour Video Handbook for Tradespeople (https://statur.co/tradespeople-video-handbook/). The videos feed the site; the site turns searches into calls.

The job: a fast, simple, honest site that the owner owns (domain, code, hosting account in their name), costs nothing to host, and that the assistant can update from a sentence.

Who does what: the assistant does everything it can in the terminal and in the browser. The owner does only what is theirs: create accounts, pay, type passwords, change DNS, say "go". Mark each owner step "OWNER" and prepare it so it takes one click.

## Single responsibility

This skill builds, tests, deploys and maintains the site. The look comes from statur-art-direction. The words come from the company context file. Article routines from videos belong to statur-trades-morning-routine; the site audit to statur-trades-setup.

## 0. Read the context first

Read the company context file (kb/01_BRAND.md, kb/01_ENTREPRISE.md or .agents/product-marketing.md), the content file (angle, photos) and any site notes (kb/06_SITE.md). Keep what is decided. Ask only for what is missing, one short question at a time:
- Trade, services, towns covered, phone, pro email, opening hours.
- The one action a visitor should take (call, ask for a visit, ask for a quote).
- Legal details for the legal notice: company name, SIREN or SIRET, address (to confirm with the accountant).
- Does a domain exist, where (OVH, Gandi, an agency), and in whose name. If an agency holds it, the first job is to get it back in the owner's name.

Write the answers in kb/06_SITE.md. Track progress there with a checklist; a step is done only with a proof you checked (a URL that opens, a commit, a test result).

## 1. Prerequisites (OWNER, about 30 minutes, guided)

Check each one yourself before going on.
1. Pro email on the domain (Google Workspace or the host's mail). Without a domain yet: buy one in the owner's name (about 5 to 15 euros a year); OWNER pays.
2. GitHub account with the pro email. Connect GitHub in the assistant's connectors.
3. Cloudflare account (free) with the pro email.
4. Node.js and git on the computer (the assistant checks `node -v` and `git --version` and installs what is missing from the terminal).

## 2. Art direction first

Run statur-art-direction until DESIGN.md is validated by the owner. No page is built on the default look. If the owner is in a hurry, at least do its steps 1 (images), 3 (refused list) and 4 (tokens) in one sitting.

## 3. Create the project (assistant)

1. In the browser, open github.com/new and fill in a public repository named site-<company>. OWNER clicks "Create repository".
2. Clone it next to the assistant's folder. Create an Astro project inside, minimal template, no UI kit: `npm create astro@latest -- --template minimal --no-install --skip-houston .` then `npm install`.
3. Copy tokens.json into src/styles and generate the CSS variables from it. One layout, one stylesheet, plain Astro components. No Tailwind template look, no icon packs by default.
4. Add `@astrojs/sitemap`, set `site` in astro.config to the final domain.
5. Commit and push to main.

## 4. Pages (assistant)

Start small and true. Every page answers what a client types in Google.
1. Home: who, where, the promise in one sentence, a real photo of the owner or a job, the phone as a big tap-to-call link, the main action.
2. One page per service, with the words clients use, the towns covered, real photos.
3. Jobs (réalisations): before / after, one page per job, no client name without their written consent.
4. About: the owner, how they work.
5. Contact: phone, pro email, area, hours, the form.
6. Legal notice and privacy: company details, host (Cloudflare), what the form collects. Information only, to confirm with the accountant.

Never invent a price, a review, a number of jobs, a certification or a guarantee. Missing facts are written "to confirm" and asked to the owner. Reviews come from the Google Business Profile, linked or quoted with permission.

## 5. Contact form

Default, no account and no server: a form that opens a pre-filled email (subject, town, project, availability) to the pro address, plus the phone link. Optional, if the owner wants messages without opening their mail app: a form service in their name (they create the account and give the public key), or a Cloudflare Pages Function. Test with a real message either way.

## 6. Tests before every deploy

- `npm run build` with zero errors.
- Screenshots at 1280 px and 390 px of every page; no horizontal scroll, text readable, phone link visible without scrolling on mobile.
- Every link and the form tested; the phone link opens the dialer.
- Refused-tells scan from statur-art-direction on the built HTML.
- Page weight: images resized and in WebP or AVIF, each page under about 1 MB.
- Basic SEO: one H1 per page, a title and a description per page, alt text on photos, sitemap present, LocalBusiness structured data with the real name, phone, address and area.

## 7. Put it online (OWNER guided, 10 minutes)

1. Cloudflare dashboard, Workers & Pages, Create, Pages, Connect to Git, allow only the site repository.
2. Framework preset Astro, build command `npm run build`, output folder `dist`. Save and deploy. The site is live on a .pages.dev address; open it and check it yourself.
3. From now on every push to main updates the site.

## 8. The owner's domain without breaking email (OWNER, careful)

Do this step on a call or step by step: one mistake stops the emails.
1. Before anything, list the current DNS records at the registrar and copy them to kb/06_SITE.md: MX, SPF (TXT v=spf1), DKIM, DMARC, verification TXT.
2. Lessons from the first site:
   - If DNSSEC is on at the registrar, switch it off before changing name servers, wait a few hours, re-enable it later at Cloudflare. Otherwise site and email go dark.
   - Keep exactly one SPF record (for Google Workspace: `v=spf1 include:_spf.google.com ~all`). Two SPF records is an error.
   - Remove the registrar's parking records (A record, ftp CNAME, old TXT) in Cloudflare before attaching the domain.
   - The bare domain can be attached to the Pages project only once the zone is active at Cloudflare.
3. Add the domain to Cloudflare, check the mail records are present there, then OWNER changes the name servers at the registrar.
4. Attach the domain and www to the Pages project. Check: the site opens on https, http redirects, and an email sent to the pro address still arrives.
5. Then sign the emails: DKIM from the mail provider, DMARC `v=DMARC1; p=none;`. Verify with "show original": SPF, DKIM and DMARC pass.

## 9. Local visibility (assistant prepares, OWNER validates)

- Google Business Profile: link the site, same name, phone and address everywhere, 10 job photos, the services and the area.
- Google Search Console: OWNER verifies the domain (a TXT record), the assistant submits the sitemap.
- Ask five happy clients for a Google review (the assistant drafts the message, the owner sends it).

## 10. Daily upkeep (scheduled task)

Offer one scheduled task, every morning or once a week, that: checks the site answers and the form works, lists broken links, reads Search Console when connected, proposes one improvement (a missing service page, a town page, a job page from the last video) as a branch with a pull request and a Cloudflare preview link. The owner looks on the phone and says "go"; the assistant merges. Before creating the task, check it runs without the owner and brings real value; otherwise do not create it.

Day-to-day changes follow the same rule: the site is public, so changes go through a branch, a preview link and the owner's "go". The owner's private notes (kb/, pilotage/) are saved directly.

## Rules

- Drafts only: nothing goes live without the owner's "go" on the preview.
- The owner owns the domain, the GitHub repository and the Cloudflare account; never in the assistant's or an agency's name.
- No passwords typed by the assistant, no payments, no account creation on the owner's behalf; DNS changes are clicked by the owner.
- No invented prices, reviews, numbers, clients, labels or guarantees; "to confirm" instead.
- No reproduction of a reference artist's work; real photos with the owner's rights only.
- Legal notice and privacy: information only, to confirm with the accountant.
