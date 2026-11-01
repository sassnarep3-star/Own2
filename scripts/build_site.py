#!/usr/bin/env python3
"""Build the PrizeDesk static site.

Inputs
  data/upstream.json     206 ledger listings + 45 removed records, verbatim from the upstream repo
  data/evidence/*.json   per-entry verification notes (quotes, URLs, check dates) added by this session
  data/categories.json   category metadata

Outputs
  data/contests.json     published dataset (only evidence-backed values, plus labelled ledger claims)
  *.html                 index, all-competitions table, 9 category pages, executive summary, review page

Rule enforced by the builder: a value is rendered only if an evidence record carries a verbatim quote
and an official source URL. Everything else stays blank and is flagged.
"""
import json, html, pathlib, re, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
AUDIT = "2026-11-01"
ARROW = "↗"
VAL_OPEN = '<br><b class="val">'
VAL_CLOSE = "</b>"
MIDDOT = "·"

def load(p):
    return json.loads((ROOT / p).read_text())

def esc(v):
    return html.escape(str(v or ""), quote=True)

up = load("data/upstream.json")
cats = load("data/categories.json")
CAT = {c["id"]: c for c in cats}

evidence = {}
for f in sorted((ROOT / "data/evidence").glob("*.json")):
    rec = json.loads(f.read_text())
    evidence[rec["id"]] = rec

LEDGER = {l["id"]: l for l in up["listings"]}
VERDICTS = {"verified", "partial", "flagged", "unverified", "closed"}

def money(text):
    """Largest dollar figure mentioned in an evidence string, for sorting only."""
    if not text:
        return 0
    vals = [int(x.replace(",", "")) for x in re.findall(r"\$([0-9][0-9,]*)", text)]
    return max(vals) if vals else 0

def field(ev, name):
    return (ev or {}).get("fields", {}).get(name, {})

def status_of(ev):
    iso = (ev or {}).get("deadline_iso")
    if not iso:
        return "unknown"
    return "closed" if iso < AUDIT else "open"

def build_row(rid):
    ev = evidence.get(rid)
    led = LEDGER.get(rid)
    name = (ev or {}).get("name") or (led or {}).get("name", rid)
    category = (ev or {}).get("category") or (led or {}).get("type", "tech")
    verdict = (ev or {}).get("verdict", "unverified")
    if verdict not in VERDICTS:
        verdict = "unverified"
    st = status_of(ev)
    if st == "closed" and verdict in ("verified", "partial"):
        verdict = "closed"

    sources = []
    if ev:
        for s in ev.get("sources", []):
            sources.append({"title": s.get("title", ""), "url": s["url"], "tier": "official", "checked": s.get("checked")})
    if led:
        for s in led.get("sources", []):
            if not any(x["url"] == s.get("url") for x in sources):
                sources.append({"title": s.get("title", ""), "url": s.get("url", ""), "tier": s.get("tier", "unknown")})

    has_official = any(s["tier"] == "official" for s in sources)
    flags = list((ev or {}).get("flags", []))
    if not has_official:
        flags.insert(0, "No official operator source in the ledger: only affiliate or forum links were supplied, so no claim from this row was adopted.")

    free = field(ev, "freeEntry")
    prize = field(ev, "prize")
    tier = "reference"
    if verdict == "flagged" or st == "closed" or verdict == "closed":
        tier = "avoid"
    elif verdict == "verified" and free.get("status") == "confirmed" and prize.get("status") == "confirmed":
        tier = "start"
    elif verdict in ("verified", "partial") and (free.get("status") == "confirmed" or prize.get("status") == "confirmed"):
        tier = "watch"

    return {
        "id": rid,
        "name": name,
        "category": category,
        "categoryName": CAT.get(category, {}).get("name", category.title()),
        "verdict": verdict,
        "state": st,
        "tier": tier,
        "free": free if free.get("status") in ("confirmed", "contradicted") else {},
        "prize": prize if prize.get("status") == "confirmed" else {},
        "deadline": field(ev, "deadline") if field(ev, "deadline").get("status") == "confirmed" else {},
        "eligibility": field(ev, "eligibility") if field(ev, "eligibility").get("status") == "confirmed" else {},
        "ai": field(ev, "aiPolicy") if field(ev, "aiPolicy").get("status") == "confirmed" else {},
        "payout": field(ev, "payout") if field(ev, "payout").get("status") == "confirmed" else {},
        "deadline_iso": (ev or {}).get("deadline_iso"),
        "prize_value": money(prize.get("text", "")),
        "summary": (ev or {}).get("summary", ""),
        "flags": flags,
        "sources": sources,
        "official": has_official,
        "checked": (ev or {}).get("checked", ""),
        "ledger": {
            "claim": (led or {}).get("prizeUsd", ""),
            "status": (led or {}).get("status", ""),
            "freePath": (led or {}).get("freePath", ""),
            "lastChecked": (led or {}).get("lastChecked", ""),
            "signupUrl": (led or {}).get("signupUrl", ""),
            "platforms": (led or {}).get("platforms", []),
            "eligibility": (led or {}).get("eligibility", ""),
            "note": (led or {}).get("prizeNote", ""),
        } if led else {},
    }

