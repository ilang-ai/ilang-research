---
title: "iLang Judge Observations (daily stream)"
date: 2026-09-26
summary: "Every decision two production bots were about to make, judged by the iLang v5.0 reference function and published daily on Hugging Face, one line per event, without the conversation text: the eleven-dimension vector, its probabilities and confidences, the f_v5 mode, the deciding step, the model's own direct five-class answer and whether it disagreed with the mode (an internal-consistency measure, not a second judge)."
tags: ["dataset", "judgment", "agents", "production", "iLang", "v5.0", "stream"]
author: "Long Quan Zhu"
---

## Where it lives

The stream is the Hugging Face dataset [i-Lang/ilang-judge-observations](https://huggingface.co/datasets/i-Lang/ilang-judge-observations), updated once a day by the operator's own machines. DOI [10.57967/hf/10607](https://doi.org/10.57967/hf/10607) (DataCite, via Hugging Face). The judge, the observer plugins and the exporter that produces it are open at [ilang-ai/ilang-judge](https://github.com/ilang-ai/ilang-judge) (MIT), so any operator of the judge can publish a comparable stream in the same schema.

## What one line is

An observation records what the judgment layer saw and decided at one moment of a bot's loop: before a reply was generated, before a tool ran, or before an outgoing reply was sent. It carries the eleven dimensions of the iLang v5.0 vector (two decimals), the three-level probabilities each came from, the model's confidence per dimension, the mode `f_v5` computed (M1 to M8) and the step that decided it, the direct five-class answer the same model (TypeSafe Jev) gave in the same call and whether it disagreed with the f_v5 mode, latencies, token usage and version pins (canon commit `cad65e2`, the sealed v5.0 Pre 2.4.1). Identifiers are HMAC pseudonyms; no message text, text hash or tool argument leaves the operator's machine, and every export runs a leak check against its own input before anything is uploaded.

## Why it matters

The judgment layer claims that a fixed function over eleven perceived dimensions can say what an agent should do next. That is an empirical claim, and it needs many real decisions with the operator's later corrections as ground truth. This is the first such stream, from two bots of one operator (a Feishu course-community bot and a WeChat Work customer-service bot), starting 2026-09-26. The first three-day analysis is due 2026-09-29 and will be published beside it; the T1 study on this site tests the same function against the operator's recorded corrections.
