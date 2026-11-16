#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The pull-request gate of the Hugging Face dataset i-Lang/media-chain. Runs on a schedule from ilang-research.

  python gate/media_chain_prs.py --spec <ilang-spec checkout> [--repo i-Lang/media-chain] [--only N] [--dry-run]

For every open pull request of the dataset it reads the head commit, skips the request if this gate already answered
that head (its own comment carries "gate: <sha>"), finds the series folders the request adds or changes, downloads the
dataset's own tools/check_series.py from main and those folders from the request, runs the check with the canon's two
validators, and answers:

  every series passes              the request is merged, with the verdict lines as the merge comment
  a series fails                   the verdict lines are posted as a comment, verbatim; the request stays open
  files outside series/<ID>/       the request stays open with a comment naming them; the examples, the card and the
                                   tools change only through the maintainer

Nothing in a submission is edited. Code decides. Requires HF_TOKEN in the environment (write on the dataset) and
huggingface_hub; the canon validators come from the checkout given with --spec.
"""
import argparse
import io
import json
import os
import subprocess
import sys
import tempfile

from huggingface_hub import HfApi, hf_hub_download, snapshot_download

REPO = "i-Lang/media-chain"
MARK = "gate: "


def head_sha(api, repo, num):
    commits = api.list_repo_commits(repo, repo_type="dataset", revision="refs/pr/%d" % num)
    return commits[0].commit_id if commits else None


def tree(api, repo, revision):
    out = {}
    for e in api.list_repo_tree(repo, repo_type="dataset", revision=revision, recursive=True):
        if getattr(e, "blob_id", None) is not None or getattr(e, "size", None) is not None:
            lfs = getattr(e, "lfs", None)
            out[e.path] = (lfs.sha256 if lfs is not None else None, getattr(e, "blob_id", None), getattr(e, "size", None))
    return out


def changed_paths(base, head):
    return sorted(p for p in head if p not in base or base[p] != head[p]) + sorted(p for p in base if p not in head)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--repo", default=REPO)
    ap.add_argument("--only", type=int, action="append", default=[])
    ap.add_argument("--dry-run", action="store_true", help="judge and print, post nothing, merge nothing")
    a = ap.parse_args()
    token = os.environ.get("HF_TOKEN")
    if not token:
        sys.exit("HF_TOKEN is not set")
    api = HfApi(token=token)
    me = api.whoami()["name"]
    base = tree(api, a.repo, "main")
    tmp = tempfile.mkdtemp(prefix="media-chain-gate-")
    checker = hf_hub_download(a.repo, "tools/check_series.py", repo_type="dataset", revision="main", cache_dir=tmp, token=token)
    prs = [d for d in api.get_repo_discussions(a.repo, repo_type="dataset", discussion_type="pull_request", discussion_status="open")]
    if a.only:
        prs = [d for d in prs if d.num in a.only]
    print("open pull requests: %d" % len(prs))
    for d in prs:
        num = d.num
        sha = head_sha(api, a.repo, num)
        if not sha:
            print("#%d: no head commit, skipped" % num)
            continue
        det = api.get_discussion_details(a.repo, num, repo_type="dataset")
        # answered: this gate already posted a verdict for this head, unless that post ended in a merge that did not happen
        answered = any(getattr(e, "author", None) == me and MARK + sha in (getattr(e, "content", "") or "")
                       and "merge did not happen" not in (getattr(e, "content", "") or "") for e in det.events)
        if answered:
            print("#%d (%s): already answered at %s" % (num, d.title, sha[:7]))
            continue
        head = tree(api, a.repo, "refs/pr/%d" % num)
        changed = changed_paths(base, head)
        outside = [p for p in changed if not (p.startswith("series/") and p.count("/") >= 2)]
        ids = sorted({p.split("/")[1] for p in changed if p.startswith("series/") and p.count("/") >= 2})
        lines = [MARK + sha, "pull request #%d by %s, %d changed path(s)" % (num, d.author, len(changed))]
        verdict_ok = False
        if outside:
            lines.append("FAIL: a pull request changes series/<ID>/ only; these paths are outside it: " + ", ".join(outside[:20]))
        elif not ids:
            lines.append("FAIL: no series/<ID>/ folder in this pull request")
        else:
            snap = snapshot_download(a.repo, repo_type="dataset", revision="refs/pr/%d" % num, cache_dir=tmp,
                                     local_dir=os.path.join(tmp, "pr-%d" % num), token=token,
                                     allow_patterns=["series/%s/*" % i for i in ids])
            out = os.path.join(tmp, "verdict-%d.json" % num)
            r = subprocess.run([sys.executable, "-X", "utf8", checker, "--spec", a.spec, "--root", snap, "--json", out]
                               + sum((["--only", os.path.join(snap, "series", i)] for i in ids), []),
                               capture_output=True, text=True, encoding="utf-8")
            lines.extend(l for l in r.stdout.splitlines() if l.strip())
            if r.returncode == 0:
                verdict_ok = True
            if r.stderr.strip() and r.returncode not in (0, 1):
                lines.append("gate error: " + r.stderr.strip()[-500:])
        body = "\n".join(lines)
        print("#%d (%s) -> %s\n  %s" % (num, d.title, "merge" if verdict_ok else "stays open", body.replace("\n", "\n  ")))
        if a.dry_run:
            continue
        if verdict_ok:
            try:
                if det.status == "draft":   # a request opened through the library is a draft; the Hub merges only published ones
                    api.change_discussion_status(a.repo, num, "open", repo_type="dataset")
                api.merge_pull_request(a.repo, num, repo_type="dataset", comment=body)
                print("#%d merged" % num)
            except Exception as e:  # a conflict with main, or a permission: say so on the request, keep it open
                api.comment_discussion(a.repo, num, repo_type="dataset", comment=body + "\n\nmerge did not happen: %s" % str(e)[:300])
                print("#%d merge failed: %s" % (num, e))
        else:
            api.comment_discussion(a.repo, num, repo_type="dataset", comment=body)
    print("done")


if __name__ == "__main__":
    main()
