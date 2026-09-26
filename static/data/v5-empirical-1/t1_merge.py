#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1 step 2 (merge) and step 3 (the operator's confirmation list).

    python3 t1_merge.py --vendor orcarouter-deepseek-free --vendor relay-qwen3.8-max ... \
        --prior t2a-judge-track.tsv --out . --batches-dir ../../../../../Downloads

Merge rule WEIGHTS-TRACK-1 (root 2): each model's vote carries its judgment-track mode accuracy
from ilang-conformance (mode_acc in t2a-judge-track.tsv, by route), normalised over the models
that answered, floor 0.01 (Axiom 1, CONST-BELOW-GATE step), renormalised. The weighted vote is
taken per field: targets, bot_mode, intended_mode. "unknown" votes are excluded from the mode
votes and their weight share is recorded. An event is consistent when every model that named a
mode named the same intended_mode and the same targets.

Confirmation list: every inconsistent event plus a 20 % sample (seed 42) of the consistent ones,
in batches of at most 40, written in plain language with the eight options. The operator's
answers override the model labels; agreement between the model consensus and the operator on the
20 % sample is the label reliability (case D of the result rules uses its Wilson lower bound).

Outputs: merged.jsonl, merge-summary.json, and the batch files. Standard library only."""
import argparse
import collections
import json
import os
import random
import re

OPTIONS = [("M1", "直接做，做完告诉我"), ("M2", "做，并且完整留痕"), ("M3", "先拿方案给我确认"),
           ("M4", "只给建议，不动手"), ("M5", "先问清楚再说"), ("M6", "交给我来定"),
           ("M7", "不做，但给个替代方案"), ("M8", "停")]
PLAIN = dict(OPTIONS)
PATH_RX = re.compile(r'@?"?[A-Za-z]:\\[^\s"]+"?')


def clean(text, n):
    t = PATH_RX.sub("[文件]", text or "").replace("\n", " ").strip()
    t = re.sub(r"\s+", " ", t)
    return t if len(t) <= n else t[:n] + "…"


def weighted_vote(votes, weights):
    """votes: {vendor: value}; returns (winner, {value: weight}) ignoring None."""
    tally = collections.defaultdict(float)
    for v, val in votes.items():
        if val is not None:
            tally[val] += weights[v]
    if not tally:
        return None, {}
    winner = max(sorted(tally), key=lambda k: tally[k])
    return winner, {k: round(w, 4) for k, w in tally.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", default="events.jsonl")
    ap.add_argument("--vendor", action="append", required=True)
    ap.add_argument("--prior", default="t2a-judge-track.tsv")
    ap.add_argument("--labels-dir", default=".", help="directory holding labels/<vendor>/")
    ap.add_argument("--out", default=".")
    ap.add_argument("--batches-dir", default=".")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--sample", type=float, default=0.20)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    events = [json.loads(l) for l in open(a.events, encoding="utf-8") if l.strip()]
    mode_acc = {}
    with open(a.prior, encoding="utf-8") as f:
        head = f.readline().rstrip("\n").split("\t")
        for line in f:
            r = dict(zip(head, line.rstrip("\n").split("\t")))
            mode_acc[r["vendor_route"]] = float(r["mode_acc"] or 0)
    labels = {v: {} for v in a.vendor}
    for v in a.vendor:
        d = os.path.join(a.labels_dir, "labels", v)
        for name in os.listdir(d) if os.path.isdir(d) else []:
            r = json.load(open(os.path.join(d, name), encoding="utf-8"))
            if r.get("status") == "ok" and r.get("parsed"):
                labels[v][r["id"]] = r["parsed"]

    merged, n_models_hist = [], collections.Counter()
    for e in events:
        answered = [v for v in a.vendor if e["id"] in labels[v]]
        n_models_hist[len(answered)] += 1
        if not answered:
            merged.append({**{k: e[k] for k in ("id", "source", "kind")}, "n_models": 0})
            continue
        raw = {v: max(mode_acc.get(v, 0.0), 0.0) for v in answered}
        total = sum(raw.values()) or 1.0
        w = {v: max(0.01, raw[v] / total) for v in answered}
        total = sum(w.values())
        w = {v: w[v] / total for v in answered}
        lab = {v: labels[v][e["id"]] for v in answered}
        targets, t_votes = weighted_vote({v: lab[v]["targets"] for v in answered}, w)
        bot, b_votes = weighted_vote({v: (lab[v]["bot_mode"] if lab[v]["bot_mode"].startswith("M") else None) for v in answered}, w)
        bot_unknown = round(sum(w[v] for v in answered if not lab[v]["bot_mode"].startswith("M")), 4)
        if e["kind"] == "control":
            intended, i_votes = bot, b_votes
        else:
            intended, i_votes = weighted_vote({v: (lab[v]["intended_mode"] if lab[v]["intended_mode"] not in ("unknown", "accepted") else None) for v in answered}, w)
        named = [lab[v]["intended_mode"] for v in answered if lab[v]["intended_mode"].startswith("M") or lab[v]["intended_mode"] == "none_fits"]
        if e["kind"] == "control":
            named = [lab[v]["bot_mode"] for v in answered if lab[v]["bot_mode"].startswith("M")]
        t_set = {lab[v]["targets"] for v in answered}
        # Agreement, per the round's design: every model names the same thing. A correction that every
        # model reads as not about whether or how to act is agreement with no mode to confirm; a control
        # on which no model could name the bot's mode has no truth and is not asked about.
        if e["kind"] == "correction":
            about_action = "do_or_how" in t_set
            consistent = len(t_set) == 1 and (not about_action or (len(named) == len(answered) and len(set(named)) == 1))
        else:
            about_action = bool(named)
            consistent = about_action and len(named) == len(answered) and len(set(named)) == 1
        ask = about_action and not consistent
        mode_consistent = consistent and about_action
        merged.append({**{k: e[k] for k in ("id", "source", "kind")}, "n_models": len(answered), "weights": {v: round(w[v], 4) for v in answered},
                       "targets": targets, "targets_votes": t_votes, "bot_mode": bot, "bot_mode_votes": b_votes, "bot_unknown_weight": bot_unknown,
                       "intended_mode": intended, "intended_votes": i_votes, "consistent": consistent,
                       "about_action": about_action, "ask": ask, "mode_consistent": mode_consistent,
                       "per_model": {v: lab[v] for v in answered}})
    with open(os.path.join(a.out, "merged.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for m in merged:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    by_id = {e["id"]: e for e in events}
    labelled = [m for m in merged if m.get("n_models", 0) >= 2]
    asked_corr = [m for m in labelled if m["kind"] == "correction" and m["ask"]]
    asked_ctrl = [m for m in labelled if m["kind"] == "control" and m["ask"]]
    mode_consistent = [m for m in labelled if m["mode_consistent"]]
    rng = random.Random(a.seed)
    sample = rng.sample(mode_consistent, int(round(a.sample * len(mode_consistent))))
    # Order of value for the operator: corrections about acting first, then controls, then the reliability sample.
    to_confirm = (sorted(asked_corr, key=lambda m: m["id"]) + sorted(asked_ctrl, key=lambda m: m["id"])
                  + sorted(sample, key=lambda m: m["id"]))
    sample_ids = {m["id"] for m in sample}
    not_asked = {"corrections_unanimous_not_about_action": sum(1 for m in labelled if m["kind"] == "correction" and not m["about_action"] and m["consistent"]),
                 "corrections_not_about_action_targets_disagree": sum(1 for m in labelled if m["kind"] == "correction" and not m["about_action"] and not m["consistent"]),
                 "controls_no_model_named_a_mode": sum(1 for m in labelled if m["kind"] == "control" and not m["about_action"])}
    os.makedirs(a.batches_dir, exist_ok=True)
    batch_files = []
    for b in range(0, len(to_confirm), 40):
        items = to_confirm[b:b + 40]
        no = b // 40 + 1
        lines = [f"# 待确认清单 第 {no} 批（共 {len(items)} 条）v1.0 2026-09-26", "",
                 "每条勾一个数字就行。八个选项：1 直接做，做完告诉我 · 2 做，并且完整留痕 · 3 先拿方案给我确认 · 4 只给建议，不动手 · 5 先问清楚再说 · 6 交给我来定 · 7 不做，但给个替代方案 · 8 停。都不对就写「都不对」再加一句你想要什么。这条根本不是关于做不做、怎么做的（只是内容问题，或不是纠正），就填 0；对照条目（你没出声的那种）看不出机器人走的是哪种，也填 0。",
                 "", "回法：在每条最后一行「你的选择：」后面填数字，改完把文件发回来即可。", ""]
        for m in items:
            e = by_id[m["id"]]
            src = "飞书机器人" if e["source"] == "feishu" else "企微口径打磨会话"
            kind = "你之后发了一条消息" if e["kind"] == "correction" else "你没有出声，机器人继续了"
            votes = "；".join(f"{v.replace('relay-', '').replace('orcarouter-', '')}: {m['per_model'][v]['intended_mode' if e['kind'] == 'correction' else 'bot_mode']}" for v in m["per_model"])
            guess = m["intended_mode"]
            guess_txt = f"{guess} {PLAIN[guess]}" if guess in PLAIN else ("八个都不合适" if guess == "none_fits" else "看不出来")
            lines += [f"### {m['id']}（{src}，{e['timestamp'][:16]}，{kind}）",
                      f"场景：{clean(e['context_before'], 160) or '（机器人在群里或私聊里收到消息后自行回复）'}",
                      f"机器人当时做了什么：{clean(e['bot_action'], 240)}"]
            if e["kind"] == "correction":
                lines.append(f"你当时说的：{clean(e['operator_message'], 160)}")
            lines += [f"模型认为你想要：{guess_txt}（各模型：{votes}）",
                      "你的选择：", ""]
        path = os.path.join(a.batches_dir, f"待确认清单-第{no}批-v1.0-2026-09-26.md")
        open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
        batch_files.append(path)
    summary = {"events": len(events), "labelled_by_2_or_more": len(labelled), "models_answered_hist": dict(n_models_hist),
               "asked_corrections": len(asked_corr), "asked_controls": len(asked_ctrl), "mode_consistent": len(mode_consistent),
               "consistent_sampled": len(sample), "not_asked": not_asked,
               "to_confirm": len(to_confirm), "batches": batch_files, "sample_ids": sorted(sample_ids),
               "weights_rule": "WEIGHTS-TRACK-1: mode_acc from ilang-conformance judge track by route, normalised, floor 0.01, renormalised",
               "targets_hist_corrections": dict(collections.Counter(m.get("targets") for m in labelled if m["kind"] == "correction")),
               "intended_hist_corrections": dict(collections.Counter(m.get("intended_mode") for m in labelled if m["kind"] == "correction")),
               "bot_hist_controls": dict(collections.Counter(m.get("bot_mode") for m in labelled if m["kind"] == "control"))}
    json.dump(summary, open(os.path.join(a.out, "merge-summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps({k: summary[k] for k in summary if k not in ("sample_ids", "batches")}, ensure_ascii=False))
    print("batches:", *batch_files, sep="\n  ")


if __name__ == "__main__":
    main()
