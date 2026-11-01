/* Free Contest Ledger — tiny enhancement layer (filters only; all data renders without JS) */
(function () {
  var bar = document.querySelector('.filters[data-filter-for="ledger"]');
  if (!bar) return;
  var table = document.querySelector('table.ledger');
  if (!table) return;
  var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));
  var input = bar.querySelector('input[type="search"]');
  var selects = bar.querySelectorAll('select');
  var note = bar.querySelector('[data-count-note]');

  function apply() {
    var q = (input && input.value || '').trim().toLowerCase();
    var status = selects[0] ? selects[0].value : '';
    var free = selects[1] ? selects[1].value : '';
    var shown = 0;
    rows.forEach(function (tr) {
      var okQ = !q || (tr.getAttribute('data-name') || '').indexOf(q) !== -1 || tr.textContent.toLowerCase().indexOf(q) !== -1;
      var okS = !status || tr.getAttribute('data-status') === status;
      var okF = !free || tr.getAttribute('data-free') === free;
      var show = okQ && okS && okF;
      tr.style.display = show ? '' : 'none';
      if (show) shown++;
    });
    if (note) note.textContent = shown + ' / ' + rows.length + ' shown';
  }

  if (input) input.addEventListener('input', apply);
  selects.forEach(function (s) { s.addEventListener('change', apply); });
  apply();
})();
