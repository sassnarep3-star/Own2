// Builds the static site into _site/ from:
//   data/source/ledger-data.js  (unmodified snapshot of the upstream ledger)
//   data/review.json            (this review's verification record, flags, irregularities)
// Rules enforced here:
//   * A prize value is shown as "verified" only if data/review.json holds an official-page value for that row.
//   * Ledger prize claims are never shown in verified columns. They appear only on flagged.html, labelled UNVERIFIED.
//   * Every row keeps a link to its official signup page.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(ROOT, '_site');

const src = fs.readFileSync(path.join(ROOT, 'data/source/ledger-data.js'), 'utf8');
const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(src, sandbox);
const L = sandbox.window.LEDGER;
const REVIEW = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/review.json'), 'utf8'));

const CHECKED_ON = REVIEW.checkedOn; // 2026-11-01
const SOURCE_COMMIT = '466f7c1e7a14b52b4a0d36beb84a00d68fd409b7';
const SOURCE_REPO = 'https://github.com/karagemop466-tech/FreeMoneyApps';
const LIVE_SITE = 'https://karagemop466-tech.github.io/FreeMoneyApps/';

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const SEV_RANK = { high: 3, medium: 2, low: 1 };

const TYPES = L.types;
const TYPE_BY_ID = Object.fromEntries(TYPES.map((t) => [t.id, t]));
const VERIF_LABEL = {
  verified: 'Verified',
  partial: 'Partially verified',
  conflict: 'Conflict with official page',
  broken: 'Broken link',
  unverified: 'Unverified',
};
const FREE_LABEL = { full: 'Free path: full', partial: 'Partly free', 'paid-cash': 'Cash needs entry fee' };
const STATUS_LABEL = { live: 'Live', ended: 'Ended', caution: 'Caution', mixed: 'Mixed' };

// ---------- build row model ----------
function autoFlags(x, manual) {
  const out = [];
  const types = new Set(manual.map((f) => f.type));
  const hasOfficial = (x.sources || []).some((s) => s.tier === 'official');
  if (!hasOfficial && !types.has('source')) out.push({ severity: 'medium', type: 'source', text: 'No official-tier source in the ledger for this row. Verify before use.' });
  if ([x.signupUrl, x.rulesUrl, x.tosUrl, x.iosUrl].some((u) => u && u.startsWith('http:')) && !types.has('link')) out.push({ severity: 'low', type: 'link', text: 'Link uses http://.' });
  if (!x.rulesUrl && !types.has('link')) out.push({ severity: 'low', type: 'link', text: 'No rules link in the ledger.' });
  if (x.code) out.push({ severity: 'low', type: 'code', text: 'Join or promo code present in ledger data. Not published here; unverified.' });
  return out;
}

const rows = L.listings.map((x) => {
  const v = REVIEW.verified[x.id] || null;
  const verif = v ? v.status : 'unverified';
  const prizeVerified = v && v.prize && verif !== 'broken' ? v.prize : null;
  const manual = (REVIEW.rowFlags[x.id] || []).slice();
  const flags = manual.concat(autoFlags(x, manual));
  const maxSev = flags.reduce((m, f) => Math.max(m, SEV_RANK[f.severity] || 0), 0);
  const sevName = maxSev === 3 ? 'high' : maxSev === 2 ? 'medium' : maxSev === 1 ? 'low' : '';
  const links = [];
  if (x.signupUrl) links.push({ label: 'Official signup / page', url: x.signupUrl });
  if (x.rulesUrl && x.rulesUrl !== x.signupUrl) links.push({ label: 'Rules', url: x.rulesUrl });
  if (x.iosUrl) links.push({ label: 'iOS App Store', url: x.iosUrl });
  if (v && v.evidence && !links.some((l) => l.url === v.evidence)) links.push({ label: 'Checked page (2026-11-01)', url: v.evidence });
  if (v && v.rules && !links.some((l) => l.url === v.rules)) links.push({ label: 'Checked rules (2026-11-01)', url: v.rules });
  return {
    id: x.id,
    name: x.name,
    type: x.type,
    typeName: (TYPE_BY_ID[x.type] || {}).name || x.type,
    ledgerStatus: x.status,
    freePath: x.freePath,
    platforms: x.platforms || [],
    links,
    verification: verif,
    verificationFinding: v ? v.finding : '',
    prizeVerified,
    ledgerPrizeClaim: x.prizeUsd || '',
    ledgerNotes: {
      eligibility: x.eligibility || '',
      payoutMethods: (x.payoutMethods || []).join(', '),
      minCashout: x.minCashout || '',
      restricted: x.restricted || '',
    },
    lastCheckedLedger: x.lastChecked,
    flags,
    flagCount: flags.length,
    maxSeverity: sevName,
    featured: L.featured.includes(x.id),
  };
});

