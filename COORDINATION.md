# Coordination board — sassnarep3-star/Own2

Shared task board for all agent sessions working on this repo. Read before starting; claim before editing; log every handoff.

**Rules in force:** claim → commit + push the claim immediately → `git pull --rebase` before every push → edit only claimed files → log sources, verification and irregularities here → mark `done` or `needs review`.

**Branch note (session `205d508d`):** the session branch is fixed by Arena as `arena/205d508d-own2`. The branch naming pattern `session-<id>/<task>` from the task brief is therefore not used; all work for every task in this session lives on `arena/205d508d-own2` and is tracked by the task table below instead.

## Task table

| Task | Status | Owner (session) | Files touched | Notes |
|---|---|---|---|---|
| T1 Repo review and irregularity log | in progress | 205d508d | `COORDINATION.md`, `data/review.json` | Repo review and source-repo review (see Log). |
| T2 Snapshot and normalize source ledger | in progress | 205d508d | `data/source/*` | Snapshot of upstream `assets/data.js` (206 listings). |
| T3 Line-by-line verification against official sources | in progress | 205d508d | `data/review.json` | Partial: 11 rows checked on official pages; the rest are unverified and flagged. |
| T4 Site build (landing, category pages, table, flagged, executive summary) | in progress | 205d508d | `scripts/build.mjs`, `scripts/check.mjs`, `site/**` | Static site generated to `_site/`. |
| T5 GitHub Pages deploy workflow | in progress | 205d508d | `.github/workflows/pages.yml`, `.gitignore`, `README.md` | |
| T6 Integration: combined verification, build, link check, PR to main, merge, Pages check | unclaimed → claimed by 205d508d | 205d508d | all | Final integration step. Only the integration session edits shared outputs (table data, index, nav). |

Status values: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page; does not block).

## Claims

- 2026-11-01 · session `205d508d` · claimed T1–T6 (single session active on this repo; no other session has written to the board).

## Log

### 2026-11-01 · session 205d508d · T1 repo review

- Repo state at start: `main` and `arena/205d508d-own2` both at `f0b01b8 Initial commit`; the only file was `README.md` (`# Own2`). No data, no site, no license, no `COORDINATION.md` existed before this session.
- Irregularity R1 (low): repo has no `LICENSE` file, and the upstream source has none either. Reuse rights for the upstream data are unconfirmed (see Flagged page).

### 2026-11-01 · session 205d508d · T2 source snapshot

- Source: https://github.com/karagemop466-tech/FreeMoneyApps (commit `466f7c1e7a14b52b4a0d36beb84a00d68fd409b7`, 2026-08-19). Snapshot stored as `data/source/ledger-data.js`, unmodified.
- Source counts reconciled against the live page (https://karagemop466-tech.github.io/FreeMoneyApps/): 206 listings ✔, 189 "true free paths" ✔ (`freePath: full`), 62 iOS options ✔ (platform includes iOS and status ≠ ended = 62; the live page does not document this definition), 60 "added this pass" ✔.

### 2026-11-01 · session 205d508d · T3 verification (partial, honest scope)

- Fetched official pages on 2026-11-01 for 11 rows (ids below). All other 195 rows are **Unverified**: prize values are left blank on the site, as the brief requires, and each is flagged.
- Checked: `espn-pickem` ✔ verified · `espn-cfb` ✔ verified · `arcprize` ✔ verified · `mlb-beat-the-streak` ✔ prize verified, status conflict · `metaculus` ◐ partial · `cbs-pro-pickem` ◐ partial (free entry and dates verified; prize amounts on later rules pages not read) · `devpost` ◐ partial · `kaggle` ✖ conflict (range understated) · `checkmate-gaming` ✖ conflict (prize range) · `draft-pro` ✖ conflict (status) · `dirty-dozen` ✖ broken link.
- Full per-row evidence: `data/review.json`.

### 2026-11-01 · session 205d508d · T4/T5 build

- Build: `node scripts/build.mjs` → `_site/`. Check: `node scripts/check.mjs` (row counts, internal links, unverified prize values blank, every row has an official-link field).
- Deploy: `.github/workflows/pages.yml` (build → check → upload-pages-artifact → deploy-pages).
