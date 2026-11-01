# Competition Desk

A mobile-friendly, source-first research directory for free-to-enter cash-prize competitions.

**Live:** https://sassnarep3-star.github.io/Own2/  
**Executive summary:** [docs/EXECUTIVE_SUMMARY.md](docs/EXECUTIVE_SUMMARY.md)

## Run

Python 3.11+ builds the static site without third-party runtime dependencies:

```sh
python3 scripts/build.py
python3 -m http.server 8000 --bind 0.0.0.0 --directory _site
```

For browser checks: `npm ci`, `npx playwright install chromium`, then `npm test`.

## Data and evidence

- `data/competitions.json`: 206 inherited entries plus 3 official event findings. Only inspected official claims populate factual fields. Every populated field carries a citation and excerpt.
- `data/imported-ledger.json`: original claims, explicitly **unverified**, preserved for completeness and traceability. Not used as factual display values.
- `docs/import-provenance.json`: upstream commit, source path and retrieval date.
- `docs/source-checks.json`: dated automated reachability evidence for inherited operator, rules and terms URLs. HTTP success is **not** verification. See the Flagged for Review page.
- `scripts/audit_sources.py`: repeatable concurrent source checker. GitHub Actions can access operator sites that this sandbox cannot.
- `COORDINATION.md`: claims, limitations, tests and publication record.

All 209 entries have unresolved requirements. Three rows have explicit free-entry and cash evidence (one platform overlaps one event); none constitutes personal eligibility clearance. No estimated earnings, win probability, payout method or AI permission is invented. One inherited press-release-only row has no established official operator source and is explicitly flagged instead of inventing one.

## Build and publish

`npm run build` writes `_site/` (ignored). `scripts/validate.py` checks row coverage, evidence integrity and local links. GitHub Actions runs data/build checks plus desktop/mobile browser tests on pull requests. The existing GitHub Pages main/root deployment publishes the checked-in static snapshot after merge. `python scripts/snapshot.py` refreshes that snapshot from `_site/`; CI checks it for drift. The main workflow runs public-URL smoke checks while GitHub’s native Pages job publishes it.

No external fonts, analytics, remote frontend libraries or backend are required. Saved items use browser local storage only. CSV export leaves unknown values empty. The website makes no contest submissions or deposits.
