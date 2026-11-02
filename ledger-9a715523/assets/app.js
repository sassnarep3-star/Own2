/* Progressive enhancement only: all rows and official links exist in static HTML. */
(() => {
  'use strict';
  const KEY = 'prizelens-9a715523-saved';
  const PAGE_SIZE = 25;
  let saved = new Set();
  try { const x = JSON.parse(localStorage.getItem(KEY) || '[]'); if (Array.isArray(x)) saved = new Set(x.filter(v => typeof v === 'string')); } catch (_) {}
  const persist = () => { try { localStorage.setItem(KEY, JSON.stringify([...saved])); } catch (_) {} };
  const syncSaves = () => document.querySelectorAll('[data-save]').forEach(b => {
    const on = saved.has(b.dataset.save); b.hidden = false; b.setAttribute('aria-pressed', String(on));
    b.textContent = on ? '★' : '☆'; b.title = on ? 'Remove from saved' : 'Save competition';
  });
  document.addEventListener('click', ev => {
    const b = ev.target.closest('[data-save]'); if (!b) return;
    const id = b.dataset.save; saved.has(id) ? saved.delete(id) : saved.add(id); persist(); syncSaves();
    document.querySelectorAll('table.catalog-table').forEach(t => { if (t._refresh) t._refresh(); });
  });
  const csvCell = v => '"' + String(v ?? '').replaceAll('"', '""') + '"';
  function exportVisible(table, visible) {
    const headers = [...table.querySelectorAll('thead th')].map(x => x.textContent.trim());
    const lines = [headers.map(csvCell).join(',')];
    visible.forEach(row => lines.push([...row.cells].map(cell => {
      const clone = cell.cloneNode(true); clone.querySelectorAll('button,.entry-links,.provenance').forEach(n => n.remove());
      return csvCell(clone.textContent.replace(/\s+/g, ' ').trim());
    }).join(',')));
    const blob = new Blob(['\ufeff' + lines.join('\r\n')], {type:'text/csv;charset=utf-8'});
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'prizelens-visible.csv'; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }
  document.querySelectorAll('table.catalog-table').forEach(table => {
    const id = table.id, all = [...table.tBodies[0].rows], mode = id;
    const search = document.getElementById(id+'-search'), category = document.getElementById(id+'-category'), status = document.getElementById(id+'-status'), agent = document.getElementById(id+'-agent');
    const count = document.querySelector(`[data-count="${id}"]`), empty = document.querySelector(`[data-empty="${id}"]`), pagination = document.querySelector(`[data-pagination="${id}"]`);
    const pageLabel = document.querySelector(`[data-page="${id}"]`), prev = document.querySelector(`[data-prev="${id}"]`), next = document.querySelector(`[data-next="${id}"]`);
    let page = 0, visible = [];
    function refresh(reset = true) {
      if (reset) page = 0;
      const q = (search?.value || '').trim().toLowerCase();
      const matched = all.filter(r => (!q || r.dataset.search.includes(q)) && (!category?.value || r.dataset.category === category.value) && (!agent?.value || r.dataset.agent === agent.value) && (!status?.value || (status.value === 'shortlist' ? r.dataset.shortlist === 'true' : status.value === 'saved' ? saved.has(r.id) : r.dataset.status === status.value)) && (mode !== 'saved' || saved.has(r.id)));
      const pages = Math.max(1, Math.ceil(matched.length / PAGE_SIZE)); page = Math.min(page, pages-1);
      all.forEach(r => r.hidden = true); visible = matched.slice(page*PAGE_SIZE,(page+1)*PAGE_SIZE); visible.forEach(r => r.hidden = false);
      if (count) count.textContent = `${matched.length} record${matched.length === 1 ? '' : 's'}${mode === 'saved' && !saved.size ? ' · save a row to build your list' : ''}`;
      if (empty) empty.hidden = matched.length > 0;
      table.closest('.table-shell').hidden = matched.length === 0;
      if (pagination) pagination.hidden = matched.length <= PAGE_SIZE;
      if (pageLabel) pageLabel.textContent = `Page ${page+1} of ${pages}`;
      if (prev) prev.disabled = page === 0; if (next) next.disabled = page >= pages-1;
    }
    table._refresh = () => refresh(false);
    [search,category,status,agent].forEach(el => el?.addEventListener('input', () => refresh(true)));
    document.querySelector(`[data-reset="${id}"]`)?.addEventListener('click', () => { if(search) search.value=''; if(category) category.value=''; if(status) status.value=''; if(agent) agent.value=''; refresh(); });
    document.querySelector(`[data-export="${id}"]`)?.addEventListener('click', () => {
      const q=(search?.value||'').trim().toLowerCase();
      const matched=all.filter(r => (!q || r.dataset.search.includes(q)) && (!category?.value || r.dataset.category===category.value) && (!agent?.value || r.dataset.agent===agent.value) && (!status?.value || (status.value==='shortlist' ? r.dataset.shortlist==='true' : status.value==='saved' ? saved.has(r.id) : r.dataset.status===status.value)) && (mode!=='saved' || saved.has(r.id)));
      exportVisible(table,matched);
    });
    prev?.addEventListener('click', () => { page--; refresh(false); table.closest('.catalog-panel')?.scrollIntoView({block:'start'}); });
    next?.addEventListener('click', () => { page++; refresh(false); table.closest('.catalog-panel')?.scrollIntoView({block:'start'}); });
    refresh();
  });
  const fs=document.getElementById('flag-search');
  if (fs) fs.addEventListener('input', () => {
    const q=fs.value.trim().toLowerCase(); let n=0;
    document.querySelectorAll('#flag-table tbody tr').forEach(r => { const show=!q||r.textContent.toLowerCase().includes(q); r.hidden=!show; if(show)n++; });
    document.getElementById('flag-count').textContent=`${n} records`; document.getElementById('flag-empty').hidden=n>0; document.getElementById('flag-table').closest('.table-shell').hidden=n===0;
  });
  syncSaves();
})();
