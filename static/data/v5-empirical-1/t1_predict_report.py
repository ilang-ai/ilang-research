#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1 steps 4 to 5 and the report: merge the models' vectors, run f_v5, compare with what the
operator wanted, and apply the result rules of the seal book §4.

    python3 t1_predict_report.py --conformance ../../../../ilang-conformance \
        --vendor orcarouter-deepseek-free --vendor relay-qwen3.8-max ... \
        [--confirmed confirmed.jsonl] --out .

Vectors: per event, the weighted average of the models' parsed vectors (weights WEIGHTS-VECTOR-1:
each model's vector_score on the conformance scenario cases, max(0, 1 - MAE/0.25) as in Part II
§7, normalised, floor 0.01), rounded to two decimals. Prediction: f_v5 of that vector, with the
step that decided and the distance to the nearest gate, computed with the pinned validator's
constants and checked against its f_v5.

Truth: the operator's confirmed answer where there is one (confirmed.jsonl from the returned
batch files), else the merged model label (merged.jsonl). Only corrections whose message was
about whether or how to act (targets = do_or_how) and controls (weak label: the bot's mode was
accepted) enter the comparison. Outputs: predictions.jsonl, report.json, report.md."""
import argparse
import collections
import json
import os
import sys

FIVE = {"M1": "act", "M2": "act", "M3": "confirm", "M4": "confirm", "M5": "ask", "M6": "hand_over", "M7": "decline_or_stop", "M8": "decline_or_stop"}
GATES = [("STEP-1", "sov", 0.15, "lt"), ("STEP-1", "ext", 0.10, "lt"), ("STEP-1", "csq", 0.10, "lt"), ("STEP-1", "rev", 0.20, "lt"),
         ("STEP-2", "cer", 0.30, "lt"), ("STEP-2", "evd", 0.25, "lt"), ("STEP-3", "aut", 0.30, "lt"),
         ("STEP-4", "S", 0.85, "band"), ("STEP-4", "S", 0.70, "band"), ("STEP-4", "S", 0.55, "band"), ("STEP-4", "S", 0.40, "band"), ("STEP-4", "S", 0.25, "band"),
         ("STEP-5", "aut", 0.55, "lt")]


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    z2 = z * z
    c = (p + z2 / (2 * n)) / (1 + z2 / n)
    h = z * ((p * (1 - p) / n + z2 / (4 * n * n)) ** 0.5) / (1 + z2 / n)
    return (round(c - h, 4), round(c + h, 4))


def f_v5_traced(x, th, weights):
    """f_v5 with the deciding step and the margin to the gate that decided (negative = inside)."""
    if x["sov"] < th["sov_survival"]:
        return "M8", "STEP-1 sov<0.15", x["sov"] - th["sov_survival"], None
    if x["ext"] < th["ext_survival"]:
        return "M8", "STEP-1 ext<0.10", x["ext"] - th["ext_survival"], None
    if x["csq"] < th["csq_survival"] and x["rev"] < th["rev_survival"]:
        return "M8", "STEP-1 csq<0.10 & rev<0.20", max(x["csq"] - th["csq_survival"], x["rev"] - th["rev_survival"]), None
    if x["cer"] < th["cer_gate"]:
        return "M5", "STEP-2 cer<0.30", x["cer"] - th["cer_gate"], None
    if x["evd"] < th["evd_gate"]:
        return "M5", "STEP-2 evd<0.25", x["evd"] - th["evd_gate"], None
    if x["aut"] < th["aut_gate"]:
        return "M6", "STEP-3 aut<0.30", x["aut"] - th["aut_gate"], None
    s = round(sum(weights[d] * x[d] for d in weights), 4)
    edges = [(th["b_m1"], "M1"), (th["b_m2"], "M2"), (th["b_m3"], "M3"), (th["b_m4"], "M4"), (th["b_m7"], "M7")]
    mode = "M8"
    for edge, m in edges:
        if s > edge:
            mode = m
            break
    nearest = min((abs(s - e), e) for e, _ in edges)
    step = "STEP-4 S band %.2f" % nearest[1]
    if x["aut"] < th["aut_cap"] and mode in ("M1", "M2"):
        return "M3", "STEP-5 aut<0.55 cap", x["aut"] - th["aut_cap"], s
    return mode, step, nearest[0], s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conformance", required=True)
    ap.add_argument("--events", default="events.jsonl")
    ap.add_argument("--merged", default="merged.jsonl")
    ap.add_argument("--vendor", action="append", required=True)
    ap.add_argument("--prior", default="t2a-judge-track.tsv")
    ap.add_argument("--confirmed", default=None)
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    sys.path.insert(0, os.path.join(os.path.abspath(a.conformance), "vendor"))
    import ilang_judge_validator as jv
    th, W = jv.TH, jv.WEIGHTS

    events = {e["id"]: e for e in (json.loads(l) for l in open(a.events, encoding="utf-8") if l.strip())}
    merged = {m["id"]: m for m in (json.loads(l) for l in open(a.merged, encoding="utf-8") if l.strip())}
    confirmed = {}
    if a.confirmed and os.path.exists(a.confirmed):
        for l in open(a.confirmed, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                confirmed[r["id"]] = r
    vscore = {}
    with open(a.prior, encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        for line in f:
            r = dict(zip(head, line.rstrip("\n").split("\t")))
            vscore[r["vendor_route"]] = float(r["vector_score"] or 0)
    vectors = {v: {} for v in a.vendor}
    for v in a.vendor:
        d = os.path.join(a.out, "vectors", v)
        for name in os.listdir(d) if os.path.isdir(d) else []:
            r = json.load(open(os.path.join(d, name), encoding="utf-8"))
            if r.get("status") == "ok" and r.get("parsed"):
                vectors[v][r["id"]] = r["parsed"]["v"]

    preds = []
    for eid, e in sorted(events.items()):
        have = [v for v in a.vendor if eid in vectors[v]]
        if len(have) < 2:
            continue
        raw = {v: max(vscore.get(v, 0.0), 0.0) for v in have}
        tot = sum(raw.values()) or 1.0
        w = {v: max(0.01, raw[v] / tot) for v in have}
        tot = sum(w.values())
        w = {v: w[v] / tot for v in have}
        vec = {d: round(sum(w[v] * vectors[v][eid][d] for v in have), 2) for d in jv.DIMS}
        mode, step, margin, s = f_v5_traced(vec, th, W)
        assert mode == jv.f_v5(vec), (eid, mode, jv.f_v5(vec))
        m = merged.get(eid, {})
        c = confirmed.get(eid)
        if c:
            truth, truth_src = c.get("operator_mode"), "operator"
        elif e["kind"] == "control":
            truth, truth_src = m.get("bot_mode"), "model_consensus_weak_accept"
        else:
            truth, truth_src = m.get("intended_mode"), "model_consensus"
        in_scope = (e["kind"] == "control" and truth in FIVE) or (
            e["kind"] == "correction" and (c or m.get("targets") == "do_or_how") and truth in FIVE)
        preds.append({"id": eid, "source": e["source"], "kind": e["kind"], "vector": vec, "weights": {v: round(w[v], 4) for v in have},
                      "pred_mode": mode, "deciding": step, "margin": round(margin, 4), "S": s,
                      "truth": truth, "truth_source": truth_src, "bot_mode": m.get("bot_mode"), "targets": m.get("targets"),
                      "in_scope": in_scope, "none_fits": bool(c and c.get("none_fits"))})
    with open(os.path.join(a.out, "predictions.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for p in preds:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    def agreement(rows):
        n = len(rows)
        k = sum(r["pred_mode"] == r["truth"] for r in rows)
        k5 = sum(FIVE[r["pred_mode"]] == FIVE[r["truth"]] for r in rows)
        return {"n": n, "exact": k, "exact_rate": round(k / n, 4) if n else None, "exact_ci": wilson(k, n),
                "five_class": k5, "five_class_rate": round(k5 / n, 4) if n else None, "five_class_ci": wilson(k5, n)}

    scope = [p for p in preds if p["in_scope"]]
    corr = [p for p in scope if p["kind"] == "correction"]
    ctrl = [p for p in scope if p["kind"] == "control"]
    rep = {"events_with_vectors": len(preds), "in_scope": len(scope), "corrections_in_scope": len(corr), "controls": len(ctrl),
           "operator_confirmed": sum(p["truth_source"] == "operator" for p in scope),
           "agreement_all": agreement(scope), "agreement_corrections": agreement(corr), "agreement_controls": agreement(ctrl)}
    base_rows = [p for p in corr if p["bot_mode"] in FIVE]
    rep["bot_baseline_corrections"] = {"n": len(base_rows), "exact": sum(p["bot_mode"] == p["truth"] for p in base_rows),
                                       "note": "controls are the bot's own mode by construction (weak label), so their baseline is 1 by definition"}
    conf8 = collections.Counter((p["truth"], p["pred_mode"]) for p in scope)
    conf5 = collections.Counter((FIVE[p["truth"]], FIVE[p["pred_mode"]]) for p in scope)
    rep["confusion_8x8"] = {f"{t}->{p}": n for (t, p), n in sorted(conf8.items())}
    rep["confusion_5x5"] = {f"{t}->{p}": n for (t, p), n in sorted(conf5.items())}
    dis = [p for p in scope if p["pred_mode"] != p["truth"]]
    by_gate = collections.Counter(p["deciding"] for p in dis)
    near = {g: sum(abs(p["margin"]) <= 0.05 for p in dis if p["deciding"] == g) for g in by_gate}
    rep["disagreements"] = {"n": len(dis), "by_deciding_gate": dict(by_gate.most_common()), "within_0.05_of_that_gate": near,
                            "margin_distribution": sorted(round(abs(p["margin"]), 2) for p in dis)}
    case = "A"
    for g, n in by_gate.items():
        if dis and n / len(dis) > 1 / 3 and near[g] == n:
            case = "B"
            rep["case_B_gate"] = g
    if any(p["none_fits"] for p in preds):
        case = case + "+C"
    rep["result_case"] = case
    rep["result_rule"] = "CONST-CLUSTER-1/3: a gate that decides more than a third of the disagreements, with every such vector within 0.05 of it, is case B (convention awaiting practice)"
    # threshold sensitivity, diagnostic only
    sens = {}
    for step, dim, val, kind in GATES:
        for delta in (-0.05, 0.05):
            th2 = dict(th)
            key = {("STEP-1", "sov"): "sov_survival", ("STEP-1", "ext"): "ext_survival", ("STEP-1", "csq"): "csq_survival", ("STEP-1", "rev"): "rev_survival",
                   ("STEP-2", "cer"): "cer_gate", ("STEP-2", "evd"): "evd_gate", ("STEP-3", "aut"): "aut_gate", ("STEP-5", "aut"): "aut_cap"}.get((step, dim))
            if kind == "band":
                key = {0.85: "b_m1", 0.70: "b_m2", 0.55: "b_m3", 0.40: "b_m4", 0.25: "b_m7"}[val]
            th2[key] = round(th[key] + delta, 2)
            k = sum(f_v5_traced(p["vector"], th2, W)[0] == p["truth"] for p in scope)
            sens[f"{step} {dim} {val:+.2f}{delta:+.2f}"] = round(k / len(scope), 4) if scope else None
    rep["threshold_sensitivity_exact_rate"] = sens
    rep["reliability_note"] = "label reliability (model consensus vs operator on the 20 % sample) is computed by t1_confirm_parse.py once the batches are back"
    json.dump(rep, open(os.path.join(a.out, "report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    A = rep["agreement_all"]
    lines = ["# T1: f_v5 against what the operator wanted", "",
             f"Events with vectors from at least two models: {len(preds)}; in scope: {len(scope)} ({len(corr)} corrections about whether or how to act, {len(ctrl)} controls with the weak acceptance label); operator-confirmed truth: {rep['operator_confirmed']}.", "",
             "| set | n | exact agreement | 95% CI | five-class agreement | 95% CI |", "|---|---|---|---|---|---|"]
    for name, r in (("all in scope", A), ("corrections", rep["agreement_corrections"]), ("controls", rep["agreement_controls"])):
        lines.append(f"| {name} | {r['n']} | {r['exact']} = {r['exact_rate']} | {r['exact_ci'][0]} to {r['exact_ci'][1]} | {r['five_class']} = {r['five_class_rate']} | {r['five_class_ci'][0]} to {r['five_class_ci'][1]} |")
    b = rep["bot_baseline_corrections"]
    lines += ["", f"Bot baseline on corrections (the mode the bot actually took, where the models could read it): {b['exact']} of {b['n']} agree with what the operator wanted.", "",
              f"Disagreements: {rep['disagreements']['n']}. By the gate that decided the prediction: " + ", ".join(f"{g}: {n} (within 0.05: {near[g]})" for g, n in by_gate.most_common()) + ".",
              f"Result case per §4: **{case}**.", "", "## Confusion, five classes (truth -> prediction)", ""]
    lines += [f"- {k}: {n}" for k, n in rep["confusion_5x5"].items()]
    lines += ["", "## Threshold sensitivity (diagnostic only; nothing is changed)", "", "| gate moved | exact agreement |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in sens.items()]
    open(os.path.join(a.out, "report.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print(json.dumps({k: rep[k] for k in ("events_with_vectors", "in_scope", "agreement_all", "agreement_corrections", "agreement_controls", "result_case")}, ensure_ascii=False))
    print("disagreements by gate:", dict(by_gate))


if __name__ == "__main__":
    main()
