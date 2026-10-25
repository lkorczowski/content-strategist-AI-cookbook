#!/usr/bin/env python3
"""The Format Library tool: validate the cards, build the index, and query the library.

Standard library only. Run from anywhere:

  python3 scripts/library.py build                     validate every card, write library/README.md, index.csv, index.json, references/taxonomy.md
  python3 scripts/library.py check                     validate, and fail if a generated file is out of date (CI)
  python3 scripts/library.py lint FILE [FILE ...]      validate only these cards (safe while others edit the library)
  python3 scripts/library.py find funnel=BOFU setup=screen-recording founder_on_camera!=yes q=demo
                                                       every filter must match; a comma means "or" (value=humour,surprising)
  python3 scripts/library.py suggest --n 8 --no-face --effort medium
                                                       a starter deck that covers TOFU, MOFU and BOFU with varied structures
  python3 scripts/library.py similar F094              the closest cards (same structure and setup): use before adding a card
  python3 scripts/library.py similar "street prank with glasses"
  python3 scripts/library.py new "Distinctive element + structure (twist)"   create a card from the template with the next free id
  python3 scripts/library.py gaps --top 15             structure x setup pairs that no card uses yet: raw material for original formats

Add --private DIR to find, suggest, similar and gaps to read a private library too (cards with ids P001, P002...).
Add --private DIR to new to create the card there with the next P id.
"""
import argparse
import csv
import datetime
import io
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
LIB = SKILL / "library"
CARDS = LIB / "formats"
TEMPLATE = SKILL / "references" / "card-template.md"
TAXO = json.loads((SKILL / "references" / "taxonomy.json").read_text(encoding="utf-8"))

REQUIRED = ["id", "name", "funnel", "value", "structure", "setup", "origin", "founder_on_camera", "effort", "length", "status", "added"]
LIST_FIELDS = ["aka", "funnel", "value", "structure", "setup"]
TAG_DIMS = ["funnel", "value", "structure", "setup"]
ENUMS = {"origin": {"mimetic", "original"}, "founder_on_camera": {"yes", "no", "optional"},
         "effort": {"low", "medium", "high"}, "status": {"draft", "tested", "proven"}}
SECTIONS = ["## Shape", "## Beats", "## Make it yours", "## Examples", "## For your AI"]
BANNED = {"—": "em dash", "–": "en dash"}
EXAMPLE_RE = re.compile(r"^- \[[^\]]+\]\((https?://[^)]+)\)", re.M)
EFFORT_RANK = {"low": 0, "medium": 1, "high": 2}
STATUS_WEIGHT = {"proven": 3.0, "tested": 2.0, "draft": 1.0}


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def vocab(dim):
    return {t["id"] for t in TAXO["dimensions"][dim]["tags"]}


def label(dim, tag):
    for t in TAXO["dimensions"][dim]["tags"]:
        if t["id"] == tag:
            return t["label"]
    return tag


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
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        data[k] = [x.strip() for x in v.split(",") if x.strip()] if k in LIST_FIELDS else v
    return data, body, text


def section(body, title):
    if title not in body:
        return ""
    return body.split(title, 1)[1].split("\n## ", 1)[0].strip()


def load(folder=CARDS, prefix="F", where_root="library/formats"):
    cards, errors = [], []
    seen_ids, seen_names = {}, {}
    id_re = re.compile(rf"^{prefix}\d{{3}}$")
    for path in sorted(Path(folder).glob("*.md")):
        where = f"{where_root}/{path.name}"
        fm, body, text = parse(path)
        if fm is None:
            errors.append(f"{where}: missing frontmatter")
            continue
        for key in REQUIRED:
            if not fm.get(key):
                errors.append(f"{where}: field '{key}' is missing or empty")
        if fm.get("id") and not id_re.match(fm["id"]):
            errors.append(f"{where}: id must look like {prefix}001")
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
        if f"# {fm.get('name', '')}" not in body:
            errors.append(f"{where}: the first heading must repeat the name")
        for dim in TAG_DIMS:
            allowed = vocab(dim)
            for tag in fm.get(dim, []):
                if tag not in allowed:
                    errors.append(f"{where}: {dim} tag '{tag}' is not in references/taxonomy.json")
        for field, allowed in ENUMS.items():
            if fm.get(field) and fm[field] not in allowed:
                errors.append(f"{where}: {field} must be one of {sorted(allowed)}")
        for sec in SECTIONS:
            if sec not in body:
                errors.append(f"{where}: missing section '{sec}'")
        for ch, name in BANNED.items():
            if ch in text:
                errors.append(f"{where}: contains an {name}")
        examples = EXAMPLE_RE.findall(section(body, "## Examples"))
        shape = section(body, "## Shape").split("\n")[0]
        fm.update(file=path.name, examples=len(examples), example_urls=examples, shape=shape, folder=str(folder))
        cards.append(fm)
    return cards, errors


