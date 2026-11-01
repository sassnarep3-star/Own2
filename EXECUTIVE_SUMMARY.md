# Executive summary — Free cash-prize competitions ledger

**Prepared:** 2026-11-01 · **Repo:** `sassnarep3-star/Own2` · **Live site:** https://sassnarep3-star.github.io/Own2/ (GitHub Pages, deployed by the workflow in `.github/workflows/pages.yml`)
**Upstream data:** https://github.com/karagemop466-tech/FreeMoneyApps (commit `466f7c1e7a14b52b4a0d36beb84a00d68fd409b7`, data as of 2026-08-19) · **Live upstream page:** https://karagemop466-tech.github.io/FreeMoneyApps/

## Bottom line

The upstream ledger is a usable catalogue of 206 free-to-enter competitions with real prizes across 9 categories. It is not yet a verified list. In this pass only **11 of 206 rows (5.3%)** were checked on an official page. Four of those checks found conflicts, and one link is broken. The other **195 rows** have blank prize values and are flagged as unverified. Use the shortlist as a starting point, and read each official rulebook before entering.

## Key numbers

| Measure | Count | Source |
|---|---|---|
| Listings | 206 | Upstream data, reconciled to the upstream live page |
| Free path: full (ledger) | 189 | Upstream data (`freePath: full`), matches live page |
| Live (ledger) | 163 | Upstream data, dated 2026-08-19 |
| Checked on an official page (this pass) | 11 (3 verified, 3 partial, 4 conflict, 1 broken) | `data/review.json` |
| Unverified (prize blank) | 195 | — |
| Rows flagged for review | 48 (5 high, 28 medium, 15 low) | `data/review.json` + build checks |
| Repo and source irregularities | 18 (5 high) | `flagged.html`, section A |
| Shortlist (read first, not ranked) | 6 | Criteria on the site |

## Verified on official pages (2026-11-01)

- **ESPN NFL Pick'em 2026** — $102,000 across 58 prizes; event 9 Sep 2026 to 10 Jan 2027; status live. https://fantasy.espn.com/games/nfl-pickem-2026/picks
- **ESPN College Pick'em 2026** — $86,000 across 46 prizes; event 5 Sep to 6 Dec 2026; status live. https://fantasy.espn.com/games/college-football-pickem-2026/picks
- **ARC Prize 2026** — $2,000,000 in prizes. https://arcprize.org/
- **MLB Beat the Streak** — US$5,600,000 headline prize confirmed. **Status conflict:** official rules end the contest with the 2026 regular season, which has passed; the ledger still says live. https://www.mlb.com/apps/beat-the-streak/official-rules
- **Metaculus** — free to enter; prize pools on the page range from $3,400 to $50,000 (ledger lower bound $3,000 not confirmed). https://www.metaculus.com/tournaments/
- **CBS Sports Pro Football Pick'em 2026** — free entry; challenge period 9 Sep 2026 to 10 Jan 2027 confirmed. Prize amounts not confirmed in the sections read. https://www.cbssports.com/fantasy/football/games/pickem/rules
- **Devpost** — listing page shows live hackathon prizes from $2,500 to $1,000,000; ledger's $10,000 lower bound is not supported by this sample. https://devpost.com/hackathons

## Conflicts and broken items

- **Checkmate Gaming** — official page shows $40 to $1,500 per free tournament, not the ledger's $10 to $180. https://www.checkmategaming.com/free-tournaments
- **Kaggle** — official Competitions page shows live pools of $35,000 to $450,000; ledger says "commonly $5,000 to $100,000+". https://www.kaggle.com/competitions
- **The Draft Pro** — ledger says live; the operator's release says entries closed before the 23 April 2026 first round. https://www.prnewswire.com/news-releases/the-draft-pro-launches-free-1-000-000-perfect-draft-challenge-ahead-of-the-2026-nfl-draft-302736409.html
- **Dirty Dozen** — the ledger link redirects to a casino games page; no contest is shown. https://www.gambling.com/games/dirty-dozen → https://www.gambling.com/games

## Policy findings

The upstream source excludes casino products and any contest requiring a gambling-operator account (sportsbook, bookmaker, real-money DFS). Still listed:

- Fanatics Sportsbook (Fanatics Survivor; featured) — sportsbook operator.
- Andy's Bet Club (£1M Predictor) — betting brand.
- Oddspedia capper contest (ended) — betting site.
- Gambling.com (Dirty Dozen; featured) — casino operator.
- Bookmaker-sponsored games (Sun Dream Team, Sky Sports FF, SPFL, Super League ×2, MLB Beat the Streak) — sponsors only; ledger says no betting account needed. Unverified.

The upstream category blurb for "Fantasy & sports picks" also mentions "sweepstakes sportsbooks", which the same source excludes.

## Other irregularities

- **No license** in the upstream repo. Reuse rights for the listing data are unconfirmed. (This repo had no license or content before this session.)
- **Misattributed links:** 13 third-party league entries link to another operator's site (nine to the official Fantasy Premier League site; four to Fantasy Football Scout's own or other official pages).
- **Affiliate-only prize sources:** three forex broker demo contests (RoboForex, FBS, NPBFX) cite affiliate sites only.
- **Stale data:** every row is dated 2026-08-19. Seven annual photo awards are listed as live with deadlines not checked.
- **Promo or join codes** appear in 12 entries' ledger data. They are not published here and are unverified.

## Recommended next steps

1. Decide whether the listing data may be republished. The upstream has no license.
2. Remove or re-classify the sportsbook and casino rows (Fanatics, Andy's Bet Club, Oddspedia, Gambling.com) and review the bookmaker-sponsored rows against the source's own policy.
3. Correct the draft-pro and MLB status rows, and the Checkmate Gaming and Kaggle prize rows, from their official pages.
4. Verify the remaining 195 rows against official pages. Fill a prize cell only from an official page, and only with the page's own wording.
5. Re-check annual photo awards and season contests before promoting them.

## Where to look

- Site: https://sassnarep3-star.github.io/Own2/ — Home, categories, All entries, Flagged for review, Methodology.
- Flagged for review (publishing requirement): https://sassnarep3-star.github.io/Own2/flagged.html
- Verification record: `data/review.json`. Upstream snapshot: `data/source/ledger-data.js`. Task board and logs: `COORDINATION.md`.
