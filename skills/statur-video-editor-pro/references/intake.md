# Intake and reference videos

## The message to send (one time)

```
Before I edit: five quick choices. If you skip one, I use the default in brackets.
1. Production level, from 1 (clean captioned cut) to 4 (backgrounds, motion design, text behind you) [2]
2. A video whose editing you like: a link, or better the file if you have it [none]
3. What I may show on screen: your site, docs, repo, dashboards, past posts [your public site and your past posts]
4. Music: your licensed track, the platform's library when you post, or a generated bed [generated bed]
5. Platforms, caption language, deadline [TikTok, Reels, Shorts; language of the speech; 48 hours]
```

## Reference video: the style card

With a file the user may use (their own export, a client master, a video saved with the platform's own download):

```
python3 scripts/style_probe.py REF.mp4 --out style.json --sheet style.jpg [--words ref_words.json]
```

Look at style.jpg (one frame after each change), then fill the card. With a link only, watch the video and step through it; fill the same card by hand and say it is an estimate.

| Item | What to write |
|---|---|
| Pace | cuts per 10 s, median shot length, visual changes per 10 s (style.json), seconds between graphic beats |
| Layouts | full face, explainer split (diagram stage with the speaker in a card), picture in picture, screen only; when each one is used |
| Face share | share of frames where the face fills the frame |
| Hook | layout of the first 3 seconds: text position, size, how many lines, what moves |
| Captions | size, position, case, emphasis style, words per line |
| Inserts | types (screen capture, page, stock, own footage, motion card) and how many per minute |
| Motion design | vocabulary: counters, lower thirds, highlights, 3D tilts, kinetic words, maps; how items are revealed (blur to sharp, wipe, pop) |
| Type | title fonts and any accent font, case, sizes |
| Proof devices | how the reference shows results (collage of past videos with view counts, screenshots, numbers) |
| Sound | effects you can see as visual events, music presence and energy |
| Color | warm or cool, contrast, skin look, any visible look |
| Level | the dial level that matches, and what to copy or skip for this brand |

Then split the card in two lists for the brand: what to copy (layouts, pacing, proof devices), what to skip (anything the company context bans, e.g. glow, gradients, rounded corners).

Copy the method, never the assets: no frames, music or graphics from the reference go into the edit.
