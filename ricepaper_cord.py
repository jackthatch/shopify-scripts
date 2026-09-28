#!/usr/bin/env python3
"""Replace the two lifestyle images with cord-visible versions."""
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
OLD_BED, OLD_CON = 50911589073137, 50911589171441

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
 ("lifestyle-bed", CDN+"20260927_204659_1cf1079b-b9a4-4941-b5f9-77d22875d880.png",
  "Rice paper table lamp glowing warm on a walnut bedside table, its black power cord running across the tabletop"),
 ("lifestyle-con", CDN+"20260927_204658_4849b9fc-11e6-4b09-b60c-87b062e1b529.png",
  "Rice paper table lamp on an oak console at dusk with its black power cord visible across the surface"),
]
ids = {}
print("uploading cord versions...")
for key, url, alt in NEW:
    st, res = api("POST", f"products/{PID}/images.json", {"image": {"src": url, "alt": alt}})
    if st == 200:
        ids[key] = res["image"]["id"]; print(f"  {key:15} image_id={ids[key]}")
    else:
        print(f"  {key:15} FAILED {st} {res}")
    time.sleep(0.7)

print("\npositioning...")
for pos, key in [(3, "lifestyle-bed"), (4, "lifestyle-con")]:
    st, _ = api("PUT", f"products/{PID}/images/{ids[key]}.json", {"image": {"id": ids[key], "position": pos}})
    print(f"  pos {pos} {key:15} HTTP {st}"); time.sleep(0.4)

print("\nremoving the cordless versions...")
for iid, why in [(OLD_BED, "old bed"), (OLD_CON, "old console")]:
    st, _ = api("DELETE", f"products/{PID}/images/{iid}.json")
    print(f"  {iid} ({why}) -> HTTP {st}"); time.sleep(0.4)

time.sleep(3)
st, res = api("GET", f"products/{PID}.json"); p = res["product"]
json.dump(p, open("/root/research/product-refresh/15198004674801/AFTER-cord.json","w"), indent=2)
print(f"\n=== FINAL GALLERY ({len(p['images'])} images) ===")
for im in sorted(p["images"], key=lambda x: x.get("position") or 0):
    print(f"  pos {im.get('position'):>2} id={im['id']}  {(im.get('alt') or '')[:66]}")
print("\nvariant:", p["variants"][0]["title"], "| $"+p["variants"][0]["price"], "| hero img:", p["variants"][0]["image_id"])