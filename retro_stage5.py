#!/usr/bin/env python3
"""Stage 5: correct endpoint for image positions + verify variant->image mapping."""
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
        with urllib.request.urlopen(r, timeout=180) as resp:
            b = resp.read().decode()
            return resp.status, (json.loads(b) if b.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]

ids = json.load(open("/root/research/product-refresh/15197432971505/20260927-retro-glass-chandelier/uploaded_image_ids.json"))
H = {k: v for k, v in ids["hero_images"].items()}
L = list(ids["lifestyle_images"].values())

life_dining, life_bedroom = L[0], L[1]
target = [(H["C4"],"hero C4 (lead)"), (life_dining,"lifestyle dining"), (life_bedroom,"lifestyle bedroom")]
for c in ["A1","A2","A3","A4","B1","B2","B3","B4","C1","C2","C3","D1","D2","D3"]:
    target.append((H[c], f"hero {c}"))
# leftover supplier images go last
st, prod = api("GET", f"products/{PID}.json"); prod = prod["product"]
known = {i for i,_ in target}
supplier = [im["id"] for im in sorted(prod["images"], key=lambda x: x.get("position") or 0) if im["id"] not in known]
for i in supplier: target.append((i, "supplier (kept)"))

print("setting positions via /products/{pid}/images/{iid}.json ...")
for pos, (iid, label) in enumerate(target, start=1):
    st, _ = api("PUT", f"products/{PID}/images/{iid}.json", {"image": {"id": iid, "position": pos}})
    print(f"  pos {pos:2}  {label:20} HTTP {st}")
    time.sleep(0.35)

time.sleep(3)
st, prod = api("GET", f"products/{PID}.json"); prod = prod["product"]
print(f"\n=== GALLERY ({len(prod['images'])} images) ===")
for im in sorted(prod["images"], key=lambda x: x.get("position") or 0):
    print(f"  pos {im.get('position'):>2}  id={im['id']}  {(im.get('alt') or '')[:52]}")

# verify variant -> image mapping
print("\n=== VARIANT -> IMAGE MAPPING ===")
NAMES = {"A1":"White On Wine Red","A2":"White On Beige","A3":"White On Pink","A4":"White On Dark Green",
         "B1":"Orange On Yellow","B2":"Orange On Beige","B3":"Orange On Wine Red","B4":"Orange On Dark Green",
         "C1":"Tea Green On Wine Red","C2":"Tea Green On Beige","C3":"Tea Green On Pink","C4":"Tea Green On Dark Green",
         "D1":"Green On Beige","D2":"Green On Yellow","D3":"Green On Dark Green"}
img_by_id = {im["id"]: (im.get("alt") or "") for im in prod["images"]}
bad = []
for v in sorted(prod["variants"], key=lambda x: x["title"]):
    code = v["title"]
    expect_id  = H.get(code)
    expect_alt = f"in {NAMES.get(code,'')}"
    got_alt = img_by_id.get(v.get("image_id"), "<none>")
    ok = v.get("image_id") == expect_id and expect_alt in got_alt
    if not ok: bad.append(code)
    print(f"  {code:3} {NAMES.get(code,''):24} image={v.get('image_id')}  {'OK' if ok else 'MISMATCH'}  alt={got_alt[:46]}")
print("\nRESULT:", "all 15 mapped correctly" if not bad else f"MISMATCHES: {bad}")
print("prices:", {v["price"] for v in prod["variants"]}, "| options:", [(o["name"],o["values"]) for o in prod["options"]])
json.dump(prod, open("/root/research/product-refresh/15197432971505/20260927-retro-glass-chandelier/AFTER-order.json","w"), indent=2)