# Prize Ledger

A mobile-friendly, evidence-first dashboard for researching free-to-enter cash prize competitions.

**Live site:** https://sassnarep3-star.github.io/Own2/

## What is included

- All **206 original listings**, organized into **nine category subpages**.
- **10 event-level research additions** and **45 historical exclusion records**, kept separate.
- **31 official source pages inspected**, with short excerpts and disclosed inspection scope.
- **Six records** with official evidence for both a free-entry path and a cash award. This is not a personal-eligibility or payout guarantee.
- Three additional Metaculus event records advertise money pools but allow cash-equivalent substitution; excluded from the strict cash filter.
- Executive summary, source notebook, and **Flagged for Review** page.
- Search, category/evidence/AI filters, deadline sorting, pagination, browser-local saved lists, CSV and JSON exports.
- Server-rendered records and source links remain usable without JavaScript.

## Important honesty boundary

**This is not 216 fully verified free-cash contests.** Every original listing was structurally audited and retained. Only independently supported operational fields are populated; everything else is `null` in JSON, empty in CSV and blank in the comparison table. Most inherited external links and claims remain unverified leads. Do not interpret source inspection as full legal or eligibility verification.

The original ledger is a **secondary source**, never authority for a current prize, deadline, fee or payout. The raw snapshot preserves provenance, not truth. Review issues do not block publication.

## Run locally

Python 3.11+ and Node 22+:

```sh
npm ci
npm run build
npm test
npm run test:browser
npm run preview
```

The preview binds `0.0.0.0:4173`. Browser tests use an NPM-distributed Chromium with bundled runtime libraries rather than downloading a browser from blocked CDN hosts. `npm run test:browser` starts and stops its own temporary test server; use `BASE_URL` to point at an existing server.

The site generator itself uses only Python's standard library. `site/`, browser binaries, dependencies, screenshots and test results are excluded from Git. Static root HTML, `.nojekyll` and CSV are deliberately committed because the existing Pages configuration publishes `main:/` and the Pages settings API denied changes. No credentials, paid APIs, fonts, analytics or third-party frontend scripts are needed.

## Files and provenance

- `data/findings.json`: curated field values, official source IDs, observed excerpts and inspection notes.
- `data/ledger.json`: generated normalized inventory; unknown facts remain null.
- `research/upstream.json`: historical snapshot from `karagemop466-tech/FreeMoneyApps`, commit `466f7c1e7a14b52b4a0d36beb84a00d68fd409b7`, retrieved through the GitHub contents API. No verification claims inherited.
- `research/AUDIT.md`: generated line-by-line inventory audit and executive findings.
- `scripts/prepare_data.py`: conservative importer; never promotes historical operational claims.
- `scripts/build.py`: generates the dashboard, category subpages, summary, review queue, source notebook and exports.
- `tests/`: row-level evidence, internal-link, inventory and CSV checks; browser interaction, responsive and automated accessibility checks.
- `COORDINATION.md`: shared claims, scope, sources, verification and publication log.

## Publishing

`.github/workflows/pages.yml` validates pushes and pull requests. The existing GitHub Pages configuration publishes from **main, repository root**. The build refreshes the exact committed static root pages and export; CI checks their reproducibility. Merge only after validation passes; GitHub’s built-in Pages workflow then publishes the root files. No alternate branch or manual settings change is needed. The redundant `site/` preview directory is not committed.

## Updating evidence

Inspect an official organizer/rules page before editing a field in `data/findings.json`. Record the source URL, inspection date, supporting excerpts, and any partial-reading caveat. Rebuild, run tests, and keep unresolved details on the review page. Do not guess deadlines, eligibility, tax thresholds, expected winnings or tool permissions. Platform and event prize pools can overlap and must not be added together.
