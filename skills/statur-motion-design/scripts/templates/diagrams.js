/* Diagram templates: a curve that draws itself, a loop of steps, a long recording cut into clips.
   Built in SVG and HTML, flat lines, one accent color: data and method made visible. */
(function () {
  const {clamp, lerp, prog, spring, env, esc, rng, el, waitImg} = STATUR.util;
  const label = (T, txt, size = 28) => `<div class="fm" style="display:flex;align-items:center;gap:16px;font-size:${size}px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:${T.accent}"><span style="width:44px;height:3px;background:${T.accent};display:inline-block"></span>${esc(txt)}</div>`;

  // y = f(x) drawn progressively, with labelled markers. f is given as sampled points [[x,y],...] in data units.
  STATUR.register('chart_curve', {
    create(e, root, T, c) {
      const p = Object.assign({x: 90, y: 300, w: 900, h: 640, draw: [0.4, 2.6], xmax: 300, ymax: 1, xticks: [0, 100, 200, 300], yticks: [0, 0.5, 1],
                               xlabel: '', ylabel: '', ytick_fmt: 'pct', markers: []}, e.props);
      const W = p.w, H = p.h, ox = 110, oy = H - 60, pw = W - ox - 30, ph = oy - 40;
      const X = v => ox + pw * v / p.xmax, Y = v => oy - ph * v / p.ymax;
      const d = p.points.map((q, i) => `${i ? 'L' : 'M'}${X(q[0]).toFixed(1)},${Y(q[1]).toFixed(1)}`).join(' ');
      const fmt = v => p.ytick_fmt === 'pct' ? Math.round(v * 100) + '%' : v;
      let svg = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" style="overflow:visible">`;
      p.yticks.forEach(v => { svg += `<line x1="${ox}" x2="${ox + pw}" y1="${Y(v)}" y2="${Y(v)}" stroke="${T.line}" stroke-width="1.5"/><text x="${ox - 18}" y="${Y(v) + 10}" text-anchor="end" font-family="${T.font_mono}" font-size="26" fill="${T.paper}" opacity=".7">${fmt(v)}</text>`; });
      p.xticks.forEach(v => { svg += `<text x="${X(v)}" y="${oy + 44}" text-anchor="middle" font-family="${T.font_mono}" font-size="26" fill="${T.paper}" opacity=".7">${v}</text>`; });
      svg += `<line x1="${ox}" x2="${ox + pw}" y1="${oy}" y2="${oy}" stroke="${T.paper}" stroke-width="2"/><line x1="${ox}" x2="${ox}" y1="${oy}" y2="${oy - ph - 10}" stroke="${T.paper}" stroke-width="2"/>`;
      svg += `<path class="cv" d="${d}" fill="none" stroke="${T.accent}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`;
      p.markers.forEach((m, i) => { svg += `<g class="mk" data-i="${i}" opacity="0"><circle cx="${X(m.x)}" cy="${Y(m.y)}" r="13" fill="${T.ink}" stroke="${T.paper}" stroke-width="4"/>
        <text x="${X(m.x) + (m.dx || 22)}" y="${Y(m.y) + (m.dy || -22)}" text-anchor="${m.anchor || 'start'}" font-family="${T.font_display}" font-weight="900" font-size="40" fill="${T.paper}">${esc(m.text)}</text></g>`; });
      svg += `<text x="${ox + pw}" y="${oy + 92}" text-anchor="end" font-family="${T.font_mono}" font-size="24" fill="${T.paper}" opacity=".7" letter-spacing="2">${esc(p.xlabel.toUpperCase())}</text></svg>`;
      const box = el('div', '', `position:absolute;left:${p.x}px;top:${p.y}px;width:${W}px`);
      box.innerHTML = `${label(T, p.label || '')}<div class="fd" style="font-size:${p.title_size || 70}px;line-height:1;color:${T.paper};margin:18px 0 30px;white-space:nowrap">${esc(p.title || '')}</div>${svg}`;
      root.appendChild(box);
      const cv = box.querySelector('.cv'); const L = cv.getTotalLength();
      cv.style.strokeDasharray = `${L} ${L}`;
      const mks = [...box.querySelectorAll('.mk')];
      return {update(lt, dur) {
        const a = prog(lt, 0, 0.35, 'outQuint'), out = clamp((dur - lt) / 0.2);
        box.style.opacity = Math.min(clamp(lt / 0.1), out); box.style.transform = `translateY(${lerp(50, 0, a)}px)`;
        const k = prog(lt, p.draw[0], p.draw[1], 'inOutCubic');
        cv.style.strokeDashoffset = L * (1 - k);
        mks.forEach((m, i) => { const mk = p.markers[i]; const vis = k * p.xmax >= mk.x; const q = vis ? spring(lt, p.draw[0] + p.draw[1] * Math.pow(mk.x / p.xmax, 0.75), 2.2, 8) : 0;
          m.setAttribute('opacity', vis ? 1 : 0); m.style.transformOrigin = 'center'; });
      }};
    }
  });

  // A loop of steps around a circle; the arc draws, the active node is marked.
  STATUR.register('loop_diagram', {
    create(e, root, T, c) {
      const p = Object.assign({cx: 540, cy: 690, r: 290, nodes: [], active: 0, draw: [0.3, 1.6], here: 'You are here'}, e.props);
      const n = p.nodes.length, S = p.r * 2 + 520, C = S / 2;
      let g = `<svg width="${S}" height="${S}" viewBox="0 0 ${S} ${S}"><circle cx="${C}" cy="${C}" r="${p.r}" fill="none" stroke="${T.line}" stroke-width="3"/>
        <circle class="arc" cx="${C}" cy="${C}" r="${p.r}" fill="none" stroke="${T.accent}" stroke-width="7" transform="rotate(-90 ${C} ${C})"/>`;
      p.nodes.forEach((nd, i) => {
        const a = -Math.PI / 2 + i * 2 * Math.PI / n, x = C + p.r * Math.cos(a), y = C + p.r * Math.sin(a);
        // labels: above the top node, below the others, centered, so nothing leaves the frame
        const above = Math.sin(a) < -0.5;
        const ty = above ? y - 48 : y + 70;
        g += `<g class="nd" opacity="0"><circle cx="${x}" cy="${y}" r="22" fill="${i === p.active ? T.accent : T.ink}" stroke="${T.paper}" stroke-width="4"/>
          <text x="${x}" y="${ty}" text-anchor="middle" font-family="${T.font_display}" font-weight="900" font-size="44" fill="${T.paper}">${esc(nd.text)}</text>
          ${nd.sub ? `<text x="${x}" y="${above ? ty - 50 : ty + 36}" text-anchor="middle" font-family="${T.font_mono}" font-size="21" fill="${T.paper}" opacity=".7">${esc(nd.sub)}</text>` : ''}</g>`;
      });
      g += '</svg>';
      const box = el('div', '', `position:absolute;left:${p.cx - S / 2}px;top:${p.cy - S / 2}px;width:${S}px;height:${S}px`);
      box.innerHTML = g;
      const top = el('div', '', `position:absolute;left:90px;top:${p.label_y || 300}px`, `${label(T, p.label || '')}<div class="fd" style="font-size:66px;color:${T.paper};margin-top:16px;line-height:1.02">${esc(p.title || '')}</div>`);
      root.appendChild(box); root.appendChild(top);
      const arc = box.querySelector('.arc'), L = 2 * Math.PI * p.r; arc.style.strokeDasharray = `${L} ${L}`;
      const nds = [...box.querySelectorAll('.nd')];
      const a0 = -Math.PI / 2 + p.active * 2 * Math.PI / n;
      const here = el('div', 'fm', `position:absolute;left:${p.cx + p.r * Math.cos(a0)}px;top:${p.cy + p.r * Math.sin(a0) + 40}px;transform:translateX(-50%);
        background:${T.accent};color:${T.paper};font-size:24px;font-weight:700;letter-spacing:.1em;padding:8px 14px;text-transform:uppercase;white-space:nowrap`, esc(p.here));
      root.appendChild(here);
      return {update(lt, dur) {
        const a = prog(lt, 0, 0.35, 'outQuint'), out = clamp((dur - lt) / 0.2);
        root.style.opacity = Math.min(clamp(lt / 0.1), out);
        box.style.transform = `scale(${lerp(0.9, 1, a)})`; top.style.transform = `translateY(${lerp(30, 0, a)}px)`;
        const k = prog(lt, p.draw[0], p.draw[1], 'inOutCubic'); arc.style.strokeDashoffset = L * (1 - k);
        nds.forEach((nd, i) => nd.setAttribute('opacity', k * n >= i - 0.02 ? 1 : 0));
        const q = spring(lt, p.draw[0] + 0.2, 2.2, 8); here.style.opacity = lt > p.draw[0] + 0.2 ? 1 : 0;
        here.style.transform = `translateX(-50%) scale(${lerp(0.6, 1, Math.min(1.05, q))})`;
      }};
    }
  });

  // A long recording as a bar with a waveform; a playhead scans it, cuts appear, clips fly into a grid.
  STATUR.register('timeline_cut', {
    create(e, root, T, c) {
      const p = Object.assign({y: 300, bar: {x: 80, y: 430, w: 920, h: 96}, scan: [0.3, 1.5], cuts: [], posters: [], grid: {x: 120, y: 590, cols: 3, w: 250, gap: 30, rows_gap: 26},
                               fly: 2.0, fly_stagger: 0.12, title: '', label: '', result: ''}, e.props);
      const B = p.bar, r = rng(11);
      let bars = ''; const nb = 150;
      for (let i = 0; i < nb; i++) { const hh = 10 + r() * (B.h - 20) * (0.45 + 0.55 * Math.abs(Math.sin(i / 7))); bars += `<rect x="${(i + 0.2) * B.w / nb}" y="${(B.h - hh) / 2}" width="${0.6 * B.w / nb}" height="${hh}" fill="${T.paper}" opacity=".55"/>`; }
      const head = el('div', '', `position:absolute;left:90px;top:${p.y}px`, `${label(T, p.label)}<div class="fd" style="font-size:64px;color:${T.paper};margin-top:14px">${esc(p.title)}</div>`);
      const bar = el('div', '', `position:absolute;left:${B.x}px;top:${B.y}px;width:${B.w}px;height:${B.h}px;border:2px solid ${T.line}`);
      bar.innerHTML = `<svg width="${B.w}" height="${B.h}" style="position:absolute;left:0;top:0">${bars}</svg>`;
      const ph = el('div', '', `position:absolute;top:-14px;width:4px;height:${B.h + 28}px;background:${T.accent}`); bar.appendChild(ph);
      const cuts = p.cuts.map(cu => { const d = el('div', '', `position:absolute;top:0;height:${B.h}px;left:${cu.s * B.w}px;width:${Math.max(4, (cu.e - cu.s) * B.w)}px;background:${T.accent};opacity:0`); bar.appendChild(d); return d; });
      const G = p.grid; const gh = G.w * 16 / 9;
      const posters = p.posters.map((src, i) => { const im = el('img', '', `position:absolute;left:0;top:0;width:${G.w}px;height:${gh}px;object-fit:cover;border:3px solid ${T.paper};transform-origin:0 0`); im.src = src; waitImg(im); root.appendChild(im); return im; });
      const res = el('div', 'fm', `position:absolute;left:${B.x}px;top:${p.result_y || (B.y + B.h + 22)}px;font-size:30px;font-weight:700;color:${T.accent};letter-spacing:.1em;text-transform:uppercase`, esc(p.result));
      root.appendChild(head); root.appendChild(bar); root.appendChild(res);
      return {update(lt, dur) {
        const a = prog(lt, 0, 0.35, 'outQuint'), out = clamp((dur - lt) / 0.2);
        root.style.opacity = Math.min(clamp(lt / 0.1), out);
        head.style.transform = `translateY(${lerp(30, 0, a)}px)`; bar.style.transform = `translateY(${lerp(40, 0, a)}px)`;
        const k = prog(lt, p.scan[0], p.scan[1], 'inOutCubic'); ph.style.left = (k * B.w - 2) + 'px';
        cuts.forEach((d, i) => { const t0 = p.scan[0] + p.scan[1] * p.cuts[i].s; d.style.opacity = lt >= t0 ? 0.95 : 0; });
        posters.forEach((im, i) => {
          const col = i % G.cols, row = Math.floor(i / G.cols);
          const tx = G.x + col * (G.w + G.gap), ty = G.y + row * (gh + G.rows_gap);
          const cu = p.cuts[i] || {s: i / posters.length, e: i / posters.length + 0.02};
          const sx = B.x + cu.s * B.w, sy = B.y;
          const q = prog(lt, p.fly + i * p.fly_stagger, 0.5, 'outQuint');
          const sc = lerp(0.12, 1, q);
          im.style.opacity = lt >= p.fly + i * p.fly_stagger ? 1 : 0;
          im.style.transform = `translate(${lerp(sx, tx, q)}px,${lerp(sy, ty, q)}px) scale(${sc})`;
        });
        res.style.opacity = prog(lt, p.fly + posters.length * p.fly_stagger + 0.3, 0.3);
      }};
    }
  });
})();
