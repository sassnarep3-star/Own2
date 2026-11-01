#!/usr/bin/env node
// Integration check: every dollar figure in a top pick's "headline" must appear in that entry's verified.json confirmed.prize text;
// every top pick must be a verified entry; verified entries must have at least one page marked read.
const fs = require('fs');
const V = JSON.parse(fs.readFileSync(__dirname + '/../data/verification/verified.json', 'utf8')).entries;
const A = JSON.parse(fs.readFileSync(__dirname + '/../data/analysis.json', 'utf8'));
let bad = 0;
const norm = s => s.replace(/\s+/g, ' ');
for (const p of A.topPicks) {
  const v = V[p.id]; if (!v) { console.error('not verified:', p.id); bad++; continue; }
  const prize = norm((v.confirmed.prize || '') + ' ' + (v.confirmed.quote || ''));
  const figs = p.headline.match(/[$€£]\d[\d,]*(?:\.\d+)?[KkMm]?/g) || [];
  for (const f of figs) if (!prize.includes(f)) { console.error(`pick ${p.id}: figure ${f} not in verified prize text`); bad++; }
  if (!v.pages.some(x => /^read/.test(x.result))) { console.error('no page read for', p.id); bad++; }
}
for (const [id, v] of Object.entries(V)) for (const pg of v.pages) if (!/^https:\/\//.test(pg.url)) { console.error('non-https page', id, pg.url); bad++; }
console.log('consistency problems:', bad); process.exit(bad ? 1 : 0);
