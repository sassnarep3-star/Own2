"""Static provenance/navigation regression checks for this independent supplement."""
import importlib.util
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
ROWS = json.loads((ROOT / 'data.json').read_text())

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'a' and 'href' in a: self.hrefs.append(a['href'])

class AuditTests(unittest.TestCase):
    def test_record_sources_and_fields(self):
        self.assertEqual(len(ROWS), 5)
        self.assertEqual(len({r['id'] for r in ROWS}), len(ROWS))
        for r in ROWS:
            self.assertRegex(r['source'], r'^https://')
            self.assertTrue(r['flag'])
            for key in ('free','prize','deadline','geography','ai'):
                f = r[key]
                if f is not None:
                    self.assertTrue(f['quote'].strip(), (r['id'], key))
                    self.assertTrue(f['value'].strip(), (r['id'], key))
                    self.assertRegex(f.get('source',r['source']), r'^https://')
        self.assertIsNone(next(r for r in ROWS if r['id']=='futureeval')['prize'], 'Cash not guaranteed by Metaculus')

    def test_pages_and_links(self):
        docs = list(ROOT.glob('*.html'))
        self.assertEqual(len(docs), 7)
        for doc in docs:
            text = doc.read_text()
            self.assertIn('name="viewport"', text)
            self.assertIn('<html lang="en">', text)
            links = Links(); links.feed(text)
            for href in links.hrefs:
                u = urlsplit(href)
                if u.scheme in ('https','http','mailto'): continue
                target = (doc.parent / unquote(u.path)).resolve() if u.path else doc
                self.assertTrue(target.is_file(), (doc.name, href))
                if u.fragment and target.suffix == '.html':
                    parsed = Links(); parsed.feed(target.read_text())
                    self.assertIn(unquote(u.fragment), parsed.ids, (doc.name, href))
            if doc.name in ('all.html','index.html'):
                for r in ROWS:
                    self.assertIn('id="' + r['id'] + '"', text)
                    self.assertIn(r['source'], text)

    def test_deterministic_build(self):
        before = {p.name:p.read_bytes() for p in ROOT.glob('*.html')}
        spec = importlib.util.spec_from_file_location('audit_build',ROOT/'build.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        self.assertEqual(before,{p.name:p.read_bytes() for p in ROOT.glob('*.html')})

if __name__ == '__main__': unittest.main()
