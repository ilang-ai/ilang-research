#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1 step 1: extract correction events and control events from the two public, desensitized
calibration logs of judgment-calibration-v1.

    python3 t1_extract_events.py --data ../judgment-calibration-v1 --out .

Sources
  wecom   zh/wecom-calibration-log.md: a Claude Code session in which the operator (@BOSS) shapes
          the WeCom customer-service bot. Turns are "### 🗣 @BOSS `HH:MM`" blocks (quoted lines)
          and "**Claude `HH:MM`**" blocks (reply text, tool-call summaries in <sub> tags).
          Correction candidate: every @BOSS turn that follows at least one Claude turn; the bot
          action is the group of Claude turns since the previous @BOSS turn; context_before is
          the previous @BOSS turn (the request the bot was acting on).
          Control candidate: a Claude turn group that the operator let run on (the next turn is
          Claude again after tool work, no @BOSS message in between). Label "operator let it
          continue", which is weak and is marked as such.
  feishu  structured/tuning-events.jsonl (152 operator messages, with prev_reply_chars when a bot
          reply preceded) and structured/user-interactions.jsonl (1,062 user and operator messages
          by chat hash; the bot's own replies are not in the public dataset).
          Correction candidate: every operator message with a preceding bot reply; context_before
          is the last non-operator messages in the same chat type within 30 minutes; bot_action is
          "[reply of N characters; text not in the public dataset]".
          Control candidate: a non-operator message followed by an API call within 90 seconds
          (the bot replied) and no operator message in that chat type within the next 30 minutes.

Controls are sampled to the same count as the corrections per source, seed 42. Output:
events.jsonl with {id, source, kind, context_before, bot_action, bot_action_available,
operator_message, timestamp, label_note}. Nothing here calls a model."""
import argparse
import datetime as dt
import json
import os
import random
import re

BOSS_RX = re.compile(r"^### 🗣 @BOSS\s+`(\d\d:\d\d)`")
CLAUDE_RX = re.compile(r"^\*\*Claude `(\d\d:\d\d)`\*\*")
DATE_RX = re.compile(r"^## (\d{4}-\d{2}-\d{2})")
SUB_RX = re.compile(r"<sub>(.*?)</sub>")


def parse_wecom(path):
    turns, cur, date = [], None, None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        m = DATE_RX.match(line)
        if m:
            date = m.group(1)
            continue
        mb, mc = BOSS_RX.match(line), CLAUDE_RX.match(line)
        if mb or mc:
            if cur:
                turns.append(cur)
            cur = {"role": "boss" if mb else "claude", "time": f"{date} {(mb or mc).group(1)}", "text": [], "tools": []}
            continue
        if cur is None:
            continue
        ms = SUB_RX.search(line)
        if ms:
            cur["tools"].append(ms.group(1).strip())
            continue
        if line.startswith("> "):
            cur["text"].append(line[2:])
        elif line.startswith(">"):
            cur["text"].append(line[1:].strip())
        elif line.strip() and not line.startswith("---"):
            cur["text"].append(line)
    if cur:
        turns.append(cur)
    for t in turns:
        t["text"] = "\n".join(x for x in t["text"] if x is not None).strip()
    return turns


ATTACH_RX = re.compile(r'@"[^"]*"')


def is_operator_message(text):
    """A @BOSS turn that is a harness notification or nothing but file attachments is not an
    operator decision and is dropped (deterministic rule, counted in the summary)."""
    if text.lstrip().startswith("<task-notification>"):
        return False
    return bool(ATTACH_RX.sub("", text).strip())


def wecom_events(turns):
    corrections, controls = [], []
    prev_boss, group = None, []
    dropped = 0
    for k, t in enumerate(turns):
        if t["role"] == "claude":
            group.append(t)
            nxt = turns[k + 1] if k + 1 < len(turns) else None
            if nxt and nxt["role"] == "claude" and t["text"]:
                controls.append({"source": "wecom", "kind": "control", "timestamp": t["time"],
                                 "context_before": prev_boss["text"] if prev_boss else "",
                                 "bot_action": t["text"] + ("\n[tools: " + "; ".join(t["tools"]) + "]" if t["tools"] else ""),
                                 "bot_action_available": True, "operator_message": "",
                                 "label_note": "operator let the bot continue; no message before the bot's next step (weak acceptance label)"})
            continue
        if not is_operator_message(t["text"]):
            dropped += 1          # a notification or attachment-only turn: the bot's group continues
            continue
        if group:
            action = "\n---\n".join(g["text"] + ("\n[tools: " + "; ".join(g["tools"]) + "]" if g["tools"] else "") for g in group if g["text"] or g["tools"])
            corrections.append({"source": "wecom", "kind": "correction", "timestamp": t["time"],
                                "context_before": prev_boss["text"] if prev_boss else "",
                                "bot_action": action, "bot_action_available": True,
                                "operator_message": t["text"], "label_note": ""})
        prev_boss, group = t, []
    wecom_events.dropped = dropped
    return corrections, controls


def ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def feishu_events(data):
    tuning = [json.loads(l) for l in open(os.path.join(data, "structured", "tuning-events.jsonl"), encoding="utf-8") if l.strip()]
    inter = [json.loads(l) for l in open(os.path.join(data, "structured", "user-interactions.jsonl"), encoding="utf-8") if l.strip()]
    calls = [ts(json.loads(l)["timestamp"]) for l in open(os.path.join(data, "structured", "api-calls.jsonl"), encoding="utf-8") if l.strip()]
    calls.sort()
    inter.sort(key=lambda r: r["timestamp"])
    corrections, controls = [], []
    for e in tuning:
        if e.get("prev_reply_chars") is None:
            continue
        t0 = ts(e["timestamp"])
        ctx = [r for r in inter if not r["is_boss"] and r["chat_type"] == e["chat_type"]
               and 0 <= (t0 - ts(r["timestamp"])).total_seconds() <= 1800]
        corrections.append({"source": "feishu", "kind": "correction", "timestamp": e["timestamp"], "feishu_id": e["id"],
                            "context_before": "\n".join(f"[{r['timestamp']}] {r['message']}" for r in ctx[-5:]),
                            "bot_action": f"[the bot replied, {e['prev_reply_chars']} characters; the reply text is not in the public dataset]",
                            "bot_action_available": False, "operator_message": e["boss_message"],
                            "label_note": f"tuning-events type={e['type']} adopted={e.get('adopted')}"})
    boss_times = {}
    for r in inter:
        if r["is_boss"]:
            boss_times.setdefault(r["chat_type"], []).append(ts(r["timestamp"]))
    import bisect
    for r in inter:
        if r["is_boss"]:
            continue
        t0 = ts(r["timestamp"])
        i = bisect.bisect_left(calls, t0)
        replied = i < len(calls) and (calls[i] - t0).total_seconds() <= 90
        if not replied:
            continue
        bt = boss_times.get(r["chat_type"], [])
        j = bisect.bisect_left(bt, t0)
        corrected = j < len(bt) and (bt[j] - t0).total_seconds() <= 1800
        if corrected:
            continue
        controls.append({"source": "feishu", "kind": "control", "timestamp": r["timestamp"],
                         "context_before": f"[{r['timestamp']}] {r['message']}",
                         "bot_action": "[the bot replied within 90 seconds; the reply text is not in the public dataset]",
                         "bot_action_available": False, "operator_message": "",
                         "label_note": "no operator message in this chat type within 30 minutes (weak acceptance label)"})
    return corrections, controls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default=".")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    wc, wctl = wecom_events(parse_wecom(os.path.join(a.data, "zh", "wecom-calibration-log.md")))
    fc, fctl = feishu_events(a.data)
    wctl_s = rng.sample(wctl, min(len(wc), len(wctl)))
    fctl_s = rng.sample(fctl, min(len(fc), len(fctl)))
    events = wc + wctl_s + fc + fctl_s
    for n, e in enumerate(events, 1):
        e["id"] = f"T1-{n:04d}"
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "events.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    summary = {"seed": a.seed, "wecom": {"corrections": len(wc), "controls_available": len(wctl), "controls_sampled": len(wctl_s),
                                          "boss_turns_dropped_as_notification_or_attachment_only": wecom_events.dropped},
               "feishu": {"corrections": len(fc), "controls_available": len(fctl), "controls_sampled": len(fctl_s)},
               "total_events": len(events)}
    json.dump(summary, open(os.path.join(a.out, "events-summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
