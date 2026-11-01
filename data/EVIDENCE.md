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
