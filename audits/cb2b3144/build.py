#!/usr/bin/env python3
"""Build the isolated cb2b3144 official-source supplement. No shared files are edited."""
from __future__ import annotations
import csv, html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'evidence.json').read_text())
RECORDS = DATA['records']
CATEGORIES = {'tech': 'Tech & AI hackathons', 'research': 'Research prizes', 'directory': 'Directories'}
FACT_FIELDS = ['status','entry','prize','deadline','eligibility','ai','payout']

def esc(x): return html.escape(str(x if x is not None else ''), quote=True)
def money(x): return '' if x is None else f'${x:,.0f}'
def link(url, label=None):
    if not url: return '<span class="muted">Not confirmed</span>'
    return f'<a href="{esc(url)}" rel="noopener noreferrer" target="_blank">{esc(label or url)}</a>'

def nav(active):
    items = [('index.html','Overview'),('all.html','All findings'),('tech.html','Tech & AI'),('research.html','Research'),('directory.html','Directories'),('flagged.html','Flagged for Review'),('methodology.html','Methodology')]
    return '<nav aria-label="Supplement navigation">' + ''.join(f'<a href="{href}"'+(' aria-current="page"' if href==active else '')+f'>{label}</a>' for href,label in items) + '</nav>'

def page(title, active, body, desc=''):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Free Cash Competition Ledger</title>
<meta name="description" content="{esc(desc or title)}">
<link rel="stylesheet" href="styles.css"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap"><p class="eyebrow">Official-source supplement · session cb2b3144</p><h1>{esc(title)}</h1><p class="lede">{esc(desc)}</p>{nav(active)}</div></header>
<main id="main" class="wrap">{body}</main>
<footer class="wrap"><p>Reviewed {esc(DATA['reviewed_utc'])} UTC. Unknown fields are blank. This supplement does not replace the main ledger or guarantee eligibility, availability, or prize payment.</p><p><a href="../../index.html">Main dashboard</a> · <a href="../../dashboard/index.html">Parallel dashboard</a> · <a href="EXECUTIVE_SUMMARY.md">Executive summary (Markdown)</a></p></footer>
<script src="app.js"></script></body></html>'''

def badges(r):
    out=[]
    if r['entry']: out.append('<span class="badge ok">Entry terms checked</span>')
    else: out.append('<span class="badge warn">Entry unverified</span>')
    if r['flags']: out.append(f'<span class="badge warn">{len(r["flags"])} flag(s)</span>')
    return ' '.join(out)

def table(rows, tid='findings'):
    head = ['Competition','Category','Status / deadline','Entry','Cash prize','AI / agent fit','Eligibility','Payout','Source','Review']
    parts=[f'<div class="table-wrap"><table id="{tid}"><caption class="sr-only">Verified and unverified competition findings</caption><thead><tr>'+''.join(f'<th scope="col">{h}</th>' for h in head)+'</tr></thead><tbody>']
    for r in rows:
        src = link(r['rules_url'] or r['url'], 'Official rules' if r['rules_url'] else 'Official page')
        if r['rules_url'] and r['url'] != r['rules_url']:
            src += '<br>' + link(r['url'], 'Event page')
        cells = [
            f'<strong>{esc(r["name"])}</strong><br><span class="muted">{esc(r["organizer"])}</span><br>{badges(r)}',
            esc(CATEGORIES[r['category']]),
            f'{esc(r["status"])}<br><strong>{esc(r["deadline"] or "Deadline not confirmed")}</strong>',
            esc(r['entry']) or '<span class="muted">Unverified</span>',
            (f'<strong>{esc(money(r["cash_total_usd"]))}</strong><br>' if r['cash_total_usd'] is not None else '') + (esc(r['prize']) or '<span class="muted">Unverified</span>'),
            esc(r['ai']) or '<span class="muted">Unverified</span>',
            esc(r['eligibility']) or '<span class="muted">Unverified</span>',
            esc(r['payout']) or '<span class="muted">Unverified</span>',
            src,
            '<a href="flagged.html#'+esc(r['id'])+'">Flags & evidence</a>' if r['flags'] else '<span class="muted">None recorded</span>',
        ]
        parts.append(f'<tr id="{esc(r["id"])}" data-category="{esc(r["category"])}">'+''.join(f'<td data-label="{esc(h)}">{c}</td>' for h,c in zip(head,cells))+'</tr>')
    parts.append('</tbody></table></div>')
    return ''.join(parts)

def evidence_section(r):
    ev=''.join(f'<li><strong>{esc(", ".join(e["fields"]))}</strong> · {esc(e["locator"])} · {link(e["url"])}<blockquote>{esc(e["quote"])}</blockquote></li>' for e in r['evidence'])
    flags=''.join(f'<li>{esc(f)}</li>' for f in r['flags']) or '<li>No irregularities recorded in this supplement.</li>'
    return f'<article class="card" id="{esc(r["id"])}"><h3>{esc(r["name"])}</h3><p>{badges(r)}</p><h4>Flagged for review</h4><ul>{flags}</ul><h4>Source evidence</h4><ul class="evidence">{ev}</ul><p>{link(r["rules_url"] or r["url"], "Open official source")}</p></article>'

# Overview
short = [r for r in RECORDS if r['category']=='tech' and r['entry']]
summary = f'''
<section class="grid stats" aria-label="Audit counts">
<div class="card stat"><strong>{len(RECORDS)}</strong><span>event-level findings</span></div>
<div class="card stat"><strong>{len(short)}</strong><span>tech events with checked entry terms</span></div>
<div class="card stat"><strong>{sum(1 for r in RECORDS if not r['entry'])}</strong><span>entry terms still unverified</span></div>
<div class="card stat"><strong>{sum(len(r['flags']) for r in RECORDS)}</strong><span>review flags</span></div>
</section>
<section class="card"><h2>Executive decision</h2>
<p>For an AI coding-agent workflow, the best current fits are <strong>Codex x TwitchCon</strong> (explicit Codex requirement, but deadline is 2026-11-02), <strong>Kiroween</strong> (Kiro required, public repo, Dec. 4), <strong>PayPal AI Hackathon</strong> (PayPal + AI, Nov. 12), <strong>UGREEN AI NAS</strong> (constrained Skill workflow, Nov. 15), and <strong>Codegeist</strong> (Forge/MCP/agent tracks, Dec. 22). Meta VR Start has a larger headline purse but is membership-gated.</p>
<p>Do not rank by headline prize alone. Confirm the live form, individual eligibility, required tools, IP/publicity terms, and whether the required demo can be completed before the deadline. No expected-earnings estimate is made because win probability and judging outcomes are not verified.</p>
<p><a class="button" href="all.html">Open all findings</a> <a class="button secondary" href="flagged.html">Review flags</a></p></section>
<section><h2>Recommended tech shortlist</h2><p class="muted">Editorial fit, not a guarantee of winning. Sorted by the practical recommendation in each row.</p>{table(short)}</section>
<section class="card"><h2>What changed in this pass</h2><ul>
<li>Added event-level rules checks instead of treating platform directories as verified competitions.</li>
<li>Separated cash prizes from credits, subscriptions, swag, and conditional headline purses.</li>
<li>Left unconfirmed entry fees, deadlines, eligibility, AI permissions, and payout fields blank.</li>
<li>Flagged a broken HeroX legacy directory path and provided the retrieved working directory.</li>
</ul></section>'''
(ROOT/'index.html').write_text(page('Competition decision brief','index.html',summary,'A mobile-friendly, official-source supplement for finding free-to-enter cash-prize competitions worth an AI agent’s time.'))

# All and category pages
controls = '''<div class="controls card"><label>Search findings <input id="q" type="search" placeholder="Name, organizer, rule, flag…"></label><label>Category <select id="cat"><option value="">All categories</option><option value="tech">Tech & AI</option><option value="research">Research</option><option value="directory">Directories</option></select></label><label><input id="flagged-only" type="checkbox"> Only rows with flags</label><p id="count" class="muted" aria-live="polite"></p></div>'''
(ROOT/'all.html').write_text(page('All findings','all.html',controls+table(RECORDS),'Every supplement row, with official source links and blank unconfirmed fields.'))
for cat,label in CATEGORIES.items():
    rows=[r for r in RECORDS if r['category']==cat]
    (ROOT/f'{cat}.html').write_text(page(label,f'{cat}.html',f'<p>{len(rows)} finding(s). Unknowns remain blank.</p>'+table(rows),f'Official-source findings in {label}.'))

# Flagged page
flagged = ''.join(evidence_section(r) for r in RECORDS if r['flags'])
(ROOT/'flagged.html').write_text(page('Flagged for Review','flagged.html','<p>Flags and unverified items are published for review and do not block the site. A flag is not proof of misconduct; it marks a gap, conflict, cost, restriction, or link issue.</p>'+flagged,'Unverified fields, irregularities, costs, restrictions, and source gaps.'))

method = f'''<section class="card"><h2>Verification standard</h2><p>{esc(DATA['method'])}</p><ul>
<li>Official source means the organizer, sponsor, administrator, or government challenge page—not the reference ledger or a review blog.</li>
<li>Every populated factual field in the table is backed by at least one evidence item in <a href="evidence.json">evidence.json</a>.</li>
<li>Blank means not confirmed from the retrieved official source. It does not mean zero, none, or unavailable.</li>
<li>Cash totals are sums of official USD prize rows where stated; credits, subscriptions, hardware, swag, and travel are not counted as cash.</li>
<li>AI fit is an editorial assessment. Explicit tool requirements and permissions are quoted separately.</li>
<li>This pass does not exhaustively verify all 206 inherited ledger entries, all external links, Texas-specific legal eligibility, tax treatment, or future rule changes.</li>
</ul></section><section class="card"><h2>Reproduce</h2><pre>python audits/cb2b3144/build.py
python audits/cb2b3144/test.py</pre><p>Outputs are static HTML and CSV. No account, API key, or manual data entry is required to build the supplement.</p></section>'''
(ROOT/'methodology.html').write_text(page('Methodology','methodology.html',method,'How facts, blanks, flags, and recommendations are separated.'))

# CSV
with (ROOT/'findings.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['id','name','category','organizer','status','entry','prize','cash_total_usd','deadline','eligibility','ai','payout','official_url','rules_url','flags'])
    for r in RECORDS: w.writerow([r['id'],r['name'],r['category'],r['organizer'],r['status'],r['entry'],r['prize'],r['cash_total_usd'],r['deadline'],r['eligibility'],r['ai'],r['payout'],r['url'],r['rules_url'],' | '.join(r['flags'])])

print(f'Built {len(RECORDS)} findings into {ROOT}')
