const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + __dirname + '/index.html');
  await p.waitForFunction(() => window.__done === true, null, { timeout: 60000 });
  const over = await p.evaluate(() => [...document.querySelectorAll('.qpage, .spage')].filter(e => e.scrollHeight > 960).map(e => e.querySelector('.qnum').textContent + ' ' + e.scrollHeight));
  if (errs.length) console.log('ERRORS', errs);
  if (over.length) console.log('TALL', over);
  await p.pdf({ path: process.argv[2] || 'out.pdf', format: 'A4', printBackground: true,
    margin: { top: '17mm', bottom: '20mm', left: '19mm', right: '19mm' },
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="width:100%;font-family:Inter,sans-serif;font-size:8px;color:#8a949e;padding:0 19mm;display:flex;justify-content:space-between"><span>Olympiad Combinatorics · Learn and Practise</span><span class="pageNumber"></span></div>' });
  await b.close();
})();
