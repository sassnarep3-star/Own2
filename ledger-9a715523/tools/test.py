#!/usr/bin/env python3
"""Static/provenance tests. External reachability is audited separately."""
import csv, hashlib, json, re, subprocess, sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]
inv=json.loads((ROOT/'data/inventory.json').read_text()); events=json.loads((ROOT/'research/events.json').read_text()); catalog=json.loads((ROOT/'data/catalog.json').read_text())
source=json.loads((ROOT.parent/'data/upstream.json').read_text())
assert len(inv['rows'])==len(source['listings'])==206
assert len({r['id'] for r in inv['rows']})==206
assert {r['id'] for r in inv['rows']}=={r['id'] for r in source['listings']}
assert Counter(r['category'] for r in inv['rows'])==Counter(r['type'] for r in source['listings'])
assert len(events['records'])==18
assert len(catalog['rows'])==224
assert len({r['id'] for r in catalog['rows']})==224
for old,new in zip(source['listings'],inv['rows']):
    assert old['id']==new['id'] and old['name']==new['name'] and old['type']==new['category']
    assert all(new['fields'][k]=='' for k in ['free','prize','deadline','eligibility','agent','requirements','payout'])
    assert new['status']=='needs-review' and new['flags']
    assert new['official_url']=='' or new['official_url'].startswith('https://')
for r in events['records']:
    assert r['official_url'].startswith('https://')
    fields={e['field'] for e in r['evidence']}
    for k,v in r['fields'].items():
        if v: assert k in fields,(r['id'],k)
    for e in r['evidence']:
        assert e['quote'] and e['url'].startswith('https://') and e['locator'] and e['checked']=='2026-11-02'
    if r['shortlist']:
        assert r['fields']['free'] and r['fields']['prize'] and r['window'] in ('open','closing')
        assert 'free' in fields and 'prize' in fields
    if r['top_cash_usd'] is not None: assert isinstance(r['top_cash_usd'],(int,float)) and r['top_cash_usd']>0
assert not any(r['id']=='event-ugreen' and r['pool_usd'] is not None for r in events['records']), 'Derived pool must not be published as an official total'
# Link audit coverage is separate from content verification, but every collected pointer must be represented.
if (ROOT/'research/link-audit.json').exists():
    audit=json.loads((ROOT/'research/link-audit.json').read_text())
    audited={r['url'] for r in audit['results']}
    expected={r['official_url'] for r in inv['rows'] if r['official_url']}
    expected|={e['url'] for r in events['records'] for e in r['evidence']}
    if 'every inherited source pointer' in audit.get('method',''):
        expected|={s['url'] for r in source['listings'] for s in r.get('sources',[]) if s.get('url')}
    assert expected<=audited,('missing link audit URLs',sorted(expected-audited)[:10])
    assert sum(audit['counts'].values())==len(audit['results'])
    assert all(r['classification'] in {'reachable','redirected','blocked','redirect-unresolved','server-error','http-error','network-error','soft-404'} for r in audit['results'])
with (ROOT/'data/catalog.csv').open(newline='',encoding='utf-8') as f: csvrows=list(csv.DictReader(f))
assert len(csvrows)==224
assert {r['id'] for r in csvrows}=={r['id'] for r in catalog['rows']}
class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.links=[];self.ids=[];self.tables=0;self.rows=0;self.h1=0;self.lang=None;self.viewport=False;self.scripts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='meta' and a.get('name')=='viewport':self.viewport=True
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if 'id' in a:self.ids.append(a['id'])
        if tag=='table':self.tables+=1
        if tag=='tr':self.rows+=1
        if tag=='h1':self.h1+=1
        if tag=='script' and 'src' in a:self.scripts.append(a['src'])
pages=sorted(ROOT.glob('*.html')); assert len(pages)==19,len(pages)
all_ids=set();local_links=[]
for p in pages:
    parser=Parser();text=p.read_text();parser.feed(text)
    assert parser.lang=='en' and parser.viewport and parser.h1==1,p.name
    assert len(parser.ids)==len(set(parser.ids)),('duplicate IDs',p.name)
    assert '<html' in text and '</html>' in text
    assert 'assets/style.css' in text
    for link in parser.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:
            assert u.scheme in ('https','mailto'),(p.name,link)
            continue
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        assert target.is_relative_to(ROOT.parent),(p.name,link)
        assert target.exists(),(p.name,link)
        local_links.append((p,target,u.fragment))
    all_ids.update((p.name,i) for i in parser.ids)
for p,target,fragment in local_links:
    if fragment and target.suffix=='.html':
        parser=Parser();parser.feed(target.read_text());assert fragment in parser.ids,(p.name,fragment)
alltext=(ROOT/'all.html').read_text()
for r in catalog['rows']: assert f'id="{r["id"]}"' in alltext,r['id']
assert alltext.count('data-name=')==224
assert (ROOT/'shortlist.html').read_text().count('data-name=')==12
for key in ['tech','creative','sports','forecasting','skill','market','trivia','pools','directory']:
    text=(ROOT/f'category-{key}.html').read_text();assert text.count('data-name=')==sum(r['category']==key for r in catalog['rows'])
# Deterministic build: generated artifacts must not depend on build time or ordering.
tracked=[p for p in ROOT.rglob('*') if p.is_file() and p.suffix in ('.html','.csv','.md') or p.name=='catalog.json']
before={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
subprocess.run([sys.executable,str(ROOT/'tools/build.py')],check=True,capture_output=True)
after={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
assert before==after,'Build is not deterministic'
print(f'PASS: {len(pages)} pages, 224 unique rows, 18 event reviews, {len(local_links)} local links, 9 category partitions, CSV parity, evidence coverage, deterministic build.')
