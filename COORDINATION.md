# Coordination — Own2

Shared task board for the Free Cash Prize Competitions site project.

## Active session

- Session ID: `arena-a310fb14-own2` (branch `arena/a310fb14-own2`)
- This is the only active session. All tasks below are claimed by this session.

## Task board

| # | Task | Status | Owner | Files touched | Sources / notes |
|---|------|--------|-------|---------------|-----------------|
| 1 | Data extraction: parse all 28 chunks of the source site into structured entries | done | arena-a310fb14-own2 | data/source_data.js, data/entries.json, tools/prepare_data.py | Source: https://karagemop466-tech.github.io/FreeMoneyApps/ (assets/data.js, pass S, reviewed 2026-08-19). 206 entries extracted; 12 have no official source and are flagged. |
| 2 | Executive summary | done | arena-a310fb14-own2 | executive-summary.html | Derived from task 1 data. |
| 3 | Site build: landing page + category subpages + tables | done | arena-a310fb14-own2 | index.html, categories/*.html, assets/css/style.css, assets/js/app.js, 404.html, .nojekyll | Static dashboard; filterable table of all 206 entries; one subpage per category. |
| 4 | Verification: every table row linked to an official source; unverified values blank + flagged | done | arena-a310fb14-own2 | data/entries.json, index.html, categories/*.html, flagged.html | 223 official / 15 affiliate / 4 forum source citations. 12 entries with NO official source have prize/cash-out fields blanked and are flagged UNVERIFIED. |
| 5 | "Flagged for Review" page (unverified / flagged items) | done | arena-a310fb14-own2 | flagged.html | 12 entries listed with source links; note on superseded 100_VERIFIED_CONTESTS.md included. |
| 6 | Integration: build check, broken-link check, GitHub Pages publish | in progress | arena-a310fb14-own2 | GitHub Pages settings | Local serve test + internal link check pending. Pages not yet enabled on GitHub. |
| 7 | PR from integration branch to main, merge, confirm Pages deploy, record result here | unclaimed | — | GitHub PR | PR link and merge result to be recorded below. |

## Irregularities log

- Source repo `100_VERIFIED_CONTESTS.md` is explicitly marked "SUPERSEDED — DO NOT USE AS A SOURCE" (failed verification; contained hallucinated entries such as Football Nation USA, USA TODAY Pro Football Survivor, NFL Pickwatch). Deliberately excluded. Maintained ledger = `assets/data.js` (pass S, reviewed 2026-08-19).
- 12 entries have no official source (all prize/cash-out fields blanked, flagged UNVERIFIED): fbs-pro-demo, npbfx-demo, roboforex-demo (market, affiliate-sourced); bona-fide, fantasy-arena, fplhub, fplmanager-india, fplstore, olka, pitchbooking, tff-fantezi-lig, thelines-survivor (sports, affiliate/forum-sourced).
- Affiliate-sourced prize tables: RoboForex, FBS, NPBFX demo contest figures come from review sites, not operator domains (flagged in entries).
- NPBFX has a 2019 non-payment allegation noted in source.

## Integration results

- PR link: (pending)
- Merge result: (pending)
- GitHub Pages deploy: (pending)

## Rules

- Claim a task by writing your session ID in the Owner column and commit/push that claim immediately.
- Never start a task another session has claimed.
- Each session edits only the files in its claimed scope (or its own branch/worktree).
- If a task requires changing a file owned by another session, log the request here instead of editing it.
- Make small, frequent commits; run `git pull --rebase` before every push.
- Mark a task done only after verification against official sources, with sources linked.
- Flagged irregularities and unverified items do not block the merge; they are published on the "Flagged for Review" page.
