#!/usr/bin/env bash
set -uo pipefail

metrics_file="${1:-docs/current-metrics.md}"

if [[ ! -f "$metrics_file" ]]; then
  echo "Metrics file not found: $metrics_file"
  exit 1
fi

fail=0
checks=0

while IFS=$'\t' read -r fact expected command; do
  checks=$((checks + 1))
  expected_clean="${expected//,/}"
  actual_raw="$(bash -lc "$command" 2>/dev/null || true)"
  actual_clean="$(printf '%s\n' "$actual_raw" | grep -Eo '[0-9][0-9,]*' | head -n1 | tr -d ',' || true)"

  if [[ -z "$actual_clean" ]]; then
    echo "FAIL [$fact] command produced no numeric output: $command"
    fail=1
    continue
  fi

  if [[ "$actual_clean" != "$expected_clean" ]]; then
    echo "FAIL [$fact] expected $expected_clean, got $actual_clean"
    echo "  command: $command"
    fail=1
  else
    echo "OK   [$fact] = $actual_clean"
  fi
done < <(
  perl -ne '
    if (/^\|\s*(.*?)\s*\|\s*([0-9][0-9,]*)\s*\|\s*`(.*)`\s*\|/) {
      print "$1\t$2\t$3\n";
    }
  ' "$metrics_file"
)

if [[ "$checks" -eq 0 ]]; then
  echo "No metric checks found in $metrics_file"
  exit 1
fi

if [[ "$fail" -ne 0 ]]; then
  exit 1
fi

echo "All metric checks passed ($checks checks)."
