# Coordination board

Session: arena-f72a1743 (integration). Required working branch: `arena/f72a1743-own2`; platform branch restriction takes precedence over requested session branch naming.

| Task | Status | Owner | File scope |
|---|---|---|---|
| Inspect original ledger and official evidence; build and validate dashboard; integrate and deploy | needs review | arena-f72a1743 | Prior implementation merged in PRs #1–2; original verification gaps remain on review.html |
| Integrate additional official-rule findings and complementary shortlist; revalidate Pages | in progress | 582a1199-own2 | COORDINATION.md, README.md, index.html, explore.html, assets/, category/, data/catalog.json, data/contests.json, data/EVIDENCE.md, flagged/, scripts/, .github/workflows/validate.yml |

## Log
- 2026-11-01: Repository inspected: only a six-byte README, no existing application or coordination board; no other claims found. Single integration session claims the complete initial implementation. Unknown facts will remain blank and be flagged. No other session branches will be created.
- Initial pull of the session branch failed because it did not exist remotely yet; rebased against origin/main and pushed the claim successfully. No merge conflict or other-session work encountered.
- 2026-11-01: Implementation completed: 13 static pages, 9 categories, 208 normalized records (206 retained leads + two specific event records), mobile breakpoints, searchable/filterable tables, executive summary and Flagged for Review. All inherited unsupported values blanked; full original assertions retained only in labeled archive.
- Sources and exact verification scope: data/EVIDENCE.md. Eight partial-evidence records; zero fully qualified opportunities. All 208 records published as needs review because free-entry confirmation remains missing. External destinations on unchecked rows are inherited and may be broken; not represented as verified. HTTP source specifically flagged.
- Validation: python scripts/build.py; python scripts/test.py; all local href/src destinations exist, 206/206 upstream listing coverage, unique IDs, blank unsupported values, JavaScript syntax, viewport/language metadata. Preview server responds on port 8000. No automated real-browser visual test performed. No full external-link health check claimed.
- PR https://github.com/sassnarep3-star/Own2/pull/1 merged successfully at 2026-11-01T13:44:50Z, merge commit 5c37dd53dac849c88655ce470be774591eb9da34. GitHub Pages deployment run 41312740175 succeeded; published landing page retrieved successfully at https://sassnarep3-star.github.io/Own2/ with expected 208-row dashboard.
- Final live-content inspection found that selecting upstream rulesUrl could prefer an affiliate explainer (Fanatics). Follow-up uses upstream sources explicitly tagged official, falling back to signup URL. Ownership/authenticity remains unverified for unchecked rows. No affiliate explainer is intentionally preferred over an available official pointer.
- Implementation and local validation: done. Full official verification and external-link audit: needs review, published at review.html; not falsely marked done.

- Final follow-up PR: https://github.com/sassnarep3-star/Own2/pull/2. Review queue is public and nonblocking; implementation delivered.

## Session 582a1199-own2 (post-merge follow-up)

- 2026-11-01: Independent session initially claimed the integration scope before seeing any other claim on `main`. During PR #3 integration, fetched `main` and discovered session `arena/f72a1743-own2` had meanwhile merged PRs #1 and #2. This is overlapping scope, not evidence of an abandoned claim. Retain that session's work; integrate the additional verified ARC Paper Track evidence without deleting its implementation. Arena fixes this session's branch name to `arena/582a1199-own2`.
- Conflict log: `git rebase origin/main` encountered add/add `COORDINATION.md` at claim commit. Preserved the other session's full board and appended this handoff note; no work discarded. Shared output work is now final integration of both sessions. File scope: `COORDINATION.md`, `README.md`, `index.html`, `assets/**`, `category/**`, `data/catalog.json`, `flagged/**`, `scripts/*.{cjs}`, `.github/workflows/pages.yml`, `.nojekyll`; existing root category pages, root JS/CSS, and Python builder are retained.

## 2026-11-01 verification and integration record

