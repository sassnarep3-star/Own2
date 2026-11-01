'use strict';
(() => {
  document.body.classList.add('js');
  const menu = document.querySelector('#menu');
  const sidebar = document.querySelector('#sidebar');
  const closeMenu = () => { sidebar?.classList.remove('open'); menu?.setAttribute('aria-expanded', 'false'); };
  menu?.addEventListener('click', () => {
    const open = sidebar.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { closeMenu(); menu?.focus(); } });
  document.addEventListener('click', e => { if (sidebar?.classList.contains('open') && !sidebar.contains(e.target) && !menu?.contains(e.target)) closeMenu(); });

  const panel = document.querySelector('#explorer');
  if (!panel) return;
  const rows = [...panel.querySelectorAll('tbody > tr')];
  rows.forEach((row, index) => { row.dataset.order = index; });
  const search = panel.querySelector('#search');
  const category = panel.querySelector('#category');
  const evidence = panel.querySelector('#evidence-filter');
  const sort = panel.querySelector('#sort');
  const tabs = [...panel.querySelectorAll('[data-view]')];
  const storageKey = 'prize-ledger-saved-v1';
  let saved = new Set();
  let memoryOnly = false;
  try {
    const parsed = JSON.parse(localStorage.getItem(storageKey) || '[]');
    saved = new Set(Array.isArray(parsed) ? parsed.filter(x => typeof x === 'string') : []);
  } catch { memoryOnly = true; }
  let view = panel.dataset.mode === 'saved' ? 'saved' : 'all';
  let page = 1;
  const perPage = 20;
  const locked = panel.dataset.categoryLock;
  const params = new URLSearchParams(location.search);
  search.value = params.get('q') || '';
  if (params.get('view') === 'free') view = 'free';
  if (params.get('view') === 'saved') view = 'saved';
  if (locked) { category.value = locked; category.disabled = true; }
  else if ([...category.options].some(o => o.value === params.get('category'))) category.value = params.get('category');
  if ([...evidence.options].some(o => o.value === params.get('evidence'))) evidence.value = params.get('evidence');
  if ([...sort.options].some(o => o.value === params.get('sort'))) sort.value = params.get('sort');

  function synchronizeSaved() {
    panel.querySelectorAll('[data-save]').forEach(button => {
      const active = saved.has(button.dataset.save);
      button.hidden = false;
      button.setAttribute('aria-pressed', String(active));
      button.textContent = active ? '★' : '☆';
      const name = button.closest('tr').querySelector('.row-name').textContent;
      button.setAttribute('aria-label', (active ? 'Unsave ' : 'Save ') + name);
    });
    panel.querySelector('[data-count="saved"]').textContent = rows.filter(r => saved.has(r.dataset.id)).length;
  }
  function updateURL() {
    const p = new URLSearchParams();
    if (search.value) p.set('q', search.value);
    if (category.value && !locked) p.set('category', category.value);
    if (evidence.value !== 'all') p.set('evidence', evidence.value);
    if (sort.value !== 'research') p.set('sort', sort.value);
    if (view !== 'all') p.set('view', view);
    // Preserve an evidence deep link while its row is explicitly targeted.
    const entry = new URLSearchParams(location.search).get('entry');
    if (entry) p.set('entry', entry);
    try { history.replaceState(null, '', location.pathname + (p.size ? '?' + p.toString() : '') + location.hash); } catch { /* file:// preview */ }
  }
  function render() {
    const query = search.value.trim().toLocaleLowerCase();
    let matches = rows.filter(row => {
      const d = row.dataset;
      return (!query || d.search.includes(query)) &&
        (!category.value || d.category === category.value) &&
        (view !== 'free' || d.free === 'true') &&
        (view !== 'saved' || saved.has(d.id)) &&
        (evidence.value !== 'checked' || d.checked === 'true') &&
        (evidence.value !== 'unverified' || d.checked === 'false') &&
        (evidence.value !== 'ai' || d.ai === 'true');
    });
    matches.sort((a,b) => {
      if (sort.value === 'name') return a.querySelector('.row-name').textContent.localeCompare(b.querySelector('.row-name').textContent);
      if (sort.value === 'deadline') return (a.dataset.date || '9999').localeCompare(b.dataset.date || '9999');
      return Number(a.dataset.order) - Number(b.dataset.order);
    });
    const pages = Math.max(1, Math.ceil(matches.length / perPage));
    page = Math.min(Math.max(1, page), pages);
    const shown = new Set(matches.slice((page - 1) * perPage, page * perPage));
    // Maintain the chosen order in the actual DOM for keyboard and screen-reader users.
    const body = panel.querySelector('tbody');
    matches.forEach(row => body.append(row));
    rows.forEach(row => { row.hidden = !shown.has(row); });
    panel.querySelector('#empty').hidden = matches.length > 0;
    const start = matches.length ? (page - 1) * perPage + 1 : 0;
    const end = Math.min(page * perPage, matches.length);
    panel.querySelector('#result-count').textContent = `Showing ${start}–${end} of ${matches.length} opportunities${memoryOnly ? ' · saves are temporary in this browser' : ''}`;
    panel.querySelector('#page-number').textContent = `${page} / ${pages}`;
    panel.querySelector('#prev').disabled = page <= 1;
    panel.querySelector('#next').disabled = page >= pages;
    tabs.forEach(tab => tab.setAttribute('aria-pressed', String(tab.dataset.view === view)));
    updateURL();
  }
  tabs.forEach(tab => tab.addEventListener('click', () => { view = tab.dataset.view; page = 1; render(); }));
  [category, evidence, sort].forEach(control => control.addEventListener('change', () => { page = 1; render(); }));
  search.addEventListener('input', () => { page = 1; render(); });
  panel.querySelector('#reset').addEventListener('click', () => {
    search.value = ''; category.value = locked || ''; evidence.value = 'all'; sort.value = 'research'; view = panel.dataset.mode === 'saved' ? 'saved' : 'all'; page = 1;
    try { history.replaceState(null, '', location.pathname); } catch {}
    render();
  });
  panel.querySelector('#prev').addEventListener('click', () => { page--; render(); panel.querySelector('h2').scrollIntoView({block:'start'}); });
  panel.querySelector('#next').addEventListener('click', () => { page++; render(); panel.querySelector('h2').scrollIntoView({block:'start'}); });
  panel.addEventListener('click', e => {
    const button = e.target.closest('[data-save]');
    if (!button) return;
    const id = button.dataset.save;
    if (saved.has(id)) saved.delete(id); else saved.add(id);
    try { localStorage.setItem(storageKey, JSON.stringify([...saved])); } catch { memoryOnly = true; }
    synchronizeSaved(); render();
  });
  window.addEventListener('storage', e => {
    if (e.key !== storageKey) return;
    try { const value = JSON.parse(e.newValue || '[]'); saved = new Set(Array.isArray(value) ? value.filter(x => typeof x === 'string') : []); } catch { saved = new Set(); }
    synchronizeSaved(); render();
  });
  panel.querySelector('.interactive').hidden = false;
  panel.querySelector('.pagination').hidden = false;
  synchronizeSaved();
  const target = params.get('entry');
  const targetRow = rows.find(r => r.dataset.id === target);
  if (targetRow) {
    search.value = ''; category.value = locked || ''; evidence.value = 'all'; sort.value = 'research'; view = 'all';
    // Research-order deep links reach their page without trusting input as a selector or HTML.
    const idx = rows.indexOf(targetRow);
    page = Math.floor(idx / perPage) + 1;
    targetRow.querySelector('details').open = true;
  }
  render();
  if (targetRow && !targetRow.hidden) targetRow.scrollIntoView({block:'center'});
})();