const BY_TYPE = Object.fromEntries(TYPES.map((t) => [t.id, rows.filter((r) => r.type === t.id)]));

// Evidence-screened candidates. Criteria: an official page was read and is not in conflict, free path full,
// ledger says live, no high-severity flag. These are candidates to read first, not rankings.
const SHORTLIST = rows.filter(
  (r) => ['verified', 'partial'].includes(r.verification) && r.freePath === 'full' && r.ledgerStatus === 'live' && r.maxSeverity !== 'high',
);
SHORTLIST.sort((x, y) => (x.verification === 'verified' ? 0 : 1) - (y.verification === 'verified' ? 0 : 1));

// ---------- stats ----------
const count = (f) => rows.filter(f).length;
const STATS = {
  listings: rows.length,
  categories: TYPES.length,
  freeFull: count((r) => r.freePath === 'full'),
  freePartial: count((r) => r.freePath === 'partial'),
  freeCashOnly: count((r) => r.freePath === 'paid-cash'),
  live: count((r) => r.ledgerStatus === 'live'),
  ended: count((r) => r.ledgerStatus === 'ended'),
  verified: count((r) => r.verification === 'verified'),
  partial: count((r) => r.verification === 'partial'),
  conflict: count((r) => r.verification === 'conflict'),
  broken: count((r) => r.verification === 'broken'),
  unverified: count((r) => r.verification === 'unverified'),
  flagged: count((r) => r.flagCount > 0),
  high: count((r) => r.maxSeverity === 'high'),
  medium: count((r) => r.maxSeverity === 'medium'),
  low: count((r) => r.maxSeverity === 'low'),
  shortlist: SHORTLIST.length,
  irregularities: REVIEW.irregularities.length,
  highIrregularities: REVIEW.irregularities.filter((i) => i.severity === 'high').length,
  fplThird: count((r) => r.flags.some((f) => f.type === 'misattributed')),
  noOfficial: count((r) => r.flags.some((f) => f.type === 'source' && f.text.startsWith('No official'))),
  http: count((r) => r.flags.some((f) => f.type === 'link' && f.text.includes('http://'))),
  noRules: count((r) => r.flags.some((f) => f.text.startsWith('No rules'))),
  codes: count((r) => r.flags.some((f) => f.type === 'code')),
  iosAlive: count((r) => r.platforms.includes('ios') && r.ledgerStatus !== 'ended'),
  verifiedTotal: 0,
};
STATS.verifiedTotal = STATS.verified + STATS.partial + STATS.conflict + STATS.broken;
STATS.pct = ((STATS.verifiedTotal / STATS.listings) * 100).toFixed(1);

// ---------- layout ----------
const CSS_VERSION = '2026-11-01a';
function layout({ title, root, active, body, description }) {
  const nav = [
    ['', 'Home', 'home'],
    ['all.html', 'All entries', 'all'],
    ['flagged.html', 'Flagged for review', 'flagged'],
    ['executive-summary.html', 'Executive summary', 'exec'],
    ['methodology.html', 'Methodology', 'method'],
  ]
    .map(([href, label, key]) => `<a href="${root}${href}"${active === key ? ' class="active" aria-current="page"' : ''}>${label}</a>`)
    .join('');
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} · Free Cash-Prize Competitions Ledger</title>
<meta name="description" content="${esc(description || 'Verification dashboard for free-to-enter competitions that can pay real money. Official sources only; unverified values left blank.')}">
<link rel="stylesheet" href="${root}assets/style.css?v=${CSS_VERSION}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="${root}">Free Cash-Prize Ledger</a>
    <nav class="nav" aria-label="Main">${nav}</nav>
  </div>
