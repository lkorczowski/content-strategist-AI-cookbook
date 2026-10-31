# Pitfalls met on real lives, and their fixes

Each item below cost a render on the first real run (a 1:40 TikTok live in French, October 2026). Read this before the first render on a new kind of source.

## Timeline

- **Late audio.** Live replays, HLS downloads and MPEG-TS files often start the audio after the video and drift. On our TikTok replay: 1.71 s late, drifting 0.19 s over 100 minutes, so every cut of the first render landed early. Fix: extract the transcription audio with `-af aresample=async=1:first_pts=0` (prep_source.sh does it), run `sync_check.py` on every new file, and pass `--sync sync.json` to every render when it reports an offset.
- **Grey frames after a cut.** Live recordings have long keyframe intervals (about 2 s on TikTok, HEVC). The renderer seeks a few seconds early, decodes forward and trims inside the filter graph. Contact sheets need the same pre-roll.
- **A silent opening on a corrupt audio stretch.** A TikTok replay can carry a damaged AAC stretch (decoder errors such as "Number of bands exceeds limit"). After a seek into or just before it, the decoder outputs silence for a few seconds, so a piece starting there plays mute while the transcript (decoded in one pass) has the words. Shortening the pre-roll brings grey frames back. Fix: `--audio-preroll 0.8` decodes the audio from its own short seek and keeps the video pre-roll. Spot it in the quality check (a whole planned phrase missing at the start of a piece) or with an isolated outlier in sync_check.py near that time.
- **A fade that mutes the clip.** Trims and fades belong inside the filter graph, after the pre-roll trim. A fade placed before an output-side seek is timed against the pre-roll and silences most of the piece.
- **Drift across many pieces.** Every piece lasts a whole number of frames, and its audio is counted in samples to the same length (fps filter, trim by frame number; atrim by sample count after resampling). Measuring audio by its timestamps let jittery replay audio drift up to 0.1 s of lip sync over a one-minute clip.
- **Variable frame rate.** Phone lives are variable: set `frame.fps` (25 for a phone live) so the output is constant.

## Words and captions

- **French heard as English.** A bilingual speaker breaks a multilingual model on long chunks. Re-read every passage a clip uses with short chunks (`refine_span.py words.json audio START END`), then keep, phrase by phrase, the reading in the right language (`merge_best.py words.orig.json words.json START END --lang fr`).
- **Word timestamps are approximate.** Parakeet places words on an 80 ms grid, and a word often starts 50 to 150 ms before its timestamp. Pass `--audio audio16k.flac` so each cut-in moves back to the speech onset on the waveform. A cut next to a removed word can still keep a short tail of it ("mais", "euh"): the quality check reports a word heard but not planned; widen the `cut` range (it is applied exactly) or accept it.
- **A lone question mark.** The model can emit punctuation as its own token. The renderer joins punctuation to the previous word, with the French space before ? ! : ;.
- **Removed words in the captions.** Captions are built only from the words kept in the edit.
- **A caption fix that is a rewrite.** A fix corrects spelling, names, numbers and punctuation. It never changes what the speaker said, and it never changes the audio. Viewers notice a caption that says something else. If a sentence must change, cut it.
- **A hidden word that stays audible.** An empty fix hides words from the captions only. To remove a word from the clip, cut it.

## Picture

- **Captions over the face.** Look at a contact sheet before the first render. A selfie live often has the face in the lower half: move the crop down (`frame.crop_y` 0.57 to 0.61 with `frame.zoom` 1.15 on a 960x1920 replay) so the eyes sit near 40% of the height. Keep the captions at 0.625 of the height: below 0.65 is the platform bottom zone (text and buttons on TikTok and Reels).
- **Resolution switches inside a live replay.** TikTok replays change resolution with the bitrate (640x1280, then 960x1920, then back). The crop box is computed on the first frame, so on the other resolution it lands on the wrong part of the picture (face cut, ceiling in view). Check with `ffprobe -skip_frame nokey -show_entries frame=width,height` and set `frame.norm` to the larger size.
- **Hook too small to read on a phone.** Hook size 90 to 100 on 1080x1920, two lines at most, one natural sentence. Two short punchy sentences read as AI-written.

## Machines and folders

- **Render where the footage is.** A 4K master never travels through a chat tool or a 20 MB upload limit. Only the review copies travel.
- **Sandboxes that stop commands.** Some agent sandboxes stop a command after a few minutes and kill background processes. Run `render_all.py --budget 150` and re-run until it prints ALL_DONE: each run resumes the clip it stopped.
- **Disk.** Rendered pieces weigh about 5 MB per second of clip; a 2-minute clip needs about 600 MB of temp space. render_all.py removes them after each clip unless `--keep-temp`. Keep the temp folder outside synced folders.
- **No deletion in connected folders.** Some sandboxes forbid deleting files in the user's folders. Put temp files in the sandbox's own temp folder, and ask the user before anything has to be removed.
- **A file staged twice.** Some file bridges cache a staged path: when a script changed, stage it under a new folder name, then check its checksum on the target machine.

## Review

- **Review copies too heavy for the page.** Keep them under 20 MB (720x1280, about 1.5 to 2 Mb/s for a 90-second clip). The master stays full quality.
- **Notes without timecodes.** The review page stamps every note with the player's time; ask reviewers to pause at the moment before writing.
