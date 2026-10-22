#!/usr/bin/env bash
# Serves the browser UI for the German practice app.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${1:-8080}"
echo "Deutsch-Lernprogramm: http://localhost:$PORT/ui/  (Strg+C zum Beenden)"
cd "$SCRIPT_DIR" && exec python3 -m http.server "$PORT" --bind 0.0.0.0
