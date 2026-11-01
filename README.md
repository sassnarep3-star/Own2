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
