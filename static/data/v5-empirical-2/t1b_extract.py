#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 2, step 1: de-identify two new sources and extract correction and control events.

    python3 t1b_extract.py --feishu <chat_records.json> --claude <export.md> [--claude <export.md>] \
        --name-map <private json, kept out of the repository> --out .

Sources
  feishu  A Lark group export (lark-cli, chat_records.json): every message of the VIP group with
          sender, minute timestamp, position, reply_to and rendered text. Only messages after the
          public cutoff of judgment-calibration-v1 (2026-09-08 01:06) are used, so nothing here
          repeats round 1. Members are renamed 学员NNN (first appearance order; the map stays
          private), the operator's display name becomes 老板, the bot keeps its public name.
          Correction: an operator message whose nearest preceding bot message is within 30 minutes;
          bot_action is that bot message (its text is available in this export), context_before is
          the member message the bot replied to (reply_to), else the nearest member message before
          it. Consecutive operator messages within 2 minutes are one event.
          Control: a bot text reply after which no operator message follows within 30 minutes.
  claude  Exports of the operator's own sessions with Claude Code, turns marked
          "## 老板 · <time>" / "## Claude · <time>" or "### 👤 老板 · <time>" / "### 🤖 Claude · <time>".
          Correction: an operator turn that follows a Claude turn; bot_action is that Claude turn,
          context_before the operator turn before it. Control: a Claude turn followed by another
          Claude turn with no operator turn between (the operator let it run on).

