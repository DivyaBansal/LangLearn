#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${GERMAN_PRACTICE_UI_PORT:-8000}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required to serve the UI."
  exit 1
fi

echo "Deutschdeck is available at http://localhost:${PORT}/ui/"
echo "Press Ctrl+C to stop."
cd "$SCRIPT_DIR"
exec python3 -m http.server "$PORT" --bind 0.0.0.0
