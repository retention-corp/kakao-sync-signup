#!/usr/bin/env bash
# public-check.sh — run before pushing this repo to a public remote.
# Fails (exit 1) when a tracked file holds internal names, private paths, emails or keys.
# Usage: tools/public-check.sh [extra-deny-word ...]
# The deny list is read from tools/public-deny.txt (one word per line, not committed when private)
# plus any words given as arguments.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

deny=()
if [[ -f tools/public-deny.txt ]]; then
  while IFS= read -r w; do [[ -n "$w" && "$w" != \#* ]] && deny+=("$w"); done < tools/public-deny.txt
fi
deny+=("$@")

fail=0
# 1. Personal paths and secrets-like strings in tracked text files.
if git grep -nI -E '/Users/[a-z]+/|op://|cfut_[A-Za-z0-9]{10,}|[0-9]{6}-[1-8][0-9]{6}' -- . ':!tools/public-check.sh' >/tmp/public-check.$$ 2>/dev/null; then
  echo "FAIL private paths or secret-like strings:"; cut -c1-160 /tmp/public-check.$$; fail=1
fi
# 2. Deny words.
for w in "${deny[@]}"; do
  if git grep -nI -F -- "$w" -- . ':!tools/public-check.sh' ':!tools/public-deny.txt' >/tmp/public-check.$$ 2>/dev/null; then
    echo "FAIL deny word '$w':"; cut -c1-160 /tmp/public-check.$$ | head -20; fail=1
  fi
done
# 3. Screenshots: OCR scan (macOS only).
if command -v swift >/dev/null && [[ -d docs/screenshots ]]; then
  joined=$(IFS=,; echo "${deny[*]:-}")
  for d in docs/screenshots/*/; do
    swift skills/kakao-sync-signup/scripts/scan-shots.swift "$d" ${joined:+--deny "$joined"} | grep -v '^OK' && fail=1 || true
  done
fi
rm -f /tmp/public-check.$$
if [[ $fail -eq 0 ]]; then echo "public-check: OK"; else echo "public-check: FAIL"; fi
exit $fail
