# Executive summary — PrizeLens

**Audit date:** 2026-11-02  
**Live site:** https://sassnarep3-star.github.io/Own2/ledger-9a715523/

## Bottom line

Use a small, rules-first shortlist rather than chasing headline prize pools. The inherited ledger has **206 listings** across **nine categories**. This isolated view retains every identity, adds **18 event-level official-source reviews**, and identifies **12 event records** with both free-entry and cash evidence plus a published open/closing window. This is not a personal-eligibility guarantee, a zero-practical-cost claim or an expected-earnings ranking.

## Recommended research order

1. **Kiroween:** explicit Kiro agent/spec/hook workflow; $30,000 first prize; closes 4 Dec 2026 at 2:00 pm Pacific. Public open-source GitHub repo and demo required. [Official rules](https://kiroween.devpost.com/rules).
2. **UGREEN AI NAS:** Singapore explicitly listed; Round 1 needs a concise PDF and initial skill ZIP, not a demo or NAS runtime. $20,000 top cash award. Only finalists get hardware access; outside-person development is barred. [Official rules](https://ugreenhackathon.devpost.com/rules).
3. **Codegeist, PayPal and NFL Big Data Bowl:** documented cash and no-fee clauses, but AI/technical-assistance language is not blanket coding-agent authorization. Check ownership, tool costs and reproducibility before building. [Codegeist](https://codegeist2026.devpost.com/rules), [PayPal](https://paypalaihackathon.devpost.com/rules), [NFL](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/rules).

Ordering is editorial, based on explicitness of the agent path, submission requirements and runway. No win probability, hourly return or expected value is asserted.

## Findings that change participation

- ESPN and CBS prohibit automated entries/point accumulation and exclude Singapore residents from prize eligibility. [ESPN rules](https://fantasy.espn.com/games/nfl-pickem-2026/howtoplay), [CBS rules](https://www.cbssports.com/fantasy/football/games/pickem/rules).
- Sony entries must originate from photographs; Wergle Flomp forbids AI-generated poem text. [Sony](https://www.worldphoto.org/sony-world-photography-awards/single-image), [Wergle](https://winningwriters.com/our-contests/wergle-flomp-humor-poetry-contest-free).
- FutureEval is explicitly bot-only, but general payout rules allow cash equivalents; its cash field is blank and it is excluded from the strict cash shortlist. [Rules](https://www.metaculus.com/tournament-rules/).
- Meta VR Start requires program membership despite a no-purchase clause; practical membership cost is unconfirmed. [Rules](https://start-developer-competition-26.devpost.com/rules).
- The old Codegeist URL serves 2024 rules; the current event uses `codegeist2026.devpost.com`. ARC’s overview and Kaggle paper track disagree on the paper deadline; the combined deadline is blank.

## Verification and limits

- Pinned upstream commit: `466f7c1e7a14b52b4a0d36beb84a00d68fd409b7`. Downloaded data matches the existing source snapshot by SHA-256.
- Every inherited row is retained once. Unsupported prize, free-entry, deadline, eligibility, payout and AI fields are blank and flagged. Seven rows still lack a confirmed official source.
- Event cells are supported by exact official excerpts in `research/events.json` and the public Source Notebook. Only cited passages support published values.
- External reachability is a separate network observation, not content verification. Blocked/timeouts are inconclusive; HTTP 200 can still be a stale or non-cash page.
- No contest account, entry, deposit, payment or prize claim was made. Personal eligibility and actual payout were not tested.

## Repository irregularities

The repo contains multiple parallel sites and historical coordination claims. This session preserves them and edits only its isolated namespace, unique workflow and append-only board section. Root summary counts are stale relative to the root checker; a correction is requested from the shared owner. Upstream has no detected license, and `100_VERIFIED_CONTESTS.md` explicitly says it failed verification and must not be used as a source.

See the public **Flagged for Review**, **Source Notebook**, **Repository Audit** and `COORDINATION.md` for the full trail.
