# shopify-scripts

Scripts and tools for an AI-assisted Shopify dropshipping workflow.

## The pipeline

1. **`find_products.py`** — find candidates (live Amazon Best Sellers demand data)
2. **`price_products.py`** — price them for margin (live AliExpress source cost)

Run them in sequence to go from "what's selling" → "what should I charge":

```bash
# 1. find candidates + save as JSON
python3 find_products.py --categories golf,furniture --top 12 --json --out candidates.json

# 2. price the top candidates against their market price
python3 price_products.py --from-json candidates.json --limit 10
```

---

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

---

## price_products.py

Pricing & margin engine. For each candidate, searches AliExpress for the real
**source (landed) cost**, then computes what you should charge to hit a target
margin — and flags whether there's actually room.

```bash
# price specific products
python3 price_products.py --products "golf umbrella,tv wall mount"

# price candidates from the finder (compares to their Amazon market price)
python3 price_products.py --from-json candidates.json --limit 10

# adjust the margin target
python3 price_products.py --products "golf umbrella" --markup 4 --shipping 5
```

### The margin model

| Input | Default | Meaning |
|---|---|---|
| `--markup` | 3.0 | retail = landed cost × markup (the "3× rule") |
| `--fee` | 0.03 | payment-processing fee |
| `--shipping` | 3.0 | per-item shipping buffer (conservative) |

At 3× markup: **gross margin ≈ 64%**, **break-even ROAS ≈ 1.57×** (you need
$1.57 back per $1 of ad spend to break even — so you can spend up to ~64% of
revenue on acquisition and still break even).

### The verdict

The engine compares your 3× price to the product's **market price** (Amazon):

- **GOOD** — 3× price is *under* market → room to price up to market and keep full margin
- **OK** — 3× price ≈ market → viable but no pricing power
- **THIN** — source too close to market → not enough margin at 3×; find a cheaper supplier or skip

### Caveats

- **Bait prices:** AliExpress shows a "from $X" price (cheapest variant/accessory).
  The engine drops sub-$2 bait prices and uses the median of the realistic range.
- **Variant mismatch:** source cost depends on matching the *exact* spec (size,
  quality, pack size). The median is a directional estimate — confirm the
  specific variant before ordering.
- **"Free shipping"** on AliExpress often already includes the shipping cost in
  the price; the `--shipping` buffer is a conservative hedge, not double-counting
  you should treat as gospel.

## Background

Built as part of research into AI-automated Shopify dropshipping. Companion
methodology documented in `docs/dropship-product-finder.md`.
