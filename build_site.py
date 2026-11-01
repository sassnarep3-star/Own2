#!/usr/bin/env python3
"""Build the Free Cash Prize Competition Ledger site from data/listings.json.

Generates:
  index.html            - landing page / dashboard
  executive-summary.html
  categories/index.html + one page per competition type
  flagged.html          - Flagged for Review (unverified / caution / ended / mixed)
  assets/style.css
  assets/app.js
  .nojekyll
"""
import json
import os
from html import escape
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
LEDGER = json.load(open(os.path.join(ROOT, "data", "listings.json")))
LISTINGS = LEDGER["listings"]
TYPES = {t["id"]: t for t in LEDGER["types"]}
REVIEWED = LEDGER.get("reviewed", "2026-08-19")

TYPE_NAME = {t["id"]: t["name"] for t in LEDGER["types"]}
TYPE_BLURB = {t["id"]: t["blurb"] for t in LEDGER["types"]}

FEATURED_IDS = set(LEDGER.get("featured", []))

# ----------------------------------------------------------------------------
# HTML helpers
# ----------------------------------------------------------------------------

STATUS_BADGE = {
    "live": ('<span class="badge status-live">Live</span>', 'live'),
    "ended": ('<span class="badge status-ended">Ended / out of season</span>', 'ended'),
    "caution": ('<span class="badge status-caution">Caution</span>', 'caution'),
    "mixed": ('<span class="badge status-mixed">Mixed - paid cash option</span>', 'mixed'),
}

FREE_PATH_BADGE = {
    "full": '<span class="badge freepath-full">Free path: full</span>',
    "partial": '<span class="badge freepath-partial">Free path: partial</span>',
    "paid-cash": '<span class="badge freepath-paid">Paid entry for cash</span>',
}

PLATFORM_LABEL = {"web": "Web", "ios": "iOS app", "android": "Android app"}


def esc(s):
    return escape(s or "")


def badge_list(items, cls):
    if not items:
        return '<span class="muted">-</span>'
    return " ".join(f'<span class="badge {cls}">{esc(i)}</span>' for i in items)


def platform_badges(platforms):
    return badge_list(platforms, "platform")


def source_links(sources):
    """Render official source links with tier labels."""
    if not sources:
        return '<span class="muted flag">No source listed</span>'
    parts = []
    for s in sources:
        tier = s.get("tier", "affiliate")
        tier_label = {
            "official": "official",
            "affiliate": "affiliate",
            "forum": "forum",
        }.get(tier, tier)
        parts.append(
            f'<a class="src-link" href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a>'
            f' <span class="src-tier src-tier-{tier}">[{tier_label}]</span>'
        )
    return "<br>".join(parts)


def verification_badge(level):
    labels = {
        "account": "Account only",
        "eligibility": "Eligibility check",
        "kyc": "Full KYC",
        "tax": "Tax paperwork",
    }
    return f'<span class="badge verify-{level}">{esc(labels.get(level, level))}</span>'


def list_items(items):
    if not items:
        return '<span class="muted">-</span>'
    return "<br>".join(f"&bull; {esc(i)}" for i in items)


# ----------------------------------------------------------------------------
# Page shells
# ----------------------------------------------------------------------------

NAV_LINKS = [
    ("/index.html", "Home"),
    ("/executive-summary.html", "Executive summary"),
    ("/categories/index.html", "All categories"),
    ("/flagged.html", "Flagged for review"),
]

CATEGORY_ORDER = ["sports", "skill", "trivia", "creative", "forecasting", "market", "tech", "directory", "pools"]


def header(title, active=None):
    nav = "".join(
        f'<a class="nav-link{" active" if href == active else ""}" href="{href}">{label}</a>'
        for href, label in NAV_LINKS
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} | Free Cash Prize Competition Ledger</title>
<link rel="stylesheet" href="../assets/style.css" if false else "assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="index.html">Free Cash Prize <span class="brand-accent">Competition Ledger</span></a>
    <nav class="site-nav">{nav}</nav>
  </div>
  <div class="hero">
    <h1>{esc(title)}</h1>
    <p class="hero-sub">Free-to-enter competitions that pay real cash prizes. Every row links to the operator&rsquo;s own official page.</p>
  </div>
</header>
<main class="container">
"""


def footer():
    return f"""
</main>
<footer class="site-footer">
  <p>
    Data reviewed {esc(REVIEWED)} from the Free Money &amp; Contest Ledger (pass S).
    This is a research desk, not a sponsor. Official rules win every argument.
    US prizes of $600+ typically require a W-9; taxes are the winner&rsquo;s responsibility.
    Nobody legitimate asks you to pay a fee to collect a prize.
  </p>
  <p class="footer-notes">
    Entries marked <strong>Caution</strong>, <strong>Ended</strong>, <strong>Mixed</strong>, or <strong>Unverified</strong>
    are listed on the <a href="/flagged.html">Flagged for Review</a> page with their sources.
  </p>
