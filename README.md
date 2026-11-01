# Own2

Free Cash Prize Competition Ledger — a clean, dashboard-style site for finding free-to-enter competitions that pay real cash prizes.

## Live site
Published on GitHub Pages from this repo (main branch). PR and merge record: https://github.com/sassnarep3-star/Own2/pull/4 — see COORDINATION.md.

## What it is
A research catalog of competition entries organized by category:
- Fantasy & sports picks (129), Skill tournaments (12), Creative contests (18), Market competitions (19), Tech & data competitions (14), Trivia competitions (2), Free pool & league platforms (7), Directories & forums (2) = 206 entries from the Free Money & Contest Ledger, plus 1 verified addition (GEMS Prize Challenge).

Entries come from the **Free Money &amp; Contest Ledger** (https://karagemop466-tech.github.io/FreeMoneyApps/), pass S, reviewed 2026-08-19. Each entry links to the operator's own official signup or rules page. This is a research desk, not a sponsor. Official rules win every argument.

## Verification
- Every table row carries source link(s), tagged official / affiliate / forum.
- If a value cannot be confirmed from an official source, it is left blank and the row is flagged unverified. Nothing is inferred.
- 12 entries have no official source and are flagged on the Flagged for Review page.
- Spot-checked against official pages: papaya.com/faq, fantasy.espn.com (NFL Pick'em $102K/58 prizes), skillz.com, checkmategaming.com/free-tournaments, devpost.com/hackathons, kaggle.com, chess.com/tournaments; plus drivendata.org/GEMS and arcprize.org (prior session evidence in data/EVIDENCE.md).

## Site structure
- `index.html` — landing page / dashboard: stats, category cards, recommended free entries
- `executive-summary.html` — executive summary, key findings, verification policy
- `categories/*.html` — one table per competition category (incl. pools)
- `flagged.html` — Flagged for Review (unverified, caution, ended, mixed entries)
- `404.html` — not-found page
- `data/listings.json` — underlying entry data (206 entries)
- `data/contests.json`, `data/categories.json`, `data/EVIDENCE.md`, `data/upstream.json` — prior session's evidence-first normalization (208-entry export)
- `scripts/build.py`, `scripts/test.py` — prior session's build/test scripts (reference)
- `COORDINATION.md` — shared task board and merge/verification record

## Important
US prizes of $600+ typically require a W-9; taxes are the winner's responsibility. Cash competitions are often geo-fenced. Nobody legitimate asks you to pay a fee to collect a prize. Bonus cash, gems, and tickets are not withdrawable USD. Always read the individual contest's own prize and payment terms before entering.
