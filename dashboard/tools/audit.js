// Offline integrity audit of data/raw/source-ledger.json. No network. Writes data/raw/offline-findings.json
const fs = require('fs');
const L = JSON.parse(fs.readFileSync('data/raw/source-ledger.json', 'utf8'));
const TODAY = new Date('2026-11-01T00:00:00Z');
const MONTHS = {january:0,february:1,march:2,april:3,may:4,june:5,july:6,august:7,september:8,october:9,november:10,december:11,jan:0,feb:1,mar:2,apr:3,jun:5,jul:6,aug:7,sep:8,sept:8,oct:9,nov:10,dec:11};
const findings = []; // {id, code, severity, detail}
const add = (id, code, severity, detail) => findings.push({ id, code, severity, detail });
const host = u => { try { return new URL(u).hostname.replace(/^www\./, ''); } catch { return null; } };
const root = h => h ? h.split('.').slice(-2).join('.') : h;
const text = x => [x.short, x.prizeUsd, x.prizeNote, x.minCashout, x.eligibility, x.restricted, ...(x.redFlags||[]), ...(x.tosNotes||[])].join(' | ');

for (const x of L.listings) {
  // URL checks
  const urls = [['signupUrl', x.signupUrl], ['iosUrl', x.iosUrl], ['tosUrl', x.tosUrl], ['rulesUrl', x.rulesUrl], ...x.sources.map((s,i)=>['sources['+i+']', s.url])].filter(p=>p[1]);
  for (const [k,u] of urls) {
    if (!/^https:\/\//.test(u)) add(x.id, 'URL_NOT_HTTPS', 'medium', `${k}: ${u}`);
    if (!host(u)) add(x.id, 'URL_INVALID', 'high', `${k}: ${u}`);
  }
  if (!x.rulesUrl) add(x.id, 'NO_RULES_URL', 'medium', 'No rulesUrl on listing');
  // tier vs domain
  const sh = root(host(x.signupUrl));
  const officialHosts = new Set([sh, root(host(x.rulesUrl)), root(host(x.tosUrl)), root(host(x.iosUrl))].filter(Boolean));
  x.sources.forEach(s => {
    const h = root(host(s.url));
    if (s.tier === 'official' && h && !officialHosts.has(h)) add(x.id, 'OFFICIAL_TIER_DOMAIN_MISMATCH', 'low', `source "${s.title}" tier=official but domain ${h} differs from signup/rules domains (${[...officialHosts].join(', ')})`);
    if (s.tier !== 'official') add(x.id, 'NON_OFFICIAL_SOURCE', s.tier==='forum'?'high':'medium', `source "${s.title}" tier=${s.tier} (${s.url})`);
  });
  if (!x.sources.some(s => s.tier === 'official')) add(x.id, 'NO_OFFICIAL_SOURCE', 'high', 'No source with tier=official');
  // staleness / dates
  const t = text(x);
  const re = /(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|sept|october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|oct|nov|dec)\.?,?\s+(20\d\d)|(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2}),?\s+(20\d\d)|(20\d\d)-(\d\d)-(\d\d)/gi;
  let m;
  while ((m = re.exec(t))) {
    let d;
    if (m[1]) d = new Date(Date.UTC(+m[3], MONTHS[m[2].toLowerCase()], +m[1]));
    else if (m[4]) d = new Date(Date.UTC(+m[6], MONTHS[m[4].toLowerCase()], +m[5]));
    else d = new Date(Date.UTC(+m[7], +m[8]-1, +m[9]));
    if (d < TODAY && x.lastChecked !== m[0] && m[0] !== x.lastChecked && !/effective|updated|checked|ToS|Terms|rules/i.test(t.substr(Math.max(0,m.index-40),40)+t.substr(m.index,60)))
      add(x.id, 'DATE_IN_PAST_REVIEW', 'low', `text mentions ${m[0]} (before 2026-11-01): "${t.substr(Math.max(0,m.index-50),110).replace(/\s+/g,' ')}"`);
  }
  // consistency
  if (x.status === 'ended' && x.freePath === 'full') add(x.id, 'ENDED_BUT_COUNTED_FREE', 'medium', 'status=ended but freePath=full (counted in "True free paths" headline)');
  if (x.status === 'caution' && x.freePath === 'full') add(x.id, 'CAUTION_BUT_FREE', 'low', 'status=caution with freePath=full');
  if (/gift ?card|amazon|voucher|merch|trip|tickets?\b|gear|credit/i.test(x.prizeUsd) && x.freePath === 'full') add(x.id, 'NON_CASH_PRIZE_TAGGED_FREE_USD', 'medium', `prizeUsd mentions non-cash item but freePath="Free USD path": "${x.prizeUsd}"`);
  if (/bonus cash|gems?\b|coins?\b|tokens?\b|points/i.test(x.prizeUsd) && x.freePath === 'full') add(x.id, 'VIRTUAL_CURRENCY_TAGGED_FREE_USD', 'medium', `prizeUsd mentions virtual currency: "${x.prizeUsd}"`);
  if (/entry fee|deposit|paid entry|buy-?in/i.test(text(x)) && x.freePath === 'full') add(x.id, 'FEE_MENTION_ON_FREE', 'low', 'Text mentions fee/deposit on a "full" free listing: ' + (text(x).match(/.{0,50}(entry fee|deposit|paid entry|buy-?in).{0,50}/i)||[''])[0].replace(/\s+/g,' '));
  if (!/\d/.test(x.prizeUsd) && !/cash|prize|usd|\$/i.test(x.prizeUsd)) add(x.id, 'PRIZE_NOT_QUANTIFIED', 'low', `prizeUsd: "${x.prizeUsd}"`);
  if (/^\s*(cash|varies|confirm|n\/a)\b/i.test(x.prizeUsd) || /confirm (in|on)/i.test(x.minCashout)) add(x.id, 'VAGUE_VALUE', 'low', `prizeUsd="${x.prizeUsd}" minCashout="${x.minCashout}"`);
  if (/\b(uk|united kingdom|india|australia|canada|turkey|uae|germany|eu)\b.*(only|resident)|(only|residents? of)\b.*\b(uk|united kingdom|india|australia|canada)\b/i.test(x.eligibility + ' ' + x.restricted)) add(x.id, 'POSSIBLE_NON_US_ONLY', 'info', `eligibility="${x.eligibility}" restricted="${x.restricted}"`);
  if (/\b(texas|\bTX\b)/.test(x.eligibility + ' ' + x.restricted)) add(x.id, 'MENTIONS_TEXAS', 'info', `${x.eligibility} ${x.restricted}`);
  if (!x.platforms.includes('web') && !x.platforms.includes('ios')) add(x.id, 'PLATFORM_ODD', 'low', x.platforms.join());
  if (x.lastChecked !== '2026-08-19') add(x.id, 'LASTCHECKED_ODD', 'low', x.lastChecked);
}
// cross-listing duplicates by signup domain
const byDom = {};
L.listings.forEach(x => { const h = host(x.signupUrl); (byDom[h] = byDom[h] || []).push(x.id); });
Object.entries(byDom).filter(([,v]) => v.length > 1).forEach(([h, v]) => v.forEach(id => add(id, 'SHARED_SIGNUP_DOMAIN', 'info', `${h} shared by: ${v.join(', ')}`)));
// all URLs unique count
const allUrls = new Set(); L.listings.forEach(x => [x.signupUrl, x.iosUrl, x.tosUrl, x.rulesUrl, ...x.sources.map(s=>s.url)].filter(Boolean).forEach(u => allUrls.add(u)));
const summary = {};
findings.forEach(f => summary[f.code] = (summary[f.code] || 0) + 1);
fs.writeFileSync('data/raw/offline-findings.json', JSON.stringify({ generated: '2026-11-01', uniqueUrls: allUrls.size, summary, findings }, null, 1) + '\n');
console.log('unique URLs', allUrls.size); console.log(summary);
