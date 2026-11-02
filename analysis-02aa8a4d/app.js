/* analysis-02aa8a4d — progressive enhancement: table filter */
(function () {
  "use strict";
  document.querySelectorAll("input[data-filter]").forEach(function (input) {
    var table = document.getElementById(input.getAttribute("data-filter"));
    if (!table) return;
    var rows = Array.prototype.slice.call(table.querySelectorAll("tbody tr"));
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      rows.forEach(function (row) {
        var hay = row.getAttribute("data-search") || row.textContent.toLowerCase();
        row.hidden = q !== "" && hay.toLowerCase().indexOf(q) === -1;
      });
    });
  });
})();