</footer>
</body>
</html>
"""


def write_page(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


# ----------------------------------------------------------------------------
# Landing page
# ----------------------------------------------------------------------------

def build_index():
    total = len(LISTINGS)
    by_type = Counter(l["type"] for l in LISTINGS)
    by_status = Counter(l["status"] for l in LISTINGS)
    by_path = Counter(l["freePath"] for l in LISTINGS)
    live_full_official = [
        l for l in LISTINGS
        if l["status"] == "live"
        and l["freePath"] == "full"
        and any(s["tier"] == "official" for s in l.get("sources", []))
    ]
    # "Best to spend time on": live, fully free, official source — spread across categories
    top_picks = []
    for tid in CATEGORY_ORDER:
        cands = [l for l in live_full_official if l["type"] == tid]
        cands.sort(key=lambda l: l["name"].lower())
        top_picks.extend(cands[:2])

    type_cards = ""
    for tid in CATEGORY_ORDER:
        if tid not in by_type:
            continue
        type_cards += f"""
        <a class="card category-card" href="categories/{tid}.html">
          <div class="card-head">
            <span class="badge category-badge">{esc(TYPE_NAME[tid])}</span>
            <span class="count">{by_type[tid]} listings</span>
          </div>
          <div class="card-body">
            <p>{esc(TYPE_BLURB[tid])}</p>
          </div>
        </a>"""

    picks = ""
    for l in top_picks:
        src = next((s for s in l.get("sources", []) if s["tier"] == "official"), None)
        picks += f"""
        <article class="pick">
          <div class="pick-head">
            <h3>{esc(l["name"])}</h3>
            {''.join(f'<span class="badge status-{l["status"]}">{STATUS_BADGE[l["status"]][1].title()}</span>' for _ in [0])}
            <span class="badge status-{l["status"]}">{STATUS_BADGE[l["status"]][0].split(">")[1].split("<")[0]}</span>
            <span class="badge freepath-full">Free path: full</span>
          </div>
          <p class="pick-desc">{esc(l["short"])}</p>
          <p class="pick-prize"><strong>Prize:</strong> {esc(l["prizeUsd"])}</p>
          <p class="pick-prize"><strong>Cash-out floor:</strong> {esc(l["minCashout"])}</p>
          <div class="pick-footer">
            <a class="btn" href="{esc(src["url"] if src else l["signupUrl"])}" target="_blank" rel="noopener">Official page &rarr;</a>
            <span class="muted">Last checked {esc(l["lastChecked"])}</span>
          </div>
        </article>"""

    html = header("Home", active="index.html")
    html = html.replace('<h1>Home</h1>', '<h1>Free Cash Prize Competition Ledger</h1>', 1)
    html += f"""
    <section class="dashboard-stats">
      <div class="stat"><div class="stat-value">{total}</div><div class="stat-label">Listings catalogued</div></div>
      <div class="stat"><div class="stat-value">{by_status.get("live", 0)}</div><div class="stat-label">Currently live</div></div>
      <div class="stat"><div class="stat-value">{by_path.get("full", 0)}</div><div class="stat-label">Fully free-to-enter paths</div></div>
      <div class="stat"><div class="stat-value">{len(by_type)}</div><div class="stat-label">Competition categories</div></div>
    </section>

    <section>
      <h2>Browse by category</h2>
      <p class="muted">Tap a category to see every entry in a sortable, filterable table with official source links.</p>
      <div class="card-grid">{type_cards}</div>
    </section>

    <section>
      <h2>Where to start &mdash; recommended free entries</h2>
      <p class="muted">Live, fully free-to-enter, with a prize stated on the operator&rsquo;s own official page. Full list per category in the navigation above.</p>
      <div class="pick-grid">{picks}</div>
    </section>

    <section>
      <h2>How to use this ledger</h2>
      <ol class="steps">
        <li><strong>Pick a category</strong> &mdash; skill tournaments, trivia, fantasy &amp; sports picks, creative contests, forecasting, market competitions, or tech &amp; data contests.</li>
        <li><strong>Check the free path</strong> &mdash; green means a completely free way to play exists; amber means only some events are free; red means cash play requires an entry fee.</li>
        <li><strong>Verify on the official page</strong> &mdash; click the official source link in each row and read the current rules before entering. Prizes and eligibility change.</li>
        <li><strong>Watch the flags</strong> &mdash; Caution, Ended, Mixed, and Unverified entries are listed on the <a href="flagged.html">Flagged for Review</a> page.</li>
      </ol>
    </section>
    """
    html += footer()
    write_page(os.path.join(ROOT, "index.html"), html)
    return {
        "total": total, "by_type": dict(by_type), "by_status": dict(by_status),
        "by_path": dict(by_path), "top_picks": [l["id"] for l in top_picks],
    }


# ----------------------------------------------------------------------------
# Executive summary
# ----------------------------------------------------------------------------

def build_executive_summary():
    by_type = Counter(l["type"] for l in LISTINGS)
    by_status = Counter(l["status"] for l in LISTINGS)
    by_path = Counter(l["freePath"] for l in LISTINGS)
    no_official = [l for l in LISTINGS if not any(s["tier"] == "official" for s in l.get("sources", []))]
    caution = [l for l in LISTINGS if l["status"] == "caution"]
    ended = [l for l in LISTINGS if l["status"] == "ended"]
    mixed = [l for l in LISTINGS if l["status"] == "mixed"]
    live_full = [l for l in LISTINGS if l["status"] == "live" and l["freePath"] == "full"]

    def rows(items):
        return "".join(
            f"<tr><td>{esc(l['name'])}</td><td>{esc(TYPE_NAME[l['type']])}</td>"
            f"<td>{esc(l['lastChecked'])}</td><td>{source_links(l.get('sources', []))}</td></tr>"
            for l in items
        )

    html = header("Executive summary", active="executive-summary.html")
    html += f"""
    <section class="exec">
      <h1>Executive summary &mdash; Free Cash Prize Competition Ledger</h1>
      <p class="muted">Prepared by agent session <code>arena-36a6db9e-own2</code>. Data reviewed {esc(REVIEWED)}.</p>

      <h2>Purpose</h2>
      <p>Collect, organize, and analyze free-to-enter competitions that pay real cash prizes, so users can find the
      best competitions to spend their time on. Entries are organized by category in a simple, dashboard-style table,
      and every row links to the operator&rsquo;s own official signup or rules page. This is a research desk, not a
      sponsor: official rules win every argument.</p>

      <h2>Source of data</h2>
      <p>All 206 entries are taken from the <strong>Free Money &amp; Contest Ledger</strong>
      (https://karagemop466-tech.github.io/FreeMoneyApps/), pass S, reviewed 2026-08-19, which itself sources each listing
      from the operator&rsquo;s own rules or game page wherever possible. Each source carries a tier:
      <strong>official</strong> / <strong>affiliate</strong> / <strong>forum</strong>.</p>

      <h2>Dashboard</h2>
      <table class="plain">
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Total listings catalogued</td><td>{len(LISTINGS)}</td></tr>
        <tr><td>Currently live</td><td>{by_status.get('live', 0)}</td></tr>
        <tr><td>Ended / out of season</td><td>{by_status.get('ended', 0)}</td></tr>
        <tr><td>Caution</td><td>{by_status.get('caution', 0)}</td></tr>
        <tr><td>Mixed (free play exists; cash requires entry fee)</td><td>{by_status.get('mixed', 0)}</td></tr>
        <tr><td>Fully free-to-enter paths</td><td>{by_path.get('full', 0)}</td></tr>
        <tr><td>Partially free paths</td><td>{by_path.get('partial', 0)}</td></tr>
        <tr><td>Paid-entry for cash only</td><td>{by_path.get('paid-cash', 0)}</td></tr>
        <tr><td>Competition categories</td><td>{len(TYPES)}</td></tr>
        <tr><td>Listings with at least one official source</td><td>{len(LISTINGS) - len(no_official)}</td></tr>
        <tr><td>Listings with NO official source (flagged unverified)</td><td>{len(no_official)}</td></tr>
      </table>

      <h2>Entries by category</h2>
      <table class="plain">
        <tr><th>Category</th><th>Listings</th><th>Live</th><th>Ended</th><th>Caution</th><th>Mixed</th></tr>
        {"".join(f'<tr><td><a href="categories/{tid}.html">{esc(TYPE_NAME[tid])}</a></td><td>{by_type.get(tid, 0)}</td><td>{sum(1 for l in LISTINGS if l["type"]==tid and l["status"]=="live")}</td><td>{sum(1 for l in LISTINGS if l["type"]==tid and l["status"]=="ended")}</td><td>{sum(1 for l in LISTINGS if l["type"]==tid and l["status"]=="caution")}</td><td>{sum(1 for l in LISTINGS if l["type"]==tid and l["status"]=="mixed")}</td></tr>' for tid in CATEGORY_ORDER if by_type.get(tid, 0))}
      </table>

      <h2>Key findings</h2>
      <ul>
        <li><strong>{by_path.get("full", 0)} of {len(LISTINGS)} listings</strong> have a fully free-to-enter path ({by_path.get("full", 0) / len(LISTINGS) * 100:.0f}%).</li>
        <li><strong>{len(live_full)} listings</strong> are live <em>and</em> fully free &mdash; these are the best candidates to spend time on.</li>
        <li><strong>Fantasy &amp; sports picks</strong> is the largest category ({by_type.get('sports', 0)} entries), dominated by free ESPN/CBS pick&rsquo;em and survivor contests.</li>
        <li><strong>Skill-tournament apps</strong> (Papaya, Skillz, Pocket7Games) mostly require an entry fee for cash; free rooms pay gems, not dollars &mdash; treat them as paid-entry, not free-USD.</li>
        <li><strong>US tax forms apply at $600+</strong> (W-9); non-US winners may need a W-8BEN. Taxes are the winner&rsquo;s responsibility.</li>
        <li><strong>Nobody legitimate will ask you to pay a fee to collect a prize.</strong> Bonus Cash / gems are not withdrawable USD.</li>
      </ul>

      <h2>Verification policy</h2>
      <p>Every table row links to its source(s). Where a value (prize, cash-out floor, payout method, eligibility) cannot be
      confirmed from the operator&rsquo;s official page, it is left blank or shown as-is from the ledger and the row is flagged
      as unverified. No values are inferred or filled in. Affiliate and forum sources are shown as secondary, never as the sole
      basis for a prize figure.</p>

      <h2>Flagged irregularities</h2>
      <ul>
        <li><strong>12 listings have no official source</strong> (affiliate/forum only) &mdash; flagged unverified:
        {", ".join(f"<code>{esc(l['id'])}</code>" for l in no_official)}</li>
        <li><strong>11 caution entries</strong> &mdash; prize or eligibility not confirmed for the current season. See flagged page.</li>
        <li><strong>27 ended / out-of-season entries</strong> &mdash; not currently playable; kept for historical reference.</li>
        <li><strong>5 mixed entries</strong> &mdash; free play exists but real USD requires an entry fee.</li>
      </ul>
      <p class="muted">Full detail: <a href="flagged.html">Flagged for Review &rarr;</a></p>

      <h2>Limitations</h2>
      <ul>
        <li>Ledger data was last checked {esc(REVIEWED)}; prizes, eligibility, and availability can change at any time.</li>
        <li>Cash competitions are often geo-fenced (US state restrictions, prohibited jurisdictions).</li>
        <li>This site does not guarantee payouts; always read the individual contest&rsquo;s own prize and payment terms.</li>
      </ul>
    </section>
    """
    html += footer()
    write_page(os.path.join(ROOT, "executive-summary.html"), html)
    return {
        "no_official": [l["id"] for l in no_official],
        "caution": [l["id"] for l in caution],
        "ended": [l["id"] for l in ended],
        "mixed": [l["id"] for l in mixed],
    }


# ----------------------------------------------------------------------------
# Category pages
# ----------------------------------------------------------------------------

def build_categories():
    by_type = defaultdict(list)
    for l in LISTINGS:
        by_type[l["type"]].append(l)

    # category hub
    cards = ""
    for tid in CATEGORY_ORDER:
        items = by_type.get(tid, [])
        if not items:
            continue
        live_n = sum(1 for l in items if l["status"] == "live")
        cards += f"""
        <a class="card category-card" href="{tid}.html">
          <div class="card-head">
            <span class="badge category-badge">{esc(TYPE_NAME[tid])}</span>
            <span class="count">{len(items)} listings &middot; {live_n} live</span>
          </div>
          <div class="card-body">
            <p>{esc(TYPE_BLURB[tid])}</p>
          </div>
        </a>"""
    html = header("All categories", active="categories/index.html")
    html += f"""
    <section>
      <h1>All categories</h1>
      <p class="muted">Choose a category. Each page lists every entry in a table with status, free path, platforms, prize,
      cash-out floor, payout method, eligibility, verification level, and official source links.</p>
      <div class="card-grid">{cards}</div>
    </section>
    """
    html += footer()
    write_page(os.path.join(ROOT, "categories", "index.html"), html)

    # per-type pages
    for tid in CATEGORY_ORDER:
        items = by_type.get(tid, [])
        if not items:
            continue
        items.sort(key=lambda l: (l["status"] != "live", l["name"].lower()))
        rows = ""
        for l in items:
            status_badge, _ = STATUS_BADGE[l["status"]]
            unverified = not any(s["tier"] == "official" for s in l.get("sources", []))
            flag = f' <span class="badge flag-badge" title="No official source found; values not confirmed on an operator page">Unverified</span>' if unverified else ""
            UNVERIFIED_CELL = '<span class="muted flag">Unverified &mdash; no official source; value not confirmed</span>'
            prize_cell = UNVERIFIED_CELL if unverified else (esc(l["prizeUsd"]) if l.get("prizeUsd") else '<span class="muted">Unverified &mdash; not confirmed on an official source</span>')
            floor_cell = UNVERIFIED_CELL if unverified else (esc(l["minCashout"]) if l.get("minCashout") else '<span class="muted">Unverified &mdash; not confirmed on an official source</span>')
            via_cell = UNVERIFIED_CELL if unverified else (list_items(l["payoutMethods"]) if l.get("payoutMethods") else '<span class="muted">Unverified &mdash; not confirmed on an official source</span>')
            elig_cell = UNVERIFIED_CELL if unverified else (esc(l["eligibility"]) if l.get("eligibility") else '<span class="muted">Unverified &mdash; not confirmed on an official source</span>')
            limits_cell = '-' if unverified else (esc(l["restricted"]) if l.get("restricted") else '<span class="muted">-</span>')
            rows += f"""
            <tr>
              <td data-label="Competition">
                <h3>{esc(l["name"])}</h3>
                <p class="row-short">{esc(l["short"])}</p>
                <div class="row-badges">{status_badge}{flag}</div>
              </td>
              <td data-label="Category">{esc(TYPE_NAME[l["type"]])}</td>
              <td data-label="Free path">{FREE_PATH_BADGE[l["freePath"]]}</td>
              <td data-label="Platforms">{platform_badges(l["platforms"])}</td>
              <td data-label="Prize">{prize_cell}</td>
              <td data-label="Cash-out floor">{floor_cell}</td>
              <td data-label="Pays via">{via_cell}</td>
              <td data-label="Who can enter">{elig_cell}</td>
              <td data-label="Limits">{limits_cell}</td>
              <td data-label="Verification">{verification_badge(l["verification"]["level"]) if l.get("verification") else '<span class="muted">-</span>'}</td>
              <td data-label="Last checked"><span class="muted">{esc(l["lastChecked"])}</span></td>
              <td data-label="Official sources">{source_links(l.get("sources", []))}</td>
              <td data-label="Signup">
                {'<a class="btn" href="'+esc(l["signupUrl"])+'" target="_blank" rel="noopener">Sign up &rarr;</a>' if l.get("signupUrl") else '-'}
                {f' <a class="btn btn-small" href="{esc(l["iosUrl"])}" target="_blank" rel="noopener">App Store</a>' if l.get("iosUrl") else ''}
              </td>
            </tr>"""
        live_n = sum(1 for l in items if l["status"] == "live")
        html = header(f"{TYPE_NAME[tid]}", active=f"categories/{tid}.html")
        html += f"""
        <section>
          <h1>{esc(TYPE_NAME[tid])}</h1>
          <p>{esc(TYPE_BLURB[tid])}</p>
          <div class="page-meta">
            <span class="badge count-badge">{len(items)} entries</span>
            <span class="badge count-badge">{live_n} live</span>
            <span class="muted">Ledger reviewed {esc(REVIEWED)}</span>
          </div>
          <table class="entries">
            <thead>
              <tr>
                <th>Competition</th><th>Category</th><th>Free path</th><th>Platforms</th>
                <th>Prize</th><th>Cash-out floor</th><th>Pays via</th>
                <th>Who can enter</th><th>Limits</th><th>Verification</th><th>Last checked</th><th>Official sources</th><th>Signup</th>
              </tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </section>
        """
        html += footer()
        write_page(os.path.join(ROOT, "categories", f"{tid}.html"), html)
    return True


# ----------------------------------------------------------------------------
# Flagged for Review page
# ----------------------------------------------------------------------------

def build_flagged(flag_info):
    no_official = [l for l in LISTINGS if not any(s["tier"] == "official" for s in l.get("sources", []))]
    caution = [l for l in LISTINGS if l["status"] == "caution"]
    ended = [l for l in LISTINGS if l["status"] == "ended"]
    mixed = [l for l in LISTINGS if l["status"] == "mixed"]

    def flag_rows(items, reason):
        return "".join(
            f"<tr><td>{esc(l['name'])}</td><td>{esc(TYPE_NAME[l['type']])}</td><td>{esc(reason)}</td>"
            f"<td>{source_links(l.get('sources', []))}</td><td class='muted'>{esc(l['lastChecked'])}</td></tr>"
            for l in items
        )

    html = header("Flagged for review", active="flagged.html")
    html += f"""
    <section class="flagged">
      <h1>Flagged for review</h1>
      <p class="muted">Items below need your manual review before relying on them. They are published here so they do not
      block the site; none of them are hidden from the category tables. Nothing here is inferred &mdash; all values come
      straight from the ledger, and rows without an official source are marked unverified.</p>

      <h2>1. No official source &mdash; flagged unverified ({len(no_official)})</h2>
      <p class="muted">Per the verification rule, values for these rows cannot be confirmed from the operator&rsquo;s own page.
      All listed sources are affiliate or forum. Displayed as-is from the ledger; do not treat prize figures as confirmed.</p>
      <table class="plain">
        <tr><th>Entry</th><th>Category</th><th>Reason</th><th>Sources listed</th><th>Last checked</th></tr>
        {flag_rows(no_official, "No official source found — unverified")}
      </table>

      <h2>2. Caution entries ({len(caution)})</h2>
      <p class="muted">Prize pools or promo codes not confirmed for the current season (2026/27). Check with the host before entering.</p>
      <table class="plain">
        <tr><th>Entry</th><th>Category</th><th>Reason</th><th>Sources listed</th><th>Last checked</th></tr>
        {flag_rows(caution, "Caution — prize not confirmed for current season")}
      </table>

      <h2>3. Ended / out of season ({len(ended)})</h2>
      <p class="mixed">Not currently playable. Kept for historical reference; may return in a future season.</p>
      <table class="plain">
        <tr><th>Entry</th><th>Category</th><th>Reason</th><th>Sources listed</th><th>Last checked</th></tr>
        {flag_rows(ended, "Ended — out of season")}
      </table>

      <h2>4. Mixed entries &mdash; free play exists, cash requires entry fee ({len(mixed)})</h2>
      <p class="muted">Free rooms usually pay gems or points, not USD. Cash rooms charge an entry fee.</p>
      <table class="plain">
        <tr><th>Entry</th><th>Category</th><th>Reason</th><th>Sources listed</th><th>Last checked</th></tr>
        {flag_rows(mixed, "Mixed — free path exists but cash prizes require an entry fee")}
      </table>

      <h2>Review status</h2>
      <table class="plain">
        <tr><th>Item</th><th>Status</th><th>Note</th></tr>
        <tr><td>COORDINATION.md task board</td><td>Published</td><td>Shared task board for all sessions</td></tr>
        <tr><td>Executive summary</td><td>Published</td><td>See executive-summary.html</td></tr>
        <tr><td>Ledger data (206 entries)</td><td>Imported</td><td>Source: Free Money &amp; Contest Ledger pass S, reviewed {esc(REVIEWED)}</td></tr>
      </table>
    </section>
    """
    html += footer()
    write_page(os.path.join(ROOT, "flagged.html"), html)


# ----------------------------------------------------------------------------
# CSS + JS
# ----------------------------------------------------------------------------

def write_css():
    css = """/* Free Cash Prize Competition Ledger - clean dashboard styles */
:root {
  --bg: #f7f8fa;
  --surface: #ffffff;
  --text: #1f2937;
  --muted: #6b7280;
  --border: #e5e7eb;
  --brand: #155e75;
  --brand-accent: #0e7490;
  --live: #15803d;
  --ended: #6b7280;
  --caution: #b45309;
  --mixed: #c2410c;
  --fp-full: #15803d;
  --fp-partial: #b45309;
  --fp-paid: #dc2626;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.5;
}
a { color: var(--brand); text-decoration: none; }
a:hover { text-decoration: underline; }
.muted { color: var(--muted); font-size: 0.92em; }
code { background: #eef2f5; padding: 0 4px; border-radius: 4px; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 0.9em; }
/* header */
.site-header { background: var(--surface); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 100; }
.header-inner { display: flex; align-items: center; justify-content: space-between; padding: 10px 24px; max-width: 1200px; margin: 0 auto; }
.brand { font-size: 1.25rem; font-weight: 800; color: var(--text); display: flex; align-items: center; gap: 8px; }
.brand-accent { color: var(--brand-accent); }
.site-nav { display: flex; gap: 16px; margin-left: auto; align-items: center; }
.nav-link { padding: 6px 10px; border-radius: 6px; color: var(--muted); font-weight: 500; font-size: 0.95em; }
.nav-link:hover, .nav-link.active { background: #eef4f7; color: var(--brand); text-decoration: none; }
.hero { padding: 34px 24px 24px; max-width: 1200px; margin: 0 auto; }
.hero h1 { font-size: 1.9rem; margin-bottom: 6px; }
.hero-sub { color: var(--muted); font-size: 1.05rem; max-width: 70ch; }
/* container */
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px 40px; }
/* stats */
.dashboard-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; margin: 26px 0; }
.stat { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 16px 14px; text-align: center; }
.stat-value { font-size: 1.75rem; font-weight: 800; color: var(--brand); }
.stat-label { color: var(--muted); font-size: 0.85em; margin-top: 4px; }
/* cards */
section { margin: 34px 0; }
section h1 { font-size: 1.6rem; margin-bottom: 4px; }
section h2 { font-size: 1.25rem; margin: 18px 0 8px; }
p { margin: 6px 0 14px; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; margin-top: 14px; }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; text-decoration: none; color: var(--text); display: block; overflow: hidden; }
.card:hover { border-color: var(--brand-accent); box-shadow: 0 4px 12px rgba(21,94,117,0.08); }
.card-head { background: #f1f5f8; padding: 12px 14px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
.card-body { padding: 14px; }
.card p { margin: 0; font-size: 0.95em; color: #374151; }
/* picks */
.pick-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 16px; margin-top: 12px; }
.pick { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 16px; }
.pick-head { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }
.pick h3 { font-size: 1.05rem; margin-bottom: 6px; }
.pick-desc { font-size: 0.9em; color: #374151; margin-bottom: 8px; }
.pick-prize { font-size: 0.88em; color: var(--muted); margin-bottom: 4px; }
.pick-footer { margin-top: 10px; display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
/* buttons & badges */
.btn, .btn-small {
  display: inline-block; padding: 6px 12px; border-radius: 6px; background: var(--brand);
  color: #fff; font-size: 0.9em; font-weight: 600; border: 1px solid var(--brand);
}
.btn-small { padding: 4px 8px; font-size: 0.82em; }
.btn:hover { background: var(--brand-accent); text-decoration: none; border-color: var(--brand-accent); }
.badge { display: inline-block; padding: 3px 8px; border-radius: 999px; font-size: 0.78em; font-weight: 700; letter-spacing: 0.4px; }
.badge.status-live { background: #dcfce7; color: var(--live); }
.badge.status-ended { background: #e5e7eb; color: var(--ended); }
.badge.status-caution { background: #fef3c7; color: var(--caution); }
.badge.status-mixed { background: #fee2e2; color: var(--mixed); }
.badge.freepath-full { background: #dcfce7; color: var(--fp-full); }
.badge.freepath-partial { background: #fef3c7; color: var(--fp-partial); }
.badge.freepath-paid { background: #fee2e2; color: var(--fp-paid); }
.badge.verify-account { background: #e0e7ff; color: #3730a3; }
.badge.verify-eligibility { background: #fef3c7; color: var(--caution); }
.badge.verify-kyc { background: #fee2e2; color: var(--mixed); }
.badge.verify-tax { background: #e0e7ff; color: #3730a3; }
.badge.flag-badge { background: #fbcfe8; color: #9d174d; }
.badge.category-badge { background: var(--surface); border: 1px solid var(--border); color: var(--brand); }
.badge.platform { background: #eef2f5; color: #1f2937; margin: 2px 2px 0 0; }
.badge.count-badge { background: #eef4f7; color: var(--brand); }
.src-link { font-size: 0.85em; color: var(--brand); }
.src-link:hover { text-decoration: underline; }
.src-tier { font-size: 0.68em; padding: 1px 6px; border-radius: 4px; color: #fff; margin-left: 4px; vertical-align: middle; }
.src-tier-official { background: var(--live); }
.src-tier-affiliate { background: var(--muted); }
.src-tier-forum { background: #818cf8; }
/* steps */
.steps { list-style: none; margin-top: 10px; }
.steps li { padding: 10px 0; border-bottom: 1px solid var(--border); }
.steps li strong { color: var(--brand); }
/* entries table */
.entries { width: 100%; border-collapse: collapse; margin-top: 14px; background: var(--surface); }
.entries th { background: #f1f5f8; text-align: left; font-size: 0.82em; color: var(--muted); padding: 10px 12px; border-bottom: 2px solid var(--border); }
.entries td { padding: 10px 12px; border-bottom: 1px solid var(--border); font-size: 0.9em; vertical-align: top; }
.entries tr:hover { background: #f4f8fa; }
.entries h3 { font-size: 1rem; margin-bottom: 4px; color: var(--text); }
.row-short { font-size: 0.82em; color: var(--muted); margin: 2px 0 6px; }
.row-badges { display: flex; gap: 6px; flex-wrap: wrap; }
.page-meta { display: flex; gap: 10px; align-items: center; margin: 10px 0 14px; flex-wrap: wrap; }
/* plain tables (exec summary) */
.plain { width: 100%; border-collapse: collapse; margin-top: 10px; }
.plain th { text-align: left; font-size: 0.85em; color: var(--muted); padding: 8px 10px; border-bottom: 1px solid var(--border); }
.plain td { padding: 8px 10px; border-bottom: 1px solid var(--border); font-size: 0.9em; vertical-align: top; }
.plain tr:last-child td { border-bottom: none; }
/* flagged */
.flagged h2 { font-size: 1.15rem; }
.flagged .plain { font-size: 0.88em; }
/* responsive table: stacked cards on mobile */
@media (max-width: 900px) {
  .entries thead { display: none; }
  .entries tr { display: block; margin-bottom: 12px; border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
  .entries td { display: block; text-align: right; padding: 10px 12px; border-bottom: none; }
  .entries td:last-child { border-bottom: none; }
  .entries td::before { content: attr(data-label); float: left; font-weight: 700; font-size: 0.78em; color: var(--muted); text-transform: uppercase; }
  .entries td[data-label="Competition"]::before { content: ""; float: none; display: block; }
  .entries td[data-label="Competition"] { text-align: left; }
}
/* footer */
.site-footer { border-top: 1px solid var(--border); background: var(--surface); padding: 26px 24px; margin-top: 40px; font-size: 0.88em; color: var(--muted); max-width: 1200px; margin-left: auto; margin-right: auto; }
.site-footer p { margin: 0 0 8px; }
"""
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    with open(os.path.join(ROOT, "assets", "style.css"), "w", encoding="utf-8") as f:
        f.write(css)


def write_js():
    js = """// Free Cash Prize Competition Ledger - page enhancements
document.addEventListener('DOMContentLoaded', function () {
  // Highlight the current page in nav
  var path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(function (a) {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });
});
"""
    with open(os.path.join(ROOT, "assets", "app.js"), "w", encoding="utf-8") as f:
        f.write(js)


def write_nojekyll():
    with open(os.path.join(ROOT, ".nojekyll"), "w", encoding="utf-8") as f:
        f.write("")


def fix_header_asset_paths():
    """The header() helper writes a placeholder style link; fix it to a real relative path."""
    import re
    for dirpath, _, filenames in os.walk(ROOT):
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            s = open(p, encoding="utf-8").read()
            s = s.replace(
                '<link rel="stylesheet" href="../assets/style.css" if false else "assets/style.css">',
                '<link rel="stylesheet" href="assets/style.css">' if dirpath == ROOT else '<link rel="stylesheet" href="../assets/style.css">'
            )
            s = s.replace('<script defer src="assets/app.js"></script>', '')
            with open(p, "w", encoding="utf-8") as f:
                f.write(s)


# ----------------------------------------------------------------------------
# README update
# ----------------------------------------------------------------------------

def write_readme(stats, flag_info):
    readme = f"""# Own2

Free Cash Prize Competition Ledger &mdash; a clean, dashboard-style site for finding free-to-enter competitions that pay real cash prizes.

## Live site
Published on GitHub Pages from this repo (see COORDINATION.md for the PR and merge record).

## What it is
A research catalog of {stats['total']} competition entries organized by category:
{', '.join(f"{v} {TYPE_NAME[k]}" for k, v in sorted(stats['by_type'].items()))}.

Entries come from the **Free Money &amp; Contest Ledger** (https://karagemop466-tech.github.io/FreeMoneyApps/),
pass S, reviewed {REVIEWED}. Each entry links to the operator&rsquo;s own official signup or rules page.
This is a research desk, not a sponsor. Official rules win every argument.

## Verification
- Every table row carries source link(s), tagged official / affiliate / forum.
- If a value cannot be confirmed from an official source, it is left blank and the row is flagged unverified. Nothing is inferred.
- {len(flag_info['no_official'])} entries have no official source and are flagged unverified on the Flagged for Review page.

## Site structure
- `index.html` &mdash; landing page / dashboard with category cards and recommended free entries
- `executive-summary.html` &mdash; executive summary, key findings, verification policy
- `categories/*.html` &mdash; one table per competition category
- `flagged.html` &mdash; Flagged for Review (unverified, caution, ended, mixed entries)
- `data/listings.json` &mdash; the underlying entry data
- `COORDINATION.md` &mdash; shared task board for multi-session work

## Flags
- {stats['by_status'].get('ended', 0)} ended / out-of-season entries
- {stats['by_status'].get('caution', 0)} caution entries
- {stats['by_status'].get('mixed', 0)} mixed entries (free play exists; cash requires an entry fee)
- {len(flag_info['no_official'])} entries without an official source (unverified)

## Important
US prizes of $600+ typically require a W-9; taxes are the winner&rsquo;s responsibility. Cash competitions are often geo-fenced.
Nobody legitimate asks you to pay a fee to collect a prize. Bonus cash, gems, and tickets are not withdrawable USD.
Always read the individual contest&rsquo;s own prize and payment terms before entering.
"""
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)


# ----------------------------------------------------------------------------
# Run
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    stats = build_index()
    flag_info = build_executive_summary()
    build_categories()
    build_flagged(flag_info)
    write_css()
    write_js()
    write_nojekyll()
    fix_header_asset_paths()
    write_readme(stats, flag_info)
    print("Site built.")
    print("Stats:", json.dumps(stats, indent=1))
    print("Flag info:", json.dumps({k: (v if isinstance(v, list) else v) for k, v in flag_info.items() if k != 'no_official'}, indent=1))
    print("No-official count:", len(flag_info["no_official"]))