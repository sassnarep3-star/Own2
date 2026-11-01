# Own2 — Free cash-prize competitions ledger

A verification dashboard for free-to-enter competitions that can pay real money.

- **Live site:** https://sassnarep3-star.github.io/Own2/ (GitHub Pages)
- **Flagged for review:** https://sassnarep3-star.github.io/Own2/flagged.html
- **Executive summary:** [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) and the site page.
- **Task board and logs:** [COORDINATION.md](COORDINATION.md)

## What is here

| Path | What it is |
|---|---|
| `data/source/ledger-data.js` | Unmodified snapshot of the upstream ledger (`karagemop466-tech/FreeMoneyApps`, commit `466f7c1`, data as of 2026-08-19). |
| `data/review.json` | This review's verification record: official pages checked on 2026-11-01, row flags, and repo and source irregularities. |
| `scripts/build.mjs` | Builds the static site into `_site/`. |
| `scripts/check.mjs` | Checks the built site: row coverage, the prize rule, internal links, and no placeholder strings. Exits non-zero on failure. |
| `site/assets/` | Stylesheet and the small script for search and filters. |
| `.github/workflows/pages.yml` | Builds, checks, and deploys to GitHub Pages. |

## Rules the site follows

1. A prize value is shown only when an official page confirms it (`data/review.json`). Otherwise the cell is blank and the row is flagged as unverified.
2. Ledger values are never shown as verified. Ledger notes appear only in expandable blocks labelled unverified.
3. Every row links to its official signup page.
4. Sportsbook, casino and real-money DFS contests are excluded by the source's own policy. Rows that conflict with it are flagged, not silently removed.

## Build and check locally

```bash
node scripts/build.mjs
node scripts/check.mjs
```

Node 22 or later. No dependencies.

## Verification status

11 of 206 rows were checked on an official page in this pass. The rest are unverified. See the Methodology page for the sources and limits.

## Licence

No licence is set. The upstream listing data has no licence either. Decide reuse terms before public reuse.
