// STATUR SIM 3D kit v2: articulated characters (people, Dr. Louis host, robots), city blocks with lit windows,
// streets, cars, lamps, screens, signs, aircraft, props. Seeded randomness only.
import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

export function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
export const V = (x, y, z) => new THREE.Vector3(x, y, z);
export const easeIO = k => k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
export function tex(w, h, draw, rep) { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); } t.userData.canvas = c; return t; }
export function gradTex(stops) { return tex(4, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); stops.forEach(([o, c]) => gr.addColorStop(o, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h); }); }
const lam = (c, o = {}) => new THREE.MeshLambertMaterial({ color: c, flatShading: true, ...o });
const box = (w, h, d) => new THREE.BoxGeometry(w, h, d);

// ---------- camera helpers ----------
export function camPath(camera, t, a, b, p0, p1, l0, l1, shake = 0) {
  const k = easeIO(Math.min(1, Math.max(0, (t - a) / (b - a)))); const p = p0.clone().lerp(p1, k), l = l0.clone().lerp(l1, k);
  if (shake) { p.x += Math.sin(t * 2.1) * shake + Math.sin(t * 5.3) * shake * .3; p.y += Math.sin(t * 1.7 + 1) * shake * .7; }
  camera.position.copy(p); camera.lookAt(l);
}

