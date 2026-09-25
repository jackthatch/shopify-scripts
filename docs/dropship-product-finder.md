---
name: dropship-product-finder
description: "Find dropshipping product candidates using AI + live Amazon Best Sellers data. Pulls real rank/price/rating/review data, filters out major brands, applies a price sweet-spot + demand-proof scoring, and outputs a ranked candidate list. Use when the user wants product ideas, 'winning products', or a way to surface trending/validated products to sell."
---

# Dropship Product Finder

Surface candidate products for a Shopify dropshipping store from live, free data.

**Reference:** `references/data-sources.md` — reconnaissance of every free
product-data source (what works vs. auth-gated/JS-walled as of 2026-09) for when
you extend the finder to add rising/trending signals.

## The tool

`/root/hermes-workspace/tools/find_products.py` — a CLI that fetches Amazon Best Sellers categories via the `r.jina.ai` reader proxy, parses rank/title/ASIN/price/rating/review-count, scores each product for dropship attractiveness, and outputs a ranked Markdown table or JSON.

```bash
python3 find_products.py                          # all default categories, top 15 each
python3 find_products.py --categories pets,beauty,kitchen
python3 find_products.py --min-price 15 --max-price 45 --min-reviews 1000
python3 find_products.py --top 30 --json
python3 find_products.py --categories kitchen --top 25 --out candidates.md
```

Category slugs: `kitchen home beauty health pets sports toys tools baby office auto crafts patio grocery fashion appliances`.

## Scoring logic (the "winning product" filters baked in)

Each product is scored +2/-3/etc. on:
- **Price sweet-spot** (default $8–50; the $15–45 zone is ideal — 3× markup on landed cost)
- **Rating floor** (default 4.0+)
- **Demand proof** (review count ≥ 500 default — high = proven demand)
- **Major-brand exclusion** (a `MAJOR_BRANDS` blocklist down-ranks YETI/STANLEY/Ninja/KitchenAid/etc. — these are brand-owned, not dropshippable)
- **Lightweight/shipping-friendly heuristic** (keywords like "scale", "sprayer", "liner", "holder")

The "Why" column explains each product's score so you can override the heuristic.

## Why Amazon Best Sellers (vs. other sources)

The winning-product validation funnel from the deep-research report is: engagement ratio → **real sales velocity** → margin gate → saturation check. Amazon Best Sellers is the best *free, no-auth, scriptable* proxy for "real, sustained demand" (review counts = accumulated sales). It surfaces *proven* demand; it does NOT surface *rising* products. For rising/trending signals you'd add TikTok Creative Center or Google Trends, but both are problematic from a datacenter IP (see pitfalls).

## Pitfalls / hard-won notes

- **User-Agent matters — a full Chrome UA string returns HTTP 403.** `r.jina.ai` returns a tiny ~134-byte 403 page when you send `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120...`, but returns full content (~50KB+) with a **bare `Mozilla/5.0`**. A ~134-byte response is the *403 page (UA problem)*, not a rate-limit — check the body, and fix by switching to the simple UA. This single bug cost the longest debugging time of the session.
- **`r.jina.ai` rate-limits hard.** Rapid requests also return tiny pages, but *after* the UA is fixed. `find_products.py` already has retry/backoff (4 attempts, 3/6/9s) + a 2s throttle between categories. If a run returns an empty table, re-run after a minute, or run fewer categories. A healthy Best Sellers page is ~50KB+ via jina.
- **TikTok Creative Center is auth-gated now.** The public API `ads.tiktok.com/creative_radar_api/v1/top_ads/list` returns `{"code":40101,"no permission"}` unauthenticated (as of 2026-09). The HTML page is JS-rendered and `r.jina.ai` only gets the shell (no ad data). Don't burn time on it without a logged-in session.
- **Google Trends / pytrends is broken** — `trending_searches()` returns 404 (Google changed endpoints). Don't rely on pytrends.
- **Amazon "Movers & Shakers"** (24h rank gainers = rising signal) is JS-walled; direct HTML and jina both return no product grid. Best Sellers is the reliable path.
- **Amazon raw HTML is gzip** — direct `curl` without `--compressed` returns binary garbage. `r.jina.ai` handles this; if you curl Amazon directly, add `--compressed`.
- **Many "winning" generic items are $8–13 retail** — below the ideal $15+ zone. The research says target $30–80 AOV, but Amazon's problem-solving-gadget winners skew cheap. Flag cheap items as needing a **bundle/multi-pack angle** to clear a 3× margin. Don't auto-discard them.

## Workflow

1. Run the finder for a category you're considering (or all).
2. Take the top-scored generic products (high reviews, clean "Why").
3. For each candidate, do the *saturation + margin* checks the script can't: search AliExpress/Alibaba for a supplier at a landed cost ≤ ~⅓ of the retail price, and count how many stores already run it.
4. Feed shortlisted products to a vision-capable LLM (with the viral/competitor video) to identify supplier equivalents.
5. Validate on TikTok Shop organic/affiliate before any ad spend.

The script is the *discovery + demand-proof* layer; it deliberately does not claim to find "winners" — nothing does. Public lists are a lagging indicator; the edge is in the margin + saturation + angle checks you run on top.
