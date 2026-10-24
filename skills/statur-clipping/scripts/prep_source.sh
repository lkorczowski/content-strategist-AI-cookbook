#!/usr/bin/env bash
# Prepare one recording (live replay, webinar, podcast, long video) for clipping: put it in RUSHS,
# probe it, extract 16 kHz mono audio (FLAC) on the VIDEO's timeline for transcription, and build
# contact sheets of the picture.
# Usage: prep_source.sh SOURCE_FILE PROJECT_DIR CODE [STEP]
#   STEP = all (default) | rush | audio | sheets   (run the steps one by one on machines that cap command time)
#   MODE=copy (default) | link | move   environment variable, how the source enters RUSHS.
#     copy: the original stays where it is (APFS and reflink file systems copy instantly).
#     link: a symbolic link, no extra disk space; the original must stay in place.
#     move: only for a file in a plain local folder. Never move a file out of a synced folder
#           (Google Drive, Dropbox, OneDrive): it would disappear from the cloud for everyone.
# Creates PROJECT_DIR/RUSHS CODE, TRAVAIL CODE (work files) and EXPORTS CODE (masters).
set -euo pipefail
SRC="$1"; PROJ="$2"; CODE="$3"; STEP="${4:-all}"; MODE="${MODE:-copy}"
RUSH="$PROJ/RUSHS $CODE"; WORK="$PROJ/TRAVAIL $CODE"
mkdir -p "$RUSH" "$WORK/sheets" "$PROJ/EXPORTS $CODE"
EXT="${SRC##*.}"; EXT="$(printf '%s' "$EXT" | tr '[:upper:]' '[:lower:]')"
DEST="$RUSH/${CODE}_source.${EXT}"

if [ "$STEP" = all ] || [ "$STEP" = rush ]; then
  if [ ! -e "$DEST" ]; then
    case "$MODE" in
      link) ln -s "$(cd "$(dirname "$SRC")" && pwd)/$(basename "$SRC")" "$DEST" ;;
      move) mv "$SRC" "$DEST" ;;
      *) if [ "$(uname)" = Darwin ]; then cp -c "$SRC" "$DEST" 2>/dev/null || cp "$SRC" "$DEST";
         else cp --reflink=auto "$SRC" "$DEST" 2>/dev/null || cp "$SRC" "$DEST"; fi ;;
    esac
  fi
  ffprobe -v error -print_format json -show_format -show_streams "$DEST" > "$WORK/source_probe.json"
fi

if [ "$STEP" = all ] || [ "$STEP" = audio ]; then
  # aresample=async=1:first_pts=0 pads the start and fills gaps so that second N of the FLAC is
  # second N of the video. Live replays often start the audio 1 to 2 s after the video and drift;
  # without this, every word timestamp (and every cut) lands early. Check with sync_check.py anyway.
  ffmpeg -nostdin -y -v error -i "$DEST" -vn -af "aresample=async=1:first_pts=0" -ac 1 -ar 16000 -c:a flac "$WORK/audio16k.flac"
fi

if [ "$STEP" = all ] || [ "$STEP" = sheets ]; then
  if ffprobe -v error -select_streams v:0 -show_entries stream=codec_type -of csv=p=0 "$DEST" | grep -q video; then
    # contact sheets: one frame every 30 s, 10 x 5 tiles. Each frame is decoded with a 5 s pre-roll
    # (live recordings have long keyframe intervals: a direct seek gives grey frames).
    DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$DEST" | cut -d. -f1)
    TMPD=$(mktemp -d)
    i=0
    START=15; if [ "$DUR" -lt 30 ]; then START=$((DUR / 2)); fi
    for ((t=START; t<DUR; t+=30)); do
      s=$((t > 5 ? t - 5 : 0)); p=$((t - s))
      ffmpeg -nostdin -y -v error -ss "$s" -i "$DEST" -ss "$p" -frames:v 1 -vf "scale=180:-2" -q:v 4 "$TMPD/f_$(printf %04d $i).jpg" || true
      i=$((i + 1))
    done
    if ls "$TMPD"/f_*.jpg >/dev/null 2>&1; then
      ffmpeg -nostdin -y -v error -framerate 1 -i "$TMPD/f_%04d.jpg" -vf "tile=10x5" -q:v 4 "$WORK/sheets/overview_%02d.jpg"
    fi
    rm -rf "$TMPD" || true
  fi
fi

echo "PREP_DONE $DEST"
