# 🦁 At Large

**A century of American newspapers reporting animals on the loose.**

→ **[Open it](https://tnriley.github.io/at-large/)**

There is no dataset of animals escaping from zoos, so this builds one out of full-text search over Chronicling America — the Library of Congress archive of digitised American newspapers. 3,413 pages from 20 period phrasings, 1758–1963, filterable by phrase, animal, decade and state, each linking to the scanned page with the term highlighted. The intended plan was to mine the OCR for what escaped and what happened next; that failed, for a reason the page explains and turns into its subject.

## Running it

One self-contained HTML file. No build step, no server, no network access at runtime — open `index.html` in a browser, or serve the directory with any static host.

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Rebuilding it from scratch

[REBUILD.md](REBUILD.md) is written for an LLM with a shell and nothing else: the data sources and their quirks, the processing decisions, the page's structure and interactions, and a table of expected values to check the result against.

## Source

The full build pipeline is in [`src/`](src/), with a README describing how to regenerate the page from scratch.

## Data

- **[Chronicling America, Library of Congress](https://www.loc.gov/collections/chronicling-america/)** — US Library of Congress — public domain

Every figure on the page is computed from the data shipped with it. Check the page's own methods panel for how each number is derived and where it should not be pushed.

## Built with

vanilla JS, canvas, Bodoni Moda.

## Licence

Code is MIT (see [LICENSE](LICENSE)). Data keeps the licence of its source, listed above.

---

Part of [Quick Projects](https://github.com/TNRiley/quick-projects) — one self-contained thing, built in one session. First published 2026-09-05.
