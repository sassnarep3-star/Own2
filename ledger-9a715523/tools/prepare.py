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
rows = []
for item in source['listings']:
    official = next((s['url'] for s in item.get('sources', []) if s.get('tier') == 'official' and s.get('url', '').startswith('https://')), None)
    rows.append({
        'id': item['id'], 'name': item['name'], 'category': item['type'],
        'kind': 'inherited', 'official_url': official,
        'provenance_url': f'https://karagemop466-tech.github.io/FreeMoneyApps/#{item["id"]}',
        'fields': {}, 'flags': ['Inherited listing: current prize, free entry, deadline, eligibility, payout and AI rules have not been confirmed by an official source in this audit.'],
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
