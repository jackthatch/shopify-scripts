#!/usr/bin/env python3
"""
price_products.py — pricing & margin engine for dropshipping candidates.

For each product, searches AliExpress for the real source (landed) cost, then
computes the pricing/margin picture: suggested retail at a target markup, gross
margin, break-even ROAS, and a go/no-go verdict against the market price.

Usage:
  python3 price_products.py --products "golf umbrella,tv wall mount"
  python3 price_products.py --products "golf umbrella" --markup 3.0
  python3 price_products.py --from-json candidates.json   # merge with finder output
"""

import argparse
import json
import re
import subprocess
import sys
import time

JINA = "https://r.jina.ai/"
MIN_OK_BYTES = 2000


def fetch(url: str, timeout: int = 40, retries: int = 4) -> str:
    last = ""
    for attempt in range(retries):
        cmd = ["curl", "-s", "-m", str(timeout), "-A", "Mozilla/5.0", JINA + url]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 10)
        if r.returncode == 0 and len(r.stdout) >= MIN_OK_BYTES:
            return r.stdout
        last = f"rc={r.returncode} len={len(r.stdout)}"
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"fetch failed ({last})")


def search_aliexpress(keyword: str) -> list[dict]:
    """Search AliExpress and return a list of {title, price, orig, sold} results."""
    slug = re.sub(r"[^a-z0-9]+", "-", keyword.lower()).strip("-")
    url = f"https://www.aliexpress.com/w/wholesale-{slug}.html"
    md = fetch(url)
    results = []
    for line in md.splitlines():
        m = re.search(r"###\s+(.+?)\s+\$([\d.]+)", line)
        if not m:
            continue
        title = m.group(1).strip()
        price = float(m.group(2))
        orig_m = re.search(r"\$([\d.]+)\s+-\d+%", line)
        orig = float(orig_m.group(1)) if orig_m else price
        sold_m = re.search(r"([\d,]+)\s*\+\s*sold|([\d,]+)\s+sold", line)
        sold = sold_m.group(1) or sold_m.group(2) if sold_m else None
        sold = int(sold.replace(",", "")) if sold else None
        free_ship = "free shipping" in line.lower()
        results.append({
            "title": title, "price": price, "orig": orig,
            "sold": sold, "free_shipping": free_ship,
        })
    # sort by price ascending (cheapest landed cost first)
    results.sort(key=lambda r: r["price"])
    return results


