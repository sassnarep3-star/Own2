import csv, json, re, unittest
from pathlib import Path
from urllib.parse import urlparse, unquote
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site/dashboard'
DATA=json.loads((ROOT/'data/ledger.json').read_text())
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=[];self.rows=[];self.title=False;self.viewport=False
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if d.get('id'):self.ids.append(d['id'])
        if tag in ['a','link','script','img']:
            url=d.get('href') or d.get('src')
            if url:self.links.append(url)
        if tag=='tr' and d.get('data-id'):self.rows.append(d['data-id'])
        if tag=='title':self.title=True
        if tag=='meta' and d.get('name')=='viewport':self.viewport=True
class SiteTests(unittest.TestCase):
    def test_published_root_matches_build(self):
        for generated in list(SITE.rglob('*.html'))+[SITE/'.nojekyll',SITE/'data/ledger.csv']:
            self.assertEqual(generated.read_bytes(),(ROOT/'dashboard'/generated.relative_to(SITE)).read_bytes(),generated)
    def test_all_original_records_retained(self):
        original=json.loads((ROOT/'research/upstream.json').read_text())
        ids=[r['id'] for r in DATA['rows']]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len(ids),216)
        self.assertEqual(len(original['listings']),206)
        self.assertEqual(len(DATA['historicalExclusions']),45)
        self.assertTrue(set(x['id'] for x in original['listings'])<=set(ids))
    def test_every_populated_field_has_official_evidence(self):
        for row in DATA['rows']:
            self.assertIn(row['category'],{c['id'] for c in DATA['categories']})
            self.assertTrue(row.get('candidates') or row.get('checkedSource'))
            for key,field in row['fields'].items():
                if field is None:
                    self.assertIn(key,row['missing']);continue
                self.assertIsInstance(field['value'],str)
                self.assertTrue(field['value']);self.assertTrue(field['sources'])
                for source in field['sources']:
                    self.assertIn(source,DATA['sources'])
                    self.assertEqual(DATA['sources'][source]['checked'],'2026-11-01')
                    self.assertTrue(DATA['sources'][source]['excerpts'])
                    self.assertTrue(DATA['sources'][source]['url'].startswith('https://'))
                if field.get('date'):self.assertRegex(field['date'],r'^\d{4}-\d{2}-\d{2}$')
    def test_no_inherited_operational_claims(self):
        curated=json.loads((ROOT/'data/findings.json').read_text())
        for r in DATA['rows']:
            if r['origin']=='upstream':
                known=curated['updates'].get(r['id'],{}).get('fields',{})
                self.assertEqual({k:v for k,v in r['fields'].items() if v},known)
    def test_free_cash_has_both_facts_no_equivalent(self):
        qualified=[r for r in DATA['rows'] if r['freeCash']]
        self.assertEqual(len(qualified),6)
        for r in qualified:
            self.assertTrue(r['fields']['entry']['value'].startswith('Free'))
            self.assertIs(r['fields']['prize']['cash'],True)
            self.assertNotEqual(r['category'],'forecasting')
    def test_all_internal_links_assets_and_fragments(self):
        docs={p:None for p in SITE.rglob('*.html')}
        self.assertEqual(len(docs),17)
        for p in docs:
            parser=Links();parser.feed(p.read_text());docs[p]=parser
            self.assertTrue(parser.title);self.assertTrue(parser.viewport)
            self.assertEqual(len(parser.ids),len(set(parser.ids)),p)
        for p,doc in docs.items():
            for url in doc.links:
                parsed=urlparse(url)
                if parsed.scheme:
                    self.assertEqual(parsed.scheme,'https',url)
                    self.assertNotIn('www.skillz.com/terms-of-service/',url)
                    continue
                target=(p.parent/unquote(parsed.path)).resolve() if parsed.path else p
                if not target.is_relative_to(SITE.resolve()):
                    target=(ROOT/'dashboard'/p.relative_to(SITE).parent/unquote(parsed.path)).resolve()
                    self.assertTrue(target.is_relative_to(ROOT.resolve()),url)
                self.assertTrue(target.exists(),f'{p}: {url}')
                if parsed.fragment and target in docs:self.assertIn(unquote(parsed.fragment),docs[target].ids,f'{p}: {url}')
    def test_category_page_membership(self):
        for c in DATA['categories']:
            p=Links();p.feed((SITE/'categories'/f'{c["id"]}.html').read_text())
            self.assertEqual(set(p.rows),{r['id'] for r in DATA['rows'] if r['category']==c['id']})
    def test_review_queue_published(self):
        p=Links();p.feed((SITE/'review.html').read_text())
        self.assertEqual(set(p.rows),{r['id'] for r in DATA['rows'] if r['flags']})
    def test_csv_unknowns_genuinely_empty(self):
        with (SITE/'data/ledger.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),216)
        for exported,record in zip(rows,DATA['rows']):
            for field,value in record['fields'].items():
                self.assertEqual(exported[field],value['value'] if value else '')
    def test_source_records_and_security(self):
        for row in DATA['rows']:
            for url in row['candidates']:
                self.assertEqual(urlparse(url).scheme,'https')
        page=(SITE/'sources.html').read_text()
        self.assertNotIn('<img src=x',page)
        self.assertEqual(len(DATA['sources']),31)
if __name__=='__main__':unittest.main()
