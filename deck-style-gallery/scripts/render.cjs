#!/usr/bin/env node
// Render slide HTML files to PNG and refuse to screenshot until every
// non-CJK web font face has loaded (Google Fonts can fail silently and the
// Latin text then falls back to a CJK face with no error).
//
//   node render.cjs slide.html [more.html ...]   -> slide.png next to each file
//   node render.cjs --check                      -> verify Playwright + Chromium
//
// Env: PLAYWRIGHT_CORE  module path or name (default "playwright-core")
//      CHROMIUM_PATH    browser executable (default: Playwright's own)
//      SLIDE_W, SLIDE_H CSS viewport (default 1920x1080); SLIDE_SCALE (default 2)
const path = require('path');
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');

const W = +(process.env.SLIDE_W || 1920), H = +(process.env.SLIDE_H || 1080);
const SCALE = +(process.env.SLIDE_SCALE || 2), TRIES = 6;

(async () => {
  const args = process.argv.slice(2);
  const opts = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {};
  const browser = await chromium.launch(opts);
  if (args[0] === '--check') { console.log('ok', browser.version()); await browser.close(); return; }
  let failed = 0;
  for (const f of args) {
    const inp = path.resolve(f), out = inp.replace(/\.html?$/, '.png');
    let done = false;
    for (let i = 1; i <= TRIES && !done; i++) {
      const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: SCALE });
      try {
        await page.goto('file://' + inp, { waitUntil: 'networkidle', timeout: 90000 });
        const r = await page.evaluate(async () => {
          await document.fonts.ready;
          const remote = !!document.querySelector('link[href*="fonts.googleapis"]');
          const faces = [...document.fonts];
          const latin = faces.filter(x => !/SC|TC|JP|KR|CJK/.test(x.family));
          await Promise.all(latin.map(x => x.load().catch(() => null)));
          await document.fonts.ready;
          const bad = latin.filter(x => x.status !== 'loaded').map(x => `${x.family} ${x.weight}`);
          return { n: faces.length, remote, bad: [...new Set(bad)] };
        });
        if ((r.remote && r.n === 0) || r.bad.length) {
          console.log(`${f} try ${i}: fonts missing ${r.n === 0 ? '(stylesheet failed)' : r.bad.join(', ')}`);
        } else {
          await page.waitForTimeout(800);
          await page.screenshot({ path: out });
          console.log(`${f} ok (try ${i})`);
          done = true;
        }
      } catch (e) { console.log(`${f} try ${i}: ${e.message.slice(0, 100)}`); }
      await page.close();
    }
    if (!done) { failed++; console.log(`${f} FAILED after ${TRIES} tries; run vendor_fonts.py`); }
  }
  await browser.close();
  process.exit(failed ? 1 : 0);
})();
