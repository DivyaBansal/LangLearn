#!/usr/bin/env python3
"""Web UI for the German practice app. Serves ui/index.html and a small JSON API
backed by the same TSV files as german-terminal-practice.sh."""
import json, os, random, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("GERMAN_PRACTICE_DATA_DIR", os.path.join(HERE, "..", "data"))
FILES = {
    "sentences": os.environ.get("GERMAN_PRACTICE_CORPUS", os.path.join(DATA_DIR, "sentences.tsv")),
    "separable": os.environ.get("GERMAN_PRACTICE_SEPARABLE_VERBS", os.path.join(DATA_DIR, "separable-verbs.tsv")),
    "inseparable": os.environ.get("GERMAN_PRACTICE_INSEPARABLE_VERBS", os.path.join(DATA_DIR, "inseparable-verbs.tsv")),
}


def load(mode):
    items = []
    with open(FILES[mode], encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if mode == "sentences":
                if len(parts) >= 2:
                    items.append({"english": parts[0], "german": parts[1]})
            else:
                if parts[0].isdigit():  # optional leading index column
                    parts = parts[1:]
                if len(parts) >= 3:
                    items.append({"german": parts[0], "english": parts[1], "example": parts[2]})
    return items


class Handler(BaseHTTPRequestHandler):
    def send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            with open(os.path.join(HERE, "index.html"), "rb") as f:
                return self.send(200, f.read(), "text/html; charset=utf-8")
        if path.startswith("/api/random/"):
            mode = path.rsplit("/", 1)[1]
            if mode in FILES:
                try:
                    items = load(mode)
                except OSError:
                    items = []
                if items:
                    body = json.dumps(random.choice(items), ensure_ascii=False).encode()
                    return self.send(200, body, "application/json; charset=utf-8")
                return self.send(500, b'{"error":"no data"}', "application/json")
        self.send(404, b"Not found", "text/plain")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 8000))
    print(f"Deutsch-Lernprogramm UI: http://localhost:{port}")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
