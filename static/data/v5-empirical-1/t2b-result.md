# T2 (b): weighted measurement against a plain average and the best single model

37 scenario cases answered by all 5 models (of 40). Gold vector: hand-written; gold mode: f_v5(gold).

| composition | MAE | f_v5 mode accuracy | 95% CI (Wilson) |
|---|---|---|---|
| relay-qwen3.8-max | 0.0998 | 26/37 = 0.7027 | 0.5422 to 0.8251 |
| relay-gemini-3.8-flash | 0.0989 | 28/37 = 0.7568 | 0.5988 to 0.8664 |
| relay-gpt-6-astra | 0.1256 | 22/37 = 0.5946 | 0.4349 to 0.7365 |
| orcarouter-deepseek-free | 0.1324 | 20/37 = 0.5405 | 0.3838 to 0.6896 |
| relay-hy3 | 0.1353 | 19/37 = 0.5135 | 0.3589 to 0.6655 |
| plain average | 0.1043 | 22/37 = 0.5946 | 0.4349 to 0.7365 |
| weighted average, leave-one-out weights | 0.1027 | 22/37 = 0.5946 | 0.4349 to 0.7365 |

Best single model by MAE on these cases (peeks): relay-gemini-3.8-flash. Best single model by prior conformance vector_score (no peek): relay-gemini-3.8-flash.

WEIGHTS-VECTOR-1: w_m = max(0, 1 - MAE_m(other 39 cases)/0.25), normalised, floor 0.01, renormalised.
