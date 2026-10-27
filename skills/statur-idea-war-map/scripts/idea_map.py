"""Idea war map: reach, camp shares, quote duels and Elo per concept.

Usage: python3 idea_map.py annotations.csv concepts.csv [--out map.json] [--main FR,JA]
Standard library only. Columns: see templates/annotations.csv and templates/concepts.csv.
"""
import argparse, csv, json
from collections import Counter, defaultdict

ap = argparse.ArgumentParser()
ap.add_argument("annotations"); ap.add_argument("concepts")
ap.add_argument("--out", default="map.json")
ap.add_argument("--main", default="", help="communities of the main camps, comma separated (default: the two largest)")
a = ap.parse_args()

rows = list(csv.DictReader(open(a.annotations, encoding="utf-8")))
labels = {r["id"]: r["label"] for r in csv.DictReader(open(a.concepts, encoding="utf-8"))}
by_id = {r["id"]: r for r in rows}
for r in rows:
    r["views"] = int(float(r["views"] or 0))

comm = Counter()
for r in rows:
    comm[r["community"]] += r["views"]
main = [c for c in a.main.split(",") if c] or [c for c, _ in comm.most_common(2)]
total = sum(comm.values()) or 1

concepts = {}
for cid, label in labels.items():
    rs = [r for r in rows if r["concept"] == cid]
    side = Counter()
    for r in rs:
        side[r["side"]] += r["views"]
    concepts[cid] = {"id": cid, "label": label, "posts": len(rs), "views": sum(r["views"] for r in rs),
                     "side_views": dict(side), "elo": 1500.0, "wins": 0, "losses": 0}

duels = []
for r in sorted(rows, key=lambda r: (r["date"], r["id"])):
    p = by_id.get(r.get("parent_id") or "")
    if not p or r.get("rel") != "rebut" or not p["views"]:
        continue
    ratio = r["views"] / p["views"]
    duels.append({"original": p["id"], "answer": r["id"], "ratio": round(ratio, 3),
                  "original_concept": p["concept"], "answer_concept": r["concept"]})
    ca, cb = concepts.get(r["concept"]), concepts.get(p["concept"])
    if ca and cb and ca is not cb:
        expected = 1 / (1 + 10 ** ((cb["elo"] - ca["elo"]) / 400))
        score = 1.0 if ratio > 1 else 0.0
        ca["elo"] += 32 * (score - expected); cb["elo"] -= 32 * (score - expected)
        (ca if score else cb)["wins"] += 1; (cb if score else ca)["losses"] += 1

for c in concepts.values():
    c["elo"] = round(c["elo"])
out = {"posts": len(rows), "views": total, "main_camps": main,
       "third_party_share": round(sum(v for k, v in comm.items() if k not in main) / total, 3),
       "communities": dict(comm.most_common()),
       "concepts": sorted(concepts.values(), key=lambda c: -c["views"]),
       "duels": sorted(duels, key=lambda d: -d["ratio"])}
json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(rows)} posts, {total:,} views, third parties {out['third_party_share']:.0%}, {len(duels)} duels -> {a.out}")
for c in out["concepts"][:10]:
    print(f"  {c['id']} {c['label'][:34]:<34} {c['views']:>12,} views  Elo {c['elo']}  {c['wins']}-{c['losses']}")