def load_all(private=None):
    cards, errors = load()
    if private:
        pcards, perrors = load(private, prefix="P", where_root=str(private))
        cards += pcards
        errors += perrors
    return cards, errors


# ---------- build ----------

def row(c):
    return {
        "id": c["id"], "name": c["name"], "funnel": " ".join(c.get("funnel", [])), "value": " ".join(c.get("value", [])),
        "structure": " ".join(c.get("structure", [])), "setup": " ".join(c.get("setup", [])), "origin": c.get("origin", ""),
        "founder_on_camera": c.get("founder_on_camera", ""), "effort": c.get("effort", ""), "length": c.get("length", ""),
        "status": c.get("status", ""), "examples": c["examples"], "aka": "; ".join(c.get("aka", [])),
        "file": f"formats/{c['file']}", "shape": c["shape"],
    }


def link(c):
    return f"[{c['name']}](formats/{c['file']})"


def generated(cards):
    cards = sorted(cards, key=lambda c: c["id"])
    rows = [row(c) for c in cards]
    files = {}
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    files[LIB / "index.csv"] = buf.getvalue()
    files[LIB / "index.json"] = json.dumps({"version": TAXO["version"], "updated": TAXO["updated"], "count": len(rows),
                                            "formats": rows}, ensure_ascii=False, indent=1) + "\n"
    n = len(cards)
    count = lambda pred: sum(1 for c in cards if pred(c))
    out = [
        "# The Format Library",
        "",
        "Generated by `scripts/library.py build` from the cards in `formats/`. Edit a card, never this file.",
        "",
        "A format is a repeatable shape for a short video: the same opening, the same structure and the same setup, with a new topic each time. "
        "A founder who posts formats judges each one on several videos and keeps what lands. Every card carries tags on four dimensions that combine freely: "
        "**funnel** (where it works), **value** (why people watch and share), **structure** (what happens, in order) and **setup** (how it is shot and edited).",
        "",
        f"**{n} formats.** {count(lambda c: c['origin'] == 'original')} original, {count(lambda c: c['origin'] == 'mimetic')} mimetic. "
        f"{count(lambda c: c['founder_on_camera'] != 'yes')} work without the founder's face. {count(lambda c: c['effort'] == 'low')} take low effort. "
        f"Taxonomy version {TAXO['version']}: [tags and definitions](../references/taxonomy.md). Machine-readable: [index.csv](index.csv), [index.json](index.json).",
        "",
        "Status: draft = described from public examples; tested = shot at least once in a real program; proven = kept after a format review on mature data.",
        "",
        "## Quick picks",
        "",
    ]
    picks = [
        ("Bottom of funnel (sell)", lambda c: "BOFU" in c["funnel"]),
        ("No face on camera", lambda c: c["founder_on_camera"] == "no"),
        ("Low effort, founder on camera", lambda c: c["effort"] == "low" and c["founder_on_camera"] == "yes"),
        ("Original (hard to copy)", lambda c: c["origin"] == "original"),
        ("Humour", lambda c: "humour" in c["value"]),
        ("Tested or proven in real programs", lambda c: c["status"] in ("tested", "proven")),
    ]
    for title, pred in picks:
        hits = [c for c in cards if pred(c)]
        if hits:
            out.append(f"- **{title}** ({len(hits)}): " + ", ".join(link(c) for c in hits))
    out += ["", "## Funnel x value", "", "How many formats sit in each cell. Use it to spot what your plan lacks.", ""]
    values = [t["id"] for t in TAXO["dimensions"]["value"]["tags"]]
    out.append("| | " + " | ".join(label("value", v) for v in values) + " |")
    out.append("|---|" + "---|" * len(values))
    for f in ("TOFU", "MOFU", "BOFU"):
        out.append(f"| {f} | " + " | ".join(str(count(lambda c, f=f, v=v: f in c["funnel"] and v in c["value"])) for v in values) + " |")
    out += ["", "## All formats", "",
            "| ID | Format | Funnel | Value | Structure | Setup | Face | Effort | Status |",
            "|---|---|---|---|---|---|---|---|---|"]
    for c in cards:
        out.append(f"| {c['id']} | {link(c)} | {', '.join(c['funnel'])} | {', '.join(c['value'])} | {', '.join(c['structure'])} | "
                   f"{', '.join(c['setup'])} | {c['founder_on_camera']} | {c['effort']} | {c['status']} |")
    for dim in TAG_DIMS:
        d = TAXO["dimensions"][dim]
        out += ["", f"## By {dim}", "", d["question"], ""]
        for t in d["tags"]:
            hits = [c for c in cards if t["id"] in c.get(dim, [])]
            if hits:
                out.append(f"- **{t['label']}** ({len(hits)}): " + ", ".join(link(c) for c in hits))
    out.append("")
    files[LIB / "README.md"] = "\n".join(out)

    tx = [
        "# Format Library taxonomy", "",
        "Generated by `scripts/library.py build` from `taxonomy.json`. Edit the JSON, then run the script.", "",
        f"Version {TAXO['version']}, {TAXO['updated']}.", "",
        "Every card carries tags on four dimensions. A card can carry several tags per dimension, and the dimensions combine freely: "
        "a founder story can be shot as yapping in a car or as a cinematic voice-over, and work at the top or the middle of the funnel.", "",
        "Why four dimensions: one flat list of tags mixes things that answer different questions (where it works, why people share it, what happens, how it is shot). "
        "Separated, they let anyone filter by goal (BOFU), by constraint (no face, low effort) or by skill (screen recording only), and they make names systematic.", "",
        "## Naming rule", "",
        "Name = distinctive element + structure + (twist or ending). In English, short enough to search.", "",
        "- \"Smart-glasses street prank (demo at the end)\": the glasses are the distinctive element, the prank is the structure, the demo is the ending.",
        "- Same structure and setup, another topic: same card, new example.",
        "- Same structure, but a setup or an ending that changes the beats: new card.", "",
        "## Other fields", "",
    ]
    for field, vals in TAXO["fields"].items():
        tx.append(f"- **{field}**: " + "; ".join(f"{k} = {v}" for k, v in vals.items()))
    for dim in TAG_DIMS:
        d = TAXO["dimensions"][dim]
        tx += ["", f"## {dim}", "", d["question"], "", "| Tag | Label (EN) | Label (FR) | Definition | Cards |", "|---|---|---|---|---|"]
        for t in d["tags"]:
            tx.append(f"| `{t['id']}` | {t['label']} | {t['fr']} | {t['def']} | {sum(1 for c in cards if t['id'] in c.get(dim, []))} |")
    tx.append("")
    files[SKILL / "references" / "taxonomy.md"] = "\n".join(tx)
    return files


