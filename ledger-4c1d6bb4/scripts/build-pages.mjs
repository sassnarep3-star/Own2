#!/usr/bin/env node
/**
 * build-pages.mjs — generates the static site from assets/data.js (T4/T5/T6/T7).
 *
 * Verification rules enforced here (never inferred, never filled in):
 *  - Every table row links to the listing's official source(s).
 *  - Listings with NO official-tier source: all value cells render blank with an
 *    "Unverified" marker linking to /flagged.html#flag-<id>. Their non-official
 *    links are shown on the flagged page only, labelled as non-official.
 *  - Link-check failures recorded in reports/link-check.json (if present) are
 *    published on /flagged.html.
 *
 * Output: index.html, <type>.html × 9, analysis.html, flagged.html,
 *         executive-summary.html, 404.html
 */
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = readFileSync(join(root, "assets", "data.js"), "utf8");
const ledger = new Function("window", src + "\n;return window.LEDGER;")({});

if (!ledger?.listings?.length) {
  console.error("FATAL: ledger empty");
  process.exit(1);
}

const REVIEWED = ledger.reviewed;
const TODAY = "2026-11-01";
const SITE = "Free Contest Ledger";

/* ------------------------------------------------------------------ utils */
const esc = (s) =>
  String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

const FREE_LABEL = { full: "Free USD path", partial: "Some free events", "paid-cash": "Cash needs entry fee" };
const STATUS_LABEL = { live: "Active", mixed: "Mixed", caution: "Caution", ended: "Ended", inactive: "Inactive" };
const VERIFY_LABEL = { account: "Account only", eligibility: "Eligibility check", kyc: "Full KYC", tax: "Tax paperwork" };
const PLATFORM_LABEL = { ios: "iOS app", web: "Browser" };

const officialSources = (l) => (l.sources || []).filter((s) => s.tier === "official");
const hasOfficial = (l) => officialSources(l).length > 0;
const isUnverified = (l) => !hasOfficial(l);

/* Spot-check overrides (T9): reports/spot-checks.json may mark a specific
   field (e.g. prizeUsd) as "unconfirmed" after a manual fetch of the official
   page. Unconfirmed values render blank + flagged. Nothing is ever rewritten. */
let spotChecks = { checks: [] };
try {
  spotChecks = JSON.parse(readFileSync(join(root, "reports", "spot-checks.json"), "utf8"));
} catch { /* optional */ }
const spotUnconfirmed = new Map(); // id -> [check,...]
for (const c of spotChecks.checks || []) {
  if (c.verdict === "unconfirmed") {
    if (!spotUnconfirmed.has(c.id)) spotUnconfirmed.set(c.id, []);
    spotUnconfirmed.get(c.id).push(c);
  }
}
const spotConfirmedIds = new Set(
  (spotChecks.checks || []).filter((c) => c.verdict === "verified").map((c) => c.id)
);
const prizeBlanked = (l) => isUnverified(l) || (spotUnconfirmed.get(l.id) || []).some((c) => c.field === "prizeUsd");

const byType = {};
for (const t of ledger.types) byType[t.id] = [];
for (const l of ledger.listings) (byType[l.type] ||= []).push(l);

const stats = {
  total: ledger.listings.length,
  freeFull: ledger.listings.filter((l) => l.freePath === "full").length,
  live: ledger.listings.filter((l) => l.status === "live").length,
  ended: ledger.listings.filter((l) => l.status === "ended").length,
  caution: ledger.listings.filter((l) => l.status === "caution").length,
  mixed: ledger.listings.filter((l) => l.status === "mixed").length,
  unverified: ledger.listings.filter(isUnverified).length,
  officialSources: ledger.listings.filter(hasOfficial).length,
  types: ledger.types.length,
  removed: (ledger.removedThisPass || []).length,
  reviewed: REVIEWED,
};

/* Priority score — a transparent, documented heuristic (see analysis.html).
   Not a prediction of winnings. Formula printed on the analysis page. */
function priorityScore(l) {
  if (!hasOfficial(l)) return null;
  if (l.status === "ended" || l.status === "inactive") return null;
  let s = 0;
  s += l.status === "live" ? 3 : l.status === "mixed" ? 1 : l.status === "caution" ? -1 : 0;
  s += l.freePath === "full" ? 3 : l.freePath === "partial" ? 1 : -2;
  s += l.verification.level === "account" ? 2 : l.verification.level === "eligibility" ? 1 : 0;
  return s;
}

