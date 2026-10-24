---
name: statur-clipping
description: Turn long recordings into ready-to-post vertical clips of 1 to 5 minutes, in French or English, with an AI agent and free local tools. Works from a live replay (TikTok, YouTube, Instagram, Facebook, LinkedIn, Twitch), a webinar, podcast or video call recording (Google Meet, Zoom), a screen recording (Loom), a long YouTube video, a Google Drive file or a whole Drive folder, or local files and folders, one recording at a time or several mixed into one clip. Covers permissions, getting the files, planning on the platform's own transcript, local transcription with word timestamps, the sync check, the clip plan, the edit with captions, layouts for screen shares and calls and a moving watermark, the quality check, the review page with timecoded notes, delivery, batches and the weekly routine. Use when someone wants clips from a live, a webinar, a call, a long video or a folder of recordings, or wants to set up a repeatable clipping routine.
license: MIT
metadata:
  author: Dr. Louis Korczowski
  version: "1.1.0"
  playbook: https://statur.co/clipping/
  repository: https://github.com/lkorczowski/content-strategist-AI-cookbook
---

# STATUR clipping

Part of the clipping playbook (https://statur.co/clipping/). Read https://statur.co/clipping.md for the human version, the costs, the limits and the sources when you can open links.

The job: one long recording in, a batch of clips ready to post out, the same day. The user records or points to the files, decides which clips to make, reviews them and posts them. The agent does the hours in between.

Companion skills in the same plugin: clip-plan (choose the moments), clip-edit (render a clip), clip-review (review page and notes). All scripts live in this skill's scripts/ folder.

## 0. Read the company context first

Look for a company context file (kb/01_BRAND.md from the blueprint, or .agents/product-marketing.md) and read it before anything else. A clipping skill without the company's own knowledge delivers a fraction of its potential: it picks entertaining moments instead of the moments that sell the company's ideas.

What the plan and the edit need from it, ask once for what is missing:
- Buyers and positioning, the formats that already work, the voice (words to avoid included).
- Numbers allowed in public, names that must never appear, the price policy.
- Clip length floor (default 60 seconds), language of the captions, caption font and colors, watermark text.

## 1. Permissions: ask first, say exactly what to click

- One working folder, for example `Clips` in the user's home. Claude desktop app: "+" next to the message box, then "Add folder". Claude Code: start it in that folder, or `/add-dir` the folder.
- The Downloads folder only if a browser download lands there, and the Google Drive for desktop folder only if a source lives in Drive. Ask for each one, one time, with the reason, before the user leaves: an unattended run cannot get the approval. The alternative: the user drops the files into the project's RUSHS folder.
- Platforms: the user signs in in their own browser. Never ask for a password, never copy cookies or tokens.
- Never delete the user's files. Temporary files go to a temp folder outside synced folders, and the agent removes only what it created.
- Never move a file out of a synced folder (Google Drive, Dropbox, OneDrive): it disappears from the cloud for everyone. Copy it.
- Some sandboxes stop a command after a few minutes or forbid deletions in connected folders: use `--budget` on the render scripts and re-run until they print DONE.

## 2. Install once

```
bash scripts/setup.sh ~/Clips/_tools
export ASR_MODEL_DIR=~/Clips/_tools/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8 VAD_MODEL=~/Clips/_tools/models/silero_vad.onnx
```

Needs ffmpeg with libass and Python 3.10 or newer. Installs sherpa-onnx and numpy, NVIDIA Parakeet TDT 0.6B v3 (25 European languages, punctuation, word timestamps, runs on a CPU) and Silero VAD from the sherpa-onnx GitHub releases, and the Archivo Black caption font. No GPU, no API key, no account.

## 3. Sources

| Source | How the file arrives | Watch out |
|---|---|---|
| Your own recording (OBS, TikTok LIVE Studio, StreamYard or Riverside local tracks, Zoom local recording) | a local path | best quality: make it the default for every live that matters |
| A live replay on the platform | the platform's own download: TikTok LIVE Center, YouTube Studio, Facebook, Instagram archive, Twitch Video Producer | replays expire (about 30 days on TikTok and Facebook); TikTok and YouTube Studio downloads come back at 720p or less; always run the sync check |
| A long YouTube video | the original upload file first; YouTube Studio download (MP4 at 720p or 360p) or Google Takeout for your own channel | a third-party downloader sits outside YouTube's terms: only for videos the user owns or has written permission for, after they confirm |
| A Google Drive file | the Google Drive for desktop path (no size limit), or a link shared as "anyone with the link" | private client footage: ask the owner, never change its sharing to make a download work |
| A Google Drive folder | the Drive for desktop folder, a shared folder link, or rclone with the user's own Google client ID | becomes a queue: one project per video |
| A local file or folder | a path | a folder becomes a queue |
| A Loom or other screen recording | the owner's "Download" in the video's menu (MP4), through the user's browser | the transcript is in the share page: plan on it before the download; non-16:9 recordings can download stretched |
| A video call (Google Meet, Zoom, Teams) | the call's cloud recording, or a local recording | your own call window shows you as a thumbnail and dims your shared screen: prefer speaker view or a local camera track |

Details, links and the commands per platform: references/sources.md.

```
python3 scripts/fetch_source.py SOURCE [SOURCE ...] --root ~/Clips [--i-own-this] [--dry-run]
```

It registers local files where they are, downloads Drive links (gdown) and, with `--i-own-this` only, YouTube links (yt-dlp) into `~/Clips/_inbox/`, and adds one item per video to `~/Clips/queue.json`. Exit code 2 with a `help` list means the agent needs a file from the user: read the list to them.

Audio-only sources (a podcast without video) transcribe and plan fine. The edit needs a video track.

When the platform shows a transcript (Loom, YouTube, TikTok captions), read it in the user's browser and plan before the download: the plan is ready when the file arrives, and only the chosen windows need a local transcription (`transcribe.py --ranges`).

## 4. One recording, step by step

1. Project folder. Name: date, code, title, for example `2026-10-24 LIVE01 Ask me anything`. Codes: LIVE, WEB (webinar), POD (podcast), VID (other video), numbered.
   `bash scripts/prep_source.sh FILE "~/Clips/<project>" LIVE01` copies the source into `RUSHS LIVE01`, writes `TRAVAIL LIVE01/source_probe.json`, the transcription audio `audio16k.flac` on the video's timeline and contact sheets, and creates `EXPORTS LIVE01`. `MODE=link` saves disk space for big files. Several recordings in one project: `SRCID=V2` names the file `WEB01_V2_source.mp4` and puts its work files in `TRAVAIL WEB01/V2/`.
2. Transcribe. `python3 scripts/transcribe.py "TRAVAIL LIVE01/audio16k.flac" "TRAVAIL LIVE01/asr"` writes words.json (one start and end time per word), a readable transcript and subtitles. Speed: about 15 minutes for 100 minutes of audio on 2 cloud vCPUs.
3. Sync check. `python3 scripts/sync_check.py "RUSHS LIVE01/LIVE01_source.mp4" "TRAVAIL LIVE01/audio16k.flac" --out "TRAVAIL LIVE01/sync.json"`. Exit 0: in sync. Exit 2: pass `--sync sync.json` to every render. One unchecked offset moves every cut.
4. Plan. Use the clip-plan skill: topic map, candidates of 60 seconds or more, hard gates, six scores, funnel stage. Show the plan as one table and let the user pick. Then write the spec of the best clip (format: references/spec.md).
5. Edit. Use the clip-edit skill: `clip_render.py` for one clip, `render_all.py` for a batch, then `qa_clip.py` on every master.
6. Review. Use the clip-review skill: a private page with the review copies, timecoded notes and a verdict per clip. Turn each note into a spec change, render the next version, answer the note.
7. Deliver. Masters in `EXPORTS LIVE01` named `LIVE01_C01_v2_slug.mp4` with their `.srt`, and per clip a brief: title, caption, hashtags, pinned comment. The root of `EXPORTS LIVE01` holds only the latest version of each clip, the one ready to post: when a new version is exported, render_all.py moves the older ones to `EXPORTS LIVE01/archives/` (moved, never deleted). A clip the user drops goes to `archives/` too, meaning it will not be used without changes. The user posts.

For the first test, stop after one clip and its review. Edit the others only after the user has seen that one.

## 5. Several recordings: a mix or a series

One project folder holds several recordings when they share a subject (a masterclass in three sessions, a week of lives). Two outputs, often both:
- a series: independent clips, each from one recording;
- a mix: one clip that strings passages of several recordings (the same idea told three times, an example from one session and the method from another).

The spec lists the recordings in `sources` and gives each segment its `src` (format: references/spec.md). The renderer levels the loudness of the sources, and each source or segment can take its own layout: the 9:16 crop for a selfie live, a camera bubble in a circle over a blurred screen, the shared screen on top with the bubble below, a call thumbnail in a rounded box. Measure each layout's rectangles on a frame of the recording, render a few seconds, look at them, then render the clip.

Video calls recorded from your own window are the hard case: you are a thumbnail, and your shared screen is dimmed. The clip becomes audio-led (thumbnail enlarged, big captions); record a camera track next time (references/sources.md).

## 6. A batch: a folder, a playlist, several lives

1. `fetch_source.py` on the folder or the links. Each video becomes a queue item.
2. Run the long steps for every item first, unattended: prep, transcription, sync check. Update the item's `status` in queue.json (prepped, transcribed, synced).
3. Plan each recording, one table per recording, and ask the user which clips to edit. Mark items `planned`.
4. Render the chosen clips, run the quality check, publish one review page per recording. Mark items `in_review`, then `delivered`.

Process the newest recording first unless the user sets another order. Replays that expire soon go first.

## 7. Watermark

Every clip carries a small moving watermark by default: the text `statur.co/clipping`, white at 55% opacity, which changes place every 3.5 to 6.5 seconds among seven spots and drifts slightly while it shows. The pattern is seeded per clip, so two clips never move the same way and a fixed crop cannot remove it. It credits the open-source tool and sends curious viewers to the playbook.

Change the text with `--watermark "yourbrand.com"` or the spec's `watermark.text`. Turn it off with `--watermark none` or `"watermark": {"enabled": false}`. Never put another platform's logo or handle on a clip meant for a different platform.

## 8. Routine

The weekly routine (check the inbox and the replays, prepare, transcribe, plan, render the top clips, send the review link) is described in references/routine.md, with the scheduled-task prompt. Switch it on only after one test ran end to end: a routine that needs the user every time adds work.

## 9. Where it breaks

The traps met on real runs (late audio, grey frames after a cut, a fade that mutes a clip, captions over the face, a lone question mark, a caption fix that changes the audio, a speaker who is a thumbnail in a call, a dimmed shared screen, two sources at different loudness, a site the agent cannot reach, an approval nobody can give at night) and their fixes: references/pitfalls.md. Read it before the first render on a new kind of source.

## Rules

- Drafts only: the agent never posts, schedules, deletes or shares anything for the user. The user posts.
- No passwords: the user signs in to every platform; the agent never asks for a password, a cookie or a token.
- No promised views or results, and no invented numbers: every figure in a hook, a caption or a report comes from the recording, the context file or a source the user can open.
- Respect each platform's terms of use: the user's own recordings or the platform's own download first; a third-party downloader only for content the user owns or has written permission for, after they confirm.
- Get the written consent of every guest before clipping them. Keep viewers' names and handles off screen unless there is a reason and their consent.
- Ask before touching any folder outside the working folder; never delete or move the user's originals.
