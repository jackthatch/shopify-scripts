#!/usr/bin/env python3
"""Tiny Shopify Admin API client. Reads creds from .env next to this file.
Usage:  python3 sapi.py GET /themes/166723944689/assets.json
        python3 sapi.py GET /products.json 'limit=5'
        python3 sapi.py POST /products.json body.json
Outputs JSON to stdout.
"""
import sys, os, json, urllib.request, urllib.error, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
creds = {}
for line in open(os.path.join(HERE, ".env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        creds[k.strip()] = v.strip().strip('"').strip("'")

STORE = creds["SHOPIFY_STORE"]
TOKEN = creds["SHOPIFY_TOKEN"]
API = f"https://{STORE}/admin/api/2024-10"

def main():
    method = sys.argv[1].upper()
    path = sys.argv[2]
    payload = None
    timeout = 180
    args = sys.argv[3:]
    for a in args:
        if a.endswith(".json") and os.path.exists(a):
            payload = json.load(open(a))
        elif "=" in a and method == "GET":
            sep = "&" if "?" in path else "?"
            path = path + sep + a
        elif a.isdigit():
            timeout = int(a)
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("X-Shopify-Access-Token", TOKEN)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            print(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode(errors='replace')[:2000]}")

main()
