# Technology slots

Each row is a craft with a default that runs on a CPU without an account, its license, and what can replace it. Change one slot at a time; the spec format and the other skills do not change. Speeds measured on 2026-10-28 on a cloud machine with 2 vCPUs and 7 GB of RAM (ffmpeg 6.1, Python 3.13, Playwright Chromium), 1080x1920.

| Slot | Default (license) | Speed | Alternatives (license) | Owner skill |
|---|---|---|---|---|
| HDR to SDR | ffmpeg zscale + tonemap mobius, reference white 203 nits (LGPL ffmpeg, zimg WTFPL) | 22 fps | libplacebo bt.2390 when a Vulkan device exists (LGPL) | statur-color-grade |
| Grade | generated .cube LUT, lut3d, cas sharpening | 28 fps | the brand's own LUT; OpenColorIO (BSD-3) | statur-color-grade |
| Skin check | skin mask inside the person matte, hue against the 123 degree line | fast | a face detector | statur-color-grade |
| Person matte | Robust Video Matting, ONNX MobileNetV3 (GPL-3.0, run as a separate tool) | 3.5 fps end to end | RVM ResNet50 (better hair, 3x slower); MODNet (Apache-2.0); SAM 2 on a GPU (Apache-2.0) | statur-video-editor-pro |
| Green screen | ffmpeg chromakey + despill | 12 fps | none needed | statur-video-editor-pro |
| Voice | highpass, arnndn with an RNNoise model, EQ, de-esser, compressor | 36x realtime | DeepFilterNet3 (MIT or Apache-2.0) | statur-sound-design |
| Effects | sfx_synth.py, generated, no license to track | instant | Freesound CC0; a paid library the brand licenses | statur-sound-design |
| Music | music_bed.py, generated bed | instant | the brand's licensed track; the platform's library at posting time; ElevenLabs Music with a paid plan | statur-sound-design |
| Motion graphics | HTML/CSS templates captured frame by frame with Playwright (Apache-2.0) | 12 to 14 fps with alpha | HyperFrames (Apache-2.0); Remotion (source-available, paid above 3 people); Lottie (MIT); After Effects on a Mac | statur-motion-design |
| Captions | captions template in the over layer | in the layer | libass ASS (ISC), the statur-clip-edit default | statur-motion-design |
| B-roll | the company's own footage and pages: capture.py, snapshot.js + render_snapshot.py | seconds | Pexels API with attribution; generated clips with provenance and labels | statur-broll-find |
| Assembly | composite.py (numpy, OpenCV) piping to x264 | 3 to 9 fps | ffmpeg filter graphs for simple edits; PyAV (BSD-3) | statur-video-editor-pro |
| Hand-off | the pro spec + layer frames + receipts | n/a | OpenTimelineIO export for Premiere or Resolve (Apache-2.0), planned | statur-video-editor-pro |
| QA | qa_pro.py + statur-clipping qa_clip.py | 1 to 2 min | VMAF where available | statur-video-editor-pro |

## Setup

```
python3 -m pip install onnxruntime opencv-python-headless numpy scipy soundfile playwright
npm i --prefix ../statur-motion-design/fonts @fontsource/archivo @fontsource/jetbrains-mono @fontsource/cormorant
curl -LO https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx
curl -LO https://raw.githubusercontent.com/GregorR/rnnoise-models/master/somnolent-hogwash-2018-09-01/sh.rnnn
```

Plus the statur-clipping setup (ffmpeg with libass and zscale, Parakeet transcription model). Model files come from GitHub releases, which most sandboxes reach; Hugging Face often is blocked.

## Licenses to watch

GPL tools run as separate programs, never copied into a closed product. Non-commercial weights stay out (BRIA RMBG, MatAnyone, MusicGen, MMAudio). Artlist forbids automated downloads. Pixabay tracks can be registered with Content ID: keep the license page with the asset. Remotion needs a company license above 3 people.
