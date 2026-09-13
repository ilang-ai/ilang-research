---
title: "I-Lang Protocol v4.0 — Overview"
date: 2026-04-25
url: /protocol/overview/
tags: ["I-Lang","protocol","AI-native","precision","AI-to-AI"]
author: "SUN"
description: "I-Lang is the native language of artificial intelligence. Structured instructions AI executes correctly the first time. 88 verbs, two syntaxes, zero ambiguity."
---

##### What is I-Lang?

I-Lang is the native communication protocol for AI. Not a prompt template. Not a compression tool. A structured language built from symbols already inside every LLM's training data: brackets, pipes, arrows, key-value pairs.

Two syntaxes, one protocol:

+ **Operations** `[]` — what AI does: `[READ:@SRC]=>[FMT|fmt=json]=>[OUT]`
+ **Declarations** `::` — what AI is: `::GENE{verify_first|conf:confirmed}`

AI-to-AI structured communication. AI internal planning. Human-to-AI in AI's own language.

##### Design Principles

+ **Zero ambiguity** — Structured instructions eliminate guessing. AI gets it right the first time.
+ **Cross-model compatibility** — Tested across ChatGPT, Claude, Gemini, DeepSeek, Kimi, Qwen and GLM. No vendor lock-in.
+ **AI-to-AI handshake** — Two agents learn I-Lang, they handshake, they collaborate. No middleware needed.
+ **Behavioral DNA** — Declarations define traits and anti-patterns that persist across sessions and models.

##### Protocol at a Glance

| Component | Count | Purpose |
|-----------|-------|---------|
| Verbs | 88 | Core operations (READ, WRIT, FMT, FILT, DRFT, FIX, etc.) |
| Greek Aliases | 13 | Single-token shortcuts (phi=FILT, Sigma=MERGE, Omega=OUT) |
| Modifiers | 29 core plus a 20-key media profile | Output control (fmt=, lng=, ton=, sty=, whr=, path=) |
| Entities | 25 (17 addressable, 8 role) | Targets (@SRC, @DST, @PREV, @LOCAL, @GH, @NULL) |

##### Ecosystem

+ **AutoCode** — You say it. AutoCode ships it. 48 skills. Code to deployment in one session. [GitHub](https://github.com/ilang-ai/autocode)
+ **Imprint** — Your AI’s DNA: one skill for memory, compression, onboarding, code review, debugging, planning, progress tracking, testing, git workflow, and SEO. [GitHub](https://github.com/ilang-ai/Imprint)
+ **AI See** — Give AI eyes. `i.ilang.ai/{url}` reads any webpage.

##### Resources

+ [Protocol Specification](https://github.com/ilang-ai/ilang-spec): v4.1 current stable, v5.0 public preview
+ [Dictionary](https://github.com/ilang-ai/ilang-dict): 88 verbs, 29 core modifiers plus a 20-key media profile, 25 entities
+ [Official Website](https://ilang.ai)
+ [Specification](https://ilang.ai/spec/)
+ [HuggingFace Dataset](https://huggingface.co/datasets/i-Lang/iLang-Spec)

##### Origin

I-Lang was designed by Max (@SUN) and co-authored with Claude Opus (@BRO), with review by GPT (@GPT) and Gemini (@GEMINI).

Genesis: 2026-03-04 · v3.0 Final: 2026-04-25 · v4.0 Final: 2026-05-11 · v5.0 Pre: 2026-06 · v4.1 Media Profile: 2026-09-12 · Spec: ilang.ai
