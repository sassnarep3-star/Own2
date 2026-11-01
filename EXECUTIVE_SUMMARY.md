# Executive summary

Prepared 2026-11-01 (UTC) by session be1d2210 for the "Free to enter cash prize competitions" project. Live site: [sassnarep3-star.github.io/Own2](https://sassnarep3-star.github.io/Own2/).

## Bottom line

- The source ledger ([karagemop466-tech/FreeMoneyApps](https://github.com/karagemop466-tech/FreeMoneyApps), commit 466f7c1) lists **206** competitions and **324 unique URLs**. Its data is **74 days old**: every entry carries the same check date, 2026-08-19.
- Only **13 of 206** entries could be re-read on their official pages in this review. **11 of those 13** showed a discrepancy or an unconfirmable figure against the old ledger, including entries that have since closed. Treat the other 191 as leads, not facts.
- For an AI-coding-agent strategy, the best-matched open opportunities confirmed today are forecasting tournaments (Metaculus), Kaggle paper tracks and hackathons, the DrivenData $300,000 GEMS challenge, and Devpost hackathons. Two free NFL pick'em games (ESPN, CBS) are open and fully sourced but are not code-driven.
- The new site follows one rule: **verified or blank**. Unconfirmed values are left empty and flagged, never filled in.

## What was delivered

- A mobile-first GitHub Pages dashboard: landing page, Top picks, nine category subpages, an all-entries table with search and filters, this summary, a method page, and a **Flagged for Review** page with source links.
- Machine-readable data: `data/ledger.json`, `data/ledger.csv`, the unmodified source extract, and the verification record `data/verification/verified.json`.
- Tooling: `tools/extract.js`, `tools/audit.js`, `tools/build.js`, `tools/linkcheck.js` (internal links) and `tools/linkcheck-external.js` (for use on a machine with open internet).
- `COORDINATION.md`: the task board with claims, sources, verification performed and irregularities.

## Key numbers

| Measure | Value |
|---|---|
| Entries in source ledger | 206 (9 categories) |
| Re-read on official page, 2026-11-01 | 13 |
| Official page unreadable (JavaScript-only) | 2 (Topcoder, Zindi) |
| Not verified (blank values, flagged) | 191 |
| Verified entries with a discrepancy or unconfirmable figure | 11 of 13 |
| Entries with no source tagged official in the old ledger | 12 |
| Old headline "true free paths" | 189, of which 26 are marked ended |

## Best opportunities confirmed on official pages (2026-11-01)

| Contest | Confirmed on the official page | Free entry | Dates |
|---|---|---|---|
| [Metaculus tournaments](https://www.metaculus.com/tournaments/) | Fall 2026 FutureEval Bot Tournament $50,000; Labor Automation $35,000; others $5,000-$15,000 | Yes (page says free) | Fall bot tournament "ends 2 months from now" |
| [Kaggle competitions](https://www.kaggle.com/competitions) | ARC Prize Paper Track $450,000; Gemma 4 Developer Agent Paper Track $35,000; NFL Big Data Bowl 2027 $100,000 | Not stated on page read | 8 days, 11 days, 2 months to go |
| [DrivenData GEMS Prize Challenge](https://www.drivendata.org/competitions/) | $300,000 | Not stated on page read | "4 weeks left" |
| [Devpost hackathons](https://devpost.com/hackathons) | Meta VR $1,000,000; Codegeist $120,000; Kiroween $100,000; PayPal AI $67,500 | Not stated on page read | Various, Nov-Dec 2026 |
| [ESPN NFL Pick'em](https://fantasy.espn.com/games/nfl-pickem-2026/make-picks) | 58 prizes, $102,000 total; $1,500 guaranteed weekly | Yes | to 10 Jan 2027 |
| [CBS Pro Football Pick'em rules](https://www.cbssports.com/fantasy/football/games/pickem/rules) | 18 x $1,000 weekly, $5,000 season, $100,000 contingency | Yes | to 10 Jan 2027 |

The ranking, and the notes on fit for an AI coding agent, are analysis rather than confirmed fact; see [Top picks](top-picks.html).

## Time-critical

- ARC Prize 2026: final submissions due **2 Nov 2026 (11:59 PM UTC)**; the ARC-AGI-2 entry deadline (26 Oct) has already passed. Paper Track papers are due 8 Nov.
- Metaculus "US Midterms 2026" ($10,000) ends in 3 days.
- NASCAR Fantasy Live registration ends 8 Nov 2026 (prize amounts not confirmed).

## Main irregularities (full list on the Flagged for Review page)

- **Stale statuses.** ESPN Survivor shows "Entry creation has closed"; the AIcrowd ARC White-Box challenge shows "Submissions closed"; the TradingView Leap edition cited is completed; Metaculus' named Summer pool is pending winners.
- **Over-broad "free USD" tag.** 26 ended entries and 47 entries with gift-card, merchandise or trip prizes are counted as free USD paths.
- **Policy contradiction.** The ledger excludes sportsbook accounts, yet lists Fanatics Survivor with a sportsbook signup domain and a third-party article as its rules link.
- **Weak sourcing.** 19 cited sources are affiliate/forum pages; 12 entries have no official-tagged source; some "official" links are generic platform pages (e.g. the FPL home page for third-party leagues).
- **Version drift.** The live site header says "Pass C · 17 Aug 2026" and the review page says 119 listings, but the data is pass S with 206.
- **Site usability.** One long page of 206 cards, no search or filters, third-party fonts, relative og:image. Not device-tested; structural observation only.

## Risks and limits

- **Coverage.** 191 entries remain unverified. Verification used live page fetches; JavaScript-only pages could not be read.
- **Link rot.** The review environment could not reach most hosts, so none of the 324 external URLs was bulk link-checked. The reported broken links are not individually confirmed. The source repo has no broken internal links.
- **Eligibility.** Texas eligibility was not confirmed per contest. Only the CBS and NASCAR rules state 50-state eligibility.
- **Automation and AI use.** Contest rules on automated entries or AI assistance were not read. Read them before using an agent in any contest. ARC Prize forbids internet/API access during Kaggle evaluation and requires open-sourcing.
- **Prize reality.** Headline pools are split across placings; confirmed prize totals are not expected returns.

## Recommended next steps

1. Run `tools/linkcheck-external.js` on an unrestricted machine and attach the report.
2. Verify the remaining 191 entries in priority order: ML/data (Codabench, Grand-Challenge, CrunchDAO, HeroX, XPRIZE), then US pick'em (Fox Super 6, NBA, NHL), then market contests.
3. Read the rules pages (not only landing pages) for the six top picks, with attention to AI/automation clauses and Texas residency.
4. Use `data/ledger.json` as the shared feed for the additional sites planned in the project.

## Sources

Official pages read on 2026-11-01 are listed per entry in [verified.json](data/verification/verified.json) and on the [Flagged for Review](flagged.html) page. Original data: [FreeMoneyApps @ 466f7c1](https://github.com/karagemop466-tech/FreeMoneyApps/tree/466f7c1e7a14b52b4a0d36beb84a00d68fd409b7).
