# Executive audit supplement — November 1, 2026 (UTC)

## Executive summary

The original ledger is a discovery inventory, not a list of 206 verified, currently available free-entry cash competitions. The main dashboard preserves its leads and flags unknowns. This independent supplement checks **13 inherited leads**, without overwriting the shared application owned by the initial integration session.

Two checked organizers explicitly document both a free entry path and a cash award:

1. **Wergle Flomp Humor Poetry Contest:** no fee; $2,000 first prize and $5,100 cash pool; submissions August 15, 2026–April 1, 2027. One original English humor poem, maximum 250 lines. **No AI-generated text or rewriting.** Limited critique is allowed with AI-use disclosure. Deadline time zone and cash-delivery mechanics remain unverified. [Official rules](https://winningwriters.com/our-contests/wergle-flomp-humor-poetry-contest-free).
2. **Sony World Photography Awards — Single Image:** up to three free images; $5,000 USD overall award; deadline January 5, 2027, 16:00 GMT. Images must be taken in 2026 and originate in a photograph. Computer-generated origin is prohibited. Payment mechanics and detailed AI-editing permissions remain unverified. [Official rules](https://www.worldphoto.org/sony-world-photography-awards/single-image).

These are evidence-backed research candidates, not claims of full legal qualification, guaranteed payment, or suitability for this particular user. They are **not good candidates for AI-generated submissions**. No expected hourly earnings, win probabilities, computing costs, or claims of verified payout history were invented.

## Important exclusions and irregularities

| Item | Finding | Official source |
|---|---|---|
| GamerSaloon 1-Rounders | Advertised $10 is Bonus Cash, explicitly not withdrawable. Exclude that promotion from a withdrawable-cash shortlist. | [Promotion and footnote](https://www.gamersaloon.com/promos/1rounder/) |
| Tom Howard/Margaret Reid Poetry Contest | $27 submission fee; currently closed with next window April 15–October 1, 2027. Not a free-entry path. | [Rules](https://winningwriters.com/our-contests/tom-howard-margaret-reid-poetry-contest) |
| NYPL Young Lions 2027 | “Now open” conflicts with September 3, 2026 deadline; publisher-only nominations. No current open status adopted. | [Submission criteria](https://www.nypl.org/about/awards/young-lions-fiction-award/submission-form) |
| Challenge.gov | Platform sunset March 30, 2026; official discovery successor is USA.gov. This does not establish HeroX equivalence. | [Official retirement notice](https://www.challenge.gov/), [USA.gov challenges](https://www.usa.gov/challenges) |
| Zindi inherited rules | Retrieved content reads “404 page not found.” No guessed replacement or HTTP status claim. | [Inherited rules destination](https://zindi.world/rules) |
| Film Prize inherited rules | Requested Film Prize URL resolves to Photo Prize rules; film conditions must not be inferred from them. | [Requested](https://www.prizefest.com/film/rules/), [resolved](https://prizefest.com/photo/rules/) |
| CheckMate Gaming | Event 267054 explicitly free; $40 displayed pool adjusted by eligible teams. Prize-claim text conflicts: 24 hours vs seven days. Header NA + EU vs US-default legal rule. | [Specific event](https://www.checkmategaming.com/tournament/cross-platform/call-of-duty-modern-warfare-4/free-entry-4v4-snd-best-of-1-267054) |
| Freelancer.com | Entry free; winner fee 10% or $5 USD, whichever greater. Platform policy is not a verified individual contest. | [Payment FAQ](https://www.freelancer.com/faq/topic.php?id=33) |
| Vocal | FAQ distinguishes regular from Vocal+ exclusive challenges; five-year-old update marker and stale country-count language mean current event rules are still required. | [Official FAQ](https://vocal.media/resources/challenges-frequently-asked-questions) |
| Kinolime | Inherited URL redirects to competition hub. 2026 feature competition completed; current development/production language does not establish a cash award. | [Current hub](https://www.kinolime.com/competitions) |
| MLB Beat the Streak | Rules explicitly no purchase; introductory sections define 2026 regular-season period and conditional streak thresholds. No current availability or cash amount established by this limited check. | [Official rules](https://www.mlb.com/apps/beat-the-streak/official-rules) |

All thirteen records remain on the supplement's [Flagged for Review](review.html) page. Blank values are unverified. This audit does not promote platform directories into verified individual events.

## Exact verification scope

- Wergle Flomp: both extracted chunks of the official contest page, including supplemental AI, eligibility, copyright and timing text.
- Sony: official awards overview plus all three extracted chunks of Single Image page, including numbered rules through §14. The former `/open` path resolved to `/single-image`. Cash is listed in the prize table; §13 says no cash alternatives. Neither is silently discarded. Device-gallery perpetual-use provision identified.
- Tom Howard/Margaret Reid: first extracted chunk including explicit fee, next submission window and AI restriction. No full payment audit claimed.
- NYPL: entire extracted submission criteria page.
- Vocal: entire extracted platform FAQ; age and Stripe statements attributed to the FAQ, not independently re-verified current event requirements.
- Kinolime: entire extracted current competition hub after redirect, not individual event rules.
- Film Prize: requested URL resolved to Photo Prize rules; first extracted chunk establishes mismatch. No Photo Prize rules adopted for Film Prize.
- GamerSaloon: first extracted chunk including the explicit nonwithdrawable Bonus Cash footnote.
- CheckMate Gaming: full free-tournament directory extraction and first of eleven extracted specific-event chunks, including event information and general legal conditions. Detailed game rules in remaining chunks not audited. This is explicitly not full event qualification.
- MLB: first of five extracted rules chunks, covering introduction, eligibility and entry period. No prize amount adopted from unread sections.
- Challenge.gov and USA.gov: complete extracted retirement notice and challenges landing page.
- Zindi: inherited URL resolves to www host with retrieved error-page text. HTTP response code not measured.
- Metaculus scores FAQ and World Press Photo contest landing page were also inspected but **not promoted into evidence rows**: neither retrieved excerpt established a specific free-entry cash opportunity.

Official pages were read through the page-retrieval tool on November 1, 2026. `evidence.json` records every adopted fact, source URL and short excerpt. Excerpts are not full archived copies; external organizers can change their pages. No bulk claim of all-206 official verification or external-link health is made.

## Repository coordination and publication

The initial integration session owns the shared `data/`, root HTML, application scripts and workflow. This session claims only `audits/2026-11-01/` and append-only coordination notes, so the shared normalized data deliberately remains untouched. A request to link and integrate the supplement is logged in root `COORDINATION.md`.

Five independent static pages provide an executive landing page, three category subpages and Flagged for Review. They require no JavaScript or network assets. Regenerate and validate:

```sh
python audits/2026-11-01/build.py
python audits/2026-11-01/test.py
```

Global verification and deployment results, PR URL and merge commit are recorded in root `COORDINATION.md`. The prior main dashboard deployment was confirmed through the GitHub Pages build API as `built` at commit `5c37dd53dac849c88655ce470be774591eb9da34` before this supplement was added.
