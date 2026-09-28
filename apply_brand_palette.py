#!/usr/bin/env python3
"""Apply the brand colour palette to Dwell (unpublished theme). Backup first."""
import os, json, urllib.request, urllib.error, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
creds = {}
for line in open(os.path.join(HERE, ".env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); creds[k.strip()] = v.strip()
STORE, TOKEN = creds["SHOPIFY_STORE"], creds["SHOPIFY_TOKEN"]
API = f"https://{STORE}/admin/api/2024-10"
TID = 186677690609  # Dwell (unpublished)

def req(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(API + path, data=data, method=method)
    r.add_header("X-Shopify-Access-Token", TOKEN)
    r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=90) as x:
            return x.status, json.loads(x.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")[:600]

# ---- read current ----
st, d = req("GET", f"/themes/{TID}/assets.json?asset%5Bkey%5D=config/settings_data.json")
sd = json.loads(d["asset"]["value"])
shutil.copy("/tmp/dwell_settings_data.json",
            "/root/research/product-refresh/dwell_settings_data.BACKUP.json")
print("[backup] saved dwell_settings_data.BACKUP.json")
print("[before] palette:", sd["current"].get("color_palette"))

# ---- brand palette ----
BRAND = {
    "background": "#F4EFE5",   # ivory  - page ground
    "foreground": "#30251F",   # espresso - text + primary buttons
    "color1":     "#C56A32",   # burnt orange - accent / sale badge
    "color3":     "#E6DFD2",   # soft border (ivory, slightly deepened)
    "color4":     "#CFC3B2",   # stronger border
}
sd["current"]["color_palette"] = BRAND
print("[after ] palette:", BRAND)

st, resp = req("PUT", f"/themes/{TID}/assets.json",
               {"asset": {"key": "config/settings_data.json", "value": json.dumps(sd, indent=2)}})
print(f"[write ] HTTP {st}")

# ---- verify ----
st, d2 = req("GET", f"/themes/{TID}/assets.json?asset%5Bkey%5D=config/settings_data.json")
got = json.loads(d2["asset"]["value"])["current"].get("color_palette")
print("[verify] palette now:", got)
print("[verify] match:", got == BRAND)