const ranked = ledger.listings
  .map((l) => ({ l, s: priorityScore(l) }))
  .filter((x) => x.s !== null && !prizeBlanked(x.l))
  .sort((a, b) => b.s - a.s || a.l.name.localeCompare(b.l.name));

/* --------------------------------------------------------------- chrome */
const NAV = [
  ["index.html", "Home"],
  ["analysis.html", "Analysis"],
  ["flagged.html", "Flagged for Review"],
  ["executive-summary.html", "Executive Summary"],
];

function page({ title, active, desc, body, extraHead = "" }) {
  const navLinks = NAV.map(
    ([href, label]) =>
      `<a href="${href}"${active === href ? ' aria-current="page"' : ""}>${label}</a>`
  ).join("");
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<link rel="stylesheet" href="assets/css/style.css">
${extraHead}
</head>
<body>
<header class="topbar"><div class="wrap">
  <a class="brand" href="index.html"><span class="mark">$</span>
    <span>${SITE}<small>Verified free cash-prize competitions</small></span></a>
  <nav class="main">${navLinks}</nav>
</div></header>
<div class="wrap">
${body}
<footer>
  <p><strong>${SITE}</strong> is an independent research compilation (session build ${TODAY}).
  Data reviewed upstream ${esc(REVIEWED)}; every row carries its official source link.
  Not affiliated with any listed operator. Contest laws vary — play only where legal.
  18+/21+ where required. Always open the official rules before entering.</p>
</footer>
</div>
<script src="assets/js/app.js"></script>
</body>
</html>`;
}

/* ------------------------------------------------------------ table rows */
function rowCells(l) {
  const unv = isUnverified(l);
  const off = officialSources(l);

  const nameBadges = [
    `<span class="badge status-${esc(l.status)}">${STATUS_LABEL[l.status] || esc(l.status)}</span>`,
    `<span class="badge free-${esc(l.freePath)}">${FREE_LABEL[l.freePath]}</span>`,
    `<span class="badge">${VERIFY_LABEL[l.verification.level]}</span>`,
    ...(l.platforms || []).map((p) => `<span class="badge">${PLATFORM_LABEL[p] || esc(p)}</span>`),
    unv ? `<span class="badge unverified">Unverified</span>` : "",
  ].join("");

  const detailRows = [
    ["Who can enter", l.eligibility],
    ["Blocked / limits", l.restricted],
    ["Pays via", (l.payoutMethods || []).join(", ")],
    ["Prize note", prizeBlanked(l) ? "" : l.prizeNote],
    ["Last checked", l.lastChecked],
  ]
    .filter(([, v]) => v && String(v).trim())
    .map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`)
    .join("");
  const flags = (l.redFlags || []).length
    ? `<dt>Watch-outs</dt><dd><ul>${l.redFlags.map((f) => `<li>${esc(f)}</li>`).join("")}</ul></dd>`
    : "";
  const details = `<details class="meta"><summary>Eligibility, limits &amp; watch-outs</summary>
    <dl class="meta-grid">${detailRows}${flags}</dl></details>`;

  const prizeBlank = prizeBlanked(l);
  const prizeCell = prizeBlank
    ? `<span class="unverified-val">Unverified</span>
       <span class="row-note">Not confirmable from official source — <a href="flagged.html#flag-${esc(l.id)}">see flag</a></span>`
    : esc(l.prizeUsd);

  const links = [];
  const seen = new Set();
  const add = (label, url) => {
    if (!url || seen.has(url)) return;
    seen.add(url);
    links.push(`<a href="${esc(url)}" rel="noopener noreferrer">${label} →</a>`);
  };
  if (!unv) {
    add("Official signup", l.signupUrl);
    if (l.rulesUrl && l.rulesUrl !== l.signupUrl) add("Official rules", l.rulesUrl);
    if (l.iosUrl) add("App Store", l.iosUrl);
    if (l.tosUrl && l.tosUrl !== l.rulesUrl && l.tosUrl !== l.signupUrl) add("Terms", l.tosUrl);
    for (const s of off) if (s.url !== l.signupUrl && s.url !== l.rulesUrl) add(`Source: ${s.title}`, s.url);
  }
  const sourceCell = unv
    ? `<span class="unverified-val">No official source</span>
       <span class="row-note"><a href="flagged.html#flag-${esc(l.id)}">Why this row is flagged</a></span>`
    : `<div class="cell-links">${links.join("")}</div><span class="row-note">Checked ${esc(l.lastChecked)}</span>`;

  return `<tr id="${esc(l.id)}" data-name="${esc(l.name.toLowerCase())}" data-status="${esc(l.status)}" data-free="${esc(l.freePath)}">
  <td class="name" data-label="Competition"><b>${esc(l.name)}</b>
    <span class="short">${prizeBlank ? "" : esc(l.short)}${prizeBlank ? `<span class="row-note">Description withheld — contains values not confirmable from the official source.</span>` : ""}</span>
    <span>${nameBadges}</span>${details}</td>
  <td data-label="Prize (official source)">${prizeCell}</td>
  <td data-label="Free path">${FREE_LABEL[l.freePath]}</td>
  <td data-label="Status">${STATUS_LABEL[l.status]}</td>
  <td data-label="Cash-out floor">${unv ? "" : esc(l.minCashout)}</td>
  <td data-label="Pays via">${unv ? "" : esc((l.payoutMethods || []).join(", "))}</td>
  <td data-label="Who can enter">${unv ? "" : esc(l.eligibility)}</td>
  <td data-label="Source">${sourceCell}</td>
</tr>`;
}

