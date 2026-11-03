"""Belief war map: reach, camp shares, stance, quote duels and Elo per belief.

Usage: python3 idea_map.py annotations.csv beliefs.csv [--out map.json] [--main FR,JA]
Standard library only. Columns: see templates/annotations.csv and templates/beliefs.csv.
A belief is what people believe ("The Japanese are suicidal"); the register (humor, argument...) is its packaging.
Duels inside one belief count support against attack. Duels between two beliefs feed the Elo.
Beliefs with an empty owner (X01...) hold posts with no belief and get no Elo.
"""
import argparse, csv, json
from collections import Counter, defaultdict

ap = argparse.ArgumentParser()
ap.add_argument("annotations"); ap.add_argument("beliefs")
ap.add_argument("--out", default="map.json")
ap.add_argument("--main", default="", help="communities of the main camps, comma separated (default: the two largest)")
a = ap.parse_args()

rows = list(csv.DictReader(open(a.annotations, encoding="utf-8")))
brows = list(csv.DictReader(open(a.beliefs, encoding="utf-8")))
labels = {r["id"]: r["label"] for r in brows}
rope = {r["id"]: bool((r.get("owner") or "").strip()) for r in brows}
by_id = {r["id"]: r for r in rows}
for r in rows:
    r["views"] = int(float(r["views"] or 0))
    r["belief"] = r.get("belief") or r.get("concept", "")  # 1.0 files used "concept"
    r["stance"] = (r.get("stance") or "neutral").strip()

comm = Counter()
for r in rows:
    comm[r["community"]] += r["views"]
main = [c for c in a.main.split(",") if c] or [c for c, _ in comm.most_common(2)]
total = sum(comm.values()) or 1

beliefs = {}
for cid, label in labels.items():
    rs = [r for r in rows if r["belief"] == cid]
    side, stance = Counter(), Counter()
    for r in rs:
        side[r["side"]] += r["views"]
        stance[r["stance"]] += r["views"]
    beliefs[cid] = {"id": cid, "label": label, "rope": rope[cid], "posts": len(rs), "views": sum(r["views"] for r in rs),
                    "side_views": dict(side), "stance_views": dict(stance), "elo": 1500.0, "wins": 0, "losses": 0,
                    "inner": {"attack_wins": 0, "support_wins": 0}}

duels = []
for r in sorted(rows, key=lambda r: (r["date"], r["id"])):
    p = by_id.get(r.get("parent_id") or "")
    if not p or r.get("rel") != "rebut" or not p["views"]:
        continue
    ratio = r["views"] / p["views"]
    duels.append({"original": p["id"], "answer": r["id"], "ratio": round(ratio, 3),
                  "original_belief": p["belief"], "answer_belief": r["belief"]})
    ca, cb = beliefs.get(r["belief"]), beliefs.get(p["belief"])
    if ca and ca is cb and {r["stance"], p["stance"]} == {"supports", "attacks"}:
        winner = r if ratio > 1 else p
        ca["inner"]["attack_wins" if winner["stance"] == "attacks" else "support_wins"] += 1
    if ca and cb and ca is not cb and ca["rope"] and cb["rope"]:
        expected = 1 / (1 + 10 ** ((cb["elo"] - ca["elo"]) / 400))
        score = 1.0 if ratio > 1 else 0.0
        ca["elo"] += 32 * (score - expected); cb["elo"] -= 32 * (score - expected)
        (ca if score else cb)["wins"] += 1; (cb if score else ca)["losses"] += 1

for c in beliefs.values():
    c["elo"] = round(c["elo"])
out = {"posts": len(rows), "views": total, "main_camps": main,
       "third_party_share": round(sum(v for k, v in comm.items() if k not in main) / total, 3),
       "communities": dict(comm.most_common()),
       "beliefs": sorted(beliefs.values(), key=lambda c: -c["views"]),
       "duels": sorted(duels, key=lambda d: -d["ratio"])}
json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(rows)} posts, {total:,} views, third parties {out['third_party_share']:.0%}, {len(duels)} duels -> {a.out}")
for c in out["beliefs"][:10]:
    sv = c["stance_views"]
    print(f"  {c['id']} {c['label'][:40]:<40} {c['views']:>12,} views  supports {sv.get('supports', 0):,} attacks {sv.get('attacks', 0):,}  Elo {c['elo']} {c['wins']}-{c['losses']}  inner {c['inner']}")
