# shopify-scripts

Tools for an AI-assisted Shopify dropshipping workflow. Three scripts form a
pipeline that goes from **"what's selling" → "what are people searching with
intent" → "what should I charge (and can I clear a high-ticket floor)".**

```
find_products.py  ──►  search_intent.py  ──►  price_products.py
   (demand)              (search intent)         (margin / high-ticket)
```

They are deliberately **modular and no-auth** — each reads the previous script's
JSON (or a plain keyword list) so you can run any stage in isolation, and none
require API keys (just `curl` + network; `search_intent.py` additionally needs
`pip install pytrends` for the Google Trends signal).

---

## Quickstart

```bash
pip install pytrends          # only needed for search_intent.py trends

# 1. Discover candidates in the high-ticket convergence niche
python3 find_products.py --categories lighting,lamps,home-decor,storage \
    --top 20 --json --out candidates.json

# 2. (optional) enrich with search-intent: long-tail queries + 12-mo trend
python3 search_intent.py --from-json candidates.json --limit 20

# 3a. Classic 3x margin vs. Amazon market price
python3 price_products.py --from-json candidates.json --limit 20

# 3b. High-ticket (Google Shopping) mode: clear a $49.99 floor at 5–10x
python3 price_products.py --from-json candidates.json --mode high-ticket --limit 20
```

---

## `find_products.py` — demand discovery

Pulls **live Amazon Best Sellers** data (rank, title, ASIN, price, rating,
review count) per category via the `r.jina.ai` reader proxy, then scores each
product for dropshipping attractiveness.

**Scoring (each product annotated with a "Why" column):**

| Signal | Effect |
|---|---|
| Price sweet-spot (default $8–50) | +3 / −1 outside band |
| Rating floor (default 4.0+) | +2 / −3 below |
| Demand proof (reviews ≥ 500) | +3 / −1 below |
| Major-brand blocklist hit | −4 (dropship/trademark risk) |
| Consumable / heavy / regulated | −3 (shipping/regulatory) |
| Lightweight/shipping-friendly keyword | +1 |

**Usage**

```bash
python3 find_products.py                          # all categories, top 15 each
python3 find_products.py --categories lighting,lamps,home-decor
python3 find_products.py --min-price 15 --max-price 80 --min-reviews 1000
python3 find_products.py --top 30 --json --out candidates.json
```

**Category slugs** — full list (see `CATEGORIES` dict in the source for URLs):

- Broad: `kitchen home beauty health pets sports toys tools baby office auto crafts patio grocery fashion appliances golf`
- Home/furniture/bedding: `furniture bedding sheets blankets comforters duvet`
- **Home-goods / lighting / outdoor (the high-ticket convergence niche):**
  `lighting outdoor-lighting wall-lights lamps home-decor wall-decor storage`

**Key caveat:** the blocklist (`MAJOR_BRANDS`) is a *best effort* — it will
occasionally let a major brand through (a false "clean" hit). Always eyeball the
top rows before trusting them. If a niche is new to you, add its brands to
`MAJOR_BRANDS` and heavy/bulky terms to `CONSUMABLE_HINTS` first.

---

## `search_intent.py` — the search-intent signal layer

Adds two free, no-auth signals measuring **what people are actually searching
with intent** (the Google-Shopping premise: the buyer is already searching with
their wallet out, so winners are products with *active, growing* search demand):

1. **Google Autocomplete** (`suggestqueries.google.com`) — the real long-tail
   queries people type. Doubles as a ready-made keyword list for SEO titles.
2. **Google Trends** (`pytrends` `interest_over_time`, 12-month) — classified
   **RISING / STABLE / DECLINING / SEASONAL**.

**Usage**

```bash
python3 search_intent.py --keywords "outdoor wall light,doormat,placemat"
python3 search_intent.py --from-json candidates.json --limit 20
python3 search_intent.py --from-json candidates.json --skip-trends   # autocomplete only
python3 search_intent.py --keywords "..." --json --out enriched.json
```

**Output columns:** `intent` (HIGH/MEDIUM/LOW/NONE from suggestion volume),
`suggestion_count`, `trend` (direction + shape), top `intent_queries`.

> **Note on pytrends:** `trending_searches()` is broken (404 — Google changed
> the endpoint), but `interest_over_time()` works fine and is what this script
> uses. From a datacenter IP it can be slow/rate-limited — `--skip-trends`
> falls back to autocomplete-only if it's being flaky.

