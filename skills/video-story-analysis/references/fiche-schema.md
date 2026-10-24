# Fiche data format (06-fiche.json and 05-graph.json)

The Fiche page is built from `06-fiche.json` plus `work/stats.json`, `01-blocks.md`, `03-loops.md`, `05-graph.json`, `07-seed.yaml` (optional, to count moves) and the SVGs. Keep every field; the replication skill reads `abilities`, `feats`, `equipment`, `flaws` and `formula`.

## 06-fiche.json

```json
{
  "fiche_version": "1.0",
  "case": "case-slug",
  "page_title": "Story Fiche",
  "eyebrow": "FICHE · STORY ANALYSIS",
  "identity": {
    "title": "original title", "creator": "channel name",
    "platforms": {"youtube": {"id": "", "published": "YYYY-MM-DD", "views_d7": 0, "comments": 0, "subscribers": 0},
                  "tiktok": {"id": "", "published": "", "plays_d7": 0, "likes": 0, "saves": 0, "shares": 0, "comments": 0, "followers": 0}},
    "runtime_s": 0, "language": "en", "niche": "", "format": "one line: voice-over, host on camera, clips, cards..."
  },
  "class": {"name": "a role-playing class that fits the storytelling role", "why": "one data-grounded line"},
  "background": {"name": "", "why": ""},
  "alignment": {"name": "", "why": ""},
  "formula": "one sentence that explains the whole video's design",
  "abilities": [{"code": "CUR", "name": "Curiosity", "score": 0, "evidence": "numbers from stats", "metric_keys": ["loops.count"]}],
  "custom_axes_example": {"axes": [{"name": "", "formula": "", "score": 0}]},
  "feats": [{"name": "", "how": "imperative, reusable on any subject", "where": "unit or block ids"}],
  "equipment": ["assets the format needs, with shares"],
  "flaws": ["weak spots, factual issues, dependencies"],
  "audience_signals": ["what the public reacted to, by mechanism"],
  "notes": {
    "structure": "optional: what the dashed arcs of the graph show in this video",
    "braid": "optional: which stretches are the riskiest and what carries them",
    "edit": "optional: what depends on the edit (host on camera share, payoffs carried by clips)",
    "method": "optional: how the material was acquired (transcript source, frames sampled, comments read)"
  }
}
```

`page_title` and `eyebrow` are optional; the page falls back to "Story Fiche" and "FICHE · STORY ANALYSIS". Empty platform blocks are skipped. Each `notes` field replaces a generic sentence on the page; leave it out to keep the generic one.

## 05-graph.json

```json
{
  "threads": {"S": {"label": "Story: the startup's first six months", "share": 0.0, "objectives": ["MOVE", "RETAIN"]},
              "L": {"label": "Lesson: onboarding explained", "share": 0.0, "objectives": ["TEACH", "TRUST"]},
              "A": {"label": "Audience: your own product", "share": 0.0, "objectives": ["ACT"]},
              "H": {"label": "Host: the creator as a character", "share": 0.0, "objectives": ["BRAND"]},
              "X": {"label": "Channel", "share": 0.0, "objectives": ["GROW"]}},
  "nodes": [{"id": "S0", "thr": "S", "blk": "B00", "t": "00:00", "when": "relaunch day (told first)", "label": "short label", "obj": ["RETAIN"]}],
  "edges": [{"from": "S2", "to": "L1", "type": "proves", "note": "a few words"}],
  "chronology": [{"order_told": 1, "real": "relaunch day", "label": "the day from the opening", "short": "1. relaunch"}],
  "real_order": ["first launch", "month 2", "relaunch day"]
}
```

Edge types: `proves` (a story node illustrates a lesson node), `pays` (a later node pays a plant), `leads` (reading order). `real_order` lists every distinct `real` value of `chronology` in the order the events happened; without it, the chronology chart keeps the order in which the values first appear.

## Class ideas

Classes from tabletop role-playing games, picked by the creator's main storytelling role: Bard (lore keeper) tells others' legends to teach; Wizard explains systems from first principles; Rogue reveals hidden mechanics and scandals; Paladin argues a moral case; Ranger guides through a territory (travel, field reports); Warlock trades on a single obsession; Fighter drills technique; Druid connects to nature and cycles; Cleric preaches a doctrine; Barbarian sells pure energy and rants; Monk teaches discipline in minimal form; Sorcerer runs on raw personal charisma.