</header>
<main id="main" class="wrap">
${body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>Snapshot of upstream ledger from <a href="${SOURCE_REPO}">${esc(SOURCE_REPO.replace('https://', ''))}</a> (commit <code>${SOURCE_COMMIT.slice(0, 7)}</code>, 2026-08-19). Verification pass: ${CHECKED_ON}.</p>
    <p>Not affiliated with any operator listed. Not legal, tax or gambling advice. Official rules always govern. Values marked blank are unverified.</p>
  </div>
</footer>
<script src="${root}assets/app.js" defer></script>
</body>
</html>
`;
}

const badge = (cls, text) => `<span class="badge ${cls}">${esc(text)}</span>`;
const verifBadge = (v) => badge(`v-${v}`, VERIF_LABEL[v]);
const sevBadge = (s) => (s ? badge(`sev-${s}`, s === 'high' ? 'High' : s === 'medium' ? 'Medium' : 'Low') : '');

function rowHtml(r, { showCategory, root = '' }) {
  const search = [r.name, r.id, r.typeName, r.ledgerStatus, r.freePath, r.verification].join(' ').toLowerCase();
  const linkHtml = r.links.map((l) => `<a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)}</a>`).join('<br>');
  const notes = [];
  if (r.ledgerNotes.eligibility) notes.push(`<li><b>Eligibility:</b> ${esc(r.ledgerNotes.eligibility)}</li>`);
  if (r.ledgerNotes.payoutMethods) notes.push(`<li><b>Payout methods:</b> ${esc(r.ledgerNotes.payoutMethods)}</li>`);
  if (r.ledgerNotes.minCashout) notes.push(`<li><b>Cash-out floor:</b> ${esc(r.ledgerNotes.minCashout)}</li>`);
  if (r.ledgerNotes.restricted) notes.push(`<li><b>Restrictions:</b> ${esc(r.ledgerNotes.restricted)}</li>`);
  const details = `<details class="notes"><summary>Ledger notes (unverified, not checked)</summary><ul>${notes.join('') || '<li>None recorded.</li>'}</ul></details>`;
  const verifCell = `${verifBadge(r.verification)}${r.verificationFinding ? `<details class="notes"><summary>What the official page shows</summary><p>${esc(r.verificationFinding)}</p></details>` : ''}`;
  const flagCell = r.flagCount
    ? `<a class="flagcount" href="${root}flagged.html#${esc(r.id)}">${sevBadge(r.maxSeverity)} ${r.flagCount} flag${r.flagCount > 1 ? 's' : ''}</a>`
    : '<span class="muted">None</span>';
  const prizeCell = r.prizeVerified
    ? `<span class="prize">${esc(r.prizeVerified)}</span>`
    : '<span class="blank">Not verified. Left blank.</span>';
  return `<tr id="${esc(r.id)}" data-verif="${r.verification}" data-type="${esc(r.type)}" data-search="${esc(search)}">
  <td data-label="Contest"><a href="${esc(r.links[0].url)}" target="_blank" rel="noopener"><b>${esc(r.name)}</b></a><div class="muted small">${esc(r.id)}</div>${details}</td>
  ${showCategory ? `<td data-label="Category">${esc(r.typeName)}</td>` : ''}
  <td data-label="Free path">${esc(FREE_LABEL[r.freePath] || r.freePath)}<div class="muted small">Ledger</div></td>
  <td data-label="Status">${esc(STATUS_LABEL[r.ledgerStatus] || r.ledgerStatus)}<div class="muted small">Ledger, 2026-08-19</div></td>
  <td data-label="Prize on official page">${prizeCell}</td>
  <td data-label="Verification">${verifCell}</td>
  <td data-label="Official sources">${linkHtml}</td>
  <td data-label="Flags">${flagCell}</td>
</tr>`;
}

function tableHtml(list, { showCategory, id = 'listings', root = '' }) {
  const head = `<tr><th>Contest</th>${showCategory ? '<th>Category</th>' : ''}<th>Free path</th><th>Status</th><th>Prize on official page</th><th>Verification</th><th>Official sources</th><th>Flags</th></tr>`;
  return `<div class="table-tools">
  <label class="search">Search <input type="search" data-filter="${id}" placeholder="Name, status, verification…" aria-label="Filter table"></label>
  <label>Verification <select data-verif-filter="${id}" aria-label="Filter by verification">
    <option value="">All</option>
    ${Object.entries(VERIF_LABEL).map(([k, v]) => `<option value="${k}">${esc(v)}</option>`).join('')}
  </select></label>
  <span class="count" data-count-for="${id}">${list.length} rows</span>
