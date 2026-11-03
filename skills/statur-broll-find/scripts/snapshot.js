/* Save the page open in YOUR browser as one self-contained HTML file (styles, fonts and images inlined),
   downloaded to your Downloads folder. Then render it anywhere at any resolution with render_snapshot.py.

   Why: a screenshot is stuck at your screen size, and a headless browser in the cloud often cannot see the
   page (sign-in, blocked style servers, bot checks). A snapshot keeps the real layout of a page you are
   allowed to see, renders crisp at 2x, and lets you hide private parts before anything is captured.

   How: open the page, then run this code in the page (an agent with a browser extension runs it for you;
   by hand: DevTools console). Await it: it returns a short report. Your own pages first; a third-party page
   needs a reason (commentary, news) and stays a decision for the human reviewer.
   Rights: you capture what you can already see; nothing is sent anywhere but your Downloads folder. */
(async (fileName = 'snapshot_' + location.hostname.replace(/\W+/g, '_') + '.html') => {
  const toData = async (url) => {
    const r = await fetch(url, {mode: 'cors', credentials: 'omit'});
    const b = await r.blob();
    return await new Promise(res => { const fr = new FileReader(); fr.onload = () => res(fr.result); fr.readAsDataURL(b); });
  };
  const links = [...document.querySelectorAll('link[rel="stylesheet"]')];
  let css = '', fontsOk = 0, fontsFail = 0, cssFail = 0;
  for (const l of links) {
    try {
      let t = await (await fetch(l.href)).text();
      const urls = [...new Set([...t.matchAll(/url\((['"]?)([^'")]+\.(?:woff2|woff|ttf|otf))\1\)/g)].map(m => m[2]))];
      for (const u of urls) {
        try { const d = await toData(new URL(u, l.href).href); t = t.split(u).join(d); fontsOk++; } catch (e) { fontsFail++; }
      }
      css += `/* ${l.href} */\n${t}\n`;
    } catch (e) { cssFail++; }
  }
  const clone = document.documentElement.cloneNode(true);
  clone.querySelectorAll('script, noscript, iframe, link[rel="stylesheet"], link[rel="preload"], link[rel="modulepreload"], link[rel="prefetch"]').forEach(n => n.remove());
  const base = document.createElement('base'); base.href = location.href; clone.querySelector('head').prepend(base);
  const st = document.createElement('style'); st.textContent = css; clone.querySelector('head').appendChild(st);
  const imgs = [...clone.querySelectorAll('img')]; let ok = 0, fail = 0;
  for (const im of imgs) {
    try { if (!im.src || im.src.startsWith('data:')) continue; im.src = await toData(im.src); im.removeAttribute('srcset'); ok++; } catch (e) { fail++; }
  }
  const meta = document.createElement('meta'); meta.name = 'snapshot-source';
  meta.content = JSON.stringify({url: location.href, title: document.title, at: new Date().toISOString(), w: innerWidth});
  clone.querySelector('head').appendChild(meta);
  const html = '<!DOCTYPE html>\n' + clone.outerHTML;
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([html], {type: 'text/html'})); a.download = fileName;
  document.body.appendChild(a); a.click(); a.remove();
  return JSON.stringify({file: fileName, url: location.href, stylesheets: links.length, cssFail, fontsOk, fontsFail, images: imgs.length, imagesInlined: ok, imagesFailed: fail, kb: Math.round(html.length / 1024)});
})()
