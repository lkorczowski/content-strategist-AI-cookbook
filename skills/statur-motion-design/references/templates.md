# Template catalog

Coordinates are pixels on a 1080x1920 stage. Local times (t, from, dur) are seconds from the element start; statur-video-editor-pro converts `t_src` (source time) into them. Colors default to the tokens.

## Text

| Template | Props | Notes |
|---|---|---|
| hook_box | text ("|" breaks a line), y (300), size (74), max_width (900), dot (true) | paper box, ink text, accent corner; pops in, words rise line by line |
| captions | words [{w, s, e, emph}] on the output timeline, y (1180), size (62), max_width (640), max_chars (15), lines (2), gap (0.45), hold (0.35), stroke (10), weight (800), case | words appear as said; current word in the accent color; emph words in an accent box; chunks break on length, pauses, sentence ends and commas |
| chips | items [{text, t, n}], y, size, gap | numbered chips that pop in one by one; the latest has an accent border |
| label_chip | text, x, y, size, anchor (center, left, right), style (ink, paper, accent), dot | small mono label, e.g. a date or a tool name |
| lower_third | name, title, sub, x, y, w | name card that wipes in from the left |
| big_text | text, y, size, color, outline, counter {from, to, format ("M" or number), prefix, suffix, t, dur}, swap [{t, text}] | for the layer behind the speaker; fits the stage width automatically |
| footnote | text, x, y, size, anchor | source line under a number |
| end_card | lockup, headline, url, sub | full-screen panel rising from the bottom |
| watermark | text, size, opacity, min, max, seed, mute [[s, e]] | moves among seven spots; hidden in mute windows |

## Cards

| Template | Props | Notes |
|---|---|---|
| panel | grid (true), enter (up, left, fade), exit (fade), color | opaque backdrop behind a card; give it z 2 and the card z 5 |
| card_list | label, title, counter, rows [{a, b, c}], x, y, w, row_h, first, stagger, max_rows | rows tick in; scrolls when rows exceed max_rows |
| page_card | img, frame {x, y, w, h}, view {x, y, w}, view_to {x, y, w} (image pixels), move [from, dur], tilt, url, label, highlights [{x, y, w, h, t, dur}] | the camera pans or zooms from view to view_to; highlight boxes draw at t; boxes come from render_snapshot.py --find |
| prompt_box | text, type_from, type_dur, enter_at, lines [...], line_stagger, who, to, x, y, w | a request typed to an assistant, then result lines |

## Diagrams

| Template | Props | Notes |
|---|---|---|
| chart_curve | points [[x, y]], xmax, ymax, xticks, yticks, markers [{x, y, text, anchor, dx, dy}], draw [from, dur], title, label, xlabel, title_size | the curve draws itself; markers pop as it passes; say "illustration" when the data is a model |
| loop_diagram | nodes [{text, sub}], active, cx, cy, r, draw, label, title, label_y, here | steps on a circle, the arc draws, "you are here" on the active node |
| timeline_cut | bar {x, y, w, h}, cuts [{s, e}] (fractions of the recording), posters [...], grid {x, y, cols, w, gap, rows_gap}, scan, fly, fly_stagger, title, label, result | a long recording scanned and cut; clips fly into a grid |

## Backgrounds (opaque, for keyed ranges)

| Template | Props | Notes |
|---|---|---|
| poster_wall | images [...], cols (3), speed [px/s per column], dim (0.62), scale | the account's own posters scrolling, toned down behind the speaker |
| ink_grid | grid (90), marks [{x, y, text, size, accent}], drift | flat brand background with a visible grid |
