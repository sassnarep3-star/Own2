# Executive summary — free-to-enter cash competitions

**Audit date:** 1 November 2026 (UTC) · **Site:** https://sassnarep3-star.github.io/Own2/
**Source ledger:** `karagemop466-tech/FreeMoneyApps`, commit `466f7c1e` (206 listings, 45 removed records)
**Prepared by:** integration session `arena-f10345ed`

---

## 1. What this project now is

A single static dashboard that answers one question: **which competitions are worth my time today?**

Every published value — free entry, prize, deadline, eligibility, AI rules, payment — is quoted from the
operator's own page, with the URL and the date it was read. If the operator does not state a value, the cell
stays blank and the row says so. The 206 original listings are all still there; nothing was deleted for being
inconvenient, and nothing was upgraded on the strength of a third-party claim.

| Page | What it is for |
|---|---|
| `index.html` | Dashboard: counts, "where to spend your time", confirmed deadlines, category cards |
| `contests.html` | All 209 competitions, searchable/filterable/sortable, evidence behind every row |
| `<category>.html` | Nine category pages with a short evidence-based read of each category |
| `summary.html` | This executive summary, on the site |
| `review.html` | Flagged for review: every contradiction, dead link and unverified row |
| `data/EVIDENCE.md` | The raw evidence log: quote, status and URL per field |
| `data/contests.json` | Machine-readable dataset, including flags and sources |

## 2. Headline numbers

- **209** competitions tracked: the 206 ledger rows plus 3 specific live events found during verification
  (GEMS Prize Challenge, PayPal AI Hackathon, NFL Big Data Bowl 2027).
- **27** rows carry recorded evidence (19 verified in this pass, 8 imported from the parallel audit with attribution).
- **9** fully verified: free entry **and** a cash prize both stated by the operator, window open.
- **8** of those are usable right now and form the "where to spend your time" shortlist.
- **17** have confirmed free entry; **15** have a confirmed cash prize.
- **10** are partly verified: one side of the free-entry/cash-prize test is confirmed, the other is not.
- **7** are flagged: the source contradicts the ledger, or the cited page no longer exists.
- **183** remain unverified leads. They are published blank, with their link, so nothing is lost and
  nothing is invented.

## 3. Where the time should actually go

Ranked by verified free entry, verified cash, and whether an AI agent can do the work.

1. **ESPN NFL Pick'em 2026** — $102,000 across 58 prizes plus $1,500 guaranteed weekly; free; 10 entries;
   open to 10 Jan 2027. Operator states "FREE to play" and publishes the total prize figure on the game page.
2. **CBS Sports Pro Football Pick'em** — free, 50 US states + DC, 18+, 18 weekly contests to 10 Jan 2027.
   Free entry is explicit in the official rules. *Prize amounts are still unread — the one gap in this row.*
3. **Devpost hackathons** — free entry is written into the rules ("NO PURCHASE OR PAYMENT NECESSARY"),
   and six-figure pools were live on the audit date: PayPal AI $67,500 (closes 12 Nov 2026),
   Kiroween $100,000, Meta VR $1,000,000, Codegeist $120,000, UGREEN $46,000. **PayPal AI is the single best
   fit for an agent-assisted workflow**: AI tools explicitly allowed, only a sandbox integration required.
4. **Metaculus** — 19 live forecasting tournaments, pools $3,400–$50,000, free to enter, nothing staked,
   and a dedicated bot track. Lowest cost per attempt of anything in the ledger.
5. **Kaggle / DrivenData** — $450,000 (ARC Prize paper track), $100,000 (NFL Big Data Bowl 2027),
   $300,000 (GEMS). Large pools with real deadlines; free entry is nowhere stated by the platform, so these
   stay "partly verified" rather than being assumed free.
6. **Sony World Photography Awards** ($25,000 Series / $5,000 Single Image, free, closes 5–12 Jan 2027) and
   **Wergle Flomp humour poetry** ($5,100, no fee, closes 1 Apr 2027) — genuinely free, but they require
   original human work and the poetry rules explicitly ban AI-generated text.
7. **Checkmate Gaming** — verified free-entry cash tournaments posted daily ($40–$120), but console FPS skill
   is mandatory and prizes are small.

## 4. What to stop doing

- **Cash skill-game apps.** Papaya, Skillz and Pocket7Games free rooms pay gems; real money needs an entry fee.
- **Tipster "predictor" games.** Andy's £1,000,000 predictor closed 18 Sep 2026, is UK/Ireland-only, and the
  headline is a near-impossible perfect-table jackpot on a betting-affiliate site. Real prizes: £500/£250/£100.
- **GamerSaloon "cash" 1-rounders.** The operator's own footnote says the $10 is Bonus Cash, "not eligible for
  withdrawal". The ledger called it "$10 cash".
- **Broker demo contests.** The three demo-account contests in the market category are sourced only from
  affiliate blogs, never from the brokers.
- **Dead links presented as live contests.** The "Dirty Dozen £12,000 weekly" row points at a gambling-affiliate
  URL that now serves a generic casino lobby; Challenge.gov, cited as the official source for federal prizes,
  was sunset on 30 March 2026 (federal competitions now list at usa.gov).
- **Reading "free to enter" off a marketing page.** Three ledger rows are actively wrong when checked:
  Tom Howard poetry charges $27 per submission and is closed until April 2027; NYPL Young Lions is
  publisher-nomination only with a 3 Sep 2026 deadline that contradicts its own "now open" label;
  and the Film Prize rules URL serves Photo Prize rules instead of film rules.
- **"£2M ARC Prize"-style headlines.** ARC's $2M is discretionary and its submissions closed one day after this audit.

## 5. Verification method (what "verified" means here)

