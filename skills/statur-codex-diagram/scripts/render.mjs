#!/usr/bin/env node
// render.mjs : render every figure of a spec module to SVG files (and an index.html contact sheet).
// Usage: node scripts/render.mjs <spec.mjs> <outdir> [--paper] [--seed N] [--style style.json] [--only name1,name2]
import { writeFileSync, mkdirSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import * as codex from './codex.mjs';

const args = process.argv.slice(2);
if (!args.length || args.includes('--help') || args.includes('-h')) {
  console.log(`render.mjs : codex-style SVG diagrams
  node scripts/render.mjs <spec.mjs> <outdir> [--paper] [--seed N] [--style style.json] [--only a,b]
  spec.mjs exports  figures = { name: (codex, opts) => Sketch }  (see examples/handbook-figures.mjs)
  --paper   add the paper ground (default: transparent, for pages that already have a paper background)
  --seed    change the hand: same seed = same drawing, another seed = another take
  --style   JSON file that overrides DEFAULT_STYLE tokens (ink, accent, fluo, shadow, hand, serif...)
  --only    render a subset
  --embed-fonts  embed the handwriting and serif fonts (Reenie Beanie, Newsreader, OFL) as data URIs: the SVG then renders the same everywhere (covers, video, image export)`);
  process.exit(0);
}
const [spec, out] = args; const flag = (k) => args.includes(k); const val = (k) => { const i = args.indexOf(k); return i > -1 ? args[i + 1] : undefined; };
const style = val('--style') ? JSON.parse(readFileSync(val('--style'), 'utf8')) : {};
const seed = val('--seed') ? parseInt(val('--seed'), 10) : undefined;
const only = val('--only') ? val('--only').split(',') : null;
const mod = await import(pathToFileURL(resolve(spec)).href);
let fontCSS = '';
if (flag('--embed-fonts')) {
  const here = new URL('..', import.meta.url).pathname;
  const face = (fam, file, styleKw = 'normal') => `@font-face{font-family:'${fam}';font-style:${styleKw};src:url(data:font/woff2;base64,${readFileSync(here + 'node_modules/@fontsource/' + file).toString('base64')}) format('woff2')}`;
  fontCSS = face('Reenie Beanie', 'reenie-beanie/files/reenie-beanie-latin-400-normal.woff2') + face('Newsreader', 'newsreader/files/newsreader-latin-400-normal.woff2') + face('Newsreader', 'newsreader/files/newsreader-latin-400-italic.woff2', 'italic');
}
mkdirSync(out, { recursive: true });
const cards = [];
for (const [name, fn] of Object.entries(mod.figures)) {
  if (only && !only.includes(name)) continue;
  const sk = fn(codex, { style, paper: flag('--paper'), seed });
  const svg = sk.toSVG({ title: name, fontCSS });
  writeFileSync(`${out}/${name}.svg`, svg);
  cards.push(`<figure><div>${svg}</div><figcaption>${name}</figcaption></figure>`);
  console.log('wrote', `${out}/${name}.svg`, (svg.length / 1024).toFixed(1) + ' kB');
}
writeFileSync(`${out}/index.html`, `<!doctype html><meta charset="utf-8"><title>codex diagrams</title>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital@0;1&family=Reenie+Beanie&display=swap" rel="stylesheet">
<style>body{background:#ECE9E1;font-family:Newsreader,Georgia,serif;margin:24px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:20px}figure{margin:0;background:#E2DED3;border:1px solid #cfc8b8}figcaption{padding:6px 10px;font-size:14px}svg{width:100%;height:auto;display:block}</style>
<main>${cards.join('\n')}</main>`);
