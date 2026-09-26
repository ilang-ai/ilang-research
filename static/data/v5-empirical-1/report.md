# T1: f_v5 against what the operator wanted

Events with vectors from at least two models: 442; in scope: 157 (45 corrections about whether or how to act, 112 controls with the weak acceptance label); operator-confirmed truth: 0.

| set | n | exact agreement | 95% CI | five-class agreement | 95% CI |
|---|---|---|---|---|---|
| all in scope | 157 | 5 = 0.0318 | 0.0137 to 0.0724 | 60 = 0.3822 | 0.3098 to 0.4601 |
| corrections | 45 | 2 = 0.0444 | 0.0123 to 0.1483 | 11 = 0.2444 | 0.1424 to 0.3867 |
| controls | 112 | 3 = 0.0268 | 0.0092 to 0.0758 | 49 = 0.4375 | 0.3492 to 0.5299 |

Bot baseline on corrections (the mode the bot actually took, where the models could read it): 7 of 30 agree with what the operator wanted.

Disagreements: 152. By the gate that decided the prediction: STEP-4 S band 0.70: 68 (within 0.05: 47), STEP-4 S band 0.85: 50 (within 0.05: 35), STEP-4 S band 0.55: 17 (within 0.05: 12), STEP-2 cer<0.30: 10 (within 0.05: 5), STEP-5 aut<0.55 cap: 5 (within 0.05: 1), STEP-3 aut<0.30: 1 (within 0.05: 1), STEP-4 S band 0.40: 1 (within 0.05: 1).
Result case per §4: **A**.

## Confusion, five classes (truth -> prediction)

- act->act: 54
- act->ask: 5
- act->confirm: 36
- act->hand_over: 1
- ask->act: 2
- ask->ask: 1
- ask->confirm: 1
- confirm->act: 38
- confirm->ask: 2
- confirm->confirm: 5
- decline_or_stop->act: 2
- decline_or_stop->ask: 3
- decline_or_stop->confirm: 3
- hand_over->act: 2
- hand_over->confirm: 2

## Threshold sensitivity (diagnostic only; nothing is changed)

| gate moved | exact agreement |
|---|---|
| STEP-1 sov +0.15-0.05 | 0.0318 |
| STEP-1 sov +0.15+0.05 | 0.0318 |
| STEP-1 ext +0.10-0.05 | 0.0318 |
| STEP-1 ext +0.10+0.05 | 0.0318 |
| STEP-1 csq +0.10-0.05 | 0.0318 |
| STEP-1 csq +0.10+0.05 | 0.0318 |
| STEP-1 rev +0.20-0.05 | 0.0318 |
| STEP-1 rev +0.20+0.05 | 0.0318 |
| STEP-2 cer +0.30-0.05 | 0.0318 |
| STEP-2 cer +0.30+0.05 | 0.0318 |
| STEP-2 evd +0.25-0.05 | 0.0318 |
| STEP-2 evd +0.25+0.05 | 0.0318 |
| STEP-3 aut +0.30-0.05 | 0.0318 |
| STEP-3 aut +0.30+0.05 | 0.0318 |
| STEP-4 S +0.85-0.05 | 0.1592 |
| STEP-4 S +0.85+0.05 | 0.0127 |
| STEP-4 S +0.70-0.05 | 0.0318 |
| STEP-4 S +0.70+0.05 | 0.0446 |
| STEP-4 S +0.55-0.05 | 0.0318 |
| STEP-4 S +0.55+0.05 | 0.0382 |
| STEP-4 S +0.40-0.05 | 0.0318 |
| STEP-4 S +0.40+0.05 | 0.0318 |
| STEP-4 S +0.25-0.05 | 0.0318 |
| STEP-4 S +0.25+0.05 | 0.0318 |
| STEP-5 aut +0.55-0.05 | 0.0318 |
| STEP-5 aut +0.55+0.05 | 0.0382 |
