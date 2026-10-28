# Where it breaks

Met on the first real run (a 97-second iPhone selfie recorded with a phone green-screen effect, edited to level 4 on 2026-10-28), with the fix.

| Trap | What happened | Fix |
|---|---|---|
| HDR phone footage | The iPhone file is HEVC 10-bit HLG in BT.2020; converted without a tone map the face looks burnt, overlays look grey | statur-color-grade plate.py first (mobius, reference white 203), every later step reads the SDR plate |
| Captions on the mouth | The face sat low in the frame (eyes at 48%, mouth at 58% of the height); captions at 62% covered the mouth | Draw the caption zone on a frame grid before planning; captions at about 74% for a low face |
| Text behind the speaker unreadable | On the room background, a word behind a close face showed four letters | Key the speaker onto a plain stage for those words, scale the speaker to about 0.82 from the bottom, words above the head (subject_keys); or a camera punch-in instead |
| Hard line on shoulders and hands | A scaled speaker's plate ends inside the picture, so an arm stopped on a straight line | `composite.py --edge-feather 96` softens the sides of the moved plate |
| Brand font replaced by Arial | A fresh clone had no fonts installed; Chromium fell back to a system sans without any error | motion_render.py now stops when a token font is missing; install fonts with npm (statur-motion-design setup) |
| Re-rendered frames hid the rest of a layer | A partial render (`--only`) wrote a manifest with only its frames | The manifest now lists every frame of the timeline found on disk |
| Speaker card shows the forehead only | A wide card cropped a close selfie at the nose | A card close to square (700x680) keeps the head and chin; check one still per card |
| Speaker card shows a laptop | During some panels the raw footage filmed a screen, or used the phone green-screen effect with numbers behind | No card where the plate has no face or shows something the edit must not show |
| Last second missing | A part rendered 2400-2699 left out the 30 tail frames, the master came out 1 s short | The last part runs to the last frame (2400-2729 for 91 s at 30 fps); QA flags a duration gap |
| Cards invisible | Each card had a full-screen panel with a higher layer order, so the panel covered it | Panels at z 2, cards at z 5; check stills before the full render |
| A word missing from the transcript | ASR skipped "packaged" after a pause, so silence trimming would have cut it | Re-transcribe doubtful spans alone (transcribe.py --max-speech 2.5) and add the word to words.json |
| Phone green-screen effect baked in | The source already had a screenshot behind the speaker, low resolution, edges flicker | The person matte works on top of the baked effect: replace the background again with a designed one |
| Pages without styles in the cloud | A headless capture of a site loaded no CSS because the style server was blocked | snapshot.js in the user's browser, then render_snapshot.py offline at 2x |
| Slow previews | Each preview decoded the whole plate through 20 split filters | One select filter for chronological pieces; a pre-graded plate; stills with --frames |
| Background job never started | A wait loop matched its own launcher with `pgrep -f` | Wait on a process id or a file, never on a command-line pattern |
| Too many effects | 124 cues on 90 s, mostly ticks and keys | Keep ticks and keys 20 dB or more below the voice; one effect per visual event |
| Render killed after an hour | A background compositing job died at frame 1,200 of 2,730 with no error | Render parts of 300 frames in the foreground (`--segment`), join them (`--join`); only blend the box where a layer has pixels (2x faster) |
| Counter showing 0 before the number is said | The counter element started 0.3 s before its word | Start a counter element on the word that says the number |
| Speech check skipped | qa_pro.py could not find the ASR model of statur-clipping when the models were installed elsewhere | Set `ASR_MODEL_DIR` and `VAD_MODEL` before qa_pro.py, or install the models in statur-clipping/models |
| A part that looked finished | A part killed halfway kept its final name, so a resumed run skipped it | composite.py now writes `*.partial.mp4` and renames it only after the encoder succeeds |
