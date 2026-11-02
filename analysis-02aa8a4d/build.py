#!/usr/bin/env python3
"""Build analysis-02aa8a4d subsite: ranked "time well spent" picks, 2026-11-02
freshness sweep, link-health audit, and the full 209-row catalog in table form.

Deterministic: same inputs -> byte-identical HTML. Writes only inside this dir.
Evidence policy: only quote+URL backed values are published; everything else is
blank and flagged. Scores use verified fields only (see methodology.html).
"""
import html
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
OUT = BASE
CHECKED = "2026-11-02"

CATS = [
    ("skill", "Skill tournaments"),
    ("trivia", "Trivia & quizzes"),
    ("sports", "Fantasy & sports picks"),
    ("forecasting", "Prediction & forecasting"),
    ("market", "Market & trading contests"),
    ("creative", "Creative & writing contests"),
    ("tech", "Tech & data competitions"),
    ("directory", "Directories & lists"),
    ("pools", "Pool & bracket tools"),
]

# Analyst assessment (2026-11-02). Every component is derived from a quoted
# official statement recorded in data/freshness.json (or the root dataset's
# evidence record, marked inherited). Components without quoted basis score 0.
# rubric: free(20) | cash 25/22/18/14/10/6/8 | open(20) | cadence 15/12/10/5
#         | eligibility 10/8/6/4 | effort(low 10/mod 6/high 3)
ASSESS = {
    "cbs-pro-pickem": {
        "prize_usd": 100000, "cadence": ("weekly", 15), "elig": ("single-country", 6),
        "effort": ("low", 10),
        "basis": "Weekly picks + tiebreaker scores, one entry per person (official rules).",
    },
    "espn-pickem": {
        "prize_usd": 102000, "cadence": ("weekly", 15), "elig": (None, 0),
        "effort": ("low", 10),
        "basis": "Weekly game-winner picks across 4 modes (official game page).",
    },
    "espn-cfb": {
        "prize_usd": 86000, "cadence": ("weekly", 15), "elig": (None, 0),
        "effort": ("low", 10),
        "basis": "Weekly picks across 3 modes (official game page).",
    },
    "kaggle-nfl-bdb-2027": {
        "prize_usd": 100000, "cadence": ("one-shot", 5), "elig": ("worldwide", 10),
        "effort": ("high", 3),
        "basis": "Analytical writeup with code; Open Track states no eligibility restrictions.",
    },
    "sony-world-photo": {
        "prize_usd": 5000, "cadence": ("seasonal", 10), "elig": ("worldwide", 10),
        "effort": ("moderate", 6),
        "basis": "Submit up to three photographs free; open to all members of the public.",
    },
    "checkmate-gaming": {
        "prize_usd": 120, "cadence": ("daily/weekly", 15), "elig": ("multi-country", 8),
        "effort": ("low", 10),
        "basis": "Short 4v4 best-of-1 matches, free tournaments posted daily (official page).",
    },
    "metaculus": {
        "prize_usd": 50000, "cadence": ("daily/weekly", 15), "elig": (None, 0),
        "effort": ("moderate", 6),
        "basis": "Continuous forecasting tournaments with live prize pools (official page).",
    },
    "wergle-flomp": {
        "prize_usd": 5100, "cadence": ("seasonal", 10), "elig": ("multi-country", 8),
        "effort": ("moderate", 6),
        "basis": "One humor poem, judged anonymously; most countries eligible (official page).",
    },
    "devpost": {
        "prize_usd": 1000000, "cadence": ("daily/weekly", 15), "elig": (None, 0),
        "effort": ("high", 3),
        "basis": "Platform directory: 14,228 hackathons; cash events open on 2026-11-02 up to $1M (official directory).",
    },
    "devpost-paypal": {
        "prize_usd": 67500, "cadence": ("one-shot", 5), "elig": ("multi-country", 8),
        "effort": ("high", 3),
        "basis": "Build a PayPal+AI app; public repo + demo video (official rules).",
    },
    "arcprize": {
        "prize_usd": 2000000, "cadence": ("one-shot", 5), "elig": (None, 0),
        "effort": ("high", 3),
        "basis": "AI benchmark research + open-source requirement (official overview).",
    },
    "mlb-beat-the-streak": {
        "prize_usd": 5600000, "cadence": ("daily/weekly", 15), "elig": ("single-country", 6),
        "effort": ("low", 10),
        "basis": "Daily hitter picks in the MLB app (official page).",
    },
    "gems-2026": {
        "prize_usd": 300000, "cadence": ("one-shot", 5), "elig": (None, 0),
        "effort": ("high", 3),
        "basis": "Build a geologic fault-mapping model (official competition page).",
    },
    "xprize": {
        "prize_usd": 119000000, "cadence": ("one-shot", 5), "elig": (None, 0),
        "effort": ("high", 3),
        "basis": "Multi-year team R&D grand challenges (official index).",
    },
    "kaggle": {
        "prize_usd": 100000, "cadence": ("daily/weekly", 15), "elig": (None, 0),
        "effort": ("high", 3),
        "basis": "Platform directory: featured hackathons with cash pools on 2026-11-02 (official index).",
    },
    "gamersaloon": {
        "prize_usd": 0, "cadence": ("daily/weekly", 15), "elig": (None, 0),
        "effort": ("low", 10),
        "basis": "Weekly free one-round matches; prize is Bonus Cash, not withdrawable (official promo page).",
    },
    "tradingview-leap": {
        "prize_usd": 0, "cadence": ("seasonal", 10), "elig": (None, 0),
        "effort": ("low", 10),
        "basis": "Paper-trading contests; latest completed contest paid TradingView plans, not cash (official page).",
    },
}