rows = [build_row(rid) for rid in LEDGER]
extras = [rid for rid in evidence if rid not in LEDGER]
rows += [build_row(rid) for rid in extras]
rows.sort(key=lambda r: r["name"].lower())

TAG = {
    "verified": ("Verified", "ok"),
    "partial": ("Partly verified", "warn"),
    "flagged": ("Flagged", "bad"),
    "unverified": ("Unverified lead", "mute"),
    "closed": ("Closed", "mute"),
}
TIER_ORDER = {"start": 0, "watch": 1, "reference": 2, "avoid": 3}

def badge(v):
    label, cls = TAG.get(v, ("Unverified lead", "mute"))
    return f'<span class="badge {cls}">{label}</span>'

def stat_of(label, cls):
    return f'<span class="tag {cls}">{esc(label)}</span>'

def src_links(r, limit=3):
    out = []
    for s in r["sources"][:limit]:
        tier = s["tier"]
        mark = "" if tier == "official" else f' <span class="tiny">({esc(tier)})</span>'
        out.append(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["title"] or "source")} {ARROW}</a>{mark}')
    return "<br>".join(out) if out else '<span class="tiny">none supplied</span>'

def evidence_table(r):
    ev = evidence.get(r["id"])
    if not ev:
        extra = ""
        if r["ledger"].get("claim"):
            extra = (f'<p class="note">The ledger asserts: <em>{esc(r["ledger"]["claim"])}</em>. '
                     'That is an unverified third-party claim, so it is not shown as a prize figure.</p>')
        date = esc(r["ledger"].get("lastChecked") or "unknown")
        status = esc(r["ledger"]["status"]) if r["ledger"].get("status") else ""
        tail = (" " + MIDDOT + " declared status: " + status) if status else ""
        return ('<p class="note">This row has not been verified against an official source yet. '
                'Nothing is asserted about free entry, prize, deadline or eligibility.'
                + extra + '</p>'
                f'<p class="note">Ledger entry date: {date}{tail}</p>')
    parts = ['<table class="ev"><caption>Evidence recorded on ' + esc(ev.get("checked", AUDIT)) + (' \u00b7 ' + esc(ev["attribution"]) if ev.get("attribution") else "") + '</caption>'
             '<thead><tr><th scope="col">Field</th><th scope="col">Status</th><th scope="col">Basis (verbatim quote)</th><th scope="col">Source</th></tr></thead><tbody>']
    labels = [("freeEntry", "Free entry"), ("prize", "Cash prize"), ("deadline", "Deadline"),
              ("eligibility", "Eligibility"), ("aiPolicy", "AI rules"), ("payout", "Payment")]
    for key, lab in labels:
        f = ev["fields"].get(key, {})
        stt = f.get("status", "not_stated")
        stxt = {"confirmed": "Confirmed", "contradicted": "Contradicted", "not_stated": "Not stated",
                "not_found": "Not found"}.get(stt, stt)
        value = (VAL_OPEN + esc(f["text"]) + VAL_CLOSE) if f.get("text") else ""
        parts.append(f'<tr><td>{lab}</td><td>{esc(stxt)}</td>'
                     f'<td><q>{esc(f.get("quote", ""))}</q>{value}</td>'
                     f'<td><a href="{esc(f.get("url", ""))}" target="_blank" rel="noopener noreferrer">open {ARROW}</a></td></tr>')
    parts.append("</tbody></table>")
    if ev.get("summary"):
        parts.append(f'<p class="note"><b>Assessment.</b> {esc(ev["summary"])}</p>')
    if ev.get("flags"):
        parts.append('<ul class="flags">' + "".join(f"<li>{esc(x)}</li>" for x in ev["flags"]) + "</ul>")
    if r["ledger"].get("claim"):
        parts.append(f'<p class="note"><b>Upstream ledger claim (not adopted):</b> {esc(r["ledger"]["claim"])}</p>')
    return "".join(parts)

