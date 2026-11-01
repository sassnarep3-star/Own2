"""Offline invariants; explicitly not a remote HTTP or legal verification test."""
import json
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit
P = Path(__file__).resolve().parent
R = P.parent.parent
rows = json.loads((P / 'evidence.json').read_text())
assert len(rows) == 13
assert len({r['id'] for r in rows}) == 13
catalog = json.loads((R / 'data/contests.json').read_text())
# Final integration: the canonical builder now wraps the same rows in entries.
upstream = {r['id'] for r in (catalog['entries'] if isinstance(catalog, dict) else catalog)}
fields = {'id', 'name', 'category', 'fee', 'prize', 'dates', 'eligibility_ai', 'finding', 'sources', 'excerpt'}
for r in rows:
    assert set(r) == fields, r['id']
    assert r['id'] in upstream, r['id']
    assert r['category'] in ('creative', 'gaming', 'research')
    assert r['sources'] and r['excerpt'] and 'review' in r['finding'].lower()
    assert all(urlsplit(s).scheme == 'https' and urlsplit(s).hostname for s in r['sources'])
for id in ('zindi', 'film-prize'):
    r = next(x for x in rows if x['id'] == id)
    assert all(r[k] == '' for k in ('fee', 'prize', 'dates', 'eligibility_ai'))
assert next(r for r in rows if r['id'] == 'gamersaloon')['prize'] == ''
assert '10%' in next(r for r in rows if r['id'] == 'freelancer-contests')['fee']
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.inrow = False
        self.sources = 0
        self.cells = 0
        self.rows = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'tr':
            self.inrow = True
            self.cells = self.sources = 0
        if tag == 'td':
            self.cells += 1
        for k in ('href', 'src'):
            if not a.get(k):
                continue
            u = urlsplit(a[k])
            assert u.scheme in ('', 'https'), a[k]
            if not u.scheme and u.path:
                dest = (self.path.parent / unquote(u.path)).resolve()
                assert dest.is_relative_to(R) and dest.is_file(), (self.path, a[k])
            if tag == 'a' and self.inrow and u.scheme == 'https':
                self.sources += 1
    def handle_endtag(self, tag):
        if tag == 'tr':
            if self.cells:
                assert self.cells == 7 and self.sources > 0, self.path
                self.rows += 1
            self.inrow = False
expected = {'index.html':13, 'creative.html':7, 'gaming.html':3, 'research.html':3, 'review.html':13}
for name, count in expected.items():
    p = P / name
    before = p.read_text()
    parser = Page(p)
    parser.feed(before)
    assert parser.rows == count, (name, parser.rows)
    assert '<html lang="en">' in before and 'name="viewport"' in before
    assert '<caption>' in before and 'scope="col"' in before
    assert '<script' not in before
    subprocess.run([sys.executable, str(P/'build.py')], check=True, capture_output=True)
    assert p.read_text() == before, 'Build is not deterministic'
print('PASS: 13 inherited IDs; field schema; blank unsupported values; review flags; source per row; five deterministic pages; local links; accessible table/viewport metadata. Remote link health not asserted.')
