# Sample case (invented)

Two invented short videos by a fictional founder, already split into units and tagged. All names, numbers and events are invented. Use it to check that the scripts run before you tag a real creator.

```
python3 -I scripts/analyze.py sample/case-00-sample/videos/01-sample-checklist 58
python3 -I scripts/analyze.py sample/case-00-sample/videos/02-sample-price 49
python3 -I scripts/aggregate_author.py sample/case-00-sample
```

Each video folder holds the files the skill asks for: meta.json, card.json, 01-blocks.md, 02-map.md, 03-loops.md and work/units-asr.tsv. The scripts add work/stats.json, 04-stats.md and the charts, and the aggregator writes 10-author-grammar.md and work/author.json at the case root.
