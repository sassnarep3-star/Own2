# Executive Summary — Free Cash-Prize Competition Ledger

**Date:** 2026-11-01 · **Session:** `4c1d6bb4` · **Repo:** `sassnarep3-star/Own2`
**Live site:** https://sassnarep3-star.github.io/Own2/
**Data source:** [karagemop466-tech/FreeMoneyApps](https://github.com/karagemop466-tech/FreeMoneyApps) (audit pass S, reviewed 2026-08-19)

---

## Goal

Collect, organize and analyze a full list of **free-to-enter competitions that
pay real cash**, and publish it as a clean, mobile-friendly dashboard where
**every value carries an official source link** and anything unconfirmable is
**left blank and flagged** — never guessed — so a human (and an AI coding
agent) can pick the best competitions to spend time on.

## What exists (data)

| Metric | Value |
|---|---|
| Listings | **206** across **9** categories |
| True free-USD paths | **189** |
| Active now | **163** (27 ended/out-of-season, 11 caution, 5 mixed) |
| Rows with an official source | **194** |
| Rows flagged unverified (no official source) | **12** — values shown blank |
| Removed by upstream policy (sweepstakes/casinos/gambling promos) | **45** — documented, not carried into tables |
| Data reviewed upstream | 2026-08-19 |

**Categories:** Fantasy & sports picks (129) · Creative contests (18) · Market
competitions (19) · Tech & data (14) · Skill tournaments (12) · Free pool
platforms (7) · Forecasting (3) · Trivia (2) · Directories (2).

## What this build adds over the reference site

The reference site was a **single 206-card scroll with no search, no filters
and no category pages** — the stated usability problem — and the user reported
broken links. This build:

1. **Responsive dashboard** — landing page + one subpage per category, all
   entries in **table format**, client-side search + status/free-path filters,
   and a mobile card layout below 720px.
2. **Verification pipeline**
   - `scripts/check-data.mjs` — structural audit (duplicate ids, bad enums,
     malformed URLs, missing official sources) — runs in CI on every push.
   - `scripts/check-links.mjs` + `.github/workflows/linkcheck.yml` — checks
     **every URL** in the data file and pages (2xx pass, 403/429 listed for
     manual review, 4xx/5xx/DNS/timeout published as broken).
   - `reports/spot-checks.json` — manual fetches of featured entries' official
     pages; **unconfirmed values are blanked and flagged automatically** at build time.
3. **Analysis page** — distributions (category/status/free-path/verification
   friction), the full priority-score formula used for the home top-15,
   policy exclusions with reasons, and patterns (free rooms rarely pay USD,
   seasonality, $600 tax threshold, geo-restrictions).
4. **Flagged for Review page** — every unverified row, every spot-check
   failure, every broken link, with source links for manual review.
5. **Executive summary** — this document, mirrored at `/executive-summary.html`.

## Verification results (2026-11-01)

- **Structural:** 206 rows, 0 duplicates, 0 malformed URLs. 12 rows lack an
  official source → blanked + flagged. (`reports/data-audit.json`)
- **Spot checks (9 featured entries fetched from official pages):** 6 verified
  exactly (ESPN NFL $102K/58 prizes; ESPN CFB $86K/46 prizes; CBS $1K×18 +
  $5K + $100K; ARC Prize $2M/3 tracks; Kaggle; DrivenData), **3 unconfirmed**
  and therefore blanked + flagged:
  - **Devpost** — official page now lists a $1,000,000 competition; ledger's
    "currently $10,000–$685,000" range contradicted → blanked.
  - **Fanatics NFL Survivor** — official homepage shows no contest/prize;
    third parties describe $1M as **FanCash**, not USD → blanked. Also a
    policy tension: operator is a licensed sportsbook.
  - **Dirty Dozen (Gambling.com)** — official URL redirects to a generic
    casino-games index; £12,000 figure unconfirmable → blanked.
- **Links (CI, run 41316899973):** 326 unique URLs — **258 ok · 2 redirect ·
  40 blocked · 26 broken**. Every broken and blocked URL is published on the
  flag page with its listing id; none were rewritten without a confirmed
  official replacement. (`reports/link-check.json`)
- **Build:** 14 pages generated; internal-link check passes; CI re-runs the
  build on every push.

## Irregularities flagged for your review

1. **12 listings with only affiliate/forum sources** (FPL mini-leagues, demo
   trading contests, TheLines survivor) — blank values, non-official links
   listed on the flag page.
2. **3 spot-check failures** (Devpost, Fanatics Survivor, Dirty Dozen) — blank
   values, fetch evidence + links on the flag page.
3. **Fanatics Survivor policy tension** — a sportsbook-operated contest sits
   in a ledger whose stated policy excludes gambling-operator products.
4. **27 ended entries** keep historical prize figures (badge-marked; excluded
   from ranking).
5. **45 policy removals** upstream (sweepstakes/casinos) — listed with reasons
   on the Analysis page.
6. **Link-check: 26 broken + 40 blocked URLs** (e.g. NHL Bracket Challenge
   404s, several DNS-dead UK/IRL fantasy domains, App Store 404s, Topcoder
   404s, expired TLS on Pensacola Songwriters; blocked = 403/429 refusals that
   may still work in a browser) — all published on the flag page with codes.

## Bottom line

**189 competitions currently advertise a genuine free path to cash.** Start at
the home page's transparent top-15 priority table, open each row's **official
source link**, and treat every prize figure as "per the official page, as of
its last check" until re-confirmed. Nothing on this site is inferred: if an
official source could not confirm a value, the cell is blank and the item is
on [Flagged for Review](https://sassnarep3-star.github.io/Own2/flagged.html).

## Key links (for manual review)

- Site: https://sassnarep3-star.github.io/Own2/
- Analysis: https://sassnarep3-star.github.io/Own2/analysis.html
- Flagged for Review: https://sassnarep3-star.github.io/Own2/flagged.html
- Data source repo: https://github.com/karagemop466-tech/FreeMoneyApps
- Verification log: [`verification-log.md`](verification-log.md)
- Coordination/task board: [`COORDINATION.md`](COORDINATION.md)
