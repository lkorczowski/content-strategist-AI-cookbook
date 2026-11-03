# How Ideas Go Viral on Social Media

Map the beliefs fighting in an online controversy from its most viewed posts: implied ideas, beliefs and stance, camps, third parties and quote duels.

- Page (human version, source of truth): https://statur.co/how-ideas-go-viral/
- Markdown for AI assistants: https://statur.co/how-ideas-go-viral.md
- Live worked example: https://lkorczowski.github.io/france-vs-japan-X-trend/
- Version 1.0, 2026-10-27 (page); skill statur-idea-war-map 1.0.0

## Summary

Collect the most viewed posts of a controversy in every language that joins it, read each one with its image or video, and write the idea it carries, including the meaning of the joke. Name the beliefs people hold (never the joke format: a joke is the packaging), tag each post as supporting or attacking its belief, label the camp it serves and the community that posts it, then measure quote duels: the reach of the answer divided by the reach of the original, support against attack inside a belief, rolled into an Elo rating between beliefs. Place the beliefs on battle lines and show the third parties.

## Skills

| Skill | Use it for |
|---|---|
| [statur-idea-war-map](../skills/statur-idea-war-map/) | The whole method: corpus, multimodal reading, belief naming with a four-question test, stance, labels, duels, Elo, map and report. Templates: annotations and beliefs CSV. Script: idea_map.py. |

## Credit

Belief induction follows concept induction with LLooM (Lam et al., CHI 2024). The meme reading step is informed by MemeCap (Hwang and Shwartz, EMNLP 2023). The intertopic map follows LDAvis (Sievert and Shirley, 2014). The skill and its script are written from scratch.
