// 白底黑字 PDF：node pdf_mono.cjs → ICOPE共學_個案＋系統討論_白底黑字.pdf（每頁一張 16:9 投影片，向量文字）
const path = require('path');
const puppeteer = require(process.env.HOME + '/Claude/影片/功能性訓練/node_modules/puppeteer-core');
const MONO = `
:root,:root[data-theme]{--paper:#fff;--sheet:#fff;--ink:#000;--ink2:#2b2b2b;--ink3:#555;--rule:#b5b5b5;--rule2:#dcdcdc;
--teal:#1f1f1f;--tealink:#000;--tealbg:#f1f1f1;--tealmid:#8c8c8c;--orange:#4a4a4a;--orangeink:#000;--orangebg:#f1f1f1;
--amber:#a6a6a6;--amberink:#000;--amberbg:#f1f1f1;--deep:#fff;--ondeep:#000;--ondeep2:#444;
--good:#9a9a9a;--warn:#9a9a9a;--serious:#555;--critical:#222;--shadow:none;--u:1px;color-scheme:light}
html,body{background:#fff!important;height:auto!important}
.deck{position:static!important;display:block!important}
.slide{display:flex!important;width:1280px!important;height:720px!important;box-shadow:none!important;border-radius:0!important;
  break-after:page;page-break-after:always;margin:0!important;animation:none!important}
.slide.divider{border-top:6px solid #000}
.bar,.fab,.notes-panel,.toc,.tip,.tb2,[data-fill],#pdcaClear{display:none!important}
.dom{background:#000!important;color:#fff!important} .dom.ok{background:#e6e6e6!important;color:#000!important}
.pill::before{background:#000!important} .pill{background:#efefef!important;color:#000!important}
.thr,.tag2{background:#e6e6e6!important;color:#000!important}
.ask{border-color:#000!important} .ask b,.ask.o b{color:#000!important}
.callout{border-left-color:#000!important}
.pick.on{border-color:#000!important}
@page{size:1280px 720px;margin:0}
`;
(async () => {
  const dir = __dirname;
  const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new' });
  const p = await b.newPage();
  await p.setViewport({ width: 1366, height: 800 });
  await p.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'light' }]);
  await p.goto('file://' + path.join(dir, 'index.html'), { waitUntil: 'networkidle0' });
  await p.evaluate(css => { document.documentElement.setAttribute('data-theme', 'light'); document.body.classList.remove('scroll');
    const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s);
    document.documentElement.style.setProperty('--u', '1px'); window.onresize = null; }, MONO);
  await new Promise(r => setTimeout(r, 800));
  const out = path.join(dir, 'ICOPE共學_個案＋系統討論_白底黑字.pdf');
  await p.pdf({ path: out, width: '1280px', height: '720px', printBackground: true, preferCSSPageSize: true });
  await b.close(); console.log('saved', out);
})();
