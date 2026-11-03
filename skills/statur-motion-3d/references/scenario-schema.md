# scenario.json

All texts, times and sound cues of one video. Times are in seconds of screen time. Text fields accept `<br>` and `<hl>keyword</hl>` (colored, glowing).

| Field | Type | Meaning |
|---|---|---|
| width, height, fps, duration | numbers | output format; overlay positions are laid out for 720x1280 |
| seed | number | seeded layout of the world (change it for a different crowd and skyline) |
| event_time, return_time | numbers | read by shots.js of the park-to-space arc |
| title | object | `html`, `to` (end time), `fade`, `icon` ("atom" or none), `icon_until` |
| hud | list | segments `{from, to, label, clock, sub}` |
| hud[].clock | object | `{countdown_to: T}` real-time countdown to screen time T; `{countdown_from: X, start: T, slow: F}` game clock starting at X, F times slower than screen time; `{count_up_from: X, start: T, slow: F}`; `{text: "BACK"}` fixed big text |
| hud[].sub | string, list or object | fixed line; or `[[t, line], ...]` switching at times t; or `{template: "EARTH IS NOW {n} MILES WIDE", keys: [[t, value], ...]}` interpolated number |
| captions | list | `[from, to, text]`, one consequence each |
| end_card | object | `{from, html, fact}` |
| sound | list | cues for scripts/sound.py |

## Sound cues

| type | fields |
|---|---|
| ambience | from, to, gain, cut (low-pass Hz) |
| ticks | from, to, every, gain |
| riser | from, to, gain |
| boom | at, size, freq, gain |
| drone, pad, rumble, shimmer | from, to, gain |
| crackle, swell | from, to, gain |
| noise | from, to, cut, gain |
| note | from, to, freq, gain |
