# The AI video editor

Turn a talking-head recording or a planned clip into an edit at the production level you choose, with an AI agent and free local tools: from the basic captioned clip (the default of STATUR clipping) to a high-production edit with color, sound design, captures of your own pages, motion design and background replacement.

- Page (human version, source of truth): https://statur.co/ai-video-editor/
- Markdown for AI assistants: https://statur.co/ai-video-editor.md
- The essay behind it (louis-korczowski.org): the future of the video editor, coming soon
- Version 1.0, 2026-10-28 (page); skills statur-video-editor-pro 1.0.0, statur-motion-design 1.0.0, statur-sound-design 1.0.0, statur-color-grade 1.0.0, statur-broll-find 1.0.0

## Summary

Production value is a dial with four levels. Level 1 is the clipping edit and stays the default. Level 2 adds a clean SDR picture, a voice chain, emphasis in the captions, a music bed and sound effects on graphic entrances. Level 3 adds cards that prove each claim: captures of your own pages, lists from your own data, stats with their source line, diagrams. Level 4 adds background replacement, text behind the speaker and motion matched to a reference video you like. The evidence says attention craft (a hook in the first two seconds, captions, sound locked to picture, proof shown with context) pays everywhere and polish pays only in bounded cases, so the dial adds craft first and polish last. Every graphic is placed on the words it serves, every insert proves a sentence, every number carries its source, and a quality gate measures loudness, safe areas and the words heard back, then refuses what should not ship. Graphics are HTML templates rendered frame by frame into transparent layers; effects and music are generated, so nothing needs a license; each craft is a slot you can swap when a better tool appears.

Built from a real run on 2026-10-28: a 97-second iPhone selfie in HDR, recorded with a phone green-screen effect, edited to level 4 in about 35 to 45 minutes of compute on 2 cloud vCPUs (person matte, 23 graphic elements, 124 sound cues, generated music, captures of the cookbook repository and of the account's own clips).

## Skills

| Skill | Use it for |
|---|---|
| [statur-video-editor-pro](../skills/statur-video-editor-pro/) | The dial, the intake (level, reference videos, assets, music), the edit plan, the render command, the compositor, the quality gate and delivery. Works on a clip from statur-clipping or on any single recording. |
| [statur-motion-design](../skills/statur-motion-design/) | Graphics, captions, cards, diagrams, backgrounds and end cards as deterministic HTML templates, rendered with alpha in the brand's tokens. |
| [statur-sound-design](../skills/statur-sound-design/) | Voice cleanup, effects on visual events, a music bed ducked under the voice, loudness, with a generated library. |
| [statur-color-grade](../skills/statur-color-grade/) | HDR to SDR plate, the grade as a readable LUT, skin and level measures. |
| [statur-broll-find](../skills/statur-broll-find/) | What to show for each sentence, captures of your own pages (also signed-in pages through a snapshot), asset log with rights. |

The cut always comes from [statur-clip-edit](../skills/statur-clip-edit/) (`--plan-only`), so clipping and the pro editor share one cut logic.

## Credit

Rendering: ffmpeg, Playwright with Chromium, OpenCV and numpy. Person matte: Robust Video Matting (Lin et al., GPL-3.0, run as a separate tool). Voice denoise: RNNoise models for ffmpeg. Transcription: NVIDIA Parakeet TDT 0.6B v3 through sherpa-onnx. Fonts: Archivo, JetBrains Mono and Cormorant (SIL Open Font License).