</div>
<div class="table-wrap">
<table class="data" id="${id}" data-table>
<thead>${head}</thead>
<tbody>
${list.map((r) => rowHtml(r, { showCategory, root })).join('\n')}
</tbody>
</table>
</div>`;
}

const kpi = (n, label, cls = '') => `<div class="kpi ${cls}"><div class="kpi-n">${n}</div><div class="kpi-l">${esc(label)}</div></div>`;

// ---------- analysis per category ----------
const CATEGORY_NOTES = {
  skill: 'Four rows are cash-only (the free rooms pay gems, not dollars). Two Papaya titles share one signup link. On official-page checks in this pass, Checkmate Gaming is in conflict on its prize range.',
  trivia: 'Only two rows. One (Givling) is marked ended, and the ledger says trivia was removed from it.',
  creative: 'Mostly photo and writing contests. The photo awards are annual; their current deadlines are not verified (see flags).',
  tech: 'ARC Prize is verified. Kaggle conflicts with the ledger: its prize range is understated against the official page. Devpost is partially verified.',
  directory: 'Directories do not pay prizes. Use them to find contests, then verify each one on its own official rules.',
  sports: 'The largest category. Many UK fantasy leagues share one official Fantasy Premier League link (see flags). One sportsbook-operated contest is in the ledger\'s featured list.',
  pools: 'Friend-group pools. Prizes are set by the group, not by an operator, so they are not comparable with operator-funded contests.',
  forecasting: 'Metaculus is partially verified: its prize pools are free to enter, but amounts vary per tournament.',
  market: 'Broker demo and paper-trading contests. Three cite affiliate-tier sources only, and a trading account may be required.',
};

function categoryAnalysis(t) {
  const list = BY_TYPE[t.id] || [];
  const n = list.length;
  const ver = list.filter((r) => r.verification !== 'unverified').length;
  const flagged = list.filter((r) => r.flagCount).length;
  const high = list.filter((r) => r.maxSeverity === 'high').length;
  const full = list.filter((r) => r.freePath === 'full').length;
  const live = list.filter((r) => r.ledgerStatus === 'live').length;
  return `<section class="analysis">
  <h2>Analysis</h2>
  <div class="kpis">
    ${kpi(n, 'Listings')}
    ${kpi(full, 'Free path: full (ledger)')}
    ${kpi(live, 'Live (ledger)')}
    ${kpi(ver, 'Checked on an official page', ver ? 'ok' : '')}
    ${kpi(flagged, 'Flagged', flagged ? 'warn' : '')}
    ${kpi(high, 'High-severity flags', high ? 'bad' : '')}
  </div>
  <p>${esc(CATEGORY_NOTES[t.id] || '')}</p>
  <p class="muted small">${esc(t.blurb)}</p>
</section>`;
}

// ---------- pages ----------
const pages = {};

// Landing dashboard
{
  const cards = TYPES.map((t) => {
    const list = BY_TYPE[t.id] || [];
    const flagged = list.filter((r) => r.flagCount).length;
    return `<a class="card cat" href="categories/${t.id}.html">
      <div class="cat-n">${list.length}</div>
      <div class="cat-t">${esc(t.name)}</div>
      <div class="muted small">${flagged} flagged · ${list.filter((r) => r.verification !== 'unverified').length} checked</div>
    </a>`;
  }).join('');
  const shortlistRows = SHORTLIST.map(
    (r) => `<li><a href="${esc(r.links[0].url)}" target="_blank" rel="noopener"><b>${esc(r.name)}</b></a> — ${verifBadge(r.verification)} <span class="muted small">${esc(r.typeName)} · ${esc(r.verificationFinding.split('. ')[0])}.</span> <a href="all.html#${esc(r.id)}">Row</a></li>`,
  ).join('');
  const body = `
<section class="hero">
  <h1>Free-to-enter cash-prize competitions</h1>
  <p class="lead">A verification dashboard for ${STATS.listings} competitions in ${STATS.categories} categories. Every row links to its official page. Prize values are shown only when an official page confirms them. Everything else is left blank and flagged.</p>
  <div class="actions">
    <a class="btn" href="all.html">Browse all ${STATS.listings} entries</a>
    <a class="btn ghost" href="flagged.html">Flagged for review (${STATS.flagged})</a>
    <a class="btn ghost" href="executive-summary.html">Executive summary</a>
  </div>
</section>

<section class="kpis wide" aria-label="Summary numbers">
  ${kpi(STATS.listings, 'Listings')}
  ${kpi(STATS.freeFull, 'Free path: full (ledger)')}
  ${kpi(STATS.verifiedTotal, `Checked on official pages (${STATS.pct}%)`, 'ok')}
  ${kpi(STATS.unverified, 'Unverified, prize blank', 'warn')}
  ${kpi(STATS.flagged, 'Rows flagged for review', 'warn')}
  ${kpi(STATS.high, 'High-severity rows', 'bad')}
</section>

<section>
  <h2>Categories</h2>
  <div class="grid cats">${cards}</div>
</section>

