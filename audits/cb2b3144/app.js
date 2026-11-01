(() => {
  'use strict';
  const table = document.querySelector('table');
  const q = document.getElementById('q');
  if (!table || !q) return;
  const cat = document.getElementById('cat');
  const flagged = document.getElementById('flagged-only');
  const count = document.getElementById('count');
  const rows = Array.from(table.tBodies[0].rows);
  function filter() {
    const query = q.value.trim().toLowerCase();
    let visible = 0;
    rows.forEach(row => {
      const match = (!query || row.textContent.toLowerCase().includes(query)) &&
        (!cat.value || row.dataset.category === cat.value) &&
        (!flagged.checked || !!row.querySelector('.badge.warn'));
      row.hidden = !match;
      if (match) visible++;
    });
    count.textContent = `${visible} of ${rows.length} findings shown`;
  }
  q.addEventListener('input', filter);
  cat.addEventListener('change', filter);
  flagged.addEventListener('change', filter);
  filter();
})();
