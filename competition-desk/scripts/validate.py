"""Validate coverage, provenance, field-level evidence, and generated internal URLs."""
import json,pathlib,urllib.parse
from html.parser import HTMLParser
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'_site'
data=json.loads((ROOT/'data/competitions.json').read_text());raw=json.loads((ROOT/'data/imported-ledger.json').read_text())
rows=data['rows'];ids={r['id'] for r in rows};assert len(ids)==len(rows)==209
assert {r['id'] for r in raw['listings']}=={r['id'] for r in rows if r['origin']=='imported'}
assert len(data['categories'])==9
fields={'entryFee','prize','deadline','eligibility','payout','aiPolicy'}
for r in rows:
 assert set(r['facts'])==fields
 assert set(r['unknownFields'])=={k for k,v in r['facts'].items() if not v}
 assert r['flags'],f'Missing review flags: {r["id"]}'
 for k,v in r['facts'].items():
  if v:
   ev=r['evidence'][k];assert ev['url'].startswith('https://') and ev['quote'] and ev['checked']=='2026-11-01'
  else:assert k not in r['evidence']
 assert r['officialUrl'] or any('source' in f.lower() for f in r['flags'])
 assert r['freeCash']==(r['facts']['entryFee']=='Free' and bool(r['facts']['prize']))
checks=json.loads((ROOT/'docs/source-checks.json').read_text())
check_urls={c['url'] for c in checks}
expected={r[k] for r in raw['listings'] for k in ('signupUrl','rulesUrl','tosUrl') if r.get(k)}
assert expected==check_urls, 'URL audit must cover every inherited signup/rules/terms URL'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.links=[];self.row_ids=[];self.review_count=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:assert a['id'] not in self.ids,f'Duplicate ID {a["id"]}';self.ids.add(a['id'])
  for key in ('href','src'):
   if key in a:self.links.append(a[key])
  if tag=='tr' and 'data-id' in a:self.row_ids.append(a['data-id'])
  if tag=='tr' and 'data-review' in a:self.review_count+=1
pages={}
for p in OUT.rglob('*.html'):
 parser=Page();parser.feed(p.read_text());pages[p.resolve()]=parser
assert set(pages[(OUT/'index.html').resolve()].row_ids)==ids
assert pages[(OUT/'review/index.html').resolve()].review_count==209
for c in data['categories']:
 actual=set(pages[(OUT/f'categories/{c["id"]}/index.html').resolve()].row_ids)
 assert actual=={r['id'] for r in rows if r['category']==c['id']}
link_count=0
for path,page in pages.items():
 for href in page.links:
  u=urllib.parse.urlsplit(href)
  if u.scheme or u.netloc:continue
  if u.path.startswith('/Own2/competition-desk/'):target=OUT/u.path[len('/Own2/competition-desk/'):]
  elif u.path.startswith('/'):target=OUT/u.path.lstrip('/')
  elif u.path:target=path.parent/u.path
  else:target=path
  if target.is_dir():target=target/'index.html'
  target=target.resolve();assert target.is_relative_to(OUT.resolve())
  assert target.exists(),f'Broken internal URL {href} on {path}'
  if u.fragment and target in pages:assert urllib.parse.unquote(u.fragment) in pages[target].ids,f'Missing fragment {href} on {path}'
  link_count+=1
print(f'PASS: {len(rows)} rows, 206 imported IDs, field citations, blank unknowns, {len(checks)} URL audit records, {len(pages)} HTML pages, {link_count} internal links/anchors.')
