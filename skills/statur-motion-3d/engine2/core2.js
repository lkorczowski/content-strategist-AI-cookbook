// Motion 3D core v2: 3D (Three.js + bloom) or 2D (canvas) stage, brand overlay (tag, title, HUD readout,
// punchy captions with keyword color and source line, end card), film grain and vignette.
// Deterministic: window.renderAt(t). Project folder given by ?p=<folder> (scenario.json + shots.js inside).
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const P = new URLSearchParams(location.search).get('p') || 'p1';
const S = await (await fetch(`${P}/scenario.json`)).json();
const W = 720, H = 1280;
const $ = id => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const ss = (a, b, x) => { const k = clamp((x - a) / (b - a)); return k * k * (3 - 2 * k); };
const lerp = (a, b, k) => a + (b - a) * k;
const fmtHL = s => (s || '').replace(/\*(.+?)\*/g, '<o>$1</o>');

// ---------- brand ----------
// Tokens (docs/BRAND-TOKENS.md) come from scenario.brand, else from brand.json at the workspace root (written by
// setup_project2.sh), else the neutral look of index.html. Texts: scenario.tag, scenario.site, end.brand.
let B = S.brand || null;
if (!B) { try { const r = await fetch('brand.json'); if (r.ok) B = await r.json(); } catch (e) { B = null; } }
B = B || {};
const BC = Object.assign({ paper: '#F6F3EC', panel: '#ECE8DE', ink: '#20262E', ink_drawing: '#33415C', secondary: '#6F747B', accent: '#1F6F5C', highlighter: '#F4D35E', highlighter_pale: '#FBF0C4' }, B.colors || {});
{ const rs = document.documentElement.style; rs.setProperty('--ink', BC.ink); rs.setProperty('--paper', BC.paper); rs.setProperty('--sig', BC.accent); }
const BNAME = B.name && B.name !== 'neutral' ? String(B.name) : '';
const SITE = S.site ?? B.site ?? '';
const TAG = S.tag ?? [BNAME.toUpperCase(), S.sim_no].filter(Boolean).join(' · ');
const esc = s => String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

// ---------- stage ----------
const ctx = { THREE, S, W, H, ss, clamp, lerp, $, brand: { name: BNAME, site: SITE, colors: BC, fonts: { display: 'BrandDisplay', label: 'BrandLabel', hand: 'BrandHand' } } };
let composer = null, bloom = null;
if (S.engine === '2d') {
  $('gl').style.display = 'none'; const c = $('c2d'); c.style.display = 'block'; ctx.g = c.getContext('2d');
} else {
  const renderer = new THREE.WebGLRenderer({ canvas: $('gl'), antialias: true, preserveDrawingBuffer: true });
  renderer.setSize(W, H, false); renderer.setPixelRatio(1); renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = S.exposure ?? 1.0;
  renderer.shadowMap.enabled = !!S.shadows; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const scene = new THREE.Scene(); const camera = new THREE.PerspectiveCamera(48, W / H, 0.05, 4000); scene.add(camera);
  composer = new EffectComposer(renderer); composer.addPass(new RenderPass(scene, camera));
  bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), S.bloom ?? .8, .55, .82); composer.addPass(bloom);
  composer.addPass(new OutputPass());
  Object.assign(ctx, { renderer, scene, camera, bloom });
}
// ---------- overlay helpers shots may use ----------
const fx = $('fx').getContext('2d'); ctx.fx = fx;
ctx.white = o => { $('white').style.opacity = o; };
ctx.black = o => { $('black').style.opacity = o; };
// grain tiles (deterministic)
const grain = []; { let s = 1234; const r = () => (s = (s * 16807) % 2147483647) / 2147483647;
  for (let k = 0; k < 6; k++) { const c = document.createElement('canvas'); c.width = 240; c.height = 427; const g = c.getContext('2d'); const im = g.createImageData(240, 427);
    for (let i = 0; i < im.data.length; i += 4) { const v = r() * 255; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; } g.putImageData(im, 0, 0); grain.push(c); } }

