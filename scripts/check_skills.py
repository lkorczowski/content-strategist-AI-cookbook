#!/usr/bin/env python3
"""Validate every skills/<name>/SKILL.md against the Agent Skills rules used in this repo.

Usage: python3 scripts/check_skills.py            (from the repo root)
Exit code 1 when a rule fails. Standard library only.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BANNED = {"—": "em dash", "–": "en dash"}


def frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end < 0:
        return None, text
    head, body = text[4:end], text[end + 4:]
    data, parent = {}, None
    for line in head.splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") and parent:
            k, _, v = line.strip().partition(":")
            data.setdefault(parent, {})[k.strip()] = v.strip().strip('"')
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if v == "":
            parent, data[k] = k, {}
        else:
            parent, data[k] = None, v.strip('"')
    return data, body


def main():
    errors, count = [], 0
    for skill_md in sorted(ROOT.glob("skills/*/SKILL.md")):
        count += 1
        folder = skill_md.parent.name
        text = skill_md.read_text(encoding="utf-8")
        fm, body = frontmatter(text)
        where = f"skills/{folder}/SKILL.md"
        if fm is None:
            errors.append(f"{where}: missing YAML frontmatter")
            continue
        name = fm.get("name", "")
        if name != folder:
            errors.append(f"{where}: name '{name}' must equal the folder name")
        if not NAME_RE.match(name) or len(name) > 64:
            errors.append(f"{where}: name must be lowercase letters, digits and hyphens, 64 chars max")
        desc = fm.get("description", "")
        if not desc or len(desc) > 1024:
            errors.append(f"{where}: description must be 1 to 1024 characters (now {len(desc)})")
        if fm.get("license") != "MIT":
            errors.append(f"{where}: license must be MIT")
        meta = fm.get("metadata") or {}
        for key in ("author", "version"):
            if key not in meta:
                errors.append(f"{where}: metadata.{key} is missing")
        if len(body.splitlines()) > 500:
            errors.append(f"{where}: body over 500 lines, move detail to references/")
        for ch, label in BANNED.items():
            if ch in text:
                errors.append(f"{where}: contains an {label}")
        if "## Rules" not in body:
            errors.append(f"{where}: missing the '## Rules' section (drafts only, no passwords, no promised views)")
    for f in sorted(ROOT.rglob("*.md")):
        if ".git" in f.parts:
            continue
        t = f.read_text(encoding="utf-8")
        for ch, label in BANNED.items():
            if ch in t:
                errors.append(f"{f.relative_to(ROOT)}: contains an {label}")
    print(f"check_skills: {count} skills checked, {len(errors)} problem(s)")
    for e in errors:
        print("  -", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