For each entry opened, I recorded the operator's own words for six fields: free entry, cash prize, deadline,
eligibility, AI rules and payment. A value is published only when a verbatim quote supports it. Where the
operator is silent the field is recorded as *not stated* — silence is treated as silence, never as permission.
Where the operator contradicts the ledger, the row is **flagged** and both statements are shown.

Enforced by `scripts/check_site.py` on every push:

- all 206 upstream listings retained, ids unique;
- every published field carries a quote and an http(s) URL;
- no row labelled unverified publishes any value;
- every row without an official source is flagged;
- rebuild is deterministic; all local links resolve; every page has charset, viewport and `lang`;
- category page row counts match the dataset.

## 6. Limits and irregularities (also on `review.html`)

1. **183 of 209 rows are unverified.** That is the honest state of a 206-row ledger checked in one pass. They
   keep their links and their "unverified" label.
2. **Free entry is not the same as free.** Kaggle, DrivenData, ARC and Topcoder publish no fee but never say
   entry is free — so they are *partly* verified, not verified.
3. **Three rows could not be sustained by their own sources:** Dirty Dozen (link dead, prize unlocatable),
   Challenge.gov (platform sunset 30 Mar 2026), GamerSaloon (prize not withdrawable).
4. **Twelve rows have no official source at all** — only affiliate or forum links (three broker demos, a set of
   FPL mini-leagues, one Turkish fantasy league). Nothing from them is published as fact.
5. **Topcoder could not be verified**: its challenge list requires JavaScript, so no prize or deadline could be read.
6. **The upstream ledger's own headline claims were not adopted:** "189 true free paths", "US tax forms apply at
   $600+" (too broad to reuse) and the August 17-vs-19 date mismatch in the original site are not repeated.
7. **Prize pools are not expected value.** No win probability, hourly rate or earnings ranking is asserted anywhere.
8. **Link health is partial by definition:** only pages actually opened were checked; unopened links may be broken.

## 7. Parallel audits preserved in this repository

- `audits/2026-11-01/` — an independent 13-lead official-source audit by a separate session, with its own report,
  review page and evidence file. Its findings are imported into this site's evidence records, attributed per row.
- `explore.html`, `category/`, `flagged/`, `assets/` — the other integration session's shortlist site, kept live
  and unchanged.
- `audits/legacy-build/` — the first dashboard's builder, kept for traceability and not run by CI.

## 8. Sources used (all official operator pages unless noted)

| Entry | Source |
|---|---|
| ESPN NFL Pick'em | https://fantasy.espn.com/games/nfl-pickem-2026/make-picks |
| CBS Pro Football Pick'em rules | https://www.cbssports.com/fantasy/football/games/pickem/rules |
| Devpost open hackathons | https://devpost.com/hackathons |
| PayPal AI Hackathon rules | https://paypalaihackathon.devpost.com/rules |
| Metaculus tournaments | https://www.metaculus.com/tournaments/ |
| Kaggle competitions / docs | https://www.kaggle.com/competitions · https://www.kaggle.com/docs/competitions |
| ARC Prize 2026 | https://arcprize.org/competitions/2026 |
| DrivenData | https://www.drivendata.org/competitions/ |
| Sony World Photography Awards | https://www.worldphoto.org/sony-world-photography-awards |
| Wergle Flomp (Winning Writers) | https://winningwriters.com/our-contests/wergle-flomp-humor-poetry-contest-free |
| Checkmate Gaming free tournaments | https://www.checkmategaming.com/free-tournaments |
| GamerSaloon 1-Rounders | https://www.gamersaloon.com/promos/1rounder/ |
| TradingView The Leap | https://www.tradingview.com/the-leap/ |
| Andy's Bet Club predictor | https://andysbetclub.co.uk/predictor-game/ |
| Challenge.gov sunset notice | https://www.challenge.gov/ · replacement https://www.usa.gov/challenges |
| Vocal challenges FAQ | https://vocal.media/resources/challenges-frequently-asked-questions |
| Tom Howard / Margaret Reid Poetry (fee, closed) | https://winningwriters.com/our-contests/tom-howard-margaret-reid-poetry-contest |
| NYPL Young Lions (publisher nomination only) | https://www.nypl.org/about/awards/young-lions-fiction-award/submission-form |
| Sony Single Image rules (free entry, AI origin) | https://www.worldphoto.org/sony-world-photography-awards/single-image |
| MLB Beat the Streak rules | https://www.mlb.com/apps/beat-the-streak/official-rules |
| Freelancer.com contest fee FAQ | https://www.freelancer.com/faq/topic.php?id=33 |
| Zindi inherited rules URL (404) | https://zindi.world/rules |
| Kinolime competitions hub | https://www.kinolime.com/competitions |
| Upstream ledger (pinned) | https://github.com/karagemop466-tech/FreeMoneyApps/commit/466f7c1e7a14b52b4a0d36beb84a00d68fd409b7 |

## 9. Recommended next actions

1. **Enter one thing this week.** PayPal AI Hackathon (closes 12 Nov 2026, AI allowed, $67,500 pool) is the
   highest-value, best-fit opportunity on the board for an agent-assisted workflow.
2. **Set the weekly routine.** ESPN and CBS pick'em run every NFL week to 10 Jan 2027 — free, high prize
   volume, 10 entries on ESPN.
3. **Cheapest compounding skill:** Metaculus tournaments, especially the bot track ($50,000 pool).
4. **Next verification pass, in this order:** CBS prize table (section 3 of the rules), ESPN eligibility rules,
   Kaggle entry terms, then the 12 rows with no official source. Each needs one page read.
5. **Do not build automation that breaks rules.** ESPN and CBS do not publish an automation policy; that is
   recorded as "not stated", not as permission.
