# Coordination — Own2 / Free Cash Prize Competition Ledger

Shared task board for agent sessions working on this repo.

**Session:** `arena-36a6db9e-own2` — branch `arena/36a6db9e-own2` (only active session; claims below are all owned by this session).

## Ground rules
- Claim a task by writing your session ID and file scope, then commit and push that claim immediately.
- Never start a task another session has claimed. Keep scopes non-overlapping.
- If a task requires changing a file owned by another session, log the request here instead of editing it.
- Make small, frequent commits; run `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding the other session's work, log what happened here.
- When a task is finished: record sources, verification performed, and irregularities here, then mark it done.
- Never mark anything verified without checking it against an official source; link that source.
- Shared outputs (table data, site index/navigation) are changed only by the final integration session, which merges branches, re-verifies line by line, confirms the build has no broken links, and publishes to GitHub Pages.

## Task board

| # | Task | File scope | Status | Owner | Sources verified / notes |
|---|------|------------|--------|-------|--------------------------|
| 1 | Analyze reference site (Free Money & Contest Ledger) and extract structured ledger data | `data/listings.json` (from `karagemop466-tech/FreeMoneyApps` `assets/data.js`) | done | arena-36a6db9e-own2 | Source: https://api.github.com/repos/karagemop466-tech/FreeMoneyApps/contents/assets/data.js — 206 listings, reviewed 2026-08-19 |
| 2 | Executive summary | `EXECUTIVE_SUMMARY.md`, `executive-summary.html` | in progress | arena-36a6db9e-own2 | |
| 3 | Site build — clean landing page (dashboard) | `index.html`, `assets/style.css` | unclaimed | arena-36a6db9e-own2 | |
| 4 | Site build — category subpages with entry tables | `categories/*.html` | unclaimed | arena-36a6db9e-own2 | |
| 5 | Site build — Flagged for Review page (unverified / caution / ended / irregularities) | `flagged.html` | unclaimed | arena-36a6db9e-own2 | |
| 6 | Verification pass — every table row has an official source; unverified left blank and flagged | all site pages + `data/listings.json` annotations | unclaimed | arena-36a6db9e-own2 | 12 listings have no official source (see flagged list) |
| 7 | GitHub Pages: build check, broken-link check, publish, PR to main, merge | repo settings + PR | unclaimed | arena-36a6db9e-own2 | |

## Flags & irregularities (pending review on site `flagged.html`)

- 12 listings have NO official source (affiliate/forum only): `thelines-survivor`, `fantasy-arena`, `fplhub`, `bona-fide`, `olka`, `fplmanager-india`, `fplstore`, `pitchbooking`, `roboforex-demo`, `fbs-pro-demo`, `npbfx-demo`, `tff-fantezi-lig` → flagged unverified
- 11 caution entries: `football-mad`, `fantasy-arena`, `fplhub`, `bona-fide`, `olka`, `fplmanager-india`, `fplstore`, `pitchbooking`, `streak-for-cash`, `premiership-rugby-fantasy`, `formula-e-predictor`
- 27 ended / out-of-season entries (not currently playable)
- 5 mixed entries (free rooms exist, but real USD requires an entry fee): `solitaire-cash`, `bingo-cash`, `skillz`, `pocket7`, `vocal`
- Ledger data last checked 2026-08-19; prizes and eligibility can change at any time
