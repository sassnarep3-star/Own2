#!/usr/bin/env node
// Internal link check for the built site (no network): every relative href/src must exist; every #anchor must exist in its target;
// every data table row must contain an external official-source link (http links are accepted but counted). Exit 1 on any failure.
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const pages = fs.readdirSync(ROOT).filter(f => f.endsWith('.html'));
const ids = {};
pages.forEach(p => { const t = fs.readFileSync(path.join(ROOT, p), 'utf8'); ids[p] = new Set([...t.matchAll(/\sid="([^"]+)"/g)].map(m => m[1])); });
let bad = 0, checked = 0, rows = 0;
for (const p of pages) {
  const t = fs.readFileSync(path.join(ROOT, p), 'utf8');
  for (const m of t.matchAll(/(?:href|src)="([^"]*)"/g)) {
    const u = m[1]; if (/^(https?:|mailto:|data:)/.test(u) || u === '') continue;
    const [file, hash] = u.split('#'); const target = file || p; checked++;
    if (!fs.existsSync(path.join(ROOT, target))) { console.error(`BROKEN  ${p} -> ${u}`); bad++; continue; }
    if (hash && target.endsWith('.html') && !(ids[target] || new Set()).has(hash)) { console.error(`NO ANCHOR ${p} -> ${u}`); bad++; }
  }
  for (const m of t.matchAll(/<tr id="([^"]+)" data-v=[\s\S]*?<\/tr>/g)) {
    rows++; if (!/<a class="out" href="https?:\/\/[^"]+"/.test(m[0])) { console.error(`ROW WITHOUT OFFICIAL LINK ${p}#${m[1]}`); bad++; }
  }
}
console.log(`pages=${pages.length} internal links checked=${checked} table rows checked=${rows} problems=${bad}`);
process.exit(bad ? 1 : 0);
