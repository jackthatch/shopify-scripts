# HANDOFF.md — strategy, findings, and decision framework

Context for anyone (human or Claude) picking up this repo. Read this **before**
running the scripts, so you understand *why* the tools are shaped the way they
are and what the two operating models are.

---

## 1. The two operating models (this is the core mental model)

There are **two different dropshipping businesses**, and they need different
economics. Don't conflate them.

### Model A — "TikTok / impulse" (classic 3× winning-product)

- Sell cheap problem-solving gadgets at **3× landed cost** (~64% GM, 1.57×
  break-even ROAS).
- Acquire via **Facebook/TikTok/IG ads** — impulse, needs fresh video creatives
  daily, can't be fully automated.
- Buyer has no intent; you *manufacture* the desire with a creative.
- **Finding:** our margin engine (`price_products.py --mode classic`) returns
  **THIN on almost every generic item** because Amazon already compresses
  prices near ~2–2.5× source. The only place 3× reliably cleared was
  **golf/travel apparel** (identity buyers pay $30–35 for $2–6 source).

### Model B — "Google Shopping / high-ticket" (volume + intent + premium)

- Sell **higher-ticket home goods** ($49.99 floor, $80–250 ideal) at **5–10×
  source**, justified by *premium* AI images, SEO titles, and **buyer intent**.
- Acquire via **Google Shopping / Performance Max** — the buyer is already
  searching ("outdoor wall light") with their wallet out; no creative needed.
- The insight: on Google you can charge **more** than Amazon for the *same*
  product because the listing *looks* premium and the buyer has intent.
- Reference: Romas Ecom's method (transcript in `/root/research/romas-transcript.txt`).
  His example store (home interior / outdoor / kitchen / storage, 2,700 SKUs)
  sells $20 AliExpress items at $125–225.

**The convergence point** we identified: the **lightweight home-goods / lighting
/ outdoor** layer. It's where (a) high-ticket economics work, (b) the "lightweight
accessory layer" of the home niche (NOT freight-heavy furniture) is viable, and
(c) buyer intent is strongest.

---

## 2. What we've built

| Script | Role | Mode |
|---|---|---|
| `find_products.py` | Amazon Best Sellers demand + brand/consumable filtering | — |
| `search_intent.py` | Google Autocomplete (long-tail intent) + Google Trends (12-mo direction) | — |
| `price_products.py` | AliExpress source cost → margin verdict | `--mode classic` (3× vs Amazon) |
| `price_products.py` | — | `--mode high-ticket` ($49.99 floor, 5–10×, premium headroom) |

Pipeline: **find → intent → price**.

---

## 3. Key findings (so far)

### The margin engine is brutal — and that's the point
Priced **34 curated un-branded candidates** across 21 niches. Result: **29 THIN,
4 GOOD, 1 OK**. The GOOD ones were *all* golf/travel apparel (Libin/Pudolla golf
pants, baleaf travel pants). Every generic gadget (meat thermometer, air-fryer
liner, MagSafe mount, LED strip, jelly bra, headlamp) was THIN at 3×.

**Interpretation:** "winning product" (high reviews) ≠ "winning dropship play."
The edge is in margin + intent + premium-justification, not in finding hot items.

### The high-ticket flip
Running `--mode high-ticket` on lighting/home-goods shows the honest split:

| Product | 5× retail | Verdict |
|---|---|---|
| Floor lamp (SUNMORY) | $85.45 | HIGH-TICKET ✓ **PREMIUM 1.94× market** (defensible) |
| Table lamp set | $52.35 | HIGH-TICKET ✓ AGGRESSIVE 2.09× market |
| Floor lamp (generic) | $91.60 | HIGH-TICKET ✓ AGGRESSIVE 3.06× market |
| Pendant light / chandelier | $80–83 | HIGH-TICKET ✓ (clears floor) |
| Desk lamp / cordless table lamp | $41–43 | LOW-TICKET (5× < $49.99) |
| Ceiling fan | $251 | OVER-PRICED (> $250 ceiling) |

**Floor lamps are the sweet spot** — source $10–18, 5× = $80–90, and the market
price ($44–47) is close enough that a premium listing is *defensible* rather
than absurd.

### Niche verdicts (across the whole sweep)
- **Strong:** golf/travel apparel (identity markup), lighting fixtures (high-ticket).
- **Viable home-goods layer:** floor lamps, pendant lights, wall sconces, table
  lamps, vanities, organizers — light enough to ship, high-ticket enough to work.
- **Avoid (brand moat):** bedding (Bedsure/Utopia/Mellanni own it), beauty/health
  consumables, pets, appliances.
- **Freight wall:** mattresses, sofas, dressers, ceiling fans (heavy), bed frames.

---

## 4. Decision framework

1. **Pick a model first** — Model A (TikTok 3×, golf apparel) or Model B (Google
   high-ticket, lighting/home-goods). Don't mix their economics.
2. **Find** candidates (`find_products.py`) in the matching category.
3. **Intent-check** (`search_intent.py`) — is demand RISING/SEASONAL, or dying?
4. **Price** (`price_products.py`):
   - Model A → `--mode classic`, want **GOOD**.
   - Model B → `--mode high-ticket`, want **HIGH-TICKET ✓ PREMIUM 1–2×** (or
     UNDERCUT); treat **AGGRESSIVE >2×** as "only if you'll genuinely build a
     brand with premium images."
5. **Saturation/angle check** (still manual) — how many stores already run it,
   and what's your differentiation (angle / bundle / creative / brand)?

---

## 5. Next steps (suggested)

1. **Run the full high-ticket pipeline on lighting** and produce a shortlist of
   floor lamps / pendants / wall sconces with `HIGH-TICKET ✓ PREMIUM 1–2×`.
2. **Add a saturation signal** — the one check the scripts still can't do
   (count competing stores / Google Shopping listings for a product). This is
   the remaining gap in the funnel.
3. **Add Google Trends "rising" as a finder signal** — currently `search_intent.py`
   is a separate enrichment step; consider folding RISING + SEASONAL into the
   finder's score for a "rising-product" mode.
4. **Build the "store" side** — the video's 5-prompt Claude + Shopify workflow
   (theme clone → bulk import → AI images → SEO titles → product pages) is the
   natural next layer after product selection. Tools referenced: Claude co-work
   + Shopify connector, Higgsfield (MCP for AI images), themesbot.com,
   Copy/Poki (bulk import), Google Performance Max.
5. **Validate on Google Shopping before scaling** — the $3.7M / $24M figures in
   the video are top-end outliers; treat the method as real but the numbers as
   survivorship bias.

---

## 6. Repo / data layout

- `find_products.py`, `search_intent.py`, `price_products.py` — the pipeline.
- `/root/research/` (dev machine) — research artifacts:
  - `niche-sweep-margin-2026-09-25.md` — the 21-niche sweep + margin findings.
  - `romas-transcript.txt` — full transcript of the Romas Ecom method video.
  - `fixtures-high-ticket.md` — the lighting high-ticket run.

The dev copies of the scripts live in `/root/hermes-workspace/tools/`; the
canonical repo is `git@github.com:jackthatch/shopify-scripts.git` (clone at
`/root/hermes-workspace/shopify-scripts`). **Copy updated scripts into the clone
before committing** (the two directories can drift).
