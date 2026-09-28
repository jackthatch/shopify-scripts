#!/usr/bin/env python3
"""Stage 1: backup product, remove 220V variants, drop the Size option, set $59.99."""
import os, json, urllib.request, urllib.error, time

HERE = os.path.dirname(os.path.abspath(__file__))
creds = {}
for line in open(os.path.join(HERE, ".env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); creds[k.strip()] = v.strip()
STORE, TOKEN = creds["SHOPIFY_STORE"], creds["SHOPIFY_TOKEN"]
PID = "15197432971505"
RUN = "/root/research/product-refresh/15197432971505/20260927-retro-glass-chandelier"

def api(method, path, payload=None):
    url = f"https://{STORE}/admin/api/2024-10/{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("X-Shopify-Access-Token", TOKEN)
    r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=90) as resp:
            body = resp.read().decode()
            return resp.status, json.loads(body) if body.strip() else {}
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]

# ---- backup ----
st, prod = api("GET", f"products/{PID}.json")
prod = prod["product"]
json.dump(prod, open(f"{RUN}/BACKUP-before-upload.json", "w"), indent=2)
print("backup written |", st, "| variants:", len(prod["variants"]), "| images:", len(prod["images"]))
print("options:", [(o["name"], o["values"]) for o in prod["options"]])

# ---- delete the 220V variants ----
v220 = [v for v in prod["variants"] if v["title"].endswith("/ 220V") or "220V" in v["title"]]
print(f"\n220V variants to delete: {len(v220)}")
deleted = []
for v in v220:
    st, _ = api("DELETE", f"products/{PID}/variants/{v['id']}.json")
    print(f"  delete {v['title']:16} id={v['id']} -> HTTP {st}")
    deleted.append(v["id"])
    if st != 200: print("     !! unexpected:", _)
    time.sleep(0.4)

# ---- re-read ----
st, prod2 = api("GET", f"products/{PID}.json"); prod2 = prod2["product"]
print(f"\nafter delete: variants={len(prod2['variants'])}")
print("options:", [(o["name"], o["values"]) for o in prod2["options"]])
json.dump(prod2, open(f"{RUN}/AFTER-variant-delete.json", "w"), indent=2)