// ---------- characters ----------
const SKIN = [0xf1c6a2, 0xd9a67e, 0xb07a54, 0x8a5a3c, 0x5e3c28];
const CLOTH = [0x2a5bd7, 0xe8e2d6, 0xd4b13a, 0xc0392b, 0x2e8b57, 0x6b4fa0, 0x30343c, 0xe67e22, 0xf2efe8, 0x17808a];
const HAIR = [0x1c1612, 0x3b2a1e, 0x6b4a2b, 0xc89b5c, 0x9a9a9a];
export function person(R, o = {}) {
  const s = o.scale ?? 1, g = new THREE.Group();
  const skinM = lam(o.skin ?? SKIN[Math.floor(R() * SKIN.length)]), clothM = lam(o.cloth ?? CLOTH[Math.floor(R() * CLOTH.length)]), pantsM = lam(o.pants ?? [0x23283a, 0x3a3a3a, 0x4b5d7a, 0x6a5a48][Math.floor(R() * 4)]), hairM = lam(o.hair ?? HAIR[Math.floor(R() * HAIR.length)]);
  const hips = new THREE.Group(); hips.position.y = .9 * s; g.add(hips);
  const torso = new THREE.Mesh(box(.46 * s, .62 * s, .26 * s), clothM); torso.position.y = .33 * s; hips.add(torso);
  const head = new THREE.Group(); head.position.y = .78 * s; hips.add(head);
  const hm = new THREE.Mesh(box(.3 * s, .32 * s, .3 * s), skinM); head.add(hm);
  if (!o.bald) { const hr = new THREE.Mesh(box(.32 * s, .1 * s, .32 * s), hairM); hr.position.y = .15 * s; head.add(hr); const hb = new THREE.Mesh(box(.32 * s, .22 * s, .08 * s), hairM); hb.position.set(0, .05 * s, -.13 * s); head.add(hb); }
  const eyeM = new THREE.MeshBasicMaterial({ color: 0x111111 });
  for (const sx of [-.07, .07]) { const e = new THREE.Mesh(box(.045 * s, .06 * s, .01), eyeM); e.position.set(sx * s, .02 * s, .151 * s); head.add(e); }
  const limb = (w, h, m, x, y, parent) => { const pv = new THREE.Group(); pv.position.set(x, y, 0); const mesh = new THREE.Mesh(box(w, h, w), m); mesh.position.y = -h / 2; pv.add(mesh); parent.add(pv); return pv; };
  const armL = limb(.13 * s, .58 * s, clothM, -.31 * s, .6 * s, hips), armR = limb(.13 * s, .58 * s, clothM, .31 * s, .6 * s, hips);
  for (const a of [armL, armR]) { const h = new THREE.Mesh(box(.12 * s, .12 * s, .12 * s), skinM); h.position.y = -.62 * s; a.add(h); }
  const legL = limb(.17 * s, .9 * s, pantsM, -.12 * s, 0, hips), legR = limb(.17 * s, .9 * s, pantsM, .12 * s, 0, hips);
  g.userData = { s, hips, torso, head, armL, armR, legL, legR, phase: R() * 6.28, mats: { skinM, clothM, pantsM, hairM } };
  if (o.phone) { const ph = new THREE.Mesh(box(.08 * s, .14 * s, .02 * s), new THREE.MeshBasicMaterial({ color: 0x9fd0ff })); ph.position.set(0, -.62 * s, .1 * s); armR.add(ph); g.userData.phone = ph; }
  if (o.sign) { const sg = signMesh(o.sign, o.signColor); sg.position.set(0, -.2 * s, .12); sg.scale.setScalar(s); armR.add(sg); g.userData.sign = sg; }
  return g;
}
// pose: mode in walk | stand | idle | cheer | march | phone | sit | type | point | shrug
export function pose(p, t, mode = 'idle', o = {}) {
  const u = p.userData, ph = u.phase + t * (o.speed ?? 6), s = u.s; const sw = Math.sin(ph);
  u.hips.position.y = .9 * s; u.hips.rotation.set(0, 0, 0); u.head.rotation.set(0, 0, 0); u.torso.rotation.set(0, 0, 0);
  u.armL.rotation.set(0, 0, 0); u.armR.rotation.set(0, 0, 0); u.legL.rotation.set(0, 0, 0); u.legR.rotation.set(0, 0, 0);
  if (mode === 'walk' || mode === 'march') { const a = mode === 'march' ? .7 : .55; u.legL.rotation.x = sw * a; u.legR.rotation.x = -sw * a; u.armL.rotation.x = -sw * a * .9; u.armR.rotation.x = sw * a * .9; u.hips.position.y = .9 * s + Math.abs(Math.cos(ph)) * .04 * s;
    if (mode === 'march') { u.armR.rotation.x = -Math.PI + .25 + Math.sin(ph * .5) * .15; } }
  else if (mode === 'cheer') { u.armL.rotation.z = -2.6 - Math.sin(ph * 1.3) * .3; u.armR.rotation.z = 2.6 + Math.sin(ph * 1.3 + 1) * .3; u.hips.position.y = .9 * s + Math.max(0, Math.sin(ph * 1.3)) * .12 * s; }
  else if (mode === 'phone') { u.armR.rotation.x = -1.25; u.armR.rotation.z = .25; u.head.rotation.x = .35 + Math.sin(ph * .3) * .03; u.torso.rotation.x = .05; }
  else if (mode === 'sit') { u.hips.position.y = .48 * s; u.legL.rotation.x = -1.5; u.legR.rotation.x = -1.5; u.armL.rotation.x = -.9; u.armR.rotation.x = -.9; }
  else if (mode === 'type') { u.hips.position.y = .48 * s; u.legL.rotation.x = -1.5; u.legR.rotation.x = -1.5; u.armL.rotation.x = -1.2 + Math.sin(ph * 3) * .08; u.armR.rotation.x = -1.2 + Math.sin(ph * 3 + 2) * .08; u.head.rotation.x = .1; }
  else if (mode === 'shrug') { const k = (Math.sin(ph * .7) + 1) / 2; u.armL.rotation.z = -.6 - k * .4; u.armR.rotation.z = .6 + k * .4; u.armL.rotation.x = -.5; u.armR.rotation.x = -.5; u.head.rotation.z = Math.sin(ph * .7) * .15; }
  else if (mode === 'point') { u.armR.rotation.x = -1.5; u.armR.rotation.y = .2; u.head.rotation.y = .2; }
  else if (mode === 'look_up') { u.head.rotation.x = -.5; u.armL.rotation.z = -.15; u.armR.rotation.z = .15; u.torso.rotation.x = -.05; }
  else { u.armL.rotation.z = -.08 + Math.sin(ph * .3) * .02; u.armR.rotation.z = .08 - Math.sin(ph * .3) * .02; u.hips.position.y = .9 * s + Math.sin(ph * .4) * .008; u.head.rotation.y = Math.sin(ph * .25) * .25; }
  if (o.angry) { u.armL.rotation.x = -2.6 + Math.sin(ph * 2) * .4; }
}
// Host character: curly hair, round glasses, lab coat, black tee with an accent dot. Chibi proportions. Recolor per brand.
export function host(scale = 1) {
  const s = scale, g = new THREE.Group(); const R = rng(77);
  const skin = lam(0xf0c9a8), coat = lam(0xf2efe8), tee = lam(0x0e0e0c), pants = lam(0x24262c), hairM = lam(0xb5642e), rim = new THREE.MeshBasicMaterial({ color: 0x111111 });
  const hips = new THREE.Group(); hips.position.y = .75 * s; g.add(hips);
  const torso = new THREE.Mesh(box(.5 * s, .58 * s, .3 * s), tee); torso.position.y = .3 * s; hips.add(torso);
  const dot = new THREE.Mesh(new THREE.CircleGeometry(.05 * s, 16), new THREE.MeshBasicMaterial({ color: 0xe8501c })); dot.position.set(0, .38 * s, .152 * s); hips.add(dot);
  for (const sx of [-1, 1]) { const flap = new THREE.Mesh(box(.16 * s, .78 * s, .32 * s), coat); flap.position.set(sx * .2 * s, .22 * s, 0); hips.add(flap); }
  const head = new THREE.Group(); head.position.y = .9 * s; hips.add(head);
  const hm = new THREE.Mesh(new THREE.SphereGeometry(.3 * s, 20, 16), lam(0xf0c9a8, { flatShading: false })); hm.scale.set(1, 1.08, .95); head.add(hm);
  // curly hair: cluster of spheres on top/back/sides
  const hairGeos = []; for (let i = 0; i < 46; i++) { const th = R() * Math.PI * 2, ph = R() * 1.25; const r = .3 * s; const x = Math.cos(th) * Math.sin(ph) * r * 1.15, y = Math.cos(ph) * r * 1.0 + .06 * s, z = Math.sin(th) * Math.sin(ph) * r * 1.15 - .04 * s; if (z > .16 * s && y < .2 * s) continue;
    const sg = new THREE.IcosahedronGeometry((.09 + R() * .06) * s, 1); sg.translate(x, y + .05 * s, z); hairGeos.push(sg); }
  const hair = new THREE.Mesh(mergeGeometries(hairGeos), lam(0xb5642e)); head.add(hair);
  // round glasses
  for (const sx of [-.11, .11]) { const r = new THREE.Mesh(new THREE.TorusGeometry(.075 * s, .012 * s, 8, 24), rim); r.position.set(sx * s, .01 * s, .29 * s); head.add(r);
    const lens = new THREE.Mesh(new THREE.CircleGeometry(.07 * s, 20), new THREE.MeshBasicMaterial({ color: 0xbfe3ff, transparent: true, opacity: .25 })); lens.position.set(sx * s, .01 * s, .292 * s); head.add(lens);
    const eye = new THREE.Mesh(new THREE.CircleGeometry(.028 * s, 12), rim); eye.position.set(sx * s, .005 * s, .293 * s); head.add(eye); }
  const bridge = new THREE.Mesh(box(.07 * s, .012 * s, .012 * s), rim); bridge.position.set(0, .02 * s, .29 * s); head.add(bridge);
  const mouth = new THREE.Mesh(box(.1 * s, .02 * s, .01 * s), new THREE.MeshBasicMaterial({ color: 0x6b2a1e })); mouth.position.set(0, -.13 * s, .285 * s); head.add(mouth);
  const limb = (w, h, m, x, y) => { const pv = new THREE.Group(); pv.position.set(x, y, 0); const mesh = new THREE.Mesh(box(w, h, w), m); mesh.position.y = -h / 2; pv.add(mesh); hips.add(pv); return pv; };
  const armL = limb(.14 * s, .5 * s, coat, -.33 * s, .55 * s), armR = limb(.14 * s, .5 * s, coat, .33 * s, .55 * s);
  for (const a of [armL, armR]) { const h = new THREE.Mesh(box(.13 * s, .13 * s, .13 * s), skin); h.position.y = -.55 * s; a.add(h); }
  const legL = limb(.17 * s, .75 * s, pants, -.13 * s, 0), legR = limb(.17 * s, .75 * s, pants, .13 * s, 0);
  g.userData = { s, hips, torso, head, armL, armR, legL, legR, mouth, phase: 0 };
  return g;
}
export function hostPose(L, t, mode = 'talk') {
  const u = L.userData, s = u.s; u.armL.rotation.set(0, 0, 0); u.armR.rotation.set(0, 0, 0); u.head.rotation.set(0, 0, 0); u.hips.position.y = .75 * s; u.legL.rotation.set(0, 0, 0); u.legR.rotation.set(0, 0, 0);
  u.mouth.scale.y = mode === 'talk' || mode === 'present' ? 1 + Math.abs(Math.sin(t * 13)) * 3 : 1;
  if (mode === 'talk') { u.armR.rotation.z = .5 + Math.sin(t * 3) * .25; u.armR.rotation.x = -.6; u.head.rotation.y = Math.sin(t * 1.3) * .2; u.head.rotation.z = Math.sin(t * 2.1) * .06; }
  else if (mode === 'present') { u.armL.rotation.z = -1.2 - Math.sin(t * 2) * .1; u.armR.rotation.z = 1.2 + Math.sin(t * 2) * .1; u.head.rotation.y = Math.sin(t) * .15; }
  else if (mode === 'shock') { u.armL.rotation.x = -2.7; u.armR.rotation.x = -2.7; u.armL.rotation.z = -.3; u.armR.rotation.z = .3; u.head.rotation.x = -.15; }
  else if (mode === 'think') { u.armR.rotation.x = -2.1; u.armR.rotation.z = .6; u.head.rotation.z = .15; u.head.rotation.x = -.1; }
  else if (mode === 'walk') { const sw = Math.sin(t * 7); u.legL.rotation.x = sw * .5; u.legR.rotation.x = -sw * .5; u.armL.rotation.x = -sw * .5; u.armR.rotation.x = sw * .5; u.hips.position.y = .75 * s + Math.abs(Math.cos(t * 7)) * .04; }
  else if (mode === 'cheer') { u.armL.rotation.z = -2.6; u.armR.rotation.z = 2.6; u.hips.position.y = .75 * s + Math.max(0, Math.sin(t * 8)) * .1; }
}
export function robot(scale = 1, color = 0xd9dde3) {
  const s = scale, g = new THREE.Group(); const body = lam(color), dark = lam(0x2a2d33), visor = new THREE.MeshBasicMaterial({ color: 0xff7a3d });
  const hips = new THREE.Group(); hips.position.y = .85 * s; g.add(hips);
  const t = new THREE.Mesh(box(.5 * s, .55 * s, .32 * s), body); t.position.y = .3 * s; hips.add(t);
  const core = new THREE.Mesh(new THREE.CircleGeometry(.06 * s, 16), visor); core.position.set(0, .35 * s, .162 * s); hips.add(core);
  const head = new THREE.Group(); head.position.y = .78 * s; hips.add(head);
  head.add(new THREE.Mesh(box(.36 * s, .28 * s, .3 * s), body)); const v = new THREE.Mesh(box(.28 * s, .07 * s, .02 * s), visor); v.position.set(0, .02 * s, .155 * s); head.add(v);
  const ant = new THREE.Mesh(new THREE.CylinderGeometry(.01 * s, .01 * s, .14 * s), dark); ant.position.y = .2 * s; head.add(ant);
  const limb = (w, h, m, x, y) => { const pv = new THREE.Group(); pv.position.set(x, y, 0); const mesh = new THREE.Mesh(box(w, h, w), m); mesh.position.y = -h / 2; pv.add(mesh); hips.add(pv); return pv; };
  const armL = limb(.11 * s, .55 * s, dark, -.32 * s, .55 * s), armR = limb(.11 * s, .55 * s, dark, .32 * s, .55 * s), legL = limb(.15 * s, .85 * s, dark, -.12 * s, 0), legR = limb(.15 * s, .85 * s, dark, .12 * s, 0);
  g.userData = { s, hips, head, armL, armR, legL, legR, visor, phase: 0 };
  return g;
}
export function robotPose(r, t, mode = 'work') {
  const u = r.userData, s = u.s; u.armL.rotation.set(0, 0, 0); u.armR.rotation.set(0, 0, 0); u.legL.rotation.set(0, 0, 0); u.legR.rotation.set(0, 0, 0); u.head.rotation.set(0, 0, 0); u.hips.position.y = .85 * s;
  if (mode === 'work') { u.armL.rotation.x = -1.2 + Math.sin(t * 9) * .15; u.armR.rotation.x = -1.2 + Math.sin(t * 9 + 1.5) * .15; u.head.rotation.x = .15; }
  else if (mode === 'walk') { const sw = Math.sin(t * 6); u.legL.rotation.x = sw * .45; u.legR.rotation.x = -sw * .45; u.armL.rotation.x = -sw * .4; u.armR.rotation.x = sw * .4; }
  else if (mode === 'wave') { u.armR.rotation.z = 2.4 + Math.sin(t * 6) * .3; }
}

