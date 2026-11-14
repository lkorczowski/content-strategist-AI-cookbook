#!/usr/bin/env bash
# Create a statur-motion-3d v2 workspace: engine2 files, Three.js and the fonts named in the brand tokens (docs/BRAND-TOKENS.md).
# Usage: setup_project2.sh <workspace_dir> [tokens.json]. Tokens: the argument, else BRAND_TOKENS, else neutral open-license fonts. Then add one folder per video: <workspace>/<name>/scenario.json and shots.js.
set -euo pipefail
if [[ $# -lt 1 || "$1" == "--help" ]]; then sed -n '2,3p' "$0"; exit 0; fi
HERE="$(cd "$(dirname "$0")/.." && pwd)"; P="$1"; TOK="${2:-${BRAND_TOKENS:-}}"
if [[ -n "$TOK" ]]; then TOK="$(cd "$(dirname "$TOK")" && pwd)/$(basename "$TOK")"; fi
mkdir -p "$P/fonts"
cp "$HERE/engine2/index.html" "$HERE/engine2/core2.js" "$HERE/engine2/lib3d.js" "$P/"
cd "$P"; [[ -f package.json ]] || npm init -y >/dev/null
if [[ -n "$TOK" ]]; then cp "$TOK" brand.json; elif [[ ! -f brand.json ]]; then echo '{"name": "neutral"}' > brand.json; fi
npm i --no-audit --no-fund three@0.170.0 >/dev/null
# Fonts: each family installs from its @fontsource package (family name in lowercase with hyphens) and is copied
# under a generic name that index.html declares. A family with no package is skipped: the page falls back to a system font.
node - <<'NODE'
const fs = require('fs'), { execSync } = require('child_process');
const f = Object.assign({ display: 'Atkinson Hyperlegible', inscription: 'IBM Plex Mono', hand: 'Caveat' }, (JSON.parse(fs.readFileSync('brand.json', 'utf8')).fonts) || {});
const want = [
  ['display', 'display-regular', [[500, 'normal'], [400, 'normal'], [600, 'normal']]],
  ['display', 'display-bold', [[900, 'normal'], [800, 'normal'], [700, 'normal']]],
  ['inscription', 'label-regular', [[400, 'normal'], [500, 'normal']]],
  ['inscription', 'label-bold', [[700, 'normal'], [600, 'normal']]],
  ['hand', 'hand', [[500, 'italic'], [400, 'italic'], [500, 'normal'], [400, 'normal'], [700, 'normal']]],
];
const tried = {};
for (const [role, out, picks] of want) {
  const pkg = String(f[role]).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  if (!(pkg in tried)) { try { execSync(`npm i --no-audit --no-fund @fontsource/${pkg}`, { stdio: 'ignore' }); tried[pkg] = true; } catch (e) { tried[pkg] = false; } }
  const hit = tried[pkg] && picks.map(([w, s]) => `node_modules/@fontsource/${pkg}/files/${pkg}-latin-${w}-${s}.woff2`).find(p => fs.existsSync(p));
  if (hit) fs.copyFileSync(hit, `fonts/${out}.woff2`); else console.log(`font not installed: ${f[role]} (${out}); the page will use a system font`);
}
NODE
echo "workspace ready in $P"
