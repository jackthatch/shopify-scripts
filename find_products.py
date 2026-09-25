#!/usr/bin/env python3
"""
find_products.py — AI-assisted dropshipping product finder.

Pulls real, current Amazon Best Sellers data (rank, title, ASIN, price, rating,
review count) across categories via the r.jina.ai reader proxy, then applies
dropshipping filters to surface candidate products worth investigating:

  * Excludes major brand-owned products (not dropshippable / trademark risk)
  * Price sweet-spot band (default $10–$50 retail)
  * Proven demand (high review count) with a rating floor
  * Scores generic/manufacturer products (keyword-stuffed titles, no strong brand)

Output: a ranked Markdown table + JSON. Designed to be re-run on demand or by cron.

Usage:
  python3 find_products.py                 # all default categories, top 15 each
  python3 find_products.py --categories pet-supplies,beauty,kitchen
  python3 find_products.py --min-price 15 --max-price 45 --min-reviews 500
  python3 find_products.py --top 30 --json
"""

import argparse
import json
import re
import subprocess
import sys
import time

JINA = "https://r.jina.ai/"
MIN_OK_BYTES = 2000  # r.jina.ai rate-limit/error pages are tiny

# Category slug -> Amazon Best Sellers URL suffix. Only dropshipping-relevant
# physical-product categories (skip digital, gift cards, books, coins, etc.)
CATEGORIES = {
    "kitchen": "Best-Sellers-Kitchen-Dining/zgbs/kitchen",
    "home": "Best-Sellers-Home-Kitchen/zgbs/home-garden",
    "beauty": "Best-Sellers-Beauty-Personal-Care/zgbs/beauty",
    "health": "Best-Sellers-Health-Household/zgbs/hpc",
    "pets": "Best-Sellers-Pet-Supplies/zgbs/pet-supplies",
    "sports": "Best-Sellers-Sports-Outdoors/zgbs/sporting-goods",
    "toys": "Best-Sellers-Toys-Games/zgbs/toys-and-games",
    "tools": "Best-Sellers-Tools-Home-Improvement/zgbs/hi",
    "baby": "Best-Sellers-Baby/zgbs/baby-products",
    "office": "Best-Sellers-Office-Products/zgbs/office-products",
    "auto": "Best-Sellers-Automotive/zgbs/automotive",
    "crafts": "Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts",
    "patio": "Best-Sellers-Patio-Lawn-Garden/zgbs/lawn-garden",
    "grocery": "Best-Sellers-Grocery-Gourmet-Food/zgbs/grocery",
    "fashion": "Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion",
    "appliances": "Best-Sellers-Appliances/zgbs/appliances",
    "golf": "Best-Sellers-Sports-Outdoors-Golf/zgbs/sporting-goods/3410851",
    "furniture": "Best-Sellers-Home-Kitchen-Furniture/zgbs/home-garden/1063306",
    "bedding": "Best-Sellers-Home-Kitchen-Bedding/zgbs/home-garden/1063252",
    "sheets": "Best-Sellers-Home-Kitchen-Sheets-Pillowcases/zgbs/home-garden/1063274",
    "blankets": "Best-Sellers-Home-Kitchen-Blankets-Throws/zgbs/home-garden/1063280",
    "comforters": "Best-Sellers-Home-Kitchen-Bedding-Comforters-Sets/zgbs/home-garden/2224405011",
    "duvet": "Best-Sellers-Home-Kitchen-Bedding-Duvet-Covers-Sets/zgbs/home-garden/21404094011",
}

