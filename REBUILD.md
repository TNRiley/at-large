# Rebuilding At Large

Written for an LLM with a shell, starting from nothing but this file. **Read section 2 before
you write any code** — it is the whole reason this project looks the way it does, and it cost
the original build most of its plan.

---

## 1. What you are building

A single self-contained HTML page: an index of American newspaper pages that report an animal on
the loose, built by full-text search over **Chronicling America**, the Library of Congress's
archive of digitised newspapers. The reader filters by phrase, animal, decade and state, screens
records keep/toss like an evidence review, and clicks through to the scanned page.

## 2. The trap, and why the project changed shape

Search the collection endpoint and each hit comes back with a `description` field of about a
thousand characters of OCR. It looks like the matching clipping. **It is not.** It is a fixed
sample of the page's text, and a broadsheet page holds tens of thousands of words.

Measured across the full harvest: **only ~4% of excerpts contain the phrase that found them.**

The original plan — read the animal out of the clipping, read whether it was recaptured or shot,
score each hit's plausibility from its wording — was therefore mining random newsprint. The first
run scored 633 of 726 records below 0.2 confidence, which is what tipped it off.

Two ways forward:

- **Fetch the real snippet per page** via the `word_coordinates_url` on each record with
  `relevant_snippet=1`. Correct, but it is one slow request per page and the API is slow enough
  that 3,400 of them is over an hour.
- **Assert only what the search guarantees** — that the phrase is on the page. Derive the animal
  from animal-specific phrases (`"escaped lion"` ⇒ lion) and score the *phrase*, not the page.

The build took the second road and made the failure the subject. If you have the time budget,
take the first: it would let the outcome analysis (recaptured vs shot) actually work, which is
the most interesting thing this dataset could support and the page currently cannot.

## 3. Get the data

```
https://www.loc.gov/collections/chronicling-america/?q=<phrase>&fo=json&c=100&sp=<page>
```

No key. Slow — budget ~2 minutes per query. It returns `date`, `partof_title` (the paper),
`location_city`, `location_state`, `number_page`, `url` (the viewer, with the term highlighted),
`image_url` (IIIF tiles) and the `description` excerpt described above. Expect intermittent
`404`s past the last page and occasional `525`s; retry with backoff and keep going.

Use **20 phrasings**, chosen for how the period actually wrote — `"escaped from the menagerie"`
and `"lion at large"` matter as much as `"escaped from the zoo"`. De-duplicate by URL.
The legacy `chroniclingamerica.loc.gov/search/pages/results/` endpoint, which used to return full
page OCR in `ocr_eng`, is **retired and 404s**; do not build on it.

## 4. Scoring

Each phrase gets a hand-assigned **specificity** 0–1: how strongly it implies a captive animal
got out. `"escaped from the zoo"` = 0.96. `"bear at large"` = 0.22, because most bears at large
in an American newspaper are just bears. It is a judgement about language, so two pages found by
the same phrase always score the same — say so on the page.

## 5. The page

Newsprint in light, **microfilm negative in dark** — which is what these scans actually are.
Bodoni Moda for the nameplate (the didone American papers used for display), Source Serif 4 for
text, Courier Prime for OCR so machine transcription reads as machine transcription.

Three-column bench: filter rail | the wall of pages | detail panel. A PRISMA-style tally across
the top — returned, filtered, kept, tossed — with **keep/toss buttons on every record, persisted
to `localStorage`**. That screening step is the point: a broad search returns far more than you
want and a human decides, which is exactly what the subject deserves.

## 6. Verification

| Check | Expected |
|---|---|
| Unique pages from 20 phrasings | ~3,400 |
| Excerpts containing their own match phrase | ~4% |
| Date range | 1758–1963 |
| Most-searched animal by hits | lion, then bear |
| Top state by pages | District of Columbia |
| `escaped from the zoological park` | ~6 hits — genuinely rare phrasing |

If your excerpts contain the search phrase far more than ~4% of the time, you are reading a
different field than `description` — check what you are actually parsing.

## 7. Say these things on the page

- This measures **newspaper coverage, not escapes**. Peaks track digitisation, not lions.
- The OCR is bad and visibly so; that is scanning, not the printer.
- Circus and travelling-menagerie escapes are in here; the papers used the words interchangeably.
- Location is **where the paper was published**, not where the animal was.
- The excerpt under each record is almost certainly not the story. Say it plainly, every time.
