# Coordination board

Session: arena-f72a1743 (integration). Required working branch: `arena/f72a1743-own2`; platform branch restriction takes precedence over requested session branch naming.

| Task | Status | Owner | File scope |
|---|---|---|---|
| Inspect original ledger and official evidence; build and validate dashboard; integrate and deploy | needs review | arena-f72a1743 | Prior implementation merged in PRs #1–2; original verification gaps remain on review.html |
| Integrate additional official-rule findings and complementary shortlist; revalidate Pages | done | 582a1199-own2 | COORDINATION.md, README.md, index.html, explore.html, assets/, category/, data/catalog.json, data/contests.json, data/EVIDENCE.md, flagged/, scripts/, .github/workflows/validate.yml |
| Integration pass 2: official-source verification, mobile-first dashboard rebuild, executive summary, deploy | in progress | arena-f10345ed | COORDINATION.md, README.md, EXECUTIVE_SUMMARY.md, index.html, contests.html, summary.html, review.html, category root pages, app.js, style.css, 404.html, data/categories.json, data/contests.json, data/evidence/**, data/EVIDENCE.md, scripts/build_site.py, scripts/check_site.py, .github/workflows/validate.yml |

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
| Additional official-source checks, independent executive audit supplement, deployment confirmation | needs review | arena-05a44eaa | audits/2026-11-01/**; this session's append-only COORDINATION.md log |

- 2026-11-01: Read existing board and rebased onto merged PR #1 (5c37dd5). Initial integration scope remains owned by arena-f72a1743; no existing application/data/build files will be edited. Fixed platform branch is arena/05a44eaa-own2. This supplement uses a separate directory and does not duplicate initial implementation.
- Integration request to arena-f72a1743: when available, link audits/2026-11-01/index.html from the shared summary/navigation after supplement merge; shared files will not be changed by this session.

- 2026-11-01: Rebase onto updated main encountered append-only COORDINATION.md conflict. Paused and resolved by retaining both the prior integration publication log and this session’s complete claim; no other-session content discarded.
- 2026-11-01: Supplement implemented in five static audit pages (landing, creative, gaming, research, Flagged for Review). Thirteen inherited leads checked against organizer/government pages; two explicit free-entry/cash paths documented without claiming complete legal or payment qualification. Sources, excerpts, adopted fields and remaining flags: audits/2026-11-01/evidence.json and REPORT.md. Source links present on every row. No shared dataset or application file edited.
- Verification: python scripts/build.py; python scripts/test.py; python audits/2026-11-01/build.py; python audits/2026-11-01/test.py. Passed deterministic builds, 13 upstream IDs, exact schema, blank unsupported cells, per-row sources, all local destinations, viewport/table accessibility metadata and JS syntax. Nine representative pages also passed real Chromium/Playwright at 390px and 1440px: no page-level horizontal overflow, root search/reset (1 Wergle match; 208 after reset), no JS exceptions or local HTTP resource errors. Mobile screenshot visually inspected. Browser binaries/dependencies remain outside Git.
- Important supplement flags: Wergle AI-generated text prohibited; Sony photograph-origin required; GamerSaloon Bonus Cash not withdrawable; Tom Howard poetry fee; NYPL open-label/date conflict; CMG claim-window and region conflicts; Challenge.gov retired; Zindi retrieved error-page content; Film rules resolves to Photo rules. Full 206-row external-link/legal verification remains explicitly incomplete and published as needs review.
- Earlier main GitHub Pages build confirmed built at 5c37dd5 via API. Supplement release/deploy confirmation follows below.
- 2026-11-01: A second append-only board conflict occurred while rebasing onto merged integration PR #3 (51bda6d). Retained all of session 582a1199-own2’s board/history and this supplement; no other-session work discarded. Revalidated combined current main: Python build/test, Node alternate-site build/check, and supplement build/test all pass with no generated diff. Repeated browser tests at 390/1440px; search reset now correctly returns 209 root records after the other session’s ARC Paper Track addition. Prior 208 count above describes the earlier snapshot, not the current site.
- Integration request updated for owner 582a1199-own2: link the independent audit at audits/2026-11-01/index.html and incorporate its field-specific findings when editing shared navigation/data. No shared-file edits made here.

- PR #3 https://github.com/sassnarep3-star/Own2/pull/3 merged to main at 2026-11-01T13:48:08Z (merge commit `51bda6d7a2633bf00b54fec80bada4a7cc397ff8`). Validation run `41313016227` succeeded. Pages deployment run `41313015897` succeeded; Pages API latest build reports `built` for the same merge commit. Live https://sassnarep3-star.github.io/Own2/?v=51bda6d7 displayed 209 records and the confirmed Paper Track; https://sassnarep3-star.github.io/Own2/explore.html and /flagged/ also loaded.
- Follow-up cleanup: three inherited source links pointed to external press/social sites and one used HTTP. Replace only their table source pointers with the source-ledger operator HTTPS sites; these rows remain unverified. Unresolved bulk verification and external-link audit remain **needs review**, published at review.html and flagged/. This follow-up will be submitted and deployed separately.
- 2026-11-01 RELEASE COMPLETE: PR https://github.com/sassnarep3-star/Own2/pull/5 merged without waiting for review at 13:49:18Z, merge commit 72afa9147a504030144da21d0a38e4f078d01946. CI validate passed. GitHub Pages deployment https://github.com/sassnarep3-star/Own2/actions/runs/41313110631 succeeded; Pages build API confirms built for that commit. Live audit landing and Flagged for Review pages retrieved successfully with the expected findings: https://sassnarep3-star.github.io/Own2/audits/2026-11-01/ and https://sassnarep3-star.github.io/Own2/audits/2026-11-01/review.html . Implementation, targeted checks and publication are done; status needs review refers solely to the explicit nonblocking source/qualification uncertainties published there. No claim of complete all-206 verification.

- Final publication-record PR #7 encountered a concurrent append conflict after PR #6 merged. Paused, retained both sessions’ complete deployment logs, and rebased; no application files changed or other-session work discarded.

## Session be1d2210 (independent "verified-or-blank" dashboard at `/dashboard/`)

| Task | Status | Owner | File scope |
|---|---|---|---|
| Repo review of karagemop466-tech/FreeMoneyApps + offline audit (T1, T2) | done | be1d2210 | `dashboard/audit/**`, `dashboard/data/raw/**`, `dashboard/tools/{extract,audit}.js` |
| Live verification of 13 entries against official pages (T3) | done for 13; remaining 191 → **needs review** (unclaimed follow-up T7) | be1d2210 | `dashboard/data/verification/**` |
| Site, executive summary, flagged page (T4, T5) | done | be1d2210 | `dashboard/**` only |
| Integration PR → main, merge, Pages check (T6) | in progress → see log | be1d2210 | `dashboard/**`, this file (append-only) |

- 2026-11-01: **Overlap note.** This session started from the initial commit (empty repo; board did not exist on that snapshot) and worked in isolation. When opening the PR it found that sessions f72a1743, 582a1199 and 05a44eaa had already merged full sites (PRs #1–#7) at the repository root. Rather than overwrite them, this session moved its entire site into `dashboard/` (an independent site; the project brief expects multiple sites), merged `origin/main` into its branch (only conflict: `README.md` modify/delete → kept the other session's README; `COORDINATION.md` taken from main and appended here), and edited **no** file outside `dashboard/` except this append-only log.
- Sources & verification (details: `dashboard/data/verification/verified.json`, `dashboard/audit/SOURCE_REPO_REVIEW.md`): source ledger at karagemop466-tech/FreeMoneyApps commit 466f7c1e7a14b52b4a0d36beb84a00d68fd409b7; official pages fetched live 2026-11-01 for arcprize.org, kaggle.com (competitions index + ARC-AGI-2), devpost.com/hackathons, drivendata.org/competitions, metaculus.com/tournaments, fantasy.espn.com (NFL Pick'em, Survivor), cbssports.com Pro Football Pick'em rules (chunks 0–1 of 5), checkmategaming.com/free-tournaments, aicrowd.com ARC White-Box, mlb.com Beat the Streak, fantasygames.nascar.com rules (chunk 0 of 5), tradingview.com/the-leap (chunk 0 of 3). Topcoder and Zindi returned no content (JS-only). 11 of 13 readable entries show a discrepancy or unconfirmable figure vs the old ledger.
- Checks run after merging main: `python scripts/build.py`, `python scripts/test.py`, `node scripts/check.cjs` (other sessions' checks) all pass with no generated diff; `node dashboard/tools/build.js`, `linkcheck.js` (17 pages, 801 internal links, 412 rows each with an official link, 0 problems) and `check-consistency.js` (0 problems) pass. External link-rot not measurable here (network allow-list); `dashboard/tools/linkcheck-external.js` provided.
- Cross-session findings: arcprize.org states Paper Track papers due 2026-11-08 while session 582a1199 reports 2026-11-09 from the Kaggle rules → logged as a discrepancy on `dashboard/flagged.html`. Our GEMS finding (free entry not confirmed) matches 582a1199's.
- **Integration requests (not performed by this session, per scope rules):** (1) owner of root `index.html`/navigation: add a link to `/dashboard/`; (2) owner of `.github/workflows/validate.yml`: optionally append `node dashboard/tools/build.js && node dashboard/tools/linkcheck.js && node dashboard/tools/check-consistency.js`.
- Irregularities: `dashboard/flagged.html` sections A–E. Not blocking.


## Session arena-f10345ed — integration pass 2 (claim, work, conflict log)

**Claim (pushed before any file work):** branch `arena/f10345ed-own2`, commit `76f3310`.
Scope: the root dashboard, its generated pages, `data/evidence/**`, the two build/check scripts, README and the
executive summary. Explicitly **not** touching `audits/**`, `assets/**`, `category/**`, `flagged/**`,
`explore.html`, `data/catalog.json` or `scripts/*.cjs`, which belong to other sessions.

**What was built**

- `data/evidence/*.json` — one record per entry read in this pass: field status (confirmed / contradicted /
  not stated / not found), a verbatim quote, the URL, the check date, flags. 19 entries written by this session;
  a further 8 records were merged from the parallel audit in `audits/2026-11-01/evidence.json` (session
  `arena-05a44eaa`), attributed per row, bringing evidence coverage to 27 of 209 rows.
- `scripts/build_site.py` — merges `data/upstream.json` with the evidence and regenerates the site. It publishes
  a value only when a quote and an http(s) URL exist; otherwise the cell stays blank and the row is flagged.
- `scripts/check_site.py` — enforces: all 206 upstream listings retained and unique; every published field has a
  quote + URL; no row labelled unverified publishes values; every row without an official source is flagged;
  deterministic rebuild; every local link resolves; every page has charset/viewport/lang; category row counts
  match the dataset; `app.js` passes `node --check`.
- Pages rebuilt mobile-first: `index.html` (dashboard, confirmed deadlines, category cards), `contests.html`
  (all 209 rows with search, category/verification/free/cash filters, sorting and a per-row evidence panel),
  nine category pages, `summary.html` (executive summary), `review.html` (every unresolved item with its link),
  `404.html`. `data/EVIDENCE.md` and `EXECUTIVE_SUMMARY.md` are generated/written from the same records.
- 8 rows are fully verified (free entry **and** cash, window open), 7 of them usable now. 191 rows remain
  unverified and blank, as before, but now with a visible reason per row.

**Merge conflict encountered and how it was resolved (no work discarded)**

`git pull --rebase origin main` conflicted on `COORDINATION.md`: main had advanced from `5c37dd5` to `dba55fd`
while this session worked (PRs #2–#7, sessions `582a1199-own2` and `arena-05a44eaa`). The rebase was aborted
(rather than resolving inside a replay), and `origin/main` was merged into the session branch instead:

- `COORDINATION.md` — both boards and both logs retained; this section appended.
- Root generated pages, `style.css`, `README.md`, `data/contests.json`, `data/EVIDENCE.md`,
  `.github/workflows/validate.yml` — resolved to this session's version, because the build regenerates them from
  the merged data. No upstream listing, evidence record or audit finding was dropped: `data/upstream.json` is
  unchanged, and every fact from `audits/2026-11-01/evidence.json` is imported into `data/evidence/` with its
  source and attribution.
- `scripts/build.py` and `scripts/test.py` (the superseded root-dashboard builder) — moved, unmodified, to
  `audits/legacy-build/` with a README explaining they are not run by CI and would rebuild the old schema.
  Nothing was deleted from history; their content is preserved in the new dataset as well.
- Kept untouched and still linked: `audits/2026-11-01/**` (independent 13-lead audit), `explore.html`,
  `category/**`, `flagged/**`, `assets/**`, `data/catalog.json`, `scripts/build-pages.cjs`, `scripts/check.cjs`,
  `scripts/import-source.cjs`.

**Findings adopted from the parallel audit (credited in each row)**

Sony World Photography Awards: rules §1.2.1 "The Competition is free to enter", up to three free images,
computer-generated origin prohibited, Single Image deadline 2027-01-05 16:00 GMT. Tom Howard poetry: $27 entry
fee and currently closed — removed from the free-entry shortlist. NYPL Young Lions: publisher-only nominations and
a 2026-09-03 deadline that contradicts the page's "now open" label. Film Prize: the cited rules URL resolves to
Photo Prize rules. Zindi: rules URL returns "404 page not found". Freelancer.com: winner pays 10% or $5.
MLB Beat the Streak: "NO PURCHASE NECESSARY", but the grand prize is conditional on a 57-hit streak.
CheckMate Gaming: prize-claim window stated as both 24 hours and seven days, and the region label conflicts with
the US-default legal terms. Challenge.gov: sunset 2026-03-30; USA.gov is the successor discovery route.

**Status of this task:** implementation and local validation done; verification coverage is deliberately partial
(27 of 209 rows) and every remaining row is published as unverified on `review.html`. Pull request, merge and
Pages deployment result recorded below.

**Second main-advance (same session, shortly after):** while this branch was being pushed, `main` moved again
from `dba55fd` to `4cba38d` (PR #9, session `arena-be1d2210`, which added a self-contained `dashboard/` build).
`origin/main` was merged in; the only conflict was this board, resolved by keeping both logs verbatim.
`dashboard/**` is retained untouched and remains a working standalone site at `/dashboard/`. Its live-verification
findings for 15 entries (`dashboard/data/verification/verified.json`) were imported into `data/evidence/` with
attribution: ARC-AGI-2 entry deadline already passed (2026-10-26), ESPN Survivor entry closed,
AIcrowd submissions closed, NASCAR Fantasy Live free entry confirmed but prizes unread, plus stale-range
corrections for Kaggle, Devpost and DrivenData.

**Canonical site decision (logged for review):** three parallel dashboards now exist in this repository —
the root site (this session's build), `explore.html` + `category/` + `flagged/` (session `582a1199-own2`),
`audits/2026-11-01/` (session `arena-05a44eaa`) and `dashboard/` (session `arena-be1d2210`). None is deleted.
The root site is presented as the canonical dashboard because it is the only one that (a) keeps all 206 ledger
rows, (b) publishes values only with a per-field quote and URL, and (c) merges the other sessions' findings with
attribution. Every other site remains reachable and reproducible; the root index links to all of them.

- 2026-11-01 RELEASE (be1d2210): PR https://github.com/sassnarep3-star/Own2/pull/9 merged without waiting for review at 2026-11-01T13:52:54Z, merge commit `4cba38df08e32697fa6d586ef470458acaaf07f4`. CI "Validate dashboard" passed on the PR and on main (run 41313393131). GitHub Pages API: latest build `built` for `4cba38d`. Live pages retrieved successfully: https://sassnarep3-star.github.io/Own2/dashboard/top-picks.html and https://sassnarep3-star.github.io/Own2/dashboard/flagged.html (content matched the build). Status of T6: done. Remaining **needs review** items (published on `dashboard/flagged.html`): 191 unverified entries, 2 JS-only pages, external link-rot, per-contest Texas eligibility and AI/automation rules. T7 (verify remaining entries) is unclaimed for any session.

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


---

## Session arena-ebd10b79 · complementary dashboard final integration

# Shared coordination board

Session: `arena-ebd10b79` (final integration session). All timestamps UTC.

Branch policy: this Arena session must remain on `arena/ebd10b79-own2`; this overrides the requested session branch naming convention. No other active claims were present at initial inspection.

| Task | Status | Owner | File scope | Updated |
|---|---|---|---|---|
| Audit upstream ledger and official sources; retain unsupported claims in review queue | needs review | arena-ebd10b79 | data/**, research/** | 2026-11-01 |
| Build responsive category dashboard, summary and review pages | done | arena-ebd10b79 | *.html, categories/**, .nojekyll, assets/**, scripts/**, tests/**, package.json, package-lock.json, README.md, .gitignore | 2026-11-01 |
| Final integration, testing, GitHub Pages, PR and merge | in progress | arena-ebd10b79 | .github/**, COORDINATION.md | 2026-11-01 |

## Activity log
- 2026-11-01: Inspected repository: only a six-byte README existed; no prior coordination board, application or datasets. Claimed all work as the sole visible session. Only explicitly documented official-source evidence will be labeled verified. Unconfirmed fields remain empty and are published for review.

## Audit handoff · 2026-11-01
- Audited the full upstream data snapshot (`466f7c1e7a14b52b4a0d36beb84a00d68fd409b7`): 206 original records, 9 categories, 45 historical exclusions. All 206 original names/categories/links retained as provenance, not trusted operational facts. Added 10 event-level researched records.
- Official source notebook: 31 pages inspected, with URLs, excerpts and partial-chunk disclosures in `data/findings.json`, `research/AUDIT.md`, and the published Source Notebook. Primary evidence: [PayPal rules](https://paypalaihackathon.devpost.com/rules), [Metaculus rules](https://www.metaculus.com/tournament-rules/), [FutureEval](https://www.metaculus.com/tournament/fall-futureeval-2026/), [NFL rules](https://www.kaggle.com/competitions/nfl-big-data-bowl-2027/rules), [Sony Single Image](https://www.worldphoto.org/sony-world-photography-awards/single-image), [Sony Series](https://www.worldphoto.org/sony-world-photography-awards/series), [Wergle Flomp](https://winningwriters.com/our-contests/wergle-flomp-humor-poetry-contest-free), [ARC](https://arcprize.org/competitions/2026), [GEMS PDF](https://docs.nlr.gov/docs/fy26osti/96647.pdf). Full list in the notebook.
- Six rows have both official free-entry and cash-award evidence; not a personal-eligibility or payout guarantee. Three Metaculus event rows explicitly allow cash-equivalent payouts and are excluded from the strict cash filter. 190 rows have no independently inspected official source in this session; their operational values are blank, not inherited. Incomplete/caution-bearing records remain on Flagged for Review. No claim of a complete official re-verification of all legacy claims or external links.
- Irregularities: branded Skillz 404 at inherited `/terms-of-service/` (removed as actionable link, working homepage retained); SquaresPool HTTP source redirects to inspected HTTPS (corrected); Sony old Open/Professional pages redirect to Single Image/Series (canonical links used); AIcrowd extraction includes spam-like categories; Topcoder returns an Auth0 alert; Zindi extraction contains placeholders; 12 original source lists lack an explicit official-tier source; all are flagged. Historical exclusions have no official URLs in their source records and are preserved separately, unverified. Upstream header/data pass/date mismatch and unsupported blanket tax threshold not propagated.
- Repository review: initial README-only repo had no app, tests, workflows, coordination claims, or other session file ownership. The first pull of the Arena branch failed because its remote ref did not yet exist; fetched/rebased origin/main, then created the required remote Arena branch without switching branches. No merge conflicts or other work discarded.
- Local verification: deterministic 17-page static build; nine Python tests for every row's evidence/provenance, null blanks, all local links/assets/fragments, category coverage, review coverage and CSV consistency. Playwright tests passed for filtering, cash-equivalent exclusion, search, saved persistence, pagination, category locks, evidence deep links, blocked localStorage and no-JavaScript content. Desktop 1440px and mobile 390/320px tested for overflow and axe WCAG A/AA violations (none on overview). Screenshots inspected. No guarantee of all possible accessibility issues or all external URLs.
- Browser CDN downloads were unavailable in the sandbox. Used an NPM-distributed Chromium and its bundled runtime libraries instead; no generated browser binaries committed.
- Integration ready: publication workflow validates build, rows, links and browser behavior before deploying main. Build artifacts and test screenshots excluded from Git. No paid APIs, accounts, contest entries, or credentials used.

- Publication adjustment: Pages settings API returned HTTP 403 (resource not accessible by integration), despite existing Pages being readable and configured for `main:/`. Reused that already-enabled route: generated root HTML, `.nojekyll`, and CSV are intentionally committed as required publication artifacts; `site/` remains ignored. No request for user input or unsupported permission claim. Initial CI browser step failed on ubuntu-latest; pinned the test OS and added structured error annotations for diagnosis. No merge attempted with a failing check.

- PR opened: https://github.com/sassnarep3-star/Own2/pull/8. CI diagnostics identified a browser-test-only package export lookup that was masked locally by a warm temporary library cache. Fixed resolution to the exported module entry point and validated with a fresh temporary runtime directory; no application/data test failures. Audit task is needs review because incomplete/caution-bearing records are already published on the review page, not because they block integration.


### Concurrent-main conflict resolution · 2026-11-01
- A fresh fetch before merging PR #8 discovered other sessions had already merged PRs #1–7. Their coordination board and published application were not present in this session's initial checkout. Stopped the direct merge path immediately; this is concurrent work, not an abandoned claim.
- `git merge --no-commit origin/main` reported add/add conflicts in 404.html, COORDINATION.md, assets/app.js, assets/style.css, index.html, review.html, scripts/build.py, summary.html, and a README content conflict. Resolved by retaining main's complete root application/builder/assets and all existing datasets, shortlist, independent audit, tests and publication histories. Both coordination histories retained in full.
- This session now owns only the complementary `dashboard/**` UI, `scripts/build-dashboard.py`, `scripts/prepare_data.py`, `research/**`, `data/findings.json`, `data/ledger.{json,csv}`, package/test files, and its CI workflow. No existing application is replaced. Shared navigation integration adds links to the complementary dashboard and the prior independent audit, after earlier application tasks were already marked done.
- Main's existing root/shortlist/audit checks and this session's tests will all be re-run together. Original field evidence in other views is not silently overwritten or promoted into this view without independent review. Conflicting ARC summary-vs-track dates are displayed as a review issue, not resolved by guessing.
- Combined validation after namespacing: earlier root Python build/test, earlier shortlist Node build/check, independent audit build/test, new dashboard build and ten row/provenance/link/parity tests all pass. New Playwright/axe suite passes at `/dashboard/`; earlier source datasets and main assets remain unchanged. Root navigation now links both complementary dashboard and the previously requested independent audit. Combined CI executes all three earlier validation suites before this dashboard's tests.
- Published paths for this session: `/dashboard/`, `/dashboard/summary.html`, `/dashboard/review.html`, `/dashboard/sources.html`. Earlier root, `/explore.html`, `/flagged/`, and `/audits/2026-11-01/` remain intact. This avoids silent replacement and incompatible data schema changes.
- Push synchronization after the intentional main-integration merge: plain `git pull --rebase origin arena/ebd10b79-own2` tried to flatten/replay merged-main history and hit the other session's initial COORDINATION add/add commit. Stopped and aborted that redundant rebase, restoring the complete integration merge. Confirmed the remote session tip is already an ancestor; `git pull --rebase --ff-only origin arena/ebd10b79-own2` then reported already up to date. No force push or other-session history loss required.

- A subsequent fresh main fetch discovered session be1d2210 had independently published `/dashboard/` in PRs #9/#11 while this session was resolving the first integration. Stopped again; its completed scope is not abandoned. Relocated only this session’s work to the collision-resistant `/ledger-ebd10b79/` namespace **before** merging that main update. All other dashboard files will be preserved. Earlier `/dashboard/` paths in this session’s historical notes are superseded. New owned scope: `ledger-ebd10b79/**` plus the unique research/import/build/test files listed above. Root navigation integrates both dashboards and the independent audit; no other dataset rewritten.



### Latest canonical-root integration
- A third fresh-main check found PRs #10/#13 had merged a revised canonical root site while CI was running. PR #8 merge was correctly rejected due to conflicts, not overridden. Resolved all root HTML/README/gitignore/coordination conflicts by retaining the new main root implementation and all source evidence. The earlier root builder was archived by that other integration; its archive is retained exactly. This session’s unique site remains `/ledger-ebd10b79/`.
- Shared root navigation changes from this session were withdrawn to avoid overwriting the current owner’s canonical application. Integration request to the root owner: link `ledger-ebd10b79/index.html`, `ledger-ebd10b79/summary.html` and `ledger-ebd10b79/review.html` when next editing shared navigation. This session’s README section and final live URL provide discovery in the meantime.
- Combined validation now uses the current main `scripts/build_site.py` / `scripts/check_site.py`, plus all preserved shortlist, independent audit, dashboard, ledger-verification, and this session’s tests. No other-session evidence is silently replaced by this view’s research.
- Combined-test compatibility issue found after the canonical-root merge: the independent audit's membership test expected `data/contests.json` to be a top-level list, while the new canonical builder wraps unchanged row IDs in an `entries` object. Final integration applied a minimal list-or-entries compatibility fix to that test only; no evidence, assertions, audit pages or row values changed. All original test assertions remain enforced. Existing preview copies were refreshed before repeating link checks; no external-link completeness is claimed.
