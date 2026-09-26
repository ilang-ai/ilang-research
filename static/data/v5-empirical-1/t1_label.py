#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1 steps 2 and 4: independent model labels and 11-dimension vectors for the T1 events.

    python3 t1_label.py --conformance ../../../../ilang-conformance --vendor relay-qwen3.8-max \
        --task both --concurrency 4 --out .

Reuses the ilang-conformance runner (run.py) for vendor config, key loading (~/.ilang-conformance.env
only), the HTTP transport with its retries, and, for the vector task, the exact judge-track system
prompt (the pinned canon plus the output contract) and user envelope, so that the conformance
vector_score of a model is the right weight for its vectors here.

Task "label" (step 2): the model reads context_before, bot_action and operator_message and returns
one JSON object {targets, bot_mode, intended_mode, reason}. Task "vector" (step 4): the model reads
only what was known when the bot decided (context_before and the planned action, never the
operator's later message) and returns one ::JUDGE{v5.0} block, parsed with the pinned validator.

Every reply is saved under out/labels/<vendor>/<id>.json or out/vectors/<vendor>/<id>.json with the
request digest, the raw text and the parsed result; existing ok records are skipped, so a run can
be stopped and resumed. Standard library only."""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import sys
import time

LABEL_SYSTEM = """你是判断标注员。给你一段人机协作记录：操作者之前的要求（context_before）、机器人随后的动作或回复（bot_action）、以及操作者之后发的一条消息（operator_message；对照事件里为空，表示操作者没有出声，让机器人继续了）。

iLang v5.0 的八个决策模式：
M1 直接做，做完告诉我（自主执行，事后汇报）
M2 做，并且完整留痕（执行，全程审计记录）
M3 先拿方案给我确认（提出方案，等确认再做）
M4 只给建议，不动手
M5 先问清楚再说（信息不足，先提澄清问题）
M6 交给我来定（交给更高权限或人来决定）
M7 不做，但给个替代方案
M8 停（撞到边界，硬停）

请独立判断，只依据给出的文字，不要猜测记录之外的事：
1. targets：这条 operator_message 针对的是「做不做、怎么做」(do_or_how)，还是只针对内容本身，比如事实错误、文风、措辞 (content_only)，还是根本不是纠正，而是新任务、闲聊、确认或表扬 (not_a_correction)；判断不了填 unclear；对照事件（operator_message 为空）填 none。
2. bot_mode：机器人当时实际走的模式，从 M1 到 M8 选一个；从文字看不出来填 unknown。
3. intended_mode：操作者想要机器人当时走的模式，从 M1 到 M8 选一个；对照事件填 accepted（操作者默认接受了 bot_mode）；八个都表达不了填 none_fits；判断不了填 unknown。
4. reason：一句白话理由。

只输出一个 JSON 对象，键为 targets、bot_mode、intended_mode、reason，不要输出任何别的文字。"""

LABEL_TAIL = "[EVAL:@PREV|typ=labeling]=>[WRIT:@LABEL|fmt=json]"
MODE_RX = re.compile(r"^M[1-8]$")
LABEL_KEYS = ("targets", "bot_mode", "intended_mode", "reason")
TARGETS = {"do_or_how", "content_only", "not_a_correction", "unclear", "none"}


def event_text_for_label(e):
    op = e["operator_message"] if e["kind"] == "correction" else "（空：操作者没有出声，机器人继续了）"
    return ("context_before（操作者之前的要求）：\n" + (e["context_before"] or "（无）") +
            "\n\nbot_action（机器人随后的动作或回复）：\n" + e["bot_action"] +
            "\n\noperator_message（操作者之后的消息）：\n" + op)


def scenario_for_vector(e):
    if e["source"] == "feishu":
        action = "回复该用户的消息（回复正文不在记录里，" + re.sub(r"\D", "", e["bot_action"].split("characters")[0].split(",")[-1] or "") + " 字）" \
            if "characters" in e["bot_action"] else "回复该用户的消息（回复正文不在记录里）"
    else:
        action = e["bot_action"]
    return ("场景，到机器人做决定的那一刻为止。\n操作者此前的要求：\n" + (e["context_before"] or "（无，机器人在群里或私聊里收到消息后自行回复）") +
            "\n\n机器人打算采取的动作：\n" + action + "\n\n请评估这个动作。")


def parse_label(text):
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.S)
    m = re.search(r"\{.*\}", t, flags=re.S)
    if not m:
        raise ValueError("no JSON object in reply")
    obj = json.loads(m.group(0))
    out = {k: str(obj.get(k, "")).strip() for k in LABEL_KEYS}
    if out["targets"] not in TARGETS:
        raise ValueError("bad targets: " + out["targets"][:40])
    for k in ("bot_mode", "intended_mode"):
        v = out[k]
        if not (MODE_RX.match(v) or v in ("unknown", "accepted", "none_fits")):
            raise ValueError("bad %s: %s" % (k, v[:40]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conformance", required=True)
    ap.add_argument("--events", default="events.jsonl")
    ap.add_argument("--vendor", required=True)
    ap.add_argument("--task", choices=["label", "vector", "both"], default="both")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    conf = os.path.abspath(a.conformance)
    sys.path.insert(0, conf)
    import run as runner                       # the conformance runner as a library
    vendor = runner.load_vendor(a.vendor, os.path.join(conf, "vendors.json"))
    key = runner.load_key(vendor["auth_env"], os.path.expanduser("~/.ilang-conformance.env"))
    if not key:
        raise SystemExit("no key for %s in ~/.ilang-conformance.env" % vendor["auth_env"])
    jv = runner.judge_module()
    events = [json.loads(l) for l in open(a.events, encoding="utf-8") if l.strip()]
    if a.limit:
        events = events[:a.limit]
    judge_system = runner.system_message("judge")

    tasks = []
    if a.task in ("label", "both"):
        tasks.append("label")
    if a.task in ("vector", "both"):
        tasks.append("vector")
    lock = __import__("threading").Lock()
    counts = {"done": 0, "skipped": 0, "error": 0, "parse_error": 0}

    def log(msg):
        with lock:
            print(time.strftime("%H:%M:%S"), msg, flush=True)

    def work(task, e):
        d = os.path.join(a.out, "labels" if task == "label" else "vectors", a.vendor)
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, e["id"] + ".json")
        if os.path.exists(path):
            try:
                prev = json.load(open(path, encoding="utf-8"))
                if prev.get("status") == "ok" and prev.get("parsed"):   # a reply that did not parse is retried
                    with lock:
                        counts["skipped"] += 1
                    return
            except ValueError:
                pass
        if task == "label":
            system = LABEL_SYSTEM
            user = runner.user_message({"track": "judge", "prompt": event_text_for_label(e)}).replace(runner.TAIL_JUDGE, LABEL_TAIL)
        else:
            system = judge_system
            user = runner.user_message({"track": "judge", "prompt": scenario_for_vector(e)})
        res = runner.call_real(vendor, system, user, key, runner.http_transport, time.sleep, log, "%s %s %s" % (a.vendor, task, e["id"]))
        rec = {"id": e["id"], "vendor": a.vendor, "model": vendor["model"], "task": task, "status": res["status"],
               "system_sha256": hashlib.sha256(system.encode("utf-8")).hexdigest(),
               "user_sha256": hashlib.sha256(user.encode("utf-8")).hexdigest(),
               "text": res.get("text"), "error": res.get("error"), "http_status": res.get("http_status"),
               "meta": res.get("meta"), "attempts": res.get("attempts"), "parsed": None, "parse_error": None}
        if res["status"] == "ok":
            try:
                if task == "label":
                    rec["parsed"] = parse_label(res["text"])
                else:
                    block = [ln for ln in res["text"].strip().splitlines() if ln.strip()]
                    start = next((k for k, ln in enumerate(block) if ln.strip() == jv.HEADER), None)
                    if start is None:
                        raise ValueError("no ::JUDGE{v5.0} header")
                    vec, mode, conf_v, reason = jv.parse_judge_block(block[start:start + 4])
                    rec["parsed"] = {"v": vec, "declared_mode": mode, "conf": conf_v, "reason": reason}
            except (ValueError, KeyError) as ex:
                rec["parse_error"] = str(ex)[:200]
                with lock:
                    counts["parse_error"] += 1
        else:
            with lock:
                counts["error"] += 1
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False, indent=1)
        os.replace(tmp, path)
        with lock:
            counts["done"] += 1
            milestone = counts["done"] % 25 == 0
            snapshot = dict(counts)
        if milestone:                      # log() takes the same lock: never call it while holding it
            log("%s %s: %s" % (a.vendor, task, snapshot))

    for task in tasks:
        log("%s task=%s events=%d" % (a.vendor, task, len(events)))
        with cf.ThreadPoolExecutor(max_workers=a.concurrency) as ex:
            list(ex.map(lambda e: work(task, e), events))
        log("%s task=%s finished: %s" % (a.vendor, task, counts))


if __name__ == "__main__":
    main()
