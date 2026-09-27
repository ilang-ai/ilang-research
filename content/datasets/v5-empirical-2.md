---
title: "v5.0 Empirical Round 2"
date: 2026-09-27
summary: "Round 2, on 226 new in-scope events (Feishu group after the round-1 cutoff, with the bot's replies present, and the operator's Claude Code sessions): f_v5 matched the operator's wanted mode 27/226 exactly (0.1195, Wilson 95 % 0.0834 to 0.1682), 54/226 with M1 and M2 read as one (0.2389), 94/226 across the five classes (0.4159); the bot itself matched 19/52 of the corrections where its mode could be read; on the 174 controls the operator let stand, f_v5 would have changed 105 across the five classes; 0 events whose wanted answer was `dont_know` (0.0000 of the 226 in-scope events plus these), which f_v5 cannot produce. Truth is the models' merged label (operator confirmations pending). Result case A. The canon is unchanged."
tags: ["dataset", "evaluation", "judgment", "conformance", "LLM", "iLang", "v5.0"]
author: "Long Quan Zhu"
---

## Download

The round is at [`/data/v5-empirical-2/`](/data/v5-empirical-2/), with a [README](/data/v5-empirical-2/README.md) covering the two changes since round 1 (the ninth label, `dont_know`, and M1 and M2 read as one class), the two new sources, the results and the limitations. The de-identified sources are published in the folder, so the round can be re-run from them.

| File | Contents |
|---|---|
| [`report.md`](/data/v5-empirical-2/report.md) | the T1 report: agreement exact, with M1 and M2 merged, and five-class, with Wilson intervals; the outside-the-mode-set rate; the bot baseline; confusion; gate sensitivity |
| [`sources/`](/data/v5-empirical-2/sources/) | the de-identified Feishu group stream after 2026-09-08 and the two Claude Code session exports |
| [`events.jsonl`](/data/v5-empirical-2/events.jsonl), `labels/`, `vectors/`, `merged.jsonl`, `predictions.jsonl` | the data at every step |
| `t1b_extract.py`, `t1_*.py` | the scripts, standard library only |

Canon under test: [ilang-spec](https://github.com/ilang-ai/ilang-spec) `cad65e2`, tag `v5.0-pre-2.4.1-sealed`, unchanged. Round 1: [v5.0 Empirical Round 1](/datasets/v5-empirical-1/).

## Quick stats

- **Events**: 393; Feishu group after the round-1 cutoff, 168 corrections and 168 controls; the operator's Claude Code sessions, 51 corrections and 6 controls
- **Models**: the same four as round 1, one per vendor
- **T1**: 226 in-scope events (52 corrections, 174 controls); exact 27/226 = 0.1195 (95 % CI 0.0834 to 0.1682), M1 and M2 as one 54/226 = 0.2389, five-class 94/226 = 0.4159; bot baseline on corrections 19/52; f_v5 would have changed 105 of 174 controls across the five classes; result case A; truth: the models' merged label (operator confirmations pending)
- **Outside the mode set**: 0 events whose wanted answer was `dont_know` (0.0000 of the 226 in-scope events plus these), which f_v5 cannot produce; the models chose the new label once in 1,572 label records and `none_fits` 82 times, so the answer the mode set lacks still surfaces only through the operator's own confirmation

## Why it is worth reading

**The bot's own words are in the record this time.** Round 1 had the operator's corrections but not the Feishu bot's replies; this round has both, so the models label and read the vector from what was actually said.

**The two lessons of round 1 were turned into method, not into a better number.** The ninth label lets the models name the answer the mode set lacks; the merged M1/M2 rate measures the function against an operator who keeps a full trace by default. Neither touches `f_v5`.

**A second kind of operator record.** The sessions with a coding agent are the same operator steering a different kind of machine; whether `f_v5` reads him the same way there is a question the data can now ask.

## Limitations

The truth for T1 is the models' merged label (operator confirmations pending); 0 of the 192 confirmation items were back at the time of this release. The control label is weak. Three routes are relays. One operator, who says himself he is not a typical user.
