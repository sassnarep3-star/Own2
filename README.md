# Own2

Free Cash Prize Competition Ledger &mdash; a clean, dashboard-style site for finding free-to-enter competitions that pay real cash prizes.

## Live site
Published on GitHub Pages from this repo (see COORDINATION.md for the PR and merge record).

## What it is
A research catalog of 207 competition entries organized by category:
18 Creative contests, 2 Directories & forums, 3 Forecasting tournaments, 19 Market competitions, 7 Free pool & league platforms, 12 Skill tournaments, 129 Fantasy & sports picks, 15 Tech & data competitions, 2 Trivia competitions.

Entries come from the **Free Money &amp; Contest Ledger** (https://karagemop466-tech.github.io/FreeMoneyApps/),
pass S, reviewed 2026-08-19. Each entry links to the operator&rsquo;s own official signup or rules page.
This is a research desk, not a sponsor. Official rules win every argument.

## Verification
- Every table row carries source link(s), tagged official / affiliate / forum.
- If a value cannot be confirmed from an official source, it is left blank and the row is flagged unverified. Nothing is inferred.
- 12 entries have no official source and are flagged unverified on the Flagged for Review page.

## Site structure
- `index.html` &mdash; landing page / dashboard with category cards and recommended free entries
- `executive-summary.html` &mdash; executive summary, key findings, verification policy
- `categories/*.html` &mdash; one table per competition category
- `flagged.html` &mdash; Flagged for Review (unverified, caution, ended, mixed entries)
- `data/listings.json` &mdash; the underlying entry data
- `COORDINATION.md` &mdash; shared task board for multi-session work

## Flags
- 27 ended / out-of-season entries
- 11 caution entries
- 5 mixed entries (free play exists; cash requires an entry fee)
- 12 entries without an official source (unverified)

## Important
US prizes of $600+ typically require a W-9; taxes are the winner&rsquo;s responsibility. Cash competitions are often geo-fenced.
Nobody legitimate asks you to pay a fee to collect a prize. Bonus cash, gems, and tickets are not withdrawable USD.
Always read the individual contest&rsquo;s own prize and payment terms before entering.
