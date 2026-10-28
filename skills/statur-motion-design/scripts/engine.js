/* STATUR motion engine: deterministic HTML/CSS motion graphics, one frame per seek(t).
   No CSS transition or animation is used: every template computes its look from the time it is given,
   so frame N always renders the same picture and a renderer can capture any frame in any order.
   A template registers create(el, root, T, ctx) and returns {update(lt, dur, t)}, where lt is the time
   since the element starts, dur its length, t the timeline time. Times are seconds. */
(function () {
  const S = {templates: {}, els: [], T: {}, W: 1080, H: 1920, pending: []};
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, k) => a + (b - a) * k;
  const ease = {
    linear: k => k,
    inCubic: k => k * k * k,
    outCubic: k => 1 - Math.pow(1 - k, 3),
    outQuint: k => 1 - Math.pow(1 - k, 5),
    inOutCubic: k => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2),
    outExpo: k => (k >= 1 ? 1 : 1 - Math.pow(2, -10 * k)),
    outBack: k => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2); },
  };
  // progress of a move that starts at t0 and lasts d, eased
  const prog = (lt, t0, d, e = 'outCubic') => ease[e](clamp((lt - t0) / Math.max(d, 1e-6)));
  // damped spring from 0 to 1 starting at t0 (overshoots once, settles)
  const spring = (lt, t0, f = 2.0, z = 6.5) => { const x = lt - t0; if (x <= 0) return 0; return 1 - Math.exp(-z * x) * Math.cos(2 * Math.PI * f * x); };
  // visibility envelope: 0 before, 1 inside, fades in over a and out over b at the end of dur
  const env = (lt, dur, a = 0.2, b = 0.2) => Math.min(clamp(lt / Math.max(a, 1e-6)), clamp((dur - lt) / Math.max(b, 1e-6)));
  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const rng = seed => { let s = (seed >>> 0) || 1; return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; };
  const el = (tag, cls, css, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (css) e.style.cssText = css; if (html != null) e.innerHTML = html; return e; };
  const waitImg = img => { if (img.complete && img.naturalWidth) return; S.pending.push(img.decode ? img.decode().catch(() => {}) : new Promise(r => { img.onload = img.onerror = r; })); };

  window.STATUR = {
    register(name, tpl) { S.templates[name] = tpl; },
    util: {clamp, lerp, ease, prog, spring, env, esc, rng, el, waitImg},
    get T() { return S.T; },
    get W() { return S.W; },
    get H() { return S.H; },
  };

  function fontFaces(fonts) {
    return (fonts || []).map(f => `@font-face{font-family:'${f.family}';src:url('${f.src}');font-weight:${f.weight || 400};font-style:${f.style || 'normal'};font-display:block}`).join('\n');
  }

  window.init = async function (tl) {
    S.W = tl.w || 1080; S.H = tl.h || 1920; S.T = Object.assign({}, tl.tokens || {});
    const T = S.T;
    const st = document.getElementById('stage');
    st.style.width = S.W + 'px'; st.style.height = S.H + 'px';
    if (tl.opaque) st.style.background = T.ink || '#000';
    const css = document.createElement('style');
    css.textContent = fontFaces(tl.fonts) + `
      :root{--ink:${T.ink};--paper:${T.paper};--accent:${T.accent};--muted:${T.muted};--line:${T.line}}
      .fd{font-family:'${T.font_display}',sans-serif;font-weight:${T.weight_display || 900}}
      .fb{font-family:'${T.font_body}',sans-serif}
      .fm{font-family:'${T.font_mono}',monospace}
      .fs{font-family:'${T.font_serif}',serif;font-style:italic}`;
    document.head.appendChild(css);
    S.els = [];
    for (const e of tl.elements) {
      const tpl = S.templates[e.type];
      if (!tpl) throw new Error('unknown template ' + e.type);
      const root = el('div', 'el el-' + e.type, `position:absolute;left:0;top:0;width:${S.W}px;height:${S.H}px;display:none;z-index:${e.z || 0}`);
      st.appendChild(root);
      const inst = tpl.create(e, root, T, {W: S.W, H: S.H, tl});
      S.els.push({e, root, inst});
    }
    await document.fonts.ready;
    if (S.pending.length) { await Promise.all(S.pending); S.pending = []; }
    return S.els.length;
  };

  // elements visible at time t (start <= t < end)
  window.activeAt = function (t) {
    return S.els.filter(x => t >= x.e.start && t < x.e.end).map(x => x.e.id);
  };

  window.seek = async function (t) {
    let n = 0;
    for (const x of S.els) {
      const on = t >= x.e.start && t < x.e.end;
      x.root.style.display = on ? 'block' : 'none';
      if (on) { x.inst.update(t - x.e.start, x.e.end - x.e.start, t); n++; }
    }
    if (S.pending.length) { await Promise.all(S.pending); S.pending = []; }
    return n;
  };
})();
