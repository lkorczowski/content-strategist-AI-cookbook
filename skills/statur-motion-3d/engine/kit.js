// statur-motion-3d scene kit. Builds a procedural low-poly world (park, skyline, crowd, trees),
// POV hands, particles, stars, Earth and Moon, and a point-cloud copy of the world.
// Every object has render modes: day, wire (white edges on black), glow, points.
// Deterministic: seeded random only, nothing depends on wall-clock time.
import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

export function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, k) => a + (b - a) * k;
export const ss = (a, b, x) => { const k = clamp((x - a) / (b - a)); return k * k * (3 - 2 * k); };
export const easeIO = k => k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
export const V = (x, y, z) => new THREE.Vector3(x, y, z);

function canvasTex(w, h, draw, repeat) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  if (repeat) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(repeat[0], repeat[1]); }
  return t;
}
export function fbmCanvas(w, h, seed, octaves, palette) {
  const r = rng(seed), G = 64, grid = []; for (let i = 0; i < G * G; i++) grid.push(r());
  const at = (x, y) => grid[((y % G + G) % G) * G + ((x % G + G) % G)];
  const vn = (x, y) => { const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi; const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
    return lerp(lerp(at(xi, yi), at(xi + 1, yi), u), lerp(at(xi, yi + 1), at(xi + 1, yi + 1), u), v); };
  const c = document.createElement('canvas'); c.width = w; c.height = h; const ctx = c.getContext('2d'); const img = ctx.createImageData(w, h);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    let s = 0, a = .5, f = 8 / 64;
    for (let o = 0; o < octaves; o++) { s += a * vn(x * f, y * f); a *= .5; f *= 2; }
    const col = palette(s); const i = (y * w + x) * 4; img.data[i] = col[0]; img.data[i + 1] = col[1]; img.data[i + 2] = col[2]; img.data[i + 3] = 255;
  }
  ctx.putImageData(img, 0, 0); return c;
}

