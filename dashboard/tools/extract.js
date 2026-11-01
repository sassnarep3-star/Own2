// Extracts the source ledger (karagemop466-tech/FreeMoneyApps assets/data.js) into plain JSON.
// Usage: node tools/extract.js /path/to/FreeMoneyApps/assets/data.js data/raw/source-ledger.json
const fs = require('fs');
const [,, inp, out] = process.argv;
global.window = {};
require(require('path').resolve(inp));
fs.writeFileSync(out, JSON.stringify(window.LEDGER, null, 1) + '\n');
console.log('listings:', window.LEDGER.listings.length);
