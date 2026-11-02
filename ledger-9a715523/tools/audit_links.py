#!/usr/bin/env python3
"""Reachability only. Never treats HTTP success as contest verification."""
import concurrent.futures, json, re, socket, ssl, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
ROOT=Path(__file__).resolve().parents[1]
inv=json.loads((ROOT/'data/inventory.json').read_text())
events=json.loads((ROOT/'research/events.json').read_text())
urls={}
def add(url, row, role):
 if url:
  urls.setdefault(url, {'url':url,'rows':[],'roles':[]})
  if row not in urls[url]['rows']: urls[url]['rows'].append(row)
  if role not in urls[url]['roles']: urls[url]['roles'].append(role)
for r in inv['rows']: add(r.get('official_url'),r['id'],'inherited official pointer')
for r in events['records']:
 add(r['official_url'],r['id'],'official event source')
 for e in r['evidence']: add(e['url'],r['id'],'field evidence')

def check(item):
 url=item['url']; start=time.monotonic(); result=dict(item)
 try:
  req=Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; PrizeLens-LinkAudit/1.0)','Accept':'text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8'})
  with urlopen(req,timeout=20) as resp:
   body=resp.read(180000); result.update(status=resp.status,final_url=resp.url,content_type=resp.headers.get('Content-Type',''))
   text=body.decode('utf-8','ignore') if 'pdf' not in result['content_type'] else ''
   title=re.search(r'<title[^>]*>(.*?)</title>',text,re.I|re.S)
   result['title']=re.sub(r'\s+',' ',title.group(1)).strip()[:200] if title else ''
   soft=bool(re.search(r'page not found|page does not exist|sorry, that page|404 page not found',result['title'],re.I))
   result['classification']='soft-404' if soft else ('redirected' if resp.url.rstrip('/')!=url.rstrip('/') else 'reachable')
 except HTTPError as e:
  result.update(status=e.code,final_url=e.url,classification='blocked' if e.code in (401,403,429) else 'http-error')
 except Exception as e:
  result.update(status=None,classification='network-error',error=f'{type(e).__name__}: {str(e)[:220]}')
 result['elapsed_ms']=round((time.monotonic()-start)*1000)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
 results=list(pool.map(check,urls.values()))
counts={}
for r in results: counts[r['classification']]=counts.get(r['classification'],0)+1
out={'checked_at':datetime.now(timezone.utc).isoformat(timespec='seconds'),'method':'GET with 20-second timeout, 10 workers; first 180 KB inspected for title/soft-404. Reachability is not official-content verification. Blocks and network errors are inconclusive.','counts':counts,'results':sorted(results,key=lambda r:r['url'])}
dest=ROOT/'research/link-audit.json'
if '--output' in sys.argv: dest=Path(sys.argv[sys.argv.index('--output')+1])
dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(counts,sort_keys=True));print(f'{len(results)} unique URLs; report: {dest}')