# ---------- queries ----------

def matches(c, flt):
    if "!=" in flt:
        k, v = flt.split("!=", 1)
        vals = c.get(k, [])
        vals = vals if isinstance(vals, list) else [vals]
        return not any(x in vals for x in v.split(","))
    k, _, v = flt.partition("=")
    if k == "q":
        hay = " ".join([c.get("name", ""), " ".join(c.get("aka", [])), c.get("shape", "")]).lower()
        return all(w in hay for w in v.lower().split())
    vals = c.get(k, [])
    vals = vals if isinstance(vals, list) else [vals]
    return any(x in vals for x in v.split(","))


def line(c):
    return (f"{c['id']}  {c['name']}  [{', '.join(c['funnel'])} | {', '.join(c['value'])} | "
            f"{', '.join(c['structure'])} | {', '.join(c['setup'])} | face {c['founder_on_camera']}, effort {c['effort']}, {c['status']}]")


def cmd_find(cards, filters):
    hits = [c for c in cards if all(matches(c, f) for f in filters)]
    for c in sorted(hits, key=lambda c: c["id"]):
        print(line(c))
    print(f"{len(hits)} format(s)")


def score(c):
    return STATUS_WEIGHT.get(c["status"], 1) + 0.3 * min(c["examples"], 3)


