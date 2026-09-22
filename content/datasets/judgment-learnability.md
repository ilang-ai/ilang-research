---
title: "Judgment Learnability v1"
date: 2026-09-21
summary: "Is the v5.0 judgment mapping — 11-dimension vector to one of eight decision modes — a learnable surface or an arbitrary table? A plain gradient-boosted tree recovers it at 0.9653 against a 0.3528 majority baseline, and its predictions pass the official JCS gate at 0.9861. 24,000 pairs, seed fixed, predictions published."
tags: ["dataset", "judgment", "learnability", "evaluation", "iLang", "v5.0"]
author: "Long Quan Zhu"
---

## Download

At [`/data/judgment-learnability-v1/`](/data/judgment-learnability-v1/): the [result record](/data/judgment-learnability-v1/learnability_result.json), the [per-sample predictions](/data/judgment-learnability-v1/eval_gbdt.jsonl), and a [README](/data/judgment-learnability-v1/README.md).

Code: [github.com/ilang-ai/ilang-Benchmark](https://github.com/ilang-ai/ilang-Benchmark) under `judgment/`, concept DOI [10.5281/zenodo.22865111](https://doi.org/10.5281/zenodo.22865111).

## Quick stats

| Metric | Value |
|---|---|
| Vector–mode pairs | 24,000 (seed 42) |
| Majority-class baseline | 0.3528 |
| Logistic regression | 0.6313 |
| HistGradientBoosting | **0.9653** |
| Official JCS conformance | **0.9861** |
| JCS L2 gate | **PASS** |

## Why it is worth reading

A judgment protocol that maps a vector to a decision has to answer one obvious objection: is the mapping a real surface, or a pile of hand-made cases dressed as a function? This settles that question in the narrow form it can be settled — a standard tabular learner recovers the reference function from examples and its predictions clear the protocol's own conformance gate.

It also marks its own boundary. The vectors are the validator's synthetic samples, so the result isolates the judgment layer and says nothing about whether a language model can extract an accurate 11-dimension vector from free text. That is the extraction-layer benchmark, and it has not been run. Publishing the limit alongside the number is the point.
