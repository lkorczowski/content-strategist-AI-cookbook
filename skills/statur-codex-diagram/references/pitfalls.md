# Pitfalls (first build, 2026-11-13)

1. Label collisions. Handwriting fonts are narrower than a serif fallback, so a layout checked without the font loaded looks crowded, and the reverse. Always render with `--embed-fonts` for the check, or load the fonts in the page before looking. Alternate rows for long labels in a row of items.
2. File size. Rough multi-stroke paths and stipple grow fast: the first medallion scale weighed 495 kB. Fixes now in the engine: dots are zero-length round-capped strokes grouped in three sizes, path numbers are rounded to one decimal. Keep stipple counts under about 3,000 per figure; prefer `fill: 'hachure'` for large areas.
3. Rough "dots" fill style creates one path per dot: use `stipple` instead.
4. A blurred copy of a thin line gives almost no shadow. The shadow layer uses the filled silhouette of closed shapes and a thick stroke (9 to 10 px) for open lines.
5. Fonts in a standalone SVG (cover, video plate, image export) fall back silently. `--embed-fonts` puts the OFL fonts in the file as data URIs (about 95 kB more per file). In a page that already loads the fonts, render without embedding.
6. Filter ids derive from the seed. The same figure rendered twice in one page shares ids, which is harmless because the filters are identical; two different figures with the same seed in one page would clash: give each figure its own seed.
7. Text inside a rough.js shape is drawn over the shadow tint: keep text short and dark, or place it outside the shape.
8. Annotations drawn over HTML text (circles, underlines) are a separate tool, rough-notation (MIT), applied in the page; this skill draws figures, not page annotations.
