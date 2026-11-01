# PrizeDesk

Evidence-first, mobile-friendly competition research dashboard. No framework, dependencies, accounts, trackers or affiliate links.

- Live site: https://sassnarep3-star.github.io/Own2/
- Executive summary: `summary.html`
- Uncertainties: `review.html`
- 206 inherited leads + 2 event records; no fully qualified free-entry cash contest is claimed.

## Reproduce

```sh
python scripts/build.py
python scripts/test.py
python -m http.server 8000 --bind 0.0.0.0
```

Edit `data/contests.json` and `scripts/build.py`, then regenerate. Generated HTML includes the full tables so content works without JavaScript; JavaScript adds filtering. Category pages are real static subpages. Blank cells are intentionally unverified. Evidence dates apply only to the fields documented, not to every claim about a platform.

`data/upstream.json` preserves the supplied ledger's assertions for traceability, not endorsement. Upstream snapshot: https://github.com/karagemop466-tech/FreeMoneyApps/tree/466f7c1e7a14b52b4a0d36beb84a00d68fd409b7 . External URLs on unverified rows are inherited destinations and have not all been authenticated or checked for availability. Internal links are tested. This is not a complete external-link or rules audit.

GitHub Pages serves the root of `main` (existing repository configuration). No third-party runtime assets required. See COORDINATION.md for ownership, checks, PR and deployment results.


## Additional official-source findings — 1 November 2026

- The starting repository contained only a placeholder README. The [external Free Money & Contest Ledger](https://karagemop466-tech.github.io/FreeMoneyApps/) contains **206** listings across nine categories, but its self-reported “189 true free paths” is **not** a verified count. Its records mix contests, discovery directories, pool tools, non-cash prizes, pay-to-enter products, and old seasons. We imported **all 206 as unverified research leads**, preserving original-record links and operator/cited URLs but blanking unconfirmed prize, fee, deadline, and eligibility fields.
- **One current opportunity meets the documented free-entry cash-prize standard:** [ARC Prize 2026 Paper Track](https://www.kaggle.com/competitions/arc-prize-2026-paper-track/rules). Its official rules explicitly say “NO PURCHASE NECESSARY” (§2.4) and specify **$75,000** in guaranteed awards (§1.5); the [overview](https://www.kaggle.com/competitions/arc-prize-2026-paper-track) gives **9 November 2026, 23:59 UTC** as the deadline. Entry requires a prior submission to ARC-AGI-2 or ARC-AGI-3 and a public writeup/notebook. A possible $375,000 bonus is **conditional**, not counted in the guaranteed prize figure. For agent-assisted work, review competition-specific code-sharing, originality, and eligibility provisions before participating.
- **One technically promising but incomplete lead:** the [GEMS Prize challenge](https://www.drivendata.org/competitions/306/competition-doe-gems/) specifies **$300,000** in cash awards and a **3 December 2026, 23:59 UTC** deadline. [Official rules](https://docs.nlr.gov/docs/fy26osti/96647.pdf) §§1.1, 1.3 and 3.2 describe prize structure, U.S. eligibility and permitted generative AI use **with disclosure**. No explicit entry-fee statement was found, so it is **not** labeled confirmed free. Its eligibility makes it a potentially relevant project for a U.S.-based technical team, subject to the full rules.
- **Important correction:** the [Premier League’s Second Chance article](https://www.premierleague.com/en/news/4220308/the-second-chance-league-is-live-in-fantasy) lists merchandise, not a cash award; the linked 2025/26 season is not a current cash contest. The source ledger’s [Skillz terms URL](https://www.skillz.com/terms-of-service/) returned a 404 page on review. Several FPL mini-league entries cite third-party roundups rather than league-specific official rules. See the [Flagged for Review page](https://sassnarep3-star.github.io/Own2/flagged/) for all records and limitations.

**Decision rule:** prioritize a competition only after its official rules confirm a no-purchase cash path, an open deadline, eligibility, and acceptable AI/tool use. Prize pools measure maximum available awards, not expected value; no success rate or ROI can be inferred from available evidence. Recheck all rules immediately before entering.


## Two complementary views

The existing [PrizeDesk dashboard](index.html) is retained and now incorporates the independently verified Paper Track row. The new [focused shortlist](explore.html) offers a simpler mobile-first view with a separate category research backlog. Both views identify unchecked leads and point to the [Flagged for Review](flagged/index.html) inventory.



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

Earlier views remain reproducible using `python scripts/build.py`, `python scripts/test.py`, `node scripts/check.cjs`, and the independent audit build/tests. No existing source data, field evidence or audit history was replaced by this view.

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
