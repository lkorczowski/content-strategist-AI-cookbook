#!/usr/bin/env bash
# Create a statur-motion-3d v2 workspace: engine2 files, Three.js, brand fonts (Archivo, JetBrains Mono, Cormorant; OFL).
# Usage: setup_project2.sh <workspace_dir>. Then add one folder per video: <workspace>/<name>/scenario.json and shots.js.
set -euo pipefail
if [[ $# -lt 1 || "$1" == "--help" ]]; then sed -n '2,3p' "$0"; exit 0; fi
HERE="$(cd "$(dirname "$0")/.." && pwd)"; P="$1"; mkdir -p "$P/fonts"
cp "$HERE/engine2/index.html" "$HERE/engine2/core2.js" "$HERE/engine2/lib3d.js" "$P/"
cd "$P"; [[ -f package.json ]] || npm init -y >/dev/null
npm i --no-audit --no-fund three@0.170.0 @fontsource/archivo @fontsource/jetbrains-mono @fontsource/cormorant >/dev/null
cp node_modules/@fontsource/archivo/files/archivo-latin-{500,700,800,900}-normal.woff2 node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-{400,700}-normal.woff2 node_modules/@fontsource/cormorant/files/cormorant-latin-500-italic.woff2 fonts/
echo "workspace ready in $P"
