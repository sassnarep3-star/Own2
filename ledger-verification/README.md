# Free cash-prize competitions — verification ledger

A verification dashboard for the 206 listings in the upstream ledger (`karagemop466-tech/FreeMoneyApps`, commit `466f7c1`, data as of 2026-08-19). Every row links to its official page. A prize value is shown only when an official page confirms it. Otherwise the cell is blank and the row is flagged.

- **Live:** https://sassnarep3-star.github.io/Own2/ledger-verification/
- **Flagged for review:** `flagged.html` (irregularities, row flags, and the unverified ledger prize claims, clearly labelled)
- **Executive summary:** `executive-summary.html` and `EXECUTIVE_SUMMARY.md`
- **Methodology and sources:** `methodology.html`

## Layout

| Path | What it is |
|---|---|
| `tools/build.mjs` | Generates every HTML page and `data/listings.json` from the sources below. Node 22, no dependencies. |
| `tools/check.mjs` | Enforces the rules: 206 rows, official signup link on every row, blank unverified prizes, evidence links, no broken internal links. |
| `data/source/ledger-data.js` | Unmodified snapshot of the upstream ledger. |
| `data/review.json` | Verification record: official pages checked on 2026-11-01, row flags, and irregularities with links. |
| `assets/` | Stylesheet and the small script for search and filters. |

## Rebuild and check

```sh
node ledger-verification/tools/build.mjs
node ledger-verification/tools/check.mjs
```

`.github/workflows/ledger-verification.yml` runs both and fails if the committed pages differ from a fresh build.

## Limits

11 of 206 rows were checked on an official page in this pass; the other 195 are unverified. External links on unverified rows are the upstream's and are not all checked. See `methodology.html`.

Licence: none. The upstream listing data has no licence either.
