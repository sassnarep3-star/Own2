#!/usr/bin/env node
// External link-rot report. Run on a machine with unrestricted internet (the build sandbox could not reach most hosts).
// Usage: node tools/linkcheck-external.js > data/external-linkcheck.json   (Node 18+)
const fs = require('fs');
const L = JSON.parse(fs.readFileSync(__dirname + '/../data/raw/source-ledger.json', 'utf8')).listings;
const urls = new Map();
L.forEach(x => [x.signupUrl, x.iosUrl, x.tosUrl, x.rulesUrl, ...x.sources.map(s => s.url)].filter(Boolean).forEach(u => { if (!urls.has(u)) urls.set(u, []); urls.get(u).push(x.id); }));
(async () => {
  const out = []; const q = [...urls.keys()]; let i = 0;
  async function worker() { while (i < q.length) { const u = q[i++]; let r; try { const c = new AbortController(); setTimeout(() => c.abort(), 15000); const res = await fetch(u, { method: 'GET', redirect: 'follow', signal: c.signal, headers: { 'user-agent': 'Mozilla/5.0 linkcheck' } }); r = { status: res.status, finalUrl: res.url }; } catch (e) { r = { status: 0, error: String(e.message || e) }; } out.push({ url: u, entries: urls.get(u), ...r }); } }
  await Promise.all(Array.from({ length: 8 }, worker));
  out.sort((a, b) => a.url.localeCompare(b.url));
  console.log(JSON.stringify({ generated: new Date().toISOString(), total: out.length, notOk: out.filter(o => o.status < 200 || o.status >= 400).length, results: out }, null, 1));
})();
