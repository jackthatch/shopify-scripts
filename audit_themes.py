#!/usr/bin/env python3
"""Phase 1 audit: read theme structure/settings for Helio (live) and Dwell (candidate)."""
import os, json, urllib.request, urllib.error

creds = {}
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); creds[k.strip()] = v.strip()
STORE, TOKEN = creds["SHOPIFY_STORE"], creds["SHOPIFY_TOKEN"]

def get(path):
    r = urllib.request.Request(f"https://{STORE}/admin/api/2024-10{path}")
    r.add_header("X-Shopify-Access-Token", TOKEN)
    try:
        with urllib.request.urlopen(r, timeout=90) as x:
            return json.loads(x.read().decode())
    except urllib.error.HTTPError as e:
        return {"__err": f"HTTP {e.code}: {e.read().decode()[:300]}"}

THEMES = {"Helio (LIVE)": 166723944689, "Dwell (candidate)": 186677690609}

for label, tid in THEMES.items():
    print("=" * 64)
    print(label, f"id={tid}")
    print("=" * 64)
    a = get(f"/themes/{tid}/assets.json")
    if "__err" in a:
        print(" ", a["__err"]); continue
    keys = [x["key"] for x in a.get("assets", [])]
    print(f" assets: {len(keys)}")
    print(" sections:", len([k for k in keys if k.startswith("sections/")]))
    print(" templates:", [k.replace("templates/", "") for k in keys if k.startswith("templates/")])

    idx = get(f"/themes/{tid}/assets.json?asset%5Bkey%5D=templates/index.json")
    if "asset" in idx:
        try:
            val = json.loads(idx["asset"]["value"])
            print(" homepage order:")
            for sid in val.get("order", []):
                s = val["sections"].get(sid, {})
                print(f"    - {s.get('type'):32} blocks={len(s.get('blocks', {}))}")
        except Exception as e:
            print("  index parse err", e)

    sd = get(f"/themes/{tid}/assets.json?asset%5Bkey%5D=config/settings_data.json")
    if "asset" in sd:
        try:
            cur = json.loads(sd["asset"]["value"]).get("current", {})
            print(f" theme settings keys: {len(cur)}")
            for k in ["logo", "favicon", "colors_schemes", "type_header_font", "type_body_font",
                      "type_body_font_size", "page_width", "social_twitter_link"]:
                if k in cur:
                    print(f"    {k} = {str(cur[k])[:150]}")
        except Exception as e:
            print("  settings parse err", e)
    print()
