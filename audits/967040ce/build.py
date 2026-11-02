"""Build the isolated, evidence-first GitHub Pages supplement (stdlib only)."""
import html
import json
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
record = json.loads((HERE / 'evidence.json').read_text())
rows = record['rows']
assert len({r['id'] for r in rows}) == len(rows)
for r in rows:
    assert urlsplit(r['source']).scheme == 'https'
    assert r['flags']
    for field in ('free', 'cash', 'deadline', 'ai'):
        assert r[field] is None or r['quotes'].get(field), (r['id'], field)

def e(value):
    return html.escape(str(value), quote=True)

def link(url, label='Official rules ↗'):
    return f'<a href="{e(url)}" rel="noopener noreferrer">{e(label)}</a>'

def frame(title, body):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | PrizeDesk independent audit</title><link rel="stylesheet" href="style.css"></head><body><a class="skip" href="#main">Skip to content</a><header><div class="wrap"><a class="brand" href="../../index.html">PrizeDesk <span>/ Independent audit</span></a><nav aria-label="Audit navigation"><a href="index.html">Findings</a><a href="flagged.html">Flagged for Review</a><a href="../../review.html">Main review queue</a></nav></div></header><main class="wrap" id="main">{body}</main><footer class="wrap">Independent spot audit • 2 Nov 2026 UTC • <a href="evidence.json">Source evidence (JSON)</a> • <a href="../../summary.html">Main executive summary</a></footer></body></html>'''

tr = []
flag_rows = []
for r in rows:
    source = link(r['source'])
    cells = [f'<th scope="row"><strong>{e(r["name"])}</strong><small>{e(r["category"])}</small></th>']
    for field in ('free', 'cash', 'deadline', 'status', 'ai', 'priority'):
        val = r[field]
        label = {'free':'Free entry','cash':'Cash prize','deadline':'Deadline','status':'Status','ai':'AI / automation','priority':'Time decision'}[field]
        cells.append(f'<td data-label="{e(label)}">{e(val) if val else "<span class=unknown>— Unverified</span>"}</td>')
    cells.append(f'<td data-label="Official source">{source} <a href="flagged.html#{e(r["id"])}">Review flags →</a></td>')
    tr.append('<tr>' + ''.join(cells) + '</tr>')
    quotes = ''.join(f'<li><strong>{e(k)}:</strong> “{e(q)}”</li>' for k,q in r['quotes'].items())
    flags = ''.join(f'<li>{e(f)}</li>' for f in r['flags'])
    flag_rows.append(f'<section class="panel" id="{e(r["id"])}"><h2>{e(r["name"])}</h2><p>{source}</p><h3>Official-page excerpts</h3><ul>{quotes}</ul><h3>Needs review / constraints</h3><ul>{flags}</ul></section>')

body = f'''<p class="eyebrow">Official-source spot audit · 2 November 2026</p><h1>Four leads, checked for real free-cash fit.</h1><p class="lede">The inherited ledger is a lead list, not a verified list of open cash opportunities. Here are four <em>additional</em> entries checked against the operator's own pages. No row below is confirmed both free to enter <strong>and</strong> currently eligible for a fiat-cash award.</p><div class="metrics"><div><b>4</b><span>official pages inspected</span></div><div><b>0</b><span>confirmed current free-cash fits</span></div><div><b>4</b><span>rows requiring review</span></div></div><h2>Decision table</h2><p>“— Unverified” means the cited page does not establish this field; it does not mean “no.” Historical prizes are marked as historical. <a href="flagged.html">Read excerpts and flags</a>.</p><div class="table-scroll"><table><thead><tr><th scope="col">Lead</th><th scope="col">Free entry</th><th scope="col">Cash prize</th><th scope="col">Deadline</th><th scope="col">Status</th><th scope="col">AI / automation</th><th scope="col">Time decision</th><th scope="col">Official source</th></tr></thead><tbody>{''.join(tr)}</tbody></table></div><section class="panel"><h2>Executive take</h2><p>Do not allocate agent-development time to the 2025 Bridgewater or INDYCAR contests. Bridgewater explicitly bars substantially AI-generated work and transfers submission IP; INDYCAR bans automated methods and its published prizes are noncash. CrunchDAO's $100,000 is denominated in USDC, and its reopened submissions are experimental, not award-eligible. Swagbucks describes a Live cash game and a separate SB game without sufficient event-specific terms to establish a free cash opportunity.</p><p>This is a four-record check, not a re-verification of all 206 inherited rows. Recheck the operator's latest rules before entering; eligibility, entry windows and award terms can change.</p></section>'''
(HERE / 'index.html').write_text(frame('Decision table', body))
(HERE / 'flagged.html').write_text(frame('Flagged for Review', '<p class="eyebrow">Evidence notebook</p><h1>Flagged for Review</h1><p class="lede">Each quote was read from the linked operator page on 2 November 2026. Short excerpts support only the stated field, not unstated costs, personal eligibility or payment guarantees. All four rows have unresolved conditions.</p>' + ''.join(flag_rows)))
print(f'Built {len(rows)} audit rows, {sum(len(r["flags"]) for r in rows)} flags')
