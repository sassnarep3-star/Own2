/* PrizeDesk client behaviour: filter, sort, and expand evidence rows.
   The page is fully readable without this file; this only adds convenience. */
(function () {
  "use strict";

  var rows = Array.prototype.slice.call(document.querySelectorAll("tr.r"));
  if (!rows.length) return;

  var q = document.getElementById("q");
  var fCat = document.getElementById("f-cat");
  var fVerdict = document.getElementById("f-verdict");
  var fFree = document.getElementById("f-free");
  var fCash = document.getElementById("f-cash");
  var fSort = document.getElementById("f-sort");
  var reset = document.getElementById("reset");
  var count = document.getElementById("count");
  var empty = document.querySelector(".empty");
  var wrap = rows[0].closest("tbody");

  function detailOf(row) {
    return document.getElementById("ev-" + row.getAttribute("data-row"));
  }

  function matches(row) {
    var term = q ? q.value.trim().toLowerCase() : "";
    if (term) {
      var hay = row.getAttribute("data-search") || "";
      if (hay.indexOf(term) === -1) return false;
    }
    if (fCat && fCat.value && row.getAttribute("data-cat") !== fCat.value) return false;
    if (fVerdict && fVerdict.value && row.getAttribute("data-verdict") !== fVerdict.value) return false;
    if (fFree && fFree.value && row.getAttribute("data-free") !== fFree.value) return false;
    if (fCash && fCash.value && row.getAttribute("data-cash") !== fCash.value) return false;
    return true;
  }

  function applySort() {
    var mode = fSort ? fSort.value : "";
    if (!mode) {
      rows.forEach(function (row) {
        var d = detailOf(row);
        wrap.appendChild(row);
        if (d) wrap.appendChild(d);
      });
      return;
    }
    var sorted = rows.slice().sort(function (a, b) {
      if (mode === "prize") {
        return (Number(b.getAttribute("data-prize")) || 0) - (Number(a.getAttribute("data-prize")) || 0);
      }
      if (mode === "deadline") {
        return (a.getAttribute("data-deadline") || "").localeCompare(b.getAttribute("data-deadline") || "");
      }
      return (a.getAttribute("data-name") || "").localeCompare(b.getAttribute("data-name") || "");
    });
    sorted.forEach(function (row) {
      var d = detailOf(row);
      wrap.appendChild(row);
      if (d) wrap.appendChild(d);
    });
  }

  function apply() {
    var shown = 0;
    rows.forEach(function (row) {
      var ok = matches(row);
      row.hidden = !ok;
      var d = detailOf(row);
      if (d) d.hidden = true;           /* collapse when filtering to avoid stale open panels */
      if (ok) shown += 1;
    });
    if (empty) empty.hidden = shown !== 0;
    if (count) {
      count.textContent = shown === rows.length
        ? "Showing all " + rows.length + " competitions."
        : "Showing " + shown + " of " + rows.length + " competitions.";
    }
  }

  [q, fCat, fVerdict, fFree, fCash].forEach(function (el) {
    if (el) el.addEventListener("input", apply);
  });
  if (fSort) fSort.addEventListener("change", function () { applySort(); apply(); });
  if (reset) {
    reset.addEventListener("click", function () {
      if (q) q.value = "";
      [fCat, fVerdict, fFree, fCash, fSort].forEach(function (el) { if (el) el.value = ""; });
      applySort();
      apply();
      if (q) q.focus();
    });
  }

  document.addEventListener("click", function (e) {
    var trigger = e.target.closest("[data-toggle]");
    if (!trigger) return;
    var id = trigger.getAttribute("data-toggle");
    var row = document.querySelector('tr.r[data-row="' + id + '"]');
    var detail = document.getElementById("ev-" + id);
    if (!row || !detail) return;
    e.preventDefault();
    var opening = detail.hidden;
    detail.hidden = !opening;
    Array.prototype.forEach.call(row.querySelectorAll('[data-toggle="' + id + '"]'), function (b) {
      if (b.tagName === "BUTTON") b.setAttribute("aria-expanded", String(opening));
    });
    if (opening) detail.scrollIntoView({ block: "nearest" });
  });

  apply();

  /* Deep link: contests.html#<id> opens that row's evidence panel. */
  function openHash() {
    var id = (location.hash || "").replace("#", "");
    if (!id) return;
    var row = document.querySelector('tr.r[data-row="' + id + '"]');
    var detail = document.getElementById("ev-" + id);
    if (!row) return;
    if (row.hidden) { if (q) q.value = ""; apply(); }
    if (detail) {
      detail.hidden = false;
      var btn = row.querySelector("button.more");
      if (btn) btn.setAttribute("aria-expanded", "true");
      row.scrollIntoView({ block: "start" });
    }
  }
  window.addEventListener("hashchange", openHash);
  openHash();
})();
