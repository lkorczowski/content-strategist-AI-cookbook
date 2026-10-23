#!/usr/bin/env python3
"""Zip every skill folder into dist/<name>.zip, the format claude.ai accepts for upload.

Usage: python3 scripts/build_zips.py      (from the repo root). Attach the zips to a GitHub release.
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
out = ROOT / "dist"
out.mkdir(exist_ok=True)
for skill in sorted((ROOT / "skills").iterdir()):
    if not (skill / "SKILL.md").exists():
        continue
    target = out / f"{skill.name}.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(skill.rglob("*")):
            if f.is_file() and f.name != ".DS_Store":
                z.write(f, f"{skill.name}/{f.relative_to(skill)}")
    print("built", target.relative_to(ROOT))
