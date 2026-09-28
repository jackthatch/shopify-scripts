#!/usr/bin/env python3
"""Apply a West Elm-inspired type system to the (unpublished) Dwell theme.

Two families, four theme slots:
  heading     = Newsreader 300   -> display serif (h1-h3)
  body        = Jost 400         -> body copy, inputs
  subheading  = Jost 500         -> nav, small titles
  accent      = Jost 500         -> card titles, eyebrows/labels, buttons
"""
import json, os, urllib.request, urllib.error, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
creds = {}
for line in open(os.path.join(HERE, ".env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); creds[k.strip()] = v.strip()
STORE, TOKEN = creds["SHOPIFY_STORE"], creds["SHOPIFY_TOKEN"]
TID = "186677690609"   # Dwell (unpublished)
BACKUP = "/root/research/product-refresh/dwell_settings_data.BACKUP2.json"

def get_asset(key):
    r = urllib.request.Request(f"https://{STORE}/admin/api/2024-10/themes/{TID}/assets.json?asset[key]={key}")
    r.add_header("X-Shopify-Access-Token", TOKEN)
    with urllib.request.urlopen(r, timeout=120) as x:
        return json.loads(x.read().decode())["asset"]["value"]

def put_asset(key, value):
    r = urllib.request.Request(f"https://{STORE}/admin/api/2024-10/themes/{TID}/assets.json",
        data=json.dumps({"asset": {"key": key, "value": value}}).encode(), method="PUT")
    r.add_header("X-Shopify-Access-Token", TOKEN); r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=120) as x:
            return x.status
    except urllib.error.HTTPError as e:
        return f"{e.code} {e.read().decode()[:200]}"

sd = json.loads(get_asset("config/settings_data.json"))
open(BACKUP, "w").write(json.dumps(sd, indent=2))

NEW = {
  # --- the four font slots: serif display + one geometric sans everywhere else
  "type_heading_font":    "newsreader_n3",   # display serif, light
  "type_body_font":       "jost_n4",         # body copy
  "type_subheading_font": "jost_n5",         # nav / small titles
  "type_accent_font":     "jost_n5",         # card titles / labels / buttons
  # --- body copy: 16px reads properly (was 14px serif)
  "type_size_paragraph":     "16",
  "type_line_height_paragraph": "body-normal",
  # --- display scale, tightened
  "type_font_h1": "heading", "type_size_h1": "56",
  "type_line_height_h1": "display-tight", "type_letter_spacing_h1": "heading-tight", "type_case_h1": "none",
  "type_font_h2": "heading", "type_size_h2": "40",
  "type_line_height_h2": "display-tight", "type_letter_spacing_h2": "heading-tight", "type_case_h2": "none",
  "type_font_h3": "heading", "type_size_h3": "24",
  "type_line_height_h3": "display-normal", "type_letter_spacing_h3": "heading-normal", "type_case_h3": "none",
  # --- card titles leave uppercase behind; only the eyebrow stays uppercase
  "type_font_h4": "accent", "type_size_h4": "18",
  "type_line_height_h4": "display-normal", "type_letter_spacing_h4": "heading-normal", "type_case_h4": "none",
  "type_font_h5": "body", "type_size_h5": "16",
  "type_line_height_h5": "display-normal", "type_letter_spacing_h5": "heading-normal", "type_case_h5": "none",
  # --- h6 is the West Elm eyebrow: small, uppercase, tracked, sans
  "type_font_h6": "accent", "type_size_h6": "12",
  "type_line_height_h6": "display-normal", "type_letter_spacing_h6": "heading-loose", "type_case_h6": "uppercase",
  # --- buttons in the sans, not the serif
  "type_font_button_primary": "accent",
  "type_font_button_secondary": "accent",
}

print("changes:")
for k, v in NEW.items():
    old = sd["current"].get(k, "<unset>")
    if old != v:
        print(f"  {k}: {old!r} -> {v!r}")
    sd["current"][k] = v

st = put_asset("config/settings_data.json", json.dumps(sd, indent=2))
print("\nPUT settings_data.json ->", st)
