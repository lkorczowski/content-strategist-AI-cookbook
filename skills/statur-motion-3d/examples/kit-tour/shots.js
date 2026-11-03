// Shot list of the "park to space" arc: hook in daylight, an event that redraws the world as wireframe,
// consequences at body, place, planet and Moon scale, a return, a loop card.
// Each shot: { from, to, run(t, k) } where k is 0..1 inside the shot. K = kit (kit.js), O = overlay, S = scenario.
// To make a new video: keep the kit, rewrite this list (cameras, modes, effects) to match the new captions.
export default function makeShots(K, O, S) {
  const { V, path, look, mode } = { V: (x, y, z) => new K.THREE.Vector3(x, y, z), path: K.path, look: K.look, mode: K.mode };
  const ss = (a, b, x) => { const k = Math.min(1, Math.max(0, (x - a) / (b - a))); return k * k * (3 - 2 * k); };
  const EV = S.event_time ?? 8.2, BACK = S.return_time ?? 63.2;
  return [
    { from: 0, to: EV, run: (t) => { mode('day'); path(t, 0, EV, V(-.2, 1.25, 5.2), V(.1, 1.3, 3.4), V(0, 9, -80), V(.5, 8, -80)); } },
    { from: EV, to: 12.6, run: (t) => { mode('wire'); path(t, EV, 12.6, V(.1, 1.3, 3.4), V(.3, 2.0, 1.5), V(.5, 8, -80), V(0, 10, -80));
        const k = Math.min(1, (t - EV) / 3.2); if (k < 1) { const fx = O.fx, x = 760 - 380 * k, y = 330; const gr = fx.createLinearGradient(x - 260, y, x + 40, y); gr.addColorStop(0, 'rgba(160,190,255,0)'); gr.addColorStop(1, 'rgba(225,235,255,.95)'); fx.fillStyle = gr; fx.fillRect(x - 260, y - 9, 300, 18);
          const g2 = fx.createRadialGradient(x + 40, y, 0, x + 40, y, 120); g2.addColorStop(0, '#fff'); g2.addColorStop(1, 'rgba(255,255,255,0)'); fx.fillStyle = g2; fx.fillRect(x - 100, y - 140, 280, 280); } } },
    { from: 12.6, to: 15.6, run: (t) => { mode('wire'); path(t, 12.6, 15.6, V(-3, 1.6, 0), V(-1, 1.1, -6), V(0, 4, -60), V(2, 3, -60)); K.streaks(t, 1); } },
    { from: 15.6, to: 20.3, run: (t, k) => { mode('wire'); path(t, 15.6, 20.3, V(-6, 1.3, 3), V(-6, 1.3, 2.8), V(-5.6, -.2, -2.5), V(-5.6, .3, -2.6)); K.hands(ss(0, 1, k), 0); K.dust(t, 1); } },
    { from: 20.3, to: 24.2, run: (t) => { mode('wire'); path(t, 20.3, 24.2, V(-1.9, 1.15, -2.9), V(-1.6, 1.2, -3.3), V(-1.2, 1.25, -6), V(-1.1, 1.3, -6)); K.dust(t, .7); } },
    { from: 24.2, to: 28.2, run: (t) => { mode('wire'); path(t, 24.2, 28.2, V(-6, 1.6, 2.5), V(-3, 1.8, 2.2), V(0, 5, -60), V(3, 5, -60)); K.dust(t, .7); } },
    { from: 28.2, to: 32.3, run: (t, k) => { mode('wire'); path(t, 28.2, 32.3, V(0, .9, 0), V(0, .7, -.6), V(0, 0, -4), V(0, .1, -4)); K.mat.LINE.opacity = .4; K.sand(t, ss(0, 1, k)); } },
    { from: 32.3, to: 36.3, run: (t, k) => { mode('glow'); path(t, 32.3, 36.3, V(-4, 1.3, 1.5), V(-4, 1.3, 1.3), V(-2, .9, -6), V(-2, 1.0, -6)); K.hands(0, .55 + .35 * ss(0, 1, k)); K.sand(t, 1); K.streaks(t, 1.6); } },
    { from: 36.3, to: 40.6, run: (t, k) => { mode('glow'); path(t, 36.3, 40.6, V(-2, 1.5, 3), V(-1, 1.7, 1.5), V(0, 8, -60), V(0, 8, -60)); K.outshine(ss(0, 1, k)); K.sand(t, 1); O.white(ss(39.4, 40.6, t) * .8); } },
    { from: 40.6, to: 44.2, run: (t) => { mode('space'); look(V(0, 1, 0), V(0, 1, -1)); const sp = K.space; sp.group.visible = true; sp.earth.scale.setScalar(1); sp.earth.position.set(0, 0, -1.2); sp.earthRim.visible = false; sp.moon.visible = false; O.white(1 - ss(42.2, 44.2, t) * .9); } },
    { from: 44.2, to: 48.2, run: (t, k) => { mode('space'); const sp = K.space; sp.group.visible = true; sp.earthRim.visible = true; sp.moon.visible = false; sp.earth.position.set(0, 0, 0); sp.earth.scale.setScalar(1); sp.earth.rotation.set(.2, t * .06, 0);
        look(V(0, 0, 1.35 + .7 * ss(0, 1, k)), V(0, 0, 0)); O.vignette(.9); } },
    { from: 48.2, to: 52.2, run: (t, k) => { mode('space'); const sp = K.space; sp.group.visible = true; sp.earthRim.visible = false; sp.moon.visible = true; sp.earth.position.set(0, 0, -260); sp.earth.scale.setScalar(200);
        sp.moon.position.set(0, -.3, -8); sp.moon.scale.setScalar(.38 + k * .05); sp.moonLight.intensity = 0; sp.moon.material.color.set(0x1d2236); look(V(0, -.6, 0), V(0, -.3, -10)); } },
    { from: 52.2, to: 55.2, run: (t) => { mode('space'); const sp = K.space; sp.group.visible = true; sp.earthRim.visible = false; sp.moon.visible = true; sp.earth.position.set(0, -101.2, -6); sp.earth.scale.setScalar(100); sp.earth.rotation.set(t * .01, 0, 0);
        sp.moon.position.set(0, 4.2, -30); sp.moon.scale.setScalar(1.6); sp.moonLight.intensity = 1.4; sp.moonLight.position.set(0, -1, 1); sp.moon.material.color.set(0xffffff); look(V(0, 0, 0), V(0, 1.2, -10)); } },
    { from: 55.2, to: BACK, run: (t, k) => { mode('space'); const sp = K.space; sp.group.visible = true; sp.earthRim.visible = false; sp.moon.visible = false; sp.earth.position.set(0, -101.2 + k * .25, -6); sp.earth.scale.setScalar(100); sp.earth.rotation.set(k * .06, 0, 0);
        look(V(0, 0, 0), V(0, 1.6 + .6 * k, -10)); } },
    { from: BACK, to: 68, run: (t) => { mode('none'); K.scene.background = K.bg.night; path(t, BACK, 68, V(0, 1.7, 9), V(0, 1.8, 5), V(0, 7, -80), V(0, 7, -80)); K.pointCloud(0); } },
    { from: 68, to: 72.2, run: (t, k) => { mode('none'); const e = ss(0, 1, k); K.scene.background = e > .25 ? K.bg.blue : K.bg.night; path(t, 68, 72.2, V(0, 1.8, 5), V(0, 2.2, 4), V(0, 7, -80), V(0, 11, -80));
        K.pointCloud(e); O.white(Math.max(0, .55 - Math.abs(e - .45) * 1.6)); if (e > .25) K.streaks(t, 3, 0xe6efff); } },
    { from: 72.2, to: 1e9, run: () => { mode('none'); O.hideHud(); } },
  ];
}
