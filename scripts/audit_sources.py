"""Check every inherited operator/rules URL. HTTP success is NOT claim verification."""
import concurrent.futures, datetime, hashlib, json, pathlib, re, urllib.request
from html.parser import HTMLParser

class Text(HTMLParser):
    def __init__(self): super().__init__(); self.skip=0; self.parts=[]
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','noscript'): self.skip+=1
    def handle_endtag(self, tag):
        if tag in ('script','style','noscript'): self.skip=max(0,self.skip-1)
    def handle_data(self, data):
        if not self.skip and data.strip(): self.parts.append(data.strip())

def check(url):
    result={'url':url,'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'httpStatus':None,'finalUrl':'','error':'','excerpt':'','sha256':''}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Own2-SourceAudit/1.0 (+https://github.com/sassnarep3-star/Own2)'})
        with urllib.request.urlopen(req,timeout=25) as r:
            raw=r.read(2500000); result['httpStatus']=r.status;result['finalUrl']=r.url
            result['sha256']=hashlib.sha256(raw).hexdigest()
            text=raw.decode('utf-8',errors='replace');p=Text();p.feed(text)
            result['excerpt']='\n'.join(p.parts)[:45000]
    except Exception as e:
        result['error']=str(e)
        if hasattr(e,'code'):result['httpStatus']=e.code
    return result

if __name__=='__main__':
    rows=json.loads(pathlib.Path('data/imported-ledger.json').read_text())['listings']
    urls=sorted({r[k] for r in rows for k in ('signupUrl','rulesUrl','tosUrl') if r.get(k)})
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool: results=list(pool.map(check,urls))
    pathlib.Path('audit-output').mkdir(exist_ok=True)
    pathlib.Path('audit-output/source-checks.json').write_text(json.dumps(results,indent=2))
    print(f'Checked {len(urls)} URLs across {len(rows)} rows; {sum(r["httpStatus"]==200 for r in results)} HTTP 200 responses. Claims still require review.')
