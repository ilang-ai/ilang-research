#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T1 step 3: read the batch files the operator sent back and compute label reliability.

    python3 t1_confirm_parse.py --batch "../../../../../Downloads/待确认清单-第1批-v1.0-2026-09-26.md" [...] \
        --merged merged.jsonl --summary merge-summary.json --out .

Each item ends with a line "你的选择：<n>" where n is 1 to 8, or "都不对" with a free-text wish.
Writes confirmed.jsonl ({id, operator_mode, none_fits, raw}) and reliability.json: on the 20 %
sample of consistent events, how often the model consensus equals the operator's answer, with the
Wilson 95 % interval; case D of the result rules applies when the lower bound is below 0.5."""
import argparse
import json
import re

ITEM = re.compile(r"^### (T1B?-\d{4})")
CHOICE = re.compile(r"^你的选择：\s*(.*)$")
NUM = re.compile(r"[0-9]")
FULL = str.maketrans("１２３４５６７８", "12345678")


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    z2 = z * z
    c = (p + z2 / (2 * n)) / (1 + z2 / n)
    h = z * ((p * (1 - p) / n + z2 / (4 * n * n)) ** 0.5) / (1 + z2 / n)
    return (round(c - h, 4), round(c + h, 4))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", action="append", required=True)
    ap.add_argument("--merged", default="merged.jsonl")
    ap.add_argument("--summary", default="merge-summary.json")
    ap.add_argument("--out", default=".")
    ap.add_argument("--sample-ids-file", default=None, help="JSON with sample_ids: the sample as issued to the operator")
    a = ap.parse_args()
    answers = {}
    for path in a.batch:
        cur = None
        for line in open(path, encoding="utf-8"):
            m = ITEM.match(line.strip())
            if m:
                cur = m.group(1)
                continue
            c = CHOICE.match(line.strip())
            if c and cur:
                raw = c.group(1).strip().translate(FULL)
                if not raw:
                    continue
                none_fits = "都不对" in raw or "none" in raw.lower()
                n = NUM.search(raw)
                not_action = bool(n) and n.group(0) == "0"      # not about whether or how to act; for a control: mode not visible
                dont_know = bool(n) and n.group(0) == "9"       # the operator wanted the bot to say it did not know
                answers[cur] = {"id": cur, "operator_mode": ("M" + n.group(0)) if (n and not none_fits and not not_action and not dont_know) else ("dont_know" if dont_know else None),
                                "none_fits": none_fits, "not_action": not_action, "dont_know": dont_know,
                                "by": "delegate" if "CC 代判" in raw else "operator", "raw": raw}
    with open(a.out.rstrip("/\\") + "/confirmed.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for r in answers.values():
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    merged = {m["id"]: m for m in (json.loads(l) for l in open(a.merged, encoding="utf-8") if l.strip())}
    src = a.sample_ids_file if a.sample_ids_file else a.summary
    sample_ids = set(json.load(open(src, encoding="utf-8")).get("sample_ids", []))
    def answer_of(r):
        return r["operator_mode"] or ("none_fits" if r["none_fits"] else "not_action" if r.get("not_action") else None)
    FIVE = {"M1": "act", "M2": "act", "M3": "confirm", "M4": "confirm", "M5": "ask", "M6": "hand_over", "M7": "decline_or_stop", "M8": "decline_or_stop"}

    def consensus(i):
        m = merged[i]
        return m["bot_mode"] if m["kind"] == "control" else m["intended_mode"]

    def reliability(ids):
        pairs = [(consensus(i), answer_of(answers[i])) for i in ids if i in answers and i in merged and answer_of(answers[i]) and answer_of(answers[i]) != "not_action"]
        k = sum(x == y for x, y in pairs)
        k5 = sum(FIVE.get(x, x) == FIVE.get(y, y) for x, y in pairs)
        m12 = lambda x: "M12" if x in ("M1", "M2") else x
        k7 = sum(m12(x) == m12(y) for x, y in pairs)
        return {"sample_answered": len(pairs), "consensus_equals_operator": k, "rate": round(k / len(pairs), 4) if pairs else None, "wilson_95": wilson(k, len(pairs)),
                "case_D": (wilson(k, len(pairs))[0] or 1) < 0.5 if pairs else None,
                "m1m2_merged_equals": k7, "m1m2_merged_rate": round(k7 / len(pairs), 4) if pairs else None, "m1m2_merged_wilson_95": wilson(k7, len(pairs)),
                "five_class_equals": k5, "five_class_rate": round(k5 / len(pairs), 4) if pairs else None, "five_class_wilson_95": wilson(k5, len(pairs)),
                "pairs": [{"consensus": x, "operator": y} for x, y in pairs]}
    own = [i for i in sample_ids if i in answers and answers[i].get("by") == "operator"]
    rel = reliability(own)
    rel["by"] = "the operator's own answers"
    rel["all_answers_including_delegated"] = reliability([i for i in sample_ids if i in answers])
    rel["answers_total"] = len(answers)
    rel["answers_by_operator"] = sum(1 for r in answers.values() if r.get("by") == "operator")
    rel["answers_delegated"] = sum(1 for r in answers.values() if r.get("by") == "delegate")
    rel["none_fits_total"] = sum(r["none_fits"] for r in answers.values())
    rel["not_action_total"] = sum(r.get("not_action", False) for r in answers.values())
    rel["dont_know_total"] = sum(r.get("dont_know", False) for r in answers.values())
    json.dump(rel, open(a.out.rstrip("/\\") + "/reliability.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(rel, ensure_ascii=False))


if __name__ == "__main__":
    main()
