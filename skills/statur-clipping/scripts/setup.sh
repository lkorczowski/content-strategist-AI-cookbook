#!/usr/bin/env bash
# Install the local toolchain of the statur-clipping skill: Python packages, the speech models and the
# caption font. Everything is free and runs offline after this step. About 650 MB of models.
# Usage: bash setup.sh [TOOLS_DIR]   (default: ~/Clips/_tools)
# Optional tools, installed only when a source needs them:
#   gdown   Google Drive links shared as "anyone with the link"   python3 -m pip install --user gdown
#   yt-dlp  YouTube videos you own (see references/sources.md)      python3 -m pip install --user yt-dlp
set -uo pipefail
DIR="${1:-$HOME/Clips/_tools}"
mkdir -p "$DIR/models" "$DIR/fonts"

if ! command -v ffmpeg >/dev/null; then
  echo "ffmpeg is missing. macOS: brew install ffmpeg   Debian/Ubuntu: sudo apt install ffmpeg   Windows: winget install ffmpeg"; exit 1
fi
ffmpeg -hide_banner -filters 2>/dev/null | grep -q " ass " || echo "WARNING: this ffmpeg has no libass, burned captions will fail. Install a full build."
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' || { echo "Python 3.10 or newer is needed."; exit 1; }

python3 -m pip install --user -q sherpa-onnx numpy 2>/dev/null || python3 -m pip install --break-system-packages -q sherpa-onnx numpy

cd "$DIR/models"
if [ ! -d sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8 ]; then
  curl -fsSL -o parakeet.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8.tar.bz2
  tar xjf parakeet.tar.bz2 && (rm -f parakeet.tar.bz2 || echo "Could not delete parakeet.tar.bz2 (about 490 MB): delete it by hand once the folder exists.")
fi
[ -f silero_vad.onnx ] || curl -fsSL -o silero_vad.onnx https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx

cd "$DIR/fonts"
[ -f ArchivoBlack-Regular.ttf ] || curl -fsSL -o ArchivoBlack-Regular.ttf https://github.com/google/fonts/raw/main/ofl/archivoblack/ArchivoBlack-Regular.ttf

echo "SETUP_DONE. Before running the scripts:"
echo "export ASR_MODEL_DIR=\"$DIR/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8\" VAD_MODEL=\"$DIR/models/silero_vad.onnx\""
