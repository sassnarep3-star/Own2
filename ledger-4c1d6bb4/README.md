# Free Contest Ledger (Own2)

**Live site:** https://sassnarep3-star.github.io/Own2/

A verified, mobile-friendly dashboard of **206 free-to-enter competitions that
can pay real cash** — skill games, trivia, fantasy & picks, creative,
forecasting, markets, tech, directories and pool tools — across 9 category
pages, with per-row official source links, an analysis page, and a
[Flagged for Review](https://sassnarep3-star.github.io/Own2/flagged.html) page
for everything that could not be confirmed from an official source.

## Verification policy (enforced in code)

1. **Every table row carries a link to an official (operator-owned) source.**
2. **If a value cannot be confirmed from an official source it is rendered
   blank and flagged** — never inferred or filled in.
3. Listings with no `official`-tier source are entirely blanked and published
   on the Flagged page with their non-official links labelled as such.
4. An automated link check runs in CI on every push and its broken-link
   report is published on the Flagged page.

## Build & verify locally

```bash
node scripts/check-data.mjs      # structural audit -> reports/data-audit.{json,md}
node scripts/build-pages.mjs     # regenerate all 14 pages + internal link check
node scripts/check-links.mjs     # full URL sweep (needs internet; runs in CI)
```

## Layout

| Path | Purpose |
|---|---|
| `index.html` | Landing dashboard: stats, transparent top-15, category cards |
| `<category>.html` | 9 category pages, table format, search/filters (mobile card layout) |
| `analysis.html` | Distributions, scoring formula, policy exclusions, patterns |
| `flagged.html` | Unverified rows, spot-check failures, broken links |
| `executive-summary.html` / `EXECUTIVE_SUMMARY.md` | Project summary |
| `assets/data.js` | Vendored ledger (provenance header; source of truth) |
| `scripts/` | Data audit, page builder, link checker |
| `reports/` | Audit + link-check + spot-check artifacts |
| `verification-log.md` | What was verified, how, with links |
| `COORDINATION.md` | Multi-session task board, PR/deploy record |

## Data provenance

Vendored from [`karagemop466-tech/FreeMoneyApps`](https://github.com/karagemop466-tech/FreeMoneyApps)
(`assets/data.js`, audit pass S, reviewed 2026-08-19) on 2026-11-01. Listing
content belongs to that upstream audit; this repo owns the presentation,
verification pipeline and flagging. See `verification-log.md` for the spot
checks performed against official operator pages.

## Disclaimer

Independent research compilation. Not affiliated with any listed operator.
Contest laws vary by jurisdiction — play only where legal. 18+/21+ where
required. US tax forms apply at $600+. Always open the official rules before
entering.
