# COORDINATION.md — shared task board

**Repo:** `sassnarep3-star/Own2`
**Purpose:** Collect, organize, and analyze free-to-enter cash-prize competitions; publish a verified, mobile-friendly GitHub Pages site.

## How sessions work here

- Each session has a session ID and works only on its claimed file scope.
- **Branch note:** this environment pins each Arena session to its own branch and forbids creating extra branches, so branch names of the form `session-<id>/<task>` are not used. Instead, file scopes below are non-overlapping; sessions must not edit files owned by another session. Request cross-scope changes by appending to the **Requests** log instead of editing.
- Claim a task by writing your session ID and file scope below, then commit and push the claim **before** starting.
- Status values: `unclaimed` | `in progress` | `done` | `needs review` (needs review = published on the Flagged for Review page; does not block anything).
- Small, frequent commits. `git pull --rebase` before every push. Log merge conflicts here and resolve without discarding others' work.
- When a task is done: record sources, verification performed, and irregularities below, and mark it `done`.
- If a session crashes or its claim is >60 minutes old with no commits, any other session may take over and log the handoff.
- **Never mark anything verified without linking the official source used.**

## Sessions

| Session ID | Branch | Status |
|---|---|---|
| `4c1d6bb4` | `arena/4c1d6bb4-own2` | active |

## Task board

| ID | Task | Status | Session | File scope | Notes |
|---|---|---|---|---|---|
| T1 | Analyze reference site `karagemop466-tech/FreeMoneyApps` (structure, data model, issues) | done | `4c1d6bb4` | none (read-only) | Findings logged below |
| T2 | Establish this coordination board | done | `4c1d6bb4` | `COORDINATION.md` | |
| T3 | Vendor + normalize ledger data (206 listings), flag rows without official sources | in progress | `4c1d6bb4` | `assets/data.js`, `scripts/build-pages.mjs`, `scripts/check-data.mjs` | |
| T4 | Build site: landing/dashboard + 9 category subpages in table format, responsive/mobile-friendly | in progress | `4c1d6bb4` | `index.html`, category `*.html` pages, `assets/css/style.css`, `assets/js/app.js` | |
| T5 | Analysis & findings page (distributions, best-opportunity ranking, patterns) | in progress | `4c1d6bb4` | `analysis.html` | |
| T6 | Flagged for Review page (all unverified/irregular items with source links) | in progress | `4c1d6bb4` | `flagged.html`, `scripts/check-data.mjs` | |
| T7 | Executive summary (repo doc + site page) | in progress | `4c1d6bb4` | `EXECUTIVE_SUMMARY.md`, `executive-summary.html` | |
| T8 | Link verification: CI workflow checking every URL in data + pages; fix or flag broken links | in progress | `4c1d6bb4` | `.github/workflows/linkcheck.yml`, `scripts/check-links.mjs` | Report artifact + job log |
| T9 | Spot verification of featured/top entries against official rules pages (manual fetch) | in progress | `4c1d6bb4` | `verification-log.md` | |
| T10 | Integration: re-verify combined data line by line, confirm no broken links, PR → main, merge, confirm Pages deploy | in progress | `4c1d6bb4` | `README.md`, `COORDINATION.md` (integration sections) | PR + deploy record below |
| T11 | Post-integration independent audit pass (available for a parallel session) | unclaimed | — | `verification-log.md` (append-only) | Parallel sessions: claim before starting |

## Requests (cross-scope change requests)

_None._

## Log

- `4c1d6bb4` 2026-11-01 — T1: cloned reference repo `karagemop466-tech/FreeMoneyApps` (codeload tarball) and read `assets/data.js` (`window.LEDGER`, 206 listings, 9 types, reviewed 2026-08-19). Issues found in reference site: single-page 206-card scroll (poor mobile UX), no search/filter, deliberate "no filters" stance, one giant list mixing categories, 12 listings lack any `official`-tier source, 27 entries ended, 45 entries previously removed by policy.
- `4c1d6bb4` 2026-11-01 — T2: created this board; claimed T1–T10 (tightly coupled single-site build; this session owns the whole critical path). T11 left unclaimed for a possible parallel audit session.

## Sources & verification records

- Reference dataset: <https://github.com/karagemop466-tech/FreeMoneyApps> (repo raw source of the 206-listing ledger; live site <https://karagemop466-tech.github.io/FreeMoneyApps/>).
- Each listing's own `sources[]` (tier `official`) is the per-row source shown in site tables — URLs recorded in `assets/data.js`.
- Link verification: GitHub Actions run of `scripts/check-links.mjs` (see `verification-log.md` for run URL and results).
- Spot checks: `verification-log.md` (T9).

## Irregularities flagged

1. **12 listings lack an official-tier source** (only affiliate/forum): `thelines-survivor`, `fantasy-arena`, `fplhub`, `bona-fide`, `olka`, `fplmanager-india`, `fplstore`, `pitchbooking`, `roboforex-demo`, `fbs-pro-demo`, `npbfx-demo`, `tff-fantezi-lig` — prize values blanked and flagged on `flagged.html`.
2. **45 entries removed by reference-site policy** (sweepstakes, casinos, gambling-operator promos, dead apps) — documented on `analysis.html` / `flagged.html` as exclusions, not carried into tables.
3. **27 listings marked ended/out-of-season** — kept in tables with status badge; prizes not current.
4. Link-check failures: to be recorded in `verification-log.md` after T8 runs (each will either be fixed with a confirmed official URL or published on `flagged.html`).

## PR & deploy record

- PR: _pending_
- Merge: _pending_
- GitHub Pages: <https://sassnarep3-star.github.io/Own2/> — deploy pending merge.
