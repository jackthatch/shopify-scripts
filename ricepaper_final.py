#!/usr/bin/env python3
"""Rice-paper lamp: upload 4 finals, map hero->variant, drop supplier imagery, order gallery,
and rewrite the description with inches-first dimensions."""
import os, json, urllib.request, urllib.error, time

HERE = os.path.dirname(os.path.abspath(__file__))
creds = {}
for line in open(os.path.join(HERE, ".env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); creds[k.strip()] = v.strip()
STORE, TOKEN = creds["SHOPIFY_STORE"], creds["SHOPIFY_TOKEN"]
PID  = "15198004674801"
VAR  = 67095118217457          # the surviving Us Plug / A variant
CDN  = "https://d8j0ntlcm91z4.cloudfront.net/user_3Jo4yBtd7wwFpQy7zLPTutB7eWo/hf_"

def api(method, path, payload=None):
    r = urllib.request.Request(f"https://{STORE}/admin/api/2024-10/{path}",
        data=json.dumps(payload).encode() if payload is not None else None, method=method)
    r.add_header("X-Shopify-Access-Token", TOKEN); r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=180) as x:
            b = x.read().decode(); return x.status, (json.loads(b) if b.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]

UP = [
 ("hero",      CDN+"20260927_204140_1c35c728-d32e-425e-9ec0-b6e98654ba2d.png",
  "Japanese rice paper table lamp lit on a black iron tripod base, \u00d811 in (28 cm) \u00d7 18.5 in (47 cm)"),
 ("packshot",  CDN+"20260927_204140_5d268cd1-e1a3-4188-b609-d364ab938d58.png",
  "Japanese rice paper lantern table lamp with a natural white shade and black metal tripod, on a white background"),
 ("lifestyle-bed", CDN+"20260927_204139_46361217-7f17-4a09-a5a7-1158c585fff5.png",
  "Rice paper table lamp glowing warm on a walnut bedside table beside a linen bed"),
 ("lifestyle-con", CDN+"20260927_204139_bc388e2a-fa05-482a-a054-ac8fac8b95d6.png",
  "Rice paper table lamp on an oak console in a warm living room at dusk"),
]

ids = {}
print("uploading 4 finals...")
for key, url, alt in UP:
    st, res = api("POST", f"products/{PID}/images.json", {"image": {"src": url, "alt": alt}})
    if st == 200:
        ids[key] = res["image"]["id"]; print(f"  {key:15} image_id={ids[key]}")
    else:
        print(f"  {key:15} FAILED {st} {res}")
    time.sleep(0.7)

st, res = api("PUT", f"variants/{VAR}.json", {"variant": {"id": VAR, "image_id": ids["hero"]}})
print(f"\nhero mapped to variant {VAR} -> HTTP {st}")

SUPPLIER = [50911496339697, 50911496372465, 50911496405233, 50911496438001,
            50911496470769, 50911496503537, 50911496536305, 50911496569073]
TEMP     = 50911563088113
print("\nremoving supplier imagery + my scratch upload...")
for iid, why in [(i, "supplier") for i in SUPPLIER] + [(TEMP, "temp-ref")]:
    st, _ = api("DELETE", f"products/{PID}/images/{iid}.json")
    print(f"  {iid} ({why}) -> HTTP {st}")
    time.sleep(0.4)

print("\nordering gallery...")
for pos, key in enumerate(["hero", "packshot", "lifestyle-bed", "lifestyle-con"], start=1):
    st, _ = api("PUT", f"products/{PID}/images/{ids[key]}.json", {"image": {"id": ids[key], "position": pos}})
    print(f"  pos {pos} {key:15} HTTP {st}")
    time.sleep(0.4)

DESC = """<p>A handcrafted rice paper lantern on a slender black tripod &mdash; quiet, warm light for a bedside table, a reading corner or a low console.</p>
<p>The shade is made the traditional way: rice paper laid over fine horizontal bamboo ribs, so the light comes through in soft, even bands. Switch it on and it pools warm, low light exactly where you need it &mdash; never harsh, never clinical.</p>
<ul>
<li><strong>Dimensions:</strong> &Oslash;11 in (28 cm) wide &times; 18.5 in (47 cm) tall &mdash; roughly the height of two stacked hardcover books</li>
<li><strong>Materials:</strong> handcrafted rice paper shade, iron tripod base</li>
<li><strong>Light source:</strong> E27 LED, 3 colour temperatures</li>
<li><strong>Switch:</strong> push button</li>
<li><strong>Plug:</strong> US plug, 110V</li>
<li><strong>Finish:</strong> natural white shade, black metal base</li>
<li><strong>Style:</strong> Japanese wabi-sabi</li>
</ul>
<p>Compact at 11 in across, so it suits small spaces as easily as it suits a large room.</p>"""
st, res = api("PUT", f"products/{PID}.json", {"product": {"id": int(PID), "body_html": DESC}})
print(f"\ndescription updated -> HTTP {st}")

time.sleep(3)
st, res = api("GET", f"products/{PID}.json"); p = res["product"]
json.dump(p, open("/root/research/product-refresh/15198004674801/AFTER-final.json","w"), indent=2)
print(f"\n=== FINAL === images {len(p['images'])} | variants {len(p['variants'])} | options {[(o['name'],o['values']) for o in p['options']]}")
for im in sorted(p["images"], key=lambda x: x.get("position") or 0):
    print(f"  pos {im.get('position'):>2} id={im['id']}  {(im.get('alt') or '')[:62]}")
for v in p["variants"]:
    print(f"  variant {v['id']} | {v['title']} | ${v['price']} | img={v['image_id']} | inv={v['inventory_quantity']}")