// ---------- signs, screens ----------
export function signTex(text, bg = '#f2efe8', fg = '#0e0e0c', w = 256, h = 160) {
  return tex(w, h, (g) => { g.fillStyle = bg; g.fillRect(0, 0, w, h); g.fillStyle = fg; g.textAlign = 'center'; g.textBaseline = 'middle'; const lines = text.split('\n'); const fs = Math.min(64, (h * .8) / lines.length);
    g.font = `900 ${fs}px Archivo`; lines.forEach((l, i) => g.fillText(l, w / 2, h / 2 + (i - (lines.length - 1) / 2) * fs * 1.05)); });
}
export function signMesh(text, color = '#f2efe8') {
  const g = new THREE.Group(); const board = new THREE.Mesh(new THREE.PlaneGeometry(.75, .47), new THREE.MeshLambertMaterial({ map: signTex(text, color), side: THREE.DoubleSide })); board.position.y = .9; g.add(board);
  const stick = new THREE.Mesh(box(.035, 1.0, .035), lam(0x8a6a48)); stick.position.y = .35; g.add(stick); return g;
}
export function screenTex(kind, seed = 1) {
  const R = rng(seed);
  return tex(256, 160, (g, w, h) => {
    const pal = [['#ff3d6e', '#ffd23d'], ['#3dd6ff', '#f2efe8'], ['#e8501c', '#f2efe8'], ['#9d5cff', '#3dffb5'], ['#ffd23d', '#0e0e0c']][Math.floor(R() * 5)];
    g.fillStyle = pal[0]; g.fillRect(0, 0, w, h); g.fillStyle = pal[1];
    if (kind === 'ad') { g.font = '900 52px Archivo'; g.textAlign = 'center'; g.fillText(['SALE', 'NEW', 'LIVE', 'BUY', 'NOW', '24/7', 'STREAM'][Math.floor(R() * 7)], w / 2, h / 2 + 18); }
    else if (kind === 'chart') { g.lineWidth = 6; g.strokeStyle = pal[1]; g.beginPath(); let y = h * .7; for (let x = 0; x <= w; x += 16) { y = Math.max(20, Math.min(h - 20, y - (R() - .4) * 24)); x ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); }
    else { for (let i = 0; i < 6; i++) { g.globalAlpha = .6 + R() * .4; g.fillRect(16, 14 + i * 24, 60 + R() * 160, 14); } }
  });
}
export const CANCELLED = () => tex(256, 256, (g, w, h) => { g.fillStyle = '#05070c'; g.fillRect(0, 0, w, h); g.font = '700 17px JBM'; const c = ['PARIS', 'TOKYO', 'NYC', 'LONDON', 'DUBAI', 'SYDNEY', 'BERLIN', 'LIMA', 'SEOUL', 'MADRID'];
  c.forEach((n, i) => { g.fillStyle = '#d8e1ff'; g.fillText(n, 14, 30 + i * 23); g.fillStyle = '#ff4a3d'; g.fillText('CANCELLED', 128, 30 + i * 23); }); });

