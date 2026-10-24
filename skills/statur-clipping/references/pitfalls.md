# Pitfalls met on real runs, and their fixes

The first items cost a render on the first real run (a 1:40 TikTok live in French, October 2026). The second run (three Loom recordings, one of them a 93-minute Google Meet session, mixed into five clips) added the sections on calls, screen recordings and mixes. Read this before the first render on a new kind of source.

## Timeline

- **Late audio.** Live replays, HLS downloads and MPEG-TS files often start the audio after the video and drift. On our TikTok replay: 1.71 s late, drifting 0.19 s over 100 minutes, so every cut of the first render landed early. Fix: extract the transcription audio with `-af aresample=async=1:first_pts=0` (prep_source.sh does it), run `sync_check.py` on every new file, and pass `--sync sync.json` to every render when it reports an offset.
- **Grey frames after a cut.** Live recordings have long keyframe intervals (about 2 s on TikTok, HEVC). The renderer seeks a few seconds early, decodes forward and trims inside the filter graph. Contact sheets need the same pre-roll.
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
- **A plan written on the platform's transcript.** Loom, YouTube and TikTok captions are timed per phrase (3 to 5 s) and mishear words. Plan on them, then transcribe only the chosen windows locally (`transcribe.py --ranges`) and snap every edge to the words (`snap_segments.py`). On our run: 13 minutes of a 93-minute call transcribed instead of the whole file.

## Picture

- **Captions over the face.** Look at a contact sheet before the first render. A selfie live often has the face in the lower half: move the crop down (`frame.crop_y` 0.6 on a 960x1920 replay) and the captions to 0.75 of the height, clear of the platform's bottom text and buttons.
- **Hook too small to read on a phone.** Hook size 90 to 100 on 1080x1920, two lines at most, one natural sentence. Two short punchy sentences read as AI-written.

## Calls, screen recordings and mixes

- **You are a thumbnail in your own call.** A recording of your own Meet or Zoom window shows the others big and you small (about 11% of the frame width). Use an audio-led layout (thumbnail enlarged in a rounded box, blurred background, big captions) and record your camera on its own next time.
- **"You are presenting".** The presenter's own view of a shared screen is dimmed under an overlay. Record the shared tab itself, or use the call's own recording.
- **Other people in the call.** They stay out of the picture and the sound unless they agreed in writing. Their short answers ("yes", "right") sit inside your sentences: cut them, and read the words around each cut.
- **Camera bubble of a screen recording.** On Loom, about 400 pixels in a 2170x1300 recording, bottom left. Crop the bubble a few pixels inside its edge, so the circle mask does not show a ring of the screen behind it.
- **Third-party videos on screen.** An analysis or a reaction shows someone else's video. Keep it to a few seconds per passage, tag the account when posting, and check the platform's rules on reused content.
- **Two recordings, two loudness levels.** A mix jumps between a quiet call and a loud solo recording. The renderer levels each source to the mean of the sources before the final normalization (`audio.level_sources`).
- **A stretched download.** Some platforms store a non-16:9 recording on a 16:9 grid. Check the file's size and sample aspect ratio with ffprobe; the renderer corrects the sample aspect ratio, and a source's `size` forces the true size.

## Machines and folders

- **Render where the footage is.** A 4K master never travels through a chat tool or a 20 MB upload limit. Only the review copies travel.
- **Sandboxes that stop commands.** Some agent sandboxes stop a command after a few minutes and kill background processes. Run `render_all.py --budget 150` and re-run until it prints ALL_DONE: each run resumes the clip it stopped.
- **Disk.** Rendered pieces weigh about 5 MB per second of clip; a 2-minute clip needs about 600 MB of temp space. render_all.py removes them after each clip unless `--keep-temp`. Keep the temp folder outside synced folders.
- **No deletion in connected folders.** Some sandboxes forbid deleting files in the user's folders. Put temp files in the sandbox's own temp folder, and ask the user before anything has to be removed.
- **A file staged twice.** Some file bridges cache a staged path: when a script changed, stage it under a new folder name, then check its checksum on the target machine.
- **A site the agent cannot reach.** The agent's own network may block the platform and its video servers. The user's browser reaches them: read the transcript in the page, start the platform's own download there.
- **An approval nobody can give.** The browser saves to the Downloads folder, and an unattended agent cannot get access to it (the request is refused while the user is away). Before the user leaves, ask for the folder, or ask them to drop the files into the project's RUSHS folder.
- **A player that starts at night.** Share pages autoplay. Pause and mute every player the agent opens on the user's computer.

## Review

- **Review copies too heavy for the page.** Keep them under 20 MB (720x1280, about 1.5 to 2 Mb/s for a 90-second clip). The master stays full quality.
- **Notes without timecodes.** The review page stamps every note with the player's time; ask reviewers to pause at the moment before writing.
