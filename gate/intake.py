#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Intake gate for ilang-research.

Reads one GitHub issue (a counterexample or an amendment filed through the issue forms), runs the
gates the canon itself defines, and writes a verdict plus a verbatim record:

  gate 1  grammar   every fenced iLang block passes the canon grammar validator in strict mode;
                    every ::JUDGE block passes the judge validator
  gate 2  canon     (amendments) the diff applies to a checkout of ilang-spec and that checkout
                    still passes the spec's own CI gate, command by command
  gate 3  judgment  (amendments) a model that is not the proposer perceives the 11-dimension
                    vector of the action "merge this amendment into the canon"; the reference
                    function f_v5 of the judge validator computes the mode; the block is written
                    in the frozen ::JUDGE{v5.0} form and checked by the same validator

Nothing here merges anything. A passed amendment only carries the label passed-gates and its
record; the owner merges by hand. Rejections are automatic and carry the failing output verbatim.
Standard library only. Python 3.12.
"""
import argparse
import datetime as dt
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

DIMS = ["int", "cap", "csq", "rel", "cer", "aut", "rev", "evd", "sov", "ine", "ext"]
CONDITIONS = ["self_exempting_proposer", "unconsented_harm", "irreversible_unabsorbable", "consistency_flag"]
FENCE = re.compile(r"```([^\n`]*)\n(.*?)\n```", re.S)
HEADING = re.compile(r"^### (.+?)\s*$", re.M)
CANON_GATE = [
    ("grammar selftest", ["python", "ilang_grammar_validator.py", "--selftest"]),
    ("canon gate (grammar + registry)", ["python", "ilang_grammar_validator.py", "--canon", "."]),
    ("judge selftest", ["python", "ilang_judge_validator.py", "--selftest"]),
    ("JUDGE blocks in SPEC-v5.0.md", ["python", "ilang_judge_validator.py", "--check", "SPEC-v5.0.md"]),
    ("JSON schemas", ["python", "schema/check_schemas.py"]),
    ("symbol audit selftest", ["python", "symbol_audit.py", "--selftest"]),
    ("symbol audit of SPEC-v5.0.md (seal S3)", ["python", "symbol_audit.py", "SPEC-v5.0.md"]),
]
DS_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/") + "/chat/completions"
DS_MODEL = os.environ.get("INTAKE_MODEL", "deepseek-flash")


# ----------------------------------------------------------------------------- helpers
def run(cmd, cwd, timeout=600):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        return 124, "timed out after %d s" % timeout


def fields(body):
    """Issue-form bodies render as '### Label' headings followed by the field's text."""
    out, pos = {}, [(m.group(1).strip(), m.start(), m.end()) for m in HEADING.finditer(body or "")]
    for i, (label, _, end) in enumerate(pos):
        stop = pos[i + 1][1] if i + 1 < len(pos) else len(body)
        out[label] = body[end:stop].strip()
    return out


def fenced(text):
    return [(lang.strip().lower(), code) for lang, code in FENCE.findall(text or "")]


def is_ilang(code):
    lines = [l for l in code.splitlines() if l.strip()]
    return bool(lines) and (lines[0].startswith("::ILANG") or any(l.startswith("::JUDGE{") for l in lines))


def is_diff(lang, code):
    return lang == "diff" or code.lstrip().startswith(("diff --git", "--- a/", "--- ", "Index: "))


def verbatim(title, text):
    return "## %s\n\n```text\n%s\n```\n" % (title, (text or "").rstrip())


def products_lint_cmd(spec):
    files = []
    for root, _, names in os.walk(os.path.join(spec, "products")):
        files += [os.path.relpath(os.path.join(root, n), spec) for n in names if n.endswith(".ilang.md")]
    return ["python", "ilang_grammar_validator.py", "--lint"] + sorted(files) + ["--strict"]


# ----------------------------------------------------------------------------- gate 1
def gate_grammar(spec, blocks, work):
    results, ok = [], True
    n = 0
    for lang, code in blocks:
        if not is_ilang(code):
            continue
        n += 1
        path = os.path.join(work, "block-%d.ilang.md" % n)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(code.rstrip("\n") + "\n")
        if code.lstrip().startswith("::ILANG"):
            c, out = run(["python", os.path.join(spec, "ilang_grammar_validator.py"), "--lint", path, "--strict"], work)
            results.append(("block %d: grammar validator --strict" % n, c, out))
            ok = ok and c == 0
        if "::JUDGE{" in code:
            c, out = run(["python", os.path.join(spec, "ilang_judge_validator.py"), "--check", path], work)
            results.append(("block %d: judge validator --check" % n, c, out))
            ok = ok and c == 0
    return n, ok, results


