# Pitfalls

Each line: date, what broke, the fix.

- 2026-11-08. A strong spotlight plus an additive halo on the speaker turns the host into a white blob in close shots. Spot intensity 140 (not 900), halo opacity 0.12 near, rising to 0.6 only once the camera is far.
- 2026-11-08. A backside fresnel sphere for the atmosphere draws a hard teal ring at the globe edge. Use a camera-facing sprite with a radial gradient that peaks just outside the globe limb (about 0.82 of the sprite radius at 2.5 globe radii) and keep it under 0.35 opacity.
- 2026-11-08. Thousands of 1 px network lines at full alpha make a white hairball that hides the opportunity beat. Line alpha 0.32, node size 2.3 px.
- 2026-11-08. The first listener sat outside the frame, so "Then one person hears you" showed nobody. Place the beat's subject inside the camera's view cone at the beat's time, and check that still before the full render.
- 2026-11-08. Too many listener halos at the same scale read as white balls. Big halo for the first three listeners, small and dimmer for the cascade.
- 2026-11-08. The star field of lib3d.stars at radius 1500 sits inside a 3000-unit globe. Parent the stars to the camera position, scale them with the far plane, and turn depth test off.
- 2026-11-08. One camera curve from 12 units to 15,800 units breaks a fixed depth range. Set camera.near to 2 percent of the distance and far to 2.2 times the distance plus 2.5 globe radii, every frame.
- 2026-11-08. vork renders only on Apple Silicon (macOS 26) or NVIDIA RTX: the cloud sandbox and the Linux VM of a Mac cannot render it. Author and validate the scene anywhere, render on the GPU machine.
