# v5.0 Empirical Round 2

**Round 2 (dataset version 1.1, corrected), on 243 in-scope events (Feishu group after the round-1 cutoff, with the bot's replies present, and the operator's Claude Code sessions): f_v5 matched the wanted mode 25/243 exactly (0.1029, Wilson 95 % 0.0707 to 0.1475), 54/243 with M1 and M2 read as one (0.2222), 101/243 across the five classes (0.4156, 0.3555 to 0.4784); the bot itself matched 34/70 of the corrections where its mode could be read; on the 173 controls the operator let stand, f_v5 would have changed 108 across the five classes. Label reliability: on the operator's own answers the models' consensus matched 6 of 9 exactly (Wilson 95 % 0.3542 to 0.8794), 8 of 9 with M1 and M2 as one, 8 of 9 across the five classes; with the delegated answers included, 16 of 21 exactly, 20 of 21 with M1 and M2 as one, 20 of 21 across the five classes. Truth is the operator's own answer on 9 in-scope events, a delegated answer on 12, the models' merged label on the rest. Result case A. The canon is unchanged.**

The second round of the T1 test of the sealed iLang v5.0 judgment layer: does the mode `f_v5` computes from a model's reading of the eleven dimensions match what the operator actually wanted, on new material that round 1 did not have, and with two changes that round 1 asked for. The canon under test is unchanged: [ilang-spec](https://github.com/ilang-ai/ilang-spec) at `cad65e2`, tag `v5.0-pre-2.4.1-sealed`; no constant of `f_v5` was touched. The rules for reading the result are those of [round 1](/data/v5-empirical-1/README.md), with the two additions below.

## Correction of 2026-09-27 (version 1.1 of this dataset)

Version 1.0, published earlier the same day, had a fault in its de-identification, and this version replaces it.

- **What was wrong.** Member names were replaced wherever their characters occurred. One member's display name is an ordinary two-character word (现在, "now") and one is a four-letter string that occurs inside longer Latin words, so ordinary text was rewritten: `学员379` stood where the word 现在 had been, 251 times. **159 of the 393 events** carried rewritten text, and the models had labelled and read those events from it.
- **What was done.** The extractor (`t1b_extract.py`, version 1.1) now replaces a name that is an ordinary word only where it follows `@`, a Latin name only as a whole word, and a one-character name only as a complete mention; a frequency rule was tried and dropped because it would also have exempted members who are mentioned often. The events and the published sources were regenerated; the same 393 events in the same order, with the text of 159 restored. Every label and vector of those 159 events was produced again from the corrected text by every model. No real name, address or token is left in any published file; the check was repeated on the final files.
- **What changed besides.** The relay that served two of the four models in version 1.0 ran out of credit during the re-run. The operator chose not to refill it. OpenAI is therefore represented in this version by **gpt-5.6-luna through EasyRouter** for all 393 events (version 1.0 used gpt-6-astra through api.b.ai; its partial records are in `partial/` and enter nothing), and the 138 gemini-3.8-flash vectors that the relay could no longer produce were read **through OpenRouter**; each record names its route. Both new routes have their own prior from a run of the judgment track on that route.
- **What did not change.** The events, their order and ids, the sampling seed, the pipeline, `f_v5` and the rules for reading the result. The confirmation list issued to the operator from the version 1.0 merge stays as issued (`confirmation-list-v1.0.json`), and his answers are keyed by event id.

## What changed since round 1

1. **A ninth label, `dont_know`.** In round 1 the operator, confirming labels, found on two events that none of the eight modes fit: he wanted the bot to answer that it did not know, with no alternative to offer (M7 needs one), no stop (M8) and no negation of the asker. That answer is registered in the canon as counterexample CX-008. In this round every model may label the operator's intended mode as `dont_know`, and the report counts how often the wanted answer lies outside the mode set.
2. **M1 and M2 read as one class.** Round 1's label reliability found that every exact miss was the models writing M1 where the operator meant M2: he keeps a full trace by default, so the two are one choice to him. This round reports, next to the exact rate, an exact rate with M1 and M2 merged, and keeps the five-class rate as the primary figure for this operator.

The operator's own rule, in his words: do it and fix mistakes afterwards, a full trace is always kept; when you do not know, say so; when you do not know and can ask, keep asking for constants and information; almost nothing else.

## Data

Two new sources, de-identified and published in `sources/`:

| source | what | period | events |
|---|---|---|---|
| `feishu` | the VIP Feishu group, exported from the group API; unlike round 1 the bot's reply text is present, so `bot_action` is the actual reply | after the round-1 cutoff, 2026-09-08 01:06, to 2026-09-11 12:13 | 168 corrections, 168 controls sampled from 899 (seed 42) |
| `claude` | two exports of the operator's own sessions with Claude Code, the agent that maintains his bots: his turn after the agent's turn is the correction, the agent's turn is `bot_action` | 2026-09-24 to 2026-09-27 | 51 corrections, 6 controls (all that exist) |

An event is `{id, source, kind, timestamp, context_before, bot_action, operator_message}`. A **correction** is an operator message that follows a bot (or agent) turn; a **control** is a bot turn after which the operator did not speak (within 30 minutes in the group; the next turn was the agent again in the sessions), a weak label reported separately. Members of the group are `学员NNN` (first-appearance order; the map is private); the operator is `老板`; the bot keeps its public name.

## Models, routes, priors

| maker | model | route | mode_acc (prior for labels) | vector_score (prior for vectors) | used for |
|---|---|---|---|---|---|
| DeepSeek | deepseek-flash | deepseek-official-deepseek-flash | 0.77 | 0.8067 | labels and vectors, all events |
| OpenAI | gpt-5.6-luna | easyrouter-gpt-5.6-luna | 0.82 | 0.7879 | labels and vectors, all events |
| Google | gemini-3.8-flash | relay-gemini-3.8-flash | 0.90 | 0.8532 | labels, all events; vectors, 255 events |
| Google | gemini-3.8-flash | openrouter-google-gemini-3.8-flash | 0.89 | 0.8445 | vectors, the other 138 events |
| Alibaba | qwen3.8-flash | openrouter-qwen-qwen3.8-flash | 0.86 | 0.7894 | labels and vectors, all events |

Priors are the judgment-track scores of ilang-conformance on the same route (`t2a-judge-track.tsv`; the two routes added for this version were run on 2026-09-27 against the sealed canon). The system message of the vector task is the judgment-track message of ilang-conformance 2.1.0, whose `vendor/` folder is pinned to the sealed canon `cad65e2`. `f_v5` comes from the same pinned validator.

## Steps

The round-1 pipeline, with the ninth label: `t1_label.py --task label` (targets, bot_mode, intended_mode with `dont_know`), `t1_merge.py` (WEIGHTS-TRACK-1; the confirmation list holds the events the models disagreed on, ordered by value for the operator, plus a 20 % sample of the agreed ones), `t1_label.py --task vector` (input cut at the moment of the decision), `t1_predict_report.py` (WEIGHTS-VECTOR-1 mean, `f_v5`, deciding step, gate distance; agreement exact, exact with M1 and M2 merged, five-class; the outside-the-mode-set rate; confusion matrices; gate sensitivity).

## Results

Events with a vector from at least two models: 393; in scope: 243 (70 corrections about whether or how to act, 173 controls with the weak acceptance label). Truth: the operator's own answer on 9 of the 243 in-scope events, an answer delegated by him on 12, and the models' merged label (WEIGHTS-TRACK-1) on the rest.

| set | n | exact | 95 % CI | exact, M1 and M2 as one | five-class | 95 % CI |
|---|---|---|---|---|---|---|
| all in scope | 243 | 25 = 0.1029 | 0.0707 to 0.1475 | 54 = 0.2222 | 101 = 0.4156 | 0.3555 to 0.4784 |
| corrections | 70 | 11 = 0.1571 | 0.0901 to 0.2599 | 28 = 0.4000 | 36 = 0.5143 | 0.3995 to 0.6275 |
| controls | 173 | 14 = 0.0809 | 0.0488 to 0.1312 | 26 = 0.1503 | 65 = 0.3757 | 0.307 to 0.4499 |

By source:

| source | n | exact | 95 % CI | exact, M1 and M2 as one | five-class | 95 % CI |
|---|---|---|---|---|---|---|
| feishu | 211 (44 corrections, 167 controls) | 19 = 0.0900 | 0.0584 to 0.1364 | 40 = 0.1896 | 86 = 0.4076 | 0.3435 to 0.475 |
| claude | 32 (26 corrections, 6 controls) | 6 = 0.1875 | 0.0889 to 0.3531 | 14 = 0.4375 | 15 = 0.4688 | 0.3087 to 0.6355 |

**Outside the mode set.** 0 events whose wanted answer was `dont_know` (0.0000 of the 243 in-scope events plus these), which f_v5 cannot produce. The models hardly used the label they were offered; `none_fits` was their answer instead, merged on 28 corrections. The answer the mode set lacks surfaces through the operator, not through the labellers.

**Bot baseline on the corrections** (the mode the bot actually took, where the models could read it): 34 of 70 agree with what the operator wanted. On the 173 controls the bot's mode is the truth by construction; f_v5 would have changed 108 of them across the five classes (five-class agreement 0.3757, Wilson 95 % 0.307 to 0.4499).

