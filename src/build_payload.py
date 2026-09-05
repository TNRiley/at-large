#!/usr/bin/env python3
"""Shape harvested Chronicling America pages into payload.json.

IMPORTANT, and the reason this file looks the way it does: the loc.gov search record's
`description` field is a ~1,000-character sample of the page's OCR, NOT the passage that
matched. Measured across the harvest, only about 4% of excerpts contain the phrase that
found them. So nothing here is inferred from the excerpt text.

What IS reliable is the phrase itself: the search guarantees it appears somewhere on that
page. So the animal, and how strongly the phrase implies a zoo escape, are read from the
QUERY, not from OCR guesswork.
"""
import json, re, datetime, collections

# per-query: (animal or None, specificity 0-100 that the phrase means a captive animal got out)
QMETA = {
 '"escaped from the zoo"':              (None, 96),
 '"escape from the zoo"':               (None, 90),
 '"escaped from the zoological garden"':(None, 96),
 '"escaped from the zoological park"':  (None, 96),
 '"broke loose from the zoo"':          (None, 96),
 '"escaped from the menagerie"':        (None, 86),
 '"escaped lion"':      ("lion", 62),      '"lion at large"':      ("lion", 48),
 '"escaped tiger"':     ("tiger", 68),     '"tiger at large"':     ("tiger", 55),
 '"escaped bear"':      ("bear", 42),      '"bear at large"':      ("bear", 22),
 '"escaped elephant"':  ("elephant", 78),  '"elephant at large"':  ("elephant", 72),
 '"escaped leopard"':   ("leopard", 70),   '"escaped monkey"':     ("monkey", 66),
 '"escaped wolf"':      ("wolf", 38),      '"escaped panther"':    ("panther", 40),
 '"escaped from his cage"': (None, 58),    '"escaped from her cage"': (None, 58),
}
norm = lambda t: re.sub(r"\s+", " ", (t or "")).strip()

raw = json.load(open("raw.json"))
papers, states, animals, phrases = {}, {}, {None: 0}, {}
def idx(tbl, v):
    if v not in tbl: tbl[v] = len(tbl)
    return tbl[v]

recs, seen = [], set()
for r in raw:
    u = r.get("url")
    if not u or not r.get("date") or u in seen: continue
    seen.add(u)
    animal, spec = QMETA.get(r["q"], (None, 50))
    text = norm(r.get("text"))
    d = r["date"]
    d = f"{d[:4]}-{d[4:6]}-{d[6:8]}" if len(d) == 8 and d.isdigit() else d
    y = d[:4]
    if not (y.isdigit() and 1750 < int(y) < 2030): continue
    paper = re.sub(r"\s*\d{4}-\d{4}\s*$", "", (r.get("paper") or "")).strip()
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    recs.append({
        "d": d[:10],
        "pa": idx(papers, paper),
        "ct": (r.get("city") or "")[:40],
        "st": idx(states, r.get("state") or ""),
        "an": idx(animals, animal),
        "ph": idx(phrases, r["q"].strip('"')),
        "cf": spec,
        "pg": str(r.get("page") or "").lstrip("0") or None,
        "tx": esc(text[:1100]),
        "u": u,
    })

recs.sort(key=lambda x: (-x["cf"], x["d"]))
years = [int(r["d"][:4]) for r in recs]
inv = lambda t: [k for k, v in sorted(t.items(), key=lambda kv: kv[1])]
out = {
    "built": datetime.date.today().isoformat(),
    "papers": inv(papers), "states": inv(states),
    "animals": [a if a else "" for a in inv(animals)],
    "phrases": inv(phrases),
    "yearMin": min(years), "yearMax": max(years),
    "recs": recs,
}
js = json.dumps(out, separators=(",", ":"), ensure_ascii=False)
open("payload.json", "w", encoding="utf-8").write(js)
print(f"records {len(recs)}  papers {len(papers)}  states {len(states)}  phrases {len(phrases)}  years {out['yearMin']}-{out['yearMax']}")
print("by phrase:", collections.Counter(out["phrases"][r["ph"]] for r in recs).most_common())
print("by animal:", collections.Counter(out["animals"][r["an"]] for r in recs if r["an"]).most_common())
print(f"payload.json {len(js):,} bytes")
