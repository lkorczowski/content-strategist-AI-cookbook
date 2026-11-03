---
name: statur-sound-design
description: Sound pass for short videos with an AI agent and free local tools: cut the voice sample-accurately from the edit list, clean it (denoise, EQ, de-esser, compression), place sound effects on visual events, lay a music bed ducked under the voice, and normalize to -14 LUFS with a report of each stem. Ships a generated effect library and a generated music bed, so nothing needs a license, and takes licensed tracks when the brand has them. Use when an edit needs sound design, music, voice cleanup or a loudness fix.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.0.0"
  playbook: https://statur.co/ai-video-editor/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# Sound design

Part of the AI video editor playbook (https://statur.co/ai-video-editor/). Called by statur-video-editor-pro; usable alone on any edit that has a cut list.

## Steps

1. Effects library, once: `python3 scripts/sfx_synth.py SFX_DIR` writes whoosh, whoosh_low, swish, swish_out, pop, tick, click, key_1 to key_6, snip, impact, riser_soft, chime. They are synthesized from noise and sines with a fixed seed: no sample, no license to track. Replace a file by a licensed sample of the same name to change its sound.
2. Music: the brand's licensed track, or `python3 scripts/music_bed.py music.wav --duration 91 --bpm 100 --key A --drops 33.5-35.9`: a calm generated bed (pad, plucked arpeggio, sub bass, soft drums) that stops its drums in the drop windows, a breath before a reveal. For TikTok, posting with a sound from the platform's commercial library is another option: then leave the music out of the master.
3. Mix: `python3 scripts/mix.py --source RAW --plan plan.json --sfx sfx.json --lib SFX_DIR --music music.wav --rnnoise sh.rnnn --out mix.wav`. It cuts the voice from the source with the plan's cut map (each piece a whole number of frames, 5 ms crossfades), runs the voice chain, places each cue, ducks the music under speech, then normalizes in two passes. mix_report.json gives the loudness of voice, effects, music and the final mix.

The cues (sfx.json) come from statur-video-editor-pro build_layers.py: every graphic entrance adds its own effect, the spec adds manual ones.

## Levels (defaults, tune per account)

| Item | Default | Why |
|---|---|---|
| Final | -14 LUFS integrated, -1.5 dBTP | common target for short-form; platforms turn loud uploads down |
| Music under speech | about 16 to 18 dB below the voice | no platform publishes a value; check voice_minus_music_db in the report |
| Music in pauses | about 10 dB below the voice | the bed comes up between sentences |
| Effects | -12 to -22 dB per cue; ticks and keys at -20 or lower | effects mark events, they never mask words |

## Rules of taste

- An effect only on a visual event: a card enters, a word lands, a number stops, a cut changes the place.
- Fewer, softer effects on a calm speaker; never an effect over a key word.
- The voice is the lead: if a word is hard to understand in the mix, lower the music, not the voice.
- Listen-free check: the report numbers, then a re-transcription of the master (statur-clipping qa_clip.py). A drop in words heard back means the mix covers the voice.

Licenses of libraries and models: references/sound.md.

## Rules

- Drafts only: the agent never posts or shares the audio or the video.
- No passwords; paid APIs only with the user's own key.
- Licensed music only: generated, the brand's own license, or the platform's library at posting time. Keep the license proof with the asset.
- Never change what the speaker said: cleanup and cuts only.
