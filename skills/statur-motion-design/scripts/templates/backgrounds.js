/* Background templates (opaque, for the "bg" layer that replaces the room behind the speaker).
   poster_wall: columns of the account's own posters scrolling slowly, toned down so the speaker stays first.
   ink_grid: flat brand background with a visible grid and marginalia. */
(function () {
  const {clamp, lerp, prog, env, esc, el, waitImg} = STATUR.util;

  STATUR.register('poster_wall', {
    create(e, root, T, c) {
      const p = Object.assign({cols: 3, gap: 22, speed: [40, -55, 35], dim: 0.62, tilt: 0, scale: 1.12}, e.props);
      const wrap = el('div', '', `position:absolute;inset:0;background:${T.ink};overflow:hidden`);
      const inner = el('div', '', `position:absolute;left:50%;top:50%;width:${c.W * p.scale}px;height:${c.H * p.scale}px;transform:translate(-50%,-50%) rotate(${p.tilt}deg);display:flex;gap:${p.gap}px`);
      wrap.appendChild(inner);
      const colW = (c.W * p.scale - p.gap * (p.cols - 1)) / p.cols, ph = colW * 16 / 9;
      const cols = [];
      for (let k = 0; k < p.cols; k++) {
        const col = el('div', '', `position:relative;width:${colW}px;height:100%`);
        const strip = el('div', '', `position:absolute;left:0;top:0;width:100%`);
        const imgs = p.images.slice(k).concat(p.images.slice(0, k));
        const seq = imgs.concat(imgs, imgs);
        seq.forEach(src => { const im = el('img', '', `display:block;width:${colW}px;height:${ph}px;object-fit:cover;margin-bottom:${p.gap}px`); im.src = src; waitImg(im); strip.appendChild(im); });
        col.appendChild(strip); inner.appendChild(col); cols.push({strip, cycle: imgs.length * (ph + p.gap), v: p.speed[k % p.speed.length], off: (k * 0.37 % 1)});
      }
      wrap.appendChild(el('div', '', `position:absolute;inset:0;background:${T.ink};opacity:${p.dim}`));
      wrap.appendChild(el('div', '', `position:absolute;inset:0;background-image:linear-gradient(${T.line} 1px,transparent 1px),linear-gradient(90deg,${T.line} 1px,transparent 1px);background-size:90px 90px;opacity:.25`));
      root.appendChild(wrap);
      return {update(lt) {
        cols.forEach(o => { const y = ((o.off * o.cycle + lt * o.v) % o.cycle + o.cycle) % o.cycle; o.strip.style.transform = `translateY(${-y}px)`; });
      }};
    }
  });

  STATUR.register('ink_grid', {
    create(e, root, T, c) {
      const p = Object.assign({grid: 90, marks: [], drift: 12}, e.props);
      const wrap = el('div', '', `position:absolute;inset:0;background:${T.ink};overflow:hidden`);
      const g = el('div', '', `position:absolute;left:-${p.grid}px;top:-${p.grid}px;right:-${p.grid}px;bottom:-${p.grid}px;background-image:linear-gradient(${T.line} 1px,transparent 1px),linear-gradient(90deg,${T.line} 1px,transparent 1px);background-size:${p.grid}px ${p.grid}px;opacity:.45`);
      wrap.appendChild(g);
      (p.marks || []).forEach(m => wrap.appendChild(el('div', 'fm', `position:absolute;left:${m.x}px;top:${m.y}px;font-size:${m.size || 24}px;color:${m.accent ? T.accent : T.paper};opacity:${m.accent ? 1 : 0.5};letter-spacing:.12em;text-transform:uppercase;white-space:nowrap`, esc(m.text))));
      root.appendChild(wrap);
      return {update(lt) { g.style.transform = `translate(${(lt * p.drift) % p.grid}px,${(lt * p.drift * 0.6) % p.grid}px)`; }};
    }
  });
})();
