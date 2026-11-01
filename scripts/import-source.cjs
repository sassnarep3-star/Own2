// Reproducible import of the external ledger; deliberately discards unsupported claims.
// Usage: node scripts/import-source.cjs /path/to/FreeMoneyApps/assets/data.js
const fs = require('node:fs');
const vm = require('node:vm');
const input = process.argv[2];
if (!input) throw new Error('Pass the source data.js path');
const sandbox = { window: {} };
vm.runInNewContext(fs.readFileSync(input, 'utf8'), sandbox, { timeout: 2000 });
const ledger = sandbox.window.LEDGER;
if (!ledger || !Array.isArray(ledger.listings)) throw new Error('Not a ledger');
const base = 'https://karagemop466-tech.github.io/FreeMoneyApps/';
const knownIssues = {
  'fpl-second-chance': 'Official Premier League 2025/26 article lists merchandise, not cash; old season.',
  'skillz': 'Source ledger terms URL returns an official 404 page; cash entry terms not confirmed.',
  'solitaire-cash': 'Official Papaya FAQ distinguishes free Gem competitions from real-money competitions; free cash path not established.',
  'bingo-cash': 'Official Papaya FAQ describes free Gems and cash competitions separately; free cash path not established.',
  'squarespool': 'Source supplied an HTTP URL; upgraded to the HTTPS operator site. This is a pool tool, not an operator-funded cash contest.',
  'draft-pro': 'Source signup URL is a press release, not the operator; operator URL replaced with its source-cited website. Current event not verified.'
};
const items = ledger.listings.map(x => ({
  id: x.id, name: x.name, category: x.type,
  operatorUrl: x.id === 'squarespool' ? 'https://www.squarespool.com/' : (x.id === 'draft-pro' ? 'https://thedraftpro.com/' : (x.signupUrl?.startsWith('https://') ? x.signupUrl : '')),
  // This is a citation supplied by the source ledger, NOT a verification by us.
  claimedRulesUrl: x.sources?.find(s => s.tier === 'official' && s.url?.startsWith('https://'))?.url || '',
  provenance: `${base}#${x.id}`,
  verification: 'unverified',
  prize: '', entry: '', deadline: '', eligibility: '',
  issue: knownIssues[x.id] || (!x.sources?.some(s => s.tier === 'official' && s.url?.startsWith('https://'))
    ? 'Source ledger has no operator-designated official evidence; prize and entry terms not confirmed.'
    : 'Source ledger citation has not been checked against current official rules; prize and entry terms not confirmed.')
}));
const catalog = {
  reviewed: '2026-11-01',
  source: base,
  categories: ledger.types.map(t => ({ id: t.id, name: t.name })),
  // Independently checked official organizer pages. Never conflate these with the historical catalog.
  opportunities: [
    { id: 'arc-paper-2026', name: 'ARC Prize 2026 — Paper Track', category: 'tech', verification: 'confirmed', entry: 'No purchase necessary', prize: '$75,000 total guaranteed; $50,000 first prize', deadline: '2026-11-09 23:59 UTC', eligibility: 'Requires an ARC-AGI-2 or ARC-AGI-3 submission and a public writeup/notebook', operatorUrl: 'https://www.kaggle.com/competitions/arc-prize-2026-paper-track', rulesUrl: 'https://www.kaggle.com/competitions/arc-prize-2026-paper-track/rules', evidence: 'Official rules §2.4 (no purchase) and §1.5 (prizes); overview (deadline, prerequisite). Optional $375,000 bonus is conditional and excluded from stated guaranteed pool.', fit: 'High technical effort · AI-agent assisted research possible; prerequisite submission required', source: 'official organizer' },
    { id: 'gems-2026', name: 'GEMS Prize — geologic fault mapping', category: 'tech', verification: 'partial', entry: '', prize: '$300,000 total; $100,000 top final-round award', deadline: '2026-12-03 23:59 UTC', eligibility: 'Individual: U.S. citizen or permanent resident, 18+; team captain: U.S. citizen or permanent resident', operatorUrl: 'https://www.drivendata.org/competitions/306/competition-doe-gems/', rulesUrl: 'https://docs.nlr.gov/docs/fy26osti/96647.pdf', evidence: 'Official challenge page (pool, deadline) and official rules §§1.1, 1.3, 3.1–3.2 (awards, eligibility, AI disclosure). An explicit no-fee statement was not located.', fit: 'High technical effort · AI use permitted with disclosure; confirm entry fee before treating as free', source: 'official organizer' }
  ],
  listings: items
};
if (items.length !== 206 || new Set(items.map(x => x.id)).size !== items.length) throw new Error('Unexpected source count/duplicate');
fs.writeFileSync('data/catalog.json', JSON.stringify(catalog, null, 2) + '\n');
console.log(`Imported ${items.length} source records. ${items.filter(x => !x.claimedRulesUrl).length} lack operator-designated rules citations.`);
