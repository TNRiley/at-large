#!/usr/bin/env python3
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
payload = open(os.path.join(HERE, "payload.json"), encoding="utf-8").read()
parts = [open(os.path.join(HERE, f), encoding="utf-8").read() for f in ("t.head.html", "t.body.html")]
js = open(os.path.join(HERE, "t.js.html"), encoding="utf-8").read().replace("__PAYLOAD__", payload)
out = os.path.join(HERE, "index.html")
open(out, "w", encoding="utf-8").write("\n".join(parts) + "\n" + js + "\n")
print("wrote", out, f"{os.path.getsize(out):,} bytes")
