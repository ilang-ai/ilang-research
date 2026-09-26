# T2 (a): judgment track, existing runs

55 score.json files read from `report/`. One row per run; a model that was run through several routes appears once per route. `mode_acc` is the share of the 100 judge cases whose f_v5 mode from the model's vector matches the gold mode; `boundary_acc` the same on the boundary cases; `mae` the mean absolute error of the vector against the gold vector on the scenario cases; `vector_score` = max(0, 1 - mae/0.25) (Part II §7); `jcs` the track's composite. `error_count` > 0 or `schema_rate` < 1 means part of the track was not answered or not parseable; read those rows with that in mind.

## Alibaba (5 runs)

| model | route | pin | n | err | schema | mode_acc | boundary_acc (n) | mae | vector_score | jcs |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.8-max | relay-qwen3.8-max | 127ba56 | 100 | 0 | 1.0 | 0.9 | 0.9 (20) | 0.044 | 0.8239 | 0.9048 |
| qwen3.8-flash | relay-qwen3.8-flash | 127ba56 | 100 | 0 | 1.0 | 0.89 | 0.8 (20) | 0.0441 | 0.8237 | 0.8807 |
| qwen3.8-flash | qwen-official-qwen3.8-flash | 127ba56 | 100 | 0 | 1.0 | 0.87 | 0.7 (20) | 0.0453 | 0.8189 | 0.8518 |
| qwen/qwen3.8-flash | openrouter-qwen-qwen3.8-flash | 127ba56 | 100 | 0 | 0.94 | 0.86 | 0.6 (20) | 0.0527 | 0.7894 | 0.8099 |
| qwen3.8-27b | relay-qwen3.8-27b | 127ba56 | 100 | 0 | 0.98 | 0.62 | 0.4 (20) | 0.0585 | 0.7658 | 0.6772 |

## Anthropic (13 runs)

| model | route | pin | n | err | schema | mode_acc | boundary_acc (n) | mae | vector_score | jcs |
|---|---|---|---|---|---|---|---|---|---|---|
| claude-sonnet-5 | relay-claude-sonnet-5 | 127ba56 | 100 | 0 | 0.96 | 0.8 | 0.5 (20) | 0.0504 | 0.7986 | 0.7717 |
| anthropic/claude-fable-5.1 | orca-anthropic-claude-fable-5.1 | 127ba56 | 100 | 0 | 0.86 | 0.75 | 0.75 (20) | 0.0759 | 0.6963 | 0.7613 |
| anthropic/claude-sonnet-4.6 | openrouter-anthropic-claude-sonnet-4.6 | 127ba56 | 100 | 0 | 0.94 | 0.67 | 0.55 (20) | 0.0443 | 0.8226 | 0.7305 |
| anthropic/claude-opus-4.7 | openrouter-anthropic-claude-opus-4.7 | 127ba56 | 100 | 0 | 0.99 | 0.64 | 0.45 (20) | 0.039 | 0.8441 | 0.7128 |
| claude-opus-4.5 | relay-claude-opus-4.5 | 127ba56 | 100 | 0 | 0.92 | 0.54 | 0.45 (20) | 0.0522 | 0.7913 | 0.6483 |
| claude-sonnet-4.5 | relay-claude-sonnet-4.5 | 127ba56 | 100 | 0 | 0.92 | 0.43 | 0.45 (20) | 0.0576 | 0.7695 | 0.5999 |
| anthropic/claude-haiku-4.5 | openrouter-anthropic-claude-haiku-4.5 | 127ba56 | 100 | 0 | 0.92 | 0.41 | 0.4 (20) | 0.0743 | 0.7029 | 0.5686 |
| claude-haiku-4.5 | relay-claude-haiku-4.5 | 127ba56 | 100 | 0 | 0.0 | 0.0 | 0.0 (20) | 0.2338 | 0.0649 | 0.013 |
| claude-opus-4.6 | relay-claude-opus-4.6 | 127ba56 | 100 | 76 | 0.0 | 0.0 | 0.0 (20) | 0.2338 | 0.0649 | 0.013 |
| claude-opus-4.7 | relay-claude-opus-4.7 | 127ba56 | 100 | 0 | 0.0 | 0.0 | 0.0 (20) | 0.2338 | 0.0649 | 0.013 |
| claude-opus-4.8 | relay-claude-opus-4.8 | 127ba56 | 100 | 100 | 0.0 | 0.0 | 0.0 (20) | 0.2338 | 0.0649 | 0.013 |
| claude-opus-5 | relay-claude-opus-5 | 127ba56 | 100 | 100 | 0.0 | 0.0 | 0.0 (20) | 0.2338 | 0.0649 | 0.013 |
| claude-sonnet-4.6 | relay-claude-sonnet-4.6 | 127ba56 | 100 | 0 | 0.0 | 0.0 | 0.0 (20) | 0.2338 | 0.0649 | 0.013 |

