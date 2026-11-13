#!/usr/bin/env node
// Headless smoke test: loads the game on a phone viewport, plays it with a
// simple aiming bot, exercises game over + rewarded/interstitial mock ads,
// and saves screenshots to ./screenshots.
const path = require('path');
const fs = require('fs');
const { chromium, devices } = require('playwright');

(async () => {
  const outDir = path.join(__dirname, '..', 'screenshots');
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ ...devices['Pixel 7'] });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));

  await page.goto('file://' + path.join(__dirname, '..', 'www', 'index.html'));
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(outDir, '1-menu.png') });

  await page.tap('#playBtn', { force: true });
  await page.waitForTimeout(400);

  // Bot: tap when the launch direction points at the next planet.
  const best = await page.evaluate(async () => {
    const g = window.__orbit;
    const t0 = performance.now();
    while (g.state === 'play' && g.score < 40 && performance.now() - t0 < 45000) {
      const p = g.player;
      if (p.mode === 'orbit') {
        const next = g.planets.find((q) => q.idx === p.planet.idx + 1);
        if (next) {
          const dx = -Math.sin(p.angle) * p.dir, dy = Math.cos(p.angle) * p.dir;
          const rx = next.x - p.x, ry = next.y - p.y;
          const along = rx * dx + ry * dy;
          const miss = Math.abs(rx * dy - ry * dx);
          if (along > 0 && miss < next.orbitR * 0.25) g.tap();
        }
      }
      await new Promise((r) => requestAnimationFrame(r));
    }
    return g.score;
  });
  console.log('Bot score:', best);
  await page.screenshot({ path: path.join(outDir, '2-gameplay.png') });

  // Force a death by launching straight away
  await page.evaluate(async () => {
    const g = window.__orbit;
    while (g.state === 'play') {
      if (g.player.mode === 'orbit') {
        const a = g.player.angle, d = g.player.dir;
        if (Math.cos(a) * d > 0.9) g.tap();     // flying straight down = death
      }
      await new Promise((r) => requestAnimationFrame(r));
    }
  });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(outDir, '3-gameover.png') });

  // Rewarded "continue"
  const canContinue = await page.isVisible('#continueBtn');
  if (canContinue) {
    await page.tap('#continueBtn', { force: true });
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(outDir, '4-rewarded-ad.png') });
    await page.waitForTimeout(5300);
    await page.tap('#mockAd button', { force: true });
    await page.waitForTimeout(300);
    console.log('After continue, state =', await page.evaluate(() => window.__orbit.state));
  }

  await page.evaluate(() => { localStorage.setItem('orbithop.save.v1', JSON.stringify({ coins: 900, best: 42, owned: ['comet', 'sun'], skin: 'sun' })); });
  await page.reload();
  await page.waitForTimeout(500);
  await page.tap('#shopBtn', { force: true });
  await page.waitForTimeout(300);
  await page.screenshot({ path: path.join(outDir, '5-shop.png') });

  console.log('Errors:', errors.length ? errors : 'none');
  await browser.close();
  process.exit(errors.length ? 1 : 0);
})();
