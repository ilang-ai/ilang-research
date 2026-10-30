# Intake gate

The canon defines how it changes (SPEC-v5.0.md Part I, MODULE::AMENDMENT and MODULE::SOURCE). This directory runs that definition as code on every issue filed through the two intake forms. Nothing here merges anything.

## What runs

| gate | applies to | passes when |
|---|---|---|
| 1 grammar | every submission | every fenced iLang block passes `ilang_grammar_validator.py --lint --strict`; every `::JUDGE` block passes `ilang_judge_validator.py --check` |
| 2 canon | amendments | the diff applies to a fresh checkout of `ilang-ai/ilang-spec` main, and the patched checkout passes the spec's own CI gate command by command (grammar canon gate, judge selftest and JUDGE check, JSON schemas, symbol audit seal S3, products strict lint) |
| 3 judgment | amendments | a model that is not the proposer perceives the 11-dimension vector of the action "merge this amendment into the canon"; `route()` applies the MODULE::ROUTING rows it reports; `f_v5()` of the judge validator computes the mode; the block is written in the frozen `::JUDGE{v5.0}` form and checked by the same validator |

The tools are taken from the checkout of the canon at the commit the record names, never vendored here.

## Verdicts

| label | meaning | issue |
|---|---|---|
| `counterexample` | gate 1 passed; recorded verbatim under `records/counterexamples/` | stays open |
| `passed-gates` | all three gates passed; recorded under `records/amendments/`; the owner merges by hand | stays open |
| `needs-record` | no fenced record, or no diff for an amendment | stays open; edit the issue to re-run |
| `needs-evidence` | f_v5 gave M5 (ask) | stays open; edit the issue to re-run |
| `rejected:grammar` | a block fails strict mode | closed, output in the record |
| `rejected:canon` | the patched canon fails its own CI | closed, output in the record |
| `rejected:judge` | f_v5 gave M6, M7 or M8 | closed, JUDGE block in the record |
| `blocked:*` | gate 3 could not run (no key, transient error, gate bug) | stays open; fails closed |

Modes M1 to M4 pass. M3 (confirm) is the expected result for a canon change: the confirmation is the owner's merge.

## Perceiver

`deepseek-flash` through the DeepSeek API, temperature 0, thinking off, JSON output, with the SOURCE, ROUTING, AMENDMENT and VECTOR modules of the canon and the proposal in the prompt. The model never assigns a mode; it returns the vector, the routing conditions it sees, a confidence and a one-line reason. Unknown dimensions are reported as `unknown:<dim>`, which routing sets to 0.50 with certainty below the gate, so f_v5 asks instead of acting. The key lives in the repository secret `DEEPSEEK_API_KEY` and never appears in a record.

## Records

One Markdown file per issue under `records/`, written by the workflow and committed to this repository: metadata, every gate command with its exit code and output verbatim, the perception JSON verbatim, the JUDGE block, and the submission verbatim. Logs are not edited.

## Running it locally

    gh api repos/ilang-ai/ilang-research/issues/N > issue.json
    git clone https://github.com/ilang-ai/ilang-spec spec
    DEEPSEEK_API_KEY=... python gate/intake.py --issue issue.json --spec spec --records records --out out
