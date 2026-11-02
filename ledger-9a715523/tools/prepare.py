#!/usr/bin/env python3
"""Import identities and source pointers, never unsupported operational claims."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1]
COMMIT = '466f7c1e7a14b52b4a0d36beb84a00d68fd409b7'
source = json.loads((ROOT / 'data/upstream.json').read_text())
assert source['commit'] == COMMIT
assert len(source['listings']) == 206
BLANK = {k: '' for k in ['free','prize','deadline','eligibility','agent','requirements','payout']}
# Operator pages retrieved 2026-11-02; these are source-pointer repairs only.
OVERRIDES = {
 'fbs-pro-demo': ('https://fbs.com/', 'Official operator homepage retrieved; historical contest news URL returns a branded 404. Current contest terms unverified.'),
 'roboforex-demo': ('https://roboforex.com/forex-trading/trading/trading-accounts/', 'Official contest path redirects to trading accounts; historical 2011 contest article is not a current offer. Current contest terms unverified.'),
 'npbfx-demo': ('https://www.nmarkets.org/fr/', 'Official NPBFX demo-account URL redirects to nmarkets.org; no current Trading Battle terms confirmed.'),
 'tff-fantezi-lig': ('https://tfffantezilig.com/', 'Official game site is linked by TFF; inherited fantazilig.tff.org hostname was reported dead. Current cash-prize terms unverified.'),
 'thelines-survivor': ('https://www.thelines.com/betting/free-games/', 'Operator games page retrieved; it advertises gift-card prizes and survivor pools. Current survivor cash form and eligibility unverified.'),
 'squarespool': ('https://www.squarespool.com/', 'HTTPS operator page replaces inherited HTTP pointer; pool tool is not evidence of an operator-funded cash prize.'),
}
rows = []
for item in source['listings']:
    official = next((s['url'] for s in item.get('sources', []) if s.get('tier') == 'official' and s.get('url', '').startswith('https://')), '')
    flags = ['Inherited listing: current prize, free entry, deadline, eligibility, payout and AI rules have not been confirmed by an official source in this audit.']
    if item['id'] in OVERRIDES:
        official, note = OVERRIDES[item['id']]
        flags.append(note)
    rows.append({
        'id': item['id'], 'name': item['name'], 'category': item['type'],
        'kind': 'inherited', 'status': 'needs-review', 'official_url': official,
        'provenance_url': f'https://karagemop466-tech.github.io/FreeMoneyApps/#{item["id"]}',
        'fields': dict(BLANK), 'flags': flags,
        'evidence': [], 'agent_policy': 'unreviewed', 'window': 'unknown',
    })
assert len({r['id'] for r in rows}) == 206
payload = {
    'source_repository': 'https://github.com/karagemop466-tech/FreeMoneyApps',
    'source_commit': COMMIT,
    'source_reviewed': source['reviewed'],
    'audit_date': '2026-11-02',
    'scope': 'All 206 inherited identities retained. Only separately quoted official evidence populates operational fields. Inherited source pointers are not proof of current contest terms.',
    'historical_exclusion_count': len(source['removed']),
    'rows': rows,
}
(OUT / 'data').mkdir(parents=True, exist_ok=True)
(OUT / 'data/inventory.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
print(f'Imported {len(rows)} identities; {sum(not r["official_url"] for r in rows)} lack an official-tier source pointer.')
