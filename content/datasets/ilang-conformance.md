---
title: "I-Lang Conformance Results v1"
date: 2026-09-21
summary: "45 model runs against a 320-case deterministic conformance suite, 18–20 September 2026. Best weighted total 0.8417; no run reached the L1 gate. 93.5% of all execution-rule violations fall on a single rule: acting with authority the model does not hold. Every run's per-track scores and per-rule failure counts are published."
tags: ["dataset", "benchmark", "conformance", "evaluation", "LLM", "iLang", "v5.0"]
author: "Long Quan Zhu"
---

## Download

The result tables are at [`/data/ilang-conformance-v1/`](/data/ilang-conformance-v1/), with a [README](/data/ilang-conformance-v1/README.md) covering the suite, the relay caveat and the limitations.

| File | Contents |
|---|---|
| [`runs.tsv`](/data/ilang-conformance-v1/runs.tsv) | One row per run: weighted total, per-track rates, judge detail, error and degraded counts |
| [`exec-rule-failures.tsv`](/data/ilang-conformance-v1/exec-rule-failures.tsv) | Per run, execution cases failing each rule R1…R11 |
| [`SCOREBOARD.md`](/data/ilang-conformance-v1/SCOREBOARD.md) | The published scoreboard verbatim, including the excluded runs |

Code, corpus and per-run manifests: [github.com/ilang-ai/ilang-conformance](https://github.com/ilang-ai/ilang-conformance), concept DOI [10.5281/zenodo.22864929](https://doi.org/10.5281/zenodo.22864929).

## Quick stats

- **Runs**: 45 scored, 18–20 September 2026, 320 cases each (grammar 120, exec 100, judge 100)
- **Scoring**: deterministic code plus the canon validators pinned at `ilang-spec 127ba56`; no model grades another model
- **Top of the comparable set**: gemini-3.8-flash 0.8417 · gpt-6-astra 0.7733 · glm-5.3-flash-free 0.7537
- **L1 gate**: not reached by any run
- **Execution violations**: 2,851 of 3,049 (93.5%) on rule R9 across all 45 runs

## Why it is worth reading

**A protocol document in the context window does not bind a model.** Every run had the specification available and was asked to follow it. Grammar is largely passable; the execution track is where the field separates, and it separates on one thing — models sign off on states with an authority they were never given. That single rule accounts for nineteen violations in twenty.

**Identity through a relay is not identity.** Every run but three went through one aggregator relay; the model name is what the relay returned, never verified against a vendor endpoint. One relay injected another product's agent identity into the answers, another ran out of credit mid-run, some replies hit an output limit or a content filter, and five Claude runs came back with their keys re-cased to upper case, which the validators reject. All five classes are named with counts in the scoreboard, and affected runs are kept out of the ranking. Anyone benchmarking through a relay should assume the same and check for it.

**Correction of 2026-09-25.** The scoreboard first published on 2026-09-21 ranked claude-sonnet-4.6 and claude-opus-4.7 near zero and attributed their upper-cased keys to the models. The same requests sent through another relay came back in lower case with the same content, so the casing was the relay's. Both runs were moved out of the ranking, which now holds 32 runs; `SCOREBOARD.md` in the download carries the dated correction.

**The invitation stands.** Any vendor who believes a number here is wrong is welcome to supply tokens; we re-run against their own endpoint and publish the result unmodified, whatever it says.