<section>
  <h2>Shortlist to read first</h2>
  <p class="muted">Rows that passed three checks: an official page was read and is not in conflict; free path is full (ledger); ledger says live; no high-severity flag. These are candidates to read first, not rankings. Prize values are shown only where the official page confirmed them.</p>
  <ul class="plain">${shortlistRows || '<li class="muted">No rows meet all three checks.</li>'}</ul>
</section>

<section class="callout">
  <h2>Before you enter anything</h2>
  <ul>
    <li>Official rules govern. Read them yourself before entering.</li>
    <li>Ledger values are from 2026-08-19 and have not been re-checked, except the rows marked above.</li>
    <li>Sportsbook, casino and real-money DFS contests are excluded by the source's own policy. Several listed rows conflict with that policy (see Flagged).</li>
    <li>Prize winners may owe tax paperwork. US prizes of $600 or more typically need a W-9. Taxes are the winner's responsibility.</li>
  </ul>
</section>`;
  pages['index.html'] = layout({ title: 'Home', root: '', active: 'home', body });
}

// Category pages
for (const t of TYPES) {
  const list = BY_TYPE[t.id] || [];
  const body = `
<p class="crumbs"><a href="../index.html">Home</a> / ${esc(t.name)}</p>
<h1>${esc(t.name)}</h1>
${categoryAnalysis(t)}
<section>
  <h2>Entries (${list.length})</h2>
  ${list.length ? tableHtml(list, { showCategory: false, id: `t-${t.id}`, root: '../' }) : '<p class="muted">No entries.</p>'}
</section>`;
  pages[`categories/${t.id}.html`] = layout({ title: t.name, root: '../', active: 'cat', body });
}

// All entries
{
  const catOpts = TYPES.map((t) => `<option value="${t.id}">${esc(t.name)} (${(BY_TYPE[t.id] || []).length})</option>`).join('');
  const body = `
<h1>All entries</h1>
<p class="muted">${STATS.listings} rows. Each row links to its official page. "Prize on official page" is blank wherever no official page value has been confirmed.</p>
<div class="table-tools">
  <label class="search">Search <input type="search" data-filter="all" placeholder="Name, status, verification…" aria-label="Filter table"></label>
  <label>Category <select data-cat-filter="all" aria-label="Filter by category"><option value="">All categories</option>${catOpts}</select></label>
  <label>Verification <select data-verif-filter="all" aria-label="Filter by verification">
    <option value="">All</option>${Object.entries(VERIF_LABEL).map(([k, v]) => `<option value="${k}">${esc(v)}</option>`).join('')}
  </select></label>
  <span class="count" data-count-for="all">${rows.length} rows</span>
</div>
<div class="table-wrap">
<table class="data" id="all" data-table>
<thead><tr><th>Contest</th><th>Category</th><th>Free path</th><th>Status</th><th>Prize on official page</th><th>Verification</th><th>Official sources</th><th>Flags</th></tr></thead>
<tbody>
${rows.map((r) => rowHtml(r, { showCategory: true })).join('\n')}
</tbody>
</table>
</div>`;
  pages['all.html'] = layout({ title: 'All entries', root: '', active: 'all', body });
}

// Flagged for review
{
  const irr = REVIEW.irregularities
    .map(
      (i) => `<tr id="${esc(i.id)}"><td>${esc(i.id)}</td><td>${sevBadge(i.severity)}</td><td><b>${esc(i.title)}</b><div>${esc(i.detail)}</div></td><td>${(i.links || []).map((l) => `<a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)}</a>`).join('<br>') || '<span class="muted">—</span>'}</td></tr>`,
    )
    .join('\n');
  const flaggedRows = rows.filter((r) => r.flagCount).sort((a, b) => (SEV_RANK[b.maxSeverity] || 0) - (SEV_RANK[a.maxSeverity] || 0));
  const rowFlagHtml = flaggedRows
    .map(
      (r) => `<div class="flag-card" id="${esc(r.id)}">
  <div class="flag-head"><b>${esc(r.name)}</b> <span class="muted small">${esc(r.id)} · ${esc(r.typeName)}</span> ${sevBadge(r.maxSeverity)} ${verifBadge(r.verification)}</div>
  <ul>${r.flags.map((f) => `<li>${sevBadge(f.severity)} ${esc(f.text)}</li>`).join('')}</ul>
  <div class="small">Official links: ${r.links.map((l) => `<a href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.label)}</a>`).join(' · ')}</div>