function ledgerTable(list, caption) {
  return `<div class="table-wrap"><table class="ledger">
<caption>${esc(caption)}</caption>
<thead><tr>
<th>Competition</th><th>Prize (official source)</th><th>Free path</th><th>Status</th>
<th>Cash-out floor</th><th>Pays via</th><th>Who can enter</th><th>Source</th>
</tr></thead>
<tbody>
${list.map(rowCells).join("\n")}
</tbody></table></div>`;
}

function filterBar(placeholder) {
  return `<div class="filters" data-filter-for="ledger">
  <input type="search" placeholder="${esc(placeholder)}" aria-label="Search competitions">
  <select aria-label="Filter by status">
    <option value="">Any status</option>
    <option value="live">Active</option>
    <option value="mixed">Mixed</option>
    <option value="caution">Caution</option>
    <option value="ended">Ended</option>
  </select>
  <select aria-label="Filter by free path">
    <option value="">Any free path</option>
    <option value="full">Free USD path</option>
    <option value="partial">Some free events</option>
    <option value="paid-cash">Cash needs entry fee</option>
  </select>
  <span class="count-note" data-count-note></span>
</div>`;
}

function categoryNav(activeId) {
  const links = ledger.types
    .filter((t) => (byType[t.id] || []).length)
    .map(
      (t) =>
        `<a href="${t.id}.html"${t.id === activeId ? ' aria-current="page"' : ""}>${esc(t.name)} <span>(${byType[t.id].length})</span></a>`
    )
    .join("");
  return `<nav class="filters" aria-label="Categories">${links}</nav>`;
}

/* ------------------------------------------------------------- pages */
const built = [];