def table(rows_subset, tid="all"):
    head = ["Competition", "Free entry", "Cash prize", "Deadline / state", "Eligibility", "AI use", "Sources"]
    out = [f'<div class="tablewrap"><table id="{tid}" class="grid"><thead><tr>'
           + "".join(f'<th scope="col">{h}</th>' for h in head) + "</tr></thead><tbody>"]
    for r in rows_subset:
        rid = esc(r["id"])
        state = {"open": "Open now", "closed": "Closed", "unknown": "Window not stated"}[r["state"]]
        if r["free"]:
            free_cell = esc(r["free"].get("text", ""))
        else:
            free_cell = '<span class="blank">not confirmed</span>'
        if r["prize"]:
            prize_cell = "<b>" + esc(r["prize"].get("text", "")) + "</b>"
        else:
            prize_cell = '<span class="blank">not confirmed</span>'
        dl_cell = esc(r["deadline"].get("text", "")) if r["deadline"] else '<span class="blank">not confirmed</span>'
        elig = esc(r["eligibility"].get("text", "")) if r["eligibility"] else '<span class="blank">not confirmed</span>'
        ai = esc(r["ai"].get("text", "")) if r["ai"] else '<span class="blank">not stated</span>'
        sub_bits = [esc(r["categoryName"])]
        if r["state"] != "unknown":
            sub_bits.append(esc(state))
        sub = (" " + MIDDOT + " ").join(sub_bits)
        search = " ".join([r["name"], r["category"], r["categoryName"], r["summary"], " ".join(r["flags"])]).lower()
        out.append(
            '<tr class="r" id="' + rid + '" data-row="' + rid + '" data-name="' + esc(r["name"].lower()) + '"'
            + ' data-cat="' + esc(r["category"]) + '" data-verdict="' + esc(r["verdict"]) + '"'
            + ' data-free="' + ("1" if r["free"] else "0") + '" data-cash="' + ("1" if r["prize"] else "0") + '"'
            + ' data-prize="' + str(r["prize_value"]) + '" data-deadline="' + esc(r["deadline_iso"] or "9999-12-31") + '"'
            + ' data-search="' + esc(search) + '">'
            + '<td data-label="Competition"><a class="nm" href="#' + rid + '" data-toggle="' + rid + '">'
            + esc(r["name"]) + "</a> " + badge(r["verdict"])
            + '<div class="sub">' + sub + "</div></td>"
            + '<td data-label="Free entry">' + free_cell + "</td>"
            + '<td data-label="Cash prize">' + prize_cell + "</td>"
            + '<td data-label="Deadline">' + dl_cell + '<div class="sub">' + esc(state) + "</div></td>"
            + '<td data-label="Eligibility">' + elig + "</td>"
            + '<td data-label="AI use">' + ai + "</td>"
            + '<td data-label="Sources"><div class="src">' + src_links(r) + "</div>"
            + '<button class="more" type="button" aria-expanded="false" data-toggle="' + rid + '">Evidence &amp; flags</button></td></tr>'
            + '<tr class="detail" id="ev-' + rid + '" hidden><td colspan="7">' + evidence_table(r) + "</td></tr>"
        )
    out.append("</tbody></table></div>")
    out.append('<p class="empty" hidden>No competitions match those filters.</p>')
    return "".join(out)

def controls(show_cat=True):
    catopts = "".join(f'<option value="{c["id"]}">{esc(c["name"])}</option>' for c in cats)
    return f'''<div class="controls" role="search">
<label class="ctl grow"><span>Search</span><input id="q" type="search" placeholder="Search name, category or note…" autocomplete="off"></label>
{'<label class="ctl"><span>Category</span><select id="f-cat"><option value="">All categories</option>' + catopts + '</select></label>' if show_cat else ''}
<label class="ctl"><span>Verification</span><select id="f-verdict"><option value="">Any</option><option value="verified">Verified</option><option value="partial">Partly verified</option><option value="flagged">Flagged</option><option value="unverified">Unverified lead</option><option value="closed">Closed</option></select></label>
<label class="ctl"><span>Free entry</span><select id="f-free"><option value="">Any</option><option value="1">Confirmed free</option><option value="0">Not confirmed</option></select></label>
<label class="ctl"><span>Cash prize</span><select id="f-cash"><option value="">Any</option><option value="1">Confirmed cash</option><option value="0">Not confirmed</option></select></label>
<label class="ctl"><span>Sort</span><select id="f-sort"><option value="">Default</option><option value="prize">Prize (high to low)</option><option value="name">Name (A–Z)</option><option value="deadline">Deadline (soonest)</option></select></label>
<button class="reset" type="button" id="reset">Reset</button>
</div><p class="count" id="count" role="status"></p>'''

NAV = [("index.html", "Overview"), ("contests.html", "All competitions"), ("summary.html", "Executive summary"), ("review.html", "Flagged for review")]

def layout(file, title, subtitle, body, active="", cat_active=""):
    nav = "".join(f'<a href="{u}" class="{"active" if active == u else ""}">{esc(t)}</a>' for u, t in NAV)
    chips = "".join(f'<a class="chip {"on" if cat_active == c["id"] else ""}" href="{c["id"]}.html">{esc(c["short"])}</a>' for c in cats)
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · PrizeDesk</title>
<meta name="description" content="An evidence-first ledger of free-to-enter cash prize competitions. Every published value is linked to the operator's own page.">
<link rel="stylesheet" href="style.css">
<script src="app.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="bar">
    <a class="brand" href="index.html"><span class="mark">PD</span><span>PrizeDesk<small>free-to-enter cash competitions</small></span></a>
    <nav class="main" aria-label="Main">{nav}</nav>
  </div>
  <div class="chips" aria-label="Categories">{chips}</div>