// ---------- city ----------
export function windowTexture(seed, litFrac, warm = true) {
  const R = rng(seed);
  return tex(128, 256, (g, w, h) => { g.fillStyle = '#000'; g.fillRect(0, 0, w, h); for (let y = 6; y < h; y += 16) for (let x = 6; x < w; x += 16) { if (R() < litFrac) { g.fillStyle = warm ? ['#ffd28a', '#ffe7b8', '#fff2d6', '#9fd0ff'][Math.floor(R() * 4)] : '#bfe0ff'; g.globalAlpha = .55 + R() * .45; g.fillRect(x, y, 9, 10); } } g.globalAlpha = 1; });
}
export function building(R, w, h, d, o = {}) {
  const g = new THREE.Group();
  const facade = o.color ?? [0x3a3f4a, 0x2f333b, 0x4a4540, 0x504a55, 0x2c3440][Math.floor(R() * 5)];
  const mats = []; const wt = windowTexture(Math.floor(R() * 1e6), o.lit ?? .45); wt.wrapS = wt.wrapT = THREE.RepeatWrapping; wt.repeat.set(Math.max(1, Math.round(w / 6)), Math.max(1, Math.round(h / 12)));
  const m = new THREE.MeshLambertMaterial({ color: facade, emissive: 0xffffff, emissiveMap: wt, emissiveIntensity: o.night ? 1.2 : .0 });
  const mesh = new THREE.Mesh(box(w, h, d), [m, m, lam(facade), lam(facade), m, m]); mesh.position.y = h / 2; mesh.castShadow = !!o.shadow; mesh.receiveShadow = !!o.shadow; g.add(mesh);
  if (R() < .4) { const top = new THREE.Mesh(box(w * .5, h * .08, d * .5), lam(facade)); top.position.y = h + h * .04; g.add(top); }
  g.userData = { winMat: m }; return g;
}
export function cityBlock(R, o = {}) {
  // two facades along a street on the z axis; returns group + list of building groups
  const g = new THREE.Group(), list = [];
  for (const side of [-1, 1]) { let z = o.z0 ?? 10; while (z > (o.z1 ?? -160)) { const d = 8 + R() * 10, w = 9 + R() * 8, h = (o.hmin ?? 12) + R() * ((o.hmax ?? 60) - (o.hmin ?? 12)); const b = building(R, w, h, d, o); b.position.set(side * ((o.width ?? 9) + w / 2), 0, z - d / 2); g.add(b); list.push(b); z -= d + .3; } }
  return { group: g, list };
}
export function car(R, color) {
  const g = new THREE.Group(); const c = color ?? [0xd23b2f, 0xf2efe8, 0x2a5bd7, 0x1c1c19, 0xd4b13a, 0x8a8780][Math.floor(R() * 6)];
  const b = new THREE.Mesh(box(1.8, .6, 4), lam(c)); b.position.y = .55; g.add(b); const cab = new THREE.Mesh(box(1.6, .5, 2.1), lam(0x1c2230)); cab.position.set(0, 1.05, -.2); g.add(cab);
  const hl = new THREE.MeshBasicMaterial({ color: 0xfff1c9 }), tl = new THREE.MeshBasicMaterial({ color: 0xff2a1a });
  for (const sx of [-.6, .6]) { const h = new THREE.Mesh(box(.35, .16, .05), hl); h.position.set(sx, .62, 2.01); g.add(h); const tt = new THREE.Mesh(box(.35, .14, .05), tl); tt.position.set(sx, .62, -2.01); g.add(tt); }
  for (const sx of [-.85, .85]) for (const sz of [-1.3, 1.3]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(.33, .33, .22, 12).rotateZ(Math.PI / 2), lam(0x111111)); w.position.set(sx, .33, sz); g.add(w); }
  g.userData = { hl, tl }; return g;
}
export function lamp(on = true) {
  const g = new THREE.Group(); const pole = new THREE.Mesh(new THREE.CylinderGeometry(.07, .09, 6, 8), lam(0x2a2d33)); pole.position.y = 3; g.add(pole);
  const arm = new THREE.Mesh(box(1.2, .08, .08), lam(0x2a2d33)); arm.position.set(.55, 5.95, 0); g.add(arm);
  const bulb = new THREE.Mesh(box(.45, .12, .3), new THREE.MeshBasicMaterial({ color: on ? 0xffd9a0 : 0x333333 })); bulb.position.set(1.05, 5.86, 0); g.add(bulb);
  const cone = new THREE.Mesh(new THREE.ConeGeometry(2.2, 5.8, 20, 1, true), new THREE.MeshBasicMaterial({ color: 0xffd9a0, transparent: true, opacity: .03, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide })); cone.position.set(1.05, 2.95, 0); g.add(cone);
  g.userData = { bulb, cone }; return g;
}
export function setLamp(l, on) { l.userData.bulb.material.color.set(on ? 0xffd9a0 : 0x2a2a2a); l.userData.cone.visible = false; }
export function aircraft(color = 0xf2efe8) {
  const g = new THREE.Group(); const m = lam(color);
  const f = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 16, 14).rotateX(Math.PI / 2), m); f.position.y = 2.2; g.add(f);
  const nose = new THREE.Mesh(new THREE.SphereGeometry(1.2, 14, 10), m); nose.position.set(0, 2.2, 8); g.add(nose);
  const wing = new THREE.Mesh(box(18, .25, 3), m); wing.position.set(0, 1.8, 1); g.add(wing);
  const tail = new THREE.Mesh(box(.25, 3, 2.2), lam(0xe8501c)); tail.position.set(0, 4.2, -7); g.add(tail);
  const stab = new THREE.Mesh(box(6, .2, 1.6), m); stab.position.set(0, 2.6, -7); g.add(stab); return g;
}
export function stars(n = 2500, rad = 1500, seed = 9) {
  const r = rng(seed), p = []; for (let i = 0; i < n; i++) { const u = r(), a = r() * Math.PI * 2, s = Math.sqrt(1 - u * u); p.push(rad * s * Math.cos(a), rad * u, rad * s * Math.sin(a)); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3));
  return new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 1.6, sizeAttenuation: false, transparent: true, opacity: .85 }));
}
export function mergeAll(geos) { return mergeGeometries(geos.map(g => g.index ? g.toNonIndexed() : g)); }
