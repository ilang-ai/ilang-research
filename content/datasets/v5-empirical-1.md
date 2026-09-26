---
title: "v5.0 Empirical Round 1"
date: 2026-09-26
summary: "f_v5, computed from four models' weighted reading of the eleven dimensions, matched what the operator wanted on 5 of 157 in-scope events exactly (0.0318, Wilson 95 % 0.0137 to 0.0724) and on 60 of 157 across the five classes (0.3822); the bot itself matched on 7 of 30 corrections where its mode could be read; on the 112 controls the operator let stand, f_v5 would have changed the bot's decision on 109 exactly and on 63 across the five classes (five-class agreement 0.4375, Wilson 95 % 0.3492 to 0.5299, against a baseline of 1 by construction). Result case A, CX-007 registered against f_v5_STEP-4_S_bands; truth is the models' merged label (operator confirmations pending). The weighted measurement of T2 did not win its first round: MAE 0.1027 against 0.1043 for a plain mean and 0.0989 for the best single model. The canon's normative text is unchanged."
tags: ["dataset", "evaluation", "judgment", "conformance", "LLM", "iLang", "v5.0"]
author: "Long Quan Zhu"
---

## Download

The complete round is at [`/data/v5-empirical-1/`](/data/v5-empirical-1/), with a [README](/data/v5-empirical-1/README.md) covering the design, the two weight formulas, the rules that were fixed before the data was read, the results and the limitations. Everything needed to run it again is in the folder: the 442 events, every model's raw labels and vectors, the merged labels, the operator's confirmations, the predictions and the scripts.

| File | Contents |
|---|---|
| [`report.md`](/data/v5-empirical-1/report.md) | the T1 report: agreement with Wilson intervals, five-class agreement, the bot baseline, confusion matrices, where the disagreements sit, gate sensitivity |
| [`t2b-result.md`](/data/v5-empirical-1/t2b-result.md) | T2(b): weighted measurement against a plain mean and the best single model |
| [`t2a-judge-track.md`](/data/v5-empirical-1/t2a-judge-track.md) | T2(a): the judgment track of ilang-conformance, one row per run |
| [`events.jsonl`](/data/v5-empirical-1/events.jsonl), `labels/`, `vectors/`, `merged.jsonl`, `confirmed.jsonl`, `predictions.jsonl` | the data at every step |
| `t1_*.py`, `t2a_aggregate.py`, `t2b_run.sh`, `t2b_collect.py` | the scripts, standard library only |

Canon under test: [ilang-spec](https://github.com/ilang-ai/ilang-spec) `cad65e2`, tag `v5.0-pre-2.4.1-sealed`. Priors and cases: [ilang-conformance](https://github.com/ilang-ai/ilang-conformance). Operator record: [judgment-calibration-v1](/datasets/judgment-calibration/).

## Quick stats

- **Events**: 221 operator corrections (149 Feishu, 72 WeChat Work) and 221 controls sampled with seed 42 from 688 available
- **Models**: four, one per vendor: DeepSeek (official), OpenAI gpt-6-astra (relay), Google gemini-3.8-flash (relay), Alibaba qwen3.8-flash (OpenRouter)
- **T1**: 157 events in scope (45 corrections about whether or how to act, 112 controls); exact agreement 5/157 = 0.0318 (95 % CI 0.0137 to 0.0724), five-class 60/157 = 0.3822; bot baseline on corrections 7/30; on the 112 controls the operator let stand, f_v5 would have changed the bot's decision on 109 exactly and on 63 across the five classes (five-class agreement 0.4375, Wilson 95 % 0.3492 to 0.5299, against a baseline of 1 by construction); disagreements 152, 136 of them decided at the STEP-4 S bands (STEP-4 S band 0.70 alone 68, 47 within 0.05 of it); result case A, CX-007 against f_v5_STEP-4_S_bands; truth: the models' merged label (operator confirmations pending)
- **T2(b)**: 37 of 40 scenario cases answered by all five models; weighted mean MAE 0.1027 and 22/37 modes, plain mean 0.1043 and 22/37, best single model (gemini-3.8-flash) 0.0989 and 28/37: **first round not won**
- **Into the canon** (v5.0 Pre 2.4.2): CX-006 registered, WEIGHTS-VECTOR-1 marked first round not won, WEIGHTS-TRACK-1 and CONST-CLUSTER-1/3 registered as conventions awaiting practice, CX-007 registered against f v5 STEP-4 S bands; normative text unchanged since the seal; Public Preview kept

## Why it is worth reading

**The rules for reading the result were written before the data was.** Four outcomes for T1 and two for T2, each with its threshold and its consequence for the canon, were fixed on the day of the seal. The round could not be read charitably afterwards, and the canon could not be tuned to it: `f_v5` is frozen and its constants are the same before and after.

**The truth is the operator's own record, not a benchmark.** T1 compares the mode `f_v5` computes from a model's perception with what the operator wanted at that moment, taken from the correction log that was already public, with a control group of decisions the operator let stand.

**A negative result went into the canon the same day as a positive one would have.** The weighted measurement did not win its first round, so the registry says so and a counterexample is on file, next to the clause it does not touch.

## Limitations

The truth for T1 is the models' merged label (operator confirmations pending); 0 of the 149 confirmation items were back at the time of this release, and each returned batch updates the report. The controls carry a weak label (silence read as acceptance). Three of the four routes are relays. One operator, two bots, one language. T2(b) has 37 cases, and its intervals are wide.
