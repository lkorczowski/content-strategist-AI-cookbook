# Agent search: let AI agents search the site instead of guessing

Version 1.0, 2026-11-28. Read by statur-trades-site (section 9 bis) and statur-landing-page-audit (section 5).

## What it is

An AI agent (ChatGPT, Claude, Perplexity, a coding agent) that lands on a page finds a search endpoint on the same domain, sends its question there, and gets back the site's own passages in Markdown with a link to each page. It then answers from the source instead of from a search engine's partial index or from third-party pages about the brand.

Cloudflare shipped it as **Search for Agents** on 2026-11-25 (beta, all plans): one toggle per domain. The idea was popularised in a TikTok explainer by TJ Robertson (2026-11-28). Contract, as documented by Cloudflare:

- Endpoint: `https://<domain>/.well-known/search?q=<query>` (GET), or the HTTP QUERY method with a plain-text body or JSON `{"q": "..."}`.
- Answer: retrieved passages in Markdown (up to 10, with source links and scores), not a generated answer.
- Discovery: four meta tags in the `<head>` of every HTML page: `agent:instructions`, `agent:endpoint` (`.../.well-known/search?q={query}`), `agent:method` (`GET`), `agent:documentation`. With Markdown for Agents on, the same data sits in the page's YAML front matter under `agent:`.

What is proven and what is not: Cloudflare shows one demo (an agent found the endpoint on its docs and answered correctly). It publishes no count on how often agents use it, nor proof that agents repeat the site more than third-party sources. Treat it as a cheap bet, not a ranking lever. It does not replace SEO, llms.txt, structured data or third-party mentions.

## Which route for which site

Check first, in this order:
1. Name servers: `dig NS <domain>` (or a DNS-over-HTTPS lookup). `*.ns.cloudflare.com` means the zone is on Cloudflare.
2. Already on? `curl -s -o /dev/null -w '%{http_code}' "https://<domain>/.well-known/search?q=test"` gives 200, and the home page HTML holds `name="agent:endpoint"`.

| Site | Route | Who clicks |
|---|---|---|
| Zone on the owner's Cloudflare account (Astro on Cloudflare Pages, any proxied site) | Route A, the toggle | OWNER (dashboard sign-in, pricing notice) |
| WordPress not on Cloudflare | Route B, the plugin in templates/agent-search-endpoint.php | OWNER uploads it, or the assistant if it has admin rights and a "go" |
| Hosted builder (GoHighLevel, Wix, Squarespace, Webflow) | Route C | OWNER (DNS) |

### Route A: Cloudflare toggle

1. OWNER: Cloudflare dashboard, select the domain, **Overview**, **Quick Actions**, turn on **Search for Agents**. Read the default settings and pricing notice, confirm.
2. Wait for the first crawl. On Workers Free: 500 pages crawled per day, up to 100,000 pages per instance. The instance is called `search-for-agents-<ZONE_ID>`, refresh every 24 hours.
3. Check with the two commands above. Also run three real questions a buyer would ask and read the passages: they show what agents will repeat. Fix the pages, not the endpoint.
4. Cost: each account gets 1,000 semantic and 1,000 full-text queries a month included, then $0.75 per 1,000 semantic queries (billing from 2026-12-01, Cloudflare limits page). Source: https://developers.cloudflare.com/ai-search/platform/limits-pricing/
5. Bot rules: requests to the endpoint follow the zone's AI Crawl Control and WAF rules. If AI crawlers are blocked, the endpoint is blocked too. If Bot Management blocks the indexer, allow the AI Search crawler (Cloudflare bot directory entry "Cloudflare AI Search").

The AI Search crawler only crawls domains onboarded on the same Cloudflare account. A site that is not on Cloudflare cannot use Route A without moving its name servers first.

### Route B: WordPress without Cloudflare

`templates/agent-search-endpoint.php` reproduces the contract with the site's own WordPress search (keyword search, no vector index, no account, no cost).

1. Read the file, set nothing (no settings).
2. Install: copy it to `wp-content/mu-plugins/`, or zip it and upload it under Plugins, Add New, Upload Plugin, then activate.
3. Check: the two commands above, then three buyer questions. If `/.well-known/search` returns the theme's 404, the host serves `.well-known` itself: add a rewrite in `.htaccess` before the WordPress block, `RewriteRule ^\.well-known/search$ /index.php [L]`.
4. Caching plugins: exclude `/.well-known/search` from the page cache.
5. Remove: delete the file.

Limits: WordPress search matches words, not meaning. Good enough for a site of a few hundred pages. For semantic search, move the zone to Cloudflare (Route A) or use a search plugin that improves WP_Query, the endpoint uses it automatically.

### Route C: hosted builders (GoHighLevel and the like)

The builder serves the pages from its own infrastructure, often behind its own Cloudflare (Cloudflare for SaaS). The owner cannot run code at `/.well-known/search`.

- The only full route: OWNER moves the domain's name servers to Cloudflare (DNS change, owner only), keeps the builder's records as given by the builder, then tries Route A. Proxying a builder already behind Cloudflare is "orange to orange" and depends on the builder. Test on a quiet day, keep a copy of the DNS zone, and switch the record back to DNS only if pages break.
- Without a DNS move: no agent endpoint. Do the rest well: llms.txt with validated facts, one H1 and a clear answer per page, structured data, and the same entity facts on every profile.
- Do not point the `agent:endpoint` tag of one domain to another domain's search. Agents would answer with the wrong site's content.

## Sources

- Cloudflare blog, Search for Agents (2026-11-25): https://blog.cloudflare.com/search-for-agents/
- How-to and meta tags: https://developers.cloudflare.com/ai-search/how-to/search-for-agents/
- Changelog: https://developers.cloudflare.com/changelog/post/2026-11-25-search-for-agents/
- Website data source (same-account rule): https://developers.cloudflare.com/ai-search/configuration/data-source/website/
- Limits and pricing: https://developers.cloudflare.com/ai-search/platform/limits-pricing/
- TJ Robertson, TikTok explainer (2026-11-28): https://www.tiktok.com/@tjrobertson52/video/7713031149597084941
