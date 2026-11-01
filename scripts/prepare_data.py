"""Normalize the upstream inventory without promoting its claims to verified facts.
Curated field values and evidence live in data/findings.json, not this importer.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def prepare():
    upstream=json.loads((ROOT/'research/upstream.json').read_text())
    curated=json.loads((ROOT/'data/findings.json').read_text())
    fields=['entry','prize','deadline','eligibility','ai','payout','requirements']
    rows=[]
    for item in upstream['listings']:
        candidates=[]
        for url in [item.get('rulesUrl'),item.get('signupUrl')]+[s['url'] for s in item.get('sources',[]) if s.get('tier')=='official']:
            if url and url not in candidates: candidates.append(url)
        row={'id':item['id'],'name':item['name'],'category':item['type'],'origin':'upstream','candidates':candidates,'listedOperator':item['signupUrl'],'fields':{f:None for f in fields},'flags':[]}
        patch=curated['updates'].get(item['id'],{})
        row.update({k:v for k,v in patch.items() if k!='fields'})
        row['fields'].update(patch.get('fields',{}))
        if not any(s.get('tier')=='official' for s in item.get('sources',[])):
            row['flags'].append('No source explicitly tagged official in the upstream source list. The inherited signup/rules link is a candidate only; authority remains unverified.')
        rows.append(row)
    for row in curated['additions']:
        row['origin']='research'; row.setdefault('candidates',[]); row.setdefault('flags',[])
        row['fields']={f:row.get('fields',{}).get(f) for f in fields}
        rows.append(row)
    for row in rows:
        row['missing']=[f for f in fields if not row['fields'][f]]
        if row['missing']: row['flags'].append('Unverified fields: '+', '.join(row['missing'])+'. Values intentionally blank.')
        if not any(row['fields'].values()): row['flags'].insert(0,'Imported discovery lead only. Current official rules and link destinations have not been independently verified.')
        row['freeCash']=bool(row['fields']['entry'] and row['fields']['entry']['value'].startswith('Free') and row['fields']['prize'] and row['fields']['prize'].get('cash'))
        row['monetaryMatch']=row['freeCash']
        if row['fields']['payout'] and 'cash equivalent' in row['fields']['payout']['value'].lower():
            row['freeCash']=False # explicit cash-equivalent substitution is not guaranteed cash
        row['checked']=bool(row.get('checkedSource')) or any(row['fields'].values())
    return {'asOf':'2026-11-01','upstreamCommit':'466f7c1e7a14b52b4a0d36beb84a00d68fd409b7','categories':[{ 'id':t['id'],'name':t['name']} for t in upstream['types']], 'sources':curated['sources'],'rows':rows,'historicalExclusions':upstream['removedThisPass']}
if __name__=='__main__':
    (ROOT/'data/ledger.json').write_text(json.dumps(prepare(),indent=2,ensure_ascii=False)+'\n')
