# COORDINATION — shared task board

Repo: `sassnarep3-star/Own2` · Live site (GitHub Pages, legacy build from `main` /): https://sassnarep3-star.github.io/Own2/

**Rules (from project brief):** read this file first · claim a task by writing session ID + file scope, commit and push immediately · never edit files outside your claimed scope (log a request instead) · small commits · `git pull --rebase` before every push · a claim older than 60 min with no commits may be taken over (note the handoff in the log) · shared outputs (table data, site index/nav) are changed only by the final integration task · nothing is marked verified without an official source link.

**Branch note:** this Arena session is hard-bound to branch `arena/be1d2210-own2`, so the `session-<id>/<task>` naming convention cannot be used here. All tasks below are committed on that one branch, in separate commits, with non-overlapping file scopes.

**Status legend:** unclaimed · in progress · done · needs review (published on the Flagged for Review page; does not block anything)

| ID | Task | Status | Owner session | Files touched | Claimed (UTC) |
|----|------|--------|---------------|---------------|---------------|
| T1 | Repo review: audit the source repo (karagemop466-tech/FreeMoneyApps) and its live site; list irregularities | in progress | be1d2210 | `audit/**` | 2026-11-01T13:42Z |
| T2 | Data extraction + offline integrity checks (URL syntax, domains, tiers, internal inconsistencies) | in progress | be1d2210 | `data/raw/**`, `tools/extract.js`, `tools/audit.js` | 2026-11-01T13:44Z |
| T3 | Live verification against official pages (fetch official URLs, record only what was read) | in progress | be1d2210 | `data/verification/**` | 2026-11-01T13:44Z |
| T4 | Site build (landing page, category subpages, flagged page, styles, JS) | unclaimed | — | `site-src/**` (templates only; no shared index/nav output) | — |
| T5 | Executive summary | unclaimed | — | `EXECUTIVE_SUMMARY.md` | — |
| T6 | Final integration: merge data, re-verify combined data, build site, link check, PR to `main`, merge, confirm Pages | unclaimed | — | root `index.html`, `*.html`, `data/ledger.json`, `README.md`, `COORDINATION.md` | — |

## Log
- 2026-11-01T13:42Z — be1d2210 — Created board. Claimed T1.
- 2026-11-01T13:44Z — be1d2210 — Claimed T2, T3 (same session; non-overlapping scopes). Source repo cloned read-only to /tmp (not modified). Source commit under review: 466f7c1e7a14b52b4a0d36beb84a00d68fd409b7.
