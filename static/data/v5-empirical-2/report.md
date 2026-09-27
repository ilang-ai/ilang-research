# T1: f_v5 against what the operator wanted

Events with vectors from at least two models: 393; in scope: 243 (70 corrections about whether or how to act, 173 controls with the weak acceptance label); operator-confirmed truth: 9.

| set | n | exact agreement | 95% CI | five-class agreement | 95% CI |
|---|---|---|---|---|---|
| all in scope | 243 | 25 = 0.1029 | 0.0707 to 0.1475 | 101 = 0.4156 | 0.3555 to 0.4784 |
| corrections | 70 | 11 = 0.1571 | 0.0901 to 0.2599 | 36 = 0.5143 | 0.3995 to 0.6275 |
| controls | 173 | 14 = 0.0809 | 0.0488 to 0.1312 | 65 = 0.3757 | 0.307 to 0.4499 |

Bot baseline on corrections (the mode the bot actually took, where the models could read it): 34 of 70 agree with what the operator wanted.

Disagreements: 218. By the gate that decided the prediction: STEP-4 S band 0.70: 110 (within 0.05: 79), STEP-4 S band 0.85: 53 (within 0.05: 41), STEP-4 S band 0.55: 34 (within 0.05: 24), STEP-4 S band 0.40: 14 (within 0.05: 10), STEP-3 aut<0.30: 3 (within 0.05: 3), STEP-5 aut<0.55 cap: 2 (within 0.05: 2), STEP-2 evd<0.25: 1 (within 0.05: 1), STEP-1 ext<0.10: 1 (within 0.05: 1).
Result case per §4: **A**.

## Confusion, five classes (truth -> prediction)

- act->act: 37
- act->confirm: 23
- ask->act: 11
- ask->ask: 1
- ask->confirm: 5
- confirm->act: 62
- confirm->ask: 1
- confirm->confirm: 63
- confirm->decline_or_stop: 11
- confirm->hand_over: 3
- decline_or_stop->act: 10
- decline_or_stop->confirm: 14
- hand_over->act: 1
- hand_over->confirm: 1

## Threshold sensitivity (diagnostic only; nothing is changed)

| gate moved | exact agreement |
|---|---|
| STEP-1 sov +0.15-0.05 | 0.1029 |
| STEP-1 sov +0.15+0.05 | 0.1029 |
| STEP-1 ext +0.10-0.05 | 0.1029 |
| STEP-1 ext +0.10+0.05 | 0.1029 |
| STEP-1 csq +0.10-0.05 | 0.1029 |
| STEP-1 csq +0.10+0.05 | 0.1029 |
| STEP-1 rev +0.20-0.05 | 0.1029 |
| STEP-1 rev +0.20+0.05 | 0.1029 |
| STEP-2 cer +0.30-0.05 | 0.0988 |
| STEP-2 cer +0.30+0.05 | 0.1029 |
| STEP-2 evd +0.25-0.05 | 0.1029 |
| STEP-2 evd +0.25+0.05 | 0.1029 |
| STEP-3 aut +0.30-0.05 | 0.1152 |
| STEP-3 aut +0.30+0.05 | 0.0988 |
| STEP-4 S +0.85-0.05 | 0.1399 |
| STEP-4 S +0.85+0.05 | 0.0864 |
| STEP-4 S +0.70-0.05 | 0.1029 |
| STEP-4 S +0.70+0.05 | 0.1029 |
| STEP-4 S +0.55-0.05 | 0.0947 |
| STEP-4 S +0.55+0.05 | 0.1481 |
| STEP-4 S +0.40-0.05 | 0.1317 |
| STEP-4 S +0.40+0.05 | 0.0782 |
| STEP-4 S +0.25-0.05 | 0.1029 |
| STEP-4 S +0.25+0.05 | 0.1029 |
| STEP-5 aut +0.55-0.05 | 0.0988 |
| STEP-5 aut +0.55+0.05 | 0.0947 |
