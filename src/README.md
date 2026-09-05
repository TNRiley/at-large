# At Large — build pipeline

```bash
python3 harvest.py         # 20 phrase searches against loc.gov -> raw.json  (slow: ~35 min)
python3 build_payload.py   # score and shape -> payload.json
python3 inject.py          # splice into the templates -> ../index.html
```

`harvest.py` writes `raw.json` after every query, so it can be interrupted and the later steps
still work on a partial harvest. Raw downloads are gitignored.

## The thing to know

The loc.gov search record's `description` field is a fixed ~1,000-character sample of the page's
OCR, **not the passage that matched** — only about 4% of excerpts contain the phrase that found
them. Everything the page asserts therefore comes from the *search phrase*, which the archive does
guarantee appears on the page, and never from the excerpt text. See `../REBUILD.md`.

Source: Chronicling America, Library of Congress. Public domain.
