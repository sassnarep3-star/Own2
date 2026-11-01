const assert = require('node:assert/strict');
const fs = require('node:fs');
const { chromium: playwright } = require('playwright');
const chromium = require('@sparticuz/chromium');
const { AxeBuilder } = require('@axe-core/playwright');
const { spawn, spawnSync } = require('node:child_process');
const path = require('node:path');
const os = require('node:os');
const zlib = require('node:zlib');
const base = process.env.BASE_URL || 'http://127.0.0.1:4180';
let server;
async function run() {
  if (!process.env.BASE_URL) {
    server = spawn('python3', ['-m', 'http.server', '4180', '--bind', '0.0.0.0', '--directory', 'site'], { stdio: ['ignore','ignore','pipe'] });
    // Python emits the request log only later; wait for its listening socket once, not a shell polling loop.
    await new Promise((resolve,reject) => { server.once('error',reject); setTimeout(resolve,600); });
  }
  // NPM-distributed Chromium avoids downloads from hosts unavailable in this sandbox.
  // Its bundled NSS/NSPR libraries also make the test portable on minimal Linux images.
  const libs = path.join(os.tmpdir(), 'prize-ledger-libs');
  if (!fs.existsSync(path.join(libs, 'lib/libnspr4.so'))) {
    fs.mkdirSync(libs, {recursive:true});
    const compressed = fs.readFileSync(path.join(path.dirname(require.resolve('@sparticuz/chromium/package.json')), 'bin/al2023.tar.br'));
    const extracted = spawnSync('tar', ['-xf', '-', '-C', libs], {input:zlib.brotliDecompressSync(compressed)});
    assert.equal(extracted.status, 0, 'Extract browser runtime libraries');
  }
  process.env.LD_LIBRARY_PATH = path.join(libs,'lib') + (process.env.LD_LIBRARY_PATH ? ':'+process.env.LD_LIBRARY_PATH : '');
  const browser = await playwright.launch({executablePath: await chromium.executablePath(), args: chromium.args, headless: true});
  const context = await browser.newContext({viewport:{width:1440,height:1000}});
  const page = await context.newPage();
  const errors=[]; page.on('pageerror', error => errors.push(error.message));
  await page.goto(base+'/index.html');
  await page.waitForSelector('tr[data-id]:visible');
  assert.equal(await page.locator('tr[data-id]:visible').count(),20);
  assert.match(await page.locator('#result-count').textContent(),/of 216/);
  await page.getByRole('button',{name:'Free + cash sourced'}).click();
  assert.equal(await page.locator('tr[data-id]:visible').count(),6);
  assert.equal(await page.locator('tr[data-id="futureeval-fall-2026"]:visible').count(),0);
  await page.locator('#reset').click();
  await page.locator('#search').fill('zzzzzzzz');
  assert.equal(await page.locator('#empty').isVisible(),true);
  await page.locator('#search').fill('PayPal AI Hackathon');
  assert.equal(await page.locator('tr[data-id]:visible').count(),1);
  await page.locator('button[data-save="paypal-ai-2026"]').click();
  await page.goto(base+'/saved.html');
  assert.equal(await page.locator('tr[data-id]:visible').count(),1);
  await page.reload();assert.equal(await page.locator('tr[data-id]:visible').count(),1);
  await page.locator('button[data-save="paypal-ai-2026"]').click();
  assert.equal(await page.locator('#empty').isVisible(),true);
  await page.goto(base+'/competitions.html');
  await page.locator('#next').click();
  assert.match(await page.locator('#result-count').textContent(),/21–40/);
  await page.locator('#reset').click();
  await page.locator('#category').selectOption('creative');
  assert.equal(await page.locator('tr[data-id]:visible:not([data-category="creative"])').count(),0);
  await page.locator('#reset').click();
  await page.locator('#evidence-filter').selectOption('ai');
  assert.equal(await page.locator('tr[data-id]:visible:not([data-ai="true"])').count(),0);
  await page.goto(base+'/competitions.html?entry=paypal-ai-2026');
  assert.equal(await page.locator('#paypal-ai-2026 details').getAttribute('open'),'');
  await page.goto(base+'/categories/tech.html');
  assert.equal(await page.locator('#category').isDisabled(),true);
  await page.locator('#reset').click();
  assert.equal(await page.locator('tr[data-id]:visible:not([data-category="tech"])').count(),0);
  fs.mkdirSync('test-results',{recursive:true});
  for (const width of [1440,390,320]) {
    await page.setViewportSize({width,height:1000});
    await page.goto(base+'/index.html');
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),true,`Horizontal overflow at ${width}px`);
    if(width===390){
      await page.locator('#menu').click();
      assert.equal(await page.locator('#menu').getAttribute('aria-expanded'),'true');
      await page.keyboard.press('Escape');
      assert.equal(await page.locator('#menu').getAttribute('aria-expanded'),'false');
    }
    const result = await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
    if(result.violations.length)fs.writeFileSync(`test-results/axe-${width}.json`,JSON.stringify(result.violations,null,2));
    assert.deepEqual(result.violations.map(v => v.id),[],`Axe violations at ${width}px`);
    await page.screenshot({path:`test-results/overview-${width}.png`,fullPage:false});
  }
  for(const path of ['review.html','summary.html','methodology.html','sources.html']) {
    await page.goto(base+'/'+path);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),true,'Overflow on '+path);
  }
  const noJS = await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
  const staticPage=await noJS.newPage();await staticPage.goto(base+'/competitions.html');
  assert.equal(await staticPage.locator('tr[data-id]').count(),216);
  assert.equal(await staticPage.locator('tr[data-id]:visible').count(),216);
  const blocked = await browser.newContext();
  await blocked.addInitScript(() => Object.defineProperty(window,'localStorage',{get(){throw new Error('storage blocked')}}));
  const blockedPage=await blocked.newPage();await blockedPage.goto(base+'/competitions.html');
  await blockedPage.locator('[data-save="paypal-ai-2026"]').click();
  assert.match(await blockedPage.locator('#result-count').textContent(),/temporary/);
  assert.deepEqual(errors,[]);
  await browser.close();
  console.log('PASS: filtering, strict cash exclusions, search, save/unsave/persistence, pagination, category locks, deep links, mobile 320/390px, desktop 1440px, axe WCAG AA, no-JS content and blocked storage.');
}
run().catch(e=>{console.error(e); console.error('::error::Browser validation failed: '+String(e.message).replace(/\n/g,' '));process.exitCode=1;}).finally(()=>server?.kill());