---

## `price_products.py` — margin + high-ticket engine

Searches **AliExpress** for the real source (landed) cost of each product, then
computes the pricing/margin picture. Two modes:

### Classic mode (default) — the "3× rule" vs. Amazon

```bash
python3 price_products.py --products "golf umbrella,tv wall mount"
python3 price_products.py --from-json candidates.json --limit 10
python3 price_products.py --products "golf umbrella" --markup 4 --shipping 5
```

- retail = landed × `--markup` (default 3.0)
- At 3×: **gross margin ≈ 64%**, **break-even ROAS ≈ 1.57×**
- Verdict vs. market: **GOOD** (3× *under* market) / **OK** (~= market) /
  **THIN** (source too close to market).

### High-ticket mode — the Google-Shopping play

```bash
python3 price_products.py --from-json fixtures.json --mode high-ticket
python3 price_products.py --products "floor lamp,pendant light" --mode high-ticket \
    --floor 49.99 --ceiling 250 --markup-lo 5 --markup-hi 10
```

The question **flips** from classic mode. Instead of "is 3× under the market
price?", it asks **"can I clear a `$49.99` minimum at `5–10×` source cost — and
how far above the Amazon market price is that?"**

Verdicts:

| Verdict | Meaning |
|---|---|
| `HIGH-TICKET ✓ UNDERCUT <1x` | you'd be *below* market — best |
| `HIGH-TICKET ✓ PREMIUM 1–2x` | defensible premium (better images justify it) |
| `HIGH-TICKET ✓ AGGRESSIVE >2x` | needs strong brand/images to justify |
| `LOW-TICKET` | 5× lands below the floor (bundle or skip) |
| `OVER-PRICED` | 5× exceeds the ceiling |

**Why this mode exists:** the classic 3× benchmark returns THIN on almost every
generic item because Amazon already compresses prices near ~2–2.5× source. The
Google-Shopping / high-ticket play instead charges *more* than Amazon for the
same product, justified by premium AI-generated images, SEO-optimized titles,
and buyer intent (searching with wallet out). Lighting fixtures (floor lamps,
pendants, chandeliers) are the canonical example — source $10–18 → $80–180
retail naturally clears the floor, whereas $2–6 accessories (doormats, placemats)
need aggressive 15–20× to clear it.

---

## Pipelines / recipes

```bash
# Golf-apparel (the classic 3x winner)
python3 find_products.py --categories golf --top 30 --json --out golf.json
python3 price_products.py --from-json golf.json --limit 20

# High-ticket lighting/home-goods (the convergence niche)
python3 find_products.py --categories lighting,lamps,outdoor-lighting,wall-lights \
    --top 25 --json --out lighting.json
python3 search_intent.py --from-json lighting.json --limit 25
python3 price_products.py --from-json lighting.json --mode high-ticket --limit 25
```

---

## Requirements

- Python 3.8+
- `curl` on PATH
- Network access (uses `https://r.jina.ai/` as a fetch proxy — no key needed)
- `pip install pytrends` (only for `search_intent.py` trends)

## Pitfalls (hard-won)

- **User-Agent matters for `r.jina.ai`:** a full Chrome UA string returns HTTP
  403 (tiny ~134-byte page). Use a bare `Mozilla/5.0`. A ~134-byte response is
  the *403 page (UA problem)*, not rate-limiting.
- **`r.jina.ai` rate-limits hard.** The scripts retry with backoff + throttle,
  but if a run returns an empty table, wait a minute and re-run, or run fewer
  categories.
- **pytrends `trending_searches()` is 404**; use `interest_over_time()`.
- **Amazon raw HTML is gzip** — `r.jina.ai` handles it; if you curl Amazon
  directly, add `--compressed`.
- **AliExpress "from $X" bait prices** — the engine drops sub-$2 bait and uses
  the median of the realistic range. Confirm the *exact variant* before ordering.
- **Category node IDs drift.** The correct Amazon node for "bedding" is
  `1063252` (not `1063278`, which is *Home Décor*). Lighting lives under
  `zgbs/hi/` (Tools & Home Improvement), not `home-garden`. Re-derive nodes from
  the Best Sellers breadcrumb if a category returns the wrong products.

## Background

Built during research into AI-automated Shopify dropshipping. Strategic context,
findings, and the decision framework are in **`HANDOFF.md`**; per-niche playbook
and data-source reconnaissance in the `dropship-product-finder` skill.
