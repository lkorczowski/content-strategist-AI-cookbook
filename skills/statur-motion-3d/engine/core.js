// statur-motion-3d core: renderer, overlay (title, HUD clock, captions, end card) driven by scenario.json,
// and window.renderAt(t) that draws one deterministic frame. Shots live in the project's shots.js.
import * as THREE from 'three';
import { buildKit, clamp, lerp, ss } from './kit.js';
import makeShots from './shots.js';

const S = await (await fetch('scenario.json')).json();
const W = S.width || 720, H = S.height || 1280;
const stage = document.getElementById('stage'); stage.style.width = W + 'px'; stage.style.height = H + 'px';
const gl = document.getElementById('gl'); gl.width = W; gl.height = H;
const fxc = document.getElementById('fx'); fxc.width = W; fxc.height = H;
const renderer = new THREE.WebGLRenderer({ canvas: gl, antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H, false); renderer.setPixelRatio(1); renderer.outputColorSpace = THREE.SRGBColorSpace;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(50, W / H, 0.05, 3000); scene.add(camera);
const K = buildKit({ scene, camera, seed: S.seed ?? 42 });
const $ = id => document.getElementById(id);
const fx = fxc.getContext('2d');
const O = {                       // overlay controls shots may use
  fx, W, H,
  white: (o) => { $('white').style.opacity = o; },
  vignette: (o) => { $('vig').style.opacity = o; },
  hideHud: () => { O._hud = false; },
};
const shots = makeShots(K, O, S);

const hl = (s) => (s || '').replace(/<hl>(.*?)<\/hl>/g, '<span class="hl">$1</span>');
const setText = (el, html) => { if (el.__h !== html) { el.innerHTML = html; el.__h = html; } };
function fmt(sec) { sec = Math.max(0, sec); const m = Math.floor(sec / 60), s = sec - m * 60; return `${m}:${s.toFixed(3).padStart(6, '0')}`; }
function interp(keys, t) { if (t <= keys[0][0]) return keys[0][1]; for (let i = 1; i < keys.length; i++) if (t <= keys[i][0]) { const [a, va] = keys[i - 1], [b, vb] = keys[i]; return lerp(va, vb, clamp((t - a) / (b - a))); } return keys[keys.length - 1][1]; }
function subAt(sub, t) {
  if (!sub) return ''; if (typeof sub === 'string') return sub;
  if (Array.isArray(sub)) { let cur = ''; for (const [a, s] of sub) if (t >= a) cur = typeof s === 'string' ? s : subAt(s, t); return cur; }
  if (sub.template) return sub.template.replace('{n}', Math.round(interp(sub.keys, t)).toLocaleString('en-US'));
  return '';
}
function clockAt(c, t) {
  if (!c) return '';
  if (c.text) return c.text;
  if (c.countdown_to !== undefined) return fmt(c.countdown_to - t);                       // real-time countdown to a screen time
  if (c.countdown_from !== undefined) return fmt(c.countdown_from - (t - c.start) / (c.slow || 1)); // slowed game clock
  if (c.count_up_from !== undefined) return fmt(c.count_up_from + (t - c.start) / (c.slow || 1));
  return '';
}
function drawAtom(cx, cy, r, t) {
  fx.save(); fx.translate(cx, cy);
  for (let k = 0; k < 3; k++) { fx.save(); fx.rotate(k * Math.PI / 3 + .3); fx.strokeStyle = 'rgba(235,240,255,.9)'; fx.lineWidth = Math.max(1, r * .035); fx.beginPath(); fx.ellipse(0, 0, r, r * .36, 0, 0, Math.PI * 2); fx.stroke();
    const a = t * (1.6 + k * .4) + k * 2, ex = Math.cos(a) * r, ey = Math.sin(a) * r * .36; const gr = fx.createRadialGradient(ex, ey, 0, ex, ey, r * .22); gr.addColorStop(0, '#fff'); gr.addColorStop(.3, 'rgba(110,170,255,.95)'); gr.addColorStop(1, 'rgba(60,120,255,0)'); fx.fillStyle = gr; fx.beginPath(); fx.arc(ex, ey, r * .22, 0, Math.PI * 2); fx.fill(); fx.restore(); }
  for (const [x, y, c] of [[-.07, -.05, '#d33'], [.07, -.04, '#eee'], [0, .07, '#d33'], [-.06, .06, '#eee'], [.06, .06, '#d33'], [0, -.1, '#eee']]) { const gx = x * r, gy = y * r, rad = r * .1; const gr = fx.createRadialGradient(gx - rad * .3, gy - rad * .3, rad * .1, gx, gy, rad); gr.addColorStop(0, '#fff'); gr.addColorStop(.4, c); gr.addColorStop(1, c === '#d33' ? '#701' : '#888'); fx.fillStyle = gr; fx.beginPath(); fx.arc(gx, gy, rad, 0, Math.PI * 2); fx.fill(); }
  fx.restore();
}
const ICONS = { atom: drawAtom };

window.renderAt = function (t) {
  fx.clearRect(0, 0, W, H); K.reset(); O.white(0); O.vignette(0); O._hud = true; $('end').style.display = 'none';
  const shot = shots.find(s => t >= s.from && t < s.to) || shots[shots.length - 1];
  shot.run(t, clamp((t - shot.from) / (shot.to - shot.from)));
  // title + icon
  const T = S.title || {}; const tA = t < (T.to ?? 5.8) - (T.fade ?? .8) ? 1 : 1 - ss((T.to ?? 5.8) - (T.fade ?? .8), T.to ?? 5.8, t);
  $('title').style.opacity = t < (T.to ?? 5.8) ? tA : 0; setText($('title'), hl(T.html));
  if (T.icon && ICONS[T.icon] && t < (T.icon_until ?? 8)) { const k = ss((T.to ?? 5.8) - .8, (T.to ?? 5.8) + .6, t); ICONS[T.icon](lerp(W / 2, 70, k), lerp(205, 560, k), lerp(70, 26, k), t); }
  // HUD
  const seg = (S.hud || []).find(h => t >= h.from && t < h.to);
  const hudOn = O._hud && !!seg; $('hud').style.display = hudOn ? 'block' : 'none';
  if (seg) { setText($('hudl'), seg.label || ''); setText($('hudt'), clockAt(seg.clock, t)); setText($('huds'), subAt(seg.sub, t)); }
  // captions
  let cap = '', ca = 0; for (const [a, b, s] of S.captions || []) if (t >= a && t < b) { cap = s; ca = Math.min(ss(a, a + .25, t), 1 - ss(b - .25, b, t)); }
  setText($('cap'), hl(cap)); $('cap').style.opacity = ca;
  // end card
  const E = S.end_card; if (E && t >= E.from) { $('end').style.display = 'block'; setText($('endt'), hl(E.html)); setText($('ends'), E.fact || ''); $('hud').style.display = 'none'; }
  renderer.render(scene, camera);
};
window.SCENARIO = S;
await document.fonts.ready;
await Promise.all(['400 50px Garamond', 'italic 500 33px Garamond', '600 14px InterX', '400 11px Mono'].map(f => document.fonts.load(f)));
const missing = ['400 16px Garamond', 'italic 500 16px Garamond', '600 16px InterX', '400 16px Mono'].filter(f => !document.fonts.check(f));
if (missing.length) { window.FONT_ERROR = 'missing fonts: ' + missing.join(', '); }
window.renderAt(0); window.READY = true;
