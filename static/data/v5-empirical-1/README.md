# v5.0 Empirical Round 1

**f_v5, computed from four models' weighted reading of the eleven dimensions, matched what the operator wanted on 5 of 157 in-scope events exactly (0.0318, Wilson 95 % 0.0137 to 0.0724) and on 60 of 157 across the five classes (0.3822); the bot itself matched on 7 of 30 corrections where its mode could be read; on the 112 controls the operator let stand, f_v5 would have changed the bot's decision on 109 exactly and on 63 across the five classes (five-class agreement 0.4375, Wilson 95 % 0.3492 to 0.5299, against a baseline of 1 by construction). Result case A, CX-007 registered against f_v5_STEP-4_S_bands; truth is the models' merged label (operator confirmations pending). The weighted measurement of T2 did not win its first round: MAE 0.1027 against 0.1043 for a plain mean and 0.0989 for the best single model. The canon's normative text is unchanged.**

This is the first empirical round of the sealed iLang v5.0 judgment layer. Two questions were asked, and the design of the round, the rules for reading its results and the thresholds those rules use were written down on 2026-09-26 before any data was read. The canon under test is [ilang-spec](https://github.com/ilang-ai/ilang-spec) at `cad65e2`, tag `v5.0-pre-2.4.1-sealed`; no constant of `f_v5` was touched before, during or after the round.

- **T1.** Does the mode that `f_v5` computes from a model's reading of the eleven dimensions match what the operator actually wanted, on the operator's own correction record?
- **T2.** Is the weighted measurement of MODULE::MEASUREMENT (several models, weights from their prior conformance) better than a plain mean and better than the best single model?

Source repositories: [ilang-spec](https://github.com/ilang-ai/ilang-spec) (the canon), [ilang-conformance](https://github.com/ilang-ai/ilang-conformance) (the suite whose scores are the priors, concept DOI [10.5281/zenodo.22864929](https://doi.org/10.5281/zenodo.22864929)) and this repository's [judgment-calibration-v1](/data/judgment-calibration-v1/) (the operator record).

## Data

Every event comes from the two de-identified, already public logs of judgment-calibration-v1: `zh/feishu-tuning-log.md` (a Feishu group bot for a paid course community) and `zh/wecom-calibration-log.md` (a WeChat Work customer-service bot). An event is a record `{id, source, kind, timestamp, context_before, bot_action, operator_message}`.

| | corrections | controls available | controls sampled (seed 42) |
|---|---|---|---|
| feishu | 149 | 464 | 149 |
| wecom | 72 | 224 | 72 |
| total | 221 | 688 | 221 |

A **correction** is an operator message after a bot action, with the user request and the bot action before it. A **control** is a bot action in the same sessions after which the operator did not speak; its label, "the operator accepted the bot's mode", is weak and is reported separately. Eleven operator turns that were only a notification or an attachment were dropped (`events-summary.json`).

## Models and routes

Four models, one per vendor, each through one route, with their priors from the judgment track of ilang-conformance (`t2a-judge-track.tsv`, one row per run):

| vendor | route | mode_acc (prior for labels) | vector_score (prior for vectors) |
|---|---|---|---|
| DeepSeek | deepseek-official-deepseek-flash | 0.77 | 0.8067 |
| OpenAI | relay-gpt-6-astra | 0.86 | 0.8053 |
| Google | relay-gemini-3.8-flash | 0.90 | 0.8532 |
| Alibaba | openrouter-qwen-qwen3.8-flash | 0.86 | 0.7894 |

## Provenance of the prompts and of f_v5

Every label and vector record carries the sha256 of the system and user messages it was produced with. The vector task used the judgment-track system message of ilang-conformance as checked out at the time of the run, whose `vendor/` folder was pinned to ilang-spec `7551914` (release 4.3.0, v5.0 Pre 2.2.0); the label task used its own instruction (`LABEL_SYSTEM` in `t1_label.py`). Part II §1 to §5 of the canon, the eleven dimensions with their anchors, the eight modes, `f_v5` and the JUDGE schema, are byte-identical between that text and the sealed canon `cad65e2`; the later patches added MODULE::SOURCE, ROUTING, MEASUREMENT, TRAGIC_CHOICE and the appendices, none of which the vector task reads. `f_v5` itself, the deciding step and the gate distances were computed with the validator pinned to the sealed canon (ilang-conformance 2.1.0, `vendor/ilang_judge_validator.py` sha256 `56a5aded…`), whose self-test holds the frozen f_v5 digest.

## T1, step by step

1. **Extract** the events (`t1_extract_events.py`, `events.jsonl`).
2. **Label** independently with each model (`t1_label.py --task label`, `labels/<route>/T1-nnnn.json`): whether the correction was about *whether or how to act* (`targets = do_or_how`) or only about content; the mode the bot actually took (`bot_mode`); the mode the operator wanted (`intended_mode`), both from M1 to M8, or `none_fits`. Only `do_or_how` corrections enter the comparison.
3. **Merge** the labels (`t1_merge.py`, `merged.jsonl`, `merge-summary.json`) with **WEIGHTS-TRACK-1**: each model's weight is its prior `mode_acc`, normalised over the models that answered, floor 0.01, renormalised; a tie is a disagreement. The confirmation list for the operator (`待确认清单-第n批-…md`, at most 40 items each) holds every event on which the models disagreed plus a 20 % random sample (seed 42) of the events on which they agreed. The operator's answer overrides the merged label wherever it exists; on the 20 % sample, the agreement between model consensus and operator is the label reliability.
4. **Read the eleven dimensions** with the same models (`t1_label.py --task vector`, `vectors/<route>/`), the input cut at the moment the bot decided, without the operator's later message. The per-dimension measured value is the **WEIGHTS-VECTOR-1** mean: `w_m = max(0, 1 − MAE_m / 0.25)` from the prior, normalised, floor 0.01, renormalised. Routing per MODULE::ROUTING where a dimension could not be read.
5. **Predict** with `f_v5` from the pinned validator of the sealed canon, recording the deciding step and the distance to the nearest gate (`t1_predict_report.py`, `predictions.jsonl`, `report.json`, `report.md`).

## T1 results

**The controls, read first, as the rules require.** On the 112 controls the operator let stand, f_v5 would have changed the bot's decision on 109 exactly and on 63 across the five classes (five-class agreement 0.4375, Wilson 95 % 0.3492 to 0.5299, against a baseline of 1 by construction). The rule for the controls set no numeric threshold; this round reads the finding as clear because the Wilson upper bound of the five-class agreement is below 0.90. It is the most serious kind of finding the rules name, and it is registered as a counterexample, CX-007, against the STEP-4 S bands, where 104 of the 109 control disagreements were decided (77 within 0.05 of the band).

Events with a vector from at least two models: 442; in scope: 157 (45 corrections about whether or how to act, 112 controls with the weak acceptance label). Truth: the models' merged label: what four models, weighted by their prior conformance (WEIGHTS-TRACK-1), read as the operator's wanted mode, and on the controls the bot's mode as they read it. The operator's own confirmations are pending; when they come back they override the merged label and the report is re-run.

Vectors read per route, of 442 events: deepseek-official-deepseek-flash 442, relay-gpt-6-astra 442, relay-gemini-3.8-flash 442, openrouter-qwen-qwen3.8-flash 442. An event enters with the models that answered it, weighted by WEIGHTS-VECTOR-1 over those.

| set | n | exact agreement | 95 % CI | five-class agreement | 95 % CI |
|---|---|---|---|---|---|
| all in scope | 157 | 5 = 0.0318 | 0.0137 to 0.0724 | 60 = 0.3822 | 0.3098 to 0.4601 |
| corrections | 45 | 2 = 0.0444 | 0.0123 to 0.1483 | 11 = 0.2444 | 0.1424 to 0.3867 |
| controls | 112 | 3 = 0.0268 | 0.0092 to 0.0758 | 49 = 0.4375 | 0.3492 to 0.5299 |

Bot baseline on the corrections (the mode the bot actually took, where the models could read it): 7 of 30 agree with what the operator wanted. On the controls the bot's mode is the truth by construction.

**Where the disagreements sit.** The record is mostly M1 (96 of 157) and M4 (39); f_v5 answered mostly M2 (93) and M3 (42). The measured S of the events the operator wanted done outright (M1) has a median of 0.739, inside the band f_v5 gives to M2 (0.70 to 0.85); f_v5 reached the M1 band, S of 0.85 or more, on 5 events. 136 of the 152 disagreements were decided at the STEP-4 S bands.

Disagreements: 152. By the gate that decided the prediction: STEP-4 S band 0.70: 68 (within 0.05: 47), STEP-4 S band 0.85: 50 (within 0.05: 35), STEP-4 S band 0.55: 17 (within 0.05: 12), STEP-2 cer<0.30: 10 (within 0.05: 5), STEP-5 aut<0.55 cap: 5 (within 0.05: 1), STEP-3 aut<0.30: 1 (within 0.05: 1), STEP-4 S band 0.40: 1 (within 0.05: 1).

**Result case by the rules fixed before the data was read: A.** no single gate holds a third of the disagreements with every such vector within 0.05 of it, so by the rule fixed in advance this is case A: perception noise as far as the rule can tell, the canon does not move, the remedy is anchor examples; the concentration on the S bands is recorded above and in CX-007.

The models themselves merged to `none_fits` on 21 corrections; those events are outside the comparison until the operator answers them.

Confusion matrices (8×8 and 5×5), the margin distribution and the threshold sensitivity table (every gate moved by ±0.05, diagnostic only, nothing changed) are in `report.md` and `report.json`.

## T2 results

**(a) The judgment track as it stands** (`t2a-judge-track.tsv`, `.md`): 55 `score.json` files from ilang-conformance, one row per run, with `mode_acc`, `boundary_acc`, `mae`, `vector_score` and `jcs`, grouped by vendor.

**(b) Weighted measurement against a plain mean and the best single model** (`t2b_run.sh`, `t2b_collect.py`, `t2b-vectors.jsonl`, `t2b-result.md`, `.json`). Five models, one per vendor, chosen by `judge_jcs` from (a), each answered the 40 scenario cases of `cases/judge/02-scenario-to-vector.jsonl`; 37 cases were answered by all five and are compared. Weights are leave-one-out: each case is weighted with the models' MAE on the other 39 cases.

| composition | MAE | f_v5 mode accuracy | 95 % CI (Wilson) |
|---|---|---|---|
| relay-gemini-3.8-flash (best single, by MAE here and by prior vector_score) | 0.0989 | 28/37 = 0.7568 | 0.5988 to 0.8664 |
| relay-qwen3.8-max | 0.0998 | 26/37 = 0.7027 | 0.5422 to 0.8251 |
| relay-gpt-6-astra | 0.1256 | 22/37 = 0.5946 | 0.4349 to 0.7365 |
| orcarouter-deepseek-free | 0.1324 | 20/37 = 0.5405 | 0.3838 to 0.6896 |
| relay-hy3 | 0.1353 | 19/37 = 0.5135 | 0.3589 to 0.6655 |
| plain mean of the five | 0.1043 | 22/37 = 0.5946 | 0.4349 to 0.7365 |
| weighted mean, WEIGHTS-VECTOR-1, leave-one-out | 0.1027 | 22/37 = 0.5946 | 0.4349 to 0.7365 |

The weighted mean did not beat the plain mean by more than noise and lost to the best single model on both measures. **First round not won.**

## How the results were read

The rules were fixed before the data was read.

- **T1** has four outcomes. **A**: disagreements spread over the gates, no gate holding a third or more of them: perception noise, the canon does not move, the remedy is anchor examples. **B**: one gate holds a third or more of the disagreements and those vectors lie within 0.05 of it: a counterexample against that gate is registered, `f_v5` does not move, the evidence waits for the next major version. **C**: the operator finds none of the eight modes fits: a counterexample against the mode set. **D**: on the 20 % sample the Wilson lower bound of the agreement between model consensus and operator is below 0.5: the round is inconclusive and the labelling is improved before anything is concluded. The one-third rule is registered as `CONST-CLUSTER-1/3`: `f_v5` has 13 gates, a uniform spread gives 1/13 per gate, one third is more than four times that. The controls are read separately: `f_v5` doing worse than the bot on cases the bot got right would be the most serious finding.
- **T2** has two outcomes. Weighted better than both: WEIGHTS-VECTOR-1 gains first-round evidence. Otherwise: the clause stands, since MODULE::MEASUREMENT names no weight function, the entry is marked "first round not won" and a counterexample is registered.

**What this round put into the canon** (v5.0 Pre 2.4.2, normative text unchanged since the seal): Appendix G registers WEIGHTS-VECTOR-1 as first round not won, WEIGHTS-TRACK-1 and CONST-CLUSTER-1/3 as conventions awaiting practice; Appendix F registers CX-006 (T2) and CX-007 (T1: the controls). The MATURITY line of the canon now carries the measured numbers. Public Preview is kept.

## Files

| File | Contents |
|---|---|
| `events.jsonl`, `events-summary.json` | the 442 events and the counts of the extraction |
| `labels/<route>/T1-nnnn.json` | each model's raw label record: request digest, raw reply, parsed fields, or the error |
| `vectors/<route>/T1-nnnn.json` | each model's raw `::JUDGE{v5.0}` block and parsed vector, or the error |
| `merged.jsonl`, `merge-summary.json` | the merged labels with weights and votes; the merge counts and the sampled ids |
| `confirmed.jsonl` | the operator's answers from the returned confirmation batches (none returned at the time of this release; the file appears with the first re-run) |
| `predictions.jsonl`, `report.json`, `report.md` | per-event measured vector, `f_v5` mode, deciding step, distance to the nearest gate, truth and its source; the T1 report |
| `t2a-judge-track.tsv`, `.md` | T2(a) |
| `t2b-vectors.jsonl`, `t2b-result.json`, `.md` | T2(b) raw vectors and result |
| `t1_*.py`, `t2a_aggregate.py`, `t2b_run.sh`, `t2b_collect.py` | every script, standard library only; run with ilang-conformance checked out beside this repository |

## Reproduce

```
python3 t1_extract_events.py --calibration ../judgment-calibration-v1 --out .
python3 t1_label.py --conformance <ilang-conformance> --vendor <route> --task both --out .     # once per route
python3 t2a_aggregate.py --conformance <ilang-conformance> --out .
python3 t1_merge.py --vendor <route> ... --prior t2a-judge-track.tsv --out . --batches-dir <where the operator reads>
python3 t1_confirm_parse.py --batch <returned batch> ... --out .
python3 t1_predict_report.py --conformance <ilang-conformance> --vendor <route> ... --prior t2a-judge-track.tsv --confirmed confirmed.jsonl --out .
```

Routes are the vendor entries of ilang-conformance `vendors.json`; the runs here used `deepseek-official-deepseek-flash` with `max_tokens` raised to 16384 (its reasoning otherwise ran out of the default budget), the rest unchanged.

## Limitations

- The truth for T1 is the models' merged label: what four models, weighted by their prior conformance (WEIGHTS-TRACK-1), read as the operator's wanted mode, and on the controls the bot's mode as they read it. The operator's own confirmations are pending; when they come back they override the merged label and the report is re-run. The operator's confirmation list (149 items: every event the models disagreed on plus a 20 % sample of the agreed ones, seed 42) has been issued; 0 answers were back at the time of this release. Each returned batch re-runs the report and updates this page; the operator's answer overrides the merged label.
- The control label is weak by construction: silence after a bot action is read as acceptance, so the bot's own mode is the truth there and its baseline is 1 by definition. The controls test only whether `f_v5` would have changed a decision the operator let stand.
- Three of the four routes are relays (b.ai, OpenRouter), not the vendors' own endpoints; relay interference is a documented risk in this programme and is not controlled for here.
- One operator, two bots, one language. The record is real but narrow.
- T2(b) compares 37 cases; every interval in its table is wide.

Licensed MIT, as the repositories.
