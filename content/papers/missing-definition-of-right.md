---
title: "The Missing Definition of Right: An Axiomatic Protocol for AI Judgment, with Conformance and Production Evidence"
date: 2026-09-21
url: /papers/missing-definition-of-right/
tags: ["AI hallucination","AI judgment","LLM evaluation","protocol conformance","structured hallucination","I-Lang"]
author: "SUN"
description: "Hallucination is a specification problem, not a precision problem. With four axioms, an eleven-dimension judgment vector and a fixed decision function defining what is right, 45 model deployments largely master protocol form (median 0.80) and fail protocol action (median 0.09); an inexpensive judge held to the definition agrees with written rules 68.4% → 80.9% in production. Preprint v1.1, DOI 10.5281/zenodo.22882691."
---

##### Download

+ [PDF (preprint v1.1, 9 pages)](/The_Missing_Definition_of_Right_v1_1.pdf)
+ [LaTeX source](/The_Missing_Definition_of_Right_v1_1_latex_source.zip)

**DOI:** [10.5281/zenodo.22882691](https://doi.org/10.5281/zenodo.22882691) (this version) · [10.5281/zenodo.22882690](https://doi.org/10.5281/zenodo.22882690) (all versions) · License CC BY 4.0

##### Abstract

Large language models are optimised to produce the most probable continuation. Nothing in that objective says which continuation is *right*, and no amount of added precision supplies the missing definition. We argue that hallucination is therefore not primarily a precision problem but a specification problem, and that it becomes measurable — and correctable — only once "right" is written down in a form a machine can be held to. I-Lang is such a form. Its judgment layer rests on four axioms (no rule carries weight 0 or 1; an irreversibility gate; consistency detection; conservation of externality), an eleven-dimension judgment vector with a uniform polarity convention, and a fixed, total reference function from vector to one of eight decision modes. Perception is learned; the decision is specified. We test what follows from this definition in two settings. In a deterministic 320-case conformance benchmark run on 45 model deployments, protocol form is largely attainable (median grammar pass rate 0.80) while protocol action is not (median execution pass rate 0.09; seven of 34 comparable runs score exactly zero), eleven runs emit perfectly valid judgment schemas yet nine of them fail most execution cases, and 93.3% of all rule violations fall on a single rule: acting with authority one does not hold. No run reaches the conformance gate. In three days of production, an inexpensive judge model placed under the protocol agrees with the operator's written rules on 68.4%, 75.1% and 80.9% of an unbiased sample, and on 87.2% of messages where it reports confidence of at least 0.85; after one rule constant was changed, deviations from that rule fell from 13 to 7 under a single, fixed criterion. The axioms, the benchmark, both result sets and the code are public and archived with DOIs. We ask readers not to trust our numbers but to re-run them.

##### Key Contributions

+ A formal definition of right action for AI agents — four axioms with explicit functional forms, an eleven-dimension judgment vector and a deterministic decision function — published in the I-Lang canon before any measurement
+ A deterministic 320-case conformance benchmark that turns the definition into three separate error signals (form, action, judgment), with results for 45 model deployments
+ A production audit of an inexpensive judge held to the definition, including a worked correction of an improvement that a changed measurement criterion would otherwise have fabricated
+ Everything needed to check the paper, archived with DOIs and reproducible in three commands

##### Data and Code

| Artifact | Where |
|---|---|
| Conformance results (45 runs) | [I-Lang Conformance Results v1](/datasets/ilang-conformance/) |
| Production audit | [Judgment Layer Audit v1](/datasets/judgment-layer-audit/) |
| Decision-layer learnability | [Judgment Learnability v1](/datasets/judgment-learnability/) |
| Benchmark code and corpus | [ilang-conformance](https://github.com/ilang-ai/ilang-conformance), DOI [10.5281/zenodo.22864929](https://doi.org/10.5281/zenodo.22864929) |
| The axioms and the judgment layer | [I-Lang canon](https://github.com/ilang-ai/ilang-spec), DOI [10.5281/zenodo.21821452](https://doi.org/10.5281/zenodo.21821452) |

##### Cite

Zhu, L. Q. (2026). *The Missing Definition of Right: An Axiomatic Protocol for AI Judgment, with Conformance and Production Evidence* (preprint v1.1). Zenodo. https://doi.org/10.5281/zenodo.22882691

##### Related

This paper supplies the formal object and the data that the earlier argument lacked: [The Inductive Dilemma of AI Hallucination](/papers/ai-hallucination/).
