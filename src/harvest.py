#!/usr/bin/env python3
"""Harvest zoo-escape reports from Chronicling America (Library of Congress).

The loc.gov collection endpoint returns, per matching newspaper page: the date, the paper,
its city and state, an OCR excerpt around the match, a link to the page viewer with the term
highlighted, and IIIF image URLs for the scan itself. There is no dataset of zoo escapes;
this builds one out of full-text search over digitised American newspapers.
"""
import json, urllib.request, urllib.parse, time, sys, os

UA = {"User-Agent": "quick-projects/1.0 (personal research; tnriley@gmail.com)"}
BASE = "https://www.loc.gov/collections/chronicling-america/"

QUERIES = [
 '"escaped from the zoo"', '"escaped from the zoological garden"', '"escaped from the menagerie"',
 '"broke loose from the zoo"', '"escaped from the zoological park"', '"escape from the zoo"',
 '"lion at large"', '"tiger at large"', '"bear at large"', '"elephant at large"',
 '"escaped lion"', '"escaped tiger"', '"escaped bear"', '"escaped elephant"',
 '"escaped leopard"', '"escaped monkey"', '"escaped wolf"', '"escaped panther"',
 '"escaped from his cage"', '"escaped from her cage"',
]
PAGES_PER_QUERY = 3
PER_PAGE = 100

def fetch(q, page):
    u = BASE + "?" + urllib.parse.urlencode({"q": q, "fo": "json", "c": PER_PAGE, "sp": page})
    for attempt in range(4):
        try:
            req = urllib.request.Request(u, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except Exception as e:
            if attempt == 3:
                print(f"    FAIL {q} p{page}: {e}", flush=True)
                return None
            time.sleep(3 * (attempt + 1))

seen, out = set(), []
for qi, q in enumerate(QUERIES):
    got = 0
    for page in range(1, PAGES_PER_QUERY + 1):
        d = fetch(q, page)
        if not d:
            break
        res = d.get("results") or []
        total = d.get("pagination", {}).get("of")
        for r in res:
            pid = r.get("id") or r.get("url")
            if not pid or pid in seen:
                continue
            seen.add(pid)
            desc = r.get("description") or []
            out.append({
                "id": pid,
                "url": r.get("url"),
                "date": r.get("date"),
                "paper": (r.get("partof_title") or [""])[0],
                "city": (r.get("location_city") or [""])[0],
                "state": (r.get("location_state") or [""])[0],
                "text": (desc[0] if desc else "")[:2600],
                "img": (r.get("image_url") or [None])[0],
                "page": r.get("number_page"),
                "q": q,
            })
            got += 1
        if not res or (d.get("pagination", {}).get("current") == d.get("pagination", {}).get("last")):
            break
        time.sleep(0.6)
    print(f"  [{qi+1}/{len(QUERIES)}] {q:42} total={total} kept_new={got} running={len(out)}", flush=True)
    json.dump(out, open("raw.json", "w"))
print(f"DONE {len(out)} unique pages -> raw.json", flush=True)
