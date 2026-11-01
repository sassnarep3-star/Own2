#!/usr/bin/env python3
"""Generate the static GitHub Pages site from data/entries.json."""
import json, html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "entries.json").read_text())
ENTRIES = DATA["entries"]
OUT = ROOT

TYPE_LABELS = DATA["byType"]
TYPE_ORDER = ["sports", "skill", "trivia", "forecasting", "market", "creative", "tech", "directory", "pools"]
TYPE_DISPLAY = {
    "sports": "Fantasy & sports picks",
    "skill": "Skill tournaments",
    "trivia": "Trivia competitions",
    "forecasting": "Forecasting tournaments",
    "market": "Market competitions",
    "creative": "Creative contests",
    "tech": "Tech & data competitions",
    "directory": "Directories & forums",
    "pools": "Free pool & league platforms",
}
TYPE_DESC = {
    "sports": "Free pick'em, survivor, bracket and fantasy contests with cash or merchandise prizes.",
    "skill": "Skill-based cash tournaments (solitaire, bingo, puzzle, esports). Some require entry fees for cash rooms.",
    "trivia": "Free trivia and rewards-app quiz games paying out in points or cash.",
    "forecasting": "Free prediction tournaments with cash or gift-card prize pools.",
    "market": "Free paper/demo trading competitions. Prizes are often account credits or funded accounts, not cash.",
    "creative": "Free writing, photography, design and film contests with cash prizes.",
    "tech": "Free data-science, ML and hackathon competitions with cash prizes.",
    "directory": "Directories and aggregators that list other free competitions.",
    "pools": "Free pool and survivor league platforms (group-funded prizes).",
}
STATUS_LABELS = {"live": "Active", "ended": "Ended / out of season", "caution": "Caution", "mixed": "Mixed (paid option)"}
FREEPATH_LABELS = {"full": "Free USD path", "partial": "Some free events", "paid-cash": "Cash needs entry fee"}

REVIEWED = DATA.get("reviewed")
PASS = DATA.get("pass")

def esc(t):
    return html.escape(str(t if t is not None else ""), quote=True)

def attr(t):
    return html.escape(str(t if t is not None else ""), quote=True)

def badge(kind, value):
    if not value:
        return ""
    cls = "b-%s-%s" % (kind, re.sub(r"[^a-z0-9]+", "-", str(value).lower()))
    return '<span class="badge %s">%s</span>' % (cls, esc(value))

def platforms(e):
    return " ".join('<span class="badge b-platform">%s</span>' % esc(x) for x in (e.get("platformLabels") or []))

def sources_html(e):
    out = []
    for s in (e.get("sources") or []):
        tier = (s.get("tier") or "").lower()
        cls = {"official": "tier-official", "affiliate": "tier-affiliate", "forum": "tier-forum"}.get(tier, "tier-forum")
        out.append('<span class="tier-tag %s">%s</span> <a href="%s" target="_blank" rel="noopener">%s</a>'
                   % (cls, esc(tier), attr(s.get("url", "")), esc(s.get("title") or s.get("url", ""))))
    return "<br>".join(out)

