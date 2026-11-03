# Pitfalls

Each line: date, what broke, the fix.

- 2026-10-30. Buildings placed too close filled the whole sky as a wall. Fix: skyline 190 to 460 m away, fewer and wider buildings, window texture repeat scaled to the facade.
- 2026-10-30. Space shots showed the park under the Earth: the world stays visible unless the shot calls `K.mode('space')` or `K.mode('none')`.
- 2026-10-30. POV hands vanished behind nearby people. Fix: hands are camera children drawn on top (depthTest off, renderOrder 999), and hand shots stand in an empty part of the park.
- 2026-10-30. The Moon sat inside the Earth sphere (scale 58 at 60 m puts the surface at 2 m). Check sphere radius against distance before a shot.
- 2026-10-30. White captions disappeared on white-out frames. Fix: dark multi-layer text shadow on captions and HUD.
- 2026-10-30. The glow phase washed the whole frame white two seconds too early. Fix: keep glow fill under 0.35 and the white overlay for the last second only.
- 2026-10-30. A font family declared only at weights 500 and 600 fails `document.fonts.check('16px Family')`. Check the exact weight and style used.
- 2026-10-30. Thin window lines alias to gray at a distance. Fix: 16 px grid on a 64 px texture, line width 1.5.
- 2026-10-30. A changed order of random draws moves trees and people: renders stay visually the same but are not pixel-identical. Keep the build order stable once a video is approved.
- 2026-10-31. Group offsets: sets built inside a group at x=400 need camera paths in world coordinates (400 + local). A forgotten offset films an empty street.
- 2026-10-31. Canvas text textures (signs) drawn before the web fonts load fall back to a default font. Load fonts before building the world (core2.js does it).
- 2026-10-31. Additive domes and glowing cities under strong bloom turn into white blobs. Keep dome opacity near 0.05 and bloom 0.9 with threshold 0.7.
- 2026-10-31. Open light cones under street lamps read as solid triangles on a CPU render. Keep them off.
- 2026-10-31. A huge torus in the sky can sit outside the frame or blend into it; a half-torus arch rising from the horizon with a flat color reads at once.
- 2026-10-31. Night scenes: characters vanish without a fill light; a point light parented to the camera fixes it cheaply.
- 2026-10-31. A neural voice needs a model install; in a locked cloud session, ship without voice and say so.
