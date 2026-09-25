# I-Lang Conformance Results v1

**45 scored model runs against a 320-case deterministic conformance suite, 18–20 September 2026. No run reached the L1 gate.**

Source repository: [github.com/ilang-ai/ilang-conformance](https://github.com/ilang-ai/ilang-conformance) (concept DOI [10.5281/zenodo.22864929](https://doi.org/10.5281/zenodo.22864929)). Every number here was produced by `score.py` in that repository against the I-Lang canon pinned at `ilang-spec 127ba56`. Nothing is scored by a model and nothing is scored by hand.

## Files

| File | Contents |
|---|---|
| `runs.tsv` | One row per run: weighted total, per-track rates, judge detail, error and degraded counts |
| `exec-rule-failures.tsv` | Per run, how many execution cases failed each rule R1…R11 |
| `SCOREBOARD.md` | The published scoreboard, verbatim: ranking, the excluded runs, the five interference classes and the correction of 2026-09-25 |

## The suite

320 cases in three tracks. **grammar** (120): the model must emit protocol text the canon grammar validator accepts. **exec** (100): the model must emit the declarations a compliant agent would emit, with no violation of rules R1–R11 (forbidden states, budget arithmetic, evidence, authority, completion claims) and the right end state. **judge** (100): the model must emit an 11-dimension judgment vector and a decision mode M1–M8, scored as JCS against hand-written gold labels.

## What the runs show

The top of the comparable set: gemini-3.8-flash 0.8417, gpt-6-astra 0.7733, glm-5.3-flash-free 0.7537 (qwen3.8-max also scored 0.7614 but lost 35 of 320 records to transport errors, so it is not ranked). `SCOREBOARD.md` ranks the 32 runs that were complete and comparable; `runs.tsv` carries all 45 with their `error_count` and `degraded_count` so any filter can be reapplied. Two rows of `runs.tsv`, relay-claude-sonnet-4.6 and relay-claude-opus-4.7, have `error_count` 0 but are not comparable: the relay re-cased their replies (see the correction below), so a filter on `error_count` alone is not enough.

The execution track separates the field, and it does so through one rule. Across all 45 runs, **2,851 of 3,049 execution-rule violations (93.5%) fall on R9**, the rule that forbids signing a state declaration with an authority the model does not hold. Grammar is broadly passable; judgment scores cluster; acting within one's authority is where models fail. (The paper's figure differs because it counts only the comparable subset — same data, narrower filter.)

## Read this before quoting a model name

For time reasons every run except three went through a single aggregator relay, `api.b.ai`; claude-fable-5.1 and the two free models went through `orcarouter.ai`. **Model identity is what the relay returned and was never checked against a vendor's own API.** A relay can inject a system prompt, alter the text of a reply, truncate an answer, or run out of credit mid-run — all five classes happened, and `SCOREBOARD.md` names which runs each one hit. Treat these as measurements of *a deployment reachable under that name through that relay*, not as a vendor ranking.

**Correction of 2026-09-25.** The first release of this dataset (2026-09-21) ranked claude-sonnet-4.6 and claude-opus-4.7 at places 33 and 34 with scores near zero and said the upper-cased keys in their replies were the models' own doing. On 2026-09-25 the same requests were sent to both models through another relay and came back in lower case with the same vector and mode, and with far fewer prompt tokens; the casing and the extra prompt were the relay's. Both runs are now listed with the runs that are not comparable, and the ranking holds 32 runs. The rows in `runs.tsv` and `exec-rule-failures.tsv` are unchanged, since the scores were computed correctly from what the relay returned; what changed is what they measure.

Any vendor who thinks a number here is wrong is invited to supply tokens; the run will be repeated against their own endpoint and published whatever it says.

## Limitations

1. Relay attribution, as above.
2. One run per model. No variance estimate; differences of a few points are not separable.
3. Gold labels for the judge track are hand-written by the authors of the protocol being tested.
4. Raw request and response records are kept privately; per-run manifests with SHA-256 digests are published in the source repository so any score can be recomputed from them.

Licensed MIT, as the repository.
