# How Ideas Go Viral on Social Media

Map the ideas fighting in an online controversy from its most viewed posts: implied ideas, contested concepts, camps, third parties and quote duels.

- Page (human version, source of truth): https://statur.co/how-ideas-go-viral/
- Markdown for AI assistants: https://statur.co/how-ideas-go-viral.md
- Live worked example: https://lkorczowski.github.io/france-vs-japan-X-trend/
- Version 1.0, 2026-10-27 (page); skill statur-idea-war-map 1.0.0

## Summary

Collect the most viewed posts of a controversy in every language that joins it, read each one with its image or video, and write the idea it carries, including the meaning of the joke. Induce the contested concepts from the posts, label the camp each idea serves and the community that posts it, then measure quote duels: the reach of the answer divided by the reach of the original, rolled into an Elo rating per concept. Place the concepts on battle lines and show the third parties.

## Skills

| Skill | Use it for |
|---|---|
| [statur-idea-war-map](../skills/statur-idea-war-map/) | The whole method: corpus, multimodal reading, concept induction, labels, duels, Elo, map and report. Templates: annotations and concepts CSV. Script: idea_map.py. |

## Credit

Concept induction follows LLooM (Lam et al., CHI 2024). The meme reading step is informed by MemeCap (Hwang and Shwartz, EMNLP 2023). The intertopic map follows LDAvis (Sievert and Shirley, 2014). The skill and its script are written from scratch.
