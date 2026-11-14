// codex.mjs : hand-drawn "notebook codex" diagrams as plain SVG strings.
// Works in Node (no DOM) and in the browser. Strokes come from rough.js (MIT, Preet Shihn).
// Look: iron-gall ink, trembling lines, a diffuse shadow around each drawn object,
// contour hatching on the shadow side, stipple shading, handwritten labels,
// one accent element and an optional fluo highlighter stroke.
//
//   import { Sketch } from './codex.mjs';
//   const s = new Sketch({ width: 640, height: 360, seed: 7 });
//   s.circle(320, 180, 200, { shadow: true, hatch: true });
//   s.label(320, 330, 'one idea', { accent: true, anchor: 'middle' });
//   const svg = s.toSVG();

import roughDefault from 'roughjs';

export const DEFAULT_STYLE = {
  ink: '#2A1F17',          // iron-gall ink, brown-black
  ink2: '#4B3527',         // aged ink for labels and secondary strokes
  accent: '#E8501C',       // the one element to remember
  fluo: 'rgba(255,138,76,.72)', // highlighter, multiplied on paper
  shadow: '#4B3527',       // tint of the diffuse shadow
  shadowOpacity: 0.26,     // near shadow
  shadowFar: 0.10,         // sfumato, far shadow
  paper: '#E9E4D8',        // used only when paper: true
  hand: "'Reenie Beanie', 'Bradley Hand', 'Segoe Print', cursive",
  serif: "Newsreader, 'Iowan Old Style', Georgia, serif",
  roughness: 1.3,
  bowing: 1.2,
  strokeWidth: 1.3,
  handScale: 1.4,         // handwriting fonts read small: hand labels are scaled up
  light: [-1, -1],         // light comes from the top left: shadow falls bottom right
  hatchAngle: 45,          // degrees; 45 = strokes falling to the right, the left-handed hatching of the codex
};

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const f = (n) => Math.round(n * 10) / 10;

// --- geometry helpers ---------------------------------------------------
export function flattenPath(d, step = 6) {
  // absolute M L H V C Q Z only; returns array of polygons
  const toks = d.match(/[MLHVCQZmlhvcqz]|-?\d*\.?\d+(?:e-?\d+)?/g) || [];
  const polys = []; let cur = [], x = 0, y = 0, i = 0, cmd = 'M';
  const num = () => parseFloat(toks[i++]);
  while (i < toks.length) {
    if (/[A-Za-z]/.test(toks[i])) cmd = toks[i++];
    const C = cmd.toUpperCase(), rel = cmd !== C;
    if (C === 'Z') { if (cur.length) polys.push(cur); cur = []; continue; }
    if (C === 'M') { if (cur.length) polys.push(cur); let nx = num(), ny = num(); if (rel) { nx += x; ny += y; } x = nx; y = ny; cur = [[x, y]]; cmd = rel ? 'l' : 'L'; continue; }
    if (C === 'L') { let nx = num(), ny = num(); if (rel) { nx += x; ny += y; } x = nx; y = ny; cur.push([x, y]); continue; }
    if (C === 'H') { let nx = num(); if (rel) nx += x; x = nx; cur.push([x, y]); continue; }
    if (C === 'V') { let ny = num(); if (rel) ny += y; y = ny; cur.push([x, y]); continue; }
    if (C === 'C' || C === 'Q') {
      const n = C === 'C' ? 3 : 2; const p = [[x, y]];
      for (let k = 0; k < n; k++) { let px = num(), py = num(); if (rel) { px += x; py += y; } p.push([px, py]); }
      const len = Math.hypot(p[n][0] - x, p[n][1] - y) + 1, steps = Math.max(4, Math.ceil(len / step));
      for (let s = 1; s <= steps; s++) { const t = s / steps, u = 1 - t; let qx, qy;
        if (n === 3) { qx = u*u*u*p[0][0] + 3*u*u*t*p[1][0] + 3*u*t*t*p[2][0] + t*t*t*p[3][0]; qy = u*u*u*p[0][1] + 3*u*u*t*p[1][1] + 3*u*t*t*p[2][1] + t*t*t*p[3][1]; }
        else { qx = u*u*p[0][0] + 2*u*t*p[1][0] + t*t*p[2][0]; qy = u*u*p[0][1] + 2*u*t*p[1][1] + t*t*p[2][1]; }
        cur.push([qx, qy]); }
      x = p[n][0]; y = p[n][1]; continue;
    }
    i++; // unsupported token: skip
  }
  if (cur.length) polys.push(cur);
  return polys;
}
export function insidePoly(poly, x, y) { let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j];
    if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) inside = !inside; }
  return inside; }
