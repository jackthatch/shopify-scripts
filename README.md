# shopify-scripts

Scripts and tools for an AI-assisted Shopify dropshipping workflow.

## find_products.py

AI-assisted dropshipping product finder. Pulls live Amazon Best Sellers data
(rank, title, ASIN, price, rating, review count) across categories, then applies
dropshipping filters to surface candidate products worth investigating.

**What it filters for:**
- Excludes major brand-owned products (not dropshippable / trademark risk)
- Down-ranks consumables / heavy / regulated items (litter, food, skincare, etc.)
- Price sweet-spot band (default $8–$50)
- Proven demand (review count) with a rating floor (4.0+)
- Scores generic / shipping-friendly products (keyword-stuffed titles, no strong brand)

### Usage

```bash
# all default categories, top 15 each
python3 find_products.py

# specific categories
python3 find_products.py --categories pets,beauty,kitchen

# tighter filters (higher margin, more demand proof)
python3 find_products.py --min-price 15 --max-price 45 --min-reviews 1000

# more candidates + JSON output
python3 find_products.py --top 30 --json

# save to file
python3 find_products.py --categories kitchen --top 25 --out candidates.md
```

### Category slugs

`kitchen home beauty health pets sports toys tools baby office auto crafts patio grocery fashion appliances`

### How it works

Fetches Amazon Best Sellers category pages through the `r.jina.ai` reader proxy
(which renders to clean Markdown and handles Amazon's gzip/JS), parses the
product grid, scores each item, and emits a ranked Markdown table or JSON.

Each product's score is annotated with a **"Why"** column so you can see (and
override) the heuristic's reasoning.

### Requirements

- Python 3.8+
- `curl` on PATH
- Network access (uses `https://r.jina.ai/` as a fetch proxy — no API key needed)

### Important caveats

This is a **demand-discovery** tool, not a "winning product" oracle:

- It surfaces **proven demand** (high review counts = sustained sales), *not*
  rising/trending products. Public best-seller lists are a lagging indicator.
- The edge is in the checks the script can't do: **margin** (confirm you can
  clear ~3× markup by finding the landed cost on AliExpress/Alibaba) and
  **saturation** (how many stores already run it, and can you differentiate).
- Most $8–13 generic winners need a **bundle / multi-pack angle** to hit the
  3× margin threshold worth running ads on.
- `r.jina.ai` rate-limits under rapid requests. The script retries with
  backoff, but if a run returns an empty table, wait a minute and re-run.

## Background

Built as part of research into AI-automated Shopify dropshipping. Companion
methodology documented in `docs/dropship-product-finder.md`.
