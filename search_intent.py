#!/usr/bin/env python3
"""
search_intent.py — the search-intent signal layer for dropshipping candidates.

Enriches find_products.py output (or a raw keyword list) with two free, no-auth
signals that measure *what people are actually searching for with intent*:

  1. Google Autocomplete — the real long-tail queries people type. High signal
     for search intent AND a ready-made keyword list for SEO titles/descriptions.
  2. Google Trends (pytrends interest_over_time) — 12-month search-interest
     trend, classified RISING / STABLE / DECLINING / SEASONAL.

Why this matters: on Google Shopping the buyer is already searching with intent
("outdoor wall light", wallet out). The products that win are the ones with
active, growing, in-season search demand — NOT impulse gadgets. This is the
"search intent" layer from the Google-Shopping / high-ticket playbook.

Usage:
  python3 search_intent.py --from-json candidates.json --limit 20
  python3 search_intent.py --keywords "outdoor wall light,doormat,placemat"
  python3 search_intent.py --from-json candidates.json --skip-trends   # autocomplete only
  python3 search_intent.py --keywords "..." --json --out enriched.json

Pipeline position: find_products.py (discovery) -> search_intent.py (intent)
-> price_products.py (margin / high-ticket).
"""

import argparse
import json
import re
import subprocess
import sys
import time

# ---------------------------------------------------------------------------
# Google Autocomplete — suggestqueries.google.com (free, no auth)
# ---------------------------------------------------------------------------

def autocomplete(keyword: str, client: str = "firefox") -> list[str]:
    """Return the long-tail completion queries for a keyword (search intent)."""
    url = "https://suggestqueries.google.com/complete/search"
    cmd = ["curl", "-s", "-m", "20", "-A", "Mozilla/5.0",
           f"{url}?client={client}&hl=en&q=" + keyword.replace(" ", "%20")]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if r.returncode != 0 or not r.stdout:
        return []
    # response is JSONP: ["kw",[sugg1,sugg2,...],...]
    m = re.search(r'\[.*?\[(.*?)\]', r.stdout, re.DOTALL)
    if not m:
        return []
    try:
        return json.loads("[" + m.group(1) + "]")
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Google Trends via pytrends — interest_over_time (works; trending_searches is broken)
# ---------------------------------------------------------------------------

def _trend(keyword: str, timeout: tuple = (10, 25)) -> dict | None:
    """Return 12-month interest-over-time for a keyword as a trend dict, or None."""
    try:
        from pytrends.request import TrendReq
    except ImportError:
        return {"error": "pytrends not installed (pip install pytrends)"}
    try:
        pt = TrendReq(hl="en-US", tz=-60, timeout=timeout)
        pt.build_payload([keyword], timeframe="today 12-m")
        df = pt.interest_over_time()
    except Exception as e:
        return {"error": f"pytrends failed: {type(e).__name__}"}
    if df is None or df.empty:
        return {"error": "no trend data"}
    # drop the isPartial helper column
    vals = df[[c for c in df.columns if c != "isPartial"]]
    series = vals.iloc[:, 0]
    non_partial = series[df["isPartial"] == False]  # noqa: E712
    if non_partial.empty:
        return {"error": "all partial data"}
    first = float(non_partial.iloc[:2].mean())
    last = float(non_partial.iloc[-2:].mean())
    peak = float(series.max())
    if first == 0:
        direction = "RISING" if last > 0 else "NONE"
    else:
        ratio = last / first
        if ratio >= 1.3:
            direction = "RISING"
        elif ratio <= 0.7:
            direction = "DECLINING"
        else:
            direction = "STABLE"
    # seasonality: peak is >1.6x the median -> spiky (seasonal) signal
    med = float(series.median())
    seasonal = "SEASONAL" if med > 0 and peak / med >= 1.6 else "STEADY"
    return {
        "direction": direction,
        "shape": seasonal,
        "first_avg": round(first, 1),
        "last_avg": round(last, 1),
        "peak": round(peak, 1),
        "current_interest": round(last, 1),
        "months": int(len(non_partial)),
    }


