#!/usr/bin/env python3
"""Launch-readiness gap audit across all products."""
import os, json, urllib.request, urllib.error, re

creds = {}
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); creds[k.strip()] = v.strip()
STORE, TOKEN = creds["SHOPIFY_STORE"], creds["SHOPIFY_TOKEN"]
API = f"https://{STORE}/admin/api/2024-10"

def get(path):
    r = urllib.request.Request(API + path)
    r.add_header("X-Shopify-Access-Token", TOKEN)
    with urllib.request.urlopen(r, timeout=90) as x:
        return json.loads(x.read().decode())

prods = get("/products.json?limit=250")["products"]
cols = get("/custom_collections.json?limit=250").get("custom_collections", [])
scols = get("/smart_collections.json?limit=250").get("smart_collections", [])

print(f"COLLECTIONS: custom={len(cols)} smart={len(scols)}")
for c in cols: print("   [custom]", c["title"], "| handle:", c["handle"])
for c in scols: print("   [smart ]", c["title"], "| handle:", c["handle"])
print()

issues_total = {}
print("=" * 78)
for p in sorted(prods, key=lambda x: x["title"].lower()):
    imgs = p.get("images", [])
    no_alt = [i for i in imgs if not (i.get("alt") or "").strip()]
    body = p.get("body_html") or ""
    has_ae_imgs = "ae-pic" in body or "alicdn" in body or "aliexpress" in body.lower()
    text_only = re.sub(r"<[^>]+>", " ", body).strip()
    variants = p.get("variants", [])
    prices = sorted({float(v["price"]) for v in variants if v.get("price")})
    untracked = [v for v in variants if not v.get("sku")]
    zero_inv = [v for v in variants if (v.get("inventory_quantity") or 0) <= 0 and v.get("inventory_management") == "shopify"]
    seo_t, seo_d = p.get("title") == (p.get("seo") or {}).get("title"), bool((p.get("seo") or {}).get("description"))

    flags = []
    if len(imgs) == 0: flags.append("NO IMAGES")
    elif len(imgs) < 3: flags.append(f"only {len(imgs)} img")
    if no_alt: flags.append(f"{len(no_alt)}/{len(imgs)} missing alt")
    if not text_only: flags.append("NO DESCRIPTION")
    elif len(text_only) < 250: flags.append(f"thin desc ({len(text_only)} ch)")
    if has_ae_imgs: flags.append("has embedded AliExpress imgs")
    if not seo_d: flags.append("no SEO description")
    if zero_inv: flags.append(f"{len(zero_inv)} variants at 0 inv")
    if untracked: flags.append(f"{len(untracked)} no SKU")
    if p.get("status") != "active": flags.append(f"status={p.get('status')}")

    print(f'{p["title"][:66]}')
    print(f'   id={p["id"]}  handle={p.get("handle","")[:52]}')
    print(f'   imgs={len(imgs)}  variants={len(variants)}  price={prices[0] if prices else "?"}'
          f'{"-"+str(prices[-1]) if prices and len(prices)>1 else ""}  status={p.get("status")}')
    print(f'   desc: {len(text_only)} chars text' + ("  (embedded supplier imgs)" if has_ae_imgs else ""))
    if flags:
        print(f'   >> ISSUES: {" | ".join(flags)}')
        for fl in flags:
            issues_total[fl.split("(")[0].strip()] = issues_total.get(fl.split("(")[0].strip(), 0) + 1
    print()

print("=" * 78)
print("ISSUE ROLL-UP:")
for k, v in sorted(issues_total.items(), key=lambda x: -x[1]):
    print(f"   {v:2d} products: {k}")
