---
title: "Repositories and DOIs"
date: 2026-09-21
url: /opensource/repositories/
tags: ["open source", "DOI", "Zenodo", "I-Lang", "archive"]
author: "SUN"
description: "Every public repository of iLang Inc., each archived on Zenodo with a concept DOI that resolves to all versions. Fifteen repositories, all MIT, as of 21 September 2026."
---

##### Why this page exists

A repository can be rewritten; an archived release cannot. Every public repository below is archived on Zenodo, and each release since 21 September 2026 is archived automatically: a version bump in the repository's `CITATION.cff` tags the release, and the archive and its DOI follow from the release event. The **concept DOI** in the table resolves to all versions of that work, so it stays correct as the code moves.

All fifteen are MIT licensed. Versions are as of 21 September 2026.

##### The protocol

| Work | What it is | Version | Concept DOI |
|---|---|---|---|
| [ilang-spec](https://github.com/ilang-ai/ilang-spec) | The I-Lang canon: 88 verbs, two syntaxes, the v5.0 judgment layer | 4.2.0 | [10.5281/zenodo.21821452](https://doi.org/10.5281/zenodo.21821452) |
| [ilang-dict](https://github.com/ilang-ai/ilang-dict) | The complete vocabulary: verbs, modifiers, entities, declarations, plus a machine-readable table | 2.2.2 | [10.5281/zenodo.22865123](https://doi.org/10.5281/zenodo.22865123) |
| [iml-protocol](https://github.com/ilang-ai/iml-protocol) | [The machine layer](/protocol/machine-layer/): fixed-width codes for the declaration set. Experimental | 0.5.1 | [10.5281/zenodo.22823285](https://doi.org/10.5281/zenodo.22823285) |
| [ilang.ai](https://github.com/ilang-ai/ilang.ai) | The protocol website and the agent-readable layer it serves | 2.0.2 | [10.5281/zenodo.22865167](https://doi.org/10.5281/zenodo.22865167) |

##### Measurement

| Work | What it is | Version | Concept DOI |
|---|---|---|---|
| [ilang-conformance](https://github.com/ilang-ai/ilang-conformance) | 320-case deterministic conformance suite and [45 scored model runs](/datasets/ilang-conformance/) | 1.0.0 | [10.5281/zenodo.22864929](https://doi.org/10.5281/zenodo.22864929) |
| [ilang-Benchmark](https://github.com/ilang-ai/ilang-Benchmark) | Prompt benchmark harness, and the [judgment learnability study](/datasets/judgment-learnability/) | 1.0.0 | [10.5281/zenodo.22865111](https://doi.org/10.5281/zenodo.22865111) |
| [ilang-research](https://github.com/ilang-ai/ilang-research) | This site: papers, datasets and records | 1.2.0 | [10.5281/zenodo.22865165](https://doi.org/10.5281/zenodo.22865165) |

##### Agent skills and tools

| Work | What it is | Version | Concept DOI |
|---|---|---|---|
| [agent-ready-geo](https://github.com/ilang-ai/agent-ready-geo) | An agent skill that makes a website machine-readable: llms.txt, Markdown for agents, MCP, WebMCP, DNS-AID | 1.0.2 | [10.5281/zenodo.22864996](https://doi.org/10.5281/zenodo.22864996) |
| [autocode](https://github.com/ilang-ai/autocode) | 48 skills that take a spoken request through building, testing and deployment | 5.1.0 | [10.5281/zenodo.22865145](https://doi.org/10.5281/zenodo.22865145) |
| [Imprint](https://github.com/ilang-ai/Imprint) | A portable working profile that carries how you work across agents | 2.3.0 | [10.5281/zenodo.22865141](https://doi.org/10.5281/zenodo.22865141) |
| [Mem-Forever](https://github.com/ilang-ai/Mem-Forever) | A Git-native persistent memory layer for AI agents | 1.0.0 | [10.5281/zenodo.22865160](https://doi.org/10.5281/zenodo.22865160) |
| [iReview](https://github.com/ilang-ai/iReview) | AI-to-AI code review with v5.0 vector judgment instead of keyword severity | 0.2.1 | [10.5281/zenodo.22865158](https://doi.org/10.5281/zenodo.22865158) |
| [ilang-openclaw](https://github.com/ilang-ai/ilang-openclaw) | Ten instruction-only skills and two plugins for OpenClaw, Hermes and other agents | 2.3.2 | [10.5281/zenodo.22865125](https://doi.org/10.5281/zenodo.22865125) |
| [TelegramGuard](https://github.com/ilang-ai/TelegramGuard) | A Telegram group guardian whose moderation rules are protocol text, not prose | 1.0.1 | [10.5281/zenodo.22865154](https://doi.org/10.5281/zenodo.22865154) |
| [trae](https://github.com/ilang-ai/trae) | ZeroCode: Chinese-language coding skills for the Trae IDE | 2.0.3 | [10.5281/zenodo.22865151](https://doi.org/10.5281/zenodo.22865151) |

##### Citing

Cite the concept DOI when you mean the work, and a version DOI when you mean the exact state you used. Each repository carries a `CITATION.cff` with the authoritative entry.
