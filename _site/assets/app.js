// Small progressive enhancement: search, verification filter, category filter.
// The site works without JavaScript; these only hide rows.
(function () {
  function applyFilters(table) {
    var id = table.id;
    var q = (document.querySelector('[data-filter="' + id + '"]') || {}).value || '';
    q = q.trim().toLowerCase();
    var v = (document.querySelector('[data-verif-filter="' + id + '"]') || {}).value || '';
    var c = (document.querySelector('[data-cat-filter="' + id + '"]') || {}).value || '';
    var shown = 0;
    Array.prototype.forEach.call(table.tBodies[0].rows, function (tr) {
      var ok = true;
      if (q && (tr.getAttribute('data-search') || '').indexOf(q) === -1) ok = false;
      if (v && tr.getAttribute('data-verif') !== v) ok = false;
      if (c && tr.getAttribute('data-cat') !== c) ok = false;
      tr.hidden = !ok;
      if (ok) shown++;
    });
    var count = document.querySelector('[data-count-for="' + id + '"]');
    if (count) count.textContent = shown + ' of ' + table.tBodies[0].rows.length + ' rows';
  }
  document.querySelectorAll('[data-table]').forEach(function (table) {
    // Category filter needs a data-cat attribute on each row; derive it from the Category cell if present.
    Array.prototype.forEach.call(table.tBodies[0].rows, function (tr) {
      if (!tr.hasAttribute('data-cat')) {
        var id = tr.getAttribute('id') || '';
        var t = tr.getAttribute('data-type');
        if (t) tr.setAttribute('data-cat', t);
      }
    });
    var inputs = document.querySelectorAll('[data-filter="' + table.id + '"],[data-verif-filter="' + table.id + '"],[data-cat-filter="' + table.id + '"]');
    Array.prototype.forEach.call(inputs, function (el) {
      el.addEventListener('input', function () { applyFilters(table); });
      el.addEventListener('change', function () { applyFilters(table); });
    });
    applyFilters(table);
  });
})();
