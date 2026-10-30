#!/usr/bin/env bash
# Create (or refresh) a statur-motion-3d project folder: engine files, an example scenario and shot list,
# Three.js and the fonts (all OFL or MIT). Usage: setup_project.sh <project_dir> [example_name]
# Example names: folders of ../examples (default: kit-tour). Existing scenario.json and shots.js are kept.
set -euo pipefail
if [[ $# -lt 1 || "$1" == "--help" ]]; then sed -n '2,4p' "$0"; exit 0; fi
HERE="$(cd "$(dirname "$0")/.." && pwd)"
P="$1"; EX="${2:-kit-tour}"
mkdir -p "$P/fonts"
cp "$HERE/engine/index.html" "$HERE/engine/core.js" "$HERE/engine/kit.js" "$P/"
[[ -f "$P/scenario.json" ]] || cp "$HERE/examples/$EX/scenario.json" "$P/"
[[ -f "$P/shots.js" ]] || cp "$HERE/examples/$EX/shots.js" "$P/"
cd "$P"
[[ -f package.json ]] || npm init -y >/dev/null
npm i --no-audit --no-fund three@0.170.0 @fontsource/eb-garamond @fontsource/inter @fontsource/jetbrains-mono >/dev/null
for f in eb-garamond-latin-400-normal eb-garamond-latin-500-normal eb-garamond-latin-400-italic eb-garamond-latin-500-italic; do cp "node_modules/@fontsource/eb-garamond/files/$f.woff2" fonts/; done
for f in inter-latin-500-normal inter-latin-600-normal; do cp "node_modules/@fontsource/inter/files/$f.woff2" fonts/; done
cp node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2 fonts/
echo "project ready in $P (scenario.json, shots.js, engine, fonts)"
