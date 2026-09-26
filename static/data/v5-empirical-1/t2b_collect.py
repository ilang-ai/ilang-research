#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T2 (b): does weighted measurement beat a plain average and the best single model?

    python3 t2b_collect.py --conformance ../../../../ilang-conformance \
        --run orcarouter-deepseek-free-2026... --run relay-qwen3.8-max-2026... [...] --out .

Reads the raw judge records of each run (the model's ::JUDGE block for the 40 scenario cases of
cases/judge/02-scenario-to-vector.jsonl), parses them with the vendored reference validator,
and compares three compositions against the hand-written gold vectors:

  1. the best single model (chosen on all 40 cases, so an optimistic baseline, and also the
     model with the best prior conformance vector_score, which does not peek);
  2. the plain average of the parsed vectors;
  3. the weighted average, where the weight of each model on case c is computed only from the
     other 39 cases: w_m = max(0, 1 - MAE_m(others)/0.25) normalised to sum 1 with a floor of 0.01
     (WEIGHTS-VECTOR-1; the same shape as WEIGHTS-TRACK-1 of T1).

Reported per composition: mean absolute error against the gold vector, and f_v5 mode accuracy
against f_v5(gold). Every parsed vector is saved. Standard library only."""
import argparse
import json
import os
import sys


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    z2 = z * z
    centre = (p + z2 / (2 * n)) / (1 + z2 / n)
    half = z * ((p * (1 - p) / n + z2 / (4 * n * n)) ** 0.5) / (1 + z2 / n)
    return (round(centre - half, 4), round(centre + half, 4))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conformance", required=True)
    ap.add_argument("--run", action="append", required=True, help="run directory name under runs/")
    ap.add_argument("--out", default=".")
    ap.add_argument("--prior", default="t2a-judge-track.tsv", help="T2 (a) table for the no-peek baseline")
    a = ap.parse_args()
    sys.path.insert(0, os.path.join(a.conformance, "vendor"))
    import ilang_judge_validator as jv   # the pinned reference validator: f_v5 and the JUDGE parser

    cases = {}
    with open(os.path.join(a.conformance, "cases", "judge", "02-scenario-to-vector.jsonl"), encoding="utf-8") as f:
        for line in f:
            if line.strip():
                c = json.loads(line)
                cases[c["id"]] = c
    ids = sorted(cases)
    gold = {i: {d: float(cases[i]["gold_v"][d]) for d in jv.DIMS} for i in ids}
    gold_mode = {i: jv.f_v5(gold[i]) for i in ids}

    vectors, models = {}, []
    for run in a.run:
        rdir = os.path.join(a.conformance, "runs", run, "judge")
        model = run.rsplit("-", 2)[0]
        models.append(model)
        vectors[model] = {}
        for i in ids:
            path = os.path.join(rdir, i + ".json")
            if not os.path.exists(path):
                continue
            rec = json.load(open(path, encoding="utf-8"))
            text = (rec.get("text") or "").strip()
            block = [ln for ln in text.splitlines() if ln.strip()]
            start = next((k for k, ln in enumerate(block) if ln.strip() == jv.HEADER), None)
            if start is None or len(block) < start + 4:
                continue
            try:
                vec, mode, conf, _ = jv.parse_judge_block(block[start:start + 4])
            except ValueError:
                continue
            vectors[model][i] = {"v": vec, "declared_mode": mode, "response_model": rec.get("response_model")}

    def mae(v, g):
        return sum(abs(v[d] - g[d]) for d in jv.DIMS) / len(jv.DIMS)

    common = [i for i in ids if all(i in vectors[m] for m in models)]
    rows, per_model = [], {}
    for m in models:
        errs = [mae(vectors[m][i]["v"], gold[i]) for i in common]
        hits = sum(jv.f_v5(vectors[m][i]["v"]) == gold_mode[i] for i in common)
        per_model[m] = {"n": len(common), "parsed": len(vectors[m]), "mae": round(sum(errs) / len(errs), 4),
                        "mode_hits": hits, "mode_acc": round(hits / len(common), 4), "ci": wilson(hits, len(common))}

    def compose(weights_fn):
        errs, hits = [], 0
        for i in common:
            w = weights_fn(i)
            v = {d: round(sum(w[m] * vectors[m][i]["v"][d] for m in models), 4) for d in jv.DIMS}
            errs.append(mae(v, gold[i]))
            hits += jv.f_v5(v) == gold_mode[i]
        return {"n": len(common), "mae": round(sum(errs) / len(errs), 4), "mode_hits": hits,
                "mode_acc": round(hits / len(common), 4), "ci": wilson(hits, len(common))}

    plain = compose(lambda i: {m: 1 / len(models) for m in models})

    def loo_weights(i):
        raw = {}
        for m in models:
            others = [c for c in common if c != i]
            e = sum(mae(vectors[m][c]["v"], gold[c]) for c in others) / len(others)
            raw[m] = max(0.0, 1 - e / 0.25)
        total = sum(raw.values()) or 1.0
        w = {m: max(0.01, raw[m] / total) for m in models}
        total = sum(w.values())
        return {m: w[m] / total for m in models}

    weighted = compose(loo_weights)
    best_peek = min(models, key=lambda m: per_model[m]["mae"])
    prior = {}
    if os.path.exists(a.prior):
        with open(a.prior, encoding="utf-8") as f:
            head = f.readline().rstrip("\n").split("\t")
            for line in f:
                r = dict(zip(head, line.rstrip("\n").split("\t")))
                prior[r["vendor_route"]] = float(r["vector_score"] or 0)
    best_prior = max(models, key=lambda m: prior.get(m, 0)) if prior else None

    result = {"cases": len(common), "models": models, "per_model": per_model, "plain_average": plain,
              "weighted_average_loo": weighted, "best_single_by_mae_on_these_cases": best_peek,
              "best_single_by_prior_vector_score": best_prior,
              "weights_formula": "WEIGHTS-VECTOR-1: w_m = max(0, 1 - MAE_m(other 39 cases)/0.25), normalised, floor 0.01, renormalised",
              "gold_mode_is": "f_v5(gold vector)"}
    os.makedirs(a.out, exist_ok=True)
    json.dump(result, open(os.path.join(a.out, "t2b-result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    with open(os.path.join(a.out, "t2b-vectors.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for m in models:
            for i in ids:
                if i in vectors[m]:
                    f.write(json.dumps({"model": m, "case": i, **vectors[m][i], "gold_v": gold[i], "gold_mode": gold_mode[i]}, ensure_ascii=False) + "\n")
    lines = ["# T2 (b): weighted measurement against a plain average and the best single model", "",
             f"{len(common)} scenario cases answered by all {len(models)} models (of 40). Gold vector: hand-written; gold mode: f_v5(gold).",
             "", "| composition | MAE | f_v5 mode accuracy | 95% CI (Wilson) |", "|---|---|---|---|"]
    for m in models:
        r = per_model[m]
        lines.append(f"| {m} | {r['mae']} | {r['mode_hits']}/{r['n']} = {r['mode_acc']} | {r['ci'][0]} to {r['ci'][1]} |")
    lines.append(f"| plain average | {plain['mae']} | {plain['mode_hits']}/{plain['n']} = {plain['mode_acc']} | {plain['ci'][0]} to {plain['ci'][1]} |")
    lines.append(f"| weighted average, leave-one-out weights | {weighted['mae']} | {weighted['mode_hits']}/{weighted['n']} = {weighted['mode_acc']} | {weighted['ci'][0]} to {weighted['ci'][1]} |")
    lines += ["", f"Best single model by MAE on these cases (peeks): {best_peek}. Best single model by prior conformance vector_score (no peek): {best_prior}.",
              "", result["weights_formula"] + "."]
    open(os.path.join(a.out, "t2b-result.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print(json.dumps({k: result[k] for k in ("cases", "plain_average", "weighted_average_loo", "best_single_by_mae_on_these_cases", "best_single_by_prior_vector_score")}, ensure_ascii=False))
    for m in models:
        print(m, per_model[m])


if __name__ == "__main__":
    main()