await document.fonts.ready;
// a font file that is not installed falls back to the system stack of index.html instead of stopping the render
await Promise.all(['900 50px BrandDisplay', '500 50px BrandDisplay', '700 14px BrandLabel', '400 14px BrandLabel', '500 40px BrandHand'].map(f => document.fonts.load(f).catch(() => [])));
if (S.ui === 'light') { for (const id of ['tag', 'site']) { $(id).style.color = BC.ink; $(id).style.textShadow = 'none'; } }
setH0($('site'), esc(SITE));
if (S.hud_top) $('hud').style.top = S.hud_top + 'px';
const mod = await import(`./${P}/shots.js`);
const shots = await mod.default(ctx);

function setH0(el, h) { el.innerHTML = h; }
const setH = (el, h) => { if (el.__h !== h) { el.innerHTML = h; el.__h = h; } };
window.renderAt = function (t) {
  fx.clearRect(0, 0, W, H); ctx.white(0); ctx.black(0); ctx.hud = true; ctx.grain = S.grain ?? .06; ctx.vig = S.vignette ?? .55;
  const shot = shots.find(s => t >= s.from && t < s.to) || shots[shots.length - 1];
  shot.run(t, clamp((t - shot.from) / (shot.to - shot.from)), t - shot.from);
  // tag + title
  setH($('tag'), esc(TAG));
  const T = S.title; const ta = t < T.to ? 1 - ss(T.to - .35, T.to, t) : 0; $('title').style.opacity = ta;
  $('title').style.transform = `scale(${lerp(.9, 1, ss(0, .25, t))})`; setH($('title'), fmtHL(T.text));
  // HUD
  const hs = (S.hud || []).find(h => t >= h.from && t < h.to); $('hud').style.display = hs && ctx.hud ? 'block' : 'none';
  if (hs) { setH($('hudl'), hs.label); setH($('hudv'), fmtHL(typeof hs.value === 'string' ? hs.value : (hs.value.find(([a]) => t >= a) ? hs.value.filter(([a]) => t >= a).pop()[1] : '')));
    const p = hs.prog ? lerp(hs.prog[0], hs.prog[1], clamp((t - hs.from) / (hs.to - hs.from))) : 0; $('hudf').style.width = (p * 100).toFixed(1) + '%'; }
  // captions: pop-in, keyword color, source line
  let cap = '', src = '', a = 0, k = 1;
  for (const c of S.captions) if (t >= c[0] && t < c[1]) { cap = c[2]; src = c[3] || ''; a = Math.min(ss(c[0], c[0] + .08, t), 1 - ss(c[1] - .1, c[1], t)); k = lerp(.86, 1, ss(c[0], c[0] + .14, t)); }
  setH($('cap'), fmtHL(cap)); $('cap').style.opacity = a; $('cap').style.transform = `scale(${k.toFixed(3)})`;
  setH($('src'), src ? 'SOURCE · ' + src : ''); $('src').style.opacity = a * .85;
  // end card
  const E = S.end; if (E && t >= E.from) { $('end').style.display = 'block'; setH($('endt'), fmtHL(E.title)); setH($('endq'), E.question); setH($('endb'), esc(E.brand ?? [BNAME.toUpperCase(), SITE].filter(Boolean).join(' · '))); $('hud').style.display = 'none'; ctx.vig = .3; }
  else $('end').style.display = 'none';
  // render
  if (composer) composer.render();
  // grain + vignette over everything
  if (ctx.grain > 0) { fx.save(); fx.globalAlpha = ctx.grain; fx.globalCompositeOperation = 'overlay'; fx.drawImage(grain[Math.floor(t * 24) % grain.length], 0, 0, W, H); fx.restore(); }
  if (ctx.vig > 0) { const gr = fx.createRadialGradient(W / 2, H / 2, H * .3, W / 2, H / 2, H * .75); gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, `rgba(0,0,0,${ctx.vig})`); fx.fillStyle = gr; fx.fillRect(0, 0, W, H); }
};
window.renderAt(0); window.READY = true;
