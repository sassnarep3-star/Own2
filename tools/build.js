#!/usr/bin/env node
// Static site generator. Inputs: data/raw/*.json, data/verification/verified.json, data/analysis.json, EXECUTIVE_SUMMARY.md
// Outputs: data/ledger.json, data/ledger.csv, *.html in the repo root. No network. Usage: node tools/build.js
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const rd = f => JSON.parse(fs.readFileSync(path.join(ROOT, f), 'utf8'));
const SRC = rd('data/raw/source-ledger.json');
const OFF = rd('data/raw/offline-findings.json');
const VER = rd('data/verification/verified.json');
const BUILD_DATE = VER.checkedOn;
const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const host = u => { try { return new URL(u).hostname.replace(/^www\./, ''); } catch { return ''; } };
const typeName = id => (SRC.types.find(t => t.id === id) || {}).name || id;

// ---------- merge ----------
const flagsById = {};
OFF.findings.forEach(f => (flagsById[f.id] = flagsById[f.id] || []).push(f));
const entries = SRC.listings.map(x => {
  const v = VER.entries[x.id];
  const officialSrc = x.sources.find(s => s.tier === 'official');
  const verifiedPage = v && v.pages.find(p => /^read/.test(p.result));
  const link = verifiedPage
    ? { url: verifiedPage.url, label: host(verifiedPage.url), trust: 'checked' }
    : officialSrc
      ? { url: officialSrc.url, label: host(officialSrc.url), trust: 'ledger-labelled' }
      : { url: x.signupUrl, label: host(x.signupUrl), trust: 'no-official-source' };
  const state = !v ? 'unverified' : (v.pages.some(p => /^read/.test(p.result)) ? 'verified' : 'unreachable');
  return {
    id: x.id, name: x.name, type: x.type, category: typeName(x.type),
    link, signupUrl: x.signupUrl, rulesUrl: x.rulesUrl || null, tosUrl: x.tosUrl || null, iosUrl: x.iosUrl || null,
    verification: { state, checkedOn: v ? VER.checkedOn : null, pages: v ? v.pages : [], confirmed: v ? v.confirmed : null, discrepancies: v ? v.discrepancies : [] },
    ledgerClaims: { status: x.status, freePath: x.freePath, prize: x.prizeUsd, prizeNote: x.prizeNote, minCashout: x.minCashout, eligibility: x.eligibility, restricted: x.restricted, platforms: x.platforms, lastChecked: x.lastChecked, sources: x.sources },
    flags: (flagsById[x.id] || []).filter(f => f.severity !== 'info').map(f => ({ code: f.code, severity: f.severity, detail: f.detail }))
  };
});
entries.forEach(e => { if (!e.link.url) throw new Error('row without link: ' + e.id); });

const stats = {
  total: entries.length,
  verified: entries.filter(e => e.verification.state === 'verified').length,
  unreachable: entries.filter(e => e.verification.state === 'unreachable').length,
  unverified: entries.filter(e => e.verification.state === 'unverified').length,
  uniqueUrls: OFF.uniqueUrls,
  noOfficial: entries.filter(e => e.link.trust === 'no-official-source').length,
  ledgerEnded: SRC.listings.filter(l => l.status === 'ended').length,
  ledgerEndedFull: SRC.listings.filter(l => l.status === 'ended' && l.freePath === 'full').length,
  ledgerFull: SRC.listings.filter(l => l.freePath === 'full').length,
  verifiedDiscrepancyEntries: entries.filter(e => e.verification.state === 'verified' && e.verification.discrepancies.length).length,
  byType: SRC.types.map(t => ({ id: t.id, name: t.name, n: entries.filter(e => e.type === t.id).length }))
};
const tok = { total: stats.total, verified: stats.verified, unreachable: stats.unreachable, unverified: stats.unverified, verifiedWithDiscrepancy: stats.verifiedDiscrepancyEntries, ledgerFull: stats.ledgerFull, ledgerEndedFull: stats.ledgerEndedFull };
const ANA = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/analysis.json'), 'utf8').replace(/\{(\w+)\}/g, (m, k) => { if (!(k in tok)) throw new Error('unknown token ' + k); return tok[k]; }));
// computed irregularities
const fplGeneric = SRC.listings.filter(l => host(l.signupUrl) === 'fantasy.premierleague.com').map(l => l.id);
const appStore = SRC.listings.filter(l => host(l.signupUrl) === 'apps.apple.com').map(l => l.id);
ANA.repoIrregularities.push({ title: 'Generic platform pages used as the "official" link for third-party contests', evidence: `${fplGeneric.length} entries use the generic Fantasy Premier League home page (fantasy.premierleague.com) as signup link — ${fplGeneric.join(', ')} — which cannot confirm a third-party league's prize or rules. ${appStore.length} entries use an App Store page as signup link (${appStore.join(', ')}).`, links: [['fantasy.premierleague.com', 'https://fantasy.premierleague.com/']], sev: 'medium' });
fs.mkdirSync(path.join(ROOT, 'data'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'data/ledger.json'), JSON.stringify({ generated: BUILD_DATE, sourceCommit: fs.readFileSync(path.join(ROOT, 'data/raw/SOURCE_COMMIT.txt'), 'utf8').trim(), note: 'ledgerClaims are carried over from the source repo and are NOT verified unless verification.state === "verified" (then see verification.confirmed).', stats, entries }, null, 1) + '\n');
const csvCell = s => '"' + String(s == null ? '' : s).replace(/"/g, '""') + '"';
fs.writeFileSync(path.join(ROOT, 'data/ledger.csv'), ['id,name,category,official_link,link_trust,verification_state,checked_on,confirmed_prize,confirmed_free_entry,confirmed_eligibility,confirmed_deadline,confirmed_state,flag_count']
  .concat(entries.map(e => { const c = e.verification.confirmed || {}; return [e.id, e.name, e.category, e.link.url, e.link.trust, e.verification.state, e.verification.checkedOn, c.prize, c.freeEntry, c.eligibility, c.deadline, c.state, e.flags.length].map(csvCell).join(','); })).join('\n') + '\n');

// ---------- layout ----------
const NAV = [['index.html', 'Home'], ['top-picks.html', 'Top picks'], ['categories.html', 'Categories'], ['all.html', 'All entries'], ['summary.html', 'Executive summary'], ['flagged.html', 'Flagged for review'], ['methodology.html', 'Method']];
const page = (file, title, body, opts = {}) => {
  const nav = NAV.map(([f, t]) => `<a href="${f}"${(f === file || (opts.navActive === f)) ? ' aria-current="page"' : ''}>${t}</a>`).join('');
  const html = `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} · Free Cash Contest Dashboard</title>
<meta name="description" content="${esc(opts.desc || 'Verified-or-blank dashboard of free-to-enter cash prize competitions. Every row links to an official source; unverified values are left blank and flagged.')}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%231f6f4a'/%3E%3Ctext x='32' y='45' font-size='38' text-anchor='middle' fill='white' font-family='sans-serif'%3E$%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="assets/site.css"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar"><a class="brand" href="index.html"><span class="mark">$</span><span>Free Cash Contest<br><small>Dashboard · checked ${BUILD_DATE}</small></span></a>
<nav aria-label="Main">${nav}</nav></div></header>
<main id="main" class="wrap">${body}</main>
<footer class="wrap foot"><p>Independent research compilation — not affiliated with any listed operator. Official rules always govern; confirm every figure on the linked official page before entering. Values not confirmed from an official source are blank and marked <b>Unverified</b>. Data: <a href="data/ledger.json">ledger.json</a> · <a href="data/ledger.csv">ledger.csv</a> · <a href="https://github.com/sassnarep3-star/Own2">Repository</a>.</p></footer>
${opts.script ? `<script src="assets/table.js"></script>` : ''}</body></html>`;
  fs.writeFileSync(path.join(ROOT, file), html);
};

const stateBadge = s => ({ open: '<span class="b ok">Open</span>', closing: '<span class="b warn">Closing soon</span>', closed: '<span class="b bad">Closed</span>', unknown: '<span class="b mute">Status unconfirmed</span>' }[s] || '');
const trustBadge = e => e.link.trust === 'checked' ? `<span class="b ok" title="Page was fetched and read on ${BUILD_DATE}">checked ${BUILD_DATE}</span>`
  : e.link.trust === 'ledger-labelled' ? '<span class="b mute" title="Labelled official in the source ledger; link not re-fetched in this review">not re-checked</span>'
  : '<span class="b bad" title="No source in the original ledger is labelled official">no official source</span>';
const long = (s, n = 150) => !s ? '' : s.length <= n ? esc(s) : `<details><summary>${esc(s.slice(0, n).replace(/\s+\S*$/, ''))}… <u>more</u></summary>${esc(s)}</details>`;
const claim = (label, v) => v ? `<span class="claim" title="Unverified claim from the original ledger">${esc(label)}: ${esc(v)}</span>` : '';

function row(e) {
  const c = e.verification.confirmed;
  const ver = e.verification.state;
  const vb = ver === 'verified' ? `<span class="b ok">Verified ${BUILD_DATE}</span>` : ver === 'unreachable' ? '<span class="b bad">Unreachable</span>' : '<span class="b flag">Unverified</span>';
  const status = c ? stateBadge(c.state) : '';
  const free = c && c.freeEntry === true ? '<span class="b ok">Free (confirmed)</span>' : '';
  const lc = e.ledgerClaims;
  const disc = e.verification.discrepancies.length ? `<details class="disc"><summary>${e.verification.discrepancies.length} discrepancy vs. ledger</summary><ul>${e.verification.discrepancies.map(d => `<li>${esc(d)}</li>`).join('')}</ul></details>` : '';
  const links = `<a class="out" href="${esc(e.link.url)}" rel="noopener noreferrer" target="_blank">${esc(e.link.label)} ↗</a> ${trustBadge(e)}`;
  const flagTxt = e.flags.length ? `<a class="fl" href="flagged.html#e-${esc(e.id)}">${e.flags.length} flag${e.flags.length > 1 ? 's' : ''}</a>` : '';
  const search = (e.name + ' ' + e.category + ' ' + (c && c.prize || '')).toLowerCase();
  return `<tr id="${esc(e.id)}" data-v="${ver}" data-s="${c ? c.state : ''}" data-q="${esc(search)}">
<td data-l="Contest"><b>${esc(e.name)}</b><br><small>${esc(e.category)}</small> ${flagTxt}</td>
<td data-l="Verification">${vb}${status ? '<br>' + status : ''}</td>
<td data-l="Prize (confirmed)">${c && c.prize ? long(c.prize) : ''}${claim('ledger says', lc.prize)}</td>
<td data-l="Entry">${free}${claim('ledger says', lc.freePath === 'full' ? 'free USD path' : lc.freePath === 'partial' ? 'some free events' : 'cash needs entry fee')}</td>
<td data-l="Eligibility">${c && c.eligibility ? long(c.eligibility, 110) : ''}${claim('ledger says', lc.eligibility)}</td>
<td data-l="Dates">${c && c.deadline ? long(c.deadline, 110) : ''}</td>
<td data-l="Official source">${links}${disc}</td></tr>`;
}
const THEAD = '<thead><tr><th>Contest</th><th>Verification</th><th>Prize (confirmed)</th><th>Entry</th><th>Eligibility</th><th>Dates</th><th>Official source</th></tr></thead>';
const controls = `<div class="controls" role="search"><input id="q" type="search" placeholder="Search contests…" aria-label="Search contests">
<select id="fv" aria-label="Verification filter"><option value="">All rows</option><option value="verified">Verified only</option><option value="unverified">Unverified only</option></select>
<select id="fs" aria-label="Status filter"><option value="">Any status</option><option value="open">Open</option><option value="closing">Closing soon</option><option value="closed">Closed</option></select>
<label class="chk"><input id="claims" type="checkbox"> Show unverified claims from the original ledger</label><span id="count" class="cnt"></span></div>`;
const tableBlock = list => `${controls}<div class="tablewrap"><table class="t">${THEAD}<tbody>${list.map(row).join('')}</tbody></table></div><p class="note">Blank cells = not confirmed from an official source. Grey italic text (when shown) is the original ledger's unverified claim and must not be relied on.</p>`;

// ---------- pages ----------
const fmt = n => n.toLocaleString('en-US');
const catCards = SRC.types.map(t => { const list = entries.filter(e => e.type === t.id); const v = list.filter(e => e.verification.state === 'verified').length;
  return `<a class="card cat" href="cat-${t.id}.html"><h3>${esc(t.name)}</h3><p>${esc(t.blurb)}</p><p class="meta"><b>${list.length}</b> entries · <b>${v}</b> verified</p></a>`; }).join('');

const picks = ANA.topPicks.map(p => ({ ...p, e: entries.find(e => e.id === p.id) }));
picks.forEach(p => { if (!p.e) throw new Error('top pick refers to unknown id ' + p.id); if (p.e.verification.state !== 'verified') throw new Error('top pick must be verified: ' + p.id); });
const pickCard = (p, i) => { const c = p.e.verification.confirmed; return `<article class="card pick"><div class="rank">${i + 1}</div><div><h3>${esc(p.title)}</h3>
<p>${stateBadge(c.state)} ${c.freeEntry ? '<span class="b ok">Free (confirmed)</span>' : '<span class="b mute">Free entry not confirmed</span>'} <span class="b mute">${esc(p.e.category)}</span></p>
<p><b>Confirmed on the official page:</b> ${esc(p.headline)}</p>
<p><b>Dates:</b> ${esc(c.deadline || '')}</p>
<p class="analysis"><b>Analysis (not an official fact):</b> ${esc(p.analysis)}</p>
${p.caveats ? `<p class="caveat"><b>Check before entering:</b> ${esc(p.caveats)}</p>` : ''}
<p><a class="btn" href="${esc(p.e.link.url)}" rel="noopener noreferrer" target="_blank">Official page ↗</a> <a href="all.html#${esc(p.id)}">Full row</a></p></div></article>`; };

page('index.html', 'Home', `
<section class="hero"><h1>Free-to-enter cash competitions — organised, sourced, honest.</h1>
<p class="lede">A mobile-friendly dashboard built from the <a href="https://github.com/karagemop466-tech/FreeMoneyApps">FreeMoneyApps</a> ledger. Every row links to an official page. Values that could not be confirmed from an official source are <b>left blank and flagged</b> — nothing is inferred or filled in.</p>
<p><a class="btn big" href="top-picks.html">See the best bets right now →</a> <a class="btn ghost big" href="categories.html">Browse categories</a></p></section>
<section class="stats" aria-label="Key numbers">
<div class="stat"><b>${stats.total}</b><span>entries in the ledger</span></div>
<div class="stat ok"><b>${stats.verified}</b><span>re-verified live on ${BUILD_DATE}</span></div>
<div class="stat warn"><b>${stats.unverified + stats.unreachable}</b><span>not yet verified (flagged)</span></div>
<div class="stat bad"><b>${stats.verifiedDiscrepancyEntries}</b><span>of the ${stats.verified} readable entries showed a discrepancy vs. the old ledger</span></div></section>
<section class="alert"><b>Read this first.</b> Of ${stats.total} ledger entries, only ${stats.verified} could be re-read on their official pages in this review (${stats.unreachable} more could not be read by a non-browser fetch). Of those ${stats.verified}, ${entries.filter(e => e.verification.state === 'verified' && e.verification.discrepancies.length).length} showed stale or contradicting data in the old ledger (closed entries, changed prizes, changed names). Treat every unverified row as a lead, not a fact. See <a href="flagged.html">Flagged for review</a>.</section>
<h2>Best bets right now <small>(verified ${BUILD_DATE}, open, official source)</small></h2>
<div class="picks">${picks.slice(0, 4).map(pickCard).join('')}</div><p><a href="top-picks.html">All ${picks.length} top picks and how they were chosen →</a></p>
<h2>Browse by category</h2><div class="cats">${catCards}</div>
<h2>Key findings</h2><ul class="find">${ANA.keyFindings.map(f => `<li>${f}</li>`).join('')}</ul>
`, { desc: 'Dashboard of free-to-enter cash prize competitions with official source links; unverified values left blank and flagged.' });

page('top-picks.html', 'Top picks', `<h1>Top picks right now</h1>
<p class="lede">Only entries that were <b>re-read on their official pages on ${BUILD_DATE}</b> can appear here. Facts come from those pages; the "Analysis" lines are our own judgement and are labelled as such.</p>
<div class="alert"><b>How these were chosen.</b> ${esc(ANA.method)}</div>
<div class="picks">${picks.map(pickCard).join('')}</div>
<h2>Checked, but not on the top-picks list</h2><div class="tablewrap"><table class="t simple"><thead><tr><th>Contest</th><th>What the official page showed</th><th>Source</th></tr></thead><tbody>${ANA.notActionable.map(n => { const e = entries.find(x => x.id === n.id); if (!e) throw new Error('unknown ' + n.id); return `<tr><td data-l="Contest"><b>${esc(e.name)}</b></td><td data-l="Finding">${esc(n.why)}</td><td data-l="Source"><a class="out" href="${esc(e.link.url)}" target="_blank" rel="noopener noreferrer">${esc(e.link.label)} ↗</a></td></tr>`; }).join('')}</tbody></table></div>`, { desc: 'Best free-to-enter cash competitions verified on official pages.' });

page('categories.html', 'Categories', `<h1>Categories</h1><p class="lede">Nine categories carried over from the original ledger. Each subpage is a sortable-by-search table with official links.</p><div class="cats">${catCards}</div>`);
SRC.types.forEach(t => {
  const list = entries.filter(e => e.type === t.id).sort((a, b) => ({ verified: 0, unreachable: 1, unverified: 2 }[a.verification.state] - { verified: 0, unreachable: 1, unverified: 2 }[b.verification.state]) || a.name.localeCompare(b.name));
  page(`cat-${t.id}.html`, t.name, `<p class="crumb"><a href="categories.html">Categories</a> /</p><h1>${esc(t.name)}</h1><p class="lede">${esc(t.blurb)} <small>(category description carried over from the original ledger)</small></p>
<p>${list.length} entries · ${list.filter(e => e.verification.state === 'verified').length} verified on ${BUILD_DATE}.</p>${tableBlock(list)}`, { script: true, navActive: 'categories.html' });
});
page('all.html', 'All entries', `<h1>All ${entries.length} entries</h1><p class="lede">Verified rows first within each category. Use the filters to narrow the list.</p>${tableBlock([...entries].sort((a, b) => a.category.localeCompare(b.category) || ({ verified: 0, unreachable: 1, unverified: 2 }[a.verification.state] - { verified: 0, unreachable: 1, unverified: 2 }[b.verification.state]) || a.name.localeCompare(b.name)))}`, { script: true });

// ----- flagged page -----
const sevOrder = { high: 0, medium: 1, low: 2 };
const codeDesc = {
  NO_OFFICIAL_SOURCE: 'No source in the original ledger is tagged "official"', NON_OFFICIAL_SOURCE: 'A cited source is an affiliate/forum/third-party page, not the operator', OFFICIAL_TIER_DOMAIN_MISMATCH: 'Source tagged official but on a different domain than the signup/rules URL — confirm it is operator-owned',
  ENDED_BUT_COUNTED_FREE: 'Status "ended" but counted in the "True free paths" headline', NON_CASH_PRIZE_TAGGED_FREE_USD: 'Prize text mentions gift cards / merchandise / trips etc. but entry is tagged "Free USD path"', VIRTUAL_CURRENCY_TAGGED_FREE_USD: 'Prize text mentions points/coins/bonus currency but is tagged "Free USD path"',
  DATE_IN_PAST_REVIEW: 'Text references a date earlier than 2026-11-01 — status may be stale', CAUTION_BUT_FREE: 'Ledger status "caution" yet tagged free', FEE_MENTION_ON_FREE: 'Text mentions fee/deposit on a listing tagged free', URL_NOT_HTTPS: 'Link uses http://', NO_RULES_URL: 'No rules URL on the listing', VAGUE_VALUE: 'Prize or cash-out value is vague/unspecified in the ledger', PRIZE_NOT_QUANTIFIED: 'Prize figure not quantified'
};
const byCode = {}; OFF.findings.filter(f => f.severity !== 'info').forEach(f => (byCode[f.code] = byCode[f.code] || []).push(f));
const nameOf = id => (entries.find(e => e.id === id) || {}).name || id;
const verDisc = entries.filter(e => e.verification.discrepancies.length);
const flaggedBody = `<h1>Flagged for review</h1>
<p class="lede">Everything below needs a human look. None of it blocks the site. Each item links to the source that should be opened to settle it. Generated ${BUILD_DATE}.</p>
<nav class="toc"><a href="#repo">A. Repository irregularities</a><a href="#live">B. Live-verification discrepancies</a><a href="#coverage">C. Verification coverage</a><a href="#entries">D. Per-entry flags</a></nav>
<h2 id="repo">A. Irregularities in the source repository</h2>
<p>Reviewed: <a href="https://github.com/karagemop466-tech/FreeMoneyApps/tree/${esc(fs.readFileSync(path.join(ROOT, 'data/raw/SOURCE_COMMIT.txt'), 'utf8').trim())}">karagemop466-tech/FreeMoneyApps @ ${fs.readFileSync(path.join(ROOT, 'data/raw/SOURCE_COMMIT.txt'), 'utf8').trim().slice(0, 7)}</a> and its <a href="https://karagemop466-tech.github.io/FreeMoneyApps/">live site</a>.</p>
<div class="tablewrap"><table class="t simple"><thead><tr><th>#</th><th>Irregularity</th><th>Evidence / how to review</th><th>Severity</th></tr></thead><tbody>${ANA.repoIrregularities.map((r, i) => `<tr><td data-l="#">${i + 1}</td><td data-l="Irregularity">${esc(r.title)}</td><td data-l="Evidence">${esc(r.evidence)} ${r.links.map(l => `<a href="${esc(l[1])}" target="_blank" rel="noopener noreferrer">${esc(l[0])} ↗</a>`).join(' · ')}</td><td data-l="Severity"><span class="b ${r.sev === 'high' ? 'bad' : r.sev === 'medium' ? 'warn' : 'mute'}">${esc(r.sev)}</span></td></tr>`).join('')}</tbody></table></div>
<h2 id="live">B. Live-verification discrepancies (ledger vs official page, ${BUILD_DATE})</h2>
<div class="tablewrap"><table class="t simple"><thead><tr><th>Entry</th><th>Discrepancy</th><th>Official page checked</th></tr></thead><tbody>${verDisc.map(e => `<tr id="e-${esc(e.id)}-v"><td data-l="Entry"><b>${esc(e.name)}</b></td><td data-l="Discrepancy"><ul>${e.verification.discrepancies.map(d => `<li>${esc(d)}</li>`).join('')}</ul></td><td data-l="Page">${e.verification.pages.map(p => `<a href="${esc(p.url)}" target="_blank" rel="noopener noreferrer">${esc(host(p.url))} ↗</a> <small>(${esc(p.result)})</small>`).join('<br>')}</td></tr>`).join('')}</tbody></table></div>
<h2 id="coverage">C. Verification coverage</h2>
<ul><li><b>${stats.verified}</b> of ${stats.total} entries were re-read on an official page on ${BUILD_DATE}; <b>${stats.unreachable}</b> could not be read (JavaScript-only pages); <b>${stats.unverified}</b> were not checked and are shown as <b>Unverified</b> with blank values.</li>
<li>The ${stats.uniqueUrls} unique URLs in the ledger could <b>not</b> be machine-link-checked from the build environment (outbound network was restricted to GitHub/npm/PyPI hosts). Run <code>node tools/linkcheck-external.js</code> from an unrestricted machine to produce a link-rot report.</li>
<li>${stats.noOfficial} entries have no source tagged "official" in the original ledger; their row link is the ledger's signup URL, marked <span class="b bad">no official source</span>.</li></ul>
<h2 id="entries">D. Per-entry flags from the offline audit</h2>
<p>These were produced by <code>tools/audit.js</code> (no network). They are <i>review prompts</i>, not confirmed errors. Info-level notes (shared domains, non-US eligibility, Texas mentions) are kept in <a href="data/raw/offline-findings.json">offline-findings.json</a>.</p>
${Object.entries(byCode).sort((a, b) => b[1].length - a[1].length).map(([code, list]) => `<details class="grp"><summary><b>${esc(code)}</b> — ${list.length} entr${list.length > 1 ? 'ies' : 'y'}<br><small>${esc(codeDesc[code] || '')}</small></summary><div class="tablewrap"><table class="t simple"><thead><tr><th>Entry</th><th>Detail</th><th>Review link</th></tr></thead><tbody>${list.sort((a, b) => (sevOrder[a.severity] - sevOrder[b.severity])).map(f => { const e = entries.find(x => x.id === f.id); return `<tr id="e-${esc(f.id)}"><td data-l="Entry"><a href="all.html#${esc(f.id)}">${esc(nameOf(f.id))}</a></td><td data-l="Detail">${esc(f.detail)}</td><td data-l="Link"><a href="${esc(e.link.url)}" target="_blank" rel="noopener noreferrer">${esc(e.link.label)} ↗</a></td></tr>`; }).join('')}</tbody></table></div></details>`).join('')}`;
page('flagged.html', 'Flagged for review', flaggedBody, { desc: 'Irregularities, discrepancies and unverified items for manual review.' });

// ----- method -----
page('methodology.html', 'Method', `<h1>Method &amp; rules</h1>
${ANA.method_html}`, {});

// ----- summary -----
const md2html = md => {
  const lines = md.split('\n'); const out = []; let list = null, table = null;
  const inl = s => esc(s).replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>').replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\[([^\]]+)\]\(([^)]+)\)/g, (m, t, u) => `<a href="${u.replace(/&amp;/g, '&')}"${/^https?:/.test(u) ? ' target="_blank" rel="noopener noreferrer"' : ''}>${t}</a>`);
  const close = () => { if (list) { out.push('</ul>'); list = null; } if (table) { out.push('</tbody></table></div>'); table = null; } };
  for (const ln of lines) {
    if (/^#\s/.test(ln)) { close(); out.push(`<h1>${inl(ln.slice(2))}</h1>`); }
    else if (/^##\s/.test(ln)) { close(); out.push(`<h2>${inl(ln.slice(3))}</h2>`); }
    else if (/^###\s/.test(ln)) { close(); out.push(`<h3>${inl(ln.slice(4))}</h3>`); }
    else if (/^\s*[-*]\s/.test(ln)) { if (table) close(); if (!list) { out.push('<ul>'); list = true; } out.push(`<li>${inl(ln.replace(/^\s*[-*]\s/, ''))}</li>`); }
    else if (/^\|/.test(ln)) { if (list) close(); const cells = ln.replace(/^\||\|$/g, '').split('|').map(s => s.trim()); if (cells.every(c => /^:?-+:?$/.test(c))) continue; if (!table) { table = true; out.push(`<div class="tablewrap"><table class="t simple"><thead><tr>${cells.map(c => `<th>${inl(c)}</th>`).join('')}</tr></thead><tbody>`); } else out.push(`<tr>${cells.map(c => `<td>${inl(c)}</td>`).join('')}</tr>`); }
    else if (/^\s*$/.test(ln)) close();
    else { close(); out.push(`<p>${inl(ln)}</p>`); }
  }
  close(); return out.join('\n');
};
const execMd = fs.readFileSync(path.join(ROOT, 'EXECUTIVE_SUMMARY.md'), 'utf8');
page('summary.html', 'Executive summary', md2html(execMd), { desc: 'Executive summary of the free cash competition review.' });

page('404.html', 'Not found', `<h1>That page is not here</h1><p><a class="btn" href="index.html">Back to the dashboard</a></p>`);

// ----- audit markdown (T1 deliverable) -----
fs.mkdirSync(path.join(ROOT, 'audit'), { recursive: true });
const am = [];
am.push(`# Source repository review — karagemop466-tech/FreeMoneyApps @ ${fs.readFileSync(path.join(ROOT, 'data/raw/SOURCE_COMMIT.txt'), 'utf8').trim().slice(0, 7)}`, '', `Generated ${BUILD_DATE} by tools/build.js from data/analysis.json and data/verification/verified.json. Published with source links at flagged.html on the site.`, '', '## A. Repository irregularities', '');
ANA.repoIrregularities.forEach((r, i) => { am.push(`${i + 1}. **${r.title}** (${r.sev}) — ${r.evidence} ${r.links.map(l => `[${l[0]}](${l[1]})`).join(' · ')}`); });
am.push('', '## B. Live-verification discrepancies', '');
verDisc.forEach(e => { am.push(`- **${e.name}** — ${e.verification.discrepancies.join(' ')} Pages: ${e.verification.pages.map(p => `[${host(p.url)}](${p.url}) (${p.result})`).join('; ')}`); });
am.push('', '## C. Offline audit finding counts (tools/audit.js)', '', '| Code | Entries |', '|---|---|');
Object.entries(OFF.summary).sort((a, b) => b[1] - a[1]).forEach(([k, v]) => am.push(`| ${k} | ${v} |`));
fs.writeFileSync(path.join(ROOT, 'audit/SOURCE_REPO_REVIEW.md'), am.join('\n') + '\n');

fs.writeFileSync(path.join(ROOT, '.nojekyll'), '');
console.log('built', entries.length, 'entries;', stats.verified, 'verified;', Object.keys(byCode).length, 'flag codes');
module.exports = { stats };