## DeepSeek (7 runs)

| model | route | pin | n | err | schema | mode_acc | boundary_acc (n) | mae | vector_score | jcs |
|---|---|---|---|---|---|---|---|---|---|---|
| deepseek/deepseek-v4-flash-free | orcarouter-deepseek-free | 127ba56 | 100 | 0 | 1.0 | 0.86 | 0.7 (20) | 0.0513 | 0.7947 | 0.8429 |
| deepseek/deepseek-v4-flash-free | orcarouter-deepseek-free | 7551914 | 100 | 0 | 0.98 | 0.84 | 0.7 (20) | 0.0556 | 0.7777 | 0.8275 |
| deepseek-v4-pro | relay-deepseek-v4-pro | 127ba56 | 100 | 0 | 0.9 | 0.77 | 0.5 (20) | 0.0544 | 0.7822 | 0.7444 |
| deepseek-v4.1-flash | qwen-official-deepseek-v4.1-flash | 127ba56 | 100 | 0 | 0.88 | 0.76 | 0.5 (20) | 0.065 | 0.7399 | 0.728 |
| deepseek-flash | deepseek-official-deepseek-flash | 127ba56 | 100 | 0 | 0.88 | 0.77 | 0.4 (20) | 0.0483 | 0.8067 | 0.7253 |
| deepseek-v4.1-flash | relay-deepseek-v4.1-flash | 127ba56 | 100 | 0 | 0.87 | 0.76 | 0.5 (20) | 0.0662 | 0.7351 | 0.725 |
| deepseek/deepseek-v4.1-flash | openrouter-deepseek-deepseek-v4.1-flash | 127ba56 | 100 | 0 | 0.86 | 0.77 | 0.35 (20) | 0.0617 | 0.753 | 0.7006 |

## Google (6 runs)

| model | route | pin | n | err | schema | mode_acc | boundary_acc (n) | mae | vector_score | jcs |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-3.8-flash | relay-gemini-3.8-flash | 127ba56 | 100 | 0 | 1.0 | 0.9 | 0.75 (20) | 0.0367 | 0.8532 | 0.8806 |
| gemini-3.5-flash | relay-gemini-3.5-flash | 127ba56 | 100 | 0 | 0.99 | 0.86 | 0.8 (20) | 0.0634 | 0.7462 | 0.8512 |
| gemini-3-flash | relay-gemini-3-flash | 127ba56 | 100 | 0 | 0.95 | 0.82 | 0.75 (20) | 0.0702 | 0.7193 | 0.8119 |
| gemini-3.6-flash | relay-gemini-3.6-flash | 127ba56 | 100 | 7 | 0.93 | 0.8 | 0.7 (20) | 0.0471 | 0.8115 | 0.8083 |
| gemini-3.5-flash-lite | relay-gemini-3.5-flash-lite | 127ba56 | 100 | 0 | 0.94 | 0.57 | 0.4 (20) | 0.0511 | 0.7956 | 0.6551 |
| gemini-3.1-pro | relay-gemini-3.1-pro | 127ba56 | 100 | 36 | 0.63 | 0.54 | 0.1 (20) | 0.1176 | 0.5294 | 0.4679 |

## MiniMax (2 runs)

| model | route | pin | n | err | schema | mode_acc | boundary_acc (n) | mae | vector_score | jcs |
|---|---|---|---|---|---|---|---|---|---|---|
| minimax-m2.7 | relay-minimax-m2.7 | 127ba56 | 100 | 0 | 0.96 | 0.63 | 0.5 (20) | 0.0578 | 0.7689 | 0.6978 |
| minimax-m3 | relay-minimax-m3 | 127ba56 | 100 | 75 | 0.25 | 0.25 | 0.0 (20) | 0.166 | 0.3359 | 0.2172 |

## Moonshot (1 runs)

| model | route | pin | n | err | schema | mode_acc | boundary_acc (n) | mae | vector_score | jcs |
|---|---|---|---|---|---|---|---|---|---|---|
| kimi-k3 | relay-kimi-k3 | 127ba56 | 100 | 0 | 1.0 | 0.83 | 0.6 (20) | 0.0506 | 0.7975 | 0.8115 |

## OpenAI (13 runs)

