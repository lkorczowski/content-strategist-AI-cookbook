// Example spec: one figure per playbook of statur.co, each drawing the idea of its page.
// Render: node scripts/render.mjs examples/handbook-figures.mjs out/
// Rule: one accent element per figure, the thing to remember.

const W = 640, H = 360;
const mk = (codex, o, seed) => new codex.Sketch({ width: W, height: H, seed: o.seed ?? seed, style: o.style, paper: o.paper });

export const figures = {
  // Korczowski scale: six medallions, the profile fills with stipple as the name carries.
  'personal-brand-scale'(codex, o) { const s = mk(codex, o, 11);
    const names = ['no time', '300-view jail', 'pays in DMs', 'face of the industry', 'generational', 'legend'];
    for (let i = 0; i < 6; i++) { const cx = 58 + i * 105; codex.medallion(s, cx, 150, 46, i);
      s.label(cx, 226, 'Type ' + i, { size: 16, anchor: 'middle', font: 'serif', italic: true, color: s.st.ink });
      s.label(cx, i % 2 ? 284 : 254, names[i], { size: 17, anchor: 'middle' }); }
    s.ellipse(268, 196, 124, 200, { accent: true, width: 2.2, roughness: 1.8, shadow: false });
    s.label(268, 336, 'the climb that changes a company', { size: 20, anchor: 'middle', accent: true });
    return s; },

  // Scale Meta ads: three organic winners feed one purchase campaign.
  'meta-ads-scaling'(codex, o) { const s = mk(codex, o, 23);
    s.label(60, 38, 'organic winners', { size: 24 });
    for (let i = 0; i < 3; i++) { const x = 60 + i * 120, y = 54;
      s.rect(x, y, 74, 122, { fill: 'hachure', gap: 7, angle: -50 + i * 20, hatch: true });
      s.polygon([[x + 28, y + 46], [x + 28, y + 76], [x + 52, y + 61]], { fill: 'solid', fillColor: '#E2DED3', shadow: false });
      s.line(x + 37, y + 132, 300, 246, { width: 1 }); }
    s.fluo(222, 276, 418, 276, 50);
    s.rect(214, 250, 212, 54, { width: 1.7, hatch: true });
    s.label(320, 284, 'one purchase campaign', { size: 18, anchor: 'middle', font: 'serif', italic: true, color: s.st.ink });
    s.arrow(430, 277, 524, 277, { width: 1.3 });
    s.label(532, 284, 'buyers', { size: 24 });
    s.label(452, 118, 'creators paid', { size: 22 }); s.label(452, 142, 'on results', { size: 22 });
    return s; },

  // Content Testing Loop: read the curve at day 7, the next video learns from it.
  'content-testing-loop'(codex, o) { const s = mk(codex, o, 37);
    s.line(60, 300, 600, 300, { width: 1 }); s.line(60, 300, 60, 40, { width: 1 });
    const pts = [[70, 80], [140, 170], [210, 214], [280, 236], [350, 248], [420, 255], [490, 258]];
    const yAt = (x) => { for (let k = 0; k < pts.length - 1; k++) if (x >= pts[k][0] && x <= pts[k + 1][0]) { const t = (x - pts[k][0]) / (pts[k + 1][0] - pts[k][0]); return pts[k][1] + t * (pts[k + 1][1] - pts[k][1]); } return 999; };
    s.stipple((x, y) => y > yAt(x) + 3 && y < 298, [70, 80, 490, 298], 2600, { density: (x, y) => .08 + (y - yAt(x)) / 200 });
    s.curve(pts, { width: 1.7, shadow: true });
    pts.forEach(([x, y], i) => { s.circle(x, y, 9, { fill: 'solid', roughness: .6, shadow: false }); s.label(x, 326, 'd' + (i + 1), { size: 20, anchor: 'middle' }); });
    s.circle(490, 258, 46, { accent: true, width: 2.2, roughness: 1.6, shadow: false });
    s.label(468, 212, 'read it here', { size: 26, anchor: 'end', accent: true });
    s.curve([[490, 258], [540, 150], [592, 118]], { width: 1.2, dash: [6, 6] });
    s.label(600, 102, 'next video', { size: 24, anchor: 'end' });
    return s; },

  // Creative-Led Growth: the loop idea, video, data, next idea. Data is where it is decided.
  'creative-led-growth'(codex, o) { const s = mk(codex, o, 41);
    const cx = 320, cy = 178, R = 118;
    s.circle(cx, cy, R * 2, { width: 1.5, stipple: 1700, hatch: { len: [7, 16] } });
    const st = [['idea', -90], ['video', 0], ['data', 90], ['next idea', 180]];
    st.forEach(([l, a]) => { const r = a * Math.PI / 180, x = cx + Math.cos(r) * R, y = cy + Math.sin(r) * R, acc = l === 'data';
      s.circle(x, y, acc ? 28 : 20, acc ? { fill: 'solid', accent: true, roughness: .8 } : { fill: 'solid', fillColor: '#E2DED3' });
      s.label(cx + Math.cos(r) * (R + (a === 180 ? 78 : 58)), cy + Math.sin(r) * (R + 40) + 8, l, { size: acc ? 30 : 26, anchor: 'middle', accent: acc });
      const a2 = (a + 42) * Math.PI / 180, ax = cx + Math.cos(a2) * R, ay = cy + Math.sin(a2) * R, tg = a2 + Math.PI / 2;
      s.line(ax, ay, ax - Math.cos(tg - .5) * 14, ay - Math.sin(tg - .5) * 14); s.line(ax, ay, ax - Math.cos(tg + .5) * 14, ay - Math.sin(tg + .5) * 14); });
    s.label(cx, cy + 8, 'one hour a day', { size: 21, anchor: 'middle', font: 'serif', italic: true, color: s.st.ink });
    return s; },

  // X Ghostwriter: brand DNA, one strand for the voice, one for the drafts, one rung checked.
  'x-ghostwriter'(codex, o) { const s = mk(codex, o, 53);
    const A = [], B = []; for (let i = 0; i <= 24; i++) { const x = 60 + i * 22; A.push([x, 180 + Math.sin(i * .5) * 82]); B.push([x, 180 - Math.sin(i * .5) * 82]); }
    s.stipple((x, y) => Math.abs(y - 180) < Math.abs(Math.sin((x - 60) / 22 * .5)) * 76, [60, 96, 590, 266], 1500);
    s.curve(A, { width: 2, shadow: true }); s.curve(B, { width: 1.2, dash: [7, 5] });
    for (let i = 1; i < 24; i += 2) s.line(A[i][0], A[i][1], B[i][0], B[i][1], i === 13 ? { accent: true, width: 2.6 } : { width: 1 });
    s.label(60, 50, 'your voice', { size: 24 }); s.label(60, 334, 'AI drafts', { size: 24 });
    s.line(A[13][0], 92, A[13][0] + 30, 60, { accent: true, width: 1.2 });
    s.label(A[13][0] + 36, 46, 'checked against', { size: 22, accent: true }); s.label(A[13][0] + 36, 68, 'your brand DNA', { size: 22, accent: true });
    return s; },

  // X launch playbook: the launch-day spike is bought, day two is what still works.
  'x-launch'(codex, o) { const s = mk(codex, o, 61);
    s.line(40, 300, 610, 300, { width: 1 });
    const pts = [[40, 282], [150, 276], [230, 262], [280, 70], [320, 236], [400, 248], [490, 244], [600, 238]];
    s.stipple((x, y) => { if (x < 230 || x > 320) return false; const top = x < 280 ? 262 - (x - 230) * 3.84 : 70 + (x - 280) * 4.15; return y > top && y < 298; }, [230, 70, 320, 298], 1500);
    s.polyline(pts, { width: 1.8, shadow: true });
    s.circle(280, 70, 12, { fill: 'solid', roughness: .6, shadow: false });
    s.label(298, 64, 'day 1: bought reach', { size: 22 });
    s.fluo(344, 244, 600, 238, 26);
    s.label(470, 212, 'day 2: what still works', { size: 24, anchor: 'middle', accent: true });
    s.line(280, 84, 280, 300, { width: .8, dash: [4, 6] });
    s.label(280, 328, 'launch', { size: 20, anchor: 'middle' });
    return s; },

  // Clipping: one long video cut into vertical clips, the clip worth posting circled.
  'clipping'(codex, o) { const s = mk(codex, o, 71);
    s.label(40, 42, 'one long video', { size: 24 });
    s.rect(40, 58, 560, 72, { width: 1.4, stipple: 2200, hatch: true });
    for (let i = 0; i < 14; i++) { s.rect(50 + i * 39, 64, 8, 7, { width: .7, roughness: .6, shadow: false }); s.rect(50 + i * 39, 117, 8, 7, { width: .7, roughness: .6, shadow: false }); }
    [150, 300, 450].forEach(x => s.line(x, 48, x, 142, { dash: [5, 5], width: 1.2 }));
    for (let i = 0; i < 4; i++) { const x = 70 + i * 140, y = 176; s.rect(x, y, 60, 104, { fill: 'hachure', gap: 6, angle: 40 + i * 25, hatch: true }); s.line(x + 30, 146, x + 30, y - 4, { width: .9 }); }
    s.ellipse(380, 228, 100, 152, { accent: true, width: 2.2, roughness: 1.7, shadow: false });
    s.label(450, 330, 'the clip worth posting', { size: 24, anchor: 'middle', accent: true });
    return s; },

  // How ideas go viral: one idea, waves through the network.
  'ideas-go-viral'(codex, o) { const s = mk(codex, o, 83);
    const src = [180, 190]; s.ripples(src[0], src[1], 6, 23);
    for (let i = 0; i < 22; i++) { const x = 60 + s.rnd() * 540, y = 40 + s.rnd() * 290, d = Math.hypot(x - src[0], y - src[1]);
      if (d < 260) s.line(src[0] + (x - src[0]) * .15, src[1] + (y - src[1]) * .15, x, y, { width: .7, roughness: 1.4 });
      s.circle(x, y, d < 230 ? 14 : 9, d < 230 ? { stipple: 70, hatch: { len: [3, 6], gap: 4 } } : { fill: 'solid', fillColor: '#E2DED3' }); }
    s.circle(src[0], src[1], 28, { fill: 'solid', accent: true, hatch: true });
    s.line(src[0] - 16, src[1] - 18, 74, 46, { accent: true, width: 1.2 });
    s.label(40, 38, 'one idea', { size: 26, accent: true });
    s.label(610, 40, 'the meme war, mapped', { size: 18, anchor: 'end' });
    return s; },

  // Home: attention compounds, the gap between now and six months later keeps widening.
  'moat'(codex, o) { const s = new codex.Sketch({ width: 1000, height: 380, seed: o.seed ?? 97, style: o.style, paper: o.paper });
    s.line(60, 330, 960, 330, { width: 1 }); s.line(60, 330, 60, 40, { width: 1 });
    const now = [], late = []; for (let m = 0; m <= 12; m++) { const x = 60 + m * 72; now.push([x, 330 - Math.pow(m / 12, 1.7) * 270]); late.push([x, m < 6 ? 330 : 330 - Math.pow((m - 6) / 12, 1.7) * 270]); }
    s.polygon(now.concat(late.slice().reverse()), { fill: 'hachure', gap: 9, angle: -35, color: 'transparent', fillColor: s.st.ink, shadow: true });
    s.curve(now, { width: 2, shadow: true }); s.curve(late, { width: 1.4, dash: [8, 6] });
    for (let m = 0; m <= 12; m += 3) s.label(60 + m * 72, 364, 'month ' + m, { size: 26, anchor: 'middle' });
    s.fluo(924, now[12][1] + 4, 924, late[12][1] - 4, 26);
    s.label(900, 74, 'start now', { size: 34, anchor: 'end', color: s.st.ink });
    s.label(905, late[12][1] + 40, 'start in six months', { size: 26, anchor: 'end' });
    s.label(520, 150, 'the gap keeps widening', { size: 38, anchor: 'middle', accent: true }); s.arrow(640, 160, 860, 196, { accent: true, width: 1.3 });
    return s; },
};
