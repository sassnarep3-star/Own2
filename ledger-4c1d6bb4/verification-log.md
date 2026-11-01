# Verification log

Session `4c1d6bb4` · branch `arena/4c1d6bb4-own2` · 2026-11-01 (UTC)

This file records **what was verified, how, and against which official source**.
Nothing here is marked verified without a link to the checked page.

## 1. Structural audit (T3/T6) — `scripts/check-data.mjs`

Run locally and in CI. Result: **206 listings, 0 duplicate ids, 0 unknown
type/status/freePath values, 0 malformed URLs, 0 rows without any source.**

**12 rows have no `official`-tier source** → rendered with blank values and
published on [Flagged for Review](https://sassnarep3-star.github.io/Own2/flagged.html):

| id | non-official source(s) present |
|---|---|
| thelines-survivor | affiliate: https://www.thelines.com/free-nfl-contest-pools-games-week-1-2024/ |
| fantasy-arena | affiliate: https://allaboutfpl.com/2025/07/list-of-free-to-join-prize-fpl-mini-leagues-ahead-of-25-26-season/ |
| fplhub | affiliate: https://fpltips.com/fpl-leagues-with-prizes/ |
| bona-fide | forum: https://www.reddit.com/r/FantasyPL/comments/1v4h6th/fpl_202627_minileagues_thread/ |
| olka | forum: https://www.reddit.com/r/FantasyPL/comments/1m6naoy/league_codes_megathread/ |
| fplmanager-india | affiliate: https://allaboutfpl.com/2025/07/list-of-free-to-join-prize-fpl-mini-leagues-ahead-of-25-26-season/ |
| fplstore | affiliate: https://fpltips.com/fpl-leagues-with-prizes/ |
| pitchbooking | forum: https://www.reddit.com/r/FantasyPL/comments/wecme0/list_of_free_to_enter_fpl_leagues_with_prizes/ |
| roboforex-demo | affiliate: https://tradingbrokers.com/roboforex-demo-contest/ |
| fbs-pro-demo | affiliate: https://fofan.org/contest/fbs-pro-demo-trading-contest/ |
| npbfx-demo | affiliate: https://www.ndfxbonus.com/2026/07/npbfx-trading-battle-demo-contest-win.html |
| tff-fantezi-lig | affiliate: https://en.shiftdelete.net/tff-launches-official-fantasy-league-mobile-game-for-super-lig/ |

Machine report: `reports/data-audit.json` / `reports/data-audit.md`.

## 2. Spot verification of featured/top entries (T9)

Method: direct fetch of each entry's **official** page on 2026-11-01; observed
text compared against the ledger's `prizeUsd`. Structured results:
`reports/spot-checks.json`.

| listing | verdict | official source fetched | observed |
|---|---|---|---|
| ESPN NFL Pick'em | ✅ verified | https://fantasy.espn.com/games/nfl-pickem-2026/make-picks | "58 prizes worth $102K"; "Total Prizes $102,000"; FREE to play; 09/09/2026–01/10/2027 — matches ledger `$102,000 total across 58 prizes` |
| ESPN College Football Pick'em | ✅ verified | https://fantasy.espn.com/games/college-football-pickem-2026/make-picks | "46 season-long and weekly prizes … $86K"; "Total Prizes $86,000" — matches ledger |
| CBS Pro Football Pick'em | ✅ verified | https://www.cbssports.com/fantasy/football/games/pickem/rules | Weekly Prize US$1,000 × 18; Season Long US$5,000; Contingency (perfect) US$100,000; max ARV US$223,000 — matches ledger `$1K/week + $5K season + $100K perfect` |
| ARC Prize 2026 | ✅ verified | https://arcprize.org/competitions/2026 | "$2M in prizes. 3 tracks." — matches ledger `$2,000,000 across three 2026 tracks` |
| Kaggle Competitions | ✅ verified | https://www.kaggle.com/competitions | Featured cash events incl. NFL Big Data Bowl 2027 ($100,000), Gemma 4 paper ($35,000), ARC paper ($450,000) — supports ledger range statement |
| DrivenData | ✅ verified | https://www.drivendata.org/competitions/ | DOE GEMS $300,000 active; Gates ASR $120,000; DaT Parkinson's €25,000 — supports hedged ledger range |
| Devpost Hackathons | ❌ unconfirmed | https://devpost.com/hackathons | Ledger says "currently $10,000 to $685,000"; official page lists **Meta VR Start Developer Competition $1,000,000** (Sep 24–Nov 18, 2026) plus $120k/$100k/$67.5k events. Stated range contradicted → **value blanked + flagged** (not rewritten) |
| Fanatics NFL Survivor | ❌ unconfirmed | https://betfanatics.com/ | Official homepage shows no Survivor contest or prize figure. Third-party reports describe $1M as **FanCash**, not USD. Currency/amount unconfirmable → **value blanked + flagged**. Extra concern: operator is a licensed sportsbook (policy tension with upstream exclusions) |
| Dirty Dozen (Gambling.com) | ❌ unconfirmed | https://www.gambling.com/games/dirty-dozen | Redirects to https://www.gambling.com/games (generic free-casino-games index); no contest page, no £12,000 figure → **value blanked + flagged** |

## 3. Link verification (T8) — `scripts/check-links.mjs`

Every URL in `assets/data.js` (signup, iOS, ToS, rules, sources) plus every
external `href`/`src` in the built pages is checked from GitHub Actions
(`.github/workflows/linkcheck.yml`) with a browser-like UA:

- `ok` (2xx) / `redirect` (3xx, final URL recorded) → pass
- `blocked` (401/403/405/429/451/999) → listed for manual review (may work in a browser)
- `broken` (other 4xx/5xx/DNS/timeout) → **published on Flagged for Review**

Run URL: see **PR & deploy record** in `COORDINATION.md`.
Reports: `reports/link-check.json`, `reports/link-check.md` (CI artifact `link-check-report`).

**Sandbox limitation (documented honestly):** the development sandbox only has
outbound access to GitHub/npm/PyPI hosts, so the full URL sweep runs in CI
(GitHub-hosted runner, full internet), not locally. Manual spot checks in
section 2 used the agent's page-fetch tool, which has broader access.

## 4. Build & internal-link check (T10)

`node scripts/build-pages.mjs` regenerates all 14 pages and fails if any
internal `href` target file is missing. Last run: **14 pages, all internal
links resolve.** The same commands run in CI on every push.

## 5. What was NOT verified (honest scope statement)

- Individual prize figures for the remaining ~191 rows were **not** re-fetched
  one by one this session; they carry their upstream official source links
  (checked upstream 2026-08-19) and are re-checked for *liveness* by the CI
  link check. The official source link is on every row for manual review.
- "Blocked" links from the CI sweep are not automatically failures — they are
  listed in `reports/link-check.json` for human review.