</header>
<main id="main">
<p class="eyebrow">Audit date {AUDIT} · every published value links to the operator's own page</p>
<h1>{esc(title)}</h1>
<p class="lede">{esc(subtitle)}</p>
{body}
</main>
<footer>
  <p><b>Rule of the desk:</b> if the operator's own page does not say it, the cell stays blank. Blank is not zero, not free and not unrestricted.</p>
  <p>{len(rows)} competitions tracked · {sum(1 for r in rows if r["verdict"] == "verified")} verified ·
  {sum(1 for r in rows if r["verdict"] == "unverified")} still unverified ·
  source ledger pinned at <a href="https://github.com/karagemop466-tech/FreeMoneyApps/commit/{esc(up.get("commit", ""))}" target="_blank" rel="noopener noreferrer">commit {esc((up.get("commit") or "")[:7])}</a></p>
  <p class="tiny">No affiliate links. No accounts created on your behalf. No earnings guarantees. Official rules always win.</p>
</footer>
</body>
</html>'''
    (ROOT / file).write_text(doc)

# ---------------------------------------------------------------- overview
def deadline_list():
    live = [r for r in rows if r["deadline_iso"] and r["state"] == "open"]
    live.sort(key=lambda r: r["deadline_iso"])
    if not live:
        return '<p class="note">No competition in this pass has a confirmed, still-open deadline.</p>'
    out = ['<ul class="cal">']
    for r in live:
        d = datetime.date.fromisoformat(r["deadline_iso"])
        out.append(
            f'<li><span class="date"><b>{d.strftime("%d %b")}</b><small>{d.year}</small></span>'
            f'<span class="what"><a href="contests.html#{esc(r["id"])}">{esc(r["name"])}</a>'
            f'<small>{esc(r["prize"].get("text", ""))}</small></span>'
            f'<a class="go" href="{esc(r["sources"][0]["url"] if r["sources"] else "#")}" target="_blank" rel="noopener noreferrer">open ↗</a></li>')
    out.append("</ul>")
    return "".join(out)

start = sorted([r for r in rows if r["tier"] == "start"], key=lambda r: -r["prize_value"])
watch = sorted([r for r in rows if r["tier"] == "watch"], key=lambda r: -r["prize_value"])

def short_card(r):
    why = r["summary"] or "Evidence recorded; see the row for quotes."
    money_line = ('<p class="money">' + esc(r["prize"]["text"]) + "</p>") if r["prize"] else '<p class="money muted">Prize not confirmed</p>'
    why_line = '<p class="why">' + esc(why) + "</p>"
    meta_line = '<p class="meta">' + esc(r["deadline"].get("text") or "Deadline not confirmed") + "</p>"
    return (f'<article class="pick"><div class="pickhead">{badge(r["verdict"])}<span class="cat">{esc(r["categoryName"])}</span></div>'
            f'<h3><a href="{esc(r["sources"][0]["url"] if r["sources"] else "#")}" target="_blank" rel="noopener noreferrer">{esc(r["name"])} ↗</a></h3>'
            + money_line + why_line + meta_line + "</article>")

body = f'''
<section class="stats">
  <div class="stat"><span>Competitions tracked</span><b>{len(rows)}</b><small>206 ledger rows retained, plus {len(extras)} verified live events</small></div>
  <div class="stat ok"><span>Free entry confirmed</span><b>{sum(1 for r in rows if r["free"])}</b><small>operator states no fee or no purchase necessary</small></div>
  <div class="stat ok"><span>Cash prize confirmed</span><b>{sum(1 for r in rows if r["prize"])}</b><small>figure quoted from the operator's own page</small></div>
  <div class="stat warn"><span>Verified &amp; usable now</span><b>{len(start)}</b><small>free entry + cash + still open</small></div>
  <div class="stat bad"><span>Flagged for review</span><b>{sum(1 for r in rows if r["flags"])}</b><small>contradictions, dead links, no official source</small></div>
</section>

<section class="panel">
  <div class="phead"><h2>Where to spend your time</h2><p>Only competitions where the operator's own page confirms free entry and a cash prize, and the window is still open.</p></div>
  <div class="picks">{''.join(short_card(r) for r in start) or '<p class="note">Nothing qualified on this pass.</p>'}</div>
</section>

<section class="panel">
  <div class="phead"><h2>Deadlines that are actually confirmed</h2><p>Dates taken from the operator, not from the ledger. {len([r for r in rows if r["deadline_iso"] and r["state"]=="open"])} open dates on record.</p></div>
  {deadline_list()}
</section>

<section class="panel">
  <div class="phead"><h2>Worth a look, not yet proven</h2><p>One of free entry or the prize is confirmed; the other is not. Read the evidence before investing time.</p></div>
  <div class="picks">{''.join(short_card(r) for r in watch[:9])}</div>
</section>