De-identification applied to every published text: member names (the group's member list, plus
third parties named in the sessions), the operator's own names, IP addresses, e-mail addresses,
phone numbers, QQ and WeChat-style ids, Lark ids (ou_/oc_/om_/cli_), UUIDs, 32+ character hex or
base62 strings, link tokens in URLs, the zsxq group number. Controls are sampled to the corrections
count per source, seed 42. Output: events.jsonl, events-summary.json, sources/<de-identified sources>.
Nothing here calls a model."""
import argparse
import datetime as dt
import json
import os
import random
import re

CUTOFF = "2026-09-08 01:06"
BOSS_OPEN_ID = "[REDACTED]"

RX = [
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "[REDACTED_IP]"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "[REDACTED_EMAIL]"),
    (re.compile(r"\b1[3-9]\d{9}\b"), "[REDACTED_PHONE]"),
    (re.compile(r"\b(?:ou|oc|om|cli|on)_[0-9a-f]{16,}\b"), "[REDACTED_ID]"),
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"), "[REDACTED_ID]"),
    (re.compile(r"\b(?:lxmcp|sk|hf|ghp|gho|xoxb|AKIA)[_-][A-Za-z0-9_-]{16,}\b"), "[REDACTED_TOKEN]"),
    (re.compile(r"\b[0-9a-f]{32,}\b"), "[REDACTED_ID]"),
    (re.compile(r"\b(?=[A-Za-z0-9]*[A-Z])(?=[A-Za-z0-9]*[a-z])(?=[A-Za-z0-9]*[0-9])[A-Za-z0-9]{32,}\b"), "[REDACTED_TOKEN]"),
    (re.compile(r"([?&](?:link_token|token|key|sig|signature)=)[^&\s)]+"), r"\1[REDACTED]"),
    (re.compile(r"(QQ群|qq群|Q群|QQ|qq)([:：\s]*)(\d{5,11})"), r"\1\2[REDACTED_QQ]"),
    (re.compile(r"(群号|群[:：]\s*)(\d{5,11})"), r"\1[REDACTED_QQ]"),
    (re.compile(r"(微信号|微信|vx|VX|wx|WX)([:：\s]+)([A-Za-z][A-Za-z0-9_-]{5,19})\b"), r"\1\2[REDACTED_WECHAT]"),
    (re.compile(r"\b96348561\b"), "[REDACTED_ID]"),
    (re.compile(r"(星球号|ZSXQ_GROUP_NUMBER)([=:：\s]*)\d{6,}"), r"\1\2[REDACTED_ID]"),
    (re.compile(r"用户(\d{5,})"), "用户[ID]"),
]

# Third parties named in the sessions who are not in the member list, and the operator's own names.
EXTRA_NAMES = [("[REDACTED]", "学员（新人）"), ("静水流深", "老板"), ("朱龙泉", "老板"), ("Long Quan Zhu", "the operator")]
CJK = re.compile(r"^[一-鿿]{2,}$")


def person_clean(text, real):
    """real: [(name, pseudonym)], longest first. A CJK name of two or more characters or a Latin
    name of four or more is replaced everywhere; a shorter handle only where it follows @, so
    ordinary words stay intact."""
    for nm, ps in real:
        if CJK.match(nm) or len(nm) >= 4:
            text = text.replace(nm, ps)
        elif len(nm) >= 2:
            text = text.replace("@" + nm, "@" + ps)
    for nm, ps in EXTRA_NAMES:
        text = text.replace(nm, ps)
    return text


def redact(text):
    for rx, rep in RX:
        text = rx.sub(rep, text)
    return text


class Names:
    """Member pseudonyms by first appearance; the map is written to a private file, never published."""

    def __init__(self, path):
        self.path = path
        self.map = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}

    def get(self, open_id, name):
        if open_id not in self.map:
            self.map[open_id] = {"pseudonym": "学员%03d" % (len(self.map) + 1), "name": name}
        return self.map[open_id]["pseudonym"]

    def real(self):
        return sorted({(v["name"], v["pseudonym"]) for v in self.map.values() if v["name"]}, key=lambda x: -len(x[0]))

    def save(self):
        json.dump(self.map, open(self.path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def T(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M")


def feishu(path, names):
    d = json.load(open(path, encoding="utf-8-sig"))
    recs = sorted(d["data"]["messages"], key=lambda r: int(r["message_position"]))
    ops_name = None

    def role(r):
        s = r["sender"]
        if s.get("id_type") == "app_id":
            return "bot"
        if s.get("id") == BOSS_OPEN_ID:
            return "operator"
        if s.get("id_type") == "open_id":
            return "member"
        return "system"
    for r in recs:
        if role(r) == "member":
            names.get(r["sender"]["id"], r["sender"].get("name") or "")
        elif role(r) == "operator":
            ops_name = r["sender"].get("name") or ops_name
    real = names.real()

    def clean(text):
        text = text or ""
        if ops_name:
            text = text.replace(ops_name, "老板")
        text = person_clean(text, real)
        text = re.sub(r"@_user_\d+", "@学员", text)
        return redact(text)
    stream, by_id = [], {}
    for r in recs:
        ro = role(r)
        if ro == "system":
            continue
        who = "bot" if ro == "bot" else "operator" if ro == "operator" else names.get(r["sender"]["id"], r["sender"].get("name") or "")
        row = {"pos": int(r["message_position"]), "time": r["create_time"], "role": ro, "who": who, "msg_type": r["msg_type"],
               "text": clean(r["content"]), "reply_to_pos": None, "_id": r["message_id"], "_reply_to": r.get("reply_to")}
        stream.append(row)
        by_id[r["message_id"]] = row
    for row in stream:
        if row["_reply_to"] in by_id:
            row["reply_to_pos"] = by_id[row["_reply_to"]]["pos"]
    idx = {row["pos"]: i for i, row in enumerate(stream)}
    after = [row for row in stream if row["time"] > CUTOFF]

    def member_before(pos, t0):
        m = idx[pos] - 1
        while m >= 0 and (t0 - T(stream[m]["time"])).total_seconds() <= 1800:
            if stream[m]["role"] == "member":
                return stream[m]
            m -= 1
        return None

    def context_of(bot):
        if bot["reply_to_pos"] is not None and stream[idx[bot["reply_to_pos"]]]["role"] == "member":
            return stream[idx[bot["reply_to_pos"]]]
        return member_before(bot["pos"], T(bot["time"]))
    corrections, controls = [], []
    i = 0
    while i < len(after):
        row = after[i]
        if row["role"] != "operator":
            i += 1
            continue
        texts = [row["text"]]
        j = i + 1
        while j < len(after) and after[j]["role"] == "operator" and (T(after[j]["time"]) - T(after[j - 1]["time"])).total_seconds() <= 120:
            texts.append(after[j]["text"])
            j += 1
        bot = None
        if row["reply_to_pos"] is not None and stream[idx[row["reply_to_pos"]]]["role"] == "bot":
            bot = stream[idx[row["reply_to_pos"]]]
        else:
            k = idx[row["pos"]] - 1
            while k >= 0 and (T(row["time"]) - T(stream[k]["time"])).total_seconds() <= 1800:
                if stream[k]["role"] == "bot":
                    bot = stream[k]
                    break
                k -= 1
        if bot is not None:
            ctx = context_of(bot)
            corrections.append({"source": "feishu", "kind": "correction", "timestamp": row["time"],
                                "context_before": ("%s：%s" % (ctx["who"], ctx["text"])) if ctx else "",
                                "bot_action": bot["text"], "bot_action_available": True,
                                "operator_message": " / ".join(texts), "feishu_pos": row["pos"], "bot_pos": bot["pos"]})
        i = j
    op_times = [T(r["time"]) for r in after if r["role"] == "operator"]
    for row in after:
        if row["role"] != "bot" or row["msg_type"] not in ("text", "post"):
            continue
        t0 = T(row["time"])
        if any(0 <= (t - t0).total_seconds() <= 1800 for t in op_times):
            continue
        ctx = context_of(row)
        if ctx is None:
            continue
        controls.append({"source": "feishu", "kind": "control", "timestamp": row["time"],
                         "context_before": "%s：%s" % (ctx["who"], ctx["text"]), "bot_action": row["text"], "bot_action_available": True,
                         "operator_message": "", "bot_pos": row["pos"], "label_note": "weak: the operator did not speak within 30 minutes"})
    public = [{k: row[k] for k in ("pos", "time", "role", "who", "msg_type", "text", "reply_to_pos")} for row in after]
    return corrections, controls, public


TURN_RX = re.compile(r"^#{2,3} (?:👤 |🤖 )?(老板|Claude) · (\d{4}-)?(\d{2}-\d{2}) (\d{2}:\d{2})\s*$")


def claude(path, tag, real):
    lines = open(path, encoding="utf-8").read().split("\n")
    turns, cur = [], None
    for ln in lines:
        m = TURN_RX.match(ln.strip())
        if m:
            who = "operator" if m.group(1) == "老板" else "bot"
            cur = {"who": who, "time": "%s%s %s" % (m.group(2) or "2026-", m.group(3), m.group(4)), "text": []}
            turns.append(cur)
        elif cur is not None:
            cur["text"].append(ln)
    for t in turns:
        t["text"] = redact(person_clean("\n".join(t["text"]).strip(), real))
    corrections, controls = [], []
    for i, t in enumerate(turns):
        if t["who"] == "operator" and i > 0 and turns[i - 1]["who"] == "bot":
            ctx = next((turns[j]["text"] for j in range(i - 2, -1, -1) if turns[j]["who"] == "operator"), "")
            corrections.append({"source": tag, "kind": "correction", "timestamp": t["time"], "context_before": ctx[:1500],
                                "bot_action": turns[i - 1]["text"][:2000], "bot_action_available": True, "operator_message": t["text"]})
        if t["who"] == "bot" and i + 1 < len(turns) and turns[i + 1]["who"] == "bot":
            ctx = next((turns[j]["text"] for j in range(i - 1, -1, -1) if turns[j]["who"] == "operator"), "")
            controls.append({"source": tag, "kind": "control", "timestamp": t["time"], "context_before": ctx[:1500],
                             "bot_action": t["text"][:2000], "bot_action_available": True, "operator_message": "",
                             "label_note": "weak: the next turn was Claude again, the operator did not speak"})
    public = "\n\n".join("## %s · %s\n\n%s" % ("老板" if t["who"] == "operator" else "Claude", t["time"], t["text"]) for t in turns)
    return corrections, controls, public


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--feishu", required=True)
    ap.add_argument("--claude", action="append", default=[])
    ap.add_argument("--name-map", required=True)
    ap.add_argument("--out", default=".")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    os.makedirs(os.path.join(a.out, "sources"), exist_ok=True)
    names = Names(a.name_map)
    fc, fctl, fpublic = feishu(a.feishu, names)
    names.save()
    with open(os.path.join(a.out, "sources", "feishu-group-after-2026-09-08.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for row in fpublic:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    cc, cctl = [], []
    for n, p in enumerate(a.claude):
        c1, c2, public = claude(p, "claude", names.real())
        cc += c1
        cctl += c2
        open(os.path.join(a.out, "sources", "claude-sessions-%d.md" % (n + 1)), "w", encoding="utf-8", newline="\n").write(
            "# The operator's sessions with Claude Code, de-identified (export %d)\n\n" % (n + 1) + public + "\n")
    fctl_s = rng.sample(fctl, min(len(fctl), len(fc)))
    cctl_s = rng.sample(cctl, min(len(cctl), len(cc)))
    events = fc + fctl_s + cc + cctl_s
    events.sort(key=lambda e: (e["source"], e["timestamp"]))
    keep = ("id", "source", "kind", "timestamp", "context_before", "bot_action", "bot_action_available", "operator_message", "label_note")
    with open(os.path.join(a.out, "events.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for n, e in enumerate(events, 1):
            e["id"] = "T1B-%04d" % n
            f.write(json.dumps({k: e[k] for k in keep if k in e}, ensure_ascii=False) + "\n")
    summary = {"seed": a.seed, "cutoff_feishu": CUTOFF,
               "feishu": {"corrections": len(fc), "controls_available": len(fctl), "controls_sampled": len(fctl_s), "members_pseudonymised": len(names.map)},
               "claude": {"exports": len(a.claude), "corrections": len(cc), "controls_available": len(cctl), "controls_sampled": len(cctl_s)},
               "total_events": len(events)}
    json.dump(summary, open(os.path.join(a.out, "events-summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