const circlePoly = (cx, cy, rx, ry, n = 72) => Array.from({ length: n }, (_, k) => { const a = k / n * Math.PI * 2; return [cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]; });

// --- the sketch -------------------------------------------------------
export class Sketch {
  constructor({ width = 640, height = 360, seed = 1, style = {}, paper = false, rough = roughDefault } = {}) {
    this.w = width; this.h = height; this.st = Object.assign({}, DEFAULT_STYLE, style);
    this.paper = paper; this.seed = seed >>> 0 || 1; this.gen = rough.generator();
    this.shadowLayer = []; this.drawLayer = []; this.fluoLayer = []; this.textLayer = [];
    this.id = 'cx' + (this.seed % 100000);
  }
  rnd() { this.seed = (this.seed * 16807) % 2147483647; return this.seed / 2147483647; }
  opt(o = {}) { const st = this.st;
    const stroke = o.accent ? st.accent : (o.color || st.ink);
    return { stroke, strokeWidth: o.width ?? st.strokeWidth, roughness: o.roughness ?? st.roughness, bowing: o.bowing ?? st.bowing,
      seed: Math.floor(this.rnd() * 1e6) + 1, fill: o.fill === 'solid' ? (o.accent ? st.accent : (o.fillColor || st.ink)) : (o.fill ? (o.fillColor || stroke) : undefined),
      fillStyle: o.fill === 'solid' ? 'solid' : (o.fill || 'hachure'), hachureGap: o.gap ?? 6, fillWeight: o.fillWeight ?? .6, hachureAngle: o.angle ?? -41,
      strokeLineDash: o.dash, disableMultiStroke: o.single || false }; }
  push(drawable) { for (const p of this.gen.toPaths(drawable)) this.drawLayer.push(`<path d="${p.d.replace(/(\d+\.\d)\d+/g, '$1')}" stroke="${p.stroke}" stroke-width="${p.strokeWidth}" fill="${p.fill || 'none'}"${p.fill && p.fill !== 'none' && drawable.options.fillStyle === 'solid' ? '' : ''}${drawable.options.strokeLineDash ? ` stroke-dasharray="${drawable.options.strokeLineDash.join(' ')}"` : ''} stroke-linecap="round" stroke-linejoin="round"/>`); return this; }
  shadowOf(svgShape) { this.shadowLayer.push(svgShape); }

