# Free Cash Contest Dashboard

Mobile-friendly GitHub Pages dashboard of free-to-enter cash prize competitions.

**Live site:** https://sassnarep3-star.github.io/Own2/dashboard/

This folder is one of several independent sites in this repository (the other sessions' dashboards live at the repository root, `/flagged/` and `/audits/2026-11-01/`). Nothing outside `dashboard/` is modified by this site. All commands below run from this folder.

Rule: **verified or blank.** Every table row links to an official source. A prize, eligibility, entry-type, date or status value appears only if it was read on an official page on 2026-11-01; otherwise it is blank and marked *Unverified*. Nothing is inferred.

| Page | Purpose |
|---|---|
| `index.html` | Landing page: key numbers, best bets, categories |
| `top-picks.html` | Verified, open, cash-prize competitions with analysis |
| `cat-*.html`, `categories.html` | One table per category |
| `all.html` | All 206 entries with search and filters |
| `summary.html` / `EXECUTIVE_SUMMARY.md` | Executive summary |
| `flagged.html` | **Flagged for Review**: irregularities, discrepancies, unverified items, with source links |
| `methodology.html` | What was and was not checked |

## Data
- `data/ledger.json`, `data/ledger.csv` — merged dataset (original claims kept separate from confirmed values)
- `data/raw/source-ledger.json` — unmodified extract of the original ledger (source commit in `data/raw/SOURCE_COMMIT.txt`)
- `data/verification/verified.json` — what was read on which official page
- `data/raw/offline-findings.json` — offline consistency audit
- `audit/SOURCE_REPO_REVIEW.md` — review of the source repository

## Rebuild
```
node tools/build.js      # regenerates all html + data/ledger.*
node tools/linkcheck.js  # internal links, anchors, every row has an official link
node tools/linkcheck-external.js > data/external-linkcheck.json   # needs open internet
```
`tools/extract.js` and `tools/audit.js` regenerate the raw data from a clone of the source repo. No dependencies beyond Node 18+.

Project coordination: see `COORDINATION.md`.
