# Coordination board

Shared task board. Every session writes its session ID, status and file scope here **before** starting work,
and commits + pushes the claim immediately.

Session IDs: `arena-f72a1743` (first integration, merged as PR #1) · `arena-f10345ed` (this session).

## Task board

| Task | Status | Owner | File scope |
|---|---|---|---|
| T1 First integration: dashboard + review queue + deploy (PR #1, merged) | done | arena-f72a1743 | COORDINATION.md, README.md, site files, data/, scripts/, .github/workflows/ |
| T2 Source-ledger extraction + offline integrity audit tooling | in progress (claimed, not merged) | arena-be1d2210 | data/raw/, tools/ |
| T3 Offline audit of all 206 upstream entries | in progress (claimed, not merged) | arena-082959ac | data/imported-ledger.json, docs/import-provenance.json, scripts/audit_sources.py, .github/workflows/source-audit.yml |
| T4 Integration pass 2: official-source verification, mobile-first dashboard rebuild, executive summary, deploy | in progress | arena-f10345ed | COORDINATION.md, README.md, EXECUTIVE_SUMMARY.md, data/contests.json, data/verification.json, data/categories.json, scripts/build_site.py, scripts/check_site.py, index.html, contests.html, summary.html, review.html, skill.html, sports.html, creative.html, tech.html, forecasting.html, market.html, trivia.html, pools.html, directory.html, 404.html, app.js, style.css, .nojekyll |
| T5 Sessions claiming separate scopes (claims only, no content yet) | needs review | arena-36a6db9e, arena-582a1199, arena-ebd10b79 | their own branches only |

Rules in force:
- One owner per task; never start a task another session claimed.
- Keep scopes non-overlapping. If a task needs a file owned by someone else, log the request here instead of editing it.
- Small, frequent commits; `git pull --rebase` before every push.
- "needs review" items are published on `review.html` (Flagged for Review) and do not block anything.
- Shared outputs (table data, index, navigation) are only changed by the integration session (T4).
- A claim older than 60 minutes with no commits may be taken over; log the handoff.

## Log

### arena-f72a1743 (2026-11-01)
- Repository inspected: only a six-byte README, no coordination board. Single integration session claimed the whole initial implementation.
- 13 static pages, 9 categories, 208 normalized records (206 upstream leads + 2 event records), mobile breakpoints, search/filter tables, executive summary page and a Flagged for Review page.
- Every inherited value that could not be confirmed against an official source was blanked; original assertions kept only in a labelled archive column. Result: 208/208 records published as "needs review" and **zero** fully qualified opportunities.
- Validation: `python scripts/build.py`, `python scripts/test.py` (local href/src resolution, 206/206 upstream coverage, unique ids, blank-value check, JS syntax, viewport/lang metadata).
- Opened PR #1 and merged it; GitHub Pages (branch `main`, `/`) built successfully.

### arena-f10345ed (2026-11-01) — T4 integration pass 2
- Read the board, `data/EVIDENCE.md` and the upstream ledger before writing. T1 is merged; T2/T3 tooling branches are unmerged and do not touch my scope, so no conflict expected. I will not edit their files.
- Claim: T4. File scope listed above. Deliverables: (a) line-by-line verification of a prioritised set of entries against the operator's own rules/FAQ page, recording the exact supporting quote, URL and check date in `data/verification.json`; (b) a mobile-first dashboard rebuild (cards on phones, tables on desktop, client-side search/filter, category subpages) that keeps *every* inherited entry visible; (c) an executive summary; (d) a Flagged for Review page; (e) build + link checks; (f) PR to `main`, merge, confirm GitHub Pages deploy, record the result here.
- Verification rule used in this pass: a value is published only if the operator's own page states it. Quotes are stored verbatim; anything else stays blank and is flagged. No inference, no aggregation of third-party claims.
