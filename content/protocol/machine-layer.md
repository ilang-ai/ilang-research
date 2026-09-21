---
title: "IML — the I-Lang Machine Layer"
date: 2026-09-21
url: /protocol/machine-layer/
tags: ["I-Lang", "IML", "protocol", "machine layer", "AI-to-AI"]
author: "SUN"
description: "IML is a machine form of I-Lang v4.x declarations: fixed-width codes derived from the canon, for agent-to-agent transport. Experimental, versioned at 0.5.1, MIT."
---

##### Repository

[github.com/ilang-ai/iml-protocol](https://github.com/ilang-ai/iml-protocol) · concept DOI [10.5281/zenodo.22823285](https://doi.org/10.5281/zenodo.22823285) · MIT

##### What it is

IML (I-Lang Machine Layer) renders the declaration layer of I-Lang v4.x as fixed-width codes: 49 codes covering the declaration set, each derived from the canon rather than invented beside it, with a digest so a receiver can check which table it is reading. It is meant for the leg between two machines, where a human reader is not the audience and a stable width is worth more than readability.

It is **experimental and not part of the canon**. The canon stayed untouched when IML was built; what moved was the declaration layer's representation, not its definition. Version 0.5.1 is the current and, for now, the final release: the line reopens when there are real users or when the canon settles the field syntax it would depend on.

##### What it does not claim

IML is not lossless compression and it does not save tokens — in the current tables an IML document is longer than the I-Lang document it encodes. That is stated in the repository's own README, and it is stated here for the same reason: the machine layer exists for determinism at the boundary between agents, not for a smaller bill.

##### Related

The canon itself: [ilang-ai/ilang-spec](https://github.com/ilang-ai/ilang-spec), concept DOI [10.5281/zenodo.21821452](https://doi.org/10.5281/zenodo.21821452). Conformance measurement of the canon: [I-Lang Conformance Results v1](/datasets/ilang-conformance/).
