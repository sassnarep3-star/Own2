# analysis-02aa8a4d/ — "Time well spent" analysis subsite

Independent analysis pass by session **arena-02aa8a4d** (2026-11-02). Complements the shared
209-row catalog on the [main dashboard](../index.html) with three deliverables:

1. **Freshness sweep** (`freshness.html`) — 19 official pages re-read on 2026-11-02; every cell quote-backed or blank.
2. **Ranked picks** (`ranked.html`) — evidence-only priority scores (rubric on `methodology.html`) answering *"where should I spend my competition time?"*.
3. **Link health** (`link-health.html`) — recheck of previously flagged broken external links + repo-wide internal link scan (160 pages, 0 broken).

Also: `all.html` (all 209 entries in one table), 9 category pages, `flagged.html` (irregularities),
`summary.html` (executive summary), `EXECUTIVE_SUMMARY.md`, `verification-log.md` (line-by-line sources).

## Evidence policy

Only quote+URL-backed values from official pages are published. Unconfirmed values stay blank and are
stamped unverified. Nothing is inferred. Every table row carries a source link or an explicit
"no official source" stamp. Scoring can never override this: free entry, cash prize, and open status
each require verbatim quotes before a row can reach tier A.

## Build & check

```bash
python3 analysis-02aa8a4d/build.py   # deterministic static build (writes only inside this dir)
python3 analysis-02aa8a4d/check.py   # evidence policy, links, counts, score math, determinism
```

Data: `data/freshness.json` (V1 sweep), `data/link-recheck.json` (V3 recheck). Both include verbatim
quotes and URLs. Generated reports: `reports/stats.json`, `reports/link-health.json`.

## Scope

Files owned by this session: `analysis-02aa8a4d/**` and its append-only section in `COORDINATION.md`.
No shared dataset, page, or other session's files were modified. No contest accounts, entries,
deposits or prize claims were made.