</div>`,
    )
    .join('\n');
  const unverifiedRows = rows
    .filter((r) => r.verification === 'unverified')
    .map(
      (r) => `<tr id="u-${esc(r.id)}"><td><b>${esc(r.name)}</b><div class="muted small">${esc(r.id)} · ${esc(r.typeName)}</div></td><td><span class="badge v-unverified">UNVERIFIED</span> ${esc(r.ledgerPrizeClaim || 'No prize recorded')}</td><td><a href="${esc(r.links[0].url)}" target="_blank" rel="noopener">Official page</a></td></tr>`,
    )
    .join('\n');
  const body = `
<div class="banner warn-banner"><b>FLAGGED FOR REVIEW.</b> Publishing this page is part of the brief. Items here are not verified, may be wrong, or may conflict with the source's own policy. Nothing on this page is a recommendation. Unverified ledger prize claims appear below only so you can check them; they are labelled UNVERIFIED and are never shown elsewhere on the site.</div>
<h1>Flagged for review</h1>
<p class="muted">Checked ${CHECKED_ON}. Counts: ${STATS.high} high-severity rows, ${STATS.medium} medium, ${STATS.low} low; ${STATS.highIrregularities} high-severity repo or source irregularities. Issues are grouped below: repo and source irregularities, then row-level flags, then the unverified prize claims.</p>

<section>
  <h2>A. Repo and source irregularities (${REVIEW.irregularities.length})</h2>
  <div class="table-wrap"><table class="data simple"><thead><tr><th>ID</th><th>Severity</th><th>Finding</th><th>Links for manual review</th></tr></thead><tbody>${irr}</tbody></table></div>
</section>

<section>
  <h2>B. Row-level flags (${flaggedRows.length} rows)</h2>
  ${rowFlagHtml}
</section>

<section>
  <h2>C. Unverified ledger prize claims (${unverifiedRows.split('<tr').length - 1} rows)</h2>
  <p class="muted">These are ledger claims, not verified values. They appear here only so you can check them against the linked official page. They do not appear in any verified column.</p>
  <div class="table-wrap"><table class="data simple"><thead><tr><th>Contest</th><th>Ledger prize claim</th><th>Official page</th></tr></thead><tbody>${unverifiedRows}</tbody></table></div>
</section>`;
  pages['flagged.html'] = layout({ title: 'Flagged for review', root: '', active: 'flagged', body });
}

// Executive summary
{
  const topFindings = [
    `The source ledger (${STATS.listings} listings, last checked 2026-08-19) is internally consistent with its own totals: ${STATS.freeFull} entries are "full free path", ${STATS.live} are "live", and the 62 iOS figure reconciles. But its data is 74 days old.`,
    `Only ${STATS.verifiedTotal} of ${STATS.listings} rows (${STATS.pct}%) were checked on an official page in this pass. The other ${STATS.unverified} rows have blank prize values and are flagged as unverified.`,
    `Of the ${STATS.verifiedTotal} rows checked: ${STATS.verified} verified, ${STATS.partial} partially verified, ${STATS.conflict} in conflict with the official page, and ${STATS.broken} broken.`,
    'Policy conflict: the source excludes sportsbook, casino and real-money DFS contests. Fanatics Sportsbook, Andy\'s Bet Club and Gambling.com (casino games page) are still listed, and two of them are in the ledger\'s featured list.',
    'Broken link: Dirty Dozen (gambling.com) redirects to a casino games page. No contest is shown.',
    'Status conflicts: draft-pro is marked live, but its operator release says entries closed before 23 April 2026. The MLB Beat the Streak official rules end the contest with the 2026 regular season, which has passed.',
    'Prize conflicts: Checkmate Gaming shows $40 to $1,500 per free tournament, not the ledger\'s $10 to $180. Kaggle live prize pools reach $450,000, not "$5,000 to $100,000+".',
    `${STATS.fplThird} third-party league entries carry links to another operator\u2019s official site or to a third-party media site (R10). Those links are misleading until fixed.`,
    'No LICENSE exists in the upstream repo. Reuse rights for the listing data are unconfirmed.',
  ]
    .map((t) => `<li>${esc(t)}</li>`)
    .join('');
  const verifiedList = rows
    .filter((r) => r.verification !== 'unverified')
    .map((r) => `<li>${verifBadge(r.verification)} <a href="all.html#${esc(r.id)}"><b>${esc(r.name)}</b></a> — ${esc(r.verificationFinding)}</li>`)
    .join('');
  const body = `
