/* Progressive enhancement. No remote APIs, analytics or user accounts. */
(async () => {
  'use strict';
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => [...document.querySelectorAll(s)];
  const prefix = document.body.dataset.prefix || '';
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const menu = $('.mobile-menu');
  menu?.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open)); $('#sidebar').classList.toggle('open', open);
  });
  document.addEventListener('click', e => {
    if (menu && !e.target.closest('#sidebar,.mobile-menu')) { $('#sidebar').classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); }
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { $('#sidebar').classList.remove('open'); menu?.setAttribute('aria-expanded','false'); }
  });
  let data;
  try { const res = await fetch(prefix + 'assets/catalog.json'); if (!res.ok) throw Error('Catalog unavailable'); data = await res.json(); }
  catch (_) { $$('.js-only').forEach(x => x.hidden = true); const count=$('#result-count'); if(count)count.textContent='Interactive data unavailable. The complete static table and source links remain available.'; return; }
  const rows = data.rows;
  const byId = new Map(rows.map(r => [r.id,r]));
  const catNames = Object.fromEntries(data.categories.map(c => [c.id,c.name]));
  const storageKey = 'own2-saved-v1';
  let saved = new Set();
  let storageAvailable = true;
  try { const raw = JSON.parse(localStorage.getItem(storageKey) || '[]'); if (Array.isArray(raw)) saved = new Set(raw.filter(id => byId.has(id))); }
  catch (_) { storageAvailable = false; }
  const toast = msg => { const el=$('.toast');el.textContent=msg;el.hidden=false;clearTimeout(toast.timer);toast.timer=setTimeout(()=>el.hidden=true,3000); };
  function saveButtons() {
    $$('[data-save]').forEach(b => { const on=saved.has(b.dataset.save);b.setAttribute('aria-pressed',String(on));b.textContent=on?'◆':'◇';b.setAttribute('aria-label',`${on?'Unsave':'Save'} ${byId.get(b.dataset.save).name}`); });
    if ($('#saved-count')) $('#saved-count').textContent=saved.size;
  }
  function toggleSave(id) {
    saved.has(id)?saved.delete(id):saved.add(id);
    try { localStorage.setItem(storageKey,JSON.stringify([...saved])); } catch (_) { storageAvailable=false; }
    saveButtons();applyFilters();
    toast(storageAvailable?'Research shortlist updated. Saved in this browser only.':'Shortlist updated for this visit. Browser storage is unavailable.');
  }
  let trigger;
  const dialog=$('#entry-dialog');
  const fieldNames={entryFee:'Entry fee / free path',prize:'Cash prize / pool',deadline:'Deadline',eligibility:'Eligibility & location',payout:'Payout method / conditions',aiPolicy:'AI and automation policy'};
  function openDetails(id,source) {
    const r=byId.get(id);if(!r)return;
    trigger=source;$('#dialog-title').textContent=r.name;
    const facts=Object.entries(fieldNames).map(([k,label])=>{
      const ev=r.evidence[k];
      return `<div class="fact"><dt>${esc(label)}</dt><dd>${r.facts[k]?esc(r.facts[k]):'<span class="unknown">— Unverified; no confirmed value</span>'}${ev?`<blockquote>${esc(ev.quote)}</blockquote><a href="${esc(ev.url)}" target="_blank" rel="noopener noreferrer">Official field source ↗</a><span class="entry-category">Checked ${esc(ev.checked)} · ${esc(ev.method)}</span>`:''}</dd></div>`;
    }).join('');
    const c=r.linkCheck;
    const check=c?`Operator URL: ${c.httpStatus?'HTTP '+esc(c.httpStatus):'network error'} · ${esc(c.checkedAt.slice(0,10))}${c.error?'<br>'+esc(c.error):''}${c.finalUrl&&c.finalUrl!==r.officialUrl?'<br>Redirect: '+esc(c.finalUrl):''}`:'No automated reachability result for this URL.';
    const extra=(r.additionalSources||[]).map(s=>`<li><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.label)} ↗</a><br>${esc(s.quote)}<span class="entry-category">Checked ${esc(s.checked)}</span></li>`).join('');
    $('#dialog-content').innerHTML=`<span class="badge ${r.reviewStatus==='partial'?'partial':''}">${r.reviewStatus==='partial'?'Partial official evidence':'Unverified imported listing'}</span> <span class="badge">${esc(catNames[r.category])}</span><p class="status-line">Audit snapshot: ${esc(data.auditDate)}. Not personal eligibility clearance.</p><dl>${facts}</dl><h3>Findings & open questions</h3><ul>${[...r.flags,...r.notes].map(n=>`<li>${esc(n)}</li>`).join('')}</ul>${extra?'<h3>Additional official evidence</h3><ul>'+extra+'</ul>':''}<p class="link-check">${check}<br>HTTP success is not claim verification. A failed request may be temporary or blocked.</p><div class="sources-list">${r.officialUrl?`<a class="button primary" href="${esc(r.officialUrl)}" target="_blank" rel="noopener noreferrer">Open operator source ↗</a>`:'<span class="badge blocked">Official operator source missing</span>'} <a class="button" href="${prefix}review/index.html">Review queue</a></div><p class="status-line">Unknown facts remain empty in the downloadable dataset. Imported names and categories are provenance labels, not verified contest claims.</p>`;
    dialog.showModal();
  }
  $('.close-dialog').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target===dialog){const b=dialog.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)dialog.close();}});
  dialog.addEventListener('close',()=>trigger?.focus());
  document.addEventListener('click',e=>{
    const detail=e.target.closest('[data-detail],[data-open]');
    if(detail){e.preventDefault();openDetails(detail.dataset.detail||detail.dataset.open,detail);}
    const save=e.target.closest('[data-save]');if(save)toggleSave(save.dataset.save);
  });
  let view=new URLSearchParams(location.search).get('view')||'all';
  if(!['all','shortlist','saved'].includes(view))view='all';
  const tbody=$('#entries');
  const domRows=tbody?[...tbody.querySelectorAll('tr')]:[];
  let visible=[];
  function applyFilters() {
    if(!tbody)return;
    const q=($('#search').value||'').trim().toLowerCase();
    const cat=$('#category').value;const status=$('#evidence').value;const free=$('#free').checked;
    visible=[];
    const sorted=[...domRows].sort((a,b)=>{
      const x=byId.get(a.dataset.id),y=byId.get(b.dataset.id);const sort=$('#sort').value;
      if(sort==='name')return x.name.localeCompare(y.name);
      if(sort==='deadline')return (x.facts.deadline||'9999').localeCompare(y.facts.deadline||'9999');
      return (x.priority||999)-(y.priority||999)||x.name.localeCompare(y.name);
    });
    for(const tr of sorted){
      const r=byId.get(tr.dataset.id);
      const text=[r.name,catNames[r.category],...Object.values(r.facts),...r.notes].join(' ').toLowerCase();
      const show=(!q||text.includes(q))&&(!cat||r.category===cat)&&(!status||r.reviewStatus===status)&&(!free||r.freeCash)&&(view!=='saved'||saved.has(r.id))&&(view!=='shortlist'||r.priority>0);
      tr.hidden=!show;tbody.append(tr);if(show)visible.push(r);
    }
    $('#empty').hidden=visible.length>0;
    $('#result-count').textContent=`Showing ${visible.length} of ${domRows.length} entries${view==='saved'?' · saved in this browser':view==='shortlist'?' · editorial research priorities':''} · unknown values are not estimates`;
    $$('[data-view]').forEach(a=>{if(a.dataset.view===view)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
    if(document.body.dataset.page==='all'){
      const nav=$$('.sidebar nav a');nav[0]?.classList.toggle('active',view!=='saved');nav[1]?.classList.toggle('active',view==='saved');
    }
  }
  if(tbody){
    ['#search','#category','#evidence','#sort','#free'].forEach(s=>$(s).addEventListener(s==='#search'?'input':'change',applyFilters));
    $('#reset').addEventListener('click',()=>{
      $('#search').value='';$('#category').value=document.body.dataset.category||'';$('#evidence').value='';$('#free').checked=false;$('#sort').value='default';view='all';
      const u=new URL(location);u.searchParams.delete('view');history.replaceState({},'',u);applyFilters();
    });
    $$('[data-view]').forEach(a=>a.addEventListener('click',e=>{
      // A category page's tabs navigate to the full directory instead of filtering its subset.
      if(document.body.dataset.category)return;
      e.preventDefault();view=a.dataset.view;const u=new URL(location);view==='all'?u.searchParams.delete('view'):u.searchParams.set('view',view);u.hash='directory';history.pushState({},'',u);applyFilters();
    }));
    addEventListener('popstate',()=>{view=new URLSearchParams(location.search).get('view')||'all';applyFilters();});
    $('#export').addEventListener('click',e=>{
      e.preventDefault();
      const fields=['id','name','category','entryFee','prize','deadline','eligibility','payout','aiPolicy','officialUrl','reviewStatus'];
      const cell=v=>'"'+String(v??'').replace(/"/g,'""')+'"';
      const lines=[fields.map(cell).join(','),...visible.map(r=>fields.map(k=>cell(r.facts[k]??r[k]??'')).join(','))];
      const blob=new Blob(['\uFEFF'+lines.join('\r\n')],{type:'text/csv;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='competition-desk-filtered.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    });
    applyFilters();
  }
  $('#review-search')?.addEventListener('input',()=>{
    const q=$('#review-search').value.trim().toLowerCase();let count=0;
    $$('[data-review]').forEach(tr=>{tr.hidden=!tr.dataset.review.includes(q);if(!tr.hidden)count++;});$('#review-count').textContent=`${count} entries need review`;
  });
  saveButtons();
  // Deep links work across filters without making official facts depend on JavaScript.
  const hash=decodeURIComponent(location.hash.slice(1));
  if(byId.has(hash))openDetails(hash,null);
})();
