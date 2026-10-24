# Acquisition: transcript, clip layer, visual layer, audience signals

Use only sources that respect the platform's terms of use. Read what the page shows to any viewer, or files the user has the right to use. Never hook the page's network requests, replay internal API calls or extract signed media or caption URLs.

Transcripts of other people's videos are for private analysis (commentary and education); never republish them, and quote at most a short phrase with credit.

## 1. Transcript sources, in order of preference

1. A transcript the user pastes into the conversation.
2. A transcript or caption file that the user or the creator owns: an SRT or VTT exported from the creator studio of the platform or from the editing tool. Ask the user for it when the video is theirs or a client's.
3. The transcript or captions the platform shows to any viewer, for example YouTube's "Show transcript" panel under the description. The user copies it, or an assistant with a browser tool opens the panel and reads the visible text on the page. Read long panels in several passes: browser tools often cut long page text.
4. A local speech-to-text run on a video the user has the right to download, such as their own. Example with the open-source Whisper command line: `whisper video.mp4 --model small --language <lang> --output_format srt`.

Long reposts on short-video platforms often have no captions. Look for the original upload: it often has a transcript panel.

Save the result as `source/transcript-raw.txt`, one line per caption: `[mm:ss] text`. First line of the file: `# Third-party content, private analysis only. Source: <url>, read on <date>.`

## 2. Normalize to [mm:ss] lines

This snippet reads a copied transcript panel (a time line, then text lines), an SRT or a VTT, and prints `[mm:ss] text` lines. Save it in `work/` and run `python3 -I work/to_mmss.py <input> > source/transcript-raw.txt`.

```python
import re, sys
TS = re.compile(r'^(?:(\d+):)?(\d{1,2}):(\d{2})(?:[.,]\d+)?')
def mmss(m):
    t = int(m.group(1) or 0) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
    return f"[{t // 60:02d}:{t % 60:02d}]"
cur, text, out, last = None, [], [], None
def flush():
    if cur and text:
        out.append(cur + ' ' + ' '.join(text))
for raw in open(sys.argv[1], encoding='utf-8'):
    line = re.sub(r'<[^>]+>', '', raw).strip()
    if not line or line.isdigit() or line.startswith('WEBVTT'):
        continue
    m = TS.match(line)
    if m and ('-->' in line or len(line) <= 8):
        flush(); cur, text = mmss(m), []
    elif cur and line != last:
        text.append(line); last = line
flush()
print('\n'.join(out))
```

Automatic captions repeat rolling lines; the snippet drops a text line equal to the previous one. Check the first and last lines against the video before going on.

## 3. Coverage

`python3 -I scripts/coverage.py source/transcript-raw.txt <runtime_s>` lists every gap over 6 s. Build the time list for the clip layer from it: one sample every 2 s inside each gap over 5 s, plus the whole span of dense foreign-language clip regions.

## 4. Clip layer and visual layer

Burned-in subtitles and on-screen text are invisible to ASR. Read them from what the player shows.

On a video file the user has the right to use, build contact sheets with ffmpeg:

```sh
# visual layer: one frame every 30 s, 20 frames per sheet, time printed on each frame
ffmpeg -i video.mp4 -vf "fps=1/30,drawtext=text='%{pts\:hms}':x=4:y=4:fontsize=18:fontcolor=yellow,scale=320:-1,tile=4x5" work/frames-%02d.jpg
# clip layer: the subtitle strip (bottom 19% of the frame), one sample every 2 s inside one gap, 26 strips per sheet
ffmpeg -ss <gap_start_s> -to <gap_end_s> -i video.mp4 -vf "fps=1/2,crop=iw:ih*0.19:0:ih*0.79,scale=625:-1,tile=2x13" work/sub-<gap_start_s>-%02d.jpg
```

On someone else's video, watch the gaps and note what the screen shows, or take screenshots of the player at the sampled times with the player's own controls (pause, seek, a link with a start time). Respect the site's terms: no download, no scripted extraction of video frames.

Run one capture session at a time. Two overlapping runs give screenshots from the wrong timestamps. Redo any sheet whose subtitle lines do not follow each other.

Write `source/clip-log.md` (one bullet per clip beat: time range, track, dialogue paraphrased or quoted short) and `source/visual-layer.md` (counts of host on camera, third-party footage, art, cards, memes, title cards).

## 5. Audience signals

Read only what the page shows to any viewer, within the site's terms.

- Comments: scroll to load about 60, then read the page text. Note the likes and the mechanism of each comment. Read the pinned comment first. Never copy comments into a public page and never keep commenter names.
- "Most replayed": some players show a replay graph above the progress bar on hover. Note the peaks and their times. In the first days after upload it is often absent: note it and check later. It is the only direct retention signal available from outside the creator's account.
- Platform numbers: views, likes, saves, shares, comments, duration and publish date, as the page displays them, with the date you read them. Platforms round large counts (5.3M): keep the label as shown.

Write `source/audience-signals.md` as a paraphrased summary grouped by mechanism.

## 6. Tips for browser tools

- Long page text is often cut: read it in chunks and check the last line of each chunk.
- Text editors and some tools strip trailing spaces: trim lines before you compare two versions of a transcript by hash.
- If the browser connection drops, reconnect and resume from the last saved file instead of restarting the whole acquisition.