def entry_row(e, detail=False):
    unverified = e.get("unverified")
    flag = ' <span class="badge b-flag">UNVERIFIED</span>' if unverified else ""
    flag_note = ('<span class="flag-note">UNVERIFIED — no official source; prize/cash-out figures are blanked per policy.</span>'
                 if unverified else "")
    src = ""
    if e.get("officialSourceUrl"):
        src += '<a href="%s" target="_blank" rel="noopener">%s</a>' % (attr(e["officialSourceUrl"]), esc(e.get("officialSourceTitle") or "Official site"))
    else:
        src += '<span class="small">none found</span>'
    if e.get("refSourceUrl"):
        src += '<br><span class="small">Reference only (%s): <a href="%s" target="_blank" rel="noopener">%s</a></span>' % (
            esc(e.get("refSourceTier", "")), attr(e["refSourceUrl"]), esc(e.get("refSourceTitle") or ""))
    ios = ('<a class="ios-link" href="%s" target="_blank" rel="noopener">iOS app</a>' % attr(e.get("iosUrl", ""))) if e.get("iosUrl") else ""
    na = '— unverified' if unverified else '— not disclosed'
    prize = esc(e.get("prizeUsd") or "") or ('<span class="small">— %s</span>' % na)
    cashout = esc(e.get("minCashout") or "") or ('<span class="small">— %s</span>' % na)
    payout = esc(e.get("payoutText") or "") or ('<span class="small">— %s</span>' % na)
    parts = [
        '<tr%s>' % (' class="flag-row"' if unverified else ""),
        '<td class="name"><a href="%s" target="_blank" rel="noopener">%s</a>%s<br>' % (attr(e.get("signupUrl", "")), esc(e["name"]), flag),
        '<span class="tiny">%s%s</span>%s</td>' % (esc(e.get("short", "")), ios, flag_note),
        '<td>' + esc(e["typeLabel"]) + '</td>',
        '<td>' + badge("status", e["statusLabel"]) + '</td>',
        '<td>' + badge("path", e["freePathLabel"]) + '</td>',
        '<td>' + platforms(e) + '</td>',
        '<td>' + prize + '</td>',
        '<td>' + cashout + '</td>',
        '<td>' + payout + '</td>',
        '<td>' + esc(e.get("eligibility") or "—") + '</td>',
        '<td>' + esc(e.get("restricted") or "—") + '</td>',
        '<td class="nowrap">' + esc(e.get("lastChecked") or "") + '</td>',
        '<td class="source-cell">' + src + '</td>',
        '<td>' + esc(e.get("verificationLevel") or "—") + '</td>',
        '</tr>',
    ]
    return "".join(parts)

TABLE_HEADER = """<thead><tr>
<th>Competition</th>
<th>Category</th>
<th class="sortable" onclick="sortBy('statusLabel')">Status</th>
<th class="sortable" onclick="sortBy('freePathLabel')">Free path</th>
<th>Platforms</th>
<th class="sortable" onclick="sortBy('prizeUsd')">Prize</th>
<th class="sortable" onclick="sortBy('minCashout')">Cash-out floor</th>
<th>Pays via</th>
<th>Who can enter</th>
<th>Blocked / limits</th>
<th class="nowrap sortable" onclick="sortBy('lastChecked')">Last checked</th>
<th>Official source</th>
<th>Verification</th>
</tr></thead>"""

def table_body(rows):
    return "<tbody id=\"entries\">" + "".join(entry_row(e) for e in rows) + "</tbody>"

def page_shell(title, body, active_page="", root=""):
    # Integration: every shared skip link must have a focusable target.
    if 'id="content"' not in body:
        body = '<span id="content" tabindex="-1"></span>\n' + body
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s — Own2</title>
<link rel="stylesheet" href="%sassets/css/style.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="topbar">
  <div class="wrap inner">
    <a class="brand" href="%sindex.html"><div class="mark">$</div><div><strong>Own2</strong><small>Free cash prize competitions — dashboard</small></div></a>
    <nav class="top">
      <a href="%sindex.html"%s>All competitions</a>
      <a href="%sexecutive-summary.html"%s>Executive summary</a>
      <a href="%sreview.html"%s>How we review</a>
      <a href="%sflagged.html"%s>Flagged for review</a>
    </nav>
  </div>
</header>
%s
<footer>
  <div class="wrap">
    <p><strong>Own2</strong> — Free-to-enter cash prize competition ledger. Compiled from the public <em>Free Money &amp; Contest Ledger</em> (reviewed %s, pass %s).</p>
    <p>This site is an independent research compilation. It is not affiliated with any listed operator. Contest laws vary by state and country. Play only where legal. 18+/21+. Links and prize figures change — always open the official rules before you enter. US tax forms apply at $600+. Nobody legitimate will ever ask you to pay a fee to collect a prize.</p>
  </div>
