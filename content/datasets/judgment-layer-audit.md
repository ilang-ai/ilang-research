---
title: "Judgment Layer Audit v1"
date: 2026-09-21
summary: "Three days of a production agent's messages judged twice — by a cheap always-on judge model and by the operator's written rules. 7,940 messages judged, 2,648 scored against the reference. Agreement 68.4% → 75.1% → 80.9%; 87.2% in the judge's top confidence band. Includes a worked correction: the rule-compliance gain everyone would have quoted, 69 → 7, is 13 → 7 once both days are measured with the same criterion."
tags: ["dataset", "LLM-as-a-judge", "judgment", "evaluation", "iLang", "v5.0"]
author: "Long Quan Zhu"
---

## Download

The dataset is at [`/data/judgment-layer-audit-v1/`](/data/judgment-layer-audit-v1/): four tab-separated files plus a [README](/data/judgment-layer-audit-v1/README.md) covering method, sampling, desensitization and limitations.

| File | Contents |
|---|---|
| [`totals.tsv`](/data/judgment-layer-audit-v1/totals.tsv) | Per-day volume, latency, tokens, cost |
| [`agreement.tsv`](/data/judgment-layer-audit-v1/agreement.tsv) | Agreement by stratum and by confidence band |
| [`confusion-matrix.tsv`](/data/judgment-layer-audit-v1/confusion-matrix.tsv) | All 45 judge → reference branch pairs, per day |
| [`rule-deviations.tsv`](/data/judgment-layer-audit-v1/rule-deviations.tsv) | Deviations per rule per day, under both criteria |

## Quick stats

- **Coverage**: 2026-09-18 → 2026-09-20, one production community agent, Asia/Shanghai calendar days
- **Judged**: 7,940 messages (operator's own 16 excluded), mean latency 0.590 / 0.612 / 0.623 s
- **Scored against the reference**: 2,648 (900 / 848 / 900; candidates all scored plus 15% random, seed = day, capped at 900)
- **Agreement, unbiased random sample**: 68.4% → 75.1% → 80.9%
- **Agreement by judge confidence** (three days pooled): 87.2% at ≥ 0.85, 57.9% from 0.5 to 0.85, 38.4% below 0.5
- **Cost of judging everything**: $0.5514 at the deployment's own price constant; the reference side's dollar cost is absent because no price constant exists on that machine

## Why it is worth reading

**A cheap judge's confidence is a usable signal.** Pooled over three days, the judge agrees with the rules 87.2% of the time when it claims confidence ≥ 0.85, and 38.4% of the time when it claims below 0.5. That gap is what makes selective review affordable: audit the bottom band, trust the top.

**It has a known direction of error.** Every one of its three largest disagreements — reading finished work, a request to be handed the answer, or plain chitchat as "this person is stuck" — points toward the same branch. A judge deployed where a miss is expensive learns to over-call the expensive branch, and its output then overstates that branch's true frequency.

**It contains a correction we could have quietly skipped.** The criterion that decides whether the agent obeyed a rule was edited mid-window, on 2026-09-20. The daily reports showed deviations on one rule going 69 → 7 across that edit. Measured with one criterion the change is 13 → 7; with the old criterion throughout it is 69 → 50. The improvement is real and roughly half the size of the headline. Both series ship in `rule-deviations.tsv` so the difference can be checked rather than believed.

## What is not in it

Message text, the rule texts, the per-message rows and the internal rule identifiers. Rules appear as `R01`…`R16`. This release publishes counts only — enough to recompute every figure above, and nothing a member of that community wrote.
