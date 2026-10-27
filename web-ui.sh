#!/usr/bin/env bash

# Serves the minimal web UI (ui/) and the data/ directory it reads from,
# rooted at the repo so relative fetches like ../data/sentences.tsv resolve.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${GERMAN_PRACTICE_UI_PORT:-8000}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required to serve the web UI." >&2
  exit 1
fi

echo "Serving Deutsch-Lernprogramm UI at http://localhost:${PORT}/ui/"
cd "$SCRIPT_DIR"
exec python3 -m http.server "$PORT" --bind 0.0.0.0
