---
title: "Judgment Calibration Dataset v1"
date: 2026-09-08
summary: "24-day longitudinal record of AI agent judgment calibration in production. 152 operator messages (41 explicit tuning instructions), 1,062 user messages, 2,162 API calls, plus a 14-day WeChat calibration log. Every figure traceable to a file."
tags: ["dataset", "alignment", "judgment", "I-Lang", "v5.0"]
author: "Long Quan Zhu"
---

## Download

The complete dataset is at [`/data/judgment-calibration-v1/`](/data/judgment-calibration-v1/).

See the [README](/data/judgment-calibration-v1/README.md) for structure, statistics, the `adopted` labeling rule, desensitization policy, and citation.

## Quick stats

- **Coverage**: Feishu bot 2026-08-15 → 2026-09-08 (24 days); WeChat bot dialogue 2026-08-09 → 2026-09-08, calibration log 2026-08-26 → 2026-09-08
- **Two production bots**: Feishu (DeepSeek-primary, 4 models by call) + WeChat Work (Claude)
- **Distinct people who talked to the bots**: 244 (Feishu) + 110 sessions (WeChat)
- **Operator messages**: 152 (Feishu, 41 explicit 🔧 tuning) + 84 directives (WeChat) = 236
- **User messages**: 1,062 (Feishu) + 533 questions (WeChat)
- **API calls with tokens and latency**: 2,162 (Feishu; 103.3M tokens in / 1.9M out; median latency 8.3 s)
- **`adopted` label**: 72 of 152 operator messages labeled by a documented lexicon rule (13 positive / 59 negative); 80 left `null` rather than guessed

## What makes this dataset unique

1. **Longitudinal, not cross-sectional** — one operator, one system, first boot to autonomous operation
2. **Natural pain signal** — "你TMD" is the negative label, not a 1–5 Likert scale
3. **Cross-model transfer** — corrections found on DeepSeek applied to Claude through policy files under the I-Lang protocol, recorded step by step
4. **Production environment** — real paying customers, real stakes, real profanity
5. **Raw and unfiltered** — grey-area requests, bot fabrications caught live, operator frustration intact
6. **Honest labels** — heuristic labels are marked as heuristic; unlabeled rows stay unlabeled

## Related papers

- [AI Hallucination and the Inductive Dilemma](/papers/ai-hallucination/)
- [Selective Forgetting](/papers/selective-forgetting/)