# ----------------------------------------------------------------------------- gate 2
HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def normalize_diff(text):
    """A diff pasted into a form loses what browsers trim: blank context lines become empty, trailing
    blank context lines disappear. Restore them from the hunk counts; change nothing else."""
    lines, out, i = text.replace("\r\n", "\n").replace("\r", "\n").split("\n"), [], 0
    while i < len(lines):
        m = HUNK.match(lines[i])
        if not m:
            out.append(lines[i]); i += 1
            continue
        out.append(lines[i]); i += 1
        old, new = int(m.group(2) or 1), int(m.group(4) or 1)
        while (old > 0 or new > 0) and i < len(lines):
            l = lines[i]
            if l == "":
                l = " "
            if l.startswith("\\"):
                out.append(l); i += 1
                continue
            if l[0] not in " +-":
                break
            if l[0] == " ":
                old -= 1; new -= 1
            elif l[0] == "-":
                old -= 1
            else:
                new -= 1
            out.append(l); i += 1
        while old > 0 and new > 0:
            out.append(" "); old -= 1; new -= 1
    return "\n".join(out).rstrip("\n") + "\n"


def gate_canon(spec, diff_text, work):
    patch = os.path.join(work, "amendment.diff")
    with open(patch, "w", encoding="utf-8", newline="\n") as f:
        f.write(normalize_diff(diff_text))
    c, out = run(["git", "apply", "--check", "--whitespace=nowarn", patch], spec)
    results = [("git apply --check", c, out)]
    if c != 0:
        return False, results
    c, out = run(["git", "apply", "--whitespace=nowarn", patch], spec)
    results.append(("git apply", c, out))
    if c != 0:
        return False, results
    ok = True
    for name, cmd in CANON_GATE + [("products lint (strict)", products_lint_cmd(spec))]:
        c, out = run(cmd, spec)
        results.append((name, c, out))
        ok = ok and c == 0
    c, out = run(["git", "diff", "--stat"], spec)
    results.append(("git diff --stat (what the amendment changes)", c, out))
    return ok, results


# ----------------------------------------------------------------------------- gate 3
def spec_excerpt(spec, start_marker, end_marker):
    text = open(os.path.join(spec, "SPEC-v5.0.md"), encoding="utf-8").read()
    i = text.find(start_marker)
    j = text.find(end_marker, i + 1) if i >= 0 else -1
    return text[i:j].strip() if i >= 0 and j > i else ""


def perception_prompt(spec, meta, f, diff_text, canon_results):
    routing = spec_excerpt(spec, "::MODULE::ROUTING{", "::MODULE::PRODUCT{")
    source = spec_excerpt(spec, "::MODULE::SOURCE{", "::MODULE::ROUTING{")
    amendment = spec_excerpt(spec, "::MODULE::AMENDMENT{", "::MODULE::SELF_CHECK{")
    vector = spec_excerpt(spec, "::MODULE::VECTOR{", "::MODULE::BOUNDARIES{")
    gate_lines = "\n".join("- %s: exit %d" % (n, c) for n, c, _ in canon_results)
    system = (
        "You are the perceiver in the iLang v5.0 judgment layer. You are not the proposer and you do not decide the mode: "
        "code computes the mode from the vector you return (f_v5). Perceive the 11 dimensions of ONE action from the "
        "record below and nothing else. Values are two-decimal numbers in [0.00, 1.00]; 1.00 is always the most "
        "favorable value (risk dimensions are inverted). A dimension you cannot perceive from the record is reported "
        "in conditions as unknown:<dim>, not guessed. Report a routing condition only when the record shows it. "
        "Answer with one JSON object and nothing else: "
        '{"v": {"int":0.00,"cap":0.00,"csq":0.00,"rel":0.00,"cer":0.00,"aut":0.00,"rev":0.00,"evd":0.00,"sov":0.00,"ine":0.00,"ext":0.00}, '
        '"conditions": [], "conf": 0.00, "reason": "one line, at most 120 characters, letters digits and underscores", '
        '"notes": "at most 600 characters on what in the record drove the values"}. '
        "Allowed condition names: " + ", ".join(CONDITIONS) + ", unknown:<dim>."
    )
    user = (
        "ACTION TO JUDGE: merge the amendment below into the iLang canon (repository ilang-ai/ilang-spec, main branch), "
        "as proposed by GitHub user %s in issue #%s. The proposer is the maker of this rule change and is bound by it first "
        "(MODULE::SOURCE). The canon gate (the spec's own CI) already ran on the patched checkout with these results:\n%s\n\n"
        "=== CANON TEXT THE PERCEPTION RESTS ON ===\n%s\n\n%s\n\n%s\n\n%s\n\n"
        "=== THE PROPOSAL (verbatim from the issue form) ===\n"
        "Clause: %s\n\nThe flaw: %s\n\nThe fix: %s\n\nSOURCE test, the proposer's own answer: %s\n\n"
        "Protection statement (AMENDMENT skin_in_the_game): %s\n\n=== THE DIFF ===\n%s\n"
    ) % (
        meta.get("author", "?"), meta.get("number", "?"), gate_lines, source, routing, amendment, vector,
        f.get("Clause", ""), f.get("The flaw", ""), f.get("The fix", ""), f.get("SOURCE test", ""),
        f.get("Protection statement", ""), diff_text,
    )
    return system, user


