#!/usr/bin/env python3
"""Validate the format cards and build the library index.

Usage (from the repo root or anywhere):
  python3 skills/format-library-coach/scripts/build_library.py          validate + write README.md, index.csv, index.json
  python3 skills/format-library-coach/scripts/build_library.py --check  validate only, exit 1 on any problem
  python3 skills/format-library-coach/scripts/build_library.py --find funnel=BOFU setup=screen-recording
                                                                        print the formats that carry every given tag

Cards live in library/formats/<slug>.md. Each card starts with a frontmatter block of
"key: value" lines (lists are comma-separated). Tags must come from references/taxonomy.json.
Standard library only.
"""
import csv
import io
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
LIB = SKILL / "library"
CARDS = LIB / "formats"
TAXO = json.loads((SKILL / "references" / "taxonomy.json").read_text(encoding="utf-8"))

REQUIRED = ["id", "name", "funnel", "value", "structure", "setup", "origin", "founder_on_camera", "effort", "length", "status", "added"]
LIST_FIELDS = ["aka", "funnel", "value", "structure", "setup"]
TAG_DIMS = ["funnel", "value", "structure", "setup"]
SECTIONS = ["## Shape", "## Beats", "## Make it yours", "## Examples", "## For your AI"]
BANNED = {"—": "em dash", "–": "en dash"}
ID_RE = re.compile(r"^F\d{3}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
EXAMPLE_RE = re.compile(r"^- \[[^\]]+\]\((https?://[^)]+)\)", re.M)


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return re.sub(r"-+", "-", s)


def parse(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text, text
    end = text.find("\n---", 4)
    head, body = text[4:end], text[end + 4:]
    data = {}
    for line in head.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if k in LIST_FIELDS:
            data[k] = [x.strip() for x in v.split(",") if x.strip()]
        else:
            data[k] = v
    return data, body, text


def vocab(dim):
    return {t["id"] for t in TAXO["dimensions"][dim]["tags"]}


def load():
    cards, errors = [], []
    seen_ids, seen_names = {}, {}
    for path in sorted(CARDS.glob("*.md")):
        where = f"library/formats/{path.name}"
        fm, body, text = parse(path)
        if fm is None:
            errors.append(f"{where}: missing frontmatter")
            continue
        for key in REQUIRED:
            if not fm.get(key):
                errors.append(f"{where}: field '{key}' is missing or empty")
        if fm.get("id") and not ID_RE.match(fm["id"]):
            errors.append(f"{where}: id must look like F001")
        if fm.get("id") in seen_ids:
            errors.append(f"{where}: id {fm['id']} already used by {seen_ids[fm['id']]}")
        seen_ids[fm.get("id")] = path.name
        key = (fm.get("name") or "").lower()
        if key in seen_names:
            errors.append(f"{where}: name already used by {seen_names[key]}")
        seen_names[key] = path.name
        expected = f"{slugify(fm.get('name', ''))}.md"
        if path.name != expected:
            errors.append(f"{where}: file name must be {expected} (slug of the name)")
        for dim in TAG_DIMS:
            allowed = vocab(dim)
            for tag in fm.get(dim, []):
                if tag not in allowed:
                    errors.append(f"{where}: {dim} tag '{tag}' is not in references/taxonomy.json")
        for field, allowed in (("origin", {"mimetic", "original"}), ("founder_on_camera", {"yes", "no", "optional"}),
                               ("effort", {"low", "medium", "high"}), ("status", {"draft", "tested", "proven"})):
            if fm.get(field) and fm[field] not in allowed:
                errors.append(f"{where}: {field} must be one of {sorted(allowed)}")
        for sec in SECTIONS:
            if sec not in body:
                errors.append(f"{where}: missing section '{sec}'")
        for ch, label in BANNED.items():
            if ch in text:
                errors.append(f"{where}: contains an {label}")
        examples = EXAMPLE_RE.findall(body.split("## Examples", 1)[-1].split("\n## ", 1)[0]) if "## Examples" in body else []
        shape = ""
        if "## Shape" in body:
            shape = body.split("## Shape", 1)[1].split("\n## ", 1)[0].strip().split("\n")[0]
        fm["file"] = path.name
        fm["examples"] = len(examples)
        fm["shape"] = shape
        cards.append(fm)
    return cards, errors


def row(c):
    return {
        "id": c["id"], "name": c["name"], "funnel": " ".join(c.get("funnel", [])), "value": " ".join(c.get("value", [])),
        "structure": " ".join(c.get("structure", [])), "setup": " ".join(c.get("setup", [])), "origin": c.get("origin", ""),
        "founder_on_camera": c.get("founder_on_camera", ""), "effort": c.get("effort", ""), "length": c.get("length", ""),
        "status": c.get("status", ""), "examples": c["examples"], "file": f"formats/{c['file']}", "shape": c["shape"],
    }


def write_outputs(cards):
    cards = sorted(cards, key=lambda c: c["id"])
    rows = [row(c) for c in cards]
    files = {}
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    files[LIB / "index.csv"] = buf.getvalue()
    files[LIB / "index.json"] = json.dumps({"version": TAXO["version"], "count": len(rows), "formats": rows}, ensure_ascii=False, indent=1) + "\n"

    def link(c):
        return f"[{c['name']}](formats/{c['file']})"

    out = [
        "# The Format Library",
        "",
        "Generated by `scripts/build_library.py` from the cards in `formats/`. Do not edit by hand: edit a card, then run the script.",
        "",
        f"{len(cards)} formats. Taxonomy version {TAXO['version']}. Tags and definitions: [references/taxonomy.md](../references/taxonomy.md). Machine-readable index: [index.csv](index.csv), [index.json](index.json).",
        "",
        "A format is a repeatable shape for a short video: the same opening, the same structure and the same setup, with a new topic each time. Every card carries four kinds of tags that combine freely: funnel (where it works), value (why people watch and share), structure (what happens, in order) and setup (how it is shot and edited).",
        "",
        "Status: draft = described from public examples; tested = shot at least once in a real program; proven = kept after a format review on mature data.",
        "",
        "## All formats",
        "",
        "| ID | Format | Funnel | Value | Structure | Setup | Founder on camera | Effort | Status |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for c in cards:
        out.append(f"| {c['id']} | {link(c)} | {', '.join(c['funnel'])} | {', '.join(c['value'])} | {', '.join(c['structure'])} | {', '.join(c['setup'])} | {c['founder_on_camera']} | {c['effort']} | {c['status']} |")
    for dim in TAG_DIMS:
        d = TAXO["dimensions"][dim]
        out += ["", f"## By {dim}", "", d["question"], ""]
        for t in d["tags"]:
            hits = [c for c in cards if t["id"] in c.get(dim, [])]
            if not hits:
                continue
            out.append(f"- **{t['label']}** ({len(hits)}): " + ", ".join(link(c) for c in hits))
    out.append("")
    files[LIB / "README.md"] = "\n".join(out)
    return files


TAXO_INTRO = """# Format Library taxonomy

Generated by `scripts/build_library.py` from `taxonomy.json`. Edit the JSON, then run the script.

Version {version}, {updated}.

A format is a repeatable shape for a short video: the same opening, the same structure and the same setup, with a new topic each time. Every card carries tags on four dimensions. A card can carry several tags per dimension, and the dimensions combine freely: a founder story can be shot as yapping in a car or as a cinematic voice-over, and work at the top or the middle of the funnel.

Why four dimensions: a single list of tags mixes things that answer different questions (where it works, why people share it, what happens, how it is shot). Separated, they let anyone filter the library by goal (BOFU), by constraint (no face, low effort) or by skill (screen recording only).

## Naming rule

Name = distinctive element + structure + (twist or ending). In English, short enough to search.

- "Smart-glasses street prank (demo at the end)": the glasses are the distinctive element, the prank is the structure, the demo is the ending.
- Same structure and setup, another topic: same card, new example.
- Same structure, a setup or an ending that changes the beats: new card.

## Other fields

"""


def write_taxonomy_md(cards):
    out = [TAXO_INTRO.format(version=TAXO["version"], updated=TAXO["updated"]).rstrip(), ""]
    for field, vals in TAXO["fields"].items():
        out.append(f"- **{field}**: " + "; ".join(f"{k} = {v}" for k, v in vals.items()))
    for dim in TAG_DIMS:
        d = TAXO["dimensions"][dim]
        out += ["", f"## {dim}", "", d["question"], "", "| Tag | Label (EN) | Label (FR) | Definition | Cards |", "|---|---|---|---|---|"]
        for t in d["tags"]:
            n = sum(1 for c in cards if t["id"] in c.get(dim, []))
            out.append(f"| `{t['id']}` | {t['label']} | {t['fr']} | {t['def']} | {n} |")
    out.append("")
    return {SKILL / "references" / "taxonomy.md": "\n".join(out)}


def find(cards, filters):
    hits = []
    for c in cards:
        ok = True
        for f in filters:
            k, _, v = f.partition("=")
            vals = c.get(k, [])
            if isinstance(vals, str):
                vals = [vals]
            if v not in vals:
                ok = False
                break
        if ok:
            hits.append(c)
    for c in sorted(hits, key=lambda c: c["id"]):
        print(f"{c['id']}  {c['name']}  [{', '.join(c['funnel'])} | {', '.join(c['value'])} | {', '.join(c['structure'])} | {', '.join(c['setup'])}]  formats/{c['file']}")
    print(f"{len(hits)} format(s)")


def main(argv):
    cards, errors = load()
    if argv[:1] == ["--lint"]:
        names = {Path(a).name for a in argv[1:]}
        mine = [e for e in errors if not names or any(f"/{n}:" in e for n in names)]
        for e in mine:
            print("  -", e)
        print(f"build_library --lint: {len(mine)} problem(s) in {len(names) or len(cards)} card(s)")
        return 1 if mine else 0
    if errors:
        print(f"build_library: {len(cards)} cards, {len(errors)} problem(s)")
        for e in errors:
            print("  -", e)
        return 1
    if argv[:1] == ["--find"]:
        find(cards, argv[1:])
        return 0
    files = write_outputs(cards)
    files.update(write_taxonomy_md(cards))
    if argv[:1] == ["--check"]:
        stale = [str(p.relative_to(SKILL)) for p, c in files.items() if not p.exists() or p.read_text(encoding="utf-8") != c]
        if stale:
            print(f"build_library: {len(cards)} cards, generated files out of date: {', '.join(stale)}. Run the script without --check.")
            return 1
        print(f"build_library: {len(cards)} cards, 0 problems, generated files up to date")
        return 0
    for p, c in files.items():
        p.write_text(c, encoding="utf-8")
    print(f"build_library: {len(cards)} cards, 0 problems, README.md, index.csv, index.json and references/taxonomy.md written")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