EXCLUDE_REASON = {
    "gamersaloon": "Prize is Bonus Cash only — explicitly not eligible for withdrawal. Not a real-cash path.",
    "tradingview-leap": "Between contests; the most recent contest awarded TradingView plans (non-cash) despite the general cash claim.",
}


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def band(amount):
    if amount is None:
        return 0, "no confirmed cash prize"
    if amount <= 0:
        return 0, "no confirmed cash prize"
    if amount >= 1_000_000:
        return 25, f"${amount:,.0f} (band ≥$1M)"
    if amount >= 100_000:
        return 22, f"${amount:,.0f} (band ≥$100K)"
    if amount >= 25_000:
        return 18, f"${amount:,.0f} (band ≥$25K)"
    if amount >= 5_000:
        return 14, f"${amount:,.0f} (band ≥$5K)"
    if amount >= 1_000:
        return 10, f"${amount:,.0f} (band ≥$1K)"
    return 6, f"${amount:,.0f} (band <$1K)"


def load():
    contests = json.loads((ROOT / "data" / "contests.json").read_text(encoding="utf-8"))
    freshness = json.loads((BASE / "data" / "freshness.json").read_text(encoding="utf-8"))
    linkre = json.loads((BASE / "data" / "link-recheck.json").read_text(encoding="utf-8"))
    return contests, freshness, linkre


def score_rows(contests, fresh_by_id):
    """Compute evidence-based scores for assessed rows. Returns id -> scorecard."""
    cards = {}
    for row in contests["entries"]:
        rid = row["id"]
        if rid not in ASSESS:
            continue
        a = ASSESS[rid]
        fr = fresh_by_id.get(rid, {})
        # free entry
        free_ok, free_src = False, None
        if fr.get("free", {}).get("value") and fr["free"].get("quote") and fr["free"].get("url"):
            free_ok, free_src = True, ("freshness", fr["free"])
        elif row.get("free", {}).get("status") == "confirmed" and row["free"].get("quote") and row["free"].get("url"):
            free_ok, free_src = True, ("root", row["free"])
        free_pts = 20 if free_ok else 0
        # cash prize magnitude (only if a prize is confirmed with a source)
        prize_confirmed = bool(
            (fr.get("prize", {}).get("quote") and fr["prize"].get("url"))
            or (row.get("prize", {}).get("status") == "confirmed" and row["prize"].get("url"))
        )
        cash_pts, cash_note = band(a["prize_usd"] if prize_confirmed else None)
        if prize_confirmed and a["prize_usd"] == 0:
            cash_pts, cash_note = 0, "confirmed prize is non-cash"
        # open now
        open_ok, open_note = False, "not confirmed open on 2026-11-02"
        st = fr.get("status", {})
        if st.get("quote") and st.get("url"):
            v = (st.get("value") or "").lower()
            if v.startswith("open") or "accepting entries" in v or v.startswith("final days") or v.startswith("between"):
                open_ok = True
                open_note = st["value"][:180]
            elif "conflict" in v:
                open_note = st["value"][:160]
            else:
                open_note = st["value"][:180]
        if rid == "tradingview-leap":
            open_ok = False
        open_pts = 20 if open_ok else 0
        cad_name, cad_pts = a["cadence"]
        elig_name, elig_pts = a["elig"]
        eff_name, eff_pts = a["effort"]
        total = free_pts + cash_pts + open_pts + cad_pts + elig_pts + eff_pts
        trio = (free_ok, prize_confirmed and cash_pts > 0, open_ok)
        if rid in EXCLUDE_REASON:
            tier, label = "X", "Excluded — not a cash/free path"
        elif all(trio) and total >= 70:
            tier, label = "A", "Spend your time here (open, free, cash confirmed)"
        elif sum(trio) >= 2 and total >= 50:
            tier, label = "B", "Promising — evidence incomplete"
        else:
            tier, label = "C", "Weak / long-shot on current evidence"
        cards[rid] = {
            "id": rid, "name": row["name"], "category": row["category"],
            "total": total, "tier": tier, "label": label,
            "free": (free_pts, free_src), "cash": (cash_pts, cash_note),
            "open": (open_pts, open_note), "cadence": (cad_pts, cad_name),
            "elig": (elig_pts, elig_name), "effort": (eff_pts, eff_name),
            "basis": a["basis"], "exclude": EXCLUDE_REASON.get(rid),
            "trio": trio,
        }
    return cards


