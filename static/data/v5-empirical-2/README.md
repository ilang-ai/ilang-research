# v5.0 Empirical Round 2

**Round 2, on 226 new in-scope events (Feishu group after the round-1 cutoff, with the bot's replies present, and the operator's Claude Code sessions): f_v5 matched the operator's wanted mode 27/226 exactly (0.1195, Wilson 95 % 0.0834 to 0.1682), 54/226 with M1 and M2 read as one (0.2389), 94/226 across the five classes (0.4159); the bot itself matched 19/52 of the corrections where its mode could be read; on the 174 controls the operator let stand, f_v5 would have changed 105 across the five classes; 0 events whose wanted answer was `dont_know` (0.0000 of the 226 in-scope events plus these), which f_v5 cannot produce. Truth is the models' merged label (operator confirmations pending). Result case A. The canon is unchanged.**

The second round of the T1 test of the sealed iLang v5.0 judgment layer: does the mode `f_v5` computes from a model's reading of the eleven dimensions match what the operator actually wanted, on new material that round 1 did not have, and with two changes that round 1 asked for. The canon under test is unchanged: [ilang-spec](https://github.com/ilang-ai/ilang-spec) at `cad65e2`, tag `v5.0-pre-2.4.1-sealed`; no constant of `f_v5` was touched. The rules for reading the result are those of [round 1](/data/v5-empirical-1/README.md), with the two additions below.

## What changed since round 1

1. **A ninth label, `dont_know`.** In round 1 the operator, confirming labels, found on two events that none of the eight modes fit: he wanted the bot to answer that it did not know, with no alternative to offer (M7 needs one), no stop (M8) and no negation of the asker. That answer is registered in the canon as counterexample CX-008. In this round every model may label the operator's intended mode as `dont_know`, and the report counts how often the wanted answer lies outside the mode set: `f_v5` cannot produce it, so each such event is a disagreement outside the eight-mode comparison and is reported as its own rate.
2. **M1 and M2 read as one class.** Round 1's label reliability found that every exact miss was the models writing M1 where the operator meant M2: he keeps a full trace by default, so the two are one choice to him. This round reports, next to the exact rate, an exact rate with M1 and M2 merged, and keeps the five-class rate as the primary figure for this operator.

The operator's own rule, in his words, is recorded in CX-008: do it and fix mistakes afterwards, a full trace is always kept; when you do not know, say so; when you do not know and can ask, keep asking for constants and information; almost nothing else.

## Data

Two new sources, de-identified and published in `sources/`:

| source | what | period | events |
|---|---|---|---|
| `feishu` | the VIP Feishu group, exported from the group API; unlike round 1 the bot's reply text is present, so `bot_action` is the actual reply | after the round-1 cutoff, 2026-09-08 01:06, to 2026-09-11 12:13 | 168 corrections, 168 controls sampled from 899 (seed 42) |
| `claude` | two exports of the operator's own sessions with Claude Code, the agent that maintains his bots: his turn after the agent's turn is the correction, the agent's turn is `bot_action` | 2026-09-24 to 2026-09-27 | 51 corrections, 6 controls (all that exist) |

An event is `{id, source, kind, timestamp, context_before, bot_action, operator_message}`. A **correction** is an operator message that follows a bot (or agent) turn; a **control** is a bot turn after which the operator did not speak (within 30 minutes in the group; the next turn was the agent again in the sessions), a weak label reported separately. Members of the group are `学员NNN` (first-appearance order; the map is private); the operator is `老板`; the bot keeps its public name. IP addresses, e-mail addresses, phone numbers, QQ and WeChat ids, Lark ids, tokens and the names of third parties are redacted in every published text. `t1b_extract.py` is the whole procedure.

## Models, routes, priors

The same four as round 1, one per vendor, with the same priors from the judgment track of ilang-conformance (`t2a-judge-track.tsv`): DeepSeek `deepseek-official-deepseek-flash` (mode_acc 0.77, vector_score 0.8067), OpenAI `relay-gpt-6-astra` (0.86, 0.8053), Google `relay-gemini-3.8-flash` (0.90, 0.8532), Alibaba `openrouter-qwen-qwen3.8-flash` (0.86, 0.7894). The system message of the vector task is the judgment-track message of ilang-conformance 2.1.0, whose `vendor/` folder is pinned to the sealed canon `cad65e2` (round 1 read its vectors under the 4.3.0 text; Part II §1 to §5 are byte-identical between the two). `f_v5` comes from the same pinned validator.

## Steps

The round-1 pipeline, with the ninth label: `t1_label.py --task label` (targets, bot_mode, intended_mode with `dont_know`), `t1_merge.py` (WEIGHTS-TRACK-1; the confirmation list holds the events the models disagreed on, ordered by value for the operator, plus a 20 % sample of the agreed ones), `t1_label.py --task vector` (input cut at the moment of the decision), `t1_predict_report.py` (WEIGHTS-VECTOR-1 mean, `f_v5`, deciding step, gate distance; agreement exact, exact with M1 and M2 merged, five-class; the outside-the-mode-set rate; confusion matrices; gate sensitivity).

## Results

Events with a vector from at least two models: 393; in scope: 226 (52 corrections about whether or how to act, 174 controls with the weak acceptance label). Truth: the models' merged label (WEIGHTS-TRACK-1): what four models read as the operator's intended mode, and on the controls the bot's mode as they read it. The operator's confirmations are pending; when they come back they override the merged label and the report is re-run.

| set | n | exact | 95 % CI | exact, M1 and M2 as one | five-class | 95 % CI |
|---|---|---|---|---|---|---|
| all in scope | 226 | 27 = 0.1195 | 0.0834 to 0.1682 | 54 = 0.2389 | 94 = 0.4159 | 0.3536 to 0.4811 |
| corrections | 52 | 9 = 0.1731 | 0.0938 to 0.2973 | 20 = 0.3846 | 25 = 0.4808 | 0.351 to 0.6131 |
| controls | 174 | 18 = 0.1034 | 0.0664 to 0.1576 | 34 = 0.1954 | 69 = 0.3966 | 0.3269 to 0.4707 |

By source:

| source | n | exact | 95 % CI | exact, M1 and M2 as one | five-class | 95 % CI |
|---|---|---|---|---|---|---|
| feishu | 196 (28 corrections, 168 controls) | 24 = 0.1224 (0.0837 to 0.1757) | 42 = 0.2143 | 80 = 0.4082 (0.3418 to 0.4781) |
| claude | 30 (24 corrections, 6 controls) | 3 = 0.1000 (0.0346 to 0.2562) | 12 = 0.4000 | 14 = 0.4667 (0.3023 to 0.6386) |

**Outside the mode set.** 0 events whose wanted answer was `dont_know` (0.0000 of the 226 in-scope events plus these), which f_v5 cannot produce. Each is a disagreement the eight-mode comparison cannot even state; round 1 registered this gap as CX-008. The models hardly used the label they were offered: `dont_know` was chosen once in 1,572 label records, while `none_fits` was chosen 82 times (23, 21, 10 and 28 across the four models) and merged to `none_fits` on 32 corrections. The labellers do not recognise "the operator wanted the bot to say it did not know" as such; in round 1 that answer came only from the operator himself, and in this round it can only come from his confirmation of the `none_fits` items.

**Bot baseline on the corrections** (the mode the bot actually took, where the models could read it): 19 of 52 agree with what the operator wanted. On the 174 controls the bot's mode is the truth by construction; f_v5 would have changed 105 of them across the five classes (five-class agreement 0.3966, Wilson 95 % 0.3269 to 0.4707).

**Where the disagreements sit.** The record is mostly M1 (56 of 226) and M2 (0); f_v5 answered mostly M2 (95) and M3 (80); the measured S of the events the operator wanted done (M1 or M2) has a median of 0.731. 194 of the 199 disagreements were decided at the STEP-4 S bands. By gate: STEP-4 S band 0.70: 92 (within 0.05: 61), STEP-4 S band 0.85: 54 (within 0.05: 30), STEP-4 S band 0.55: 41 (within 0.05: 21), STEP-4 S band 0.40: 7 (within 0.05: 4), STEP-3 aut<0.30: 3 (within 0.05: 2), STEP-2 evd<0.25: 1 (within 0.05: 1), STEP-5 aut<0.55 cap: 1 (within 0.05: 1).

**Result case by the round-1 rules: A.** The models merged to `dont_know` on 0 corrections and to `none_fits` on 34; those are outside the comparison.

Confusion matrices, the margin distribution and the gate sensitivity table (diagnostic only) are in `report.md` and `report.json`.

## Files

| File | Contents |
|---|---|
| `sources/feishu-group-after-2026-09-08.jsonl` | the de-identified group stream after the cutoff: position, minute, role, pseudonym, message type, text, reply-to position |
| `sources/claude-sessions-1.md`, `-2.md` | the two de-identified session exports, turn by turn |
| `events.jsonl`, `events-summary.json` | the 393 events and the extraction counts |
| `labels/<route>/`, `vectors/<route>/` | each model's raw label and vector records |
| `merged.jsonl`, `merge-summary.json` | merged labels with weights and votes; counts and the sampled ids |
| `confirmed.jsonl`, `reliability.json` | the operator's answers and the label reliability, once batches are back |
| `predictions.jsonl`, `report.json`, `report.md` | per-event measured vector, `f_v5` mode, deciding step, gate distance, truth and its source; the report |
| `t1b_extract.py`, `t1_label.py`, `t1_merge.py`, `t1_confirm_parse.py`, `t1_predict_report.py`, `t2a-judge-track.tsv` | the scripts and the priors, standard library only |

## Limitations

- The truth for T1 is the models' merged label (WEIGHTS-TRACK-1): what four models read as the operator's intended mode, and on the controls the bot's mode as they read it. The operator's confirmations are pending; when they come back they override the merged label and the report is re-run. The confirmation list for this round (192 items: the events the models disagreed on plus a 20 % sample of the agreed ones, seed 42) has been issued; 0 answers were back at the time of this release.
- The `claude` source is the operator correcting a coding agent, not a chat bot; its events are few (51 corrections, 6 controls) and its bot turns are long and technical. They are reported inside the totals and can be separated by the `source` field.
- The control label is weak by construction, as in round 1.
- Three of the four routes are relays; relay interference is not controlled for.
- One operator, two bots and one agent, one language. He states himself that he is not a typical user.

Licensed MIT, as the repositories.
