#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for file in ui/index.html ui/styles.css ui/app.js start-ui.sh; do
  if [[ ! -s "$repo_dir/$file" ]]; then
    echo "Expected $file to exist and contain content."
    exit 1
  fi
done

if ! grep -q '../data/sentences.tsv' "$repo_dir/ui/app.js"; then
  echo "Expected the UI to use the terminal app's sentence corpus."
  exit 1
fi

if ! grep -q '../data/separable-verbs.tsv' "$repo_dir/ui/app.js" ||
   ! grep -q '../data/inseparable-verbs.tsv' "$repo_dir/ui/app.js"; then
  echo "Expected the UI to support both verb practice modes."
  exit 1
fi

echo "UI structure test passed"