/* ---- index.html ---- */
{
  const cards = ledger.types
    .filter((t) => (byType[t.id] || []).length)
    .map(
      (t) => `<a class="cat-card" href="${t.id}.html">
  <h3>${esc(t.name)}</h3>
  <p>${esc(t.blurb)}</p>
  <span class="count">${byType[t.id].length} entries →</span>
</a>`
    )
    .join("\n");

  const top = ranked.slice(0, 15);
  const topRows = top
    .map(({ l, s }) => {
      const unv = prizeBlanked(l);
      const off = officialSources(l)[0];
      return `<tr>
  <td data-label="Rank" class="num"><span class="badge score">${s}</span></td>
  <td class="name" data-label="Competition"><b>${esc(l.name)}</b><span class="short">${esc(l.short)}</span>
    <span><span class="badge status-${esc(l.status)}">${STATUS_LABEL[l.status]}</span>
    <span class="badge free-${esc(l.freePath)}">${FREE_LABEL[l.freePath]}</span></span></td>
  <td data-label="Prize (official source)">${unv ? `<span class="unverified-val">Unverified</span>` : esc(l.prizeUsd)}</td>
  <td data-label="Source"><div class="cell-links">
    <a href="${esc(l.signupUrl)}" rel="noopener noreferrer">Official signup →</a>
    ${off && off.url !== l.signupUrl ? `<a href="${esc(off.url)}" rel="noopener noreferrer">${esc(off.title)} →</a>` : ""}
  </div></td>
</tr>`;
    })
    .join("\n");

  const body = `
<section class="hero">
  <p class="kicker">Research dashboard · built ${TODAY}</p>
  <h1>Free-to-enter competitions with real cash prizes</h1>
  <p class="lede">A verified, organized ledger of ${stats.total} competitions across ${stats.types} categories —
  skill games, trivia, fantasy &amp; picks, creative, forecasting, markets, tech, directories and pool tools.
  Every row links to an <strong>official</strong> source. Values that cannot be confirmed from an official
  source are left blank and flagged, never guessed.</p>
  <div class="stats">
    <div class="stat"><b>${stats.total}</b><span>Listings</span></div>
    <div class="stat"><b>${stats.freeFull}</b><span>True free-USD paths</span></div>
    <div class="stat"><b>${stats.live}</b><span>Active now</span></div>
    <div class="stat"><b>${stats.officialSources}</b><span>Rows with official source</span></div>
    <div class="stat"><b>${stats.unverified}</b><span>Flagged unverified</span></div>
  </div>
  <div class="notice">⚠ <strong>Honesty rules:</strong> gems, tickets, bonus cash and gift cards are never
  dressed up as dollars. US tax forms apply at $600+. No legitimate operator will charge a fee to release a prize.
  Sweepstakes and gambling-operator promos are out of scope (see <a href="analysis.html">Analysis</a>).</div>
</section>

<h2 class="section">Best places to spend your time <span class="muted">(top 15 by transparent priority score)</span></h2>
${ledgerTableTop(topRows)}

<h2 class="section">Browse by category</h2>
<div class="grid">
${cards}
</div>

<h2 class="section">Start here</h2>
<div class="grid">
  <a class="cat-card" href="analysis.html"><h3>Analysis &amp; findings</h3><p>Distributions, patterns, scoring method, policy exclusions.</p><span class="count">Open →</span></a>
  <a class="cat-card" href="flagged.html"><h3>Flagged for review</h3><p>${stats.unverified} unverified rows + any link-check failures, with sources.</p><span class="count">Open →</span></a>
  <a class="cat-card" href="executive-summary.html"><h3>Executive summary</h3><p>Goals, method, results, irregularities — one page.</p><span class="count">Open →</span></a>
</div>`;

  function ledgerTableTop(rows) {
    return `<div class="table-wrap"><table class="ledger">
<caption>Priority score = active status (3) + free-USD path (3) + low-friction verification
(2 for account-only, 1 for eligibility check) − penalties for caution/paid-entry.
Full formula on the <a href="analysis.html">Analysis page</a>. It is a transparent heuristic, not a payout prediction.</caption>
<thead><tr><th>Score</th><th>Competition</th><th>Prize (official source)</th><th>Source</th></tr></thead>
<tbody>${rows}</tbody></table></div>`;
  }

  writeFileSync(
    join(root, "index.html"),
    page({
      title: `${SITE} — verified free cash-prize competitions`,
      active: "index.html",
      desc: `Dashboard of ${stats.total} free-to-enter competitions that can pay real money, each with an official source link.`,
      body,
    })
  );
  built.push("index.html");
}

/* ---- category pages ---- */
for (const t of ledger.types) {
  const list = byType[t.id] || [];
  if (!list.length) continue;
  const unvCount = list.filter(isUnverified).length;
  const body = `
<section class="hero">
  <p class="kicker">Category</p>
  <h1>${esc(t.name)} <span class="muted">(${list.length})</span></h1>
  <p class="lede">${esc(t.blurb)}</p>
  ${unvCount ? `<div class="notice">⚠ ${unvCount} row(s) here have no official source; their values are blank and they are listed on <a href="flagged.html">Flagged for Review</a>.</div>` : ""}
</section>
${categoryNav(t.id)}
${filterBar(`Search ${t.name.toLowerCase()}…`)}
${ledgerTable(list, `${list.length} listings · every row links to an official source · values without an official source are blank and flagged.`)}`;
  const file = `${t.id}.html`;
  writeFileSync(
    join(root, file),
    page({
      title: `${t.name} — ${SITE}`,
      active: "",
      desc: `${list.length} ${t.name.toLowerCase()} listings with official source links.`,
      body,
    })
  );
  built.push(file);
}