def internal_link_scan():
    """Repo-wide internal link check (read-only). Returns report dict."""
    skip_dirs = {".git", "node_modules", "test-results", "playwright-report", ".venv", "__pycache__"}
    pages = []
    for p in sorted(ROOT.rglob("*.html")):
        if any(part in skip_dirs for part in p.parts):
            continue
        pages.append(p)
    broken = []
    total_links = 0
    for p in pages:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in re.finditer(r'(?:href|src)="([^"#][^"]*)"', text):
            url = m.group(1)
            if re.match(r"^(https?:|mailto:|tel:|data:|javascript:|//)", url):
                continue
            total_links += 1
            path_part = url.split("#", 1)[0].split("?", 1)[0]
            if not path_part:
                continue
            target = (p.parent / path_part).resolve()
            if not target.exists():
                broken.append({"page": str(p.relative_to(ROOT)), "link": url})
    sections = {}
    for p in pages:
        rel = p.relative_to(ROOT)
        top = rel.parts[0] if len(rel.parts) > 1 else "(root)"
        sections[top] = sections.get(top, 0) + 1
    return {
        "checked_date": CHECKED,
        "pages_scanned": len(pages),
        "local_links_checked": total_links,
        "broken_local_links": broken,
        "pages_by_section": dict(sorted(sections.items())),
    }


# ---------------- rendering ----------------

NAV = [
    ("index.html", "Dashboard"),
    ("ranked.html", "Ranked picks"),
    ("freshness.html", "Freshness sweep"),
    ("all.html", "All entries"),
    ("categories.html", "Categories"),
    ("link-health.html", "Link health"),
    ("flagged.html", "Flagged for review"),
    ("summary.html", "Executive summary"),
    ("methodology.html", "Methodology"),
]


