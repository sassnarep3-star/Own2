# PrizeDesk

Evidence-first, mobile-friendly competition research dashboard. No framework, dependencies, accounts, trackers or affiliate links.

- Live site: https://sassnarep3-star.github.io/Own2/
- Executive summary: `summary.html`
- Uncertainties: `review.html`
- 206 inherited leads + 2 event records; no fully qualified free-entry cash contest is claimed.

## Reproduce

```sh
python scripts/build.py
python scripts/test.py
python -m http.server 8000 --bind 0.0.0.0
```

Edit `data/contests.json` and `scripts/build.py`, then regenerate. Generated HTML includes the full tables so content works without JavaScript; JavaScript adds filtering. Category pages are real static subpages. Blank cells are intentionally unverified. Evidence dates apply only to the fields documented, not to every claim about a platform.

`data/upstream.json` preserves the supplied ledger's assertions for traceability, not endorsement. Upstream snapshot: https://github.com/karagemop466-tech/FreeMoneyApps/tree/466f7c1e7a14b52b4a0d36beb84a00d68fd409b7 . External URLs on unverified rows are inherited destinations and have not all been authenticated or checked for availability. Internal links are tested. This is not a complete external-link or rules audit.

GitHub Pages serves the root of `main` (existing repository configuration). No third-party runtime assets required. See COORDINATION.md for ownership, checks, PR and deployment results.


## Additional official-source findings — 1 November 2026

- The starting repository contained only a placeholder README. The [external Free Money & Contest Ledger](https://karagemop466-tech.github.io/FreeMoneyApps/) contains **206** listings across nine categories, but its self-reported “189 true free paths” is **not** a verified count. Its records mix contests, discovery directories, pool tools, non-cash prizes, pay-to-enter products, and old seasons. We imported **all 206 as unverified research leads**, preserving original-record links and operator/cited URLs but blanking unconfirmed prize, fee, deadline, and eligibility fields.
- **One current opportunity meets the documented free-entry cash-prize standard:** [ARC Prize 2026 Paper Track](https://www.kaggle.com/competitions/arc-prize-2026-paper-track/rules). Its official rules explicitly say “NO PURCHASE NECESSARY” (§2.4) and specify **$75,000** in guaranteed awards (§1.5); the [overview](https://www.kaggle.com/competitions/arc-prize-2026-paper-track) gives **9 November 2026, 23:59 UTC** as the deadline. Entry requires a prior submission to ARC-AGI-2 or ARC-AGI-3 and a public writeup/notebook. A possible $375,000 bonus is **conditional**, not counted in the guaranteed prize figure. For agent-assisted work, review competition-specific code-sharing, originality, and eligibility provisions before participating.
- **One technically promising but incomplete lead:** the [GEMS Prize challenge](https://www.drivendata.org/competitions/306/competition-doe-gems/) specifies **$300,000** in cash awards and a **3 December 2026, 23:59 UTC** deadline. [Official rules](https://docs.nlr.gov/docs/fy26osti/96647.pdf) §§1.1, 1.3 and 3.2 describe prize structure, U.S. eligibility and permitted generative AI use **with disclosure**. No explicit entry-fee statement was found, so it is **not** labeled confirmed free. Its eligibility makes it a potentially relevant project for a U.S.-based technical team, subject to the full rules.
- **Important correction:** the [Premier League’s Second Chance article](https://www.premierleague.com/en/news/4220308/the-second-chance-league-is-live-in-fantasy) lists merchandise, not a cash award; the linked 2025/26 season is not a current cash contest. The source ledger’s [Skillz terms URL](https://www.skillz.com/terms-of-service/) returned a 404 page on review. Several FPL mini-league entries cite third-party roundups rather than league-specific official rules. See the [Flagged for Review page](https://sassnarep3-star.github.io/Own2/flagged/) for all records and limitations.

**Decision rule:** prioritize a competition only after its official rules confirm a no-purchase cash path, an open deadline, eligibility, and acceptable AI/tool use. Prize pools measure maximum available awards, not expected value; no success rate or ROI can be inferred from available evidence. Recheck all rules immediately before entering.


## Two complementary views

The existing [PrizeDesk dashboard](index.html) is retained and now incorporates the independently verified Paper Track row. The new [focused shortlist](explore.html) offers a simpler mobile-first view with a separate category research backlog. Both views identify unchecked leads and point to the [Flagged for Review](flagged/index.html) inventory.
