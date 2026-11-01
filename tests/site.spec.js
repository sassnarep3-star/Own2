const { test, expect } = require('@playwright/test');
async function ready(page,path='/') {
  await page.goto(path);
  await expect(page.locator('#result-count')).toContainText('Showing');
  // Confirm enhancement has attached, rather than only seeing prerendered content.
  await page.waitForFunction(()=>document.querySelector('#result-count').textContent.includes('of'));
}
test('catalog, live counts and all unknown values remain honest',async({page})=>{
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await ready(page);await expect(page.locator('#entries tr')).toHaveCount(209);
 await expect(page.locator('#entries tr:not([hidden])')).toHaveCount(209);
 await expect(page.locator('.stat strong').first()).toHaveText('209');
 await page.locator('#search').fill('FutureEval');await expect(page.locator('#entries tr:not([hidden])')).toHaveCount(1);
 await page.locator('#search').fill('absolutely-no-match');await expect(page.locator('#empty')).toBeVisible();
 await page.locator('#reset').click();await expect(page.locator('#entries tr:not([hidden])')).toHaveCount(209);
 await page.locator('#free').check();await expect(page.locator('#entries tr:not([hidden])')).toHaveCount(3);
 expect(errors).toEqual([]);
});
test('evidence dialog, official citations, keyboard dismissal and missing fields',async({page})=>{
 await ready(page);await page.locator('[data-detail="futureeval-fall-2026"]').click();
 await expect(page.getByRole('dialog')).toBeVisible();await expect(page.locator('#dialog-title')).toContainText('FutureEval');
 await expect(page.locator('#dialog-content')).toContainText('Unverified; no confirmed value');
 await expect(page.locator('#dialog-content a[href="https://www.metaculus.com/tournament/fall-futureeval-2026/"]').first()).toBeVisible();
 await page.keyboard.press('Escape');await expect(page.getByRole('dialog')).not.toBeVisible();
 await expect(page.locator('[data-detail="futureeval-fall-2026"]')).toBeFocused();
});
test('saved shortlist persists, supports unsave, and empty state',async({page})=>{
 await ready(page);await page.locator('[data-save="futureeval-fall-2026"]').click();await expect(page.locator('#saved-count')).toHaveText('1');
 await page.reload();await page.waitForFunction(()=>document.querySelector('#saved-count').textContent==='1');
 await page.locator('[data-view="saved"]').click();await expect(page.locator('#entries tr:not([hidden])')).toHaveCount(1);
 await page.locator('[data-save="futureeval-fall-2026"]').click();await expect(page.locator('#empty')).toBeVisible();
});
test('category, evidence, research view and sorting filters',async({page})=>{
 await ready(page);await page.locator('#category').selectOption('tech');
 await expect(page.locator('#entries tr:not([hidden])')).toHaveCount(16);
 await page.locator('#evidence').selectOption('partial');await expect(page.locator('#entries tr:not([hidden])')).toHaveCount(3);
 await page.locator('#sort').selectOption('name');
 await expect(page.locator('#entries tr:not([hidden]) .entry-name').first()).toHaveText('ARC Prize (via Kaggle)');
 await page.locator('#reset').click();await page.locator('[data-view="shortlist"]').click();await expect(page.locator('#entries tr:not([hidden])')).toHaveCount(4);
});
test('CSV exports filtered facts and blanks without unsupported values',async({page})=>{
 await ready(page);await page.locator('#search').fill('GEMS Prize');
 const downloadPromise=page.waitForEvent('download');await page.locator('#export').click();const download=await downloadPromise;
 const stream=await download.createReadStream();let text='';for await(const b of stream)text+=b.toString();
 expect(text).toContain('GEMS Prize');expect(text).toContain('"","$300,000');expect(text).not.toContain('Solitaire');
});
test('mobile navigation and contained horizontal table scroll',async({page,isMobile})=>{
 await ready(page);expect(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth)).toBe(true);
 if(isMobile){await page.getByRole('button',{name:'Toggle navigation'}).click();await expect(page.locator('#sidebar')).toHaveClass(/open/);}
 await page.locator('.sidebar a[href="categories/creative/index.html"]').click();
 await expect(page.locator('h1')).toHaveText('Creative contests');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=document.documentElement.clientWidth)).toBe(true);
 await expect(page.locator('#entries tr')).toHaveCount(18);
});
test('summary and complete searchable review queue',async({page})=>{
 await page.goto('/summary/index.html');await expect(page.locator('h1')).toContainText('Executive summary');
 await page.goto('/review/index.html');await expect(page.locator('[data-review]')).toHaveCount(209);
 await page.locator('#review-search').fill('press-release distributor');await expect(page.locator('[data-review]:not([hidden])')).toHaveCount(1);
 await expect(page.locator('[data-review]:not([hidden])')).toContainText('Official source missing');
});
test('static table works with JavaScript disabled',async({browser})=>{
 const context=await browser.newContext({javaScriptEnabled:false});const page=await context.newPage();
 await page.goto('http://127.0.0.1:8000/');await expect(page.locator('#entries tr')).toHaveCount(209);
 await expect(page.locator('#futureeval-fall-2026 a')).toHaveAttribute('href','https://www.metaculus.com/tournament/fall-futureeval-2026/');
 await expect(page.locator('noscript p')).toContainText('All entries and sources are available');await context.close();
});
