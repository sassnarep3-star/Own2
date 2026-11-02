# Executive summary — analysis pass (session arena-02aa8a4d, 2026-11-02)

**Goal.** Answer the project's core question — *which free-to-enter, cash-prize competitions are the best use of your time right now?* — using only official, quote-backed sources, and publish every finding in simple tables with source links on every row.

**Where this fits.** This repository already holds a 209-row shared catalog (main dashboard) and several parallel subsites. This pass (`analysis-02aa8a4d/`) adds three things none of them had: (1) a **freshness sweep** — what is actually open on 2026-11-02, read live from official pages; (2) a **transparent evidence-only ranking** ("where to spend your time"); (3) a **link-health audit** — a recheck of previously flagged broken links plus a repo-wide internal link scan.

## The best places to spend your time right now (tier A — free entry, cash prize, and open status all confirmed on 2026-11-02)

| # | Competition | Score | Verified facts (official source) |
|---|---|---|---|
| 1 | CBS Pro Football Pick'em 2026 | 93 | Free ("The Challenge is FREE to play"), 18 × $1,000 weekly + $5,000 season + $100,000 contingency; open to 2027-01-10 ([rules](https://www.cbssports.com/fantasy/football/games/pickem/rules)) |
| 2 | ESPN NFL Pick'em 2026 | 87 | Free ("FREE to play. Create up to 10 entries"), $102,000 across 58 prizes + $1,500/week; to 2027-01-10 ([game page](https://fantasy.espn.com/games/nfl-pickem-2026/picks)) |
| 2 | ESPN College Pick'em 2026 | 87 | Free ("FREE to play"), $86,000 across 46 prizes; Week 10 locks 2026-11-07 ([game page](https://fantasy.espn.com/games/college-football-pickem-2026/picks)) |
| 4 | Devpost (platform) | 83 | 14,228 hackathons; open cash events to $1,000,000 (Meta VR Start) ([directory](https://devpost.com/hackathons)) |
| 5 | NFL Big Data Bowl 2027 (Kaggle) | 80 | "NO PURCHASE NECESSARY TO ENTER OR WIN", $100,000 ($45K + $45K + $10K), closes 2027-01-06 ([rules](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/rules)) |
| 5 | Sony World Photography Awards — Single Image | 80 | "1.2.1 The Competition is free to enter", $5,000 + equipment, deadline 2027-01-05 ([page](https://www.worldphoto.org/sony-world-photography-awards/single-image)) |
| 7 | Checkmate Gaming free tournaments | 79 | "Totally free to enter with real cash prizes. New tournaments posted daily"; $40–$120 events listed for 2026-11-02 ([page](https://www.checkmategaming.com/free-tournaments)) |
| 7 | Metaculus tournaments | 79 | "participate for free and win cash prizes"; 19 live tournaments, pools up to $50,000 ([page](https://www.metaculus.com/tournaments/)) |
| 9 | Wergle Flomp Humor Poetry Contest | 78 | "No fee to enter", $5,100, window 2026-08-15 → 2027-04-01 ([page](https://winningwriters.com/our-contests/wergle-flomp-humor-poetry-contest-free)) |
| 10 | PayPal AI Hackathon | 74 | "NO PURCHASE OR PAYMENT NECESSARY", $67,500 cash (site also says $69,750 — conflict), closes 2026-11-12 ([rules](https://paypalaihackathon.devpost.com/rules)) |
| 11 | ARC Prize 2026 | 73 | $2M / 3 tracks; **final submissions due today (2026-11-02)**, papers due 2026-11-08 ([overview](https://arcprize.org/competitions/2026)) |

## Tier B — promising, evidence incomplete (do not treat as confirmed)

- **GEMS Prize Challenge (US DOE)** — $300,000 confirmed, open until 2026-12-03, but **free entry is not stated** on the competition page or rules gateway ([competition page](https://www.drivendata.org/competitions/306/competition-doe-gems/), rules PDF at [nlr.gov](https://www.nlr.gov/docs/fy26osti/96647.pdf), unread this pass).
- **MLB Beat the Streak** — $5,600,000 headline prize and "NO PURCHASE NECESSARY" confirmed, but official terms say the window ended with the 2026 MLB regular season while the page still says "Start playing now" ([page](https://www.mlb.com/apps/beat-the-streak)) — status conflict, unresolved.
- **XPRIZE** — active purses to $119M confirmed at index level; free entry and new-entry viability unconfirmed.

## Excluded (stamped honestly)

- **GamerSaloon 1-Rounders** — $10 prize is **Bonus Cash, "not eligible for withdrawal"** ([promo page](https://www.gamersaloon.com/promos/1rounder/)).
- **TradingView The Leap** — between contests; the most recent contest paid **TradingView plans (non-cash)** despite the general "real-money prizes" claim ([page](https://www.tradingview.com/the-leap/)).

## Key irregularities (all published on the Flagged for Review page, non-blocking)

1. **ARC Paper deadline discrepancy (live again today):** arcprize.org says "November 8, 2026 - Papers due"; the Kaggle Paper Track card showed "7 days to go" on 2026-11-02 (≈ Nov 9) and prior sessions recorded Kaggle rules "2026-11-09 23:59 UTC". Not reconciled.
2. **PayPal hackathon prize conflict:** "$67,500 in cash" (prizes card + directory) vs "$69,750 in total prizes" (About text) — on the same official site.
3. **DSH Hacks V2** advertises "$100k+ in prizes!" while Devpost's official card says "5 non-cash prizes".
4. **Zindi** moved domains (zindi.africa → zindi.world); its challenge list is JS-only and not machine-verifiable ("Open Challenges: —").
5. **11 of 12 re-checked broken links are still broken** (NHL Bracket Challenge 404, Topcoder behind an Auth0 alert, A-Leagues fantasy 404, Solitaire Cash App Store 404, HyperMind 503, Pensacola WordPress crash, 4 dead fantasy domains, OHHA 404). **1 recovered:** UEFA Champions League Fantasy.
6. **Repo-wide internal link scan (160 HTML pages): 0 broken local links.**

## Coverage honesty

- 209 catalog rows tracked; **17 assessed** in this pass (12 tier A, 3 tier B, 2 excluded); **192 unranked** with blank values — never inferred.
- 19 official pages re-read on 2026-11-02 with verbatim quotes (see `verification-log.md` and `data/freshness.json`).
- No contest accounts, entries, deposits, or prize claims were made. Legal/tax/personal eligibility is out of scope: official rules win every argument.

## Recommended next actions

1. Enter the tier-A games that match your location (CBS/ESPN games are US-oriented; eligibility cells are blank where the fetched page did not state them).
2. Decide *today/this week*: ARC Paper Track ($450K, ~7 days), PayPal AI Hackathon ($67.5K, 10 days), then GEMS ($300K, 4 weeks) after confirming free entry from the NLR rules PDF.
3. For AI-agent-assisted competition work, prefer tech/data events where rules allow tooling (Kaggle BDB, Devpost events); note Wergle Flomp **forbids** AI-generated text and Sony requires photographic origin.
4. Extend verification to the 192 unassessed rows; each row on the review queue lists its official link.
