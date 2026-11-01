'use strict';
const dataUrl = new URL('../data/catalog.json', document.currentScript.src);
const mode = document.body.dataset.view || 'home';
const cat = document.body.dataset.category || '';
const el = (tag, cls, text) => { const n = document.createElement(tag); if(cls)n.className=cls; if(text!=null)n.textContent=text; return n; };
function link(text, url) { const a=el('a','',text); a.href=url; if(/^https?:/.test(url)){a.target='_blank';a.rel='noopener noreferrer';} return a; }
function cell(label, content) { const td=el('td');td.dataset.label=label; if(content instanceof Node)td.append(content);else if(content)td.textContent=content;else td.append(el('span','empty','—'));return td; }
function row(item, kind) {
  const tr=el('tr');
  if(kind==='opportunity'){
    const name=el('span');name.append(link(item.name,item.operatorUrl),el('span','minor',item.fit));
    const evidence=el('span'); evidence.append(link('Rules ↗',item.rulesUrl),el('span','minor',item.evidence));
    tr.append(cell('Opportunity',name),cell('Entry',item.entry),cell('Prize',item.prize),cell('Deadline',item.deadline),cell('Eligibility',item.eligibility),cell('Official evidence',evidence));
  }else{
    const name=el('span');name.append(el('strong','',item.name),el('span','minor',item.id));
    const official=el('span'); if(item.claimedRulesUrl)official.append(link('Source-cited page ↗',item.claimedRulesUrl));
    else if(item.operatorUrl)official.append(link('Operator site ↗',item.operatorUrl));
    else official.append(el('span','empty','—'));
    if(item.operatorUrl && item.claimedRulesUrl && item.operatorUrl!==item.claimedRulesUrl) official.append(el('span','minor','Listed operator: '),link('Open ↗',item.operatorUrl));
    official.append(el('span','minor','Link carried over from source; not independently validated.'));
    tr.append(cell('Listing',name),cell('Prize',item.prize),cell('Free entry',item.entry),cell('Status',el('span','tag warn','Unverified')),cell('Issue',item.issue),cell('Official link',official),cell('Original record',link('Ledger ↗',item.provenance)));
  }
  return tr;
}
function buildTable(items,kind,container){
  const headings=kind==='opportunity'?['Opportunity','Entry','Prize','Deadline','Eligibility','Official evidence']:['Listing','Prize','Free entry','Status','Issue','Operator / source','Original record'];
  const wrap=el('div','table-scroll'),table=el('table'),thead=el('thead'),hrow=el('tr'),tbody=el('tbody');
  headings.forEach(h=>hrow.append(el('th','',h)));thead.append(hrow);items.forEach(x=>tbody.append(row(x,kind)));table.append(thead,tbody);wrap.append(table);container.append(wrap);return tbody;
}
fetch(dataUrl).then(r=>{if(!r.ok)throw Error('Data unavailable');return r.json()}).then(data=>{
  const count=id=>data.listings.filter(x=>x.category===id).length;
  document.querySelectorAll('[data-stat="catalog"]').forEach(n=>n.textContent=data.listings.length);
  document.querySelectorAll('[data-stat="confirmed"]').forEach(n=>n.textContent=data.opportunities.filter(x=>x.verification==='confirmed').length);
  document.querySelectorAll('[data-stat="partial"]').forEach(n=>n.textContent=data.opportunities.filter(x=>x.verification==='partial').length);
  const cards=document.querySelector('#category-cards'); if(cards)data.categories.forEach(c=>{const a=el('a','cat-card');a.href=`category/${c.id}.html`;a.append(el('span','count',`${count(c.id)} source listings →`),el('h3','',c.name),el('small','', 'Explore & review'));cards.append(a);});
  const active=cat?data.categories.find(c=>c.id===cat):null;
  if(cat&&!active)throw Error('Unknown category');
  if(active){document.querySelectorAll('[data-category-name]').forEach(n=>n.textContent=active.name);document.querySelectorAll('[data-category-count]').forEach(n=>n.textContent=count(cat));}
  const opportunities=document.querySelector('#opportunities');if(opportunities){const rows=mode==='home'?data.opportunities:data.opportunities.filter(x=>x.category===cat);buildTable(rows,'opportunity',opportunities);}
  const backlog=document.querySelector('#backlog');if(backlog){const items=mode==='flagged'?data.listings:data.listings.filter(x=>x.category===cat);const tbody=buildTable(items,'backlog',backlog);const input=document.querySelector('#search');const result=document.querySelector('#result-count');if(result)result.textContent=`${items.length} records`;
    if(input)input.addEventListener('input',()=>{const q=input.value.trim().toLocaleLowerCase();let visible=0;Array.from(tbody.children).forEach((tr,i)=>{const match=!q||`${items[i].name} ${items[i].id} ${items[i].issue}`.toLocaleLowerCase().includes(q);tr.hidden=!match;if(match)visible++;});if(result)result.textContent=`${visible} of ${items.length} records`;});}
}).catch(e=>{const target=document.querySelector('main');target.prepend(el('p','notice',`Catalog could not load: ${e.message}. Try refreshing the page.`));});
