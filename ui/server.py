#!/usr/bin/env python3
"""Serve the browser UI for the German practice app.

Reads the same data files as german-terminal-practice.sh and exposes them as
JSON at /api/data. Uses only the Python standard library.

Usage:
  python3 ui/server.py [--port 8000]

Honours the same environment variables as the terminal script:
  GERMAN_PRACTICE_DATA_DIR, GERMAN_PRACTICE_CORPUS,
  GERMAN_PRACTICE_SEPARABLE_VERBS, GERMAN_PRACTICE_INSEPARABLE_VERBS
"""

import argparse
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

UI_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_DIR = os.path.dirname(UI_DIR)
DATA_DIR = os.environ.get("GERMAN_PRACTICE_DATA_DIR", os.path.join(SCRIPT_DIR, "data"))
CORPUS = os.environ.get("GERMAN_PRACTICE_CORPUS", os.path.join(DATA_DIR, "sentences.tsv"))
SEPARABLE_VERBS = os.environ.get(
    "GERMAN_PRACTICE_SEPARABLE_VERBS", os.path.join(DATA_DIR, "separable-verbs.tsv")
)
INSEPARABLE_VERBS = os.environ.get(
    "GERMAN_PRACTICE_INSEPARABLE_VERBS", os.path.join(DATA_DIR, "inseparable-verbs.tsv")
)


def read_lines(path):
    with open(path, encoding="utf-8") as handle:
        return [line.rstrip("\n") for line in handle]


def load_sentences(path):
    sentences = []
    for line in read_lines(path):
        # Same rule as the terminal script: a line needs a TAB separator.
        if "\t" not in line:
            continue
        english, german = line.split("\t", 1)
        sentences.append({"english": english, "german": german})
    return sentences


def load_verbs(path):
    verbs = []
    for line in read_lines(path):
        if not line or line.startswith("#"):
            continue
        fields = (line.split("\t") + ["", "", ""])[:3]
        verbs.append({"german": fields[0], "english": fields[1], "example": fields[2]})
    return verbs


def build_payload():
    return {
        "sentences": load_sentences(CORPUS),
        "separableVerbs": load_verbs(SEPARABLE_VERBS),
        "inseparableVerbs": load_verbs(INSEPARABLE_VERBS),
    }


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=UI_DIR, **kwargs)

    def do_GET(self):
        if self.path == "/api/data":
            try:
                body = json.dumps(build_payload(), ensure_ascii=False).encode("utf-8")
            except OSError as error:
                self.send_error(500, f"Could not read data files: {error}")
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description="Browser UI for the German practice app")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Deutsch-Lernprogramm UI: http://{args.host}:{args.port}/  (Strg+C zum Beenden)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