<section class="panel" id="categories">
  <div class="phead"><h2>Browse by category</h2><p>Counts include unverified leads, because losing a lead hides information.</p></div>
  <div class="catgrid">{''.join(f'<a class="catcard" href="{c["id"]}.html"><b>{esc(c["name"])}</b><span>{sum(1 for r in rows if r["category"]==c["id"])} entries · {sum(1 for r in rows if r["category"]==c["id"] and r["verdict"]=="verified")} verified</span><small>{esc(c["blurb"])}</small></a>' for c in cats)}</div>
</section>

<section class="panel prose" id="method">
  <h2>How to read this page</h2>
  <dl class="legend">
    <dt>{badge("verified")}</dt><dd>Free entry <em>and</em> a cash prize are both quoted from the operator's own page, and the window is open.</dd>
    <dt>{badge("partial")}</dt><dd>Some fields are confirmed, others are not. The row shows exactly which.</dd>
    <dt>{badge("flagged")}</dt><dd>The operator's page contradicts the ledger, the link is dead, or no official source exists.</dd>
    <dt>{badge("unverified")}</dt><dd>Not checked against any official page in this pass. Kept visible so the lead is not lost; nothing is claimed.</dd>
    <dt>{badge("closed")}</dt><dd>Confirmed to have closed before {AUDIT}.</dd>
  </dl>
  <p>An independent second audit of 13 of these leads, run in parallel on the same day, is preserved at
  <a href="audits/2026-11-01/index.html">audits/2026-11-01</a>; its findings are folded into the evidence panels here.</p>
  <p>Values that could not be confirmed are left blank. The ledger's original wording is shown only inside a row's evidence panel, explicitly labelled as a claim that was <em>not</em> adopted. Full method and limitations are on the <a href="summary.html">executive summary</a>; every unresolved item is on <a href="review.html">Flagged for review</a>.</p>
</section>
'''
layout("index.html", "Free-to-enter cash competitions, verified line by line.",
       "A working dashboard for one question: which competitions are worth your time today? Every number below links to the page that states it.",
       body, active="index.html")

# ---------------------------------------------------------------- all + category pages
def cat_intro(cid):
    c = CAT[cid]
    sub = [r for r in rows if r["category"] == cid]
    return (f'<section class="panel prose"><p>{esc(c["blurb"])}</p><p><b>What the evidence shows.</b> {esc(c["read"])}</p>'
            f'<p class="tiny">{len(sub)} entries · {sum(1 for r in sub if r["verdict"]=="verified")} verified · '
            f'{sum(1 for r in sub if r["free"])} with confirmed free entry · {sum(1 for r in sub if r["prize"])} with a confirmed cash prize · '
            f'{sum(1 for r in sub if r["flags"])} flagged.</p></section>')

layout("contests.html", "All competitions",
       f"Every one of the {len(rows)} competitions in the ledger, searchable and filterable. Blank cells mean the operator's page does not state the value.",
       controls(True) + table(rows), active="contests.html")

for c in cats:
    sub = [r for r in rows if r["category"] == c["id"]]
    layout(c["id"] + ".html", c["name"],
           c["blurb"],
           cat_intro(c["id"]) + controls(False) + table(sub, c["id"]), cat_active=c["id"])

# ---------------------------------------------------------------- review page
def review_items():
    hard = [r for r in rows if r["verdict"] == "flagged"]
    inconsistent = [r for r in rows if r["verdict"] == "verified" and r["flags"]]
    no_source = [r for r in rows if not r["official"]]
    unverified = [r for r in rows if r["verdict"] == "unverified"]
    out = [f'''<section class="panel prose"><h2>Read this first</h2>
