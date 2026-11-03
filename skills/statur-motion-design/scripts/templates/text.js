/* Text templates: hook box, captions, chips, lower third, big text behind the speaker, footnote,
   end card, moving watermark. Colors and fonts come from the brand tokens (T). */
(function () {
  const {clamp, lerp, prog, spring, env, esc, rng, el} = STATUR.util;

  // Opening text hook: one sentence in a paper box near the top. "|" forces a line break.
  STATUR.register('hook_box', {
    create(e, root, T, c) {
      const p = Object.assign({y: 300, size: 74, max_width: 900, pad: [22, 34], align: 'center', dot: true}, e.props);
      const lines = String(p.text).split('|');
      const box = el('div', 'fd', `position:absolute;left:50%;top:${p.y}px;transform-origin:50% 0;width:max-content;max-width:${p.max_width}px;
        background:${T.paper};color:${T.ink};padding:${p.pad[0]}px ${p.pad[1]}px;font-size:${p.size}px;line-height:1.08;
        letter-spacing:-0.01em;text-align:${p.align};border-radius:${T.radius || 0}px`);
      box.innerHTML = lines.map(l => `<div class="ln" style="overflow:hidden"><div class="in">${esc(l.trim())}</div></div>`).join('');
      if (p.dot) box.appendChild(el('div', '', `position:absolute;left:-7px;top:-7px;width:14px;height:14px;background:${T.accent}`));
      root.appendChild(box);
      const ins = [...box.querySelectorAll('.in')];
      return {update(lt, dur) {
        const a = prog(lt, 0, 0.32, 'outBack'), out = clamp((dur - lt) / 0.18);
        box.style.opacity = Math.min(clamp(lt / 0.12), out);
        box.style.transform = `translateX(-50%) translateY(${lerp(18, 0, a) - (1 - out) * 10}px) scale(${lerp(0.92, 1, a)})`;
        ins.forEach((n, i) => { const k = prog(lt, 0.05 + i * 0.07, 0.28, 'outCubic'); n.style.transform = `translateY(${lerp(100, 0, k)}%)`; });
      }};
    }
  });

  // Word-by-word captions. words: [{w, s, e, emph}] on the output timeline. Words appear as they are said;
  // the current word takes the accent color; emphasized words get an accent box.
  STATUR.register('captions', {
    create(e, root, T, c) {
      const p = Object.assign({y: 1180, size: 62, max_width: 640, max_chars: 15, lines: 2, gap: 0.45, hold: 0.35,
                               stroke: 10, color: T.paper, active: T.accent, case: 'none', weight: 800}, e.props);
      const words = p.words.filter(w => w.w && w.w.trim());
      const chunks = []; let cur = [], len = 0;
      const lim = p.max_chars * p.lines;
      words.forEach((w, i) => {
        const prev = words[i - 1];
        const brk = cur.length && (len + w.w.length + 1 > lim || (prev && w.s - prev.e > p.gap) || /[.!?]$/.test(prev ? prev.w : '') || (cur.length >= 3 && /,$/.test(prev ? prev.w : '')));
        if (brk) { chunks.push(cur); cur = []; len = 0; }
        cur.push(w); len += w.w.length + 1;
      });
      if (cur.length) chunks.push(cur);
      chunks.forEach((ch, k) => { ch.s = ch[0].s - 0.04; const nx = chunks[k + 1]; ch.e = Math.min(nx ? nx[0].s - 0.02 : 1e9, ch[ch.length - 1].e + p.hold); });
      const box = el('div', '', `position:absolute;left:50%;top:${p.y}px;width:${p.max_width}px;transform:translate(-50%,-50%);text-align:center;
        font-family:'${T.font_display}',sans-serif;font-weight:${p.weight};font-size:${p.size}px;line-height:1.16;letter-spacing:-0.005em;
        text-transform:${p.case}`);
      root.appendChild(box);
      let shown = -1, spans = [];
      const mk = ch => {
        box.innerHTML = ch.map(w => `<span style="display:inline-block;margin:0 0.03em;padding:0 0.07em;position:relative;
          paint-order:stroke fill;-webkit-text-stroke:${p.stroke}px ${T.ink};color:${p.color}">${esc(w.w)}</span>`).join(' ');
        spans = [...box.children];
      };
      return {update(lt, dur, t) {
        const k = chunks.findIndex(ch => t >= ch.s && t < ch.e);
        if (k < 0) { box.style.display = 'none'; return; }
        box.style.display = 'block';
        if (k !== shown) { mk(chunks[k]); shown = k; }
        const ch = chunks[k];
        ch.forEach((w, i) => {
          const s = spans[i]; const said = t >= w.s - 0.03; const now = said && (i === ch.length - 1 ? t < w.e + 0.25 : t < ch[i + 1].s - 0.01);
          const pop = spring(t, w.s - 0.03, 2.4, 9);
          s.style.opacity = said ? 1 : 0;
          s.style.transform = `translateY(${said ? lerp(10, 0, Math.min(1, pop)) : 10}px) scale(${said ? lerp(0.86, 1, Math.min(1.04, pop)) : 0.86})`;
          if (w.emph) {
            s.style.background = said ? T.accent : 'transparent'; s.style.color = T.paper;
            s.style.webkitTextStroke = '0px'; s.style.borderRadius = (T.radius || 0) + 'px';
          } else {
            s.style.color = now ? p.active : p.color;
          }
        });
      }};
    }
  });

  // A row of numbered chips that appear one by one (steps, lists of three).
  STATUR.register('chips', {
    create(e, root, T, c) {
      const p = Object.assign({y: 300, size: 34, gap: 18, items: []}, e.props);
      const row = el('div', '', `position:absolute;left:50%;top:${p.y}px;transform:translateX(-50%);display:flex;gap:${p.gap}px;white-space:nowrap`);
      root.appendChild(row);
      const chips = p.items.map((it, i) => {
        const ch = el('div', 'fd', `display:flex;align-items:center;gap:12px;padding:14px 20px;background:${T.ink};color:${T.paper};
          font-size:${p.size}px;border:2px solid ${T.line};transform-origin:50% 50%;border-radius:${T.radius || 0}px`,
          `<span class="fm" style="font-weight:700;color:${T.accent};font-size:${Math.round(p.size * 0.7)}px">${esc(it.n || String(i + 1).padStart(2, '0'))}</span><span>${esc(it.text)}</span>`);
        row.appendChild(ch); return ch;
      });
      return {update(lt, dur) {
        const out = clamp((dur - lt) / 0.2);
        chips.forEach((ch, i) => {
          const t0 = p.items[i].t || 0, k = spring(lt, t0, 2.2, 8);
          const last = p.items.filter(x => (x.t || 0) <= lt).length - 1 === i;
          ch.style.opacity = (lt >= t0 ? 1 : 0) * out;
          ch.style.transform = `scale(${lt >= t0 ? lerp(0.6, 1, Math.min(1.06, k)) : 0.6})`;
          ch.style.borderColor = last ? T.accent : T.line;
        });
      }};
    }
  });

  // Small label chip anywhere (mono text), for context like a tool name or a date.
  STATUR.register('label_chip', {
    create(e, root, T, c) {
      const p = Object.assign({x: 540, y: 300, size: 30, anchor: 'center', style: 'ink'}, e.props);
      const bg = p.style === 'accent' ? T.accent : p.style === 'paper' ? T.paper : T.ink;
      const fg = p.style === 'paper' ? T.ink : T.paper;
      const ch = el('div', 'fm', `position:absolute;top:${p.y}px;left:${p.x}px;padding:12px 18px;background:${bg};color:${fg};font-size:${p.size}px;
        font-weight:700;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap;border:2px solid ${p.style === 'ink' ? T.line : bg}`,
        p.dot ? `<span style="color:${T.accent}">[&bull;]</span> ${esc(p.text)}` : esc(p.text));
      root.appendChild(ch);
      const ax = p.anchor === 'left' ? '0%' : p.anchor === 'right' ? '-100%' : '-50%';
      return {update(lt, dur) {
        const k = prog(lt, 0, 0.28, 'outBack'), out = clamp((dur - lt) / 0.18);
        ch.style.opacity = Math.min(clamp(lt / 0.1), out);
        ch.style.transform = `translate(${ax},${lerp(14, 0, k)}px)`;
      }};
    }
  });

  // Name card: who is speaking and why they are credible.
  STATUR.register('lower_third', {
    create(e, root, T, c) {
      const p = Object.assign({x: 70, y: 980, w: 720}, e.props);
      const box = el('div', '', `position:absolute;left:${p.x}px;top:${p.y}px;width:${p.w}px;background:${T.ink};border-left:10px solid ${T.accent};padding:22px 28px 24px`);
      box.innerHTML = `<div class="fd" style="font-size:50px;color:${T.paper};line-height:1.02">${esc(p.name)}</div>
        <div class="fb" style="font-weight:600;font-size:30px;color:${T.paper};opacity:.82;margin-top:10px">${esc(p.title)}</div>
        ${p.sub ? `<div class="fm" style="font-weight:700;font-size:22px;color:${T.accent};letter-spacing:.08em;text-transform:uppercase;margin-top:12px">${esc(p.sub)}</div>` : ''}`;
      root.appendChild(box);
      const kids = [...box.children];
      return {update(lt, dur) {
        const a = prog(lt, 0, 0.42, 'outQuint'), b = prog(lt, dur - 0.3, 0.3, 'inCubic');
        box.style.clipPath = `inset(0 ${lerp(100, 0, a) + b * 100}% 0 0)`;
        kids.forEach((k, i) => { const q = prog(lt, 0.12 + i * 0.07, 0.35); k.style.transform = `translateX(${lerp(-24, 0, q)}px)`; k.style.opacity = q; });
      }};
    }
  });

  // Big type, meant for the "under" layer so the speaker stays in front of it. Optional counter.
  STATUR.register('big_text', {
    create(e, root, T, c) {
      const p = Object.assign({y: 640, size: 300, color: T.paper, align: 'center', tracking: -0.04, outline: 0, swap: null}, e.props);
      const box = el('div', 'fd', `position:absolute;left:0;right:0;top:${p.y}px;text-align:${p.align};font-size:${p.size}px;line-height:.9;
        letter-spacing:${p.tracking}em;color:${p.outline ? 'transparent' : p.color};${p.outline ? `-webkit-text-stroke:${p.outline}px ${p.color};` : ''}
        transform-origin:50% 50%;white-space:nowrap`);
      root.appendChild(box);
      const fmt = (v) => {
        const cn = p.counter; if (!cn) return p.text;
        const x = Math.round(v);
        return (cn.prefix || '') + (cn.format === 'M' ? Math.round(x) + 'M' : x.toLocaleString('en-US')) + (cn.suffix || '');
      };
      return {update(lt, dur) {
        const a = prog(lt, 0, 0.35, 'outQuint'), out = clamp((dur - lt) / 0.22);
        if (p.counter) {
          const k = prog(lt, p.counter.t || 0, p.counter.dur || 1.0, 'outCubic');
          box.textContent = fmt(lerp(p.counter.from || 0, p.counter.to, k));
        } else if (p.swap) {
          const cur = p.swap.filter(s => lt >= s.t).pop();
          box.textContent = cur ? cur.text : p.text;
        } else box.textContent = p.text;
        // fit the line to the stage width once the text is set
        box.style.fontSize = p.size + 'px';
        const w = box.scrollWidth; if (w > c.W - 60) box.style.fontSize = Math.floor(p.size * (c.W - 60) / w) + 'px';
        box.style.opacity = Math.min(clamp(lt / 0.12), out);
        box.style.transform = `translateY(${lerp(60, 0, a)}px) scale(${lerp(1.08, 1, a)})`;
      }};
    }
  });

  // Source line under a number: small mono text.
  STATUR.register('footnote', {
    create(e, root, T, c) {
      const p = Object.assign({x: 540, y: 1300, size: 24, anchor: 'center'}, e.props);
      const n = el('div', 'fm', `position:absolute;top:${p.y}px;left:${p.x}px;font-size:${p.size}px;color:${T.paper};opacity:.85;letter-spacing:.04em;
        white-space:nowrap;background:${T.ink};padding:8px 14px`, esc(p.text));
      root.appendChild(n);
      const ax = p.anchor === 'left' ? '0%' : p.anchor === 'right' ? '-100%' : '-50%';
      return {update(lt, dur) { n.style.opacity = env(lt, dur, 0.2, 0.2) * 0.92; n.style.transform = `translate(${ax},0)`; }};
    }
  });

  // End card: full-screen panel that rises from the bottom, lock-up, headline, URL.
  STATUR.register('end_card', {
    create(e, root, T, c) {
      const p = Object.assign({lockup: '[•] STATUR.', headline: '', url: '', sub: ''}, e.props);
      const pan = el('div', '', `position:absolute;left:0;top:0;width:${c.W}px;height:${c.H}px;background:${T.ink}`);
      pan.innerHTML = `<div style="position:absolute;inset:0;background-image:linear-gradient(${T.line} 1px,transparent 1px),linear-gradient(90deg,${T.line} 1px,transparent 1px);background-size:90px 90px;opacity:.35"></div>
        <div style="position:absolute;left:90px;right:90px;top:520px">
          <div class="fm k1" style="font-size:34px;font-weight:700;letter-spacing:.12em;color:${T.paper}">${esc(p.lockup).replace('[•]', `[<span style="color:${T.accent}">&bull;</span>]`)}</div>
          <div class="fd k2" style="font-size:104px;line-height:.98;color:${T.paper};margin-top:40px;letter-spacing:-0.02em">${esc(p.headline)}</div>
          <div class="fm k3" style="font-size:44px;font-weight:700;color:${T.accent};margin-top:56px;display:inline-block;border-bottom:4px solid ${T.accent};padding-bottom:8px">${esc(p.url)}</div>
          ${p.sub ? `<div class="fm k4" style="font-size:28px;color:${T.paper};opacity:.7;margin-top:40px;letter-spacing:.06em;text-transform:uppercase">${esc(p.sub)}</div>` : ''}
        </div>`;
      root.appendChild(pan);
      const ks = ['.k1', '.k2', '.k3', '.k4'].map(s => pan.querySelector(s)).filter(Boolean);
      return {update(lt, dur) {
        const a = prog(lt, 0, 0.45, 'outQuint');
        pan.style.transform = `translateY(${lerp(100, 0, a)}%)`;
        ks.forEach((k, i) => { const q = prog(lt, 0.25 + i * 0.12, 0.4); k.style.opacity = q; k.style.transform = `translateY(${lerp(30, 0, q)}px)`; });
      }};
    }
  });

  // Small moving watermark: a new spot every 3.5 to 6.5 s among seven safe spots, slight drift, seeded.
  STATUR.register('watermark', {
    create(e, root, T, c) {
      const p = Object.assign({text: 'statur.co', size: 28, opacity: 0.5, min: 3.5, max: 6.5, seed: 7, mute: []}, e.props);
      const spots = [[0.22, 0.17], [0.74, 0.19], [0.18, 0.42], [0.70, 0.46], [0.24, 0.58], [0.66, 0.60], [0.50, 0.30]];
      const r = rng(p.seed); const plan = []; let t = 0, last = -1;
      while (t < (e.end - e.start) + 1) { let k; do { k = Math.floor(r() * spots.length); } while (k === last); last = k; const d = p.min + r() * (p.max - p.min); plan.push({t, d, k, dx: (r() - .5) * 40, dy: (r() - .5) * 30}); t += d; }
      const n = el('div', 'fb', `position:absolute;font-weight:700;font-size:${p.size}px;color:${T.paper};white-space:nowrap;
        paint-order:stroke fill;-webkit-text-stroke:3px rgba(14,14,12,.55)`, esc(p.text));
      root.appendChild(n);
      return {update(lt) {
        const s = plan.filter(x => x.t <= lt).pop() || plan[0]; const q = (lt - s.t) / s.d;
        const [fx, fy] = spots[s.k];
        n.style.left = (fx * c.W + s.dx * q) + 'px'; n.style.top = (fy * c.H + s.dy * q) + 'px';
        n.style.transform = 'translate(-50%,-50%)';
        const muted = p.mute.some(([a, b]) => lt >= a - e.start - 0.15 && lt < b - e.start + 0.15);
        n.style.opacity = muted ? 0 : p.opacity * Math.min(clamp((lt - s.t) / 0.3), clamp((s.t + s.d - lt) / 0.3));
      }};
    }
  });
})();
