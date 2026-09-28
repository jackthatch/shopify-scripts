#!/usr/bin/env python3
"""Stage 2: drop the single-value Size option, set every variant to $59.99."""
import os, json, urllib.request, urllib.error, time

HERE = os.path.dirname(os.path.abspath(__file__))
creds = {}
for line in open(os.path.join(HERE, ".env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); creds[k.strip()] = v.strip()
STORE, TOKEN = creds["SHOPIFY_STORE"], creds["SHOPIFY_TOKEN"]
PID = "15197432971505"
PRICE = "59.99"

def api(method, path, payload=None):
    url = f"https://{STORE}/admin/api/2024-10/{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("X-Shopify-Access-Token", TOKEN)
    r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=90) as resp:
            b = resp.read().decode()
            return resp.status, json.loads(b) if b.strip() else {}
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500]

st, prod = api("GET", f"products/{PID}.json"); prod = prod["product"]
body_vals = next(o["values"] for o in prod["options"] if o["name"] == "Body Color")

# --- 1. remove the Size option ---
print("attempting to remove Size option...")
st, res = api("PUT", f"products/{PID}.json",
              {"product": {"id": int(PID), "options": [{"name": "Body Color", "values": body_vals}]}})
print("  PUT options ->", st, "" if st == 200 else str(res)[:300])

time.sleep(2)
st, prod = api("GET", f"products/{PID}.json"); prod = prod["product"]
print("  options now:", [(o["name"], o["values"]) for o in prod["options"]])
print("  variants:", len(prod["variants"]))
if prod["variants"]:
    print("  sample titles:", [v["title"] for v in prod["variants"]][:4])

# --- 2. price -> 59.99 ---
print(f"\nsetting price {PRICE} on all variants...")
for v in prod["variants"]:
    st, res = api("PUT", f"variants/{v['id']}.json",
                  {"variant": {"id": v["id"], "price": PRICE}})
    print(f"  {v['title']:14} {v['price']:>8} -> HTTP {st}" + ("" if st == 200 else f"  {str(res)[:150]}"))
    time.sleep(0.35)

time.sleep(2)
st, prod = api("GET", f"products/{PID}.json"); prod = prod["product"]
prices = {v["price"] for v in prod["variants"]}
print("\nfinal distinct prices:", prices, "| variants:", len(prod["variants"]))
json.dump(prod, open("/root/research/product-refresh/15197432971505/20260927-retro-glass-chandelier/AFTER-price.json", "w"), indent=2)
print("variant map (code -> id):")
for v in sorted(prod["variants"], key=lambda x: x["title"]):
    print(f"   {v['title']:8} id={v['id']}  ${v['price']}  sku={v.get('sku')}")