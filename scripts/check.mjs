// Verifies the generated site in _site/ against the rules in the brief. Exits non-zero on any failure.
//   1. Every listing appears exactly once in the all-entries table, with an official signup link.
//   2. Category pages together contain every listing once.
//   3. Every internal link and asset resolves to a file in _site/.
//   4. Verified prize cells contain only values that come from an official page (review.json), and
//      every unverified row shows a blank prize.
//   5. Verified or partial rows carry a checked-page link.
//   6. No placeholder or leaked-template strings (undefined, NaN, [object Object]).
//   7. Only https external links, except the one ledger link the Flagged page calls out (http://squarespool).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SITE = path.join(ROOT, '_site');
const data = JSON.parse(fs.readFileSync(path.join(SITE, 'data/listings.json'), 'utf8'));
const review = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/review.json'), 'utf8'));
const failures = [];
const notes = [];
const fail = (m) => failures.push(m);

function htmlFiles(dir, rel = '') {
  const out = [];
  for (const e of fs.readdirSync(path.join(dir, rel), { withFileTypes: true })) {
    const r = path.join(rel, e.name);
    if (e.isDirectory()) out.push(...htmlFiles(dir, r));
    else if (e.name.endsWith('.html')) out.push(r);
  }
  return out;
}
const pages = htmlFiles(SITE);
const read = (p) => fs.readFileSync(path.join(SITE, p), 'utf8');
const decode = (s) => s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");

// --- 1 & 2: row coverage ---
const all = read('all.html');
const allIds = [...all.matchAll(/<tr id="([^"]+)" data-verif="/g)].map((m) => m[1]);
if (allIds.length !== data.rows.length) fail(`all.html has ${allIds.length} rows; expected ${data.rows.length}`);
if (new Set(allIds).size !== allIds.length) fail('all.html has duplicate row ids');
for (const r of data.rows) {
  if (!allIds.includes(r.id)) fail(`row ${r.id} missing from all.html`);
  const signup = r.links[0] && r.links[0].url;
  if (!signup || !/^https?:\/\//.test(signup)) fail(`row ${r.id} has no official signup link`);
  if (signup && !all.includes(`href="${signup.replace(/&/g, '&amp;')}"`)) fail(`row ${r.id} signup link not rendered`);
}
let catRows = 0;
for (const t of new Set(data.rows.map((r) => r.type))) {
  const p = `categories/${t}.html`;
  if (!fs.existsSync(path.join(SITE, p))) { fail(`missing category page ${p}`); continue; }
  const n = [...read(p).matchAll(/<tr id="([^"]+)" data-verif="/g)].length;
  const expected = data.rows.filter((r) => r.type === t).length;
  if (n !== expected) fail(`${p} has ${n} rows; expected ${expected}`);
  catRows += n;
}
if (catRows !== data.rows.length) fail(`category pages hold ${catRows} rows in total; expected ${data.rows.length}`);

// --- 4: prize rule ---
const prizeCells = [...all.matchAll(/<td data-label="Prize on official page">([\s\S]*?)<\/td>/g)].map((m) => m[1]);
if (prizeCells.length !== data.rows.length) fail(`prize cells: ${prizeCells.length}; expected ${data.rows.length}`);
data.rows.forEach((r, i) => {
  const cell = prizeCells[i] || '';
  if (r.verification === 'unverified') {
    if (!cell.includes('Not verified')) fail(`unverified row ${r.id} shows a prize value`);
    if (r.prizeVerified) fail(`unverified row ${r.id} has a prizeVerified value`);
  } else if (r.prizeVerified) {
    if (!cell.includes(decode(r.prizeVerified).slice(0, 20).replace(/[&<>"']/g, ''))) {
      // cell is escaped; compare after decoding
      if (!decode(cell).includes(decode(r.prizeVerified).slice(0, 20))) fail(`verified prize for ${r.id} not rendered`);
    }
  }
  if (r.prizeVerified && !review.verified[r.id]) fail(`prize for ${r.id} has no official-page record`);
  if (['verified', 'partial', 'conflict'].includes(r.verification) && !review.verified[r.id].evidence) fail(`row ${r.id} has no evidence link`);
});

// --- 5: evidence link for checked rows
for (const r of data.rows) {
  if (r.verification !== 'unverified') {
    const ev = review.verified[r.id].evidence;
    if (!r.links.some((l) => l.url === ev)) fail(`checked row ${r.id} missing its evidence link in the rendered links`);
  }
}

// --- 3: internal links and assets ---
const hrefRe = /(?:href|src)="([^"]+)"/g;
for (const p of pages) {
  const html = read(p);
  for (const m of html.matchAll(hrefRe)) {
    const url = m[1];
    if (/^(https?:|mailto:|#)/.test(url)) continue;
    const clean = url.split('#')[0].split('?')[0];
    if (!clean) continue; // pure anchor after strip
    const target = path.normalize(path.join(path.dirname(p), clean));
    if (!fs.existsSync(path.join(SITE, target))) fail(`${p}: broken internal link ${url}`);
  }
  // --- 6: leaked template strings
  for (const bad of ['undefined', 'NaN', '[object Object]']) {
    if (html.includes(bad)) fail(`${p}: contains "${bad}"`);
  }
  // --- 7: external protocol check
  for (const m of html.matchAll(/href="(http:\/\/[^"]+)"/g)) {
    if (!/squarespool\.com/.test(m[1])) fail(`${p}: non-https external link ${m[1]}`);
    else notes.push(`${p}: non-https link flagged in ledger (${m[1]})`);
  }
  if (!/<html lang="en">/.test(html)) fail(`${p}: missing lang`);
  if (!/<title>[^<]+<\/title>/.test(html)) fail(`${p}: missing title`);
}

// Sanity: review record covers only known ids
for (const id of Object.keys(review.verified)) {
  if (!data.rows.some((r) => r.id === id)) fail(`review.json verified id ${id} is not a listing`);
}
for (const id of Object.keys(review.rowFlags)) {
  if (!data.rows.some((r) => r.id === id)) fail(`review.json flag id ${id} is not a listing`);
}

const result = { pages: pages.length, rows: data.rows.length, categoryRows: catRows, verifiedTotal: data.stats.verifiedTotal, unverified: data.stats.unverified, notes, failures };
console.log(JSON.stringify(result, null, 2));
if (failures.length) {
  console.error(`CHECK FAILED: ${failures.length} problem(s)`);
  process.exit(1);
}
console.log('CHECK PASSED');