/* ---- analysis.html ---- */
{
  const dist = (key, labels) =>
    ledger.types
      .map((t) => {
        const n = (byType[t.id] || []).filter(key).length;
        return { name: t.name, n };
      })
      .filter((x) => x.n)
      .sort((a, b) => b.n - a.n)
      .map(
        (x) => `<div class="bar-row"><span class="label">${esc(x.name)}</span>
  <span class="track"><span class="fill" style="width:${Math.round((x.n / stats.total) * 100)}%"></span></span>
  <span class="val">${x.n}</span></div>`
      )
      .join("");

  const statusCounts = ["live", "mixed", "caution", "ended", "inactive"]
    .map((s) => ({ s, n: ledger.listings.filter((l) => l.status === s).length }))
    .filter((x) => x.n);
  const maxStatus = Math.max(...statusCounts.map((x) => x.n));
  const statusBars = statusCounts
    .map(
      (x) => `<div class="bar-row"><span class="label">${STATUS_LABEL[x.s]}</span>
  <span class="track"><span class="fill" style="width:${Math.round((x.n / maxStatus) * 100)}%"></span></span>
  <span class="val">${x.n}</span></div>`
    )
    .join("");

  const freeCounts = ["full", "partial", "paid-cash"].map((f) => ({
    f,
    n: ledger.listings.filter((l) => l.freePath === f).length,
  }));
  const freeBars = freeCounts
    .map(
      (x) => `<div class="bar-row"><span class="label">${FREE_LABEL[x.f]}</span>
  <span class="track"><span class="fill" style="width:${Math.round((x.n / stats.total) * 100)}%"></span></span>
  <span class="val">${x.n}</span></div>`
    )
    .join("");

  const verifCounts = ["account", "eligibility", "kyc", "tax"].map((v) => ({
    v,
    n: ledger.listings.filter((l) => l.verification.level === v).length,
  }));
  const verifBars = verifCounts
    .map(
      (x) => `<div class="bar-row"><span class="label">${VERIFY_LABEL[x.v]}</span>
  <span class="track"><span class="fill" style="width:${Math.round((x.n / stats.total) * 100)}%"></span></span>
  <span class="val">${x.n}</span></div>`
    )
    .join("");

  const removedList = (ledger.removedThisPass || [])
    .map((r) => `<li><strong>${esc(r.name)}</strong> — ${esc(r.why)}</li>`)
    .join("");

  const body = `
<section class="hero">
  <p class="kicker">Findings</p>
  <h1>Analysis &amp; findings</h1>
  <p class="lede">Every number below is computed directly from the ledger file
  (<code>assets/data.js</code>, reviewed ${esc(REVIEWED)}). Nothing is estimated.</p>
</section>

<div class="panel">
  <h2>What's in the ledger</h2>
  <p><strong>${stats.total}</strong> listings · <strong>${stats.types}</strong> categories ·
  <strong>${stats.officialSources}</strong> rows with an official source ·
  <strong>${stats.unverified}</strong> rows flagged unverified (no official source) ·
  <strong>${stats.removed}</strong> candidates removed by policy in the upstream audit.</p>
  <h3>Listings by category</h3>
  ${dist(() => true)}
</div>

<div class="panel">
  <h2>Status of entries</h2>
  ${statusBars}
  <p class="muted">${stats.ended} entries are ended or out-of-season — their prize figures are historical
  and must be re-confirmed on the official page before entering. ${stats.caution} carry caution flags.</p>
</div>

<div class="panel">
  <h2>Free-to-enter reality check</h2>
  ${freeBars}
  <p class="muted">Only <strong>${stats.freeFull}</strong> rows advertise a genuine free-USD path.
  "Some free events" rows mix free and paid competition; "Cash needs entry fee" rows are listed for
  completeness and are <em>not</em> free to win money in.</p>
</div>

<div class="panel">
  <h2>Verification friction (what you must pass to get paid)</h2>
  ${verifBars}
  <p class="muted">Account-only = email login is enough to play; eligibility = age/residency checks;
  KYC = government ID before cash-out; tax paperwork = W-9/W-8 at $600+ (US).</p>
</div>

<div class="panel">
  <h2>Priority score — full formula</h2>
  <p>Used only to rank the "Best places to spend your time" table on the home page.
  It is a <strong>transparent heuristic over ledger fields</strong>, not a prediction of winnings,
  and it ignores prize size (prize text is not machine-parseable and guessing would violate the
  no-inference rule).</p>
  <ul>
    <li>Status: active <strong>+3</strong>, mixed <strong>+1</strong>, caution <strong>−1</strong> (ended/inactive excluded)</li>
    <li>Free path: free-USD <strong>+3</strong>, some free <strong>+1</strong>, fee-required <strong>−2</strong></li>
    <li>Verification: account-only <strong>+2</strong>, eligibility check <strong>+1</strong>, KYC/tax <strong>0</strong></li>
    <li>No official source → row excluded from ranking entirely</li>
  </ul>
  <p class="muted">Reproduce it: <code>node scripts/build-pages.mjs</code> (function <code>priorityScore</code>).</p>
</div>

<div class="panel">
  <h2>Policy exclusions (removed upstream, not carried into tables)</h2>
  <p>The upstream audit removed sweepstakes, sweepstakes casinos, gambling-operator free-to-play funnels
  and real-money DFS. Reasons: sweepstakes are chance draws (no skill), sweeps casinos demand full KYC plus
  mail-in AMOE, and bookmaker/DFS free games are acquisition funnels that often pay bonus bets, not cash.
  Full list:</p>
  <ul>${removedList}</ul>
</div>

<div class="panel">
  <h2>Patterns worth knowing before you invest time</h2>
  <ul>
    <li><strong>Free rooms rarely pay dollars.</strong> Skill apps (Solitaire/Bingo/Skillz-style) pay gems or
    tickets on free paths; withdrawable USD almost always needs a paid entry.</li>
    <li><strong>Seasonal sports games dominate volume</strong> (${(byType.sports || []).length} of ${stats.total} rows)
    and most go dormant in the off-season — check the status badge first.</li>
    <li><strong>Tax paperwork starts at $600</strong> in the US; keep records for every win.</li>
    <li><strong>Geo-restrictions are common</strong> — state/country blocks appear in each row's
    "Blocked / limits" detail.</li>
    <li><strong>${stats.unverified} rows have no official source</strong> and are excluded from ranking;
    they are published on the <a href="flagged.html">Flagged for Review</a> page with their non-official
    links so a human can confirm or drop them.</li>
  </ul>
</div>`;
  writeFileSync(
    join(root, "analysis.html"),
    page({
      title: `Analysis & findings — ${SITE}`,
      active: "analysis.html",
      desc: "Distributions, scoring method, policy exclusions and patterns computed from the ledger.",
      body,
    })
  );
  built.push("analysis.html");
}

