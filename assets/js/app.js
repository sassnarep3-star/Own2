/* Own2 dashboard — client-side filter, sort, search. No external dependencies. */
(function () {
  var entries = window.__OWN2_ENTRIES || [];
  var tbody = document.getElementById("entries");
  var tmpl = document.getElementById("row-template");
  var countEl = document.getElementById("count");
  var activeFilters = { type: "", status: "", path: "", q: "" };
  var sortKey = null;
  var sortDir = 1;

  function esc(t) {
    return String(t == null ? "" : t)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function badge(kind, value) {
    if (!value) return "";
    var cls = "b-" + kind + "-" + String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-");
    return "<span class=\"badge " + cls + "\">" + esc(value) + "</span>";
  }

  function platforms(e) {
    var p = e.platformLabels || [];
    return p.map(function (x) { return "<span class=\"badge b-platform\">" + esc(x) + "</span>"; }).join(" ");
  }

  function sourcesHtml(e) {
    var out = [];
    (e.sources || []).forEach(function (s) {
      var tier = (s.tier || "").toLowerCase();
      var cls = tier === "official" ? "tier-official" : tier === "affiliate" ? "tier-affiliate" : "tier-forum";
      out.push("<span class=\"tier-tag " + cls + "\">" + esc(tier) + "</span>"
        + "<a href=\"" + esc(s.url) + "\" target=\"_blank\" rel=\"noopener\">" + esc(s.title || s.url) + "</a>");
    });
    return out.join("<br>");
  }

  function render() {
    var q = activeFilters.q.toLowerCase();
    var filtered = entries.filter(function (e) {
      if (activeFilters.type && e.type !== activeFilters.type) return false;
      if (activeFilters.status && e.status !== activeFilters.status) return false;
      if (activeFilters.path && e.freePath !== activeFilters.path) return false;
      if (q && !(e.name.toLowerCase().indexOf(q) > -1
        || e.typeLabel.toLowerCase().indexOf(q) > -1
        || (e.short || "").toLowerCase().indexOf(q) > -1
        || (e.prizeUsd || "").toLowerCase().indexOf(q) > -1)) return false;
      return true;
    });

    if (sortKey) {
      filtered.sort(function (a, b) {
        var av = a[sortKey] == null ? "" : String(a[sortKey]).toLowerCase();
        var bv = b[sortKey] == null ? "" : String(b[sortKey]).toLowerCase();
        return av < bv ? -sortDir : av > bv ? sortDir : 0;
      });
    }

    if (countEl) countEl.textContent = filtered.length + " of " + entries.length;
    tbody.innerHTML = "";
    filtered.forEach(function (e) {
      var row = document.createElement("tr");
      if (e.unverified) row.classList.add("flag-row");
      row.innerHTML =
        "<td class=\"name\"><a href=\"" + esc(e.signupUrl) + "\" target=\"_blank\" rel=\"noopener\">" + esc(e.name) + "</a>"
        + (e.iosUrl ? "<br><a class=\"ios-link\" href=\"" + esc(e.iosUrl) + "\" target=\"_blank\" rel=\"noopener\">iOS app</a>" : "")
        + (e.unverified ? "<span class=\"flag-note\">UNVERIFIED — no official source</span>" : "") + "</td>"
        + "<td>" + esc(e.typeLabel) + "</td>"
        + "<td>" + badge("status", e.statusLabel) + "</td>"
        + "<td>" + badge("path", e.freePathLabel) + "</td>"
        + "<td>" + platforms(e) + "</td>"
        + "<td>" + (e.prizeUsd ? esc(e.prizeUsd) : "<span class=\"small\">— unverified</span>") + "</td>"
        + "<td>" + (e.minCashout ? esc(e.minCashout) : "<span class=\"small\">— unverified</span>") + "</td>"
        + "<td>" + (e.payoutText ? esc(e.payoutText) : "<span class=\"small\">— unverified</span>") + "</td>"
        + "<td>" + esc(e.eligibility || "—") + "</td>"
        + "<td>" + esc(e.restricted || "—") + "</td>"
        + "<td class=\"nowrap\">" + esc(e.lastChecked) + "</td>"
        + "<td class=\"source-cell\">" + (e.officialSourceUrl ? "<a href=\"" + esc(e.officialSourceUrl) + "\" target=\"_blank\" rel=\"noopener\">" + esc(e.officialSourceTitle || "Official site") + "</a>" : "<span class=\"small\">none found</span>")
        + (e.refSourceUrl ? "<br><span class=\"small\">Reference only (" + esc(e.refSourceTier) + "): <a href=\"" + esc(e.refSourceUrl) + "\" target=\"_blank\" rel=\"noopener\">" + esc(e.refSourceTitle) + "</a></span>" : "") + "</td>"
        + "<td>" + esc(e.verificationLevel || "—") + "</td>";
      tbody.appendChild(row);
    });
  }

  function addFilter(kind, label, value) {
    if (activeFilters[kind] === value) return;
    activeFilters[kind] = value;
    var bar = document.getElementById("filters-" + kind);
    if (!bar) return;
    bar.innerHTML = "";
    if (value) {
      var chip = document.createElement("div");
      chip.className = "filter active";
      chip.innerHTML = esc(label) + " <span class=\"x\" onclick=\"removeFilter('" + kind + "')\">✕</span>";
      bar.appendChild(chip);
    }
    render();
  }
  window.removeFilter = function (kind) {
    activeFilters[kind] = "";
    var bar = document.getElementById("filters-" + kind);
    if (bar) bar.innerHTML = "";
    render();
  };

  function sortBy(key) {
    if (sortKey === key) sortDir = -sortDir;
    else { sortKey = key; sortDir = 1; }
    render();
  }

  document.addEventListener("DOMContentLoaded", function () {
    render();
    var search = document.getElementById("search");
    if (search) {
      search.addEventListener("input", function () { activeFilters.q = this.value; render(); });
    }
    // expose sort for onclick in HTML
    window.sortBy = sortBy;
  });
})();
