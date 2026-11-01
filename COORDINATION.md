# Coordination — Own2 / Free Cash Prize Competition Ledger

Shared task board for agent sessions working on this repo.

**Session:** `arena-36a6db9e-own2` — branch `arena/36a6db9e-own2` (only active session; all claims below owned by this session).

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
| 1 | Analyze reference site (Free Money & Contest Ledger) and extract structured ledger data | `data/listings.json` (from `karagemop466-tech/FreeMoneyApps` `assets/data.js`) | done | arena-36a6db9e-own2 | Source: https://api.github.com/repos/karagemop466-tech/FreeMoneyApps/contents/assets/data.js — 206 listings, reviewed 2026-08-19, pass S |
| 2 | Executive summary | `EXECUTIVE_SUMMARY.md` content on `executive-summary.html` | done | arena-36a6db9e-own2 | Dashboard, category table, key findings, verification policy, limitations |
| 3 | Site build — clean landing page (dashboard) | `index.html`, `assets/style.css`, `assets/app.js` | done | arena-36a6db9e-own2 | Responsive cards, stats, recommended free entries |
| 4 | Site build — category subpages with entry tables | `categories/index.html` + 8 type pages | done | arena-36a6db9e-own2 | One table per category; every row links to official source(s) |
| 5 | Site build — Flagged for Review page | `flagged.html` | done | arena-36a6db9e-own2 | Unverified/caution/ended/mixed registers with sources |
| 6 | Verification pass — every table row has official source; unverified left blank and flagged | all site pages + `data/listings.json` | done (spot checks logged below) | arena-36a6db9e-own2 | 12 listings have no official source → flagged unverified |
| 7 | GitHub Pages: build check, publish, PR to main, merge, record PR link | repo settings + PR | in progress | arena-36a6db9e-own2 | |

## Verification performed (spot checks against official sources, 2026-11-01)

| Official source checked | Result | Matches ledger? |
|-------------------------|--------|-----------------|
| https://www.papaya.com/faq | Loads. "No. PAPAYA offers both free competitions using Gems and real money competitions." Platform takes a fee from the entry pool. | Yes — solitaire-cash, bingo-cash entries (Gem vs cash rooms, Bonus Cash not withdrawable) |
| https://fantasy.espn.com/games/nfl-pickem-2026/make-picks | Loads. "58 prizes ... worth $102K", FREE to play, up to 10 entries, event dates 09/09/2026 - 01/10/2027, official rules linked | Yes — ESPN NFL Pick'em entry ($102,000 total across 58 prizes) |
| https://www.skillz.com/ | Homepage loads ("Win cash and real-world prizes...") | Yes — skillz entry |
| https://www.checkmategaming.com/free-tournaments | Loads. "Totally free to enter with real cash prizes. New tournaments posted daily." Live free-entry tournaments listed | Yes — checkmate-gaming entry |
| https://devpost.com/hackathons | Loads. Hackathons with published cash prizes (e.g. $67,500, $100,000, $1,000,000) | Yes — devpost entry |
| https://www.kaggle.com/ | Loads. Competitions with prizes (ARC Prize $850,000 / $700,000 / $450,000 tracks visible) | Yes — kaggle / arcprize entries |
| https://www.chess.com/tournaments | Loads. Tournaments starting every few minutes | Yes — chesscom-tournaments entry |

Every category-table row carries at least one source link tagged official / affiliate / forum.
Rows whose only sources are affiliate/forum (no operator page) are flagged "Unverified" and their prize / cash-out / payout / eligibility cells are blanked, per the verification rule.

## Irregularities flagged (published on site `flagged.html`; do not block launch)

1. **12 listings with no official source** — flagged unverified: `thelines-survivor`, `fantasy-arena`, `fplhub`, `bona-fide`, `olka`, `fplmanager-india`, `fplstore`, `pitchbooking` (sports), `roboforex-demo`, `fbs-pro-demo`, `npbfx-demo` (market), `tff-fantezi-lig` (sports). Sources listed are affiliate/forum only.
2. **skillz.com/terms-of-service/** returns 404 (tosUrl on the `skillz` entry). The entry's official source link https://www.skillz.com/ still loads. Value claims for this entry rest on the ledger's earlier audit; treat the terms link as broken.
3. **11 caution entries**: `football-mad`, `fantasy-arena`, `fplhub`, `bona-fide`, `olka`, `fplmanager-india`, `fplstore`, `pitchbooking`, `streak-for-cash`, `premiership-rugby-fantasy`, `formula-e-predictor`.
4. **27 ended / out-of-season entries** — not currently playable.
5. **5 mixed entries** — free play exists but cash requires an entry fee: `solitaire-cash`, `bingo-cash`, `skillz`, `pocket7`, `vocal`.
6. Ledger data last checked 2026-08-19; prizes, eligibility, and availability can change at any time. US prizes of $600+ typically require a W-9; taxes are the winner's responsibility.
