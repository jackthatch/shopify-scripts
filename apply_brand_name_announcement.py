#!/usr/bin/env python3
"""Set brand name (shop.name) + announcement bar text on Dwell."""
import os, json, urllib.request, urllib.error, time, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
creds = {}
for line in open(os.path.join(HERE, ".env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); creds[k.strip()] = v.strip()
STORE, TOKEN = creds["SHOPIFY_STORE"], creds["SHOPIFY_TOKEN"]
API = f"https://{STORE}/admin/api/2024-10"
TID = 186677690609

def req(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(API + path, data=data, method=method)
    r.add_header("X-Shopify-Access-Token", TOKEN)
    r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=90) as x:
            return x.status, x.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")[:700]

# ================= 1. ANNOUNCEMENT BAR =================
st, raw = req("GET", f"/themes/{TID}/assets.json?asset%5Bkey%5D=sections/header-group.json")
hg = json.loads(json.loads(raw)["asset"]["value"])
open("/root/research/product-refresh/dwell_header-group.BACKUP.json", "w").write(json.dumps(hg, indent=2))

sec = hg["sections"]["header_announcements_pbXTDf"]
blk = sec["blocks"]["announcement_KMAGKG"]
print("[announce] before:", repr(blk["settings"]["text"]))
blk["settings"]["text"] = "Free shipping on orders over $75"
print("[announce] after :", repr(blk["settings"]["text"]))

st, resp = req("PUT", f"/themes/{TID}/assets.json",
               {"asset": {"key": "sections/header-group.json", "value": json.dumps(hg, indent=2)}})
print(f"[announce] write HTTP {st} {resp[:200] if st != 200 else ''}")

# ================= 2. BRAND NAME =================
print()
st, raw = req("GET", "/shop.json")
print("[shop] current name:", json.loads(raw)["shop"]["name"])
st, resp = req("PUT", "/shop.json", {"shop": {"name": "Sunday Form"}})
print(f"[shop] update HTTP {st}")
print("[shop] response:", resp[:400])