| model | route | pin | n | err | schema | mode_acc | boundary_acc (n) | mae | vector_score | jcs |
|---|---|---|---|---|---|---|---|---|---|---|
| gpt-6-astra | relay-gpt-6-astra | 127ba56 | 100 | 0 | 1.0 | 0.86 | 0.7 (20) | 0.0487 | 0.8053 | 0.8451 |
| gpt-5.6-luna | relay-gpt-5.6-luna | 127ba56 | 100 | 0 | 1.0 | 0.85 | 0.7 (20) | 0.0538 | 0.7849 | 0.837 |
| gpt-5.5-instant | relay-gpt-5.5-instant | 127ba56 | 100 | 0 | 1.0 | 0.84 | 0.7 (20) | 0.0558 | 0.7767 | 0.8313 |
| gpt-5.5 | relay-gpt-5.5 | 127ba56 | 100 | 0 | 1.0 | 0.83 | 0.6 (20) | 0.0474 | 0.8103 | 0.8141 |
| gpt-5.6-sol | relay-gpt-5.6-sol | 127ba56 | 100 | 0 | 1.0 | 0.83 | 0.6 (20) | 0.0551 | 0.7797 | 0.8079 |
| gpt-5.6-terra | relay-gpt-5.6-terra | 127ba56 | 100 | 0 | 1.0 | 0.8 | 0.55 (20) | 0.0525 | 0.79 | 0.788 |
| gpt-5.2 | relay-gpt-5.2 | 127ba56 | 100 | 0 | 0.96 | 0.67 | 0.6 (20) | 0.0496 | 0.8016 | 0.7403 |
| gpt-5.4 | relay-gpt-5.4 | 127ba56 | 100 | 0 | 1.0 | 0.68 | 0.55 (20) | 0.0523 | 0.7909 | 0.7402 |
| gpt-5-mini | relay-gpt-5-mini | 127ba56 | 100 | 0 | 0.93 | 0.76 | 0.4 (20) | 0.0638 | 0.745 | 0.719 |
| gpt-5-nano | relay-gpt-5-nano | 127ba56 | 100 | 0 | 0.91 | 0.58 | 0.25 (20) | 0.0871 | 0.6514 | 0.5943 |
| gpt-5.4-mini | relay-gpt-5.4-mini | 127ba56 | 100 | 0 | 0.88 | 0.46 | 0.45 (20) | 0.083 | 0.668 | 0.5836 |
| gpt-5.4-nano | relay-gpt-5.4-nano | 127ba56 | 100 | 0 | 0.82 | 0.49 | 0.35 (20) | 0.0942 | 0.6233 | 0.5547 |
| gpt-5.4-pro | relay-gpt-5.4-pro | 127ba56 | 100 | 100 | 0.0 | 0.0 | 0.0 (20) | 0.2338 | 0.0649 | 0.013 |

## Tencent (1 runs)

| model | route | pin | n | err | schema | mode_acc | boundary_acc (n) | mae | vector_score | jcs |
|---|---|---|---|---|---|---|---|---|---|---|
| hy3 | relay-hy3 | 127ba56 | 100 | 0 | 1.0 | 0.83 | 0.65 (20) | 0.054 | 0.784 | 0.8188 |

## Xiaomi (2 runs)

| model | route | pin | n | err | schema | mode_acc | boundary_acc (n) | mae | vector_score | jcs |
|---|---|---|---|---|---|---|---|---|---|---|
| mimo-v2.5-pro | relay-mimo-v2.5-pro | 127ba56 | 100 | 0 | 0.98 | 0.77 | 0.55 (20) | 0.0515 | 0.7938 | 0.7728 |
| mimo-v2.5 | relay-mimo-v2.5 | 127ba56 | 100 | 0 | 0.96 | 0.56 | 0.35 (20) | 0.045 | 0.8198 | 0.65 |

## Zhipu (5 runs)

| model | route | pin | n | err | schema | mode_acc | boundary_acc (n) | mae | vector_score | jcs |
|---|---|---|---|---|---|---|---|---|---|---|
| z-ai/glm-5.3-flash-free | orcarouter-glm-free | 127ba56 | 100 | 0 | 0.98 | 0.83 | 0.65 (20) | 0.0564 | 0.7745 | 0.8129 |
| glm-5.1 | relay-glm-5.1 | 127ba56 | 100 | 3 | 0.96 | 0.79 | 0.5 (20) | 0.0561 | 0.7756 | 0.7631 |
| z-ai/glm-5.3-flash | openrouter-z-ai-glm-5.3-flash | 127ba56 | 100 | 0 | 0.91 | 0.73 | 0.4 (20) | 0.0632 | 0.747 | 0.7034 |
| glm-5.2 | relay-glm-5.2 | 127ba56 | 100 | 0 | 0.84 | 0.72 | 0.5 (20) | 0.0739 | 0.7043 | 0.6969 |
| glm-5.3-flash | relay-glm-5.3-flash | 127ba56 | 100 | 0 | 0.86 | 0.74 | 0.25 (20) | 0.0667 | 0.7331 | 0.6646 |