</footer>
<script src="%sassets/js/app.js"></script>
<script>window.__OWN2_ENTRIES = %s;</script>
</body>
</html>""" % (
        attr(title), root, root,
        root, ' class="active"' if active_page == "all" else "",
        root, ' class="active"' if active_page == "exec" else "",
        root, ' class="active"' if active_page == "review" else "",
        root, ' class="active"' if active_page == "flagged" else "",
        body,
        esc(REVIEWED), esc(PASS),
        root, json.dumps(ENTRIES),
    )

# ---------------- Index (dashboard + full table) ----------------
def stat(num, label):
    return '<div class="stat"><b>%s</b><span>%s</span></div>' % (num, label)

index_body = []
index_body.append('<section class="hero" id="content">')
index_body.append('<p class="kicker">Free competitions that can pay real money</p>')
index_body.append('<h1>Own2 — Free Cash Prize Competitions</h1>')
index_body.append('<p class="lede">A clean, mobile-friendly dashboard of free-to-enter skill, prediction, fantasy, trivia, forecasting, market, creative and tech competitions that can pay real cash prizes. Every entry links to the operator&rsquo;s official signup or rules page. No sweepstakes, no deposit required to enter, no search box needed — filter by category, status or free path.</p>')
index_body.append('<div class="stats">')
index_body.append(stat(DATA["total"], "Listings"))
index_body.append(stat(sum(1 for e in ENTRIES if e["freePath"] == "full"), "True free paths"))
index_body.append(stat(sum(1 for e in ENTRIES if "ios" in e.get("platforms", [])), "iOS options"))
index_body.append(stat(DATA["unverifiedCount"], "Flagged — unverified"))
index_body.append('</div>')
index_body.append('<div class="notice"><b>Research desk, not a sponsor.</b> Official rules win every argument. US tax forms apply at $600+. Nobody legitimate will ever ask you to pay a fee to collect a prize. &ldquo;Free&rdquo; apps that pay only in gems, tickets or bonus cash are flagged so you know the difference.</div>')
index_body.append('</section>')

# jump nav
jumps = []
for t in TYPE_ORDER:
    jumps.append('<a href="categories/%s.html">%s (%d)</a>' % (t, TYPE_DISPLAY[t], TYPE_LABELS[t]))
index_body.append('<nav class="jumpnav" id="jumpnav" aria-label="Jump to section">' + " ".join(jumps) + '</nav>')

# filters
index_body.append('<main class="grid">')
index_body.append('<div class="filters">')
for kind, label, vals in [
    ("type", "Category", TYPE_DISPLAY),
    ("status", "Status", STATUS_LABELS),
    ("path", "Free path", FREEPATH_LABELS),
]:
    index_body.append('<div id="filters-%s"></div>' % kind)
    for v, lv in vals.items():
        index_body.append('<span class="filter tag" onclick="addFilter(\'%s\', %r, %r)">%s</span>' % (kind, lv, v, esc(lv)))
index_body.append('<input class="search" id="search" placeholder="Filter competitions…">')
index_body.append('<div id="filters-q"></div>')
index_body.append('</div>')
index_body.append('<p id="count" class="small" style="margin-bottom:8px;"></p>')
index_body.append('<div class="table-wrap"><table><caption style="text-align:left;font-weight:600;padding:8px 10px;font-size:13px;background:#fafafa;border-bottom:1px solid var(--border);">All %d entries — click a column header to sort, tap a filter chip to narrow.</caption>%s%s</table></div>' % (len(ENTRIES), TABLE_HEADER, table_body(ENTRIES)))
index_body.append('</main>')

# category index cards
index_body.append('<h2>Browse by category</h2>')
for t in TYPE_ORDER:
    n = TYPE_LABELS[t]
    index_body.append(
        '<div class="card">'
        '<h3><a href="categories/%s.html">%s</a></h3>' % (t, TYPE_DISPLAY[t]) +
        '<p class="small">%s — %d entries</p>' % (TYPE_DESC[t], n) +
        '</div>'
    )

with open(OUT / "index.html", "w") as f:
    f.write(page_shell("All competitions", "\n".join(index_body), active_page="all"))
print("wrote index.html")

# ---------------- Category pages ----------------
ROOT_LINK = "../"
for t in TYPE_ORDER:
    items = [e for e in ENTRIES if e["type"] == t]
    body = []
    body.append('<section class="cathead">')
    body.append('<p class="kicker">Category • %s</p>' % TYPE_DISPLAY[t])
    body.append('<h1>%s</h1>' % TYPE_DISPLAY[t])
    body.append('<p>%s</p>' % TYPE_DESC[t])
    body.append('<p><a class="btn" href="%sindex.html">&larr; All categories</a> <a class="btn btn-ghost" href="%sflagged.html">Flagged for review</a></p>' % (ROOT_LINK, ROOT_LINK))
    body.append('</section>')
    body.append('<div class="filters">')
    body.append('<div id="filters-status"></div>')
    for v, lv in STATUS_LABELS.items():
        body.append('<span class="filter tag" onclick="addFilter(\'status\', %r, %r)">%s</span>' % (lv, v, esc(lv)))
    body.append('<div id="filters-path"></div>')
    for v, lv in FREEPATH_LABELS.items():
        body.append('<span class="filter tag" onclick="addFilter(\'path\', %r, %r)">%s</span>' % (lv, v, esc(lv)))
    body.append('<input class="search" id="search" placeholder="Filter this category…">')
    body.append('</div>')
    body.append('<p id="count" class="small" style="margin-bottom:8px;"></p>')
    body.append('<div class="table-wrap"><table><caption style="text-align:left;font-weight:600;padding:8px 10px;font-size:13px;background:#fafafa;border-bottom:1px solid var(--border);">%d entries in %s</caption>%s%s</table></div>' % (len(items), TYPE_DISPLAY[t], TABLE_HEADER, table_body(items)))
    with open(OUT / "categories" / ("%s.html" % t), "w") as f:
        f.write(page_shell(TYPE_DISPLAY[t], "\n".join(body), active_page="", root=ROOT_LINK))
    print("wrote categories/%s.html (%d entries)" % (t, len(items)))

# ---------------- Flagged page ----------------
flagged = [e for e in ENTRIES if e.get("unverified")]
body = []
body.append('<section class="cathead">')
body.append('<p class="kicker">Flagged for review</p>')
body.append('<h1>Flagged for Review — Unverified Entries</h1>')
body.append('<p>The entries below <strong>have no official-source confirmation</strong>. Per site policy, their prize, cash-out and payout values are left blank and they are flagged for manual review. Do not rely on the figures shown in their reference links — treat them as unverified until the operator&rsquo;s own rules confirm them.</p>')
body.append('<div class="alert alert-red"><b>Why these are flagged:</b> each entry&rsquo;s sources are affiliate or forum sites only — none link to the operator&rsquo;s own rules, terms or game page. Values were taken from those third-party pages and cannot be confirmed from an official source.</div>')
body.append('<div class="alert alert-amber"><b>Also note:</b> the source repo&rsquo;s <em>100_VERIFIED_CONTESTS.md</em> is explicitly marked <strong>SUPERSEDED — DO NOT USE AS A SOURCE</strong> (it failed verification and contained hallucinated entries). It is not used anywhere on this site. The maintained ledger is <em>assets/data.js</em> (pass S, reviewed 2026-08-19).</div>')
body.append('<div class="filters">')
body.append('<div id="filters-type"></div>')
for v, lv in TYPE_DISPLAY.items():
    body.append('<span class="filter tag" onclick="addFilter(\'type\', %r, %r)">%s</span>' % (lv, v, esc(lv)))
body.append('<input class="search" id="search" placeholder="Search flagged entries…">')
body.append('</div>')
body.append('<p id="count" class="small" style="margin-bottom:8px;"></p>')
body.append('<div class="table-wrap"><table>%s%s</table></div>' % (TABLE_HEADER, table_body(flagged)))
with open(OUT / "flagged.html", "w") as f:
    f.write(page_shell("Flagged for review", "\n".join(body), active_page="flagged"))
print("wrote flagged.html (%d entries)" % len(flagged))

# ---------------- Executive summary ----------------
exec_body = []
exec_body.append('<section class="cathead">')
exec_body.append('<p class="kicker">Executive summary</p>')
exec_body.append('<h1>Executive Summary — Free Cash Prize Competitions</h1>')
exec_body.append('</section>')
exec_body.append('<div class="grid" style="display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin-bottom:24px;">')
exec_body.append('<div class="card"><h3>Source &amp; method</h3><p class="small">Compiled from the public <em>Free Money &amp; Contest Ledger</em> (<a href="https://karagemop466-tech.github.io/FreeMoneyApps/" target="_blank" rel="noopener">karagemop466-tech.github.io/FreeMoneyApps/</a>), pass S, reviewed %s. 206 listings extracted and restructured into a filterable dashboard. The source repo&rsquo;s superseded <em>100_VERIFIED_CONTESTS.md</em> was deliberately excluded (it failed verification and contained hallucinated entries).</p></div>' % esc(REVIEWED))
exec_body.append('<div class="card"><h3>Scale</h3><p class="small"><b>%d listings</b> across 9 categories. <b>%d</b> are true free paths (no entry fee), <b>%d</b> have some free events, <b>4</b> are paid-cash apps (free gem rooms exist; cash rooms charge entry). <b>%d</b> are live today; %d ended/out of season; %d carry a caution; %d are mixed paid/free.</p></div>' % (
    DATA["total"],
    sum(1 for e in ENTRIES if e["freePath"] == "full"),
    sum(1 for e in ENTRIES if e["freePath"] == "partial"),
    sum(1 for e in ENTRIES if e["status"] == "live"),
    sum(1 for e in ENTRIES if e["status"] == "ended"),
    sum(1 for e in ENTRIES if e["status"] == "caution"),
    sum(1 for e in ENTRIES if e["status"] == "mixed")))
exec_body.append('<div class="card"><h3>iOS &amp; platforms</h3><p class="small"><b>%d</b> entries offer an iOS app. Most are browser-based; a few are iOS-only. Android availability is noted where the source lists it.</p></div>' % sum(1 for e in ENTRIES if "ios" in e.get("platforms", [])))
exec_body.append('<div class="card"><h3>Flagged for review</h3><p class="small"><b>%d</b> entries have <strong>no official source</strong> and are listed on the Flagged for Review page. Their prize and cash-out figures are blanked pending confirmation from the operator&rsquo;s own rules.</p></div>' % DATA["unverifiedCount"])
exec_body.append('</div>')

exec_body.append('<h2>Category breakdown</h2>')
exec_body.append('<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:24px;">')
exec_body.append('<tr><th style="text-align:left;padding:8px;border-bottom:1px solid var(--border);">Category</th><th style="text-align:right;padding:8px;border-bottom:1px solid var(--border);">Entries</th><th style="text-align:right;padding:8px;border-bottom:1px solid var(--border);">Live</th><th style="text-align:right;padding:8px;border-bottom:1px solid var(--border);">Ended</th><th style="text-align:right;padding:8px;border-bottom:1px solid var(--border);">Caution</th><th style="text-align:right;padding:8px;border-bottom:1px solid var(--border);">Unverified</th></tr>')
for t in TYPE_ORDER:
    items = [e for e in ENTRIES if e["type"] == t]
    exec_body.append('<tr><td style="padding:8px;border-bottom:1px solid var(--border);"><a href="categories/%s.html">%s</a></td>' % (t, TYPE_DISPLAY[t]))
    exec_body.append('<td style="padding:8px;border-bottom:1px solid var(--border);text-align:right;">%d</td>' % len(items))
    exec_body.append('<td style="padding:8px;border-bottom:1px solid var(--border);text-align:right;">%d</td>' % sum(1 for e in items if e["status"]=="live"))
    exec_body.append('<td style="padding:8px;border-bottom:1px solid var(--border);text-align:right;">%d</td>' % sum(1 for e in items if e["status"]=="ended"))
    exec_body.append('<td style="padding:8px;border-bottom:1px solid var(--border);text-align:right;">%d</td>' % sum(1 for e in items if e["status"]=="caution"))
    exec_body.append('<td style="padding:8px;border-bottom:1px solid var(--border);text-align:right;">%d</td>' % sum(1 for e in items if e.get("unverified")))
    exec_body.append('</tr>')
exec_body.append('</table>')

exec_body.append('<h2>Notable cash prizes (per operator-published figures)</h2>')
exec_body.append('<ul>')
exec_body.append('<li><b>Beat the Streak (MLB)</b> — $5,600,000 headline (&asymp;$3,000,000 lump sum); $10,000 top streak prize. Free, 21+, US/Canada excluding Quebec.</li>')
exec_body.append('<li><b>ARC Prize 2026 (via Kaggle)</b> — $2,000,000 across three tracks; submissions due 2 Nov 2026.</li>')
exec_body.append('<li><b>HIPA photography award</b> — $1,000,000 total pool, $200,000 grand prize.</li>')
exec_body.append('<li><b>Devpost hackathons</b> — up to $685,000 (RevenueCat Shipaton) on live index.</li>')
exec_body.append('<li><b>Sony World Photography Awards</b> — $25,000 Photographer of the Year; $5,000 Open winner.</li>')
exec_body.append('<li><b>Trading demo competitions</b> — e.g. TradingView The Leap $50,000; moomoo $200,000 total; MultiBank $15,000/round; XM $25,000/week. Prizes are often account credits or funded accounts, not direct cash.</li>')
exec_body.append('</ul>')

exec_body.append('<h2>How to use this site</h2>')
exec_body.append('<ol>')
exec_body.append('<li>Browse <strong>All competitions</strong> or jump to a category from the dashboard.</li>')
exec_body.append('<li>Use the filter chips and search box to narrow by category, status (Active / Ended / Caution) or free path.</li>')
exec_body.append('<li>Open the <strong>Official source</strong> link for every entry before entering — confirm the current prize and rules yourself.</li>')
exec_body.append('<li>Check <strong>Flagged for review</strong> for entries that lack official-source confirmation; treat them as unverified.</li>')
exec_body.append('</ol>')

exec_body.append('<h2>Honest framing</h2>')
exec_body.append('<ul>')
exec_body.append('<li>Most entrants earn $0. Treat these as competitions, not income.</li>')
exec_body.append('<li>Many &ldquo;free&rdquo; apps only pay in gems/points; cash rooms usually require an entry fee you can lose.</li>')
exec_body.append('<li>Forecasting and tech contests can require weeks of work for winner-take-most outcomes.</li>')
exec_body.append('<li>Demo trading competition prizes are often funded-account challenges or account credits — read the terms before investing time.</li>')
exec_body.append('</ul>')
with open(OUT / "executive-summary.html", "w") as f:
    f.write(page_shell("Executive summary", "\n".join(exec_body), active_page="exec"))
print("wrote executive-summary.html")

# ---------------- Review / methodology ----------------
review_body = []
review_body.append('<section class="cathead">')
review_body.append('<p class="kicker">Methodology</p>')
review_body.append('<h1>How we review and verify</h1>')
review_body.append('</section>')
review_body.append('<div class="alert alert-blue"><b>Sourcing rule:</b> any listing that states a specific prize figure must cite the operator&rsquo;s own rules or game page. Each source carries a tier: <b>official</b> (operator&rsquo;s own site/rules), <b>affiliate</b> or <b>forum</b> (secondary — listed for reference, never as sole basis for a figure).</div>')
review_body.append('<h2>Verification policy</h2>')
review_body.append('<ul>')
review_body.append('<li>Every table row links to an official source where one exists.</li>')
review_body.append('<li>If a value cannot be confirmed from an official source, it is left blank and the entry is flagged as unverified.</li>')
review_body.append('<li>No values are inferred or filled in.</li>')
review_body.append('<li>Entries with no official source are published on the Flagged for Review page with their source links for manual review.</li>')
review_body.append('<li>Flagged irregularities do not block publication.</li>')
review_body.append('</ul>')
review_body.append('<h2>Source tiers used on this site</h2>')
review_body.append('<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:16px;">')
review_body.append('<tr><th style="text-align:left;padding:8px;border-bottom:1px solid var(--border);">Tier</th><th style="text-align:left;padding:8px;border-bottom:1px solid var(--border);">Meaning</th></tr>')
review_body.append('<tr><td style="padding:8px;border-bottom:1px solid var(--border);"><span class="tier-tag tier-official">official</span></td><td style="padding:8px;border-bottom:1px solid var(--border);">Operator&rsquo;s own rules, game page, terms of use or help center.</td></tr>')
review_body.append('<tr><td style="padding:8px;border-bottom:1px solid var(--border);"><span class="tier-tag tier-affiliate">affiliate</span></td><td style="padding:8px;border-bottom:1px solid var(--border);">Third-party review or affiliate page; consistent but not confirmed on the operator&rsquo;s domain.</td></tr>')
review_body.append('<tr><td style="padding:8px;border-bottom:1px solid var(--border);"><span class="tier-tag tier-forum">forum</span></td><td style="padding:8px;border-bottom:1px solid var(--border);">Community forum post; treat as secondary and unconfirmed.</td></tr>')
review_body.append('</table>')
review_body.append('<h2>Exclusions</h2>')
review_body.append('<ul>')
review_body.append('<li>Sweepstakes, sweepstakes casinos, casino products and contests requiring a gambling-operator account are excluded by policy.</li>')
review_body.append('<li>The source repo&rsquo;s <em>100_VERIFIED_CONTESTS.md</em> is superseded and not used.</li>')
review_body.append('<li>Paid-entry-only leagues (e.g. MyFantasyLeague after trial, Gridiron Games commissioner-paid) are noted as paid where applicable.</li>')
review_body.append('</ul>')
review_body.append('<p class="small">Last checked date on every entry: %s (source ledger pass %s).</p>' % (esc(REVIEWED), esc(PASS)))
with open(OUT / "review.html", "w") as f:
    f.write(page_shell("How we review", "\n".join(review_body), active_page="review"))
print("wrote review.html")

# ---------------- 404 ----------------
not_found = """
<section class="cathead">
  <p class="kicker">Not found</p>
  <h1>Page not found</h1>
  <p>The page you&rsquo;re looking for doesn&rsquo;t exist. Go to <a href="index.html">All competitions</a> or view the <a href="executive-summary.html">Executive summary</a>.</p>
</section>
"""
with open(OUT / "404.html", "w") as f:
    f.write(page_shell("Not found", not_found))
print("wrote 404.html")

# copy nojekyll
(OUT / ".nojekyll").write_text("")
print("wrote .nojekyll")

print("\nAll pages generated.")
print("Index: %d entries, %d unverified" % (len(ENTRIES), DATA["unverifiedCount"]))
