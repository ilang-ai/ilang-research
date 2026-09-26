---
title: "Anchor Examples v1"
date: 2026-09-26
summary: "One hundred anchor scenarios for ten dimensions of the iLang v5.0 judgment vector: five levels per dimension, one Chinese and one English sentence each, drafted by Meta's Muse agent from the canon's definitions and reviewed by the authors (nine changes). The open set of Part II §5, published here because the canon's v5.0 text is sealed."
tags: ["dataset", "anchors", "judgment", "labeling", "iLang", "v5.0"]
author: "Long Quan Zhu"
---

## Download

The set is at [`/data/anchor-examples-v1/`](/data/anchor-examples-v1/): [`anchors.jsonl`](/data/anchor-examples-v1/anchors.jsonl) for machines, [`anchor-examples-v1.1-2026-09-26.md`](/data/anchor-examples-v1/anchor-examples-v1.1-2026-09-26.md) in the canon's `::CASE` form, the [README](/data/anchor-examples-v1/README.md), the draft as delivered and the review record.

## Quick facts

- **Scope**: the ten dimensions the canon left unanchored (`int`, `cap`, `csq`, `rel`, `cer`, `aut`, `evd`, `sov`, `ine`, `ext`); `rev` is anchored in the canon itself and was the pattern
- **Shape**: 5 anchors × 2 languages × 10 dimensions = 100 sentences, 30 to 120 characters, no real names or brands
- **Provenance**: drafted 2026-09-26 by Meta's Muse agent (`Muse Spark`) from an engineering book; reviewed by the authors, nine changes recorded
- **Status**: open set (Part II §5 `anchor_examples`), not part of the sealed canon; untested against labelers or models so far

## Why it is worth reading

The judgment vector is only as good as the scale each dimension is read on. The canon fixed the two ends of every dimension and wrote out the full five-level scale for one of them. This set writes the other ten in the same form, so that a labeler or a model rates every dimension against the same kind of sentence. Two of the drafted anchors turned out to describe a neighbouring dimension rather than their own, which is exactly the failure the single-salient-dimension rule exists to catch; the review record shows both.
