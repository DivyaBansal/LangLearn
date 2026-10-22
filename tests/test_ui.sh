#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
server="$repo_dir/ui/server.py"
port="${GERMAN_PRACTICE_UI_TEST_PORT:-18765}"
base="http://127.0.0.1:$port"

GERMAN_PRACTICE_UI_QUIET=1 python3 "$server" --port "$port" &
server_pid=$!
trap 'kill "$server_pid" 2>/dev/null || true' EXIT

for _ in $(seq 1 50); do
  if curl -fsS "$base/api/data" -o /dev/null 2>/dev/null; then
    break
  fi
  sleep 0.1
done

data="$(curl -fsS "$base/api/data")"
printf '%s' "$data" | python3 -c '
import json, sys
data = json.load(sys.stdin)
assert len(data["sentences"]) > 0, "no sentences"
assert all(s["english"] and s["german"] for s in data["sentences"]), "empty sentence"
assert len(data["separable"]) > 0, "no separable verbs"
assert len(data["inseparable"]) > 0, "no inseparable verbs"
assert all(v["german"] and v["english"] for v in data["separable"] + data["inseparable"]), "empty verb"
' || {
  echo "Expected /api/data to return sentences and verbs."
  exit 1
}

page="$(curl -fsS "$base/")"
if [[ "$page" != *"Deutsch-Lernprogramm"* ]]; then
  echo "Expected the UI page to be served at /."
  exit 1
fi

script_js="$(curl -fsS "$base/app.js")"
if [[ "$script_js" != *"/api/data"* ]]; then
  echo "Expected app.js to be served and load /api/data."
  exit 1
fi

echo "UI API test passed"