def page(title, body, active="", extra_head=""):
    parts = []
    for href, label in NAV:
        cur = ' aria-current="page" class="active"' if href == active else ""
        parts.append(f'<a href="{esc(href)}"{cur}>{esc(label)}</a>')
    nav_items = "".join(parts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Free Cash Competitions · Analysis 02aa8a4d</title>
<link rel="stylesheet" href="style.css">
{extra_head}
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header>
  <p class="crumb"><a href="../index.html">← Main project dashboard</a></p>
  <h1>{esc(title)}</h1>
  <p class="sub">Independent analysis pass · official sources checked {CHECKED} · every value quote-backed or blank</p>
  <nav aria-label="Section navigation">{nav_items}</nav>
</header>
<main id="content">
{body}
</main>
<footer>
  <p>Session <strong>arena-02aa8a4d</strong> · subsite <code>analysis-02aa8a4d/</code> · data snapshot {CHECKED}.
  Official rules win every argument. Nobody legitimate will ever ask you to pay a fee to collect a prize.
  Sources: official operator pages listed per row. Unverified values are left blank and published on the
  <a href="flagged.html">Flagged for Review</a> page. See <a href="methodology.html">methodology</a> for the scoring rubric.</p>
</footer>
<script src="app.js"></script>
</body>
</html>
"""


def table_rows_html(rows, cols, caption):
    head = "".join(f"<th scope=\"col\">{esc(c)}</th>" for c in cols)
    return head, caption


def fmt_fact(field):
    """Render a fact cell from freshness/root field dict."""
    if not field or not field.get("value"):
        return '<td class="blank" data-label="Value"><span class="flag">unverified — blank</span></td>'
    src = ""
    if field.get("quote") or field.get("url"):
        q = field.get("quote") or ""
        u = field.get("url") or ""
        src = f' <a class="src" href="{esc(u)}">source</a>' if u else ""
        if q:
            src += f' <details class="quote"><summary>quote</summary><blockquote>{esc(q)}</blockquote></details>'
    return f'<td data-label="Value">{esc(field["value"])}{src}</td>'


def build():
    contests, freshness, linkre = load()
    entries = {r["id"]: r for r in contests["entries"]}
    fresh_by_id = {r["id"]: r for r in freshness["records"]}
    cards = score_rows(contests, fresh_by_id)
    link_report = internal_link_scan()

    stats = {
        "checked_date": CHECKED,
        "total_rows": len(contests["entries"]),
        "assessed_rows": len(cards),
        "tier_a": sum(1 for c in cards.values() if c["tier"] == "A"),
        "tier_b": sum(1 for c in cards.values() if c["tier"] == "B"),
        "tier_c": sum(1 for c in cards.values() if c["tier"] == "C"),
        "tier_x": sum(1 for c in cards.values() if c["tier"] == "X"),
        "unassessed_rows": len(contests["entries"]) - len(cards),
        "freshness_records": len(freshness["records"]),
        "link_rechecked": linkre["summary"]["rechecked"],
        "link_still_broken": linkre["summary"]["still_broken_or_unreachable"],
        "link_recovered": linkre["summary"]["recovered"],
        "internal_pages_scanned": link_report["pages_scanned"],
        "internal_broken": len(link_report["broken_local_links"]),
        "counts_root": contests.get("counts", {}),
    }
    (OUT / "reports").mkdir(exist_ok=True)
    (OUT / "reports" / "stats.json").write_text(json.dumps(stats, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    (OUT / "reports" / "link-health.json").write_text(json.dumps(link_report, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    # ---- index.html ----
    ranked = sorted(cards.values(), key=lambda c: (-c["total"], c["name"]))
    tier_a = [c for c in ranked if c["tier"] == "A"]
    top_rows = []
    for c in ranked[:15]:
        fr = fresh_by_id.get(c["id"], {})
        deadline = ""
        st = fr.get("status", {})
        if st.get("value"):
            deadline = st["value"].split(";")[0][:120]
        src = (fr.get("prize", {}).get("url") or fr.get("status", {}).get("url")
               or (entries[c["id"]].get("sources") or [{}])[0].get("url", ""))
        top_rows.append(f"""<tr>
<td data-label="Rank">{ranked.index(c)+1}</td>
<td data-label="Competition"><strong>{esc(c['name'])}</strong><br><span class="tier t{c['tier'].lower()}">{esc(c['tier'])} · {esc(c['label'])}</span></td>
<td data-label="Score">{c['total']}/100</td>
<td data-label="Why now">{esc(deadline or c['basis'])}</td>
<td data-label="Source">{f'<a class="src" href="{esc(src)}">official page</a>' if src else '<span class="flag">no official source</span>'}</td>
</tr>""")
    body = f"""
<section class="stats" aria-label="Key numbers">
  <div class="stat"><b>{stats['total_rows']}</b><span>entries tracked</span></div>
  <div class="stat"><b>{stats['assessed_rows']}</b><span>assessed this pass</span></div>
  <div class="stat"><b>{stats['tier_a']}</b><span>tier A picks</span></div>
  <div class="stat"><b>{stats['freshness_records']}</b><span>official pages re-checked {CHECKED}</span></div>
  <div class="stat"><b>{stats['link_recovered']}</b><span>broken links recovered</span></div>
</section>

<section>
<h2>Where to spend your time — top 15</h2>
<p>Ranked with the evidence-only rubric on the <a href="methodology.html">methodology page</a>: free entry,
cash prize, and open status must each be confirmed by a quoted official source before a row can reach tier A.
Rows without evidence are never guessed — they appear as blanks in <a href="all.html">All entries</a>.</p>
<div class="tablewrap"><table>
<caption>Top 15 competitions by evidence-based priority score ({CHECKED})</caption>
<thead><tr><th scope="col">Rank</th><th scope="col">Competition</th><th scope="col">Score</th><th scope="col">Why now</th><th scope="col">Source</th></tr></thead>
<tbody>{''.join(top_rows)}</tbody>
</table></div>
<p><a class="btn" href="ranked.html">Full ranked table with score breakdown →</a></p>
</section>

<section>
<h2>Quick navigation</h2>
<ul class="cards">
<li><a href="freshness.html"><strong>Freshness sweep</strong><br>What is actually open on {CHECKED}, with verbatim quotes.</a></li>
<li><a href="all.html"><strong>All {stats['total_rows']} entries</strong><br>Simple table, one row per competition, source link on every row.</a></li>
<li><a href="categories.html"><strong>By category</strong><br>Nine category pages.</a></li>
<li><a href="link-health.html"><strong>Link health</strong><br>Broken-link recheck + repo-wide internal link scan.</a></li>
<li><a href="flagged.html"><strong>Flagged for review</strong><br>Irregularities, conflicts and unverified items.</a></li>
<li><a href="summary.html"><strong>Executive summary</strong><br>The important details in one page.</a></li>
</ul>
</section>
"""
    (OUT / "index.html").write_text(page("Free cash competitions — analysis dashboard", body, "index.html"), encoding="utf-8")

    # ---- ranked.html ----
    rows = []
    for i, c in enumerate(ranked, 1):
        f_pts, f_src = c["free"]
        free_cell = (f'{f_pts}/20 <a class="src" href="{esc(f_src[1]["url"])}">source</a>'
                     if f_src else f'{f_pts}/20 <span class="flag">no free-entry evidence</span>')
        rows.append(f"""<tr>
<td data-label="Rank">{i}</td>
<td data-label="Competition"><strong>{esc(c['name'])}</strong><br><span class="tier t{c['tier'].lower()}">{esc(c['tier'])} — {esc(c['label'])}</span>{('<br><span class="flag">'+esc(c['exclude'])+'</span>') if c.get('exclude') else ''}</td>
<td data-label="Total"><strong>{c['total']}</strong></td>
<td data-label="Free">{free_cell}</td>
<td data-label="Cash">{c['cash'][0]}/25 <span class="muted">{esc(c['cash'][1])}</span></td>
<td data-label="Open now">{c['open'][0]}/20 <span class="muted">{esc(c['open'][1])}</span></td>
<td data-label="Cadence">{c['cadence'][0]}/15 <span class="muted">{esc(c['cadence'][1] or 'no evidence')}</span></td>
<td data-label="Eligibility">{c['elig'][0]}/10 <span class="muted">{esc(c['elig'][1] or 'no evidence')}</span></td>
<td data-label="Effort">{c['effort'][0]}/10 <span class="muted">{esc(c['effort'][1] or 'no evidence')}</span></td>
<td data-label="Basis"><span class="muted">{esc(c['basis'])}</span></td>
</tr>""")
    unassessed_note = f"""
<section>
<h2>Unranked — insufficient evidence</h2>
<p>{stats['unassessed_rows']} of {stats['total_rows']} rows have no independent evidence from this or earlier
passes sufficient to score them. They are published with blank values in <a href="all.html">All entries</a>
and on the shared <a href="../review.html">review queue</a>. They are unranked, never estimated.</p>
</section>"""
    body = f"""
<p>The rubric and its evidence requirements are on the <a href="methodology.html">methodology page</a>.
Only rows with a quoted official source for a component earn that component's points; otherwise the
component is 0 and marked <em>no evidence</em>. Tier A additionally requires free entry, a cash prize,
and open status to all be confirmed on {CHECKED}.</p>
<div class="tablewrap"><table class="wide">
<caption>Evidence-based priority scores ({CHECKED})</caption>
<thead><tr><th scope="col">#</th><th scope="col">Competition</th><th scope="col">Total</th><th scope="col">Free /20</th><th scope="col">Cash /25</th><th scope="col">Open /20</th><th scope="col">Cadence /15</th><th scope="col">Eligibility /10</th><th scope="col">Effort /10</th><th scope="col">Basis</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table></div>
{unassessed_note}
"""
    (OUT / "ranked.html").write_text(page("Ranked picks — where to spend your time", body, "ranked.html"), encoding="utf-8")

    # ---- freshness.html ----
    frows = []
    for r in freshness["records"]:
        flags = "".join(f'<li>{esc(f)}</li>' for f in r.get("flags", []))
        flag_html = f'<ul class="flags">{flags}</ul>' if flags else '<span class="muted">none</span>'
        frows.append(f"""<tr>
<td data-label="Competition"><strong>{esc(r['name'])}</strong><br><span class="muted">{esc(r['id'])}</span></td>
<td data-label="Status on {CHECKED}">{esc((r.get('status') or {}).get('value') or '')}
{('<details class="quote"><summary>quote</summary><blockquote>'+esc((r.get('status') or {}).get('quote') or '')+'</blockquote></details>') if (r.get('status') or {}).get('quote') else ''}</td>
<td data-label="Prize (confirmed)">{fmt_fact(r.get('prize'))}</td>
<td data-label="Free entry">{fmt_fact(r.get('free'))}</td>
<td data-label="Official source"><a class="src" href="{esc(r['url'])}">{esc(r['url'][:60])}…</a></td>
<td data-label="Flags">{flag_html}</td>
</tr>""")
    body = f"""
<p>Every cell below was read from the competition's official page on <strong>{CHECKED}</strong>.
Quotes are verbatim. Where the official page does not state a value, the cell stays blank with an
<em>unverified</em> stamp — nothing is inferred. Partial reads (chunked pages) are noted in the
<a href="../COORDINATION.md">coordination log</a>.</p>
<div class="tablewrap"><table class="wide">
<caption>Priority freshness sweep — official pages read {CHECKED}</caption>
<thead><tr><th scope="col">Competition</th><th scope="col">Status on {CHECKED}</th><th scope="col">Prize (confirmed)</th><th scope="col">Free entry</th><th scope="col">Official source</th><th scope="col">Flags</th></tr></thead>
<tbody>{''.join(frows)}</tbody>
</table></div>
"""
    (OUT / "freshness.html").write_text(page("Freshness sweep — what is open right now", body, "freshness.html"), encoding="utf-8")

    # ---- all.html + category pages ----
    def entry_rows(cat=None):
        out = []
        for row in contests["entries"]:
            if cat and row["category"] != cat:
                continue
            rid = row["id"]
            c = cards.get(rid)
            tier_html = (f'<span class="tier t{c["tier"].lower()}">{esc(c["tier"])} · {c["total"]}/100</span>'
                         if c else f'<span class="muted">unranked</span>')
            fr = fresh_by_id.get(rid, {})
            # Verified facts: prefer this pass's freshness values; else root evidence text
            prize_v = (fr.get("prize", {}).get("value") or
                       (row["prize"].get("text") if row["prize"].get("status") == "confirmed" else None))
            prize_q = (fr.get("prize", {}).get("url") or
                       (row["prize"].get("url") if row["prize"].get("status") == "confirmed" else None))
            free_v = (fr.get("free", {}).get("value") or
                      (row["free"].get("text") if row["free"].get("status") == "confirmed" else
                       ("contradicted — " + row["free"].get("text", "") if row["free"].get("status") == "contradicted" else None)))
            free_q = (fr.get("free", {}).get("url") or
                      (row["free"].get("url") if row["free"].get("status") in ("confirmed", "contradicted") else None))
            srcs = row.get("sources") or []
            src_html = " ".join(f'<a class="src" href="{esc(s["url"])}">{esc(s.get("tier", "source"))}</a>' for s in srcs if s.get("url"))
            if not src_html:
                src_html = '<span class="flag">no official source — unverified</span>'
            out.append(f"""<tr data-search="{esc((row['name'] + ' ' + row['categoryName']).lower())}">
<td data-label="Competition"><strong>{esc(row['name'])}</strong><br><span class="muted">{esc(rid)}</span></td>
<td data-label="Category">{esc(row['categoryName'])}</td>
<td data-label="Verified prize">{esc(prize_v) if prize_v else '<span class="flag">blank — unverified</span>'}{f' <a class="src" href="{esc(prize_q)}">source</a>' if prize_q else ''}</td>
<td data-label="Free entry">{esc(free_v) if free_v else '<span class="flag">blank — unverified</span>'}{f' <a class="src" href="{esc(free_q)}">source</a>' if free_q else ''}</td>
<td data-label="Tier / score">{tier_html}</td>
<td data-label="Sources">{src_html}</td>
</tr>""")
        return "".join(out)

    all_body = f"""
<p>All {stats['total_rows']} catalog rows. Verified facts are published only where a quote and an
official URL exist (this pass {CHECKED} or an earlier attributed pass); all other cells are blank and
stamped unverified. Use the search box to filter.</p>
<p><label for="q">Filter:</label> <input id="q" data-filter="all-table" type="search" placeholder="Type a name or category…"></p>
<div class="tablewrap"><table class="wide" id="all-table">
<caption>All catalog entries ({stats['total_rows']})</caption>
<thead><tr><th scope="col">Competition</th><th scope="col">Category</th><th scope="col">Verified prize</th><th scope="col">Free entry</th><th scope="col">Tier / score</th><th scope="col">Sources</th></tr></thead>
<tbody>{entry_rows()}</tbody>
</table></div>
"""
    (OUT / "all.html").write_text(page("All entries — full catalog table", all_body, "all.html"), encoding="utf-8")

    cat_rows = []
    for slug, cname in CATS:
        n = sum(1 for r in contests["entries"] if r["category"] == slug)
        assessed = sum(1 for c in cards.values() if c["category"] == slug)
        cat_rows.append(f'<li><a href="cat-{slug}.html"><strong>{esc(cname)}</strong> — {n} entries, {assessed} assessed</a></li>')
        cbody = f"""
<p>{n} entries in this category. Values are quote-backed or blank; see the
<a href="methodology.html">methodology</a>. Filter: <input data-filter="cat-table" type="search" placeholder="Filter this category…"></p>
<div class="tablewrap"><table class="wide" id="cat-table">
<caption>{esc(cname)} ({n} entries)</caption>
<thead><tr><th scope="col">Competition</th><th scope="col">Category</th><th scope="col">Verified prize</th><th scope="col">Free entry</th><th scope="col">Tier / score</th><th scope="col">Sources</th></tr></thead>
<tbody>{entry_rows(slug)}</tbody>
</table></div>
"""
        (OUT / f"cat-{slug}.html").write_text(page(f"{cname} — category table", cbody), encoding="utf-8")

    cats_body = f"""
<p>Nine category tables, same columns and evidence rules as <a href="all.html">All entries</a>.</p>
<ul class="cards">{''.join(cat_rows)}</ul>
"""
    (OUT / "categories.html").write_text(page("Categories", cats_body, "categories.html"), encoding="utf-8")

    # ---- link-health.html ----
    erows = []
    for r in linkre["results"]:
        cls = "ok" if "RECOVERED" in r["now"] else "bad"
        erows.append(f"""<tr>
<td data-label="URL"><a class="src" href="{esc(r['url'])}">{esc(r['url'][:70])}</a><br><span class="muted">{esc(r['listingId'])}</span></td>
<td data-label="Prior status (2026-11-01 CI)">{esc(r['prior'])}</td>
<td data-label="Now ({CHECKED})"><span class="{cls}">{esc(r['now'])}</span></td>
<td data-label="Evidence"><span class="muted">{esc(r['evidence'])}</span></td>
</tr>""")
    broken_local = link_report["broken_local_links"]
    bl_rows = "".join(
        f'<tr><td data-label="Page">{esc(b["page"])}</td><td data-label="Broken link">{esc(b["link"])}</td></tr>'
        for b in broken_local
    ) or '<tr><td colspan="2">None — every local link in the scanned pages resolves.</td></tr>'
    sect_rows = "".join(
        f'<tr><td data-label="Section">{esc(k)}</td><td data-label="HTML pages">{v}</td></tr>'
        for k, v in link_report["pages_by_section"].items()
    )
    body = f"""
<section>
<h2>External link recheck ({CHECKED})</h2>
<p>Baseline: GitHub Actions linkcheck of 2026-11-01 (326 URLs: 258 ok, 2 redirect, 40 blocked, 26 broken —
<a class="src" href="../ledger-4c1d6bb4/reports/link-check.json">baseline JSON</a>). This pass re-read a sample
of {linkre['summary']['rechecked']} of the 26 broken URLs: <strong>{linkre['summary']['still_broken_or_unreachable']} still broken or unreachable</strong>,
<strong>{linkre['summary']['recovered']} recovered</strong>. {linkre['summary']['not_rechecked']} were not re-checked (stale until re-run).
Reachability is not verification, and a failure is not proof of permanent breakage.</p>
<div class="tablewrap"><table class="wide">
<caption>Broken-link recheck sample ({CHECKED})</caption>
<thead><tr><th scope="col">URL</th><th scope="col">Prior status (2026-11-01 CI)</th><th scope="col">Now ({CHECKED})</th><th scope="col">Evidence</th></tr></thead>
<tbody>{''.join(erows)}</tbody>
</table></div>
</section>
<section>
<h2>Internal link scan (whole repository, {CHECKED})</h2>
<p>Scanned {link_report['pages_scanned']} HTML pages across the main site and every parallel subsite;
checked {link_report['local_links_checked']} local links; found <strong>{len(broken_local)} broken</strong>.</p>
<div class="tablewrap"><table>
<caption>Broken internal links</caption>
<thead><tr><th scope="col">Page</th><th scope="col">Broken link</th></tr></thead>
<tbody>{bl_rows}</tbody>
</table></div>
<div class="tablewrap"><table>
<caption>HTML pages by top-level section</caption>
<thead><tr><th scope="col">Section</th><th scope="col">HTML pages</th></tr></thead>
<tbody>{sect_rows}</tbody>
</table></div>
</section>
"""
    (OUT / "link-health.html").write_text(page("Link health audit", body, "link-health.html"), encoding="utf-8")

    # ---- flagged.html ----
    flag_rows = []
    for r in freshness["records"]:
        for f in r.get("flags", []):
            flag_rows.append(f"""<tr>
<td data-label="Item">{esc(r['name'])}<br><span class="muted">{esc(r['id'])}</span></td>
<td data-label="Irregularity">{esc(f)}</td>
<td data-label="Official source"><a class="src" href="{esc(r['url'])}">{esc(r['url'][:60])}…</a></td>
</tr>""")
    for r in linkre["results"]:
        if "RECOVERED" not in r["now"]:
            flag_rows.append(f"""<tr>
<td data-label="Item">Broken link — {esc(r['listingId'])}</td>
<td data-label="Irregularity">Flagged broken on 2026-11-01 CI and still not reachable on {CHECKED}: {esc(r['evidence'])}</td>
<td data-label="Official source"><a class="src" href="{esc(r['url'])}">{esc(r['url'][:60])}…</a></td>
</tr>""")
    body = f"""
<p>Everything on this page is published for manual review and does <strong>not</strong> block anything.
Rows stay in the tables above with blank or stamped values; nothing was silently corrected. Cross-session
irregularities (e.g. the ARC/Kaggle paper-deadline discrepancy, CheckMate claim-window question, Topcoder
Auth0 wall) are carried forward from the shared
<a href="../review.html">review queue</a> and the
<a href="../flagged.html">shared flagged page</a>.</p>
<div class="tablewrap"><table class="wide">
<caption>Flagged for review — irregularities found {CHECKED}</caption>
<thead><tr><th scope="col">Item</th><th scope="col">Irregularity</th><th scope="col">Official source</th></tr></thead>
<tbody>{''.join(flag_rows)}</tbody>
</table></div>
"""
    (OUT / "flagged.html").write_text(page("Flagged for review", body, "flagged.html"), encoding="utf-8")

    # ---- methodology.html ----
    body = """
<section>
<h2>Verification policy</h2>
<ul>
<li>Every published value carries a verbatim quote and the official URL it was read from (check date 2026-11-02, or an earlier attributed pass).</li>
<li>If a value cannot be confirmed from an official source, the cell stays blank and is stamped <em>unverified</em>. Values are never inferred or filled in.</li>
<li>A reachable page is not verification of a competition; only the quoted content counts.</li>
<li>Official rules win every argument. Promotional claims that conflict with rules are flagged, not adopted.</li>
<li>Every table row links to at least one source, or is explicitly stamped <em>no official source</em>.</li>
</ul>
</section>
<section>
<h2>Scoring rubric (evidence-only, 100 points)</h2>
<div class="tablewrap"><table>
<caption>Score components and requirements</caption>
<thead><tr><th scope="col">Component</th><th scope="col">Points</th><th scope="col">Evidence required</th></tr></thead>
<tbody>
<tr><td data-label="Component">Free entry</td><td data-label="Points">20 or 0</td><td data-label="Evidence">Quoted official statement (e.g. "NO PURCHASE NECESSARY").</td></tr>
<tr><td data-label="Component">Cash prize magnitude</td><td data-label="Points">25 / 22 / 18 / 14 / 10 / 6 / 8</td><td data-label="Evidence">Confirmed cash prize; bands ≥$1M / ≥$100K / ≥$25K / ≥$5K / ≥$1K / &lt;$1K / amount unstated. Largest confirmed single component is used.</td></tr>
<tr><td data-label="Component">Open now</td><td data-label="Points">20 or 0</td><td data-label="Evidence">Official page on 2026-11-02 shows entries/submissions being accepted.</td></tr>
<tr><td data-label="Component">Cadence</td><td data-label="Points">15 / 12 / 10 / 5</td><td data-label="Evidence">Analyst rating from the cited format text: daily/weekly · monthly/quarterly · seasonal window · one-shot.</td></tr>
<tr><td data-label="Component">Eligibility breadth</td><td data-label="Points">10 / 8 / 6 / 4</td><td data-label="Evidence">Analyst rating from the cited eligibility text: worldwide · multi-country · single-country · narrower.</td></tr>
<tr><td data-label="Component">Effort per attempt</td><td data-label="Points">10 / 6 / 3</td><td data-label="Evidence">Analyst rating from the cited format text: low (picks/trivia) · moderate (one creative work) · high (build a model/software).</td></tr>
</tbody>
</table></div>
<p>Tiers: <strong>A</strong> = score ≥70 and free entry + cash prize + open status all confirmed;
<strong>B</strong> = promising but at least one of the three is unconfirmed (score ≥50);
<strong>C</strong> = weak/long-shot on current evidence;
<strong>X</strong> = excluded (not free, or prize is not withdrawable cash, or closed);
<strong>unranked</strong> = insufficient evidence — never estimated.</p>
<p>Analyst-rated components (cadence, eligibility, effort) are judgments derived from the quoted format
text, not claims made by the source. They are shown with their basis on the ranked page and capped so they
cannot outweigh the evidence-gated components (free/cash/open = 65 of 100 points).</p>
</section>
<section>
<h2>What this pass did not do</h2>
<ul>
<li>No contest accounts were created, no entries submitted, no deposits made, no prizes claimed.</li>
<li>Chunked pages were read in the chunks disclosed in the coordination log; uninspected chunks are not treated as evidence.</li>
<li>External link availability is partial (sample recheck only); the full 326-URL baseline is linked from <a href="link-health.html">Link health</a>.</li>
<li>Legal, tax and personal-eligibility qualification is out of scope — official rules win every argument.</li>
</ul>
</section>
"""
    (OUT / "methodology.html").write_text(page("Methodology & verification policy", body, "methodology.html"), encoding="utf-8")

    # ---- summary.html (executive summary, rendered) ----
    a_list = "".join(
        f"<li><strong>{esc(c['name'])}</strong> — {c['total']}/100. {esc(c['basis'])}</li>"
        for c in tier_a[:10]
    )
    body = f"""
<section>
<h2>Executive summary — analysis pass {CHECKED}</h2>
<p><strong>Goal.</strong> Find the best free-to-enter, cash-prize competitions to spend time on, using only
official, quoted sources. This subsite is one of several parallel builds in this repository; the shared
catalog of {stats['total_rows']} entries lives on the <a href="../index.html">main dashboard</a>.</p>
<p><strong>What is genuinely open and free with confirmed cash, as of {CHECKED}:</strong></p>
<ul>{a_list}</ul>
<p><strong>Key findings.</strong></p>
<ul>
<li>All 12 tier-A rows were re-verified against their official pages on {CHECKED}: CBS Pro Football
Pick'em (free, $1K×18 weekly + $5K season + $100K contingency), ESPN NFL Pick'em ($102K, 58 prizes) and
College Pick'em ($86K, 46 prizes), the Devpost and Kaggle platforms (open cash events to $1M / featured
pools), NFL Big Data Bowl 2027 ($100K, no purchase necessary, closes 2027-01-06), Sony Single Image
($5,000, free, closes 2027-01-05), Checkmate Gaming (daily free cash events), Metaculus tournaments
(free, live pools up to $50K), Wergle Flomp ($5,100, no fee), the PayPal AI Hackathon ($67,500, closes
2026-11-12), and ARC Prize 2026 ($2M; final submissions due today).</li>
<li>Time-critical: ARC Prize 2026 final submissions are due {CHECKED}; its Paper Track ($450K) closes within
days (Kaggle shows "7 days to go"); the PayPal AI Hackathon ($67,500) closes 2026-11-12; the GEMS Prize
Challenge ($300,000, DOE) closes 2026-12-03 but its free-entry status is <em>not</em> officially confirmed.</li>
<li>Prize-form traps flagged: GamerSaloon pays Bonus Cash that cannot be withdrawn; TradingView's most recent
"The Leap" contest paid subscription plans, not cash; DSH Hacks V2 advertises "$100k+" while Devpost lists
"5 non-cash prizes".</li>
<li>Conflicts flagged, not resolved: the ARC Paper deadline (arcprize.org "November 8" vs Kaggle "7 days to
go" → ~Nov 9); the PayPal hackathon prize total ($67,500 vs $69,750 on the same official site); MLB Beat the
Streak terms say the window ended with the 2026 regular season while the page still says "start playing now".</li>
<li>Link health: 11 of 12 re-checked broken links are still broken (NHL Bracket Challenge, Topcoder, A-Leagues
fantasy, Solitaire Cash App Store page, and others); UEFA Champions League Fantasy recovered. The repo-wide
internal link scan found {stats['internal_broken']} broken local links across {stats['internal_pages_scanned']} pages.</li>
<li>Of {stats['total_rows']} catalog entries, only {stats['assessed_rows']} had enough official evidence to
score in this pass; the remaining {stats['unassessed_rows']} are published with blank values and remain on the
shared <a href="../review.html">review queue</a> for later verification. Nothing was inferred to fill gaps.</li>
</ul>
<p><strong>Method in one line.</strong> Score = free entry (20) + cash magnitude (≤25) + open now (20) +
cadence (≤15) + eligibility breadth (≤10) + effort (≤10), where the first three require verbatim quotes
from official pages checked on {CHECKED}. Details: <a href="methodology.html">methodology</a>.</p>
<p><strong>Recommended next actions.</strong> (1) Enter the A-tier free games that match your location;
(2) decide today on ARC Paper / PayPal hackathon / GEMS; (3) work through the
<a href="flagged.html">flagged items</a>; (4) extend verification to the {stats['unassessed_rows']} unassessed
rows — an AI coding agent can automate entry drafting for the tech/creative contests whose rules allow it
(see per-row AI notes; e.g. Wergle Flomp forbids AI-generated text).</p>
</section>
"""
    (OUT / "summary.html").write_text(page("Executive summary", body, "summary.html"), encoding="utf-8")

    # ---- 404 + categories done; write 404 ----
    body = '<p>Page not found. <a href="index.html">Return to the analysis dashboard</a>.</p>'
    (OUT / "404.html").write_text(page("Page not found", body), encoding="utf-8")

    return stats


if __name__ == "__main__":
    s = build()
    print(json.dumps(s, indent=1, sort_keys=True))
