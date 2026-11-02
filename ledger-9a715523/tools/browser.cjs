const assert=require('node:assert/strict');
const fs=require('node:fs');const path=require('node:path');const os=require('node:os');const zlib=require('node:zlib');
const {spawn,spawnSync}=require('node:child_process');
const {chromium:playwright}=require('playwright');const chromium=require('@sparticuz/chromium');const {AxeBuilder}=require('@axe-core/playwright');
const ROOT=path.resolve(__dirname,'..');const OUT=path.join(ROOT,'test-results');
async function run(){
 const libs=path.join(os.tmpdir(),'prizelens-browser-libs');
 if(!fs.existsSync(path.join(libs,'lib/libnspr4.so'))){fs.mkdirSync(libs,{recursive:true});const compressed=fs.readFileSync(path.resolve(path.dirname(require.resolve('@sparticuz/chromium')),'../../bin/al2023.tar.br'));const r=spawnSync('tar',['-xf','-','-C',libs],{input:zlib.brotliDecompressSync(compressed)});assert.equal(r.status,0);}
 process.env.LD_LIBRARY_PATH=path.join(libs,'lib')+(process.env.LD_LIBRARY_PATH?':'+process.env.LD_LIBRARY_PATH:'');
 const base=process.env.BASE_URL||'http://127.0.0.1:4189';let server;
 if(!process.env.BASE_URL){server=spawn('python3',['-m','http.server','4189','--bind','127.0.0.1','--directory',ROOT],{stdio:'ignore'});await new Promise((res,rej)=>{server.once('error',rej);setTimeout(res,700);});}
 const browser=await playwright.launch({executablePath:await chromium.executablePath(),args:chromium.args,headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));fs.mkdirSync(OUT,{recursive:true});
 try{
  await page.goto(base+'/all.html');assert.equal(await page.locator('#all tbody tr').count(),224);assert.equal(await page.locator('#all tbody tr:visible').count(),25);
  await page.locator('#all-search').fill('Kiroween');assert.equal(await page.locator('#all tbody tr:visible').count(),1);
  await page.locator('[data-reset="all"]').click();await page.locator('#all-category').selectOption('creative');assert.equal(await page.locator('#all tbody tr:visible:not([data-category="creative"])').count(),0);
  await page.locator('[data-reset="all"]').click();await page.locator('#all-agent').selectOption('prohibited');assert.equal(await page.locator('#all tbody tr:visible').count(),3);
  await page.locator('[data-reset="all"]').click();await page.locator('#all-status').selectOption('shortlist');assert.match(await page.locator('[data-count="all"]').textContent(),/^12 records/);
  await page.locator('[data-reset="all"]').click();await page.locator('[data-next="all"]').click();assert.match(await page.locator('[data-page="all"]').textContent(),/Page 2/);
  await page.locator('#all-search').fill('zzzzzzzz');assert.equal(await page.locator('[data-empty="all"]').isVisible(),true);await page.locator('[data-reset="all"]').click();
  await page.locator('#all-search').fill('Kiroween');await page.locator('[data-save="event-kiroween"]').click();await page.goto(base+'/saved.html');assert.equal(await page.locator('#saved tbody tr:visible').count(),1);await page.reload();assert.equal(await page.locator('#saved tbody tr:visible').count(),1);await page.locator('[data-save="event-kiroween"]').click();assert.equal(await page.locator('[data-empty="saved"]').isVisible(),true);
  await page.goto(base+'/shortlist.html');await page.locator('#shortlist-search').fill('UGREEN');const downloadPromise=page.waitForEvent('download');await page.locator('[data-export="shortlist"]').click();const download=await downloadPromise;const csv=fs.readFileSync(await download.path(),'utf8');assert.match(csv,/UGREEN/);assert.match(csv,/Official source/);
  await page.goto(base+'/flagged.html');await page.locator('#flag-search').fill('PayPal');assert.ok(await page.locator('#flag-table tbody tr:visible').count()<224);assert.match(await page.locator('#flag-count').textContent(),/records/);
  for(const width of [1440,390,320]){
   await page.setViewportSize({width,height:1000});
   for(const file of ['index.html','all.html','shortlist.html','summary.html','flagged.html','sources.html','methodology.html','category-tech.html','saved.html']){
    await page.goto(base+'/'+file);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`Overflow ${file} at ${width}px`);
   }
   await page.goto(base+'/index.html');const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();if(axe.violations.length)fs.writeFileSync(path.join(OUT,`axe-${width}.json`),JSON.stringify(axe.violations,null,2));assert.deepEqual(axe.violations.map(v=>v.id),[],`Axe violations at ${width}px`);await page.screenshot({path:path.join(OUT,`overview-${width}.png`),fullPage:false});
  }
  const noJS=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const staticPage=await noJS.newPage();await staticPage.goto(base+'/all.html');assert.equal(await staticPage.locator('#all tbody tr').count(),224);assert.equal(await staticPage.locator('#all tbody tr:visible').count(),224);assert.equal(await staticPage.locator('[data-save="solitaire-cash"]').isVisible(),false);
  const blocked=await browser.newContext();await blocked.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}}));const bp=await blocked.newPage();await bp.goto(base+'/all.html');await bp.locator('#all-search').fill('Kiroween');await bp.locator('[data-save="event-kiroween"]').click();assert.equal(await bp.locator('[data-save="event-kiroween"]').getAttribute('aria-pressed'),'true');
  assert.deepEqual(errors,[]);console.log('PASS: search, category/agent/evidence filters, pagination, save persistence, CSV export, review search, 320/390/1440px overflow, axe WCAG AA, no-JS rows, blocked storage, no page errors.');
 }finally{await browser.close();server?.kill();}
}
run().catch(e=>{console.error(e);process.exitCode=1;});