# Major brand-owned names. Products from these brands can't be dropshipped
# profitably (trademark + sold direct), so we exclude or down-rank them.
MAJOR_BRANDS = {
    "yeti", "stanley", "ninja", "kitchenaid", "rubbermaid", "reynolds",
    "owala", "hydrojug", "hydro flask", "amazon basics", "amazonbasics",
    "cuisinart", "instant pot", "le creuset", "oxo", "pyrex", "t-fal",
    "tramontina", "ninja", "breville", "keurig", "nespresso", "dyson",
    "philips", "braun", "oral-b", "crest", "colgate", "gillette", "dove",
    "maybelline", "l'oreal", "neutrogena", "cerave", "cetaphil", "olay",
    "nike", "adidas", "under armour", "puma", "the north face", "patagonia",
    "coleman", "clorox", "lysol", "glad", "ziploc", "swiffer", "scotch-brite",
    "bounty", "charmin", "cascade", "tide", "downy", "snuggle", "bounce",
    "mr. clean", "febreze", "purina", "pedigree", "blue buffalo", "hill's",
    "royal canin", "merrick", "wellness", "frisco", "kong", "chuckit",
    "samsung", "apple", "sony", "lg", "bose", "jbl", "anker", "belkin",
    "otterbox", "spigen", "logitech", "microsoft", "fisher-price", "lego",
    "hasbro", "mattel", "nerf", "play-doh", "melissa & doug", "vtech",
    "crayola", "sharpie", "bic", "post-it", "3m", "dewalt", "milwaukee",
    "makita", "bosch", "ryobi", "craftsman", "kobalt", "irwin", "klein",
    "pampers", "huggies", "johnson's", "aveeno", "gerber", "graco", "chicco",
    # golf brands
    "callaway", "taylormade", "titleist", "ping", "cobra", "wilson", "mizuno",
    "srixon", "bridgestone", "footjoy", "under armour", "flexfit", "wrx", "odyssey",
    # bedding brands
    "mellanni", "bedsure", "utopia", "cgk", "danjor", "elegant comfort",
    "cosy house", "comfytemp", "bare home", "boll & branch", "brooklinen",
    "parachute", "casper", "purple", "brookstone", "tempur", "sijo", "quince",
    "linen & plaid", "nestl", "nectar", "lane linen", "hippie dee",
    "bedelite", "cozylux", "moomee", "bare home", "jollyvogue", "evergracehome",
    "love's cabin", "geniani", "yescool", "california design den", "bestouch",
    "mildly", "nexhome",
}

