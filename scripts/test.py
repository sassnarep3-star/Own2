import json,pathlib,re,subprocess
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
R=pathlib.Path(__file__).resolve().parent.parent
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('href','src') and v and not v.startswith(('#','data:','mailto:')):
    u=urlsplit(v)
    if not u.scheme: assert (R/unquote(u.path)).is_file(),v
rows=json.loads((R/'data/contests.json').read_text());up=json.loads((R/'data/upstream.json').read_text())
assert len(rows)==209 and len({x['id'] for x in rows})==209
assert {x['id'] for x in up['listings']} <= {x['id'] for x in rows}
assert len(up['listings'])==206
for r in rows:
 assert urlsplit(r['source']).scheme == 'https',r['id']
 if r['id']!='arc-paper-2026': assert not r['free'],r['id']
 if not r['checked']:assert not any(r[k] for k in ['prize','deadline','eligibility','ai'])
for p in R.glob('*.html'):
 text=p.read_text();Links().feed(text)
 assert 'name="viewport"' in text and '<html lang="en">' in text
assert (R/'index.html').read_text().count('<tr data-search=')==209
subprocess.run(['node','--check',str(R/'app.js')],check=True)
print('PASS: data integrity, upstream coverage, blank unsupported fields, all local links/assets, responsive metadata, JavaScript syntax.')