def price_analysis(keyword, results, markup, fee, shipping, market_price=None):
    """Compute margin/pricing from AliExpress results."""
    if not results:
        return None
    # take the cheapest 5 as the realistic source range; drop bait "from $2" prices
    top = [r for r in results[:10] if r["price"] >= 2.0]
    if not top:
        top = results[:5]
    top = top[:5]
    cheapest = top[0]
    prices = sorted(r["price"] for r in top)
    lo, hi = prices[0], prices[-1]
    median = sorted(prices)[len(prices) // 2]

    landed = median + shipping  # conservative: median source + shipping buffer
    suggested = landed * markup
    gross_margin = (suggested - landed - fee * suggested) / suggested if suggested else 0
    break_even = 1 / gross_margin if gross_margin > 0 else float("inf")

    verdict = ""
    if market_price:
        if landed * markup <= market_price:
            verdict = "GOOD — 3x price under market"
        elif landed * markup <= market_price * 1.2:
            verdict = "OK — 3x price ~= market"
        else:
            verdict = "THIN — source too close to market"
    else:
        verdict = "GOOD" if gross_margin >= 0.5 else "THIN"

    return {
        "keyword": keyword,
        "source_lo": lo,
        "source_hi": hi,
        "source_median": median,
        "landed": round(landed, 2),
        "suggested_retail": round(suggested, 2),
        "gross_margin": round(gross_margin * 100, 1),
        "break_even_roas": round(break_even, 2),
        "market_price": market_price,
        "verdict": verdict,
        "top_source": cheapest["title"][:50],
        "top_source_sold": cheapest["sold"],
    }


def _keyword_from_title(title: str) -> str:
    """Extract a short, clean AliExpress search keyword from a keyword-stuffed
    Amazon title. Cuts at first comma/pipe, drops a leading brand token."""
    t = re.split(r"[,|]", title)[0].strip()
    words = t.split()
    # drop a leading brand-ish token (single capitalized word, not a common word)
    common = {"the", "a", "an", "for", "with", "and", "of", "men", "women", "mens",
              "womens", "golf", "kids", "baby", "kitchen", "home", "heavy", "duty"}
    if words and words[0][0].isupper() and words[0].lower() not in common and len(words) > 2:
        words = words[1:]
    # keep up to 4 words, drop pure-number/size tokens
    kept = [w for w in words if not re.fullmatch(r"[\d./\"x-]+", w)]
    return " ".join(kept[:4]).strip()


def main():
    ap = argparse.ArgumentParser(description="Dropship pricing & margin engine")
    ap.add_argument("--products", default="", help="comma-separated product keywords")
    ap.add_argument("--from-json", default="", help="JSON from find_products.py (merge Amazon price)")
    ap.add_argument("--limit", type=int, default=0, help="only price top N items from JSON (0 = all)")
    ap.add_argument("--markup", type=float, default=3.0, help="target retail markup (default 3x)")
    ap.add_argument("--fee", type=float, default=0.03, help="payment fee as decimal (default 0.03)")
    ap.add_argument("--shipping", type=float, default=3.0, help="per-item shipping buffer $ (default 3)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    items = []  # list of {keyword, market_price}
    if args.from_json:
        with open(args.from_json) as f:
            data = json.load(f)
        for p in data:
            kw = _keyword_from_title(p.get("title", ""))
            items.append({"keyword": kw, "market_price": p.get("price")})
        if args.limit:
            items = items[:args.limit]
    else:
        if not args.products:
            print("Provide --products or --from-json", file=sys.stderr)
            sys.exit(1)
        for kw in [k.strip() for k in args.products.split(",") if k.strip()]:
            items.append({"keyword": kw, "market_price": None})

    rows = []
    for i, item in enumerate(items):
        if i > 0:
            time.sleep(2)
        kw = item["keyword"]
        try:
            results = search_aliexpress(kw)
        except Exception as e:
            print(f"[warn] {kw}: {e}", file=sys.stderr)
            continue
        a = price_analysis(kw, results, args.markup, args.fee, args.shipping, item["market_price"])
        if a:
            rows.append(a)
            print(f"[ok] {kw}: source ${a['source_lo']:.2f}–${a['source_hi']:.2f} "
                  f"-> retail ${a['suggested_retail']:.2f} ({a['gross_margin']}% GM, "
                  f"{a['break_even_roas']}x breakeven) {a['verdict']}", file=sys.stderr)
        else:
            print(f"[warn] {kw}: no AliExpress results", file=sys.stderr)

    rows.sort(key=lambda r: -r["gross_margin"])

    if args.json:
        out = json.dumps(rows, indent=2)
    else:
        lines = ["# Pricing & Margin Analysis", "",
                 f"Markup target: {args.markup}x  |  payment fee: {args.fee*100:.0f}%  |  shipping buffer: ${args.shipping}", "",
                 "| Product | Source cost (AliExpress) | Landed | Suggested retail (3x) | Market price | Gross margin | Break-even ROAS | Verdict |",
                 "|---|---|---|---|---|---|---|---|"]
        for r in rows:
            mk = f"${r['market_price']:.2f}" if r["market_price"] else "—"
            lines.append(
                f"| {r['keyword'][:40]} | ${r['source_lo']:.2f}–${r['source_hi']:.2f} | "
                f"${r['landed']:.2f} | ${r['suggested_retail']:.2f} | {mk} | "
                f"{r['gross_margin']}% | {r['break_even_roas']}x | {r['verdict']} |"
            )
        out = "\n".join(lines)

    if args.out:
        with open(args.out, "w") as f:
            f.write(out + "\n")
        print(f"Wrote {len(rows)} rows to {args.out}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
