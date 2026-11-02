# PrizeDesk — free-to-enter cash competitions, verified line by line

A static, dependency-free dashboard built from a 206-row source ledger plus three event-level entries.
Every published value is quoted from the operator's own page; everything else is blank and flagged.

- **Live site:** https://sassnarep3-star.github.io/Own2/
- **Executive summary:** [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md) · [`summary.html`](summary.html)
- **Flagged for review:** [`review.html`](review.html)
- **Evidence log (quote + URL per field):** [`data/EVIDENCE.md`](data/EVIDENCE.md)
- **Independent audit reports:** [`audits/index.html`](audits/index.html) links the separate findings and review flags. The reports are limited spot checks, not a full re-verification of all inherited listings.

## What is on the site

| Page | Purpose |
|---|---|
| `index.html` | Dashboard: counts, shortlist, confirmed deadlines, category entry points |
| `contests.html` | All 209 competitions with search, category/verification/free/cash filters, sorting, per-row evidence |
| `sports.html` `tech.html` `creative.html` `forecasting.html` `skill.html` `market.html` `pools.html` `trivia.html` `directory.html` | Category pages |
| `summary.html` | Executive summary and method |
| `review.html` | Every unresolved, contradicted or unsourced item, with links |
| `audits/index.html` | Index of five separate official-source audits and each report's Flagged for Review page |

Parallel sessions' material is preserved, not replaced: the independent 13-lead audit lives at
`audits/2026-11-01/`, the independent report index at `audits/index.html` (linking separate 1–2 November
reports and review flags), the alternate shortlist at `explore.html` + `category/` + `flagged/`, a third standalone
dashboard at `dashboard/`, the first dashboard's builder at `audits/legacy-build/`,
the Competition Desk at `competition-desk/`, the Prize Ledger dashboard at `ledger-ebd10b79/`,
the ledger verification subsite at `ledger-verification/`, and a verified-ledger table site at
`ledger-4c1d6bb4/` (session 4c1d6bb4: 206-row table dashboard with CI link checks and spot-check
blanking — see `ledger-4c1d6bb4/verification-log.md`).

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

- Current root checks report 34 entries with recorded evidence (supporting 90 published field values with quotes and official URLs); 176 of 209 rows remain unverified and blank. An evidence record is not the same as a fully verified opportunity.
- "Free entry confirmed" means the operator states no fee is required. It does not mean the competition is
  free to *win* — your time, compute and travel are real costs.
- Prize pools are not expected value. No win probability, hourly rate or earnings ranking is asserted.
- Only pages actually opened were checked for availability; unopened links may be broken.
- Rules change. Every row shows the date it was read; re-check before entering.
- Upstream snapshot: <https://github.com/karagemop466-tech/FreeMoneyApps/commit/466f7c1e7a14b52b4a0d36beb84a00d68fd409b7>

GitHub Pages serves the root of `main` (legacy build, `.nojekyll` present). No third-party runtime assets,
no trackers, no affiliate links, no accounts created on your behalf. Session ownership, checks, PR and
deployment results are recorded in [`COORDINATION.md`](COORDINATION.md).


---

## Additional complementary view: Prize Ledger dashboard

This additional [Prize Ledger dashboard](ledger-ebd10b79/index.html) retains the earlier root dashboard, [focused shortlist](explore.html) and [independent audit](audits/2026-11-01/index.html). Its counts and evidence scope are independent, not an aggregate of all views.

**Live:** https://sassnarep3-star.github.io/Own2/ledger-ebd10b79/

- 216 records: all 206 source listings plus 10 event-level additions, in nine category subpages.
- 31 official pages inspected; source excerpts and partial-reading disclosures in `data/findings.json` and the dashboard source notebook.
- Six records with official free-entry and cash-award evidence. Personal eligibility, payout and other conditions still apply. Three Metaculus events allow cash-equivalent substitution and are excluded from the strict cash filter.
- Most inherited claims and external URLs remain unverified leads, with unsupported operational values blank. **This is not a complete all-206 official verification or external-link audit.** All caution-bearing rows are on the dashboard's Flagged for Review page.
- Search, evidence/category/AI filters, deadline sorting, browser-local saved lists, pagination, CSV/JSON export and an executive summary.

### Build and test this view

```sh
npm ci
npm run build
npm test
npm run test:browser
npm run preview
```

Preview listens on `0.0.0.0:4173`; this view is at `/ledger-ebd10b79/`. The browser suite starts/stops its own temporary test server; `BASE_URL` can point at an existing dashboard URL.

`npm run build` runs `scripts/build-dashboard.py`, not the earlier root generator. It refreshes committed `ledger-ebd10b79/` static pages and exports, `data/ledger.json`, and `research/AUDIT.md`. The preview-only combined `site/`, dependencies, runtime libraries and test screenshots are ignored. Dashboard static output must be committed because existing Pages publishes `main:/` and the settings API denied changes; no alternate branch or manual setting change is required.

Earlier views remain reproducible using `python scripts/build_site.py`, `python scripts/check_site.py`, `node scripts/check.cjs`, and the independent audit build/tests. No existing source data, field evidence or audit history was replaced by this view.

### Evidence files

- `data/findings.json`: official source URLs, checked excerpts and curated field values.
- `data/ledger.json` / `data/ledger.csv`: normalized inventory; unsupported values are null/empty.
- `research/upstream.json`: historical source snapshot, not official authority for operational claims.
- `research/AUDIT.md`: line-by-line inventory and source scope.
- `scripts/prepare_data.py`: conservative importer; never promotes inherited facts.
- `scripts/build-dashboard.py`: this dashboard generator.
- `tests/`: evidence/provenance/null/internal-link checks and Playwright/axe browser tests.
- `COORDINATION.md`: preserved histories, integration scope, conflicts, PRs and deployment records.

Do not infer a prize, no-purchase path, date, eligibility, AI permission, tax threshold or expected earnings from missing evidence. Source pages and rules may change after the 1 November 2026 research snapshot.
