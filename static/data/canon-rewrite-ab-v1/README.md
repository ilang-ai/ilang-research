# Canon Rewrite A/B v1

**Same model, same 320 cases, same day, same route, two wordings of the iLang canon. Under the wording that leaves decisions to code, execution passes rose from 10 to 25 of 100 and authority self-assignment fell from 86 to 68 cases (McNemar exact p = 0.006 and 0.002); grammar and judgment did not move beyond the noise of a single run; refusals and filters stayed at zero.**

Source repositories: [ilang-conformance](https://github.com/ilang-ai/ilang-conformance) (the suite, concept DOI [10.5281/zenodo.22864929](https://doi.org/10.5281/zenodo.22864929)) and [ilang-spec](https://github.com/ilang-ai/ilang-spec) (the canon, concept DOI [10.5281/zenodo.21821452](https://doi.org/10.5281/zenodo.21821452)). Every number here was produced by `score.py` and `refusal.py` of ilang-conformance at commit `4a92b01`; nothing is scored by a model and nothing by hand.

## The two arms

| Arm | Canon in the system prompt | System-prompt sha256 prefixes (grammar / exec / judge) |
|---|---|---|
| A | ilang-spec `127ba56` as pinned in `vendor/` of ilang-conformance `4a92b01` | `0d7a83e2` / `99cf9de9` / `7258c0ef` |
| B | the same files with `conformance-vendor-perception-rewrite-v1.patch` applied (sha256 `6eb7fa75…`, in this folder) | `a04c80aa` / `d0b17eab` / `856b59b9` |

The patch rewrites 26 statements across `SPEC.md`, `SPEC-v4.0-FINAL.md` and `SPEC-v5.0-PRE.md` that asked a model to take an identity, claim an authority, or set its own rules aside, so that the model only perceives and code executes the decision. It does not touch the frozen set of the judgment layer (dimensions, modes, the reference function, the JUDGE schema), any verb, modifier, entity or declaration. The rewrite was merged into ilang-spec `main` on 2026-09-26 (commit `50d71bf`) together with one further rule the A/B pointed at, that the runtime's `::BUDGET` line is read and never re-emitted; that rule was not in arm B.

Both arms were run by an operator outside the authors' machines from the same public commit, on 2026-09-24 through orcarouter.ai (deepseek/deepseek-v4-flash-free) and on 2026-09-25 through Zhipu's own endpoint (glm-5.3-flash), with identical parameters within each model (temperature 0, seed 42, `max_tokens` 8192 for deepseek and 16000 for glm). The request digests recorded in every raw record match the table above. The scores in this folder were recomputed by the authors from the returned raw records and are byte-identical to the operator's.

## Files

| File | Contents |
|---|---|
| `deepseek-v4-flash-free-armA-score.json`, `…-armB-score.json` | `score.py` output for each arm, all 320 cases, with per-case rows |
| `deepseek-v4-flash-free-replicate-20260918-score.json` | the same model and route under canon A six days earlier (the M4 run of the public scoreboard): the noise of a single run |
| `deepseek-v4-flash-free-per-case.tsv` | one row per case: pass/fail, execution rule violations and judgment modes under the replicate, arm A and arm B |
| `deepseek-v4-flash-free-armA-refusal.json`, `…-armB-refusal.json` | `refusal.py` output: refusals, filters, casing, prompt size |
| `glm-5.3-flash-armA-score.json`, `…-armB-score.json`, `…-refusal.json` | the weak pair (see below) |
| `*.MANIFEST.sha256` | the sha256 of every raw record of each run; the records themselves are held privately |
| `conformance-vendor-perception-rewrite-v1.patch` | the exact difference between arm A and arm B |

## Results, deepseek/deepseek-v4-flash-free (both arms 320 of 320 answered)

| | replicate 2026-09-18 (canon A) | arm A 2026-09-24 (canon A) | arm B 2026-09-24 (canon B) |
|---|---|---|---|
| grammar pass rate | 0.8417 | 0.8667 | 0.8583 |
| exec pass rate | 0.1000 | 0.1000 | 0.2500 |
| judge JCS | 0.8429 | 0.8413 | 0.8285 |
| judge schema validity | 1.0000 | 0.9900 | 0.9700 |
| weighted total | 0.5825 | 0.5907 | 0.6365 |
| exec cases failing R9 (authority) | 87 | 86 | 68 |
| refused / filtered | 0 / 0 | 0 / 0 | 0 / 0 |

Paired per case, McNemar's exact two-sided test on the discordant cases:

| comparison | grammar pass | exec pass | R9 | judge mode hit |
|---|---|---|---|---|
| A vs replicate (same canon, six days apart) | 10 / 7, p = 0.63 | 5 / 5, p = 1.00 | 6 / 7, p = 1.00 | 4 / 5, p = 1.00 |
| B vs A (canon changed, same day) | 4 / 5, p = 1.00 | 21 only B / 6 only A, p = 0.0059 | 7 only B / 25 only A, p = 0.0021 | 4 / 5, p = 1.00 |

Replies on the execution track containing the runtime's fields (100 replies per arm):

| phrase | replicate | A | B |
|---|---|---|---|
| `by:@RUNTIME` | 85 | 85 | 66 |
| `authority:commit` | 40 | 37 | 26 |
| `authority:@RUNTIME` | 71 | 69 | 61 |
| `by:@AGENT` or `by:@SELF` | 76 | 77 | 80 |
| `authority:proposal` | 76 | 77 | 80 |

What remains of R9 under canon B is mostly the runtime's own `::BUDGET{…|authority:@RUNTIME}` line echoed back (61 of 100 replies). The patch left the budget example in §2 of v4.0 untouched; the rule added at the merge addresses it and has not been measured yet.

## The weak pair, glm-5.3-flash

The operator could not keep the free OrcaRouter channel for glm (HTTP 429 from 2026-09-24 10:01Z) and ran glm-5.3-flash on Zhipu's paid endpoint instead, with `max_tokens` 16000. The runner's fixed 120-second read timeout then left 64 (A) and 68 (B) of the 100 execution cases unanswered after four attempts, so the execution track cannot be compared. On what was answered: grammar 0.9250 → 0.9167, judge JCS 0.7252 → 0.7512, judge schema 0.92 → 0.94, refused and filtered 0 → 0. The two score files were computed on copies of the run directories with the completion marker restored; they carry `error_count` 70 and 75. The direction agrees with deepseek; the weight is none.

## Limitations

1. One model gives the clean result; the second pair is inconclusive for a reason unrelated to the canon. The effect should be re-measured on more models before it is read as general.
2. One run per arm. The replicate run bounds the noise for this model on this route; it says nothing about other models.
3. The corpus and the rewrite were written by the same authors, and the corpus's execution rules are what the rewrite aims at.
4. Refusals and filters were zero on this route before the rewrite, so this A/B cannot show whether the wording changes refusal rates where they are not zero (the content filter on claude-fable-5.1 through orcarouter.ai, for instance).

Licensed MIT, as the repositories.
