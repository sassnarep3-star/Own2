"""Render a small independently sourced supplement; no inherited claims are promoted."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'data.json').read_text())
CATEGORIES = ('Technology', 'Forecasting', 'Creative')

def esc(value):
    return html.escape(value, quote=True)

def link(url, label):
    return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)} ↗</a>'

def shell(title, body):
    nav = '<nav aria-label="Site navigation"><a href="index.html">Overview</a><a href="all.html">All findings</a>' + ''.join(f'<a href="{esc(c.lower())}.html">{esc(c)}</a>' for c in CATEGORIES) + '<a href="flagged.html">Flagged for review</a><a href="methodology.html">Method</a><a href="../../index.html">Main ledger</a></nav>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)} · PrizeDesk independent audit</title><meta name="description" content="Official-source evidence for free-entry prize competitions, with unresolved questions clearly flagged."><link rel="stylesheet" href="style.css"></head><body><a class="skip" href="#content">Skip to content</a><header><div class="wrap"><span class="eyebrow">PRIZEDESK / INDEPENDENT AUDIT · 02 NOV 2026</span><h1>{esc(title)}</h1><p>Singapore-access and AI-use desk · five event-level records · official operator links for every row</p>{nav}</div></header><main id="content" class="wrap">{body}</main><footer class="wrap">Research snapshot: 2 November 2026 UTC. No personalized eligibility or winnings guarantee. <a href="../../review.html">Main flagged ledger</a> · <a href="EXECUTIVE_SUMMARY.md">Executive summary (Markdown)</a></footer></body></html>'''

def table(rows):
    head = '<div class="table-scroll" role="region" aria-label="Officially sourced competition findings" tabindex="0"><table><thead><tr><th scope="col">Competition / source</th><th scope="col">Free entry</th><th scope="col">Cash prize</th><th scope="col">Deadline</th><th scope="col">Geography rule</th><th scope="col">AI / agent rule</th><th scope="col">Review</th></tr></thead><tbody>'
    result = []
    for r in rows:
        def cell(key):
            field = r.get(key)
            if not field or not field.get('quote'):
                return '<span class="blank" aria-label="Unverified: no official evidence">— unverified</span>'
            url = field.get('source', r['source'])
            return f'{esc(field["value"])}<small>{link(url, "Evidence")}</small>'
        src = link(r['source'], 'Official rules')
        result.append(f'<tr id="{esc(r["id"])}"><th scope="row"><strong>{esc(r["name"])}</strong><small>{esc(r["category"])} · {src}<br>Checked {esc(r["checked"])}</small></th>' + ''.join(f'<td data-label="{label}">{cell(key)}</td>' for key,label in [('free','Free entry'),('prize','Cash prize'),('deadline','Deadline'),('geography','Geography rule'),('ai','AI / agent rule')]) + f'<td data-label="Review">{esc(r["flag"])} <small><a href="flagged.html#{esc(r["id"])}">Review detail →</a></small></td></tr>')
    return head + ''.join(result) + '</tbody></table></div>'

intro = '<section class="hero"><span class="pill">Evidence-first shortlist</span><h2>Prioritize the rules, not the headline prize.</h2><p>These five records are a focused cross-check of the existing ledger, <strong>not five new competitions</strong>. Free entry, prize, deadlines and restrictions are individually linked to official rules. Singapore-specific eligibility and payment are not asserted without express confirmation. A prize pool is not a probability-adjusted return.</p><div class="stats"><div><b>5</b><span>audited events</span></div><div><b>3</b><span>categories</span></div><div><b>5</b><span>flagged for review</span></div></div></section>'
(ROOT / 'index.html').write_text(shell('Independent competition audit', intro + '<h2>Where an agent may help</h2><div class="cards"><article><h3>Build an AI-integrated project</h3><p>PayPal requires a PayPal sandbox integration and AI tool in the product. It does not expressly approve coding-agent authorship; confirm use and submit a working demo.</p><a href="technology.html#paypal">See official-rule row →</a></article><article><h3>Build a forecasting bot</h3><p>FutureEval is bot-only. Its event-specific permission matters: Metaculus generally excludes bots from tournament prizes unless permitted. Payout may be cash equivalent.</p><a href="forecasting.html#futureeval">See bot event →</a></article><article><h3>Keep creative work human</h3><p>Wergle Flomp prohibits AI-generated poem text; Sony requires a photographic origin, not computer-generated content. These are poor agent-output targets.</p><a href="creative.html">See creative rules →</a></article></div><p class="callout">No ranking by expected income: no official source establishes win probability, required hours, compute costs or your individual eligibility. <a href="flagged.html">Read all unresolved checks →</a></p>' + '<h2>All audited records</h2>' + table(DATA)), encoding='utf-8')
(ROOT / 'all.html').write_text(shell('All audited findings', '<p>One row per specific event. “Unverified” means no field-level official quote; all other cells link to their source.</p>' + table(DATA)), encoding='utf-8')
for cat in CATEGORIES:
    rows = [r for r in DATA if r['category'] == cat]
    (ROOT / (cat.lower()+'.html')).write_text(shell(cat + ' competitions', f'<p>{len(rows)} audited event-level record(s). A category count is not a claim of all competitions available in that category.</p>' + table(rows)), encoding='utf-8')
flags = '<p>Open questions are not silently treated as approvals. Check official rules again immediately before participation.</p>' + ''.join(f'<article class="flag" id="{esc(r["id"])}"><h2>{esc(r["name"])}</h2><p>{esc(r["flag"])}</p><p>{link(r["source"], "Operator rules")}' + (f' · {link(r["extra"], "General tournament rules")}' if r.get('extra') else '') + (f' · {link(r["botSource"], "Bot tournament resource")}' if r.get('botSource') else '') + f' · <a href="all.html#{esc(r["id"])}">Audited row</a></p></article>' for r in DATA)
(ROOT / 'flagged.html').write_text(shell('Flagged for review', flags), encoding='utf-8')
method = '<h2>Method and boundaries</h2><ol><li>Read the source ledger and five operator event/rules pages on 2 November 2026. Consulted general Metaculus tournament rules and its FutureEval resource page as exceptions to event rules.</li><li>For every displayed field, stored a literal operator excerpt and linked its actual source in <a href="data.json">data.json</a>. The FutureEval cash-prize cell is blank because its official general rules allow cash equivalents. Its event page advertises a $50,000 prize pool, not a guaranteed cash payout.</li><li>Kept Singapore-specific residence and payout approval unresolved when not explicitly named; eligibility is personal and subject to local rules. No entrant account, submission, or payment was attempted.</li><li>Never rank by expected winnings, never assume AI-tool use equals coding-agent permission, and never extrapolate platform rules to every event.</li></ol><h2>Source links</h2><ul>' + ''.join(f'<li>{link(r["source"],r["name"])}</li>' for r in DATA) + '</ul><p>Other official sources: ' + link('https://www.metaculus.com/tournament-rules/', 'Metaculus tournament rules') + ' · ' + link('https://www.metaculus.com/notebooks/38928/ai-benchmark-resources/', 'FutureEval bot resources') + '.</p>'
(ROOT / 'methodology.html').write_text(shell('Methods & official sources', method), encoding='utf-8')
print('Built 7 pages; 5 operator-sourced records')