- Source inventory: imported 206 unique IDs in nine categories from [external source data](https://github.com/karagemop466-tech/FreeMoneyApps/blob/main/assets/data.js); original entries are **unverified**. This is a completeness check against that source, **not** line-by-line verification of 206 operator claims. 13 source records have no HTTPS operator-designated rules citation, but each catalog row has an operator/platform URL and a link to its original entry. Blank value fields are intentional.
- Checked against official source: [ARC Prize Paper Track overview](https://www.kaggle.com/competitions/arc-prize-2026-paper-track) and [rules](https://www.kaggle.com/competitions/arc-prize-2026-paper-track/rules), particularly rules §1.5 and §2.4. Confirmed cash award, no-purchase entry, 2026-11-09 deadline, and prior ARC challenge submission requirement. Optional bonus excluded from guaranteed prize pool.
- Checked against official source: [GEMS challenge](https://www.drivendata.org/competitions/306/competition-doe-gems/) and [official NLR rules PDF](https://docs.nlr.gov/docs/fy26osti/96647.pdf), §§1.1, 1.3, 3.1–3.2. Confirmed pool, deadline, eligibility, AI-use disclosure; **free entry not confirmed** and marked partial.
- Irregularities: [Premier League Second Chance article](https://www.premierleague.com/en/news/4220308/the-second-chance-league-is-live-in-fantasy) offers merchandise (not cash) and concerns 2025/26; [Skillz terms link](https://www.skillz.com/terms-of-service/) resolves to the operator's 404 page; [Papaya FAQ](https://www.papaya.com/faq) distinguishes free Gems from cash competitions; [SquaresPool HTTPS page](https://www.squarespool.com/) describes a pool tool, not an operator-funded cash prize. FPL mini-league and third-party-only citations are not sufficient proof. All remain flagged on the site.
- Static QA: `node scripts/check.cjs` passed: 11 pages, 206 source records, two independently checked shortlist rows, no missing local links, no nonempty unverified fact cells. Local HTTP GET for `/index.html` and `/category/tech.html` returned 200. **External links have not been exhaustively checked**; neither their availability nor content should be assumed current.
- Deployment task remains in progress until a successful Pages deployment is confirmed. This sentence described the pre-rebase snapshot; superseded by the handoff log above. The prior session merged first; this branch has been rebased on it without deleting its work.

- 2026-11-01 integration: Rebasing on merged PRs #1–2 caused conflicts in COORDINATION.md, README.md and index.html. Preserved the earlier root dashboard and both audit histories; published the complementary mobile shortlist as explore.html. Updated the earlier builder and dataset to 209 records (206 historical + 3 event-level), including the officially confirmed ARC Paper Track. Its 208 unresolved rows remain flagged. Re-ran `python scripts/build.py`, `python scripts/test.py`, `node scripts/build-pages.cjs`, and `node scripts/check.cjs` successfully. Existing Pages source is legacy main-root, so removed a redundant workflow and extended existing validation workflow. External URLs are not exhaustively audited.
- Push coordination: `git pull --rebase origin arena/582a1199-own2` after rebasing onto newly merged `main` attempted to replay the old session-branch history against the newer integrated history and hit a COORDINATION.md add/add conflict. Aborted that redundant rebase; confirmed the current branch already contains all merged-main commits and both sessions' records. The session branch alone will be updated with `--force-with-lease` (never `main`) to reflect the intentional rebase, without discarding upstream work.
## Session arena-05a44eaa: independent verification supplement

| Task | Status | Owner | File scope |
|---|---|---|---|
| Additional official-source checks, independent executive audit supplement, deployment confirmation | in progress | arena-05a44eaa | audits/2026-11-01/**; this session's append-only COORDINATION.md log |

- 2026-11-01: Read existing board and rebased onto merged PR #1 (5c37dd5). Initial integration scope remains owned by arena-f72a1743; no existing application/data/build files will be edited. Fixed platform branch is arena/05a44eaa-own2. This supplement uses a separate directory and does not duplicate initial implementation.
- Integration request to arena-f72a1743: when available, link audits/2026-11-01/index.html from the shared summary/navigation after supplement merge; shared files will not be changed by this session.

- 2026-11-01: Rebase onto updated main encountered append-only COORDINATION.md conflict. Paused and resolved by retaining both the prior integration publication log and this session’s complete claim; no other-session content discarded.
- 2026-11-01: Supplement implemented in five static audit pages (landing, creative, gaming, research, Flagged for Review). Thirteen inherited leads checked against organizer/government pages; two explicit free-entry/cash paths documented without claiming complete legal or payment qualification. Sources, excerpts, adopted fields and remaining flags: audits/2026-11-01/evidence.json and REPORT.md. Source links present on every row. No shared dataset or application file edited.
- Verification: python scripts/build.py; python scripts/test.py; python audits/2026-11-01/build.py; python audits/2026-11-01/test.py. Passed deterministic builds, 13 upstream IDs, exact schema, blank unsupported cells, per-row sources, all local destinations, viewport/table accessibility metadata and JS syntax. Nine representative pages also passed real Chromium/Playwright at 390px and 1440px: no page-level horizontal overflow, root search/reset (1 Wergle match; 208 after reset), no JS exceptions or local HTTP resource errors. Mobile screenshot visually inspected. Browser binaries/dependencies remain outside Git.
- Important supplement flags: Wergle AI-generated text prohibited; Sony photograph-origin required; GamerSaloon Bonus Cash not withdrawable; Tom Howard poetry fee; NYPL open-label/date conflict; CMG claim-window and region conflicts; Challenge.gov retired; Zindi retrieved error-page content; Film rules resolves to Photo rules. Full 206-row external-link/legal verification remains explicitly incomplete and published as needs review.
- Earlier main GitHub Pages build confirmed built at 5c37dd5 via API. Supplement release/deploy confirmation follows below.
- 2026-11-01: A second append-only board conflict occurred while rebasing onto merged integration PR #3 (51bda6d). Retained all of session 582a1199-own2’s board/history and this supplement; no other-session work discarded. Revalidated combined current main: Python build/test, Node alternate-site build/check, and supplement build/test all pass with no generated diff. Repeated browser tests at 390/1440px; search reset now correctly returns 209 root records after the other session’s ARC Paper Track addition. Prior 208 count above describes the earlier snapshot, not the current site.
- Integration request updated for owner 582a1199-own2: link the independent audit at audits/2026-11-01/index.html and incorporate its field-specific findings when editing shared navigation/data. No shared-file edits made here.

---

## Session arena-205d508d · ledger verification subsite (appended; no other session's entries edited)

Fixed platform branch for this session: `arena/205d508d-own2` (the requested `session-<id>/<task>` naming is not available here; all tasks live on this branch).

| Task | Status | Owner | File scope |
|---|---|---|---|
| T1 Repo review and irregularity log | done | 205d508d | `ledger-verification/data/review.json` (irregularities R1–R18) |
| T2 Snapshot upstream ledger (206 listings) | done | 205d508d | `ledger-verification/data/source/ledger-data.js` (unmodified upstream `assets/data.js`, commit `466f7c1e`) |
| T3 Official-source verification | needs review | 205d508d | `ledger-verification/data/review.json`. 11 of 206 rows checked on official pages; 195 unverified, prize blank, flagged. |
| T4 Subsite build: landing, 9 category pages, all entries, Flagged for Review, executive summary, methodology | done | 205d508d | `ledger-verification/**` |
| T5 Check workflow | done | 205d508d | `.github/workflows/ledger-verification.yml` (new file; the other workflow is untouched) |
| T6 Integration of the subsite into `main` by PR; Pages confirmation | in progress | 205d508d | this section of `COORDINATION.md`, `ledger-verification/**` |

### Coordination decisions

- **Scope isolated.** Only `ledger-verification/**`, the new `.github/workflows/ledger-verification.yml`, and this appended section were changed. Root `index.html`, `README.md`, `data/*.json`, `scripts/*`, `category/`, `audits/`, `flagged/`, `explore.html`, `assets/` and `validate.yml` are untouched.
- **Pages not changed.** Pages is `legacy`, source `main` `/` (checked with `gh api repos/sassnarep3-star/Own2/pages`). This subsite is served from the repo root as `/ledger-verification/`. The deploy workflow this session first added (`pages.yml`) was removed for that reason, as the other session noted for its own build.
- **Merge conflicts.** `COORDINATION.md` (add/add) and `README.md` conflicted with `origin/main`. Resolved by keeping `origin/main`'s version in full and appending this section. No other session's work was discarded.
- **Other open PRs not touched:** #4 (`arena/36a6db9e-own2`, open) and #6 (`arena/582a1199-own2`, open).

### Integration request (for the owner of shared navigation)

- Please link `ledger-verification/index.html` from the root navigation, and `ledger-verification/flagged.html` from the Flagged for Review page. This session did not edit shared navigation.

### Sources and verification (2026-11-01)

Official pages read on 2026-11-01, with the rows they support:

- ESPN NFL Pick'em 2026: https://fantasy.espn.com/games/nfl-pickem-2026/picks (`espn-pickem`: $102,000, 58 prizes, dates, status live)
- ESPN College Pick'em 2026: https://fantasy.espn.com/games/college-football-pickem-2026/picks (`espn-cfb`: $86,000, 46 prizes, dates, live)
- ARC Prize homepage: https://arcprize.org/ (`arcprize`: $2,000,000 in prizes)
- MLB Beat the Streak: https://www.mlb.com/apps/beat-the-streak and rules (`mlb-beat-the-streak`: $5.6M prize confirmed; end date conflicts with "live")
- Metaculus: https://www.metaculus.com/tournaments/ (`metaculus`: partial)
- CBS Pro Football Pick'em rules: https://www.cbssports.com/fantasy/football/games/pickem/rules (`cbs-pro-pickem`: partial)
- Devpost hackathons: https://devpost.com/hackathons (`devpost`: partial)
- Kaggle competitions: https://www.kaggle.com/competitions (`kaggle`: conflict, range understated)
- Checkmate Gaming free tournaments: https://www.checkmategaming.com/free-tournaments (`checkmate-gaming`: conflict, prize range)
- The Draft Pro release (PR Newswire): https://www.prnewswire.com/news-releases/the-draft-pro-launches-free-1-000-000-perfect-draft-challenge-ahead-of-the-2026-nfl-draft-302736409.html (`draft-pro`: status conflict)
- Gambling.com (redirect target of the Dirty Dozen link): https://www.gambling.com/games (`dirty-dozen`: broken link)

Upstream: https://github.com/karagemop466-tech/FreeMoneyApps (commit `466f7c1e7a14b52b4a0d36beb84a00d68fd409b7`).

### Irregularities (full list with links: `ledger-verification/flagged.html`, section A)

- High: no licence (upstream and here); ledger data stale (2026-08-19); sportsbook and casino entries conflict with the source's own exclusion policy, including two featured entries; Dirty Dozen link broken; draft-pro status conflict.
- Medium: Checkmate Gaming and Kaggle prize conflicts; MLB end date; 13 third-party league entries with misattributed links; affiliate-only prize sources (three broker demo contests); annual photo awards not re-checked.
- Low: promo codes present in ledger data (not published); undocumented iOS count (reconciled); ESPN link redirects; six rows with no rules link.

### Validation

- `node ledger-verification/tools/build.mjs` and `node ledger-verification/tools/check.mjs`: pass. 206 rows on all-entries; 206 across categories; 15 pages; no broken internal links; unverified prizes blank; evidence present on checked rows.
- Build is deterministic (repeat build produces identical HTML).
- External links are not exhaustively checked. Only the official pages listed above were read.

### PR and merge

- PR and merge result: recorded in the PR description and the session summary (see below, appended after merge).
