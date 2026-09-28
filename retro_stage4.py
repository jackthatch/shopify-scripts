#!/usr/bin/env python3
"""Stage 4: upload 15 heroes + 2 lifestyle, map heroes to variants, drop superseded
supplier diagrams, and order the gallery."""
import os, json, base64, urllib.request, urllib.error, time

HERE = os.path.dirname(os.path.abspath(__file__))
creds = {}
for line in open(os.path.join(HERE, ".env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); creds[k.strip()] = v.strip()
STORE, TOKEN = creds["SHOPIFY_STORE"], creds["SHOPIFY_TOKEN"]
PID = "15197432971505"
CDN = "https://d8j0ntlcm91z4.cloudfront.net/user_3Jo4yBtd7wwFpQy7zLPTutB7eWo/hf_"

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
        return e.code, e.read().decode()[:400]

# code -> (retail name, cdn filename, variant_id)
V = {
 "C4": ("Tea Green On Dark Green","20260927_200015_f1ee8225-7b35-491e-bc7c-5318a119e859.png",67093442035953),
 "A1": ("White On Wine Red",     "20260927_200112_4f80b0b1-0902-4dbe-a63f-b90391563399.png",67093441708273),
 "A2": ("White On Beige",        "20260927_200146_5ab6fbc6-de52-4698-98c6-197009f72f95.png",67093441642737),
 "A3": ("White On Pink",         "20260927_200112_ee1783b1-3502-4d53-8ff5-09a4de8db2fc.png",67093442101489),
 "A4": ("White On Dark Green",   "20260927_200112_83b54223-8d12-4a89-b64d-add931b030dd.png",67093441773809),
 "B1": ("Orange On Yellow",      "20260927_200146_443cb602-7c7c-4878-a2cf-158be6e26918.png",67093441609969),
 "B2": ("Orange On Beige",       "20260927_200145_8f563d57-bff2-47bb-b1e7-0e3b44ea1abd.png",67093442167025),
 "B3": ("Orange On Wine Red",    "20260927_200113_e5167a4b-1020-4d35-aa2c-79b9aa273171.png",67093441839345),
 "B4": ("Orange On Dark Green",  "20260927_200146_641cc896-908f-4b08-9d87-0352c58b2f32.png",67093442265329),
 "C1": ("Tea Green On Wine Red", "20260927_200219_54488ecd-0650-4eb4-896e-976346e9060f.png",67093441970417),
 "C2": ("Tea Green On Beige",    "20260927_200219_597611ef-d346-4bf3-964e-092332e12808.png",67093441904881),
 "C3": ("Tea Green On Pink",     "20260927_200219_c3b5d92d-8ca4-4c69-a71b-a50115136594.png",67093442330865),
 "D1": ("Green On Beige",        "20260927_201152_89c811c2-f128-428f-ad05-8beb7db1e890.png",67093442461937),
 "D2": ("Green On Yellow",       "20260927_201153_2cce0346-2068-4d91-8554-01651f1b9640.png",67093442396401),
 "D3": ("Green On Dark Green",   "20260927_201153_3b64e985-f856-4fb2-b18f-bd2fc29dad62.png",67093442527473),
}
# supplier diagrams that currently serve as the variant images -> superseded
OLD_DIAGRAMS = [50904650219761,50904650416369,50904650449137,50904650481905,50904650514673,
                50904650547441,50904650580209,50904650612977,50904650645745,50904650678513,
                50904650711281,50904650744049,50904650776817,50904650809585,50904650842353]

# ---- 1. upload the 15 heroes via src ----
img_ids = {}
print("uploading heroes...")
for code, (name, fn, vid) in sorted(V.items()):
    st, res = api("POST", f"products/{PID}/images.json",
                  {"image": {"src": CDN + fn,
                             "alt": f"Nordic glass pendant lamp in {name}"}})
    if st == 200:
        iid = res["image"]["id"]; img_ids[code] = iid
        print(f"  {code:3} {name:24} image_id={iid}")
    else:
        print(f"  {code:3} FAILED HTTP {st} {str(res)[:200]}")
    time.sleep(0.6)

# ---- 2. upload the 2 lifestyle shots (local -> base64) ----
print("\nuploading lifestyle...")
life_ids = {}
for fn, alt in [("/tmp/01-lifestyle-dining-D3.png",  "Nordic glass pendant lamp over a dining table"),
                ("/tmp/02-lifestyle-bedroom-A1.png", "Wine red Nordic glass pendant lamp beside a bed")]:
    b64 = base64.b64encode(open(fn, "rb").read()).decode()
    st, res = api("POST", f"products/{PID}/images.json",
                  {"image": {"attachment": b64, "filename": os.path.basename(fn), "alt": alt}})
    if st == 200:
        life_ids[fn] = res["image"]["id"]; print(f"  {os.path.basename(fn):32} image_id={res['image']['id']}")
    else:
        print(f"  {os.path.basename(fn):32} FAILED HTTP {st} {str(res)[:200]}")
    time.sleep(0.6)

# ---- 3. map each hero to its variant ----
print("\nmapping heroes -> variants...")
for code, (name, fn, vid) in sorted(V.items()):
    if code not in img_ids: print(f"  {code} skipped (no image)"); continue
    st, res = api("PUT", f"variants/{vid}.json",
                  {"variant": {"id": vid, "image_id": img_ids[code]}})
    print(f"  {code:3} variant {vid} <- image {img_ids[code]}  HTTP {st}")
    time.sleep(0.4)

json.dump({"hero_images": img_ids, "lifestyle_images": life_ids},
          open("/root/research/product-refresh/15197432971505/20260927-retro-glass-chandelier/uploaded_image_ids.json","w"), indent=2)

# ---- 4. delete superseded supplier diagrams ----
print("\ndeleting superseded supplier diagrams...")
for iid in OLD_DIAGRAMS:
    st, _ = api("DELETE", f"products/{PID}/images/{iid}.json")
    print(f"  delete image {iid} -> HTTP {st}")
    time.sleep(0.4)

# ---- 5. order the gallery ----
order = [("hero","C4"),("life","/tmp/01-lifestyle-dining-D3.png"),("life","/tmp/02-lifestyle-bedroom-A1.png")]
order += [("hero",c) for c in ["A1","A2","A3","A4","B1","B2","B3","B4","C1","C2","C3","D1","D2","D3"]]
print("\nordering gallery...")
pos = 1
for kind, key in order:
    iid = img_ids.get(key) if kind == "hero" else life_ids.get(key)
    if not iid: pos += 1; continue
    st, _ = api("PUT", f"product_images/{iid}.json", {"image": {"id": iid, "position": pos}})
    print(f"  pos {pos:2}  {kind:4} {key.split('/')[-1]:28} HTTP {st}")
    pos += 1
    time.sleep(0.35)

time.sleep(3)
st, prod = api("GET", f"products/{PID}.json"); prod = prod["product"]
json.dump(prod, open("/root/research/product-refresh/15197432971505/20260927-retro-glass-chandelier/AFTER-upload.json","w"), indent=2)
print(f"\n=== FINAL === images: {len(prod['images'])} | variants: {len(prod['variants'])}")
for im in sorted(prod["images"], key=lambda x: x.get("position") or 0):
    print(f"  pos {im.get('position'):>2}  id={im['id']}  alt={im.get('alt')}")