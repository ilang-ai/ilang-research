# Judgment Learnability v1

**Is the I-Lang v5.0 judgment mapping — 11-dimension vector to one of eight decision modes — a learnable decision surface, or an arbitrary table? A plain gradient-boosted tree recovers it at 0.9653 against a 0.3528 majority baseline, and its predictions pass the official JCS gate at 0.9861.**

Source repository: [github.com/ilang-ai/ilang-Benchmark](https://github.com/ilang-ai/ilang-Benchmark) (concept DOI [10.5281/zenodo.22865111](https://doi.org/10.5281/zenodo.22865111)), directory `judgment/`.

## Files

| File | Contents |
|---|---|
| `learnability_result.json` | The result record: sample size, seed, mode distribution, three accuracies, the JCS score and gate verdict |
| `eval_gbdt.jsonl` | Per-sample predictions from the evaluated model |

## The numbers

| Metric | Value |
|---|---|
| Vector–mode pairs | 24,000 (seed 42) |
| Majority-class baseline | 0.3528 |
| Logistic regression | 0.6313 |
| HistGradientBoosting | **0.9653** |
| Lift over baseline | +0.6125 |
| Official JCS conformance | **0.9861** |
| JCS L2 gate | **PASS** |

## What it proves, and what it does not

**Proves:** the reference function `f_v5` is well formed and learnable. A standard tabular learner recovers it from examples and its predictions clear the protocol's own conformance gate. The mapping is a surface, not a lookup table of special cases.

**Does not prove:** that a language model can extract accurate 11-dimension vectors from free text. The vectors here are the validator's synthetic samples, by design — the study isolates the judgment layer from the extraction layer. The extraction side is a separate benchmark that has not been run.

The scoring validator is a version-locked copy of `ilang_judge_validator.py` from `ilang-ai/ilang-spec`.

## Note on the parent repository

`ilang-Benchmark` also contains a 30-case compression harness. Its previously published report was generated with a mock model as a pipeline smoke test, and citing those numbers as evidence was wrong; the report was withdrawn and the mock outputs archived under a label that says so. Only the judgment-layer result above rests on real computation, which is why it is the only part mirrored here.

Licensed MIT, as the repository.
