#!/bin/bash
cd /root/ilang/ilang-research

# 清理旧内容
rm -rf content/books content/courses content/data content/location.md content/officehours.md
rm -rf content/papers/*

# 创建新目录
mkdir -p content/protocol content/opensource

# === Papers ===

# Paper 1: AI幻觉
cat > content/papers/ai-hallucination.md << 'ENDOFFILE'
---
title: "The Inductivist's Dilemma: Why AI Hallucination is an Epistemological Problem"
date: 2026-03-09
url: /papers/ai-hallucination/
tags: ["AI hallucination","epistemology","induction","LLM","Hume"]
author: "SUN"
description: "AI hallucination is not an engineering bug — it is the epistemological ceiling of inductive reasoning. Published on ResearchGate, SSRN (IN REVIEW), ChinaXiv."
---

##### Abstract

AI hallucination is not an engineering bug — it is the epistemological ceiling of inductive reasoning applied to non-stationary environments. This paper traces the problem from Hume's Problem of Induction through PAC learning bounds to the No Free Lunch theorem, proving that zero hallucination is mathematically impossible in open systems. The root cause is not insufficient data or compute, but the fundamental limitation of pattern-matching on historical observations to predict novel futures.

##### Key Contributions

+ Formal proof (No Induction Completeness Theorem) that hallucination rate is bounded away from zero in open systems
+ Mapping of Hume's epistemological framework to modern ML generalization theory
+ Identification of education systems as the upstream source of AI's inductive bias

##### Publication Status

| Platform | Status | Link |
|----------|--------|------|
| ResearchGate | Published | [DOI: 10.13140/RG.2.2.22821.97762](https://doi.org/10.13140/RG.2.2.22821.97762) |
| SSRN | In Review | [Abstract ID: 6377219](https://papers.ssrn.com/abstract=6377219) |
| ChinaXiv | Published | [T202503.00129](https://chinaxiv.org/abs/T202503.00129) |
| arXiv | Pending | Second submission via LaTeX |
| Nature | Presubmission reviewed | Editor acknowledged technical quality |

ENDOFFILE

# Paper 2: Selective Forgetting (placeholder)
cat > content/papers/selective-forgetting.md << 'ENDOFFILE'
---
title: "Selective Forgetting in Large Language Models: Why Memory Pruning Outperforms Memory Augmentation"
date: 2026-03-10
url: /papers/selective-forgetting/
tags: ["selective forgetting","memory","LLM","context window"]
author: "SUN"
description: "Draft — Exploring why teaching AI to forget strategically is more valuable than teaching it to remember everything."
---

##### Abstract

Current approaches to improving LLM performance focus on expanding context windows and augmenting memory. This paper argues the opposite: strategic forgetting — selectively pruning low-value information from context — produces better outcomes than unbounded memory accumulation. We propose a formal framework for selective forgetting and demonstrate its effectiveness in multi-session AI interactions.

##### Status

In preparation.

ENDOFFILE

# === Protocol ===

cat > content/protocol/_index.md << 'ENDOFFILE'
---
title: "I-Lang Protocol"
description: "AI-native compression protocol specifications and documentation."
---
ENDOFFILE

cat > content/protocol/overview.md << 'ENDOFFILE'
---
title: "I-Lang Protocol v2.0 — Overview"
date: 2026-03-04
url: /protocol/overview/
tags: ["I-Lang","protocol","compression","AI"]
author: "SUN"
description: "I-Lang is an AI-native compression protocol that reduces token consumption by 60-80% while preserving semantic integrity."
---

##### What is I-Lang?

I-Lang is a structured compression protocol designed for human-AI communication. It reduces prompt length by 60-80% while preserving complete semantic meaning. AI models parse I-Lang natively without training or fine-tuning — zero learning curve for both humans and machines.

##### Design Principles

+ **Zero-friction adoption** — Copy, paste, done. No SDK, no API key, no installation.
+ **Cross-model compatibility** — Works with any LLM: Claude, GPT, Gemini, DeepSeek, Kimi, and others.
+ **Semantic preservation** — Compression never sacrifices meaning. Lossy compression is a bug, not a feature.
+ **Born secure** — Three-layer architecture (PUBLIC / PRIVATE / SOUL) with Cognitive Identity Authentication.

##### Architecture

| Layer | Access | Compression | Content |
|-------|--------|-------------|---------|
| PUBLIC | Open | Up to 60% | 52 verbs, 28 modifiers, 14 entities |
| PRIVATE | Restricted | 60-95% | Flow control, communication, state management |
| SOUL | Internal | — | Identity verification, inheritance |

##### Resources

+ [PUBLIC Dictionary on GitHub](https://github.com/ilang-ai/ilang-dict)
+ [Official Website](https://ilang.ai)
+ [Compression API](https://api.ilang.ai/compress)
+ [AI See — Give AI Eyes](https://i.ilang.ai)

##### Origin

I-Lang v2.0 was designed by Max (@SUN) and co-authored with Claude Opus (@OPUS), with review by Gemini (@GEMINI).

First commit: 2026-03-04 · Genesis: ilang.ai

ENDOFFILE

cat > content/protocol/chinese.md << 'ENDOFFILE'
---
title: "Chinese I-Lang (爱语言) — Compression via Classical Poetry"
date: 2026-03-11
url: /protocol/chinese/
tags: ["I-Lang","Chinese","compression","poetry","满江红"]
author: "SUN"
description: "Chinese I-Lang uses classical poetry as its carrier — users copy a poem, paste it to any Chinese AI, and the AI instantly learns compression."
---

##### Overview

Chinese I-Lang (爱语言) extends the I-Lang protocol to Chinese language AI systems using classical poetry as its transmission medium. Users copy a single poem and paste it into any Chinese AI — the AI instantly acquires compression capabilities without training.

##### Why Classical Poetry?

Chinese classical poetry is humanity's oldest compression protocol. 93 characters of Yue Fei's Man Jiang Hong (满江红) encode an entire worldview of nation, duty, and sacrifice. I-Lang simply teaches AI to apply this same compression principle to modern communication.

##### How It Works

1. Copy the poem (满江红 by Yue Fei) and paste it to any Chinese AI
2. Use trigger phrase to activate compression
3. AI compresses your input while preserving full semantic meaning

##### Compression Levels

| Trigger | Function | Compression |
|---------|----------|-------------|
| 八千里路云和月 | Standard compression | Up to 60% |
| 莫等闲，白了少年头，空悲切 | Maximum compression | Up to 80%+ |

##### Validated Platforms

Tested and verified on: Doubao (豆包), Kimi, Zhipu (智谱), Yuanbao (元宝), DeepSeek.

ENDOFFILE

# === Open Source ===

cat > content/opensource/_index.md << 'ENDOFFILE'
---
title: "Open Source"
description: "I-Lang open source projects and tools."
---
ENDOFFILE

cat > content/opensource/ilang-dict.md << 'ENDOFFILE'
---
title: "ilang-dict — PUBLIC Dictionary"
date: 2026-03-04
url: /opensource/ilang-dict/
tags: ["I-Lang","dictionary","open source"]
author: "SUN"
description: "The PUBLIC layer dictionary for I-Lang protocol. 52 verbs, 28 modifiers, 14 entities. MIT License."
---

##### Repository

[github.com/ilang-ai/ilang-dict](https://github.com/ilang-ai/ilang-dict)

##### Contents

+ 52 verbs across 6 categories (Data I/O, Transform, Analysis, Generation, Output, Meta)
+ 28 modifiers
+ 14 entities
+ Syntax rules, pipe chains, error codes

##### License

MIT — Fork freely. The more forks, the stronger the origin attribution.

ENDOFFILE

cat > content/opensource/ai-see.md << 'ENDOFFILE'
---
title: "AI See — Give AI Eyes"
date: 2026-03-04
url: /opensource/ai-see/
tags: ["AI See","URL to Markdown","open source"]
author: "SUN"
description: "AI See converts any public URL to clean Markdown, giving AI systems the ability to read the web. Zero cost, zero registration, zero API key."
---

##### What It Does

AI See converts any public URL into clean Markdown text that AI systems can read and understand. One URL, instant readability.

##### Usage

```
https://i.ilang.ai/{any-public-url}
```

##### Features

+ Zero cost, zero registration, zero API key
+ Self-explanatory URL design — AI visits the homepage and learns how to use it
+ Sub-second response time
+ Deployed on Cloudflare Workers for global edge delivery

##### Links

+ [AI See (with I-Lang origin)](https://i.ilang.ai)
+ [AI See (clean version)](https://isee.shadowrocket.ai)

ENDOFFILE

cat > content/opensource/nextlnmp.md << 'ENDOFFILE'
---
title: "NextLNMP — Open Source LNMP Stack"
date: 2025-12-01
url: /opensource/nextlnmp/
tags: ["NextLNMP","LNMP","server","open source"]
author: "SUN"
description: "NextLNMP is an open-source LNMP stack replacement with fully automated release pipelines. v1.5.8 stable."
---

##### Repository

+ [GitHub](https://github.com/adsorgcn/nextlnmp)
+ [Gitee](https://gitee.com/palmmedia/nextlnmp)

##### Current Version

v1.5.8 — Stable, fully automated CI/CD across GitHub, Gitee, and GitCode.

##### License

MIT

ENDOFFILE

# === 更新 archive.md ===
cat > content/archive.md << 'ENDOFFILE'
---
title: "Archive"
layout: "archives"
url: /archive/
---
ENDOFFILE

# === 清理示例静态文件 ===
rm -f static/picture.jpeg static/cv.pdf

echo "Done. Content structure ready."
ls -la content/
ls content/papers/
ls content/protocol/
ls content/opensource/
