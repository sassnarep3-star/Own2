"""Offline integrity checks for this independent supplement."""
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
repo = HERE.parents[1]
rows = json.loads((HERE / 'evidence.json').read_text())['rows']
legacy = {r['id'] for r in json.loads((repo / 'data/contests.json').read_text())['entries']}
assert len(rows) == 4 and len({r['id'] for r in rows}) == 4
assert all(r['id'] in legacy for r in rows)
assert all(r['free'] is None or r['cash'] is None or r['status'].startswith('Closed') for r in rows)
for row in rows:
    assert urlsplit(row['source']).hostname in {'www.bridgewater.com', 'hub.crunchdao.com', 'www.indycar.com', 'help.swagbucks.com'}
    assert row['flags']
    for key in ('free', 'cash', 'deadline', 'ai'):
        assert row[key] is None or row['quotes'].get(key), (row['id'], key)
    if row['id'] == 'crunchdao':
        assert row['cash'] is None and row['free'] is None
    if row['id'] == 'indycar-fantasy':
        assert row['cash'] is None and row['ai']

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.local = []
        self.sources = []
    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        url = dict(attrs).get('href', '')
        if urlsplit(url).scheme == 'https':
            self.sources.append(url)
        elif url and not url.startswith('#'):
            self.local.append(url.split('#')[0])

before = {p.name: p.read_text() for p in HERE.glob('*.html')}
subprocess.run([sys.executable, str(HERE / 'build.py')], check=True)
assert before == {p.name: p.read_text() for p in HERE.glob('*.html')}, 'build changed committed HTML'
for name in ('index.html', 'flagged.html'):
    page = (HERE / name).read_text()
    links = Links()
    links.feed(page)
    assert 'name="viewport"' in page
    assert all((HERE / url).is_file() for url in links.local)
    for row in rows:
        assert row['source'] in links.sources
        assert row['name'].replace('&', '&amp;') in page
assert len(re.findall('<tr>', before['index.html'])) == 5
print('OK: four distinct legacy IDs, source and quote coverage, blank policy, reproducibility, mobile metadata, internal links')
