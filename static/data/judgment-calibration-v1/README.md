# Judgment Calibration Dataset v1

**An open longitudinal record of AI judgment calibration in production — from first boot to autonomous operation.**

> 24 days. 152 operator messages to the bot, 41 of them explicit tuning instructions. From "你TMD人呢" to running without human intervention.

## What this is

Raw logs from two production AI customer-service bots, plus the complete calibration process that turned them from generic chatbots into judgment-bearing agents. Every number below is computed from the files in this directory; where a figure is operator-reported rather than present in the data, it is marked as such.

This is not a curated benchmark. It is what real-world AI judgment calibration looks like before anyone cleaned it up.

## Why it matters

Existing alignment datasets are cross-sections: many annotators each scoring one response. This dataset is a **longitudinal cut**: one operator calibrating one system from day one to maturity. Cross-sections train models. Longitudinal cuts show **how judgment functions emerge**.

The pain signal is natural, not designed. When the operator types "你TMD" (roughly: "WTF are you doing"), that is a negative signal with high intensity. When they say "漂亮" ("beautiful"), that is a positive one. No annotation guidelines, no paid labelers — a business owner watching their bot talk to paying customers and reacting in real time.

## Dataset structure

```
judgment-calibration-v1/
├── zh/                              Chinese originals (desensitized)
│   ├── feishu-tuning-log.md         Feishu bot: 152 operator messages, 24 days
│   ├── wecom-calibration-log.md     WeChat bot: 84 operator directives × 308 assistant responses, 14 days
│   └── wecom-dialogue-full.md       WeChat bot: 110 sessions, 533 customer questions, 30 days
├── structured/                      Machine-readable
│   ├── tuning-events.jsonl          152 operator messages with type + adopted label (Feishu)
│   ├── api-calls.jsonl              2,162 API calls: model / tokens / latency / cache (Feishu)
│   └── user-interactions.jsonl      1,062 messages with sender hash + is_boss (Feishu)
├── analysis/
│   ├── convergence-curve.py         Event frequency over time + adopted-label breakdown
│   └── compression-ratio.py         Token comparison across zh / en / ilang renderings
└── README.md
```

## Key statistics

All Feishu figures are computed from `structured/`. WeChat per-call API records were not exported; those figures are counted from `zh/wecom-*.md` or operator-reported.

| Metric | Feishu bot | WeChat Work bot |
|---|---|---|
| Platform | Feishu (Lark) group + DM | WeChat Work 企微 1:1 customer service |
| Coverage | 2026-08-15 → 2026-09-08 | dialogue 2026-08-09 → 2026-09-08; calibration 2026-08-26 → 2026-09-08 |
| Base models (by API call) | deepseek-v4-pro 1,686 (78.0%) · claude-opus-4-6 294 (13.6%) · grok-4.3 157 (7.3%) · deepseek-v4-flash 25 (1.2%) | Claude Sonnet 5 per pipeline config (operator-reported; no per-call records in this dataset) |
| Distinct senders who talked to the bot | **244** | **110** sessions |
| Operator messages | **152** (41 explicit 🔧 tuning, 111 directives) | **84** directives |
| Assistant responses | 1,021 (from send log) | **308** |
| Customer/user messages | **1,062** non-empty text (1,081 inbound incl. media) | **533** questions |
| API calls | **2,162** | not exported (operator estimate ~190) |
| Tokens in / out | **103,260,395 / 1,911,629** | not exported |
| Median API latency | **8.3 s** | operator-reported ~7.8 s |
| Monthly cost | operator-reported ~1,000 RMB | operator-reported ~$29 |

> Earlier drafts of this README cited "447+ paying users". That number is the paid community's membership, not something in this dataset. The data contains **244** distinct senders; that is the figure to cite.

## The `adopted` label

`structured/tuning-events.jsonl` carries one row per operator message to the Feishu bot. Each row has:

- `type` — `tuning` if the message begins with 调教 (an explicit "tune this" instruction), else `directive`
- `prev_reply_chars` — length of the bot's most recent reply in the same chat before this message
- `adopted` — `1`, `0`, or `null`
- `adopted_rule` — which rule fired: `pos`, `neg`, `ambiguous`, `no_prior_reply`

`adopted` is assigned by a **lexicon heuristic, not by human annotation**:

- positive lexicon without any negative term → `1` (漂亮 / 可以 / 不错 / 好的 / 很好 / 对的 / 没问题 / 正确 / 棒 / 👍 / 表扬 / 牛)
- negative lexicon without any positive term → `0` (TMD / 你妈 / 调教 / 铁律 / 记住 / 以后 / 不对 / 错了 / 不要 / 别再 / 为什么 / 怎么回事 / 又 / 没有 / 不是 / 瞎 / 乱 / 重新 / 改)
- both, neither, or no prior bot reply → `null`

Result: **13 × `adopted=1`, 59 × `adopted=0`, 80 × `null`** (47% of rows labeled). Treat the label as a weak signal suitable for trend analysis, not as ground truth for per-row training. Anyone wanting a stronger label should annotate the 80 `null` rows by hand; the raw text is there.

## Pain formula (proposed)

```
pain = tokens_consumed × (1 - adopted)
```

Computable on the 72 labeled rows by joining `tuning-events.jsonl` to `api-calls.jsonl` on timestamp proximity. It is proposed as a metric, not validated here; `analysis/convergence-curve.py` reports the labeled/unlabeled breakdown per day so the coverage is always visible.

## Cross-model judgment transfer

The Feishu bot (DeepSeek-primary) and the WeChat bot (Claude) share calibration. Corrections discovered on one were transferred to the other through policy files (a SOUL persona file plus skill files), not retraining. The protocol layer (I-Lang) is the transfer mechanism. `zh/wecom-calibration-log.md` records that transfer step by step — including the cases where the transfer initially failed and had to be re-done.

This supports the hypothesis that a large share of outcome quality lives in the protocol/policy layer rather than the base model. The dataset does not by itself quantify that share.

## Desensitization

**Principle: strip identity, keep judgment.** Applied uniformly by one script with one shared mapping, so nothing can be cross-referenced between files.

Removed:

- Customer identities → `客户001` … `客户110`, mapped by account id (not by display name) and shared across both WeChat files. Single-character or punctuation-only display names are never string-replaced; display names that are also common words are replaced only in session headers, never in prose.
- Feishu `open_id` / `chat_id` / `message_id` → SHA-256 truncated to 16 hex, or `[FEISHU_UID]` / `[FEISHU_CHAT]` inside message text
- Contact handles → `[REDACTED_WECHAT]` / `[REDACTED_QQ]`
- Every IPv4 address → `[SERVER_IP]` / `[IP]`; phone numbers → `[PHONE]`; local usernames and paths → `[USER]`
- Operator remarks characterizing customers as a group → `[内部沟通，已删除]` (15 sentences). These were internal communication, never customer-facing, and are not part of the calibration signal.

Kept:

- Timestamps (the convergence curve needs the x-axis)
- Operator corrections verbatim, including profanity — that is the pain signal's intensity scale
- The bot's wrong answers, caught live
- Grey-area customer requests — real-world judgment requires real-world mess
- Iron rules / 铁律 as written into policy files

## Citation

```bibtex
@dataset{zhu2026judgment,
  author    = {Zhu, Long Quan},
  title     = {Judgment Calibration Dataset: 24-Day Longitudinal Record of AI Agent Calibration in Production},
  year      = {2026},
  publisher = {I-Lang Research, iLang Inc.},
  url       = {https://github.com/ilang-ai/ilang-research},
  doi       = {10.5281/zenodo.21821452},
  license   = {MIT}
}
```

## License

MIT. Use it, study it, build on it. A citation is appreciated but not required.

## Related

- [I-Lang Protocol Specification](https://github.com/ilang-ai/ilang-spec)
- [I-Lang Dictionary](https://github.com/ilang-ai/ilang-dict)
- [research.ilang.ai](https://research.ilang.ai)
- ORCID: [0009-0004-4540-8082](https://orcid.org/0009-0004-4540-8082)
- Related prior work: [arXiv:2510.27328](https://arxiv.org/abs/2510.27328), Lu, Song & Wang (2025), a Valence-Assent Axis inside eight LLMs that subordinates reasoning to judgment. Their evidence is internal to the model; this dataset records judgment calibration from outside.

---

*This dataset is raw. It contains profanity, grey-area business discussions, bot fabrications caught in real time, and unfiltered operator frustration. That is the point. Cleaned data teaches models to be polite. This data shows how judgment actually forms.*