def call_deepseek(system, user, key):
    body = {
        "model": DS_MODEL,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0,
        "thinking": {"type": "disabled"},
        "response_format": {"type": "json_object"},
        "max_tokens": 2000,
    }
    req = urllib.request.Request(DS_URL, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read().decode("utf-8"))
    content = data["choices"][0]["message"]["content"]
    return json.loads(content), data.get("usage", {}), data.get("model", DS_MODEL)


def load_judge(spec):
    s = importlib.util.spec_from_file_location("ilang_judge_validator", os.path.join(spec, "ilang_judge_validator.py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def judge_block(spec, perceived, work):
    j = load_judge(spec)
    v = {}
    for d in DIMS:
        x = float(perceived["v"][d])
        if not 0.0 <= x <= 1.0:
            raise ValueError("dimension %s out of range: %s" % (d, x))
        v[d] = round(x, 2)
    conditions = [c for c in perceived.get("conditions", []) if c in CONDITIONS or c.startswith("unknown:")]
    routed = j.route(v, conditions)
    routed = {d: round(float(routed[d]), 2) for d in DIMS}
    mode = j.f_v5(routed)
    score = round(j.action_score(routed), 4)
    conf = min(1.0, max(0.0, float(perceived.get("conf", 0.5))))
    reason = re.sub(r"[^A-Za-z0-9_]+", "_", str(perceived.get("reason", "")).strip()).strip("_")[:120] or "no_reason_given"
    block = "::JUDGE{v5.0}\nV:[%s]\nM:%s|conf:%.2f\nR:%s\n" % (",".join("%s=%.2f" % (d, routed[d]) for d in DIMS), mode, conf, reason)
    path = os.path.join(work, "judge.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(block + "\n")
    c, out = run(["python", os.path.join(spec, "ilang_judge_validator.py"), "--check", path], work)
    return block, mode, score, conditions, routed, (c, out)


# ----------------------------------------------------------------------------- record + verdict
def verdict_for_mode(mode):
    if mode in ("M1", "M2", "M3", "M4"):
        return "passed-gates", False
    if mode == "M5":
        return "needs-evidence", False
    return "rejected:judge", True


def main():
    ap = argparse.ArgumentParser(description="ilang-research intake gate")
    ap.add_argument("--issue", required=True, help="JSON file: the GitHub issue object (gh api .../issues/N)")
    ap.add_argument("--spec", required=True, help="checkout of ilang-ai/ilang-spec")
    ap.add_argument("--records", default="records")
    ap.add_argument("--out", default="out")
    a = ap.parse_args()

    issue = json.load(open(a.issue, encoding="utf-8"))
    labels = [l["name"] if isinstance(l, dict) else str(l) for l in issue.get("labels", [])]
    kind = "amendment" if "amendment" in labels else "counterexample" if "counterexample" in labels else "other"
    meta = {"number": issue.get("number"), "url": issue.get("html_url"), "author": (issue.get("user") or {}).get("login"),
            "title": issue.get("title"), "opened": issue.get("created_at"), "labels": labels, "kind": kind}
    body = issue.get("body") or ""
    f = fields(body)
    os.makedirs(a.out, exist_ok=True)
    work = tempfile.mkdtemp(prefix="intake-", dir=a.out)
    c, spec_commit = run(["git", "rev-parse", "HEAD"], a.spec)
    meta["spec_commit"] = spec_commit.strip()
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    sections, verdict, close = [], None, False

    if kind == "other":
        summary = {"kind": kind, "verdict": "none", "labels_add": [], "close": False}
        json.dump(summary, open(os.path.join(a.out, "summary.json"), "w"), indent=2)
        print("not an intake kind; nothing to do")
        return 0

    # gate 1
    blocks = fenced(body)
    n_blocks, g1_ok, g1 = gate_grammar(a.spec, blocks, work)
    sections.append("## Gate 1: grammar\n\n" + ("%d iLang block(s) found.\n\n" % n_blocks) +
                    "".join(verbatim("%s (exit %d)" % (name, c), out) for name, c, out in g1))
    if not g1_ok:
        verdict, close = "rejected:grammar", True
    elif kind == "counterexample":
        verdict = "counterexample" if n_blocks else "needs-record"
    else:
        diffs = [code for lang, code in blocks if is_diff(lang, code)]
        if not diffs:
            verdict = "needs-record"
            sections.append("## Gate 2: canon\n\nNo diff block in the submission; nothing to apply.\n")
        else:
            g2_ok, g2 = gate_canon(a.spec, diffs[0], work)
            sections.append("## Gate 2: canon (the spec's own CI on the patched checkout)\n\n" +
                            "".join(verbatim("%s (exit %d)" % (name, c), out) for name, c, out in g2))
            if not g2_ok:
                verdict, close = "rejected:canon", True
            else:
                key = os.environ.get("DEEPSEEK_API_KEY", "")
                if not key:
                    verdict = "blocked:no-key"
                    sections.append("## Gate 3: judgment\n\nNot run: the repository has no DEEPSEEK_API_KEY secret. The gate fails closed.\n")
                else:
                    system, user = perception_prompt(a.spec, meta, f, diffs[0], g2)
                    try:
                        perceived, usage, model = call_deepseek(system, user, key)
                        block, mode, score, conditions, routed, chk = judge_block(a.spec, perceived, work)
                        verdict, close = verdict_for_mode(mode)
                        if chk[0] != 0:
                            verdict, close = "blocked:judge-schema", False
                        sections.append(
                            "## Gate 3: judgment\n\nPerceiver: %s (not the proposer). Mode by f_v5 of the judge validator at spec commit %s. "
                            "Conditions applied by MODULE::ROUTING: %s. Action score S=%.4f.\n\n" % (model, meta["spec_commit"][:7], ", ".join(conditions) or "none", score) +
                            verbatim("perception (verbatim JSON from the model)", json.dumps(perceived, ensure_ascii=False, indent=2)) +
                            verbatim("JUDGE block", block) + verbatim("judge validator --check (exit %d)" % chk[0], chk[1]) +
                            verbatim("token usage", json.dumps(usage)))
                    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, KeyError, json.JSONDecodeError) as e:
                        verdict = "blocked:judge-error"
                        sections.append("## Gate 3: judgment\n\nThe perception call or the block check failed: %s\n" % str(e)[:300])

    # record
    rec_dir = os.path.join(a.records, "amendments" if kind == "amendment" else "counterexamples")
    os.makedirs(rec_dir, exist_ok=True)
    rec_path = os.path.join(rec_dir, "%s-issue-%s.md" % (today, meta["number"]))
    head = "# Intake record: issue #%s (%s)\n\n" % (meta["number"], kind) + "".join(
        "- %s: %s\n" % (k, meta[k]) for k in ("url", "author", "title", "opened", "spec_commit")) + "- verdict: %s\n- recorded: %s\n\n" % (verdict, today)
    with open(rec_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(head + "\n".join(sections) + "\n## Submission (verbatim)\n\n" + body.rstrip() + "\n")

    # comment
    explain = {
        "rejected:grammar": "A fenced iLang block in this submission does not pass the canon grammar validator in strict mode. The validator output is in the record. Fix the block and open a new issue.",
        "rejected:canon": "The amendment applies, but the patched canon no longer passes the spec's own CI gate. The failing command and its output are in the record. Repair the proposal and open a new issue.",
        "rejected:judge": "The judgment layer routed this amendment to a stop, defer or decline mode (see the JUDGE block in the record). It is not merged.",
        "needs-evidence": "The judgment layer could not reach a confident mode (M5: ask). Add the evidence it lacked, edit this issue, and the gate runs again.",
        "needs-record": "The submission has no fenced record (an iLang block, or a diff for an amendment). Add it, edit this issue, and the gate runs again.",
        "passed-gates": "Every automatic gate passed. The record is filed. Nothing is merged by this workflow; the owner reads passed items on their own schedule and merges by hand.",
        "counterexample": "Recorded verbatim. A counterexample alone does not change a clause (MODULE::AMENDMENT); an amendment with a proposed fix can.",
        "blocked:no-key": "Gates 1 and 2 passed; gate 3 could not run because the repository has no model key configured. The gate fails closed until the owner adds it.",
        "blocked:judge-error": "Gates 1 and 2 passed; gate 3 failed on a transient error. Re-run the workflow.",
        "blocked:judge-schema": "Gates 1 and 2 passed; the JUDGE block the gate wrote did not pass the judge validator. This is a gate bug; the owner will look.",
    }
    comment = "**Intake: %s**\n\n%s\n\nRecord: `%s` (spec commit `%s`).\n" % (verdict, explain.get(verdict, ""), rec_path.replace("\\", "/"), meta["spec_commit"][:7])
    with open(os.path.join(a.out, "comment.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(comment)
    summary = {"kind": kind, "verdict": verdict, "labels_add": [verdict], "close": close, "record": rec_path.replace("\\", "/"), "spec_commit": meta["spec_commit"]}
    json.dump(summary, open(os.path.join(a.out, "summary.json"), "w"), indent=2)
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
