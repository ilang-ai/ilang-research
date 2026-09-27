# T1: f_v5 against what the operator wanted

Events with vectors from at least two models: 393; in scope: 226 (52 corrections about whether or how to act, 174 controls with the weak acceptance label); operator-confirmed truth: 0.

| set | n | exact agreement | 95% CI | five-class agreement | 95% CI |
|---|---|---|---|---|---|
| all in scope | 226 | 27 = 0.1195 | 0.0834 to 0.1682 | 94 = 0.4159 | 0.3536 to 0.4811 |
| corrections | 52 | 9 = 0.1731 | 0.0938 to 0.2973 | 25 = 0.4808 | 0.351 to 0.6131 |
| controls | 174 | 18 = 0.1034 | 0.0664 to 0.1576 | 69 = 0.3966 | 0.3269 to 0.4707 |

Bot baseline on corrections (the mode the bot actually took, where the models could read it): 19 of 52 agree with what the operator wanted.

Disagreements: 199. By the gate that decided the prediction: STEP-4 S band 0.70: 92 (within 0.05: 61), STEP-4 S band 0.85: 54 (within 0.05: 30), STEP-4 S band 0.55: 41 (within 0.05: 21), STEP-4 S band 0.40: 7 (within 0.05: 4), STEP-3 aut<0.30: 3 (within 0.05: 2), STEP-2 evd<0.25: 1 (within 0.05: 1), STEP-5 aut<0.55 cap: 1 (within 0.05: 1).
Result case per §4: **A**.

## Confusion, five classes (truth -> prediction)

- act->act: 30
- act->confirm: 25
- act->hand_over: 1
- ask->act: 7
- ask->ask: 2
- ask->confirm: 8
- confirm->act: 59
- confirm->ask: 1
- confirm->confirm: 61
- confirm->decline_or_stop: 5
- confirm->hand_over: 2
- decline_or_stop->act: 7
- decline_or_stop->confirm: 15
- decline_or_stop->decline_or_stop: 1
- hand_over->act: 2

## Threshold sensitivity (diagnostic only; nothing is changed)

| gate moved | exact agreement |
|---|---|
| STEP-1 sov +0.15-0.05 | 0.1195 |
| STEP-1 sov +0.15+0.05 | 0.1195 |
| STEP-1 ext +0.10-0.05 | 0.1195 |
| STEP-1 ext +0.10+0.05 | 0.115 |
| STEP-1 csq +0.10-0.05 | 0.1195 |
| STEP-1 csq +0.10+0.05 | 0.1195 |
| STEP-1 rev +0.20-0.05 | 0.1195 |
| STEP-1 rev +0.20+0.05 | 0.1195 |
| STEP-2 cer +0.30-0.05 | 0.115 |
| STEP-2 cer +0.30+0.05 | 0.1195 |
| STEP-2 evd +0.25-0.05 | 0.1195 |
| STEP-2 evd +0.25+0.05 | 0.115 |
| STEP-3 aut +0.30-0.05 | 0.1239 |
| STEP-3 aut +0.30+0.05 | 0.115 |
| STEP-4 S +0.85-0.05 | 0.1327 |
| STEP-4 S +0.85+0.05 | 0.1062 |
| STEP-4 S +0.70-0.05 | 0.1195 |
| STEP-4 S +0.70+0.05 | 0.1327 |
| STEP-4 S +0.55-0.05 | 0.1018 |
| STEP-4 S +0.55+0.05 | 0.146 |
| STEP-4 S +0.40-0.05 | 0.1327 |
| STEP-4 S +0.40+0.05 | 0.0796 |
| STEP-4 S +0.25-0.05 | 0.1195 |
| STEP-4 S +0.25+0.05 | 0.1195 |
| STEP-5 aut +0.55-0.05 | 0.1195 |
| STEP-5 aut +0.55+0.05 | 0.1195 |
