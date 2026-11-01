# Competition Desk — executive summary

**Audit snapshot: November 1, 2026 UTC.** Independent research, not an endorsement or income forecast.

## Scope and bottom line

The original [Free Money & Contest Ledger](https://karagemop466-tech.github.io/FreeMoneyApps/) contains **206 listings in nine categories**, not 206 established currently open, free cash competitions. All rows are preserved. Three specific events discovered on official pages bring the new catalog to **209 entries**.

Only independently inspected official claims populate the approved dataset. Unconfirmed entry fee, prize, deadline, eligibility, payout and AI-policy fields are empty. Inherited assertions remain in a separate, explicitly unverified provenance file. Imported names and categories do not imply verification.

No entry is fully cleared for participation. A platform page is not competition-specific rules, a successful HTTP response is not verification, and a cash pool is not a promised payout to an individual. No win probability, earnings/hour, or expected value is invented.

## Research priorities for the AI-agent goal

1. **[Fall 2026 FutureEval Bot Tournament](https://www.metaculus.com/tournament/fall-futureeval-2026/)**: $50,000 pool, bot-only, closes January 6, 2027. Metaculus explicitly describes [free participation and cash prizes](https://www.metaculus.com/tournaments/). The [resources page](https://www.metaculus.com/notebooks/38928/ai-benchmark-resources/) describes three-hour question windows and one forecast per question. Full personal prize eligibility and payout method remain unverified; late entry can miss questions. AI/API compute is not necessarily cost-free.
2. **[NFL Big Data Bowl 2027](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/overview)**: $100,000 total across tracks; final submissions January 6, 2027, 23:59 UTC. A public notebook and data-analysis writeup are required. [Rules](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/rules) impose team, data-use and licensing conditions. Entry fee, full eligibility, payout and AI-assistance policy remain unconfirmed. Restricted data must not be uploaded to AI services without permission.
3. **[GEMS Prize](https://www.drivendata.org/competitions/306/competition-doe-gems/)**: $300,000 pool, December 3, 2026, 23:59 UTC deadline; geologic fault mapping algorithm task. Entry fee, full eligibility, payout and AI-tool permission remain unconfirmed. The [rules gateway](https://www.drivendata.org/competitions/306/competition-doe-gems/rules/) delegates to a HeroX rules resource.
4. **[ARC Prize 2026](https://arcprize.org/competitions/2026)**: $2M across three tracks; submissions November 2, papers November 8. Near-immediate deadline, required open sourcing, and no internet/API-based systems during Kaggle evaluation. Entry fee and full eligibility not reconfirmed.

This is an editorial order for **research**, not a ranking of expected return or entry-ready opportunities.

## Important counterexamples

- [Papaya FAQ](https://www.papaya.com/faq): free competitions use Gems, while cash competitions are separate. A free Gems path is not established as a free withdrawable-cash competition.
- [Wergle Flomp](https://winningwriters.com/our-contests/wergle-flomp-humor-poetry-contest-free): free entry, $5,100 cash total plus subscriptions, April 1, 2027 closing date. It explicitly prohibits AI-generated text, allows limited error/clarity feedback, and requires disclosure. Not suitable for an AI-written entry.
- [Metaculus directory](https://www.metaculus.com/tournaments/): valid official discovery path. `/competitions/` returned “Page not found”; do not use it. Not all listed tournaments carry prizes or allow bots to win.

## Original-site findings

The original HTML explicitly advertises no search or filters. Its long repeating cards impose substantial reading load. Header and data review dates disagree (August 17 vs August 19, 2026). The “True free paths” total is driven by inherited labels, not newly checked contest-specific eligibility. Several mini-leagues link only to their host platform; The Draft Pro links to a press-release distributor. Generic prize ranges and old-year URL paths do not establish a current offer. The original blanket $600+ tax statement was not republished as advice.

Sources for audit: [landing markup](https://github.com/karagemop466-tech/FreeMoneyApps/blob/main/index.html), [application logic](https://github.com/karagemop466-tech/FreeMoneyApps/blob/main/assets/js/app.js), and the exact commit recorded in `import-provenance.json`. Original markup was inspected, not subjected to a device usability study.

## Delivery and limitations

The replacement provides a responsive, static GitHub Pages dashboard, category subpages, searchable comparison tables, evidence filters, locally saved research, CSV export, field-level official source excerpts and a Flagged for Review queue. Tables and official source links remain visible without JavaScript.

A GitHub Actions audit attempts every unique inherited signup/rules/terms URL. Dated HTTP status, redirect, error and excerpts are recorded in `source-checks.json`. Failures can be bot protection, region restrictions, timeouts or real missing pages; they are not proof of fraud. HTTP 200 may still be a soft 404 or generic homepage. Sandbox direct operator-domain access and Actions artifact downloads are restricted; official content was additionally inspected using the page-reader tool. All limitations are visible; no row is declared fully verified.

No contest accounts were created; no entries, deposits or prize claims were submitted. Unknowns remain published review items and do not block site deployment.
