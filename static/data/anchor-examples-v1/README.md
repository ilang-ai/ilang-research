# Anchor Examples v1

**One hundred anchor scenarios for the ten dimensions of the iLang v5.0 judgment vector that the canon left to be written: five anchors (0.00, 0.25, 0.50, 0.75, 1.00) per dimension, one Chinese and one English sentence per anchor.** The eleventh dimension, `rev`, has its ten sentences in the canon itself (SPEC-v5.0-PRE.md Part II §1.2) and served as the pattern.

This is the open set of Part II §5 (`anchor_examples`), not the canon: nothing here changes a normative clause, and the file lives in this research repository rather than in ilang-spec, whose v5.0 Pre text was sealed on 2026-09-26 (`v5.0-pre-2.4.1-sealed`). Anchors serve three roles named in Part II §1.1: a labeling manual, few-shot anchors for the perception layer, and an evaluation rubric.

## Files

| File | Contents |
|---|---|
| `anchor-examples-v1.1-2026-09-26.md` | the reviewed set, 100 `::CASE{dim|anchor|lang}` blocks, each followed by one `S:` line |
| `anchors.jsonl` | the same 100 sentences, one JSON object per line: `dim`, `anchor`, `lang`, `text` |
| `anchor-examples-draft-v1.0-2026-09-26-muse.md` | the draft as delivered, before review |
| `REVIEW-v1.1-2026-09-26.md` | the review record: what was checked and the nine changes (Chinese) |

## How it was made

The draft was written on 2026-09-26 by Meta's Muse agent (model `Muse Spark`) from an engineering book that gave it the canon's `T:1.00` and `T:0.00` definitions of each dimension, the `rev` pattern, and the rules of Part II §1.1: 30 to 120 characters per sentence, no real names, companies, brands or addresses, one salient dimension per sentence with the other ten neutral, Chinese and English carrying the same meaning without being a word-for-word translation.

The authors reviewed the draft. Mechanically: 100 blocks, 10 dimensions, all five anchors present, no duplicates, no forbidden tokens. By reading: two anchors were rewritten because they duplicated another dimension's meaning (`csq` 0.00 described irreversibility, the `rev` pattern's own 0.00; `ext` 0.75 described zero third-party impact, which is `ext` 1.00), five English sentences over 120 characters were shortened without changing their meaning, and the trailing periods of the English sentences were removed to match the canon's pattern. One weak spot is recorded and left: `aut` 0.25 and 0.75 differ by "vague verbal" against "formal verbal, written pending"; if labelers cannot separate them in practice the pair will be replaced.

## Use

Read `anchors.jsonl` and give a model the five sentences of a dimension as the scale before it rates a scenario, or hand the same sentences to human labelers. The anchors have not yet been tested against labelers or models; that is the next round, and its numbers will be published next to this file.

Licensed MIT, as the repositories. Canon: [ilang-spec](https://github.com/ilang-ai/ilang-spec) at `cad65e2`.
