#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T2 (a): aggregate the judgment-track results already in ilang-conformance report/*/score.json.

    python3 t2a_aggregate.py --report-dir ../../../../ilang-conformance/report --out .

Writes t2a-judge-track.tsv (one row per run) and t2a-judge-track.md (grouped by model maker).
Standard library only. Nothing is scored here; the numbers are copied from score.json, which
score.py produced deterministically from the raw records."""
import argparse
import glob
import json
import os

MAKERS = [  # substring of the model name -> maker
    ("claude", "Anthropic"), ("deepseek", "DeepSeek"), ("qwen", "Alibaba"), ("gemini", "Google"),
    ("gpt", "OpenAI"), ("glm", "Zhipu"), ("kimi", "Moonshot"), ("minimax", "MiniMax"),
    ("mimo", "Xiaomi"), ("hy", "Tencent"),
]


def maker_of(model):
    m = model.lower()
    for key, maker in MAKERS:
        if key in m:
            return maker
    return "other"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-dir", required=True)
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    rows = []
    for path in sorted(glob.glob(os.path.join(a.report_dir, "*", "score.json"))):
        d = json.load(open(path, encoding="utf-8"))
        j = d["tracks"]["judge"]
        run = os.path.basename(os.path.dirname(path))
        rows.append({
            "run": run, "vendor_route": d.get("vendor", ""), "model": d.get("model", ""),
            "maker": maker_of(d.get("model", "")), "spec_pin": str(d.get("spec_pin", ""))[:12],
            "n": j.get("n"), "error_count": j.get("error_count"), "schema_rate": j.get("schema_rate"),
            "mode_acc": j.get("mode_acc"), "boundary_acc": j.get("boundary_acc"),
            "boundary_n": j.get("boundary_n"), "mae": j.get("mae"),
            "vector_score": j.get("vector_score"), "jcs": j.get("jcs"),
            "weighted_total": d.get("summary", {}).get("weighted_total"),
        })
    cols = ["maker", "model", "vendor_route", "run", "spec_pin", "n", "error_count", "schema_rate",
            "mode_acc", "boundary_acc", "boundary_n", "mae", "vector_score", "jcs", "weighted_total"]
    rows.sort(key=lambda r: (r["maker"], -(r["jcs"] or 0)))
    with open(os.path.join(a.out, "t2a-judge-track.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            f.write("\t".join("" if r[c] is None else str(r[c]) for c in cols) + "\n")
    lines = ["# T2 (a): judgment track, existing runs", "",
             f"{len(rows)} score.json files read from `{os.path.basename(os.path.normpath(a.report_dir))}/`. "
             "One row per run; a model that was run through several routes appears once per route. "
             "`mode_acc` is the share of the 100 judge cases whose f_v5 mode from the model's vector matches the gold mode; "
             "`boundary_acc` the same on the boundary cases; `mae` the mean absolute error of the vector against the gold vector "
             "on the scenario cases; `vector_score` = max(0, 1 - mae/0.25) (Part II §7); `jcs` the track's composite. "
             "`error_count` > 0 or `schema_rate` < 1 means part of the track was not answered or not parseable; read those rows with that in mind.", ""]
    for maker in sorted({r["maker"] for r in rows}):
        sub = [r for r in rows if r["maker"] == maker]
        lines += [f"## {maker} ({len(sub)} runs)", "",
                  "| model | route | pin | n | err | schema | mode_acc | boundary_acc (n) | mae | vector_score | jcs |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in sub:
            lines.append(f"| {r['model']} | {r['vendor_route']} | {r['spec_pin'][:7]} | {r['n']} | {r['error_count']} | "
                         f"{r['schema_rate']} | {r['mode_acc']} | {r['boundary_acc']} ({r['boundary_n']}) | {r['mae']} | "
                         f"{r['vector_score']} | {r['jcs']} |")
        lines.append("")
    with open(os.path.join(a.out, "t2a-judge-track.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"{len(rows)} runs -> t2a-judge-track.tsv, t2a-judge-track.md")


if __name__ == "__main__":
    main()
