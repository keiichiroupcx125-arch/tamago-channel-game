const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1080, height: 1920 }, recordVideo: { dir: 'vid', size: { width: 1080, height: 1920 } } });
  const recStart = Date.now();
  const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8766/short.html');
  await p.waitForTimeout(1500);
  p.evaluate(() => window.__go());
  const shots = { 2600: 's1', 5200: 's2', 7200: 's3', 12000: 's4a', 19500: 's4b', 23500: 's5', 28500: 's6' };
  const t0 = Date.now();
  for (const [ms, name] of Object.entries(shots)) {
    const wait = +ms - (Date.now() - t0); if (wait > 0) await p.waitForTimeout(wait);
    await p.screenshot({ path: `f_${name}.png` });
  }
  await p.waitForFunction(() => window.__done, null, { timeout: 60000 });
  const t0wall = await p.evaluate(() => window.__t0wall);
  const ev = await p.evaluate(() => window.__events);
  await p.waitForTimeout(300);
  const video = p.video();
  await ctx.close();
  const path = await video.path();
  require('fs').writeFileSync('events.json', JSON.stringify({ offset: (t0wall - recStart) / 1000, ev, path }, null, 1));
  console.log('offset', (t0wall - recStart) / 1000, 'events', ev.length, path, errs);
  await b.close();
})();
