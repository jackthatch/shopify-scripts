#!/usr/bin/env python3
"""Swap in: cord-receding lifestyle shots + corded packshot. Hero (pos 1) stays clean."""
import os, json, urllib.request, urllib.error, time

HERE = os.path.dirname(os.path.abspath(__file__))
creds = {}
for line in open(os.path.join(HERE, ".env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); creds[k.strip()] = v.strip()
STORE, TOKEN = creds["SHOPIFY_STORE"], creds["SHOPIFY_TOKEN"]
PID = "15198004674801"
CDN = "https://d8j0ntlcm91z4.cloudfront.net/user_3Jo4yBtd7wwFpQy7zLPTutB7eWo/hf_"

# old ids being replaced: pos2 packshot, pos3 bed, pos4 console
OLD = {2: 50911588942065, 3: 50911615418609, 4: 50911615615217}

def api(method, path, payload=None):
    r = urllib.request.Request(f"https://{STORE}/admin/api/2024-10/{path}",
        data=json.dumps(payload).encode() if payload is not None else None, method=method)
    r.add_header("X-Shopify-Access-Token", TOKEN); r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=180) as x:
            b = x.read().decode(); return x.status, (json.loads(b) if b.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]

NEW = [
 (2, CDN+"20260927_204952_ebca5855-dada-4175-a522-84c7a6686e95.png",
     "Japanese rice paper lantern table lamp with its black power cord trailing away from the camera across the white surface"),
 (3, CDN+"20260927_205149_b5b2fea4-279b-44c4-a620-97cd974f764d.png",
     "Rice paper table lamp glowing on a walnut bedside table, its black power cord receding away from the camera toward the back of the table"),
 (4, CDN+"20260927_205150_794e4f6b-4cfd-4ef5-b9b9-44fab27b6381.png",
     "Rice paper table lamp on an oak console at dusk, its black power cord trailing back into the depth of the scene"),
]
ids = {}
print("uploading finals...")
for pos, url, alt in NEW:
    st, res = api("POST", f"products/{PID}/images.json", {"image": {"src": url, "alt": alt}})
    if st == 200:
        ids[pos] = res["image"]["id"]; print(f"  pos{pos} image_id={ids[pos]}")
    else:
        print(f"  pos{pos} FAILED {st} {res}")
    time.sleep(0.7)

print("\npositioning...")
for pos in (2, 3, 4):
    if pos not in ids: continue
    st, _ = api("PUT", f"products/{PID}/images/{ids[pos]}.json", {"image": {"id": ids[pos], "position": pos}})
    print(f"  pos {pos} -> HTTP {st}"); time.sleep(0.4)

print("\nremoving the superseded versions...")
for pos, iid in OLD.items():
    st, _ = api("DELETE", f"products/{PID}/images/{iid}.json")
    print(f"  pos{pos} old {iid} -> HTTP {st}"); time.sleep(0.4)

time.sleep(3)
st, res = api("GET", f"products/{PID}.json"); p = res["product"]
json.dump(p, open("/root/research/product-refresh/15198004674801/AFTER-cord-final.json","w"), indent=2)
print(f"\n=== FINAL GALLERY ({len(p['images'])} images) ===")
for im in sorted(p["images"], key=lambda x: x.get("position") or 0):
    print(f"  pos {im.get('position'):>2} id={im['id']}  {(im.get('alt') or '')[:74]}")
v = p["variants"][0]
print(f"\nvariant: {v['title']} | ${v['price']} | hero img {v['image_id']} | inv {v['inventory_quantity']}")