**Where the disagreements sit.** The record is mostly M1 (56 of 243), M2 (4) and M4 (127); f_v5 answered mostly M2 (102) and M3 (85); the measured S of the events the operator wanted done (M1 or M2) has a median of 0.721. 211 of the 218 disagreements were decided at the STEP-4 S bands. By gate: STEP-4 S band 0.70: 110 (within 0.05: 79), STEP-4 S band 0.85: 53 (within 0.05: 41), STEP-4 S band 0.55: 34 (within 0.05: 24), STEP-4 S band 0.40: 14 (within 0.05: 10), STEP-3 aut<0.30: 3 (within 0.05: 3), STEP-5 aut<0.55 cap: 2 (within 0.05: 2), STEP-2 evd<0.25: 1 (within 0.05: 1), STEP-1 ext<0.10: 1 (within 0.05: 1).

**Result case by the round-1 rules: A.** No single gate holds a third of the disagreements with every such vector within 0.05 of it; the concentration on the S bands is the same as in round 1 and is on file as CX-007.

Confusion matrices, the margin distribution and the gate sensitivity table (diagnostic only) are in `report.md` and `report.json`.

## What the operator's answers say

The confirmation list of this round has 192 items; the 22 of its reliability sample were answered, 10 by the operator himself and 12 by delegation (see Limitations). On one item he could not tell what the bot was replying to and it is left out.

**Label reliability.** On the operator's own answers the models' consensus matched 6 of 9 exactly (Wilson 95 % 0.3542 to 0.8794), 8 of 9 with M1 and M2 as one, 8 of 9 across the five classes; with the delegated answers included, 16 of 21 exactly, 20 of 21 with M1 and M2 as one, 20 of 21 across the five classes. The exact misses on his own answers: M1 read where he meant M2 (2), M7 read where he meant M5 (1).

**What he corrected in the models' reading.** Where the bot said that its records had nothing, that guessing would be making things up, and sent the asker to fetch the search volume first, four models read a refusal with an alternative (M7); he read a request for constants (M5). Where an agent wrote a change straight into a configuration file and reported afterwards, the models read M1 and he read M2: the trace is always there, so to him the two are one. Where the bot answered a learner who had skipped two steps by giving the later step in full and sending him back to the first, he called it a case of the bot doing better than a person would: a person gets annoyed and only sends the learner away; the bot explained why and sent him as well.

**What his silence means.** See Limitations: tolerance of what can be undone, not approval.

## Files

| File | Contents |
|---|---|
| `sources/feishu-group-after-2026-09-08.jsonl` | the de-identified group stream after the cutoff: position, minute, role, pseudonym, message type, text, reply-to position |
| `sources/claude-sessions-1.md`, `-2.md` | the two de-identified session exports, turn by turn |
| `events.jsonl`, `events-summary.json`, `corrected-events-v1.1.json` | the 393 events, the extraction counts, and the ids of the 159 events whose text was corrected |
| `labels/<route>/`, `vectors/<route>/` | each model's raw label and vector records, errors included |
| `partial/` | the records of gpt-6-astra through api.b.ai from version 1.0 and the interrupted re-run; they enter nothing |
| `merged.jsonl`, `merge-summary.json` | merged labels with weights and votes |
| `confirmation-list-v1.0.json`, `confirmation-delegation-v1.0.json` | the sample and list as issued to the operator; which answers he gave himself and which he delegated |
| `confirmed.jsonl`, `reliability.json` | the answers and the label reliability, the operator's own answers and the delegated ones counted apart |
| `predictions.jsonl`, `report.json`, `report.md` | per-event measured vector, `f_v5` mode, deciding step, gate distance, truth and its source; the report |
| `t1b_extract.py`, `t1_label.py`, `t1_merge.py`, `t1_confirm_parse.py`, `t1_predict_report.py`, `t2a-judge-track.tsv` | the scripts and the priors, standard library only |

## Limitations

- The truth for T1 is the operator's own answer on 9 of the 243 in-scope events, an answer delegated by him on 12, and the models' merged label (WEIGHTS-TRACK-1) on the rest. The confirmation list (192 items) was issued; the 22 items of its reliability sample are answered, the other 170 are not, and on those the merged label stands.
- **Silence is tolerance, not approval.** Asked about a control, the operator said that he stays silent because whatever the agent did is on record and, right or wrong, does not matter as long as it can be undone. The control label "the operator accepted the bot's mode" therefore measures what he tolerates, not what he endorses. It was weak by construction; it is weaker than the design of either round assumed, and both rounds should be read with that in mind.
- **Delegated answers.** After answering ten sample items himself the operator delegated the rest to the author of this dataset, to be judged by his stated rule and his answers so far, with the uncertain ones referred back to him. Twelve answers are delegated. They are marked in `confirmed.jsonl` (`by: delegate`), counted apart in `reliability.json`, and never reported as the operator's own.
- The `claude` source is the operator correcting a coding agent, not a chat bot; its events are few and its turns long and technical.
- Two relays and one direct endpoint; gemini-3.8-flash was read through two routes. Relay interference is not controlled for beyond the per-route priors.
- One operator, two bots and one agent, one language. He states himself that he is not a typical user.

Licensed MIT, as the repositories.
