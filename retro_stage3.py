#!/usr/bin/env python3
"""Stage 3: drop the Size option by supplying variant data (Shopify requires it)."""
import os, json, urllib.request, urllib.error, time

HERE = os.path.dirname(os.path.abspath(__file__))
creds = {}
for line in open(os.path.join(HERE, ".env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); creds[k.strip()] = v.strip()
STORE, TOKEN = creds["SHOPIFY_STORE"], creds["SHOPIFY_TOKEN"]
PID = "15197432971505"

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
        return e.code, e.read().decode()[:600]

st, prod = api("GET", f"products/{PID}.json"); prod = prod["product"]
json.dump(prod, open("/root/research/product-refresh/15197432971505/20260927-retro-glass-chandelier/BACKUP-before-option-removal.json","w"), indent=2)

codes = []
variants_payload = []
for v in prod["variants"]:
    code = v["title"].split(" / ")[0].strip()
    codes.append(code)
    variants_payload.append({"id": v["id"], "option1": code, "price": v["price"]})

payload = {"product": {
    "id": int(PID),
    "options": [{"name": "Body Color", "values": codes}],
    "variants": variants_payload,
}}
st, res = api("PUT", f"products/{PID}.json", payload)
print("PUT ->", st)
if st != 200: print("   error:", res)

time.sleep(3)
st, prod = api("GET", f"products/{PID}.json"); prod = prod["product"]
print("\noptions now:", [(o["name"], o["values"]) for o in prod["options"]])
print("variants:", len(prod["variants"]))
print("titles:", sorted(v["title"] for v in prod["variants"]))
print("prices:", {v["price"] for v in prod["variants"]})
json.dump(prod, open("/root/research/product-refresh/15197432971505/20260927-retro-glass-chandelier/AFTER-option-removal.json","w"), indent=2)