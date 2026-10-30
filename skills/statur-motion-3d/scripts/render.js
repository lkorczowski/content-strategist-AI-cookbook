#!/usr/bin/env node
// statur-motion-3d renderer. Serves a project folder, opens it in headless Chromium (SwiftShader, CPU only),
// calls window.renderAt(t) per frame and pipes JPEG screenshots to ffmpeg.
//   node render.js <project> stills <t1,t2,...> <outdir>     one JPEG per time, for review before a full render
//   node render.js <project> video <out.mp4> [from] [to]      silent H.264 video (fps, size, duration from scenario.json)
//   node render.js --help
const help = 'usage: node render.js <project> stills <t1,t2,...> <outdir> | node render.js <project> video <out.mp4> [from] [to]';
if (process.argv.length < 5 || process.argv.includes('--help')) { console.log(help); process.exit(process.argv.includes('--help') ? 0 : 1); }
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const [project, mode, a, b, c] = process.argv.slice(2);
const ROOT = path.resolve(project);
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2', '.png': 'image/png', '.jpg': 'image/jpeg' };
const srv = http.createServer((q, r) => { const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if (!p.startsWith(ROOT)) { r.writeHead(403); r.end(); return; }
  fs.readFile(p, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' }); r.end(d); }); });
(async () => {
  const S = JSON.parse(fs.readFileSync(path.join(ROOT, 'scenario.json'), 'utf8'));
  const W = S.width || 720, H = S.height || 1280, fps = S.fps || 30, dur = S.duration;
  await new Promise(r => srv.listen(0, r)); const port = srv.address().port;
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  let failed = false;
  page.on('pageerror', e => { failed = true; console.error('PAGE ERROR', e.message); });
  page.on('console', m => { if (m.type() === 'error') console.error('PAGE', m.text()); });
  await page.goto(`http://localhost:${port}/index.html`);
  await page.waitForFunction('window.READY === true || window.FONT_ERROR', null, { timeout: 180000 });
  const fontErr = await page.evaluate('window.FONT_ERROR'); if (fontErr) { console.error(fontErr + ' (run setup_project.sh again)'); process.exit(2); }
  if (failed) process.exit(3);
  const stage = await page.$('#stage');
  if (mode === 'stills') {
    fs.mkdirSync(b, { recursive: true });
    for (const t of a.split(',').map(Number)) { await page.evaluate(t => window.renderAt(t), t); await stage.screenshot({ path: path.join(b, `t${t.toFixed(2).padStart(6, '0')}.jpg`), type: 'jpeg', quality: 88 }); }
    console.log(`stills written to ${b}`);
  } else if (mode === 'video') {
    const from = Number(b || 0), to = Number(c || dur);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', a], { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round((to - from) * fps), t0 = Date.now();
    for (let i = 0; i < n; i++) {
      const t = from + i / fps; await page.evaluate(t => window.renderAt(t), t);
      const buf = await stage.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 150 === 0) console.log(`frame ${i}/${n} t=${t.toFixed(2)} ${((i + 1) / ((Date.now() - t0) / 1000)).toFixed(2)} fps`);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); console.log(`video written to ${a} in ${((Date.now() - t0) / 60000).toFixed(1)} min`);
  } else { console.log(help); }
  await browser.close(); srv.close();
})();