  // contour hatching on the shadow side of a closed polygon
  hatchContour(poly, { len = [6, 14], gap = 5, offset = 3, color, side = 'shadow' } = {}) {
    const [lx, ly] = this.st.light, ang = this.st.hatchAngle * Math.PI / 180;
    const dx = Math.cos(ang), dy = Math.sin(ang);
    // centroid for outward normal
    const cx = poly.reduce((a, p) => a + p[0], 0) / poly.length, cy = poly.reduce((a, p) => a + p[1], 0) / poly.length;
    let acc = 0;
    for (let i = 0; i < poly.length; i++) {
      const a = poly[i], b = poly[(i + 1) % poly.length]; const seg = Math.hypot(b[0] - a[0], b[1] - a[1]); acc += seg;
      if (acc < gap) continue; acc = 0;
      let nx = a[0] - cx, ny = a[1] - cy; const nl = Math.hypot(nx, ny) || 1; nx /= nl; ny /= nl;
      const facing = -(nx * lx + ny * ly) / Math.hypot(lx, ly); // 1 = facing away from light
      if (side === 'shadow' && facing < .25) continue;
      const L = len[0] + (len[1] - len[0]) * Math.min(1, facing) * (.6 + this.rnd() * .5);
      const sx = a[0] + nx * offset, sy = a[1] + ny * offset;
      this.push(this.gen.line(sx, sy, sx + dx * L, sy + dy * L, this.opt({ width: .7, roughness: .6, color: color || this.st.ink2, single: true })));
    }
    return this;
  }
  // stipple a region: test(x,y) -> bool, density(x,y) -> 0..1
  stipple(test, bbox, n = 800, { r = .9, density, accent = false, color } = {}) {
    // dots are zero-length round-capped strokes, in three sizes: about 10 bytes per dot
    const [x0, y0, x1, y1] = bbox, col = accent ? this.st.accent : (color || this.st.ink); const b = [[], [], []];
    for (let i = 0; i < n; i++) { const x = x0 + this.rnd() * (x1 - x0), y = y0 + this.rnd() * (y1 - y0);
      if (!test(x, y)) continue; if (density && this.rnd() > density(x, y)) continue;
      b[Math.floor(this.rnd() * 3)].push(`M${f(x)} ${f(y)}h0`); }
    b.forEach((d, k) => { if (d.length) this.drawLayer.push(`<path d="${d.join('')}" stroke="${col}" stroke-width="${(r * 2 * (.65 + k * .3)).toFixed(2)}" stroke-linecap="round"/>`); });
    return this;
  }
  // light-side density helper: darker away from the light, inside a shape's bbox
  shade(bbox, strength = .7, floor = .12) { const [x0, y0, x1, y1] = bbox, [lx, ly] = this.st.light;
    return (x, y) => { const u = (x - x0) / (x1 - x0 || 1) - .5, v = (y - y0) / (y1 - y0 || 1) - .5; const d = -(u * lx + v * ly) / Math.hypot(lx, ly); return Math.max(0, Math.min(1, floor + strength * (d + .5))); }; }

