# Evidence log · 2026-11-01 UTC

Official pages read through the page retrieval tool. Verification is field-specific, not an endorsement of the operator. Blank values remain unresolved. Excerpts below are short transcriptions of the retrieved official content.

| Row(s) | Official source | Confirmed evidence | Not confirmed |
|---|---|---|---|
| solitaire-cash, bingo-cash | https://www.papaya.com/faq | “PAPAYA offers both free competitions using Gems and cash competitions.” | Free-to-enter withdrawable cash route, eligibility, withdrawal details |
| kaggle | https://www.kaggle.com/competitions | Directory has “Featured” prize competitions and “Getting Started” practice events | Event-level fees, rules, eligibility |
| drivendata | https://www.drivendata.org/competitions/ | Separate prize, benchmark and practice sections | All event-specific qualifications |
| topcoder | https://www.topcoder.com/challenges | Challenge directory retrieved, categories and registration filters visible | Individual dynamic challenge information; authentication alert appeared in extracted page |
| arcprize, arc-2026 | https://arcprize.org/competitions/2026 | “$2M in prizes. 3 tracks”; Nov 2 submissions, Nov 8 papers; open source required; no internet during Kaggle evaluation | Explicit free-entry requirement and full track eligibility |
| gems-2026 | https://www.drivendata.org/competitions/306/competition-doe-gems/ | Dec 3, 2026 11:59 p.m. UTC; $300,000 pool; $100,000 final first award | Explicit free entry and AI-assistance permissions |
| gems-2026 | https://docs.nlr.gov/docs/fy26osti/96647.pdf | §1.3: individual U.S. citizen/permanent resident; under 18/age of majority excluded; team and institutional restrictions; A.2: ACH banking and IRS W-9 within 30 days | No claim that this is an exhaustive legal eligibility summary |

Rules discovery chain: https://www.drivendata.org/competitions/306/competition-doe-gems/rules/ → https://www.herox.com/GEMSPrize/resource/2274 → https://www.nlr.gov/docs/fy26osti/96647.pdf (redirected to docs.nlr.gov).

## Upstream provenance

Original landing page retrieved: https://karagemop466-tech.github.io/FreeMoneyApps/ . Source HTML and JavaScript inspected using GitHub contents API. Snapshot commit: https://github.com/karagemop466-tech/FreeMoneyApps/commit/466f7c1e7a14b52b4a0d36beb84a00d68fd409b7 . Retained 206 listings and 45 removed records in upstream.json. Every normalized row was tested for source presence, unique identity, upstream coverage and blank unsupported fields. Unchecked URLs are pointers attributed to upstream, not independently established official ownership. No exhaustive external link audit or all-206 official rules audit is claimed.

## Specific flags

- Original header date differs from dataset date.
- Original “189 true free paths” is not independently reproduced or accepted.
- Original tax threshold statement is not reused.
- At least one inherited source (squarespool) uses HTTP; flagged without speculative URL repair.
- Counts include platforms/directories, not just individual contests.
- No ranking by expected earnings is possible from verified facts alone.

## Follow-up: independently checked Paper Track, 2026-11-01

| Row | Official source | Confirmed | Outstanding |
|---|---|---|---|
| arc-paper-2026 | [Kaggle Paper Track overview](https://www.kaggle.com/competitions/arc-prize-2026-paper-track) and [official rules](https://www.kaggle.com/competitions/arc-prize-2026-paper-track/rules) | Rules §2.4 explicitly says no purchase necessary; §1.5 guarantees $75,000 across three awards ($50k/$20k/$5k); overview sets 9 Nov 2026 at 23:59 UTC and requires an ARC-AGI-2 or ARC-AGI-3 submission plus writeup. | A participant must verify individual eligibility and linked prediction-track conditions; the possible $375k bonus is conditional. |
| gems-2026 | [Official NLR rules](https://docs.nlr.gov/docs/fy26osti/96647.pdf) §3.2 | Generative AI may be used in development, but use must be disclosed in the narrative. | Explicit no-fee clause was not located. |

The original summary's statement that there are zero fully qualified rows described the earlier snapshot, before these additional rules were inspected. One row now has a confirmed no-purchase cash path, not a universal eligibility guarantee. [The Premier League's Second Chance article](https://www.premierleague.com/en/news/4220308/the-second-chance-league-is-live-in-fantasy) lists merchandise, not cash, and is from the 2025/26 season. [Skillz terms link](https://www.skillz.com/terms-of-service/) returned an operator 404.

## Operator-pointer cleanup after live inspection

The original source ledger cited a social post for Valorant Pick'em and third-party Myfxbook articles for XM and Headway. The normalized table now points to the source-ledger operator sites (`valorantesports.com`, `xm.com`, `hw.online`), **not** as proof that those contests currently exist or pay cash. SquaresPool's original HTTP URL was updated to the HTTPS operator site after an [official page retrieval](https://www.squarespool.com/) succeeded. All four rows remain unverified. The source-ledger claim for each operator still needs independent event-level review.
