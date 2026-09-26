#!/usr/bin/env bash
# T2 (b): run the judge track for the five models chosen from T2 (a) (best judge_jcs per maker),
# one after another, with the ilang-conformance runner as pinned in that repository.
# Usage: bash t2b_run.sh /path/to/ilang-conformance
set -u
CONF="${1:?path to ilang-conformance}"
cd "$CONF" || exit 1
for v in relay-qwen3.8-max relay-gemini-3.8-flash relay-gpt-6-astra orcarouter-deepseek-free relay-hy3; do
  echo "=== $v $(date -u +%FT%TZ) ==="
  python run.py --vendor "$v" --track judge --concurrency 4 2>&1 | tail -3
done
echo "=== done $(date -u +%FT%TZ) ==="
ls -dt runs/*-2026* | head -5