  // --- primitives (all accept: shadow, hatch, stipple, accent, fill, dash, width) ---
  _decorate(poly, bbox, o) {
    if (o.shadow !== false) this.shadowOf(`<polygon points="${poly.map(p => f(p[0]) + ',' + f(p[1])).join(' ')}"/>`);
    if (o.hatch) this.hatchContour(poly, typeof o.hatch === 'object' ? o.hatch : {});
    if (o.stipple) { const n = typeof o.stipple === 'number' ? o.stipple : 900; this.stipple((x, y) => insidePoly(poly, x, y), bbox, n, { density: this.shade(bbox), accent: o.accent && o.stippleAccent }); }
  }
  circle(cx, cy, d, o = {}) { const r = d / 2; this._decorate(circlePoly(cx, cy, r, r), [cx - r, cy - r, cx + r, cy + r], o); return this.push(this.gen.circle(cx, cy, d, this.opt(o))); }
  ellipse(cx, cy, w, h, o = {}) { this._decorate(circlePoly(cx, cy, w / 2, h / 2), [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], o); return this.push(this.gen.ellipse(cx, cy, w, h, this.opt(o))); }
  rect(x, y, w, h, o = {}) { const poly = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]; this._decorate(poly, [x, y, x + w, y + h], o); return this.push(this.gen.rectangle(x, y, w, h, this.opt(o))); }
  polygon(pts, o = {}) { const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]); this._decorate(pts, [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)], o); return this.push(this.gen.polygon(pts, this.opt(o))); }
  path(d, o = {}) { const polys = flattenPath(d); const all = polys.flat(); const xs = all.map(p => p[0]), ys = all.map(p => p[1]);
    if (o.closed !== false) polys.forEach(poly => this._decorate(poly, [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)], Object.assign({}, o, { stipple: false })));
    if (o.stipple) { const n = typeof o.stipple === 'number' ? o.stipple : 900, bb = [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
      this.stipple((x, y) => polys.some(p => insidePoly(p, x, y)), bb, n, { density: o.density || this.shade(bb) }); }
    return this.push(this.gen.path(d, this.opt(o))); }
  line(x1, y1, x2, y2, o = {}) { if (o.shadow) this.shadowOf(`<line x1="${f(x1)}" y1="${f(y1)}" x2="${f(x2)}" y2="${f(y2)}" stroke-width="9" stroke-linecap="round"/>`); return this.push(this.gen.line(x1, y1, x2, y2, this.opt(o))); }
  curve(pts, o = {}) { if (o.shadow) this.shadowOf(`<polyline points="${pts.map(p => f(p[0]) + ',' + f(p[1])).join(' ')}" fill="none" stroke-width="10" stroke-linejoin="round"/>`); return this.push(this.gen.curve(pts, this.opt(o))); }
  polyline(pts, o = {}) { if (o.shadow) this.shadowOf(`<polyline points="${pts.map(p => f(p[0]) + ',' + f(p[1])).join(' ')}" fill="none" stroke-width="10"/>`); return this.push(this.gen.linearPath(pts, this.opt(o))); }
  arrow(x1, y1, x2, y2, o = {}) { this.line(x1, y1, x2, y2, o); const a = Math.atan2(y2 - y1, x2 - x1), L = o.head || 13;
    this.line(x2, y2, x2 - Math.cos(a - .45) * L, y2 - Math.sin(a - .45) * L, o); return this.line(x2, y2, x2 - Math.cos(a + .45) * L, y2 - Math.sin(a + .45) * L, o); }
  rays(cx, cy, r1, r2, n = 40, o = {}) { for (let k = 0; k < n; k++) { const a = k / n * Math.PI * 2 + this.rnd() * .08, rr = r2 * (.75 + this.rnd() * .3);
      this.push(this.gen.line(cx + Math.cos(a) * r1, cy + Math.sin(a) * r1, cx + Math.cos(a) * rr, cy + Math.sin(a) * rr, this.opt({ width: .6, roughness: .5, single: true, color: this.st.ink2, ...o }))); } return this; }
  ripples(cx, cy, n, step, o = {}) { for (let i = 1; i <= n; i++) this.push(this.gen.circle(cx, cy, i * step * 2, this.opt({ width: .8, roughness: .9, color: i % 2 ? this.st.ink : this.st.ink2, ...o }))); return this; }
  fluo(x1, y1, x2, y2, width = 18) { const mx = (x1 + x2) / 2 + (this.rnd() - .5) * 4, my = (y1 + y2) / 2 + (this.rnd() - .5) * 4;
    this.fluoLayer.push(`<path d="M${f(x1)} ${f(y1)} Q${f(mx)} ${f(my)} ${f(x2)} ${f(y2)}" stroke="${this.st.fluo}" stroke-width="${width}" stroke-linecap="round" fill="none"/>`); return this; }
  label(x, y, text, { size = 22, anchor = 'start', accent = false, color, font = 'hand', italic = false, mirror = false, opacity } = {}) {
    const fam = font === 'hand' ? this.st.hand : this.st.serif, col = accent ? this.st.accent : (color || this.st.ink2);
    if (font === 'hand') size = Math.round(size * this.st.handScale);
    const weight = font === 'hand' ? ` stroke="${col}" stroke-width="${(size / 60).toFixed(2)}" paint-order="stroke"` : '';
    const tr = mirror ? ` transform="translate(${f(x * 2)} 0) scale(-1 1)"` : '';
    this.textLayer.push(`<text x="${f(x)}" y="${f(y)}" font-family="${esc(fam)}" font-size="${size}" fill="${col}" text-anchor="${anchor}"${weight}${italic ? ' font-style="italic"' : ''}${opacity ? ` opacity="${opacity}"` : ''}${tr}>${esc(text)}</text>`); return this; }
  note(x, y, text, o = {}) { return this.label(x, y, text, Object.assign({ mirror: true, opacity: .45, size: 20 }, o)); }

  toSVG({ title = '', idSuffix = '', fontCSS = '' } = {}) {
    const st = this.st, id = this.id + idSuffix;
    const paper = this.paper ? `<rect width="100%" height="100%" fill="${st.paper}"/>` +
      Array.from({ length: 5 }, () => `<ellipse cx="${f(this.rnd() * this.w)}" cy="${f(this.rnd() * this.h)}" rx="${f(60 + this.rnd() * 180)}" ry="${f(40 + this.rnd() * 120)}" fill="${st.shadow}" opacity="${(.025 + this.rnd() * .04).toFixed(3)}" filter="url(#${id}-soft)"/>`).join('') : '';
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${this.w} ${this.h}" role="img"${title ? ` aria-label="${esc(title)}"` : ''}>
<defs>${fontCSS ? `<style>${fontCSS}</style>` : ''}
<filter id="${id}-near" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="${id}-far" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="${id}-soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>
</defs>
${paper}<g fill="${st.shadow}" stroke="${st.shadow}" opacity="${st.shadowFar}" filter="url(#${id}-far)" transform="translate(4 7)">${this.shadowLayer.join('')}</g>
<g fill="${st.shadow}" stroke="${st.shadow}" opacity="${st.shadowOpacity}" filter="url(#${id}-near)" transform="translate(2 3)">${this.shadowLayer.join('')}</g>
<g style="mix-blend-mode:multiply">${this.fluoLayer.join('')}</g>
<g fill="none">${this.drawLayer.join('')}</g>
<g>${this.textLayer.join('')}</g>
</svg>`;
  }
}

// --- reusable figures ---------------------------------------------------
// Profile of a head (facing right) in a 200 x 240 box, for medallions and busts.
export const PROFILE = 'M60,236 L62,182 C38,150 36,64 96,40 C132,26 152,46 154,72 L151,96 L167,119 L156,125 L158,133 L153,137 L156,143 L151,148 C155,160 147,171 132,173 C125,182 128,205 131,236 Z';

export function medallion(s, cx, cy, R, level = 3, { accent = false } = {}) {
  s.circle(cx, cy, R * 2, { width: 1.2, hatch: { len: [4, 9], gap: 6 } });
  if (level >= 4) s.circle(cx, cy, R * 2 - 10, { width: .8, roughness: 1, shadow: false });
  const sc = R * 1.5 / 240, ox = cx - 100 * sc - R * .05, oy = cy - 132 * sc;
  // transform the profile into place
  const pts = flattenPath(PROFILE)[0].map(([x, y]) => [ox + x * sc, oy + y * sc]);
  const d = 'M' + pts.map(p => f(p[0]) + ' ' + f(p[1])).join(' L') + ' Z';
  if (level === 0) { s.path(d, { dash: [3, 5], width: 1.1, roughness: .8, shadow: false }); return s; }
  const n = [0, 500, 1300, 2600, 4200, 6200][Math.min(5, level)] * (R / 44) ** 2;
  s.path(d, { width: level > 2 ? 1.2 : .9, roughness: .9, stipple: Math.round(n), accent });
  if (level >= 3) for (let k = 0; k < 9 + level * 3; k++) { const a = s.rnd() * Math.PI * .95 + Math.PI * 1.02, rr = (52 + s.rnd() * 18) * sc;
    s.circle(ox + 98 * sc + Math.cos(a) * rr * .9, oy + 92 * sc + Math.sin(a) * rr, (9 + s.rnd() * 8) * sc * 2, { width: .8, roughness: 1.6, shadow: false }); }
  return s;
}