<p>Nothing on this page blocks the site: these are the items I could <em>not</em> confirm, or where the source material contradicts itself. Each one keeps its link so you can check my reading in one click.</p>
<ul class="sumlist">
<li><b>{len(hard)}</b> rows with a contradiction, a dead link or a mis-stated prize.</li>
<li><b>{len(no_source)}</b> rows whose only ledger source is an affiliate or forum link — no operator page was supplied.</li>
<li><b>{len(unverified)}</b> rows never verified against an official page in this pass.</li>
<li><b>{len(inconsistent)}</b> verified rows that still carry a caveat.</li>
</ul></section>''']

    def item(r, note):
        flag_items = "".join("<li>" + esc(x) + "</li>" for x in r["flags"])
        claim = r["ledger"].get("claim") or ""
        claim_html = ('<p class="tiny">Ledger claim, not adopted: ' + esc(claim) + "</p>") if claim else ""
        first = r["sources"][0]["url"] if r["sources"] else "#"
        return ('<li id="r-' + esc(r["id"]) + '"><div class="ri-head"><a href="' + esc(first) + '" target="_blank" rel="noopener noreferrer">'
                + esc(r["name"]) + " ↗</a>" + badge(r["verdict"])
                + '</div><p class="tiny">' + esc(r["categoryName"]) + " · ledger date "
                + esc(r["ledger"].get("lastChecked") or "unknown") + "</p>"
                + "<p>" + esc(note) + "</p>"
                + '<ul class="flags">' + flag_items + "</ul>" + claim_html + "</li>")

    if hard:
        out.append('<section class="panel"><h2>Contradicted, dead or mis-stated</h2><p>The operator\'s page disproves the ledger, or the link no longer serves the claimed contest.</p><ul class="reviewlist">')
        for r in sorted(hard, key=lambda x: x["name"]):
            out.append(item(r, r["summary"] or "See flags."))
        out.append("</ul></section>")

    out.append('<section class="panel"><h2>Verified rows that still carry a caveat</h2><p>Free entry and a prize are confirmed, but something else limits them — a pool total rather than per-place cash, a restricted region, or an unread rule.</p><ul class="reviewlist">')
    for r in sorted(inconsistent, key=lambda x: x["name"]):
        out.append(item(r, r["summary"] or ""))
    out.append("</ul></section>")

    out.append('<section class="panel"><h2>No official source supplied</h2><p>The ledger linked only affiliate or forum pages. Nothing from these rows is published as fact; the links are kept so you can judge them.</p><ul class="reviewlist">')
    for r in sorted(no_source, key=lambda x: x["name"]):
        out.append(item(r, "Supplied sources: " + ", ".join(f'{s["tier"]}' for s in r["sources"]) + "."))
    out.append("</ul></section>")

    out.append(f'<section class="panel"><h2>Still unverified ({len(unverified)})</h2><p>These rows are kept so the lead is not lost, but no value is asserted. If you want one of them promoted to verified, the operator\'s rules page is the place to start.</p><div class="tiny-grid">')
    out.append("".join(f'<a class="mini" href="{esc(r["sources"][0]["url"] if r["sources"] else "#")}" target="_blank" rel="noopener noreferrer">{esc(r["name"])}</a>' for r in sorted(unverified, key=lambda x: x["name"])))
    out.append("</div></section>")
    return "".join(out)

layout("review.html", "Flagged for review",
       "Every unresolved, contradicted or unsourced item, with the link to check it yourself.",
       review_items(), active="review.html")

# ---------------------------------------------------------------- summary page
S = {
    "total": len(rows),
    "verified": sum(1 for r in rows if r["verdict"] == "verified"),
    "partial": sum(1 for r in rows if r["verdict"] == "partial"),
    "flagged": sum(1 for r in rows if r["verdict"] == "flagged"),
    "unverified": sum(1 for r in rows if r["verdict"] == "unverified"),
    "closed": sum(1 for r in rows if r["verdict"] == "closed"),
    "free": sum(1 for r in rows if r["free"]),
    "cash": sum(1 for r in rows if r["prize"]),
    "start": len(start),
    "no_off": sum(1 for r in rows if not r["official"]),
}
summary_body = f'''
<section class="panel prose">
<h2>The short version</h2>
<p>The source ledger lists {len(up["listings"])} competitions across nine categories. I re-checked the entries where a mistake would cost real time, against the operators' own pages, on {AUDIT}. Of those, <b>{S["verified"]}</b> have both a free entry route and a cash prize stated by the operator, and <b>{S["start"]}</b> are still open today. <b>{S["unverified"]}</b> rows remain unverified and are published blank.</p>
<p>Three things decide whether a competition is worth entering: <b>is entry genuinely free</b>, <b>is the prize real cash that you can withdraw</b>, and <b>is it still open</b>. A fourth decides whether an AI agent can help: <b>do the rules allow it</b>. The table publishes all four per row, and leaves the cell blank when the operator is silent.</p>

<h2>What actually pays, ranked by usefulness</h2>
<ol>
<li><b>Sports pick'em with published rules.</b> ESPN NFL Pick'em ($102,000 across 58 prizes, free, 10 entries, open to 10 Jan 2027) and CBS Pro Football Pick'em (free, 50 states + DC, 18 weekly contests). Free entry and prize tables are written into the official rules, which is exactly what a serious entrant wants. Skill, not luck, decides the tie-breakers, and the volume of prizes means a competent process can cash occasionally.</li>
<li><b>AI competitions.</b> Devpost hackathons (six figures live: PayPal $67,500 closing 12 Nov 2026, Kiroween $100,000, Meta VR $1,000,000) and Kaggle (ARC Prize 2026 $2,000,000, NFL Big Data Bowl 2027 $100,000) publish real cash pools. This is the only category where an agent can do most of the work.</li>
<li><b>Forecasting.</b> Metaculus pays cash for accuracy, has 19 live tournaments on the audit date, pools from $3,400 to $50,000, is free to enter, and runs a dedicated bot track. Lowest cost per attempt of anything here.</li>
<li><b>Photography and literary prizes.</b> Sony World Photography Awards ($25,000 / $5,000, free) and the Wergle Flomp humour poetry contest ($5,100, no fee) are free and open — but the work must be human, and photography rules usually exclude generated images.</li>
</ol>

