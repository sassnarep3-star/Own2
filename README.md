# PrizeDesk — free-to-enter cash competitions, verified line by line

A static, dependency-free dashboard built from a 206-row competition ledger. Every published value is
quoted from the operator's own page; everything else is blank and flagged.

- **Live site:** https://sassnarep3-star.github.io/Own2/
- **Executive summary:** [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md) · [`summary.html`](summary.html)
- **Flagged for review:** [`review.html`](review.html)
- **Evidence log (quote + URL per field):** [`data/EVIDENCE.md`](data/EVIDENCE.md)

## What is on the site

| Page | Purpose |
|---|---|
| `index.html` | Dashboard: counts, shortlist, confirmed deadlines, category entry points |
| `contests.html` | All 209 competitions with search, category/verification/free/cash filters, sorting, per-row evidence |
| `sports.html` `tech.html` `creative.html` `forecasting.html` `skill.html` `market.html` `pools.html` `trivia.html` `directory.html` | Category pages |
| `summary.html` | Executive summary and method |
| `review.html` | Every unresolved, contradicted or unsourced item, with links |

Mobile-first: below 820px the tables become cards, with the same evidence available per row.
Content is fully rendered in the HTML, so the site works without JavaScript; `app.js` only adds
filtering, sorting and the evidence toggle.

## Data model

```
data/upstream.json     the supplied ledger, unchanged (206 listings + 45 removed records)
data/evidence/*.json   one file per verified entry: field status, verbatim quote, source URL, check date, flags
data/categories.json   the nine categories and their evidence-based summary
data/contests.json     generated: the published dataset (values + evidence + flags + ledger claims)
data/EVIDENCE.md       generated: human-readable evidence log
```

`python scripts/build_site.py` merges the ledger with the evidence files and writes every page, the dataset
and the evidence log. `python scripts/check_site.py` enforces the rules below and fails the build if any is
broken.

### Publication rules enforced by the checks

1. A value is published only if an evidence record carries a verbatim quote **and** an http(s) URL.
2. A row labelled *unverified* publishes no values at all.
3. A row with no official operator source is automatically flagged.
4. Every upstream listing is retained; ids are unique; rebuilding is deterministic.
5. All local links resolve, every page has charset/viewport/lang, and category counts match the dataset.

## Reproduce locally

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
python3 -m http.server 8000 --bind 0.0.0.0     # http://localhost:8000
```

CI (`.github/workflows/validate.yml`) rebuilds the site, fails if the committed pages are stale, then runs
the checks.

## Honest limits

- 191 of 209 rows are inherited leads that could not be verified in this pass. They keep their link and are
  labelled unverified; no value from them is published.
- "Free entry confirmed" means the operator states no fee is required. It does not mean the competition is
  free to *win* — your time, compute and travel are real costs.
- Prize pools are not expected value. No win probability, hourly rate or earnings ranking is asserted.
- Only pages actually opened were checked for availability; unopened links may be broken.
- Rules change. Every row shows the date it was read; re-check before entering.
- Upstream snapshot: <https://github.com/karagemop466-tech/FreeMoneyApps/commit/466f7c1e7a14b52b4a0d36beb84a00d68fd409b7>

GitHub Pages serves the root of `main` (legacy build, `.nojekyll` present). No third-party runtime assets,
no trackers, no affiliate links, no accounts created on your behalf. Session ownership, checks, PR and
deployment results are recorded in [`COORDINATION.md`](COORDINATION.md).
