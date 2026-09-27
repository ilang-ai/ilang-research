---
title: "v5.0 Empirical Round 2"
date: 2026-09-27
summary: "Round 2 (dataset version 1.1, corrected), on 243 in-scope events (Feishu group after the round-1 cutoff, with the bot's replies present, and the operator's Claude Code sessions): f_v5 matched the wanted mode 25/243 exactly (0.1029, Wilson 95 % 0.0707 to 0.1475), 54/243 with M1 and M2 read as one (0.2222), 101/243 across the five classes (0.4156, 0.3555 to 0.4784); the bot itself matched 34/70 of the corrections where its mode could be read; on the 173 controls the operator let stand, f_v5 would have changed 108 across the five classes. Label reliability: on the operator's own answers the models' consensus matched 6 of 9 exactly (Wilson 95 % 0.3542 to 0.8794), 8 of 9 with M1 and M2 as one, 8 of 9 across the five classes; with the delegated answers included, 16 of 21 exactly, 20 of 21 with M1 and M2 as one, 20 of 21 across the five classes. Truth is the operator's own answer on 9 in-scope events, a delegated answer on 12, the models' merged label on the rest. Result case A. The canon is unchanged."
tags: ["dataset", "evaluation", "judgment", "conformance", "LLM", "iLang", "v5.0"]
author: "Long Quan Zhu"
---

## Download

The round is at [`/data/v5-empirical-2/`](/data/v5-empirical-2/), with a [README](/data/v5-empirical-2/README.md) covering the correction of 2026-09-27, the two changes since round 1 (the ninth label, `dont_know`, and M1 and M2 read as one class), the two new sources, the results, what the operator's own answers say, and the limitations. The de-identified sources are published in the folder, so the round can be re-run from them.

| File | Contents |
|---|---|
| [`report.md`](/data/v5-empirical-2/report.md) | the T1 report: agreement exact, with M1 and M2 merged, and five-class, with Wilson intervals; the outside-the-mode-set rate; the bot baseline; confusion; gate sensitivity |
| [`reliability.json`](/data/v5-empirical-2/reliability.json) | label reliability on the sample, the operator's own answers and the delegated ones counted apart |
| [`sources/`](/data/v5-empirical-2/sources/) | the de-identified Feishu group stream after 2026-09-08 and the two Claude Code session exports |
| [`events.jsonl`](/data/v5-empirical-2/events.jsonl), `labels/`, `vectors/`, `merged.jsonl`, `confirmed.jsonl`, `predictions.jsonl` | the data at every step |
| `t1b_extract.py`, `t1_*.py` | the scripts, standard library only |

Canon under test: [ilang-spec](https://github.com/ilang-ai/ilang-spec) `cad65e2`, tag `v5.0-pre-2.4.1-sealed`, unchanged. Round 1: [v5.0 Empirical Round 1](/datasets/v5-empirical-1/).

## Correction of 2026-09-27

Version 1.0 of this dataset, published earlier the same day, replaced member names wherever their characters occurred; one name is an ordinary word, so ordinary text was rewritten in 159 of the 393 events and the models had read those events from the rewritten text. Version 1.1 restores the text, keeps every real name protected, and produces every label and vector of the 159 events again. During the re-run the relay behind two of the models ran out of credit: OpenAI is now represented by gpt-5.6-luna through EasyRouter for all events, and 138 gemini vectors were read through OpenRouter. The README has the details; the numbers below are those of version 1.1.

## Quick stats

- **Events**: 393; Feishu group after the round-1 cutoff, 168 corrections and 168 controls; the operator's Claude Code sessions, 51 corrections and 6 controls
- **Models**: DeepSeek deepseek-flash, OpenAI gpt-5.6-luna, Google gemini-3.8-flash, Alibaba qwen3.8-flash, each weighted by its own route's prior
- **T1**: 243 in-scope events (70 corrections, 173 controls); exact 25/243 = 0.1029 (95 % CI 0.0707 to 0.1475), M1 and M2 as one 54/243 = 0.2222, five-class 101/243 = 0.4156; bot baseline on corrections 34/70; f_v5 would have changed 108 of 173 controls across the five classes; result case A; truth: the operator's own answer on 9 in-scope events, a delegated answer on 12, the models' merged label on the rest
- **Outside the mode set**: 0 events whose wanted answer was `dont_know` (0.0000 of the 243 in-scope events plus these), which f_v5 cannot produce
- **Label reliability**: on the operator's own answers the models' consensus matched 6 of 9 exactly (Wilson 95 % 0.3542 to 0.8794), 8 of 9 with M1 and M2 as one, 8 of 9 across the five classes; with the delegated answers included, 16 of 21 exactly, 20 of 21 with M1 and M2 as one, 20 of 21 across the five classes

## Why it is worth reading

**The bot's own words are in the record this time.** Round 1 had the operator's corrections but not the Feishu bot's replies; this round has both, so the models label and read the vector from what was actually said.

**The operator said what his silence means.** Asked about a decision he had let stand, he answered that he stays silent because the action is on record and can be undone, right or wrong. The control label measures tolerance, not approval; both rounds are to be read with that in mind.

**The two lessons of round 1 were turned into method, not into a better number.** The ninth label lets the models name the answer the mode set lacks; the merged M1/M2 rate measures the function against an operator who keeps a full trace by default. Neither touches `f_v5`.

**A fault in our own data is corrected in the open.** What was wrong, how many events it touched and what was done are stated in the dataset itself.

## Limitations

The truth for T1 is the operator's own answer on 9 in-scope events, a delegated answer on 12, the models' merged label on the rest. The control label is weak, and by the operator's own account measures tolerance. Twelve of the sample answers are delegated and counted apart. gemini-3.8-flash was read through two routes. One operator, who says himself he is not a typical user.
