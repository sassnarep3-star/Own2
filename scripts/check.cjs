const fs=require('node:fs'),path=require('node:path');
const d=JSON.parse(fs.readFileSync('data/catalog.json','utf8'));
const assert=(ok,message)=>{if(!ok)throw Error(message)};
assert(d.listings.length===206,'Source listing count changed');
assert(new Set(d.listings.map(x=>x.id)).size===206,'Duplicate IDs');
assert(d.categories.length===9,'Unexpected category count');
const validUrl=x=>!x||/^https:\/\/[^/\s]+/.test(x);
for(const x of [...d.listings,...d.opportunities]){
  assert(d.categories.some(c=>c.id===x.category),`Unknown category ${x.id}`);
  assert(validUrl(x.operatorUrl)&&validUrl(x.claimedRulesUrl)&&validUrl(x.rulesUrl),`Invalid URL ${x.id}`);
  assert(x.operatorUrl||x.claimedRulesUrl||x.rulesUrl,`No operator link ${x.id}`);
  if(x.verification==='unverified')assert(!x.prize&&!x.entry&&!x.deadline&&!x.eligibility,`Unsupported assertion ${x.id}`);
  if(x.verification==='confirmed')assert(x.rulesUrl&&x.prize&&x.entry,`Missing evidence ${x.id}`);
}
const pages=['index.html','flagged/index.html',...d.categories.map(c=>`category/${c.id}.html`)];
for(const file of pages){const html=fs.readFileSync(file,'utf8'); assert(html.includes('<meta name="viewport"'),`No viewport: ${file}`);for(const m of html.matchAll(/(?:href|src)="([^"]+)"/g)){const u=m[1];if(u.startsWith('http')||u.startsWith('#'))continue;const [rel]=u.split('#');if(!rel)continue;assert(fs.existsSync(path.resolve(path.dirname(file),rel)),`Broken local link ${file}: ${u}`);}}
assert(pages.length===11,'Missing page');
console.log(`PASS: ${pages.length} pages, ${d.listings.length} flagged source records, ${d.opportunities.length} individually checked opportunities; local links resolve.`);