<p class="crumbs"><a href="index.html">Home</a> / Executive summary</p>
<h1>Executive summary</h1>
<p class="muted">Prepared ${CHECKED_ON} from upstream ledger <a href="${SOURCE_REPO}">${esc(SOURCE_REPO.replace('https://', ''))}</a> (commit ${SOURCE_COMMIT.slice(0, 7)}, data as of 2026-08-19).</p>

<section class="callout">
  <h2>Bottom line</h2>
  <p>This is a usable catalogue of ${STATS.listings} free-to-enter competitions with real prizes across ${STATS.categories} categories. It is not yet a verified list. Only ${STATS.verifiedTotal} rows have been checked on an official page, and several important ledger claims are wrong or out of date. Use the shortlist as a starting point and check each official rule before you enter.</p>
</section>

<section>
  <h2>Key numbers</h2>
  <div class="kpis wide">
    ${kpi(STATS.listings, 'Listings')}
    ${kpi(STATS.freeFull, 'Free path: full')}
    ${kpi(STATS.live, 'Live (ledger)')}
    ${kpi(STATS.verifiedTotal, 'Checked on official pages', 'ok')}
    ${kpi(STATS.high, 'High-severity rows', 'bad')}
    ${kpi(STATS.highIrregularities, 'High-severity irregularities', 'bad')}
  </div>
</section>

<section>
  <h2>Findings</h2>
  <ul>${topFindings}</ul>
</section>

<section>
  <h2>What was checked, and what is confirmed</h2>
  <ul class="plain">${verifiedList}</ul>
</section>

<section>
  <h2>Recommended next steps for review</h2>
  <ol>
    <li>Decide whether the listing data can be republished. The upstream repo has no license.</li>
    <li>Remove or re-classify the sportsbook and casino rows: Fanatics Sportsbook, Andy's Bet Club, Oddspedia, Gambling.com, and the sportsbook-sponsored rows flagged on the Flagged page.</li>
    <li>Fix the draft-pro and MLB Beat the Streak status rows, and the Checkmate Gaming and Kaggle prize rows, using their official pages.</li>
    <li>Verify the remaining ${STATS.unverified} rows against official pages, starting with live rows that carry the largest prizes. Fill blanks only from official pages.</li>
    <li>Re-check annual photo awards and season contests before they are promoted.</li>
  </ol>
</section>

<section>
  <h2>Where to look next</h2>
  <p><a href="flagged.html">Flagged for review</a> · <a href="all.html">All entries</a> · <a href="methodology.html">Methodology and sources</a></p>
</section>`;
  pages['executive-summary.html'] = layout({ title: 'Executive summary', root: '', active: 'exec', body });
}

// Methodology
{
  const sourcesList = [
    ['Upstream ledger (snapshot)', SOURCE_REPO, 'Used for the listing structure only. Its values are unverified until shown in a verified column.'],
    ['Upstream live site', LIVE_SITE, 'Counts reconciled: 206 listings, 189 free-path full, 62 iOS, 60 added.'],
    ['ESPN NFL Pick\'em page', 'https://fantasy.espn.com/games/nfl-pickem-2026/picks', 'Prize and dates confirmed.'],
    ['ESPN College Pick\'em page', 'https://fantasy.espn.com/games/college-football-pickem-2026/picks', 'Prize and dates confirmed.'],
    ['ARC Prize homepage', 'https://arcprize.org/', 'Prize confirmed.'],
    ['MLB Beat the Streak', 'https://www.mlb.com/apps/beat-the-streak', 'Prize confirmed; end date conflicts.'],
    ['MLB Beat the Streak official rules', 'https://www.mlb.com/apps/beat-the-streak/official-rules', 'Linked for review.'],
    ['Metaculus tournaments', 'https://www.metaculus.com/tournaments/', 'Prize pool sample.'],
    ['CBS Sports Pro Football Pick\'em rules', 'https://www.cbssports.com/fantasy/football/games/pickem/rules', 'Free entry and dates confirmed; prize sections not read.'],
    ['Devpost hackathons', 'https://devpost.com/hackathons', 'Prize sample.'],
    ['Kaggle competitions', 'https://www.kaggle.com/competitions', 'Prize pools; conflict with ledger range.'],
    ['Checkmate Gaming free tournaments', 'https://www.checkmategaming.com/free-tournaments', 'Prize range; conflict with ledger.'],
    ['The Draft Pro press release (PR Newswire)', 'https://www.prnewswire.com/news-releases/the-draft-pro-launches-free-1-000-000-perfect-draft-challenge-ahead-of-the-2026-nfl-draft-302736409.html', 'Entries close before 23 April 2026; status conflict.'],
    ['Gambling.com games page (redirect target)', 'https://www.gambling.com/games', 'Redirect target of the dirty-dozen link.'],
  ]
    .map(([t, u, n]) => `<tr><td>${esc(t)}</td><td><a href="${esc(u)}" target="_blank" rel="noopener">${esc(u)}</a></td><td>${esc(n)}</td></tr>`)
    .join('');
  const body = `
