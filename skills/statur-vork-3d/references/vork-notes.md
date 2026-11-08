# vork notes

Read on 2026-11-08 from the vork README and its help pages (github.com/voyager-so/vork, main branch) and from the launch post on X (2026-11-06). Written in our own words; the README is the source.

## The launch post, checked against the README

| Claim in the post | What the README says |
|---|---|
| Core API fits in about 2,500 tokens | Not measured in the README. `vork help` is short by design and points to topics; treat the number as the author's. |
| 2x more token-efficient than Blender, Unreal Engine, Houdini | No method or numbers in the README. Unverified. |
| Up to 24x faster rendering | Preview profile only, earlier build: 14.6 to 36.4x faster than EEVEE on simple clips, with different settings. Default final profile: 1.14 to 2.32x faster than EEVEE on movies. Path tracing: 2 to 5.8x slower than Cycles. |
| 1 million birds in 97 s on one NVIDIA L4, EEVEE 31 min | 96.9 s is the measured vork movie (192 frames, 4 samples, 1080p24) without setup (244 s) and warmup (166 s). The EEVEE figure is a projection from eight frames at 16 samples, not a measured movie; the 4-sample projection is about 8 to 11x slower than vork. |
| Thread | A single post; the author's replies only point to the repo ("tell any agent to read the README and follow the install instructions"). |

Takeaway: a serious engine with honest benchmark notes in its README; the speed headline is the best case. For a short video, setup and shader compilation (minutes on first use) matter as much as render speed.

## Facts that drive our choices

- Rendering: Apple Silicon with Metal and macOS 26 (older macOS unqualified, Intel Macs unsupported), or Linux or Windows x64 with a recent NVIDIA GPU and a ray-tracing Vulkan driver. No CPU renderer. Docker needs a GPU on its host; Docker Desktop on a Mac does not pass Metal through.
- Install: install.sh from the GitHub release (checks SHA256SUMS, installs under ~/.local/lib/vork, runs `vork setup`). SDKs install from the vork folder, not from npm or PyPI. Release binaries were not downloadable from our cloud sandbox on 2026-11-08 (proxy 504), which is fine: the sandbox has no GPU anyway.
- Scene: JSON version 2, right-handed, Y up, metres, seconds, radians; unknown fields are errors. Editor schema: packages/ts/scene.schema.json (also published at voyager.so/vork/schema/scene.schema.json).
- Nodes: node, mesh, asset (glTF), camera, light. Meshes take `geometry` (a name, buffers, or a std builder such as sphere, box, grid, cylinder, cone, torus, capsule, rounded_box, revolve) and `instances` (TRANSLATION, ROTATION, SCALE buffers).
- Materials: OpenPBR (std/openpbr) with base_color, specular_roughness, emission_color, emission_luminance, transmission. Linear Rec.709 colors.
- Animation: `animation` layers of tracks; a track has a path of segments (["nodes", "cam", "translation"], ["materials", "m", "inputs", "emission_luminance"]) and keys [[t, value], ...], LINEAR by default. Camera target is structural: aim at a named node and animate that node.
- Profiles: std/previs (blocking), std/draft (4 samples, denoised), std/final (8 samples, default), std/path (path tracing). Stills with `--at SECONDS`, movies with `.mp4` output and `--frame-start/--frame-end` (inclusive).
- Compositing: compositor nodes with programs such as std/bloom (see the black-hole example for a full bloom chain).
- Limits in this preview: fog and volumes ignored, large scenes and dense transparency can fail, fine detail softens at low samples, first use of a program can compile for minutes.
- License: source-available preview license, free during the preview including commercial work, not open source. Example assets keep their own licenses.

## Our std-geometry validation trick

The editor schema describes scenes after std builders expand. vork_scene.py swaps every `{"std": ...}` geometry for a name before validating; the official examples/first-scene.json needs the same swap to pass. Python's jsonschema (Draft 2020-12) is enough.