def _keyword_from_title(title: str) -> str:
    """Extract a short search keyword from a keyword-stuffed Amazon title."""
    t = re.split(r"[,|]", title)[0].strip()
    words = t.split()
    common = {"the", "a", "an", "for", "with", "and", "of", "men", "women",
              "mens", "womens", "golf", "kids", "baby", "kitchen", "home",
              "heavy", "duty"}
    if words and words[0][0].isupper() and words[0].lower() not in common and len(words) > 2:
        words = words[1:]
    kept = [w for w in words if not re.fullmatch(r"[\d./\"x-]+", w)]
    return " ".join(kept[:4]).strip()


def enrich(keyword: str, do_trends: bool) -> dict:
    """Return autocomplete + trend enrichment for a single keyword."""
    out = {"keyword": keyword}

    suggs = autocomplete(keyword)
    out["suggestions"] = suggs
    out["suggestion_count"] = len(suggs)
    # strip the leading echo (autocomplete repeats the query first) to get
    # the *distinct* intent queries for keyword expansion
    distinct = [s for s in suggs if s.lower() != keyword.lower()]
    out["intent_queries"] = distinct[:8]

    if do_trends:
        t = _trend(keyword)
        out["trend"] = t
    else:
        out["trend"] = {"skipped": True}

    # a simple "intent score": suggestion volume is a weak proxy for active search
    n = len(distinct)
    if n >= 8:
        out["intent"] = "HIGH"
    elif n >= 4:
        out["intent"] = "MEDIUM"
    elif n >= 1:
        out["intent"] = "LOW"
    else:
        out["intent"] = "NONE"
    return out


def main():
    ap = argparse.ArgumentParser(description="Search-intent signal layer for dropship candidates")
    ap.add_argument("--from-json", default="", help="JSON from find_products.py")
    ap.add_argument("--keywords", default="", help="comma-separated keywords")
    ap.add_argument("--limit", type=int, default=0, help="only enrich top N from JSON")
    ap.add_argument("--skip-trends", action="store_true", help="autocomplete only (no pytrends)")
    ap.add_argument("--throttle", type=float, default=2.0, help="seconds between items (default 2)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    items = []
    if args.from_json:
        with open(args.from_json) as f:
            data = json.load(f)
        for p in data:
            items.append(_keyword_from_title(p.get("title", "")))
    elif args.keywords:
        items = [k.strip() for k in args.keywords.split(",") if k.strip()]
    else:
        print("Provide --from-json or --keywords", file=sys.stderr)
        sys.exit(1)

    # de-dupe, keep order
    seen = set()
    items = [k for k in items if k and not (k in seen or seen.add(k))]
    if args.limit:
        items = items[: args.limit]

    rows = []
    for i, kw in enumerate(items):
        if i > 0:
            time.sleep(args.throttle)
        try:
            rows.append(enrich(kw, not args.skip_trends))
        except Exception as e:
            rows.append({"keyword": kw, "error": str(e)})
        print(f"[ok] {kw}: intent={rows[-1].get('intent')} "
              f"sugg={rows[-1].get('suggestion_count', 0)} "
              f"trend={rows[-1].get('trend', {}).get('direction', '-')}",
              file=sys.stderr)

    # order: RISING first, then HIGH intent
    def sort_key(r):
        d = r.get("trend", {}).get("direction", "")
        rank = {"RISING": 0, "STABLE": 1, "DECLINING": 2, "NONE": 3}.get(d, 4)
        return (rank, -r.get("suggestion_count", 0))
    rows.sort(key=sort_key)

    if args.json:
        out = json.dumps(rows, indent=2)
    else:
        lines = ["# Search-Intent Analysis", "",
                 "Google Autocomplete (long-tail intent queries) + Google Trends (12-mo direction).",
                 "Intent = active search demand; RISING = growing; SEASONAL = spikey demand.", ""]
        lines.append("| Keyword | Intent | Suggs | Trend | Shape | Top intent queries |")
        lines.append("|---|---|---|---|---|---|")
        for r in rows:
            t = r.get("trend", {})
            d = t.get("direction", "—")
            shp = t.get("shape", "—")
            q = "; ".join(r.get("intent_queries", [])[:3])[:60]
            lines.append(f"| {r['keyword'][:30]} | {r.get('intent','—')} | "
                         f"{r.get('suggestion_count',0)} | {d} | {shp} | {q} |")
        out = "\n".join(lines)

    if args.out:
        with open(args.out, "w") as f:
            f.write(out + "\n")
        print(f"Wrote {len(rows)} rows to {args.out}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