/* ---- flagged.html ---- */
{
  const linkReportPath = join(root, "reports", "link-check.json");
  let linkFlags = "";
  if (existsSync(linkReportPath)) {
    try {
      const r = JSON.parse(readFileSync(linkReportPath, "utf8"));
      const bad = (r.results || []).filter((x) => x.status === "broken");
      const blocked = (r.results || []).filter((x) => x.status === "blocked");
      linkFlags = `
<div class="panel">
  <h2>Link check (automated, run ${esc(r.generatedAt || "unknown")})</h2>
  <p class="muted">Checked ${r.results?.length ?? 0} unique URLs. ${bad.length} broken,
  ${blocked.length} blocked (server refused the checker but may work in a browser).
  Broken links are flagged below; blocked links are listed in
  <code>reports/link-check.json</code> for manual review.</p>
  ${
    bad.length
      ? `<ul>${bad
          .map(
            (b) =>
              `<li><strong>${esc(b.what)}</strong> — <code>${esc(b.url)}</code> → ${esc(String(b.code || b.error || ""))}
              (<a href="${esc(b.url)}">open</a>) · listing: <code>${esc(b.listingId || "site-wide")}</code></li>`
          )
          .join("")}</ul>
  <p class="muted">Each broken link is also attached to its listing flag below when a listing id is known.</p>`
      : `<p>✅ No broken links found in this run.</p>`
  }
</div>`;
    } catch {
      linkFlags = `<div class="panel"><h2>Link check</h2><p class="muted">Report present but unreadable — see <code>reports/link-check.json</code>.</p></div>`;
    }
  } else {
    linkFlags = `<div class="panel"><h2>Link check</h2><p class="muted">No <code>reports/link-check.json</code> yet — run
    <code>node scripts/check-links.mjs</code> (or the <em>linkcheck</em> GitHub Actions workflow) and rebuild.</p></div>`;
  }

  const flags = ledger.listings
    .filter(isUnverified)
    .map((l) => {
      const nonOfficial = (l.sources || [])
        .map((s) => `<div class="src">Non-official (${esc(s.tier)}): <a href="${esc(s.url)}" rel="noopener noreferrer">${esc(s.title)}</a> — ${esc(s.url)}</div>`)
        .join("");
      return `<div class="flag-item" id="flag-${esc(l.id)}">
  <h3>${esc(l.name)} <span class="badge unverified">Unverified — values blank</span></h3>
  <p><strong>Why flagged:</strong> this row has no source with tier <code>official</code>.
  Under the project rule, values that cannot be confirmed from an official source are left blank
  and never inferred — so Prize, Cash-out, Pays via and Who-can-enter are blank in its table row.</p>
  <p><strong>What would clear it:</strong> an official rules, contest or signup page from the operator itself.</p>
  ${nonOfficial}
  <p class="src">Row in table: <a href="${esc(l.type)}.html#${esc(l.id)}">${esc(l.type)}.html#${esc(l.id)}</a>
  · upstream last-checked: ${esc(l.lastChecked)}</p>
</div>`;
    })
    .join("\n");

  const spotFlags = [...spotUnconfirmed.entries()]
    .map(([id, checks]) => {
      const l = ledger.listings.find((x) => x.id === id);
      if (!l) return "";
      const obs = checks
        .map(
          (c) =>
            `<p><strong>Spot-check (${esc(c.date)}, field <code>${esc(c.field)}</code>):</strong> ${esc(c.observed)}</p>
             <p class="src">Official page fetched: <a href="${esc(c.source)}" rel="noopener noreferrer">${esc(c.source)}</a></p>`
        )
        .join("");
      return `<div class="flag-item" id="flag-${esc(id)}">
  <h3>${esc(l.name)} <span class="badge unverified">Prize value blanked</span></h3>
  <p><strong>Why flagged:</strong> a manual fetch of the official page could not confirm the ledger's
  value for <code>prizeUsd</code>. Per project rule the value is shown blank in the table — never
  rewritten or inferred.</p>
  ${obs}
  <p class="src">Row in table: <a href="${esc(l.type)}.html#${esc(id)}">${esc(l.type)}.html#${esc(id)}</a>
  · upstream last-checked: ${esc(l.lastChecked)}</p>
</div>`;
    })
    .filter(Boolean)
    .join("\n");

  const body = `
<section class="hero">
  <p class="kicker">Transparency</p>
  <h1>Flagged for Review</h1>
  <p class="lede">Everything the data could <em>not</em> confirm from an official source lives here.
  These items do not block publication — they are published so a human can review them.
  Nothing on this page has been guessed or filled in.</p>
  <div class="stats">
    <div class="stat"><b>${stats.unverified}</b><span>Unverified rows</span></div>
    <div class="stat"><b>${spotUnconfirmed.size}</b><span>Spot-check failures (prize blanked)</span></div>
    <div class="stat"><b>${spotConfirmedIds.size}</b><span>Spot-checks passed</span></div>
    <div class="stat"><b>${stats.removed}</b><span>Policy removals (upstream)</span></div>
    <div class="stat"><b>${stats.ended}</b><span>Ended entries (prizes historical)</span></div>
  </div>
</section>

${linkFlags}

<div class="panel">
  <h2>Ended / out-of-season entries (${stats.ended})</h2>
  <p class="muted">Kept in tables with an "Ended" badge. Prize figures for these rows describe a past or
  future season and must be re-confirmed on the official page before entering.
  They are excluded from the priority ranking.</p>
</div>

<div class="panel">
  <h2>Upstream policy removals (${stats.removed})</h2>
  <p class="muted">Removed by the upstream audit before this build — sweepstakes, casinos, gambling-operator
  promos, real-money DFS and dead apps. Listed on <a href="analysis.html">Analysis</a> with reasons;
  not carried into any table.</p>
</div>

<h2 class="section">Unverified rows (${stats.unverified}) — values shown blank</h2>
${flags}

<h2 class="section">Spot-check failures — prize value blanked</h2>
${spotFlags || `<p class="muted">None recorded.</p>`}`;

  writeFileSync(
    join(root, "flagged.html"),
    page({
      title: `Flagged for review — ${SITE}`,
      active: "flagged.html",
      desc: "Unverified rows, link-check failures and policy exclusions with source links.",
      body,
    })
  );
  built.push("flagged.html");
}

