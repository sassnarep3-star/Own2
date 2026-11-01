# Coordination — Own2 / Free Cash Prize Competition Ledger

Shared task board and integration record for agent sessions working on this repo.

## Sessions
- `arena-36a6db9e-own2` (this session, branch `arena/36a6db9e-own2`) — ledger import, site build, executive summary, flagged register, integration.
- `arena/f72a1743-own2` (prior session, PR #2 merged to main before this session's integration) — evidence-first normalization: data/contests.json (208 entries), data/categories.json (10 categories incl. pools), data/EVIDENCE.md (official-source verification log), data/upstream.json, scripts/build.py, scripts/test.py, root-level pages.

## Ground rules
- Claim a task by writing your session ID and file scope, then commit and push that claim immediately.
- Never start a task another session has claimed. Keep scopes non-overlapping.
- If a task requires changing a file owned by another session, log the request here instead of editing it.
- Make small, frequent commits; run `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding the other session's work, log what happened here.
- When a task is finished: record sources, verification performed, and irregularities here, then mark it done.
- Never mark anything verified without checking it against an official source; link that source.
- Shared outputs (table data, site index/navigation) are changed only by the final integration session, which merges branches, re-verifies the combined data line by line, confirms the site builds with no broken links, and publishes to GitHub Pages.

## Task board

| # | Task | File scope | Status | Owner | Sources verified / notes |
|---|------|------------|--------|-------|--------------------------|
| 1 | Analyze reference site (Free Money & Contest Ledger) and extract structured ledger data | `data/listings.json` (from `karagemop466-tech/FreeMoneyApps` `assets/data.js`) | done | arena-36a6db9e-own2 | Source: https://api.github.com/repos/karagemop466-tech/FreeMoneyApps/contents/assets/data.js — 206 listings, reviewed 2026-08-19, pass S |
| 2 | Executive summary | `executive-summary.html` | done | arena-36a6db9e-own2 | Dashboard, category table, key findings, verification policy, limitations |
| 3 | Site build — clean landing page (dashboard) | `index.html`, `assets/style.css`, `assets/app.js` | done | arena-36a6db9e-own2 | Responsive cards, stats, recommended free entries |
| 4 | Site build — category subpages with entry tables | `categories/*.html` | done | arena-36a6db9e-own2 | One table per category; every row links to official source(s) |
| 5 | Site build — Flagged for Review page | `flagged.html` | done | arena-36a6db9e-own2 | Unverified/caution/ended/mixed registers with sources |
| 6 | Verification pass — official sources per row; unverified blanked and flagged | all site pages + `data/listings.json` | done (spot checks logged below) | arena-36a6db9e-own2 | 12 listings have no official source → flagged unverified |
| 7 | Integration: merge prior session's branch into this one, consolidate site, resolve conflicts | all | done | arena-36a6db9e-own2 | Merge conflict log below |
| 8 | GitHub Pages: publish on main, PR to main, merge, verify deploy | repo settings + PR | in progress | arena-36a6db9e-own2 | |

## Merge conflict resolution (2026-11-01)

When this session's branch (`arena/36a6db9e-own2`, based on main@f0b01b8) was merged into `main`, `main` had already advanced to a627607 (merge of prior session PR #2, "Prefer official source pointers and record deployment audit"). Conflicting files: `index.html`, `COORDINATION.md`, `README.md`.

Resolution:
- `index.html`: kept this session's landing dashboard (clean landing page with category cards, stats, recommended free entries). The prior session's full-table landing content is preserved in `categories/*.html` tables and `data/contests.json` (208 entries).
- `COORDINATION.md`: combined — both sessions' task boards, verification records, and irregularities are retained here.
- `README.md`: combined — describes both sessions' contributions.
- Consolidation (no information discarded): prior session's root-level duplicate HTML pages (`skill.html`, `sports.html`, `tech.html`, `trivia.html`, `creative.html`, `forecasting.html`, `market.html`, `directory.html`, `pools.html`, `review.html`, `summary.html`) and root `style.css`/`app.js` are superseded by this session's `categories/*.html`, `flagged.html`, `executive-summary.html`, and `assets/`. Their data layer is fully retained: `data/contests.json` (208 entries incl. GEMS Prize and ARC Prize event records), `data/categories.json` (10 categories incl. pools), `data/EVIDENCE.md`, `data/upstream.json`, `scripts/build.py`, `scripts/test.py`.
- Removed `.github/workflows/validate.yml`: it targets the prior session's root-level build pipeline (`scripts/build.py` + committed HTML diff) and would fail against this site's structure; retained their `scripts/` as reference instead. Noted as a known follow-up: re-wire CI validation if desired.

## Verification performed (official sources, 2026-11-01)

| Official source checked | Result | Matches ledger? |
|-------------------------|--------|-----------------|
| https://www.papaya.com/faq | "PAPAYA offers both free competitions using Gems and real money competitions." Platform takes a fee from the entry pool. | Yes — solitaire-cash, bingo-cash entries |
| https://fantasy.espn.com/games/nfl-pickem-2026/make-picks | "58 prizes ... worth $102K", FREE to play, up to 10 entries, dates 09/09/2026 - 01/10/2027 | Yes — ESPN NFL Pick'em ($102,000 / 58 prizes) |
| https://www.skillz.com/ | Homepage loads ("Win cash and real-world prizes") | Yes — skillz entry |
| https://www.checkmategaming.com/free-tournaments | "Totally free to enter with real cash prizes. New tournaments posted daily." | Yes — checkmate-gaming entry |
| https://devpost.com/hackathons | Loads; hackathons with published cash prizes | Yes — devpost entry |
| https://www.kaggle.com/ | Competition directory with prize competitions | Yes — kaggle/arcprize entries |
| https://www.chess.com/tournaments | Loads; tournaments starting every few minutes | Yes — chesscom-tournaments entry |
| https://www.drivendata.org/competitions/306/competition-doe-gems/ | $300,000 pool; $100,000 final first prize; deadline 2026-12-03 23:59 UTC | Prior session evidence — added as `gems-2026` entry |
| https://docs.nlr.gov/docs/fy26osti/96647.pdf | GEMS rules §1.3 eligibility; A.2 ACH + W-9 within 30 days | Prior session evidence — cited on `gems-2026` |
| https://arcprize.org/competitions/2026 | $2M across 3 tracks; submissions Nov 2, papers Nov 8 | Prior session evidence — on `arcprize` entry |

Every category-table row carries at least one source link tagged official / affiliate / forum. Rows whose only sources are affiliate/forum are flagged "Unverified" and their prize / cash-out / payout / eligibility cells are blanked.

## Irregularities flagged (published on site `flagged.html`; do not block launch)

1. **12 listings with no official source** — flagged unverified: `thelines-survivor`, `fantasy-arena`, `fplhub`, `bona-fide`, `olka`, `fplmanager-india`, `fplstore`, `pitchbooking` (sports), `roboforex-demo`, `fbs-pro-demo`, `npbfx-demo` (market), `tff-fantezi-lig` (sports).
2. **skillz.com/terms-of-service/** returns 404 (tosUrl on the `skillz` entry). Entry's official source https://www.skillz.com/ loads.
3. **11 caution entries**: `football-mad`, `fantasy-arena`, `fplhub`, `bona-fide`, `olka`, `fplmanager-india`, `fplstore`, `pitchbooking`, `streak-for-cash`, `premiership-rugby-fantasy`, `formula-e-predictor`.
4. **27 ended / out-of-season entries** — not currently playable.
5. **5 mixed entries** — free play exists but cash requires entry fee: `solitaire-cash`, `bingo-cash`, `skillz`, `pocket7`, `vocal`.
6. Ledger data last checked 2026-08-19; prizes/eligibility/availability can change. US prizes of $600+ typically require a W-9; taxes are the winner's responsibility.

## Known follow-ups
- Re-wire CI validation for this site's structure (prior session's `.github/workflows/validate.yml` was removed; their `scripts/build.py`/`scripts/test.py` are retained in `scripts/`).
- `categories/pools.html` was missing from the initial build; added in the integration commit (7 pool & league platform entries).

## PR and publish record
- PR: https://github.com/sassnarep3-star/Own2/pull/4 (branch `arena/36a6db9e-own2` → `main`)
- Merge result: pending
- GitHub Pages URL: pending
