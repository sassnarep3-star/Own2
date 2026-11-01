"""Run after deployment; verify the actual public project subpath and assets."""
import json,time,urllib.request
BASE='https://sassnarep3-star.github.io/Own2/'
data=json.load(open('data/competitions.json'))
paths=['index.html','summary/index.html','review/index.html','assets/styles.css','assets/app.js','assets/catalog.json','data/competitions.csv','docs/source-checks.json']+[f'categories/{c["id"]}/index.html' for c in data['categories']]
for path in paths:
    for attempt in range(5):
        try:
            with urllib.request.urlopen(BASE+path,timeout=30) as r:
                assert r.status==200
                body=r.read().decode('utf-8')
                if path=='index.html':assert 'Competition directory' in body and 'futureeval-fall-2026' in body
                if path=='assets/catalog.json':assert len(json.loads(body)['rows'])==209
            print('PASS',BASE+path)
            break
        except Exception:
            if attempt==4:raise
            time.sleep(10)
print(f'Public deployment smoke checks passed: {len(paths)} URLs.')
