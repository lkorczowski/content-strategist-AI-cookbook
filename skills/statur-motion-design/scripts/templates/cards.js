/* Card templates: full-screen panel, list card, page capture card, prompt box.
   Cards stay out of the caption zone (props.safe_bottom) so captions keep running under them. */
(function () {
  const {clamp, lerp, prog, spring, env, esc, el, waitImg} = STATUR.util;

  const grid = (T, size = 90, op = 0.35) => `<div style="position:absolute;inset:0;background-image:linear-gradient(${T.line} 1px,transparent 1px),linear-gradient(90deg,${T.line} 1px,transparent 1px);background-size:${size}px ${size}px;opacity:${op}"></div>`;
  const label = (T, txt, size = 28) => `<div class="fm" style="display:flex;align-items:center;gap:16px;font-size:${size}px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:${T.accent}"><span style="width:44px;height:3px;background:${T.accent};display:inline-block"></span>${esc(txt)}</div>`;

  // Opaque full-screen panel that covers the A-roll (B-roll moment). Slides or fades in and out.
  STATUR.register('panel', {
    create(e, root, T, c) {
      const p = Object.assign({grid: true, enter: 'up', exit: 'fade', color: T.ink}, e.props);
      const pan = el('div', '', `position:absolute;left:0;top:0;width:${c.W}px;height:${c.H}px;background:${p.color}`);
      if (p.grid) pan.innerHTML = grid(T);
      root.appendChild(pan);
      return {update(lt, dur) {
        const a = prog(lt, 0, 0.34, 'outQuint'), b = clamp((dur - lt) / 0.16);
        pan.style.transform = p.enter === 'up' ? `translateY(${lerp(100, 0, a)}%)` : p.enter === 'left' ? `translateX(${lerp(-100, 0, a)}%)` : 'none';
        pan.style.opacity = p.enter === 'fade' ? Math.min(a, b) : (p.exit === 'fade' ? b : 1);
      }};
    }
  });

  // List card (schedule, results): label, title, rows that tick in one by one, optional counter.
  STATUR.register('card_list', {
    create(e, root, T, c) {
      const p = Object.assign({x: 70, y: 300, w: 940, row_h: 74, stagger: 0.16, first: 0.35, max_rows: 8, scroll_after: 0}, e.props);
      const box = el('div', '', `position:absolute;left:${p.x}px;top:${p.y}px;width:${p.w}px;background:${T.ink};border:2px solid ${T.line};padding:30px 34px 22px`);
      box.innerHTML = `${label(T, p.label || '')}
        <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:18px">
          <div class="fd" style="font-size:64px;color:${T.paper};line-height:1">${esc(p.title || '')}</div>
          ${p.counter ? `<div class="fm cnt" style="font-size:30px;font-weight:700;color:${T.paper};opacity:.9">${esc(p.counter)}</div>` : ''}
        </div>
        <div class="rows" style="position:relative;margin-top:22px;height:${p.row_h * Math.min(p.max_rows, p.rows.length)}px;overflow:hidden">
          <div class="inner" style="position:absolute;left:0;right:0;top:0"></div></div>`;
      const inner = box.querySelector('.inner');
      const rows = p.rows.map((r, i) => {
        const d = el('div', '', `position:relative;display:flex;align-items:center;gap:22px;height:${p.row_h}px;border-top:1px solid ${T.line}`);
        d.innerHTML = `<span class="fm" style="font-size:28px;font-weight:700;color:${T.accent};width:96px">${esc(r.a)}</span>
          <span class="fm" style="font-size:24px;color:${T.paper};opacity:.7;width:220px;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap">${esc(r.b)}</span>
          <span class="fb" style="font-size:30px;font-weight:700;color:${T.paper};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1">${esc(r.c)}</span>`;
        inner.appendChild(d); return d;
      });
      root.appendChild(box);
      return {update(lt, dur) {
        const a = prog(lt, 0, 0.36, 'outQuint'), out = clamp((dur - lt) / 0.2);
        box.style.opacity = Math.min(clamp(lt / 0.12), out);
        box.style.transform = `translateY(${lerp(80, 0, a)}px) scale(${lerp(0.96, 1, a)})`;
        let shown = 0;
        rows.forEach((d, i) => {
          const t0 = p.first + i * p.stagger, k = prog(lt, t0, 0.22);
          d.style.opacity = k; d.style.transform = `translateX(${lerp(-18, 0, k)}px)`;
          if (lt >= t0) shown = i + 1;
        });
        const over = Math.max(0, shown - p.max_rows);
        const cur = parseFloat(inner.dataset.y || 0), target = -over * p.row_h;
        inner.style.transform = `translateY(${target}px)`; inner.dataset.y = target;
      }};
    }
  });

  // Capture of a page in a frame. view = crop of the image shown at the start, view_to at the end
  // (image pixels), so the camera pans or zooms across the capture. highlights draw an accent box.
  STATUR.register('page_card', {
    create(e, root, T, c) {
      const p = Object.assign({frame: {x: 60, y: 330, w: 960, h: 720}, move: [0.3, 3.0], tilt: 8, url: '', label: ''}, e.props);
      const F = p.frame;
      const wrap = el('div', '', `position:absolute;left:${F.x}px;top:${F.y - 64}px;width:${F.w}px;perspective:1600px`);
      wrap.innerHTML = `<div class="hd" style="display:flex;justify-content:space-between;align-items:center;height:52px;margin-bottom:12px">
          ${label(T, p.label, 26)}<span class="fm" style="font-size:24px;color:${T.paper};opacity:.75">${esc(p.url)}</span></div>
        <div class="fr" style="position:relative;width:${F.w}px;height:${F.h}px;overflow:hidden;border:2px solid ${T.paper};background:#fff;transform-origin:50% 0">
          <img class="im" style="position:absolute;left:0;top:0;transform-origin:0 0" src="${p.img}"></div>`;
      root.appendChild(wrap);
      const fr = wrap.querySelector('.fr'), im = wrap.querySelector('.im'), hd = wrap.querySelector('.hd');
      waitImg(im);
      const hls = (p.highlights || []).map(h => { const d = el('div', '', `position:absolute;border:5px solid ${T.accent};pointer-events:none`); fr.appendChild(d); return {h, d}; });
      const V0 = p.view, V1 = p.view_to || p.view;
      return {update(lt, dur) {
        const a = prog(lt, 0, 0.42, 'outQuint'), out = clamp((dur - lt) / 0.2);
        wrap.style.opacity = Math.min(clamp(lt / 0.1), out);
        fr.style.transform = `rotateX(${lerp(p.tilt, 0, a)}deg) translateY(${lerp(120, 0, a)}px)`;
        hd.style.transform = `translateY(${lerp(40, 0, a)}px)`;
        const k = prog(lt, p.move[0], p.move[1], 'inOutCubic');
        const vx = lerp(V0.x, V1.x, k), vy = lerp(V0.y, V1.y, k), vw = lerp(V0.w, V1.w, k);
        const s = F.w / vw;
        im.style.transform = `scale(${s}) translate(${-vx}px,${-vy}px)`;
        hls.forEach(({h, d}) => {
          const q = prog(lt, h.t, h.dur || 0.35, 'outCubic');
          d.style.left = ((h.x - vx) * s - 8) + 'px'; d.style.top = ((h.y - vy) * s - 6) + 'px';
          d.style.width = Math.max(0, (h.w * s + 16) * q) + 'px'; d.style.height = (h.h * s + 12) + 'px';
          d.style.opacity = q > 0 ? 1 : 0;
        });
      }};
    }
  });

  // Prompt box: a request typed to an AI assistant, then the result lines.
  STATUR.register('prompt_box', {
    create(e, root, T, c) {
      const p = Object.assign({x: 70, y: 330, w: 940, text: '', type_from: 0.3, type_dur: 1.6, enter_at: null, lines: [], line_stagger: 0.32,
                               who: 'You', to: 'Claude'}, e.props);
      const box = el('div', '', `position:absolute;left:${p.x}px;top:${p.y}px;width:${p.w}px`);
      box.innerHTML = `${label(T, `${p.who} to ${p.to}`, 26)}
        <div class="ib" style="margin-top:22px;border:3px solid ${T.paper};background:${T.ink};padding:30px 32px;min-height:150px">
          <div class="fb tx" style="font-size:46px;font-weight:700;color:${T.paper};line-height:1.2"></div></div>
        <div class="ls" style="margin-top:34px"></div>`;
      root.appendChild(box);
      const tx = box.querySelector('.tx'), ib = box.querySelector('.ib'), ls = box.querySelector('.ls');
      const lines = p.lines.map(l => { const d = el('div', '', `display:flex;gap:20px;align-items:baseline;padding:16px 0;border-top:1px solid ${T.line}`,
        `<span class="fm" style="font-size:30px;font-weight:700;color:${T.accent}">[&bull;]</span><span class="fb" style="font-size:38px;font-weight:700;color:${T.paper}">${esc(l)}</span>`); ls.appendChild(d); return d; });
      const enterAt = p.enter_at == null ? p.type_from + p.type_dur + 0.15 : p.enter_at;
      return {update(lt, dur) {
        const a = prog(lt, 0, 0.34, 'outQuint'), out = clamp((dur - lt) / 0.2);
        box.style.opacity = Math.min(clamp(lt / 0.1), out);
        box.style.transform = `translateY(${lerp(60, 0, a)}px)`;
        const n = Math.floor(p.text.length * clamp((lt - p.type_from) / p.type_dur));
        const caret = (lt < enterAt && Math.floor(lt * 2.5) % 2 === 0) || (lt >= p.type_from && lt < p.type_from + p.type_dur);
        tx.innerHTML = esc(p.text.slice(0, n)) + (lt < enterAt ? `<span style="display:inline-block;width:18px;height:44px;background:${T.accent};vertical-align:-6px;margin-left:6px;opacity:${caret ? 1 : 0}"></span>` : '');
        ib.style.borderColor = lt >= enterAt && lt < enterAt + 0.25 ? T.accent : T.paper;
        lines.forEach((d, i) => { const q = prog(lt, enterAt + 0.25 + i * p.line_stagger, 0.25); d.style.opacity = q; d.style.transform = `translateX(${lerp(-20, 0, q)}px)`; });
      }};
    }
  });
})();