<p class="crumbs"><a href="index.html">Home</a> / Methodology</p>
<h1>Methodology and sources</h1>
<h2>How the data is built</h2>
<ol>
  <li>The upstream ledger's <code>assets/data.js</code> was snapshotted unmodified (<code>data/source/ledger-data.js</code>, commit ${SOURCE_COMMIT.slice(0, 7)}).</li>
  <li>Each listing is loaded and checked against a verification record (<code>data/review.json</code>). Official pages were fetched on ${CHECKED_ON}.</li>
  <li>A value is shown as <b>verified</b> only when an official page confirms it on that date. Otherwise the prize cell is left blank and the row is flagged.</li>
  <li>Ledger values are kept, labelled "unverified", in expandable notes only. They never appear in a verified column.</li>
  <li>Flags come from this review, plus automatic checks: missing official source, http links, missing rules link, and the presence of promo codes (codes are not published).</li>
</ol>
<h2>Verification status</h2>
<table class="data simple"><thead><tr><th>Status</th><th>Meaning</th></tr></thead><tbody>
<tr><td>${verifBadge('verified')}</td><td>An official page was fetched on ${CHECKED_ON} and the stated value matched.</td></tr>
<tr><td>${verifBadge('partial')}</td><td>An official page was fetched. Some fields matched; the rest were not confirmed.</td></tr>
<tr><td>${verifBadge('conflict')}</td><td>An official page contradicts the ledger. The official value is shown.</td></tr>
<tr><td>${verifBadge('broken')}</td><td>The ledger link does not show the claimed contest.</td></tr>
<tr><td>${verifBadge('unverified')}</td><td>Not checked against an official page in this pass. Prize blank.</td></tr>
</tbody></table>
<h2>Limits of this pass</h2>
<ul>
  <li>${STATS.verifiedTotal} of ${STATS.listings} rows were checked. The rest are unverified.</li>
  <li>Official pages were read with a page fetcher. Logins, eligibility tests and account sign-ups were not done.</li>
  <li>Pages were read as they stood on ${CHECKED_ON}. Contests can change.</li>
  <li>Rules pages can run to several sections. Where a prize section was not read, the prize is blank.</li>
</ul>
<h2>Sources used in this pass</h2>
<div class="table-wrap"><table class="data simple"><thead><tr><th>Source</th><th>Link</th><th>Use</th></tr></thead><tbody>${sourcesList}</tbody></table></div>
<h2>Reproduce</h2>
<p><code>node scripts/build.mjs</code> then <code>node scripts/check.mjs</code>. Output is written to <code>_site/</code>. The site is deployed by GitHub Pages from <code>.github/workflows/pages.yml</code>.</p>`;
  pages['methodology.html'] = layout({ title: 'Methodology', root: '', active: 'method', body });
}

// 404
pages['404.html'] = layout({
  title: 'Not found',
  root: '',
  active: '',
  body: '<h1>Page not found</h1><p><a href="index.html">Back to home</a></p>',
});

// ---------- write ----------
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(path.join(OUT, 'categories'), { recursive: true });
fs.mkdirSync(path.join(OUT, 'assets'), { recursive: true });
fs.mkdirSync(path.join(OUT, 'data'), { recursive: true });
for (const [rel, html] of Object.entries(pages)) fs.writeFileSync(path.join(OUT, rel), html);
fs.copyFileSync(path.join(ROOT, 'site/assets/style.css'), path.join(OUT, 'assets/style.css'));
fs.copyFileSync(path.join(ROOT, 'site/assets/app.js'), path.join(OUT, 'assets/app.js'));
fs.writeFileSync(path.join(OUT, '.nojekyll'), '');
fs.writeFileSync(
  path.join(OUT, 'data/listings.json'),
  JSON.stringify({ checkedOn: CHECKED_ON, sourceCommit: SOURCE_COMMIT, stats: STATS, rows, irregularities: REVIEW.irregularities }, null, 2),
);

console.log(JSON.stringify(STATS, null, 2));
console.log(`Wrote ${Object.keys(pages).length} pages to ${path.relative(ROOT, OUT)}/`);
