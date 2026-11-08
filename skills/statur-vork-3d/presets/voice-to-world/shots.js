// "Voice to world": one speaker in a sea of people, rings that reach no one, then one listener, then a network
// that compounds over a real-geography dot globe, one teal opportunity that travels back, and an Earth that
// spins faster and faster after the speaker's light goes out. Deterministic: everything is a function of t.
import * as L from '../lib3d.js';
export default async function (C) {
  const { THREE, scene, camera, ss, clamp, lerp } = C; const V = L.V; const R = L.rng(11);
  const D = await (await fetch(new URL('data.json', import.meta.url))).json();
  const RG = 3000, TOP = V(0, RG, 0);
  const PAPER = new THREE.Color(0xf2efe8), TEAL = new THREE.Color(0x5fe3c8), SIG = new THREE.Color(0xe8501c);
  scene.background = new THREE.Color(0x050506); camera.fov = 48;
  const world = new THREE.Group(); scene.add(world);           // everything that spins with the Earth
  const NORTH = V(...D.north).normalize();

  // ---------- lights ----------
  scene.add(new THREE.HemisphereLight(0x9aa6c0, 0x0a0a0c, .35));
  const key = new THREE.SpotLight(0xffe2c4, 140, 60, .5, .6, 1.6); key.position.set(3, RG + 14, 6); key.target.position.copy(TOP); scene.add(key, key.target);
  const fill = new THREE.PointLight(0xc8d4ff, 40, 40, 1.2); scene.add(fill);

  // ---------- globe ----------
  const sphere = new THREE.Mesh(new THREE.SphereGeometry(RG - 1.2, 192, 128), new THREE.MeshLambertMaterial({ color: 0x0c0d10 }));
  world.add(sphere);
  const atm = new THREE.Sprite(new THREE.SpriteMaterial({ map: L.tex(512, 512, (g, w) => { const gr = g.createRadialGradient(w / 2, w / 2, 0, w / 2, w / 2, w / 2); gr.addColorStop(0, 'rgba(95,227,200,0)'); gr.addColorStop(.79, 'rgba(95,227,200,0)'); gr.addColorStop(.825, 'rgba(95,227,200,.5)'); gr.addColorStop(.88, 'rgba(95,227,200,.12)'); gr.addColorStop(1, 'rgba(95,227,200,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, w); }), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0 }));
  atm.scale.setScalar(RG * 2.5); scene.add(atm);
  // ground disk under the crowd, radial fade so the edge never shows
  const groundTex = L.tex(256, 256, (g, w, h) => { const gr = g.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2); gr.addColorStop(0, 'rgba(34,34,36,1)'); gr.addColorStop(.6, 'rgba(20,20,22,1)'); gr.addColorStop(1, 'rgba(12,13,16,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  const ground = new THREE.Mesh(new THREE.CircleGeometry(90, 64).rotateX(-Math.PI / 2), new THREE.MeshLambertMaterial({ map: groundTex, transparent: true, depthWrite: false }));
  ground.position.copy(TOP); ground.position.y -= .01; world.add(ground);

  // ---------- shader helpers: points and lines that switch on at their own time ----------
  const ptsMat = (size, extra = '') => new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 }, uA: { value: 1 }, uS: { value: size } }, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    vertexShader: `attribute float aT; attribute vec3 aC; attribute vec3 aC0; uniform float uT; uniform float uS; varying vec3 vC; varying float vA;
      void main(){ float on = step(aT, uT); float age = uT - aT; vC = mix(aC0, aC, on); vA = mix(.55, 1., on);
        float pop = on * (1. + 1.6*exp(-age*4.)); vec4 mv = modelViewMatrix*vec4(position,1.); gl_Position = projectionMatrix*mv; gl_PointSize = uS*mix(.8,1.,on)*pop; ${extra} }`,
    fragmentShader: `uniform float uA; varying vec3 vC; varying float vA; void main(){ vec2 q = gl_PointCoord-.5; float r = length(q); if(r>.5) discard; float a = smoothstep(.5,.0,r); gl_FragColor = vec4(vC*a*vA*uA, 1.); }` });
  const lineMat = () => new THREE.ShaderMaterial({
    uniforms: { uT: { value: 0 }, uA: { value: 1 } }, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    vertexShader: 'attribute float aT; attribute vec3 aC; varying float vT; varying vec3 vC; void main(){ vT = aT; vC = aC; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: 'uniform float uT; uniform float uA; varying float vT; varying vec3 vC; void main(){ if(uT < vT) discard; float head = exp(-(uT-vT)*2.5); gl_FragColor = vec4(vC*(.45 + 1.4*head)*uA, 1.); }' });
  function points(pos, tOn, col, col0, mat) {
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('aT', new THREE.Float32BufferAttribute(tOn, 1)); g.setAttribute('aC', new THREE.Float32BufferAttribute(col, 3)); g.setAttribute('aC0', new THREE.Float32BufferAttribute(col0, 3));
    const p = new THREE.Points(g, mat); p.frustumCulled = false; return p;
  }
  // polylines: list of {pts:[Vector3...], t0, t1, c:Color}; aT grows along the polyline from t0 to t1
  function lines(list) {
    const pos = [], at = [], col = [];
    for (const l of list) { const n = l.pts.length - 1; for (let i = 0; i < n; i++) { for (const j of [i, i + 1]) { const p = l.pts[j]; pos.push(p.x, p.y, p.z); at.push(lerp(l.t0, l.t1, j / n)); col.push(l.c.r, l.c.g, l.c.b); } } }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('aT', new THREE.Float32BufferAttribute(at, 1)); g.setAttribute('aC', new THREE.Float32BufferAttribute(col, 3));
    const m = new THREE.LineSegments(g, lineMat()); m.frustumCulled = false; return m;
  }
  const arc = (a, b, lift, n = 28) => { const out = []; const om = a.angleTo(b); for (let i = 0; i <= n; i++) { const k = i / n; const v = new THREE.Vector3().copy(a).normalize().lerp(b.clone().normalize(), k).normalize(); // nlerp is fine for om < pi
      out.push(v.multiplyScalar(RG * (1 + lift * Math.sin(Math.PI * k) * om))); } return out; };

  // ---------- the speaker (host mascot) and the crowd ----------
  const host = L.host(1.25); host.position.copy(TOP); world.add(host);
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: L.tex(64, 64, (g, w) => { const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.3, 'rgba(255,255,255,.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, w); }), color: 0xffd8b0, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }));
  world.add(halo);
  const HEAD = TOP.clone().add(V(0, 2.1, 0));
  const crowdPos = []; // static crowd baked into one vertex-colored mesh (people on their phones)
  const geos = [];
  for (let i = 0; i < 520; i++) {
    const r = 2.6 + Math.sqrt(R()) * 26, a = R() * Math.PI * 2; const x = Math.cos(a) * r, z = Math.sin(a) * r;
    if (Math.abs(x) < 3 && z > 0 && z < 14) continue; // keep a clear line between camera and speaker
    crowdPos.push(V(x, 0, z));
    const p = L.person(R, { phone: true }); L.pose(p, R() * 10, 'phone'); p.position.set(x, RG, z); p.rotation.y = R() * Math.PI * 2; p.updateMatrixWorld(true);
    p.traverse(o => { if (!o.isMesh) return; const g = o.geometry.clone().toNonIndexed(); g.applyMatrix4(o.matrixWorld); const c = o.material.color; const n = g.attributes.position.count; const ca = new Float32Array(n * 3); for (let k = 0; k < n; k++) { ca[k * 3] = c.r; ca[k * 3 + 1] = c.g; ca[k * 3 + 2] = c.b; } g.setAttribute('color', new THREE.BufferAttribute(ca, 3)); for (const key of Object.keys(g.attributes)) if (!['position', 'normal', 'color'].includes(key)) g.deleteAttribute(key); geos.push(g); });
  }
  const crowd = new THREE.Mesh(L.mergeAll(geos), new THREE.MeshLambertMaterial({ vertexColors: true })); world.add(crowd);
  // the listeners: live people who turn to the speaker when the voice reaches them
  const LIST = [[8.3, V(2.2, 0, -3.2)], [10.8, V(-4.8, 0, -2.6)], [11.9, V(4.6, 0, 2.2)]];
  for (let i = 0; i < 14; i++) { const a = R() * Math.PI * 2, r = 6 + R() * 16; LIST.push([12.3 + i * .07, V(Math.cos(a) * r, 0, Math.sin(a) * r)]); }
  const listeners = LIST.map(([t0, p]) => { const m = L.person(R, { phone: true }); m.position.copy(TOP).add(p); m.userData.t0 = t0; m.userData.face = Math.atan2(-p.x, -p.z); m.userData.away = R() * 6.28; const h = new THREE.Sprite(halo.material.clone()); h.material.color.set(0xf2efe8); world.add(h); m.userData.h = h; world.add(m); return m; });
  const listenLines = lines(LIST.map(([t0, p]) => ({ pts: [HEAD, TOP.clone().add(p).add(V(0, 1.75, 0))], t0: t0 - .25, t1: t0, c: PAPER }))); world.add(listenLines);
  // voice rings
  const rings = []; for (let i = 0; i < 8; i++) { const m = new THREE.Mesh(new THREE.RingGeometry(.96, 1, 96).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ color: 0xf2efe8, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide })); world.add(m); rings.push(m); }

  // ---------- network on the cap, land dots, global arcs ----------
  const NP = D.nodes.map(v => v * (RG + 1.5));
  const nV = i => V(NP[i * 3], NP[i * 3 + 1], NP[i * 3 + 2]);
  const tNode = D.d.map(d => 12.6 + 6.0 * Math.log(d / 0.004) / Math.log(0.42 / 0.004) + (R() - .5) * .25);
  const nCol = [], nCol0 = []; D.d.forEach(() => { nCol.push(.95, .93, .9); nCol0.push(0, 0, 0); });
  const nodePts = points(NP, tNode, nCol, nCol0, ptsMat(2.3)); world.add(nodePts);
  const netLines = lines(D.parent.map((p, i) => p < 0 ? null : { pts: [nV(p), nV(i)], t0: tNode[p], t1: Math.max(tNode[p] + .05, tNode[i]), c: new THREE.Color(.55, .55, .55) }).filter(Boolean)); world.add(netLines);
  // opportunity chain: node lights teal at 19.0, the light travels back to the speaker by 22.5
  const chain = D.chain.map(nV); chain.push(HEAD.clone());
  const trail = []; const tTrail = [], cT = [], c0 = [];
  for (let s = 0; s < chain.length - 1; s++) for (let k = 0; k < 12; k++) { const p = chain[s].clone().lerp(chain[s + 1], k / 12); trail.push(p.x, p.y + 2, p.z); tTrail.push(19.4 + 3.1 * (s + k / 12) / (chain.length - 1)); cT.push(TEAL.r, TEAL.g, TEAL.b); c0.push(0, 0, 0); }
  const trailPts = points(trail, tTrail, cT, c0, ptsMat(5)); world.add(trailPts);
  const oppSprite = new THREE.Sprite(halo.material.clone()); oppSprite.material.color = TEAL.clone(); world.add(oppSprite);
  const pulse = new THREE.Sprite(halo.material.clone()); pulse.material.color = TEAL.clone(); world.add(pulse);
  // land dots light up from the speaker outwards between 24.0 and 30.5
  const LP = D.land.map(v => v * (RG + 2)); const tLand = D.land_ang.map(a => 24.0 + 6.5 * a / Math.PI + (R() - .5) * .3);
  const lCol = [], lCol0 = []; D.land_ang.forEach(() => { lCol.push(.95, .93, .88); lCol0.push(.16, .16, .17); });
  const landMat = ptsMat(2.4); const landPts = points(LP, tLand, lCol, lCol0, landMat); world.add(landPts);
  const gArcs = lines(D.arcs.map(([a, b]) => { const A = V(...a), B = V(...b); const t0 = 24.0 + 6.0 * A.angleTo(B) / Math.PI * .5 + R() * 1.5; return { pts: arc(A, B, .22), t0, t1: t0 + 1.4, c: R() < .06 ? TEAL : PAPER }; })); world.add(gArcs);

  // stars on a shell that follows the camera
  const stars = L.stars(3000, 1, 5); stars.renderOrder = -1; if (stars.material) { stars.material.depthTest = false; stars.material.depthWrite = false; stars.material.sizeAttenuation = false; stars.material.size = 1.6; } scene.add(stars);

  // ---------- camera keys: [t, target, direction, distance] ----------
  const K = [
    [0, V(0, RG + .6, 0), V(.12, .36, 1), 12], [7.6, V(0, RG + .6, 0), V(.45, .45, 1), 14.5],
    [13.2, V(0, RG + .5, 0), V(.35, .9, .8), 46], [18.8, V(0, RG, 0), V(.25, 1, .55), 1700],
    [22.6, V(0, RG, 0), V(.18, 1, .5), 2300], [30.8, V(0, 0, 0), V(.18, .82, .62), 15800], [41, V(0, 0, 0), V(.18, .82, .62), 15800]];
  function cam(t) {
    let i = 0; while (i < K.length - 2 && t > K[i + 1][0]) i++;
    const [ta, A, dA, la] = K[i], [tb, B, dB, lb] = K[i + 1]; const k = L.easeIO(clamp((t - ta) / (tb - ta)));
    const tgt = A.clone().lerp(B, k), dir = dA.clone().normalize().lerp(dB.clone().normalize(), k).normalize(), dist = Math.exp(lerp(Math.log(la), Math.log(lb), k));
    const shake = dist < 60 ? .04 * dist / 10 : 0; const pos = tgt.clone().add(dir.multiplyScalar(dist)); pos.x += Math.sin(t * 1.9) * shake; pos.y += Math.sin(t * 1.3 + 1) * shake * .6;
    camera.position.copy(pos); camera.lookAt(tgt); camera.near = Math.max(.05, dist * .02); camera.far = dist * 2.2 + RG * 2.5; camera.updateProjectionMatrix();
    stars.position.copy(camera.position); stars.scale.setScalar(camera.far * .9);
    fill.position.copy(pos); return dist;
  }

  const run = (t) => {
    const dist = cam(t);
    // Earth spin: accelerates after 30.8 around the real axis
    const u = Math.max(0, t - 30.8); const ang = .02 * u + .09 * u * u * u;
    world.quaternion.setFromAxisAngle(NORTH, ang);
    // speaker
    L.hostPose(host, t, t < 8 ? 'talk' : t < 13.2 ? 'present' : 'talk'); host.rotation.y = Math.sin(t * .4) * .25;
    const glow = 1 + 2.5 * Math.exp(-Math.max(0, t - 22.5) * 1.2) * (t > 22.5 ? 1 : 0);
    const fade = 1 - ss(33.0, 35.0, t); // the speaker's light goes out; the network stays
    halo.position.copy(HEAD); halo.scale.setScalar(Math.max(2.2, dist * .03) * glow); halo.material.opacity = (t < 13 ? .12 : lerp(.12, .6, ss(13, 18, t))) * fade;
    halo.material.color.copy(t > 22.5 ? new THREE.Color(0xffd8b0).lerp(TEAL, Math.exp(-(t - 22.5) * .6)) : new THREE.Color(0xffd8b0));
    host.visible = dist < 400; crowd.visible = dist < 600; ground.material.opacity = 1 - ss(200, 600, dist);
    // rings: every 1.3 s; before 8 s they fade out short, after 8 s they travel further
    rings.forEach((m, i) => { const per = 1.3, age = ((t - i * per) % (per * 8) + per * 8) % (per * 8); const reach = t < 8 ? 9 : 16; const r = .4 + age * 5.5; m.position.copy(TOP).add(V(0, 1.7, 0)); m.scale.setScalar(r); m.material.opacity = t < 13.6 && r < reach ? (1 - r / reach) * .35 : 0; });
    // listeners: phone down, turn, look up, a light on their head
    listeners.forEach((m) => { const t0 = m.userData.t0; const on = ss(t0, t0 + .6, t); m.rotation.y = lerp(m.userData.away, m.userData.face, on); L.pose(m, t, on > .5 ? (t < t0 + 1.4 ? 'cheer' : 'look_up') : 'phone'); m.visible = dist < 600; const h = m.userData.h; h.position.copy(m.position).add(V(0, 2.0, 0)); const big = m.userData.t0 < 12; h.scale.setScalar(big ? 2.8 : 1.6); h.material.opacity = on * (big ? .9 : .5) * (1 - ss(60, 300, dist)); });
    listenLines.material.uniforms.uT.value = t; listenLines.material.uniforms.uA.value = 1 - ss(200, 900, dist);
    // network
    nodePts.material.uniforms.uT.value = t; netLines.material.uniforms.uT.value = t; netLines.material.uniforms.uA.value = .32 * ss(40, 300, dist) * (1 - .5 * ss(8000, 14000, dist));
    nodePts.material.uniforms.uA.value = ss(25, 200, dist) * (1 - .6 * ss(8000, 14000, dist));
    // opportunity
    const opp = chain[0]; oppSprite.position.copy(opp).multiplyScalar(1.001); const ob = ss(19.0, 19.3, t) * (1 - ss(29, 31, t)); oppSprite.scale.setScalar(dist * .07 * (1 + .25 * Math.sin(t * 6))); oppSprite.material.opacity = ob;
    trailPts.material.uniforms.uT.value = t; trailPts.material.uniforms.uA.value = 1 - ss(27, 31, t);
    const tk = clamp((t - 19.4) / 3.1) * (chain.length - 1); const si = Math.min(chain.length - 2, Math.floor(tk)); pulse.position.copy(chain[si]).lerp(chain[si + 1], tk - si); pulse.position.y += 2;
    pulse.scale.setScalar(dist * .05); pulse.material.opacity = t > 19.4 && t < 22.6 ? 1 : 0;
    // globe
    landMat.uniforms.uT.value = t; landMat.uniforms.uA.value = ss(900, 4000, dist); landMat.uniforms.uS.value = lerp(3.4, 2.2, ss(3000, 14000, dist));
    gArcs.material.uniforms.uT.value = t; gArcs.material.uniforms.uA.value = .45;
    atm.material.opacity = ss(5000, 12000, dist) * .35;
    C.hud = t < 37;
  };
  return [{ from: 0, to: 1e9, run }];
}
