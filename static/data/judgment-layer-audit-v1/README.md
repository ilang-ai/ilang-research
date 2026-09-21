# Judgment Layer Audit v1

**Three days of a production agent's messages judged twice — by a cheap always-on judge model, and by the operator's written rules — released as aggregate counts.**

> 7,940 messages judged, 2,648 of them scored against the reference, 18–20 September 2026. Agreement rises 68.4% → 75.1% → 80.9% on the unbiased sample. The headline rule-compliance improvement everyone would have quoted, 69 → 7, turns out to be mostly a change in the measuring stick; under one stick it is 13 → 7. That correction is the point of this release.

## What this is

A community agent answers real people all day. Every incoming message is classified twice:

- **the judge** — a small always-on model (internal deployment label `jev`) that decides what the person is actually asking for, one of eight branches;
- **the reference** — a second model (deepseek-flash) applying the operator's written rules to the same message, run once a day over a sample.

Both sides land in the same database with their branch, the rule the reference invoked, the agent's actual behaviour label, and the judge's self-reported confidence. This dataset publishes the counts derived from those rows.

It is not a benchmark and there is no human gold standard. It measures how often a cheap judge agrees with the rules it stands in for, whether its confidence means anything, and what happens to a time series when the criterion moves underneath it.

## Files

| File | Contents |
|---|---|
| `totals.tsv` | Per-day volume, latency, tokens, cost |
| `agreement.tsv` | Agreement counts and rates by stratum and by confidence band |
| `confusion-matrix.tsv` | Every `judge_branch → reference_branch` pair, per day, not truncated |
| `rule-deviations.tsv` | Deviations per rule per day, under both criteria |

Tab-separated, header row, UTF-8. `day` is a calendar day in Asia/Shanghai, or `all` for a pooled figure. `rate` is `agreements / n` to three decimals.

## Headline numbers

| | 2026-09-18 | 2026-09-19 | 2026-09-20 |
|---|---|---|---|
| Messages judged (operator's own excluded) | 2,903 | 2,439 | 2,598 |
| Scored against the reference | 900 | 848 | 900 |
| Agreement, unbiased random sample | **68.4%** (141/206) | **75.1%** (202/269) | **80.9%** (216/267) |
| Agreement, candidate sample (selected to disagree) | 40.3% (280/694) | 44.6% (258/579) | 52.6% (333/633) |
| Mean judge latency | 0.590 s | 0.612 s | 0.623 s |

Agreement by the judge's own confidence, three days pooled: **87.2%** (558/640) at confidence ≥ 0.85, **57.9%** (302/522) from 0.5 to 0.85, **38.4%** (570/1,486) below 0.5. That is the one directly actionable result here: the top band can be trusted without a second opinion, the bottom band cannot.

Judging all 7,940 messages cost **$0.5514** of input tokens at the deployment's own price constant ($0.042 per million; 13,129,303 tokens). The reference side's dollar cost is **not published**: its collection script records tokens only and no unit price constant exists on that machine. Its token counts are in `totals.tsv`.

## The criterion moved mid-window

On 2026-09-20 at 16:04 the criterion itself was edited. The criterion defines, per branch, which agent behaviours count as obeying a rule. The edit touched one branch — third-party platform problems — and added two behaviours to its allowed set, because a rule had been split in two that same day and those two behaviours had become correct.

The daily report for the affected rule read **69 deviations on 09-19 and 7 on 09-20**. Subtracting those two numbers measures the edit, not the agent.

Recomputed over the same rows:

| Criterion | 09-18 | 09-19 | 09-20 | 09-19 → 09-20 |
|---|---|---|---|---|
| As reported daily (two criteria mixed) | 46 | 69 | 7 | not subtractable |
| Current criterion throughout | **16** | **13** | **7** | **−46%** |
| Old criterion throughout | 46 | 69 | 50 | −28%, still above where the window started |

Both series are in `rule-deviations.tsv` under `criterion = current_criterion` and `reported_daily`. The defensible claim is the second row: deviations on that rule fell from 13 to 7. The rest of the 69 → 7 gap is the measuring stick.

The general form: when the rules, the judge and the criterion are all under active development, a series is only a series if one of them holds still — and the paper owes the reader a note about which one moved.

## The branch taxonomy

`confusion-matrix.tsv` reads `judge_branch → reference_branch`: what the judge said, then what the reference said.

| Branch | The message is |
|---|---|
| `concrete_block` | a specific blocker in the step the person is on |
| `deliverable` | finished work being shown for review |
| `handout` | a request to be handed the result rather than shown the step |
| `platform_issue` | a problem owned by a third-party platform, not by us |
| `hypothetical` | a what-if question not tied to the person's current step |
| `chitchat` | social talk |
| `spell_command` | a request to run a prompt or command |
| `admin_cert` | membership or certification administration |

The three largest disagreements over the window — `deliverable→concrete_block` (231), `handout→concrete_block` (140), `chitchat→concrete_block` (78) — all point the same way: the judge reads an ambiguous message as someone being stuck. That matches how it is deployed, since missing a stuck person costs more than a false alarm, but it means its branch distribution overstates real demand for help. The largest single pair fell from 105 to 43 across the three days.

## Method

**Population.** Every message in the community except the operator's own (16 across three days, excluded everywhere). The judge runs continuously on a ten-minute timer; the reference runs once a day over a sample.

**Sampling.** Messages the daily job flags as likely disagreements are all scored; the rest are sampled at 15%. The strata are merged, ordered by time and truncated to 900. `random.seed(day)` makes the draw reproducible. 09-18 and 09-20 hit the cap, so those days skew toward earlier messages; 09-19 did not (848). Use the `random_sample` rows for an unbiased rate; `candidate_sample` is selected for disagreement by construction.

**Agreement** means both sides chose the same branch out of eight. It is consistency with the written rules as read by a second model — not truth.

**Deviation** means the agent's actual behaviour fell outside the set the criterion allows for the branch the reference chose.

## Desensitization

Principle, as in the other datasets on this site: **strip identity, keep judgment.** This release goes further than the others because it does not need message content at all — it publishes counts only.

Not published: message text, the rule texts, per-message rows, and the internal rule identifiers. Rules appear as `R01`…`R16`, ordered by three-day total. The rule texts are the operator's own system prompt; the messages belong to the people who wrote them, who published nothing. Everything needed to check the arithmetic in this README is in the four files.

## Limitations

1. No human gold standard; agreement is consistency with one model's reading of the rules.
2. The reference side is not homogeneous across the window — its prompt was edited on 09-20 when the rule was split, so 09-18 and 09-19 were judged by the older prompt. Those days were deliberately not re-run: a sample records the system as it was that day, and rewriting it to match the current version would erase the evidence of the change.
3. Two of three days hit the 900 sample cap (see sampling).
4. One earlier hand classification could not be reproduced and is therefore absent; for 09-19 only the machine-recorded behaviour labels survive.
5. One deployment, three days, one language community. Nothing here transfers to another agent without being re-run there.

## Citation

Zhu, Long Quan (2026). *Judgment Layer Audit v1*, in I-Lang Research. Concept DOI [10.5281/zenodo.22865165](https://doi.org/10.5281/zenodo.22865165). See [CITATION.cff](https://github.com/ilang-ai/ilang-research/blob/main/CITATION.cff).

Licensed MIT, as the repository.
