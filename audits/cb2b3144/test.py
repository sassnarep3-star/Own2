#!/usr/bin/env python3
"""Deterministic data and internal-link checks for the isolated supplement."""
import csv, json, re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'evidence.json').read_text())
rows=d['records']
ids=[r['id'] for r in rows]
assert len(ids)==len(set(ids)), 'Duplicate IDs'
assert len(rows)==10
facts=['status','entry','prize','deadline','eligibility','ai','payout']
for r in rows:
    assert r['url'].startswith('https://'), r['id']
    assert r['category'] in {'tech','research','directory'}
    assert isinstance(r['flags'],list)
    covered={f for e in r['evidence'] for f in e['fields']}
    for f in facts:
        if r[f]: assert f in covered, (r['id'],f,'missing evidence')
    for e in r['evidence']:
        assert e['url'].startswith('https://') and e['quote'] and e['locator']
    if r['cash_total_usd'] is not None:
        assert isinstance(r['cash_total_usd'],int) and r['cash_total_usd']>0
        assert r['prize_basis']
# Explicit blanks must remain blank, not be replaced with guesses.
for rid, fields in {'kidney-ai-discovery-2026':['entry'], 'blaise-xtech-phase1-2026':['entry','payout'], 'xprize-quantum-applications':['entry','deadline','eligibility','ai','payout'], 'herox-directory-link':['entry','prize','deadline','eligibility','ai','payout']}.items():
    r=next(x for x in rows if x['id']==rid)
    for f in fields: assert r[f]=='', (rid,f)

class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.ids=set(); self.fragments=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        for key in ('href','src'):
            if key in a: self.links.append(a[key])
pages=sorted(ROOT.glob('*.html'))
assert len(pages)==7
parsed={}
for p in pages:
    parser=Links(); parser.feed(p.read_text()); parsed[p.name]=parser
    text=p.read_text()
    assert 'name="viewport"' in text and '<html lang="en">' in text
    assert '<table' not in text or '<caption' in text
for name,parser in parsed.items():
    for url in parser.links:
        u=urlparse(url)
        if u.scheme or u.netloc or url.startswith('mailto:'): continue
        target=(ROOT/unquote(u.path)) if u.path else ROOT/name
        assert target.exists(), (name,url,'missing target')
        if u.fragment:
            if target.suffix=='.html':
                tp=Links(); tp.feed(target.read_text()); assert unquote(u.fragment) in tp.ids, (name,url,'missing anchor')
with (ROOT/'findings.csv').open() as f: assert len(list(csv.DictReader(f)))==len(rows)
print(f'PASS: {len(rows)} rows; {len(pages)} HTML pages; source evidence coverage, explicit blanks, CSV, local links and anchors.')