def cmd_suggest(cards, n, no_face, effort, funnels, avoid):
    pool = [c for c in cards if EFFORT_RANK.get(c["effort"], 2) <= EFFORT_RANK[effort]]
    if no_face:
        pool = [c for c in pool if c["founder_on_camera"] != "yes"]
    for a in avoid:
        pool = [c for c in pool if not matches(c, a)]
    chosen = []
    per_stage = max(1, n // (len(funnels) + 1))

    def penalty(c):
        p = 0.0
        for d in chosen:
            if set(c["structure"]) & set(d["structure"]):
                p += 1.2
            if set(c["setup"]) & set(d["setup"]):
                p += 0.4
            if set(c["value"]) == set(d["value"]):
                p += 0.3
        return p

    def pick(cands):
        cands = [c for c in cands if c not in chosen]
        if not cands:
            return None
        best = max(cands, key=lambda c: score(c) - penalty(c))
        chosen.append(best)
        return best

    for f in funnels:
        for _ in range(per_stage):
            pick([c for c in pool if f in c["funnel"]])
    if not any(c["origin"] == "original" for c in chosen):
        pick([c for c in pool if c["origin"] == "original"])
    while len(chosen) < n and pick(pool):
        pass
    print(f"Starter deck: {len(chosen)} formats (effort up to {effort}{', no face' if no_face else ''}). Shoot 2 or 3 videos per format before judging it.\n")
    for c in chosen:
        print(line(c))
        print(f"      {c['shape']}")
    stages = {f: sum(1 for c in chosen if f in c["funnel"]) for f in ("TOFU", "MOFU", "BOFU")}
    print(f"\nCoverage: {stages}; original formats: {sum(1 for c in chosen if c['origin'] == 'original')}")


def tokens(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2}


def cmd_similar(cards, target, top=6):
    ref = next((c for c in cards if c["id"].lower() == target.lower()), None)
    if ref:
        tags = set(ref["structure"]) | set(ref["setup"])
        words = tokens(ref["name"] + " " + ref["shape"])
    else:
        words = tokens(target)
        tags = {t for dim in ("structure", "setup") for t in vocab(dim) if t.replace("-", " ") in target.lower() or t in target.lower()}
    scored = []
    for c in cards:
        if ref and c["id"] == ref["id"]:
            continue
        ct = set(c["structure"]) | set(c["setup"])
        tag_sim = len(tags & ct) / len(tags | ct) if (tags | ct) else 0
        cw = tokens(c["name"] + " " + c["shape"] + " " + " ".join(c.get("aka", [])))
        word_sim = len(words & cw) / len(words | cw) if (words | cw) else 0
        scored.append((0.6 * tag_sim + 0.4 * word_sim, c))
    scored.sort(key=lambda x: -x[0])
    for s, c in scored[:top]:
        print(f"{s:.2f}  {line(c)}")
    print("Above 0.50: probably the same format, add your video as an example of that card. Below 0.30: probably a new format.")


def cmd_new(cards, name, private):
    folder, prefix = (Path(private), "P") if private else (CARDS, "F")
    folder.mkdir(parents=True, exist_ok=True)
    ids = [int(c["id"][1:]) for c in cards if c["id"].startswith(prefix)]
    new_id = f"{prefix}{(max(ids) + 1 if ids else 1):03d}"
    path = folder / f"{slugify(name)}.md"
    if path.exists():
        sys.exit(f"{path} already exists")
    if name.lower() in {c["name"].lower() for c in cards}:
        sys.exit(f"the name '{name}' is already used")
    text = TEMPLATE.read_text(encoding="utf-8")
    text = text.replace("id: F000", f"id: {new_id}").replace("Distinctive element + structure (twist or ending)", name)
    text = re.sub(r"added: \d{4}-\d{2}-\d{2}", f"added: {datetime.date.today().isoformat()}", text)
    path.write_text(text, encoding="utf-8")
    print(f"created {path} with id {new_id}. Fill every section, then run: python3 scripts/library.py lint {path}")


def cmd_gaps(cards, top):
    from collections import Counter
    s_count = Counter(t for c in cards for t in c["structure"])
    u_count = Counter(t for c in cards for t in c["setup"])
    pairs = Counter((s, u) for c in cards for s in c["structure"] for u in c["setup"])
    cands = []
    for s, ns in s_count.items():
        for u, nu in u_count.items():
            if pairs[(s, u)] == 0:
                cands.append((ns * nu, s, u))
    cands.sort(reverse=True)
    print("Structure x setup pairs that no card uses yet, most promising first (both sides are common elsewhere).")
    print("Each is a candidate original format: add a distinctive element from your company and name it.\n")
    for w, s, u in cands[:top]:
        print(f"- {label('structure', s)} x {label('setup', u)}   ({s_count[s]} cards use {s}, {u_count[u]} use {u})")


def main(argv):
    ap = argparse.ArgumentParser(description="The Format Library tool", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    sub.add_parser("check")
    p = sub.add_parser("lint"); p.add_argument("files", nargs="*")
    p = sub.add_parser("find"); p.add_argument("filters", nargs="*"); p.add_argument("--private")
    p = sub.add_parser("suggest"); p.add_argument("--n", type=int, default=8); p.add_argument("--no-face", action="store_true")
    p.add_argument("--effort", choices=["low", "medium", "high"], default="medium"); p.add_argument("--funnel", default="TOFU,MOFU,BOFU")
    p.add_argument("--avoid", action="append", default=[], help="a filter to exclude, for example value=shocking"); p.add_argument("--private")
    p = sub.add_parser("similar"); p.add_argument("target"); p.add_argument("--private")
    p = sub.add_parser("new"); p.add_argument("name"); p.add_argument("--private")
    p = sub.add_parser("gaps"); p.add_argument("--top", type=int, default=15); p.add_argument("--private")
    a = ap.parse_args(argv)

    private = getattr(a, "private", None)
    cards, errors = load_all(private)
    if a.cmd == "lint":
        names = {Path(f).name for f in a.files}
        mine = [e for e in errors if not names or any(f"/{n}:" in e for n in names)]
        for e in mine:
            print("  -", e)
        print(f"library lint: {len(mine)} problem(s) in {len(names) or len(cards)} card(s)")
        return 1 if mine else 0
    if errors and a.cmd in ("build", "check"):
        print(f"library: {len(cards)} cards, {len(errors)} problem(s)")
        for e in errors:
            print("  -", e)
        return 1
    if errors:
        print(f"(library: {len(errors)} validation problem(s); run 'lint' to see them. Results below may be incomplete.)\n", file=sys.stderr)
    if a.cmd in ("build", "check"):
        public = [c for c in cards if c["id"].startswith("F")]
        files = generated(public)
        if a.cmd == "check":
            stale = [str(p.relative_to(SKILL)) for p, t in files.items() if not p.exists() or p.read_text(encoding="utf-8") != t]
            if stale:
                print(f"library: {len(public)} cards, generated files out of date: {', '.join(stale)}. Run: python3 scripts/library.py build")
                return 1
            print(f"library: {len(public)} cards, 0 problems, generated files up to date")
            return 0
        for p, t in files.items():
            p.write_text(t, encoding="utf-8")
        print(f"library: {len(public)} cards, 0 problems; wrote library/README.md, library/index.csv, library/index.json, references/taxonomy.md")
        return 0
    if a.cmd == "find":
        cmd_find(cards, a.filters)
    elif a.cmd == "suggest":
        cmd_suggest(cards, a.n, a.no_face, a.effort, a.funnel.split(","), a.avoid)
    elif a.cmd == "similar":
        cmd_similar(cards, a.target)
    elif a.cmd == "new":
        cmd_new(cards, a.name, private)
    elif a.cmd == "gaps":
        cmd_gaps(cards, a.top)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
