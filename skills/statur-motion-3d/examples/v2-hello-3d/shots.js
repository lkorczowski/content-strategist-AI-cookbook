// Minimal v2 3D example: host character on a sunny plaza with a walking crowd and shadows.
import * as L from '../lib3d.js';
export default async function (C) {
  const { THREE, scene, camera } = C; const V = L.V; const R = L.rng(1);
  scene.background = L.gradTex([[0, '#7fb2e6'], [1, '#f4e6cf']]); scene.add(new THREE.HemisphereLight(0xfff4e0, 0x9a8a70, 1.3));
  const sun = new THREE.DirectionalLight(0xffefd6, 2.4); sun.position.set(-25, 45, 30); sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024); Object.assign(sun.shadow.camera, { left: -30, right: 30, top: 30, bottom: -30 }); scene.add(sun);
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(200, 200).rotateX(-Math.PI / 2), new THREE.MeshLambertMaterial({ color: 0xece5d6 })); ground.receiveShadow = true; scene.add(ground);
  const host = L.host(1.25); scene.add(host); const crowd = [];
  for (let i = 0; i < 20; i++) { const p = L.person(R); p.position.set(-14 + R() * 28, 0, -2 - R() * 14); p.userData.x0 = p.position.x; p.rotation.y = Math.PI / 2; scene.add(p); crowd.push(p); }
  scene.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  return [
    { from: 0, to: 6, run: (t) => { L.hostPose(host, t, t < 2.4 ? 'present' : 'talk'); crowd.forEach(p => { p.position.x = p.userData.x0 + t * 1.3; L.pose(p, t, 'walk'); }); L.camPath(camera, t, 0, 6, V(0, 2.2, 10), V(1, 2.4, 7), V(0, 2.2, 0), V(0, 2.4, 0), .03); } },
    { from: 6, to: 1e9, run: () => { C.hud = false; } },
  ];
}