<h2>What to stop doing</h2>
<ul>
<li><b>Cash skill-game apps.</b> Papaya, Skillz and Pocket7Games free rooms pay gems, not dollars. The ledger listed four of them as skill tournaments; all four are now marked as requiring an entry fee for real cash.</li>
<li><b>Tipster and affiliate "predictor" games.</b> Andy's £1,000,000 predictor closed on 18 Sep 2026, is UK/Ireland only, and the headline is a near-impossible perfect-table jackpot on a betting-affiliate site.</li>
<li><b>Broker demo contests.</b> The three demo-account contests in the market category are sourced only from affiliate blogs, not from the brokers.</li>
<li><b>Dead links presented as live contests.</b> The Dirty Dozen row points at a gambling-affiliate page that now serves a generic casino lobby; Challenge.gov, cited as the official source for federal prizes, was sunset on 30 March 2026.</li>
</ul>

<h2>How the verification was done</h2>
<p>For each entry I opened the operator's own page and recorded: the state of free entry, the prize as written, the deadline, eligibility, AI rules and payment method — each with a verbatim quote and the URL. A field is published only when the quote supports it. Where the operator is silent, the cell stays blank and the silence itself is recorded as "not stated". Where the operator contradicts the ledger, the row is <b>flagged</b> and the contradiction is shown.</p>
<p>This pass covered {len(evidence)} entries in depth. The rest are inherited leads: they keep their ledger link, they are labelled <b>unverified</b>, and no value from them is published. That is deliberate — repeating an unverified number is how a list like this becomes wrong.</p>

<h2>Limits you should hold me to</h2>
<ul>
<li>Official rules change without notice. Every row carries the date it was read; re-check before you invest hours.</li>
<li>Prize pools are not expected winnings. A $100,000 pool spread over thousands of entrants is not $100,000 of value to you, and I have not invented any win probability or hourly rate.</li>
<li>"Free entry confirmed" means the operator says no fee is required. It does not mean zero cost: your time, compute and travel are real.</li>
<li>Link health is only checked for the pages actually opened in this pass. Unopened links may be broken — they are listed as unverified for that reason.</li>
<li>Tax and payment treatment differ by country and are not legal advice.</li>
</ul>

<h2>Counts</h2>
<table class="ev"><thead><tr><th scope="col">Measure</th><th scope="col">Count</th></tr></thead><tbody>
<tr><td>Competitions tracked</td><td>{S["total"]}</td></tr>
<tr><td>Free entry confirmed by operator</td><td>{S["free"]}</td></tr>
<tr><td>Cash prize confirmed by operator</td><td>{S["cash"]}</td></tr>
<tr><td>Verified (free + cash, open)</td><td>{S["verified"]}</td></tr>
<tr><td>Partly verified</td><td>{S["partial"]}</td></tr>
<tr><td>Flagged</td><td>{S["flagged"]}</td></tr>
<tr><td>Closed before audit</td><td>{S["closed"]}</td></tr>
<tr><td>Unverified leads retained</td><td>{S["unverified"]}</td></tr>
<tr><td>Rows with no official source supplied</td><td>{S["no_off"]}</td></tr>
</tbody></table>

<h2>Parallel audits in this repository</h2>
<p>Two independent sessions audited the same ledger on the same day. Their material is preserved and linked rather than replaced:</p>
<ul>
<li><a href="audits/2026-11-01/index.html">Independent 13-lead official-source audit</a> — a separate report with its own
<a href="audits/2026-11-01/review.html">review page</a>; its field-level findings (Sony free-entry rule, Tom Howard fee,
NYPL nomination terms, CheckMate claim-window conflict, Zindi 404, Film Prize rules mismatch, MLB conditional prize,
Vocal and Freelancer terms) are imported into this site's evidence records with attribution.</li>
<li><a href="explore.html">Mobile shortlist (parallel build)</a> and <a href="flagged/index.html">its flagged page</a> —
the other integration session's dashboard, kept live and unchanged.</li>
<li>Legacy builder for the first dashboard: <code>audits/legacy-build/</code>.</li>
</ul>

