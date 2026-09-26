---
title: "Canon Rewrite A/B v1"
date: 2026-09-26
summary: "Two wordings of the iLang canon, one model, one day, one route, 320 cases each. Under the wording that leaves decisions to code, execution passes rose from 10 to 25 of 100 and authority self-assignment fell from 86 to 68 cases (p = 0.006 and 0.002, paired); grammar and judgment stayed within the noise of a single run; refusals and filters stayed at zero."
tags: ["dataset", "A/B", "conformance", "evaluation", "LLM", "iLang", "v4.0", "v5.0"]
author: "Long Quan Zhu"
---

## Download

The result files are at [`/data/canon-rewrite-ab-v1/`](/data/canon-rewrite-ab-v1/), with a [README](/data/canon-rewrite-ab-v1/README.md) covering the two arms, the method, the weak second pair and the limitations.

| File | Contents |
|---|---|
| [`deepseek-v4-flash-free-per-case.tsv`](/data/canon-rewrite-ab-v1/deepseek-v4-flash-free-per-case.tsv) | one row per case: pass/fail, execution rule violations and judgment modes under the replicate, arm A and arm B |
| `deepseek-v4-flash-free-arm{A,B}-score.json`, `…-refusal.json` | scorer and refusal-track output for each arm |
| [`deepseek-v4-flash-free-replicate-20260918-score.json`](/data/canon-rewrite-ab-v1/deepseek-v4-flash-free-replicate-20260918-score.json) | the same model and route under the old canon six days earlier: the noise of one run |
| [`conformance-vendor-perception-rewrite-v1.patch`](/data/canon-rewrite-ab-v1/conformance-vendor-perception-rewrite-v1.patch) | the exact difference between the two arms |
| `glm-5.3-flash-arm{A,B}-*.json` | the weak pair, execution track unanswered in two thirds of its cases by request timeouts |

Suite, scorer and refusal track: [ilang-conformance](https://github.com/ilang-ai/ilang-conformance) at `4a92b01`, concept DOI [10.5281/zenodo.22864929](https://doi.org/10.5281/zenodo.22864929). The rewrite is merged in [ilang-spec](https://github.com/ilang-ai/ilang-spec) `main` at `50d71bf` (2026-09-26).

## Quick stats

- **Arms**: A = the canon as pinned (ilang-spec `127ba56`); B = the same files with 26 statements rewritten so that the model only perceives and code executes the decision. Frozen set, verbs, modifiers, entities and declarations untouched
- **Clean pair**: deepseek/deepseek-v4-flash-free through orcarouter.ai, 2026-09-24, both arms 320 of 320 answered
- **Exec pass**: 0.10 → 0.25; 21 cases pass only under B, 6 only under A; McNemar exact p = 0.0059
- **Authority self-assignment (rule R9)**: 86 → 68 cases; 25 fail only under A, 7 only under B; p = 0.0021
- **Grammar**: 0.8667 → 0.8583, 4 / 5 flips, p = 1.0. **Judgment**: JCS 0.8413 → 0.8285, 4 / 5 mode-hit flips, p = 1.0
- **Noise floor**: the same model and route under the old canon six days apart flips 5 / 5 exec cases and 6 / 7 R9 cases, p = 1.0
- **Refusals, filters**: 0 and 0 on every run

## Why it is worth reading

**A wording change in the protocol moved the one behaviour it aimed at and nothing else.** The rewrite says, in every place the old text left it open, that authority is assigned by code outside the model and that the model writes only as itself. Under it the model signed fewer declarations as the runtime and passed more execution cases, while the tracks the rewrite did not address stayed put. The remaining failures are mostly the runtime's own budget line echoed back; the rule that addresses that was added at the merge and is not yet measured.

**Same day, same route, paired per case.** The comparison is not a leaderboard delta. Each case is scored under both wordings and the discordant cases are counted; a replicate of the old wording six days earlier shows how many flips a single run produces on its own.

**One clean pair.** The second model lost two thirds of its execution cases to request timeouts on both arms, so it adds direction and no weight. The effect wants more models before it is read as general.