export function buildKit({ scene, camera, seed = 42 }) {
  const R = rng(seed); const rr = (a, b) => a + (b - a) * R();
  const K = { THREE, scene, camera };

  // ---------- textures ----------
  const skyDay = canvasTex(4, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#a9a6bd'); gr.addColorStop(.55, '#d8d3dd'); gr.addColorStop(1, '#efe6e4'); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  const grassTex = new THREE.CanvasTexture(fbmCanvas(256, 256, 7, 4, s => { const v = 0.75 + s * 0.5; return [52 * v, 128 * v, 38 * v]; }));
  grassTex.wrapS = grassTex.wrapT = THREE.RepeatWrapping; grassTex.repeat.set(60, 60); grassTex.colorSpace = THREE.SRGBColorSpace;
  const speckTex = canvasTex(512, 512, (g, w, h) => { g.fillStyle = '#000'; g.fillRect(0, 0, w, h); const r = rng(3);
    for (let i = 0; i < 26000; i++) { const v = 40 + r() * 150; g.fillStyle = `rgb(${v},${v},${v + 10})`; g.fillRect(r() * w, r() * h, 1 + (r() < .1), 1); } }, [260, 260]);
  const windowTex = day => canvasTex(64, 64, (g, w, h) => {
    if (day) { g.fillStyle = '#9a9ca6'; g.fillRect(0, 0, w, h); g.fillStyle = '#525a6a'; for (let y = 4; y < h; y += 16) for (let x = 4; x < w; x += 16) g.fillRect(x, y, 9, 10); }
    else { g.fillStyle = '#000'; g.fillRect(0, 0, w, h); g.strokeStyle = 'rgba(230,238,255,.95)'; g.lineWidth = 1.5; for (let y = 1; y < h; y += 16) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); } for (let x = 1; x < w; x += 16) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, h); g.stroke(); } }
  }, [1, 1]);
  const glowTex = canvasTex(128, 128, (g) => { const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.25, 'rgba(235,242,255,.7)'); gr.addColorStop(1, 'rgba(200,215,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); });
  const cloudTex = new THREE.CanvasTexture(fbmCanvas(1024, 512, 11, 6, s => { const v = clamp((s - .25) * 1.6); return [lerp(150, 250, v), lerp(170, 252, v), lerp(220, 255, v)]; }));
  cloudTex.colorSpace = THREE.SRGBColorSpace; cloudTex.wrapS = cloudTex.wrapT = THREE.RepeatWrapping;
  const moonTex = new THREE.CanvasTexture(fbmCanvas(256, 128, 5, 5, s => { const v = 80 + s * 90; return [v, v, v * 1.02]; })); moonTex.colorSpace = THREE.SRGBColorSpace;
  K.tex = { skyDay, glowTex, cloudTex };

  // ---------- materials ----------
  const lam = (o) => new THREE.MeshLambertMaterial(o);
  const M = {
    grass: lam({ map: grassTex }), crown: lam({ color: 0x2f4a22, flatShading: true }), crown2: lam({ color: 0x3b5a28, flatShading: true }),
    trunk: lam({ color: 0x4a3a2c, flatShading: true }), bldg: lam({ map: windowTex(true) }), bldgBrick: lam({ color: 0x9a6a55, map: windowTex(true) }),
    skin: lam({ color: 0xd9a67e, flatShading: true }), pants: lam({ color: 0x2d3446, flatShading: true }),
    blanket: lam({ map: canvasTex(64, 64, (g) => { for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) { g.fillStyle = (x + y) % 2 ? '#f2f0ee' : '#c8202a'; g.fillRect(x * 8, y * 8, 8, 8); } }) }),
  };
  const shirtMats = [0x2a5bd7, 0xe8e2d6, 0xd4b13a, 0xc0392b, 0x2e8b57, 0x6b4fa0, 0x333333, 0xe67e22, 0xffffff].map(c => lam({ color: c, flatShading: true }));
  const off = { polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 };
  const BLACK = new THREE.MeshBasicMaterial({ color: 0x000000, ...off });
  const WIREWIN = new THREE.MeshBasicMaterial({ map: windowTex(false), ...off });
  const WIREGROUND = new THREE.MeshBasicMaterial({ map: speckTex });
  const LINE = new THREE.LineBasicMaterial({ color: 0xdfe8ff, transparent: true, opacity: 0.95 });
  const GLOWFILL = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0 });
  K.mat = { LINE, GLOWFILL, shirtMats };

  scene.add(new THREE.HemisphereLight(0xe9e6f2, 0x4a6a35, 1.6));
  const sun = new THREE.DirectionalLight(0xfff3e6, 1.5); sun.position.set(-40, 80, 30); scene.add(sun);

  // ---------- world (geometries collected per material, then merged) ----------
  const buckets = new Map(), edgeGeos = [], fillGeos = [], winGeos = [], surfPts = [];
  function put(geo, mat, opts = {}) {
    if (!buckets.has(mat)) buckets.set(mat, []); buckets.get(mat).push(geo);
    edgeGeos.push(new THREE.EdgesGeometry(geo, opts.edgeAngle ?? 25));
    (opts.windows ? winGeos : fillGeos).push(geo);
    const n = opts.samples ?? 0; const p = geo.attributes.position;
    for (let i = 0; i < n; i++) { const a = Math.floor(R() * p.count / 3) * 3; const u = R(), v = R() * (1 - u);
      const A = new THREE.Vector3().fromBufferAttribute(p, a), B = new THREE.Vector3().fromBufferAttribute(p, a + 1), C = new THREE.Vector3().fromBufferAttribute(p, a + 2);
      surfPts.push(A.multiplyScalar(1 - u - v).add(B.multiplyScalar(u)).add(C.multiplyScalar(v))); }
  }
  const box = (w, h, d, x, y, z, ry = 0, rx = 0, rz = 0) => { const g = new THREE.BoxGeometry(w, h, d).toNonIndexed(); g.applyMatrix4(new THREE.Matrix4().makeRotationFromEuler(new THREE.Euler(rx, ry, rz))); g.translate(x, y, z); return g; };
  K.put = put; K.box = box; K.M = M;

  const groundDay = new THREE.Mesh(new THREE.PlaneGeometry(1600, 1600).rotateX(-Math.PI / 2), M.grass); scene.add(groundDay);
  const groundWire = new THREE.Mesh(new THREE.PlaneGeometry(1600, 1600).rotateX(-Math.PI / 2), WIREGROUND); scene.add(groundWire);
  { const pts = []; for (let i = 0; i < 6; i++) { const z = -8 - i * 7 - rr(0, 3); pts.push(-60, 0.02, z, 60, 0.02, z + rr(-2, 2)); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3)); edgeGeos.push(g); }

  for (let i = 0; i < 46; i++) {           // skyline
    const x = rr(-330, 330), z = rr(-190, -460), w = rr(18, 40), d = rr(18, 34);
    let h = rr(40, 110); if (R() < .3) h = rr(140, 230); if (Math.abs(x) < 90 && R() < .45) h = rr(230, 330);
    const g = box(w, h, d, x, h / 2, z); const uv = g.attributes.uv; for (let k = 0; k < uv.count; k++) uv.setXY(k, uv.getX(k) * w / 9, uv.getY(k) * h / 9);
    put(g, R() < .25 ? M.bldgBrick : M.bldg, { windows: true, edgeAngle: 30, samples: Math.floor(h * .9) });
    if (h > 140 && R() < .6) { const sh = rr(15, 40); put(box(w * .55, sh, d * .55, x, h + sh / 2, z), M.bldg, { windows: true, samples: 30 }); }
  }
  function tree(x, z, s) {
    const th = rr(2.4, 3.6) * s;
    put(new THREE.CylinderGeometry(.18 * s, .28 * s, th, 5).toNonIndexed().translate(x, th / 2, z), M.trunk, { samples: 6 });
    for (let b = 0; b < 2; b++) { const a = rr(-.6, .6); put(new THREE.CylinderGeometry(.08 * s, .12 * s, 1.6 * s, 4).toNonIndexed().applyMatrix4(new THREE.Matrix4().makeRotationZ(a)).translate(x + Math.sin(-a) * .6 * s, th * .85, z), M.trunk); }
    const cg = new THREE.IcosahedronGeometry(1, 0).toNonIndexed(); const p = cg.attributes.position;
    for (let k = 0; k < p.count; k++) p.setXYZ(k, p.getX(k) * (1 + rr(-.08, .08)), p.getY(k), p.getZ(k));
    cg.scale(rr(2.6, 3.4) * s, rr(1.5, 2.0) * s, rr(2.6, 3.4) * s); cg.rotateY(rr(0, 6)); cg.translate(x, th + 1.2 * s, z);
    put(cg, R() < .5 ? M.crown : M.crown2, { edgeAngle: 1, samples: 90 });
  }
  for (let i = 0; i < 150; i++) tree(rr(-70, 70), rr(-22, -75), rr(.9, 1.4));
  for (let i = 0; i < 18; i++) tree(rr(-50, -14) * (R() < .5 ? 1 : -1), rr(-14, -20), rr(.8, 1.1));

  function person(x, z, ry, pose, mat, s = 1, dress = false) {
    const m = new THREE.Matrix4().makeRotationY(ry); const T = (g) => { g.applyMatrix4(m); g.translate(x, 0, z); return g; };
    const sit = pose === 'sit'; const hip = sit ? 0.28 : 0.95 * s;
    put(T(box(.44 * s, .58 * s, .26 * s, 0, hip + .3 * s, 0)), mat, { samples: 14 });
    put(T(box(.22 * s, .25 * s, .22 * s, 0, hip + .76 * s, 0)), M.skin, { samples: 6 });
    if (dress) put(T(new THREE.CylinderGeometry(.2 * s, .42 * s, .62 * s, 6).toNonIndexed().translate(0, hip - .25 * s, 0)), mat, { samples: 10 });
    if (sit) { for (const sx of [-.12, .12]) put(T(box(.17 * s, .16 * s, .62 * s, sx * s, .1, .3 * s)), M.pants, { samples: 6 }); }
    else { for (const sx of [-.12, .12]) put(T(box(.17 * s, hip, .18 * s, sx * s, hip / 2, 0)), dress ? M.skin : M.pants, { samples: 6 }); }
    const armA = sit ? .5 : .1; put(T(box(.12 * s, .55 * s, .13 * s, -.3 * s, hip + .3 * s, .05, 0, -armA, .15)), mat); put(T(box(.12 * s, .55 * s, .13 * s, .3 * s, hip + .3 * s, .05, 0, -armA, -.15)), mat);
  }
  K.person = person; K.tree = tree;
  // foreground picnic group, scattered crowd (corridor x -3..1, z > -12 kept clear for close shots), one standing figure
  put(new THREE.PlaneGeometry(2.4, 1.8).rotateX(-Math.PI / 2).rotateY(.15).translate(1.2, 0.015, -1.6).toNonIndexed(), M.blanket, { edgeAngle: 1, samples: 40 });
  person(0.4, -1.2, 2.3, 'sit', shirtMats[1]); person(1.3, -2.3, 3.0, 'sit', shirtMats[0]); person(2.1, -1.4, -2.0, 'sit', shirtMats[2]);
  for (let i = 0; i < 70; i++) { const z = rr(-9, -30), x = rr(-30, 30); if (Math.abs(x + 1.2) < 2 && z > -12) continue; person(x, z, rr(0, 6.28), R() < .45 ? 'sit' : 'stand', shirtMats[Math.floor(R() * shirtMats.length)], rr(.9, 1.05)); }
  for (let i = 0; i < 7; i++) put(new THREE.PlaneGeometry(2, 1.5).rotateX(-Math.PI / 2).rotateY(rr(0, 3)).translate(rr(-20, 20), .015, rr(-8, -20)).toNonIndexed(), M.blanket, { edgeAngle: 1 });
  person(-1.2, -6.0, 0.25, 'stand', shirtMats[6], 1.05, true);
  K.anchors = { picnic: V(1.2, 0, -1.6), standing: V(-1.2, 0, -6), skyline: V(0, 9, -80) };

  // merge into three render groups
  const dayGroup = new THREE.Group(); for (const [mat, geos] of buckets) dayGroup.add(new THREE.Mesh(mergeGeometries(geos), mat)); scene.add(dayGroup);
  const strip = (g, keepUV) => { const c = g.clone(); if (!keepUV) c.deleteAttribute('uv'); c.deleteAttribute('normal'); return c; };
  const wireGroup = new THREE.Group();
  const fillMesh = new THREE.Mesh(mergeGeometries(fillGeos.map(g => strip(g, false))), BLACK);
  wireGroup.add(fillMesh, new THREE.Mesh(mergeGeometries(winGeos.map(g => strip(g, true))), WIREWIN), new THREE.LineSegments(mergeGeometries(edgeGeos), LINE));
  scene.add(wireGroup);
  const glowGroup = new THREE.Mesh(fillMesh.geometry, GLOWFILL); scene.add(glowGroup);

  // stars
  function starField(n, rad, sd, size) {
    const r = rng(sd), p = []; for (let i = 0; i < n; i++) { const u = r() * 2 - 1, a = r() * Math.PI * 2, s = Math.sqrt(1 - u * u); p.push(rad * s * Math.cos(a), rad * Math.abs(u) * (r() < .85 ? 1 : -1), rad * s * Math.sin(a)); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3));
    return new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size, sizeAttenuation: false, transparent: true, opacity: .9 }));
  }
  const stars = new THREE.Group(); stars.add(starField(4000, 1500, 9, 1.6), starField(900, 1500, 19, 2.6)); scene.add(stars);

  // POV hands (camera children, drawn on top)
  function makeHand(side) {
    const g = [box(.40, .40, .1, 0, 0, 0)]; const L = [.27, .31, .29, .22];
    for (let f = 0; f < 4; f++) g.push(box(.068, L[f], .08, -.135 + f * .09, .2 + L[f] / 2 + .015, 0, 0, 0, (f - 1.5) * -.06));
    g.push(box(.075, .24, .08, .25, .02, 0, 0, 0, -.75), box(.30, .9, .16, 0, -.66, 0));
    const geo = mergeGeometries(g); geo.scale(.55, .55, .55); if (side < 0) geo.scale(-1, 1, 1);
    const fill = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, depthTest: false }));
    const lines = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 20), new THREE.LineBasicMaterial({ color: 0xe8eeff, transparent: true, depthTest: false }));
    fill.renderOrder = 998; lines.renderOrder = 999; const grp = new THREE.Group(); grp.add(fill, lines); grp.userData = { fill, lines }; grp.visible = false; camera.add(grp); return grp;
  }
  const hands = [makeHand(-1), makeHand(1)];
  K.hands = (spread = 0, glow = 0) => { hands.forEach((h, i) => { const s = i ? 1 : -1; h.visible = true; h.position.set(s * (.2 + spread * .03), -.33, -1.35); h.rotation.set(-.15, -s * .25, -s * (.12 - spread * .2));
    h.userData.fill.material.opacity = glow; h.userData.lines.material.opacity = .95; }); };

  // particles: dust, sand, sparks, streaks
  const NP = 2600, pr = rng(77), pBase = new Float32Array(NP * 3), pVel = new Float32Array(NP * 3);
  for (let i = 0; i < NP * 3; i++) { pBase[i] = pr(); pVel[i] = pr(); } for (let i = 0; i < NP; i++) pBase[i * 3] = pBase[i * 3] * 2 - 1;
  const pGeo = new THREE.BufferGeometry(); pGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(NP * 3), 3));
  const pMat = new THREE.PointsMaterial({ color: 0xffffff, size: 2, sizeAttenuation: false, transparent: true, depthWrite: false });
  const points = new THREE.Points(pGeo, pMat); points.frustumCulled = false; scene.add(points);
  const sparkMat = new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true });
  const sparks = []; for (let i = 0; i < 160; i++) { const s = new THREE.Sprite(sparkMat); s.visible = false; scene.add(s); sparks.push(s); }
  const NS = 500, sGeo = new THREE.BufferGeometry(); sGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(NS * 6), 3));
  const streaks = new THREE.LineSegments(sGeo, new THREE.LineBasicMaterial({ color: 0xbfd0ff, transparent: true, opacity: .6 })); streaks.frustumCulled = false; scene.add(streaks);
  const sr = rng(99), sBase = []; for (let i = 0; i < NS; i++) sBase.push([sr(), sr(), sr(), sr()]);
  K.dust = (t, amt = 1) => { points.visible = true; const a = pGeo.attributes.position.array, c = camera.position;
    for (let i = 0; i < NP; i++) { const y = ((pBase[i * 3 + 1] * 6 - t * .25 * (pVel[i * 3] + .2)) % 6 + 6) % 6; a.set([c.x + pBase[i * 3] * 14, y * amt, c.z - 1 - pBase[i * 3 + 2] * 18], i * 3); }
    pGeo.attributes.position.needsUpdate = true; pMat.size = 1.6; pMat.opacity = .7; pMat.color.set(0xc9d6ff); };
  K.sand = (t, ign) => { points.visible = true; const a = pGeo.attributes.position.array, c = camera.position;
    for (let i = 0; i < NP; i++) { const lift = ign * pVel[i * 3 + 1] * 2.2 * (.5 + .5 * Math.sin(t * 2 + i)); a.set([c.x + pBase[i * 3] * 6, .01 + lift * pVel[i * 3 + 2], c.z - .3 - pBase[i * 3 + 2] * 9], i * 3); }
    pGeo.attributes.position.needsUpdate = true; pMat.size = 1.5 + ign * 2.5; pMat.opacity = .5 + .5 * ign; pMat.color.set(0xffffff);
    const n = Math.floor(ign * sparks.length);
    for (let i = 0; i < n; i++) { const s = sparks[i]; s.visible = true; s.position.set(c.x + pBase[i * 3] * 4, .05 + pVel[i * 3 + 1] * 1.8 * ign, c.z - .6 - pBase[i * 3 + 2] * 6);
      const sc = (.06 + (.5 + .5 * Math.sin(t * 9 + i * 1.7)) * .12) * (1 + ign); s.scale.set(sc, sc, 1); } };
  K.streaks = (t, speed = 1, color = 0xbfd0ff) => { streaks.visible = true; streaks.material.color.set(color); const a = sGeo.attributes.position.array, c = camera.position;
    for (let i = 0; i < NS; i++) { const [u, v, w, z] = sBase[i]; const x = c.x + (u - .5) * 24, zz = c.z - 1 - w * 22; const y = (((v * 10 - t * 6 * speed * (.6 + z)) % 10 + 10) % 10) - 1, len = .25 + z * .35 * speed;
      a.set([x, y, zz, x + len * .45, y + len, zz], i * 6); } sGeo.attributes.position.needsUpdate = true; };

  // glow sprites on people
  const gp = rng(5), pglow = [];
  for (let i = 0; i < 93; i++) { const p = i < 90 ? V(gp() * 50 - 25, 1.0, -2 - gp() * 22) : [V(.4, .6, -1.2), V(1.3, .6, -2.3), V(2.1, .6, -1.4)][i - 90];
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true })); s.position.copy(p); s.visible = false; scene.add(s); pglow.push(s); }
  K.outshine = (g) => { glowGroup.visible = true; GLOWFILL.opacity = .08 + .25 * g; LINE.color.setRGB(1, 1, 1);
    pglow.forEach((s, i) => { s.visible = true; const sc = (1.6 + 4.5 * g) * (1 + (i % 5) * .15); s.scale.set(sc, sc * 1.6, 1); s.material.opacity = .45 + .4 * g; }); };

  // space: Earth (cloud texture), rim, Moon
  const space = new THREE.Group(); scene.add(space);
  const earth = new THREE.Mesh(new THREE.SphereGeometry(1, 96, 64), new THREE.MeshBasicMaterial({ map: cloudTex }));
  const earthRim = new THREE.Mesh(new THREE.SphereGeometry(1.04, 64, 48), new THREE.MeshBasicMaterial({ color: 0x9fb8ff, transparent: true, opacity: .25, side: THREE.BackSide }));
  const moon = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 32), new THREE.MeshLambertMaterial({ map: moonTex }));
  const moonLight = new THREE.DirectionalLight(0xffffff, 0); space.add(earth, earthRim, moon, moonLight);
  K.space = { group: space, earth, earthRim, moon, moonLight };

  // point-cloud copy of the world (for "return", "scan" or "ghost" shots)
  const NC = surfPts.length, cBase = new Float32Array(NC * 3), cDir = new Float32Array(NC * 3), cCol = new Float32Array(NC * 3), cr = rng(123);
  surfPts.forEach((p, i) => { cBase.set([p.x, p.y, p.z], i * 3); const d = V(p.x, p.y + 5, p.z + 20).normalize(); cDir.set([d.x + (cr() - .5), d.y + cr() * .6, d.z + (cr() - .5)], i * 3);
    const b = .55 + cr() * .45; cCol.set([.55 * b, .72 * b, b], i * 3); });
  const cloudPts = new THREE.BufferGeometry(); cloudPts.setAttribute('position', new THREE.BufferAttribute(new Float32Array(NC * 3), 3)); cloudPts.setAttribute('color', new THREE.BufferAttribute(cCol, 3));
  const cloudMesh = new THREE.Points(cloudPts, new THREE.PointsMaterial({ size: 2.2, sizeAttenuation: false, vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
  cloudMesh.frustumCulled = false; scene.add(cloudMesh);
  K.pointCloud = (explode = 0) => { cloudMesh.visible = true; const a = cloudPts.attributes.position.array, e = explode * explode * 140;
    for (let i = 0; i < NC; i++) a.set([cBase[i * 3] + cDir[i * 3] * e, cBase[i * 3 + 1] + cDir[i * 3 + 1] * e, cBase[i * 3 + 2] + cDir[i * 3 + 2] * e], i * 3);
    cloudPts.attributes.position.needsUpdate = true; cloudMesh.material.opacity = 1 - explode * .5; };
  const grad = (stops) => canvasTex(4, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); stops.forEach(([o, c]) => gr.addColorStop(o, c)); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  K.bg = { night: grad([[0, '#000004'], [.44, '#02040f'], [.47, '#0b1a5a'], [1, '#030824']]), blue: grad([[0, '#7fa0e6'], [.6, '#4f7bd8'], [1, '#2f5fc9']]), day: skyDay };

  // ---------- modes and reset ----------
  K.mode = (mode) => {
    const day = mode === 'day', wire = mode === 'wire' || mode === 'glow', world = day || wire;
    dayGroup.visible = groundDay.visible = day; wireGroup.visible = groundWire.visible = wire;
    scene.background = day ? skyDay : new THREE.Color(0x000000); scene.fog = day ? new THREE.Fog(0xd9d3dc, 60, 520) : null;
    stars.visible = wire || mode === 'space'; if (!world) { dayGroup.visible = wireGroup.visible = groundDay.visible = groundWire.visible = false; }
  };
  K.reset = () => {
    points.visible = streaks.visible = false; sparks.forEach(s => s.visible = false); pglow.forEach(s => s.visible = false);
    hands.forEach(h => h.visible = false); space.visible = false; cloudMesh.visible = false; glowGroup.visible = false; GLOWFILL.opacity = 0;
    LINE.color.set(0xdfe8ff); LINE.opacity = .95; camera.fov = 50; camera.updateProjectionMatrix();
  };
  K.look = (pos, tgt) => { camera.position.copy(pos); camera.lookAt(tgt); };
  K.path = (t, a, b, p0, p1, t0, t1) => { const k = easeIO(clamp((t - a) / (b - a))); K.look(p0.clone().lerp(p1, k), t0.clone().lerp(t1, k)); };
  return K;
}