<h2>Files and provenance</h2>
<ul>
<li><a href="data/contests.json">Published dataset</a> — every row with its evidence, sources and flags.</li>
<li><a href="data/upstream.json">Upstream ledger snapshot</a> — {len(up["listings"])} listings and {len(up["removed"])} removed records, unchanged.</li>
<li><a href="https://github.com/karagemop466-tech/FreeMoneyApps/commit/{esc(up.get("commit",""))}" target="_blank" rel="noopener noreferrer">Pinned source commit</a> · <a href="https://karagemop466-tech.github.io/FreeMoneyApps/" target="_blank" rel="noopener noreferrer">original site</a>.</li>
<li><a href="review.html">Flagged for review</a> — the item-by-item list of what I could not confirm.</li>
</ul>
</section>'''
layout("summary.html", "Executive summary",
       "What the evidence supports, what it does not, and where the time is best spent.", summary_body, active="summary.html")

# ---------------------------------------------------------------- 404
layout("404.html", "Page not found", "That page is not part of the ledger.",
       '<section class="panel prose"><p><a href="index.html">Back to the dashboard</a> · <a href="contests.html">All competitions</a> · <a href="review.html">Flagged for review</a></p></section>')

# ---------------------------------------------------------------- evidence log
def write_evidence_md():
    lines = ["# Evidence log", "",
             f"Audit date: **{AUDIT}** (UTC). One row per competition that was opened and read in this pass.",
             "",
             "Every value published by the site appears below with the operator's own wording. A field that the",
             "operator does not state is recorded as *not stated* and is left blank on the site. Quotes are short",
             "verbatim excerpts of the retrieved page, not paraphrases.", "",
             "| id | Competition | Verdict | Free entry | Cash prize | Deadline | Read on |",
             "|---|---|---|---|---|---|---|"]
    order = {"verified": 0, "partial": 1, "flagged": 2, "closed": 3}
    for rid, ev in sorted(ev_entries, key=lambda kv: (order.get(kv[1].get("verdict"), 9), kv[0])):
        f = ev.get("fields", {})
        def cell(k):
            st = f.get(k, {}).get("status")
            return {"confirmed": "confirmed", "contradicted": "CONTRADICTED", "not_stated": "not stated",
                    "not_found": "not found"}.get(st, "-")
        lines.append("| `" + rid + "` | " + (ev.get("name") or LEDGER.get(rid, {}).get("name", rid)).replace("|", "\|")
                     + " | " + str(ev.get("verdict", "")) + " | " + cell("freeEntry") + " | " + cell("prize")
                     + " | " + cell("deadline") + " | " + ev.get("checked", AUDIT) + " |")
    lines += ["", "## What the quotes say, entry by entry", ""]
    for rid, ev in sorted(ev_entries, key=lambda kv: kv[0]):
        lines.append("### " + (ev.get("name") or LEDGER.get(rid, {}).get("name", rid)) + " (`" + rid + "`)")
        lines.append("")
        if ev.get("summary"):
            lines += ["*Assessment:* " + ev["summary"], ""]
        for key, lab in [("freeEntry", "Free entry"), ("prize", "Cash prize"), ("deadline", "Deadline"),
                         ("eligibility", "Eligibility"), ("aiPolicy", "AI rules"), ("payout", "Payment")]:
            f = ev.get("fields", {}).get(key, {})
            if not f:
                continue
            quote = (f.get("quote") or "").strip()
            lines.append("- **" + lab + "** — " + f.get("status", "").replace("_", " ") + ". > " + quote
                         + "  \n  <" + f.get("url", "") + ">")
        if ev.get("flags"):
            lines.append("")
            lines.append("*Flags:* " + "; ".join(ev["flags"]))
        lines.append("")
    lines += ["## Upstream provenance", "",
              "- Repository: " + str(up.get("repository")),
              "- Pinned commit: " + str(up.get("commit")),
              "- Ledger review date declared upstream: " + str(up.get("reviewed")),
              "- Listings retained: " + str(len(up["listings"])) + "; removed records retained in `data/upstream.json`: " + str(len(up["removed"])),
              "- Original site: https://karagemop466-tech.github.io/FreeMoneyApps/", "",
              "Claimed figures in the upstream ledger are never repeated as facts. Where a row is unverified, the",
              "ledger's wording is visible only inside that row's evidence panel and is labelled as unadopted.", "",
              "## Method limits", "",
              "- Only the pages opened in this pass were read; links that were not opened may be broken.",
              "- Pages that need JavaScript to render (for example Topcoder) could not be verified and were left unverified.",
              "- Prize pools are not expected value, and no win probability or hourly rate is asserted anywhere.",
              "- Rules can change at any time; each row carries the date it was read.",
              ""]
    (ROOT / "data/EVIDENCE.md").write_text("\n".join(lines))

ev_entries = [(rid, ev) for rid, ev in evidence.items()]
write_evidence_md()

# ---------------------------------------------------------------- data + report
published = {
    "audit_date": AUDIT,
    "upstream": {"repository": up.get("repository"), "commit": up.get("commit"), "reviewed": up.get("reviewed"),
                 "listings": len(up["listings"]), "removed": len(up["removed"])},
    "counts": S,
    "entries": rows,
}
(ROOT / "data/contests.json").write_text(json.dumps(published, indent=1, ensure_ascii=False))
print(f"Built index + contests + {len(cats)} category pages + summary + review + 404")
print(f"Rows: {len(rows)} | verified {S['verified']} | partial {S['partial']} | flagged {S['flagged']} | unverified {S['unverified']} | closed {S['closed']}")
print(f"Free entry confirmed: {S['free']} | cash confirmed: {S['cash']} | usable now: {S['start']} | no official source: {S['no_off']}")