BRAND_RE = re.compile(
    r"^(?:" + "|".join(re.escape(b) for b in sorted(MAJOR_BRANDS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)

# Consumables / liquids / heavy / regulated items are poor dropship candidates
# (shipping weight, FDA/OTC rules, brand-trust required, thin margins on
# replenishment goods). Down-rank (not hard-exclude) so the operator can judge.
CONSUMABLE_HINTS = (
    "litter", "cat food", "dog food", "wet cat", "dry cat", "wet dog", "dry dog",
    "treat", "biscuit", "jerky", "chew", "kabob", "squeeze", "purée", "puree",
    "shampoo", "conditioner", "lotion", "moisturiz", "cream", "serum", "toner",
    "supplement", "probiotic", "vitamin", "deodorant", "soap", "wash", "cleanse",
    "mascara", "eyeliner", "lip liner", "swab", "cotton round", "antiperspirant",
    "wipes", "pee pad", "potty", "scent", "odor eliminator", "enzyme",
    "mrs. meyer", "refill", "detergent", "dishwasher",
    # bulky furniture / freight-shipping items
    "mattress", "bed frame", "topper", "sofa", "couch", "recliner", "dresser",
    "armoire", "wardrobe", "futon", "bunk bed", "loft bed", "headboard",
    "nightstand", "bookshelf", "bookcase", "tv stand", "coffee table",
)


def _consumable(title: str) -> bool:
    t = title.lower()
    return any(h in t for h in CONSUMABLE_HINTS)


def fetch(url: str, timeout: int = 40, retries: int = 4) -> str:
    """Fetch a URL through the r.jina.ai reader proxy (with retry/backoff)."""
    last = ""
    for attempt in range(retries):
        cmd = [
            "curl", "-s", "-m", str(timeout), "-A", "Mozilla/5.0",
            JINA + url,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 10)
        if r.returncode == 0 and len(r.stdout) >= MIN_OK_BYTES:
            return r.stdout
        last = f"rc={r.returncode} len={len(r.stdout)}"
        time.sleep(3 * (attempt + 1))  # backoff: 3s, 6s, 9s
    raise RuntimeError(f"fetch failed after {retries} attempts ({last})")


def parse_best_sellers(md: str) -> list[dict]:
    """Parse r.jina.ai Markdown of an Amazon Best Sellers page into product dicts."""
    products = []
    for line in md.splitlines():
        asins = re.findall(r"/dp/([A-Z0-9]{10})", line)
        if not asins:
            continue
        rating_m = re.search(r"_(\d\.\d) out of 5 stars_ ([\d,]+)", line)
        price_m = re.search(r"\$(\d+(?:\.\d+)?)", line)
        rank_m = re.search(r"#(\d{1,3})", line)
        # Title: the markdown link whose URL contains /dp/ASIN — take link text.
        title = ""
        for m in re.finditer(r"\[([^\]]+)\]\((https://www\.amazon\.com/[^)]*?/dp/[A-Z0-9]{10}[^)]*)\)", line):
            text = m.group(1).strip()
            if text and not text.startswith("_") and not text.startswith("$") and len(text) > 5:
                title = text
                break
        if not title:
            # fallback: image alt text
            alt = re.search(r"!\[Image \d+: ([^\]]+)\]", line)
            title = alt.group(1) if alt else ""

        products.append({
            "asin": asins[0],
            "title": title.strip(),
            "rank": int(rank_m.group(1)) if rank_m else None,
            "rating": float(rating_m.group(1)) if rating_m else None,
            "reviews": int(rating_m.group(2).replace(",", "")) if rating_m else None,
            "price": float(price_m.group(1)) if price_m else None,
        })
    return products


def score(p: dict, args) -> tuple[float, str]:
    """Score a product for dropshipping attractiveness. Returns (score, reason)."""
    reasons = []
    score = 0.0

    if not p["price"] or not p["reviews"] or not p["rating"]:
        return -1.0, "missing data (skip)"

    # Price band
    if args.min_price <= p["price"] <= args.max_price:
        score += 3
    elif p["price"] < args.min_price:
        reasons.append(f"price too low (${p['price']})")
        score -= 1
    else:
        reasons.append(f"price too high (${p['price']})")
        score -= 1

    # Rating floor
    if p["rating"] >= args.min_rating:
        score += 2
    else:
        reasons.append(f"rating {p['rating']} < {args.min_rating}")
        score -= 3

    # Demand proof (review count)
    if p["reviews"] >= args.min_reviews:
        score += 3
    else:
        reasons.append(f"only {p['reviews']} reviews")
        score -= 1

    # Brand detection
    if BRAND_RE.match(p["title"]):
        reasons.append("major brand (dropship risk)")
        score -= 4
    else:
        score += 2

    # Consumable / heavy / regulated
    if _consumable(p["title"]):
        reasons.append("consumable/heavy (poor dropship)")
        score -= 3

    # Lightweight / small-item heuristic (shipping-friendly keywords)
    light_hints = ("scale", "thermometer", "sprayer", "liner", "bag", "holder",
                   "organizer", "brush", "sponge", "clip", "mold", "mat", "wrap",
                   "dispenser", "cutter", "slicer", "scoop", "strainer", "whisk",
                   "scraper", "tray", "bottle", "jar", "silicone", "straw", "cover",
                   "lid", "strap", "case", "light", "lamp", "brush", "comb")
    if any(h in p["title"].lower() for h in light_hints):
        score += 1

    return score, "; ".join(reasons) if reasons else "clean"


def main():
    ap = argparse.ArgumentParser(description="AI dropshipping product finder")
    ap.add_argument("--categories", default=",".join(CATEGORIES.keys()),
                    help="comma-separated category slugs (default: all)")
    ap.add_argument("--top", type=int, default=15, help="products to keep per category (default 15)")
    ap.add_argument("--min-price", type=float, default=8.0)
    ap.add_argument("--max-price", type=float, default=50.0)
    ap.add_argument("--min-rating", type=float, default=4.0)
    ap.add_argument("--min-reviews", type=int, default=500)
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    ap.add_argument("--out", default="", help="write output to file")
    args = ap.parse_args()

    cats = [c.strip() for c in args.categories.split(",") if c.strip()]
    unknown = [c for c in cats if c not in CATEGORIES]
    if unknown:
        print(f"Unknown categories: {unknown}\nValid: {', '.join(CATEGORIES)}", file=sys.stderr)
        sys.exit(1)

    all_results = []
    for i, cat in enumerate(cats):
        if i > 0:
            time.sleep(2)  # throttle between categories to avoid proxy rate-limit
        url = "https://www.amazon.com/" + CATEGORIES[cat]
        try:
            md = fetch(url)
        except Exception as e:
            print(f"[warn] {cat}: fetch failed ({e})", file=sys.stderr)
            continue
        prods = parse_best_sellers(md)
        for p in prods:
            p["category"] = cat
            p["score"], p["reason"] = score(p, args)
        # keep only data-complete, non-skipped items
        prods = [p for p in prods if p["score"] >= 0 and p["price"] and p["reviews"]]
        prods.sort(key=lambda x: (-x["score"], x["rank"] if x["rank"] else 999))
        all_results.extend(prods[:args.top])

    all_results.sort(key=lambda x: -x["score"])

    if args.json:
        out = json.dumps(all_results, indent=2)
    else:
        lines = []
        lines.append("# Dropshipping Product Candidates")
        lines.append("")
        lines.append("Sourced from Amazon Best Sellers (live) — filtered for generic, "
                     "price-sweet-spot, proven-demand products. Score = dropship attractiveness.")
        lines.append("")
        lines.append("| Score | Rank | Category | Product | Price | Rating | Reviews | Why |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for p in all_results:
            title = p["title"][:60]
            lines.append(
                f"| {p['score']:.0f} | {p['rank'] or '-'} | {p['category']} | "
                f"{title} | ${p['price']:.2f} | {p['rating']} | {p['reviews']:,} | {p['reason'] or ''} |"
            )
        out = "\n".join(lines)

    if args.out:
        with open(args.out, "w") as f:
            f.write(out + "\n")
        print(f"Wrote {len(all_results)} products to {args.out}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
