# Legacy builder (superseded 2026-11-01)

`build_root_dashboard.py` and `test_root_dashboard.py` built the first root dashboard
(208 rows, every value blank, all rows "needs review"). The integration session
`arena-f10345ed` replaced that dashboard with the evidence-backed build in
`scripts/build_site.py` / `scripts/check_site.py`, which reads the same
`data/upstream.json` plus per-entry evidence in `data/evidence/`.

The scripts are kept, unmodified, for traceability. They are **not** run by CI: they
would regenerate pages from the superseded `data/contests.json` schema and overwrite
the current site. The parallel audit pages in `audits/2026-11-01/` and the alternate
shortlist site (`explore.html`, `category/`, `flagged/`, built by `scripts/build-pages.cjs`)
are untouched and still reproducible.