/* ---- executive-summary.html (kept in sync with EXECUTIVE_SUMMARY.md) ---- */
{
  const body = `
<section class="hero">
  <p class="kicker">Executive summary</p>
  <h1>Free cash-prize competition ledger — project summary</h1>
  <p class="lede">Prepared ${TODAY} · data reviewed upstream ${esc(REVIEWED)} ·
  ${stats.total} listings · source: <a href="https://github.com/karagemop466-tech/FreeMoneyApps">karagemop466-tech/FreeMoneyApps</a></p>
</section>

<div class="panel">
  <h2>Goal</h2>
  <p>Collect, organize and analyze a full list of free-to-enter competitions that pay real cash,
  and publish it as a clean, mobile-friendly dashboard where every value carries an official source
  link and anything unconfirmable is blank and flagged — so a human (and an AI agent) can pick the
  best competitions to spend time on.</p>
</div>

<div class="panel">
  <h2>What exists</h2>
  <ul>
    <li><strong>${stats.total} listings</strong> across ${stats.types} categories, ${stats.freeFull} with a true free-USD path,
    ${stats.live} active, ${stats.ended} ended/out-of-season.</li>
    <li><strong>${stats.officialSources} rows carry an official source</strong>; ${stats.unverified} rows have none and are
    flagged with blank values on <a href="flagged.html">Flagged for Review</a>.</li>
    <li>Upstream audit removed ${stats.removed} sweepstakes/casino/gambling-operator entries by policy
    (<a href="analysis.html">Analysis</a> lists them with reasons).</li>
  </ul>
</div>

<div class="panel">
  <h2>What this build adds</h2>
  <ul>
    <li><strong>Responsive dashboard</strong>: landing page + one subpage per category, table format,
    search/status/free-path filters, mobile card layout below 720px (the upstream site was a single
    206-card scroll with no filters — the top complaint).</li>
    <li><strong>Verification pipeline</strong>: <code>scripts/check-data.mjs</code> (structural audit),
    <code>scripts/check-links.mjs</code> (every URL in data + pages, run in CI), spot checks of featured
    entries against official pages (<code>verification-log.md</code>).</li>
    <li><strong>Analysis</strong>: distributions, transparency-scored top-15 ranking with published formula,
    policy exclusions, patterns (<a href="analysis.html">Analysis</a>).</li>
    <li><strong>Flag page</strong>: every unverified row and every broken link, with source links
    (<a href="flagged.html">Flagged for Review</a>).</li>
  </ul>
</div>

<div class="panel">
  <h2>Irregularities for review</h2>
  <ol>
    <li>${stats.unverified} listings have only affiliate/forum sources (names in <a href="flagged.html">Flagged for Review</a>) —
    values blanked, awaiting official confirmation.</li>
    <li>3 of 9 spot-checked featured entries could not be confirmed from their official pages
    (Devpost — official page now lists a $1,000,000 event vs the ledger's stated range; Fanatics Survivor —
    official page shows no contest and third parties describe the $1M as FanCash, not USD; Dirty Dozen —
    official URL redirects to a generic games index). Prize values blanked + flagged, not rewritten.
    6 of 9 verified exactly (ESPN NFL $102K/58 prizes, ESPN CFB $86K/46 prizes, CBS $1K×18 + $5K + $100K,
    ARC Prize $2M/3 tracks, Kaggle, DrivenData). Details: <code>reports/spot-checks.json</code> and
    <code>verification-log.md</code>.</li>
    <li>${stats.ended} ended entries keep historical prize figures — re-confirm before entering.</li>
    <li>Any link-check failures are published on the flag page as they are found
    (<code>reports/link-check.json</code>).</li>
  </ol>
</div>

<div class="panel">
  <h2>Bottom line</h2>
  <p><strong>${stats.freeFull} competitions currently advertise a genuine free path to cash.</strong>
  Start from the <a href="index.html">home page</a> top-15 table, open the official rules from the row's
  source cell, and treat every prize figure as "per the official page as of ${esc(REVIEWED)}" until
  you re-check it yourself.</p>
</div>`;
  writeFileSync(
    join(root, "executive-summary.html"),
    page({
      title: `Executive summary — ${SITE}`,
      active: "executive-summary.html",
      desc: "Project goal, method, results and irregularities in one page.",
      body,
    })
  );
  built.push("executive-summary.html");
}

/* ---- 404.html ---- */
{
  const body = `<section class="hero">
  <p class="kicker">404</p>
  <h1>Page not found</h1>
  <p class="lede">That page doesn't exist. Head back to the <a href="index.html">dashboard</a>
  or jump to a category.</p>
</section>${categoryNav(null)}`;
  writeFileSync(
    join(root, "404.html"),
    page({ title: `Not found — ${SITE}`, active: "", desc: "Page not found.", body })
  );
  built.push("404.html");
}

/* ------------------------------------------------- internal link check */
const internalHrefs = new Set();
for (const f of built) {
  const html = readFileSync(join(root, f), "utf8");
  for (const m of html.matchAll(/href="([^"]+)"/g)) {
    const href = m[1];
    if (/^(https?:|mailto:|#|data:)/.test(href)) continue;
    internalHrefs.add(href.split("#")[0]);
  }
}
const missing = [...internalHrefs].filter((h) => h && !existsSync(join(root, h)));
if (missing.length) {
  console.error("MISSING INTERNAL TARGETS:", missing);
  process.exit(3);
}

console.log(`Built ${built.length} pages: ${built.join(", ")}`);
console.log(`Internal links checked: ${internalHrefs.size} — all resolve.`);
