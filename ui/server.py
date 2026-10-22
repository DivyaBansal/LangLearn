#!/usr/bin/env python3
"""Local web UI for german-terminal-practice.sh.

Serves the static front-end in this directory and a small JSON API that reads
the same TSV files as the terminal script. Standard library only.

Usage:
  python3 ui/server.py [--host 127.0.0.1] [--port 8000]

The data file locations honour the same environment variables as the script:
GERMAN_PRACTICE_DATA_DIR, GERMAN_PRACTICE_CORPUS,
GERMAN_PRACTICE_SEPARABLE_VERBS and GERMAN_PRACTICE_INSEPARABLE_VERBS.
"""

import argparse
import json
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

UI_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(UI_DIR)
DATA_DIR = os.environ.get("GERMAN_PRACTICE_DATA_DIR", os.path.join(REPO_DIR, "data"))
CORPUS = os.environ.get("GERMAN_PRACTICE_CORPUS", os.path.join(DATA_DIR, "sentences.tsv"))
SEPARABLE_VERBS = os.environ.get(
    "GERMAN_PRACTICE_SEPARABLE_VERBS", os.path.join(DATA_DIR, "separable-verbs.tsv")
)
INSEPARABLE_VERBS = os.environ.get(
    "GERMAN_PRACTICE_INSEPARABLE_VERBS", os.path.join(DATA_DIR, "inseparable-verbs.tsv")
)


def read_lines(path):
    """Return non-comment, non-blank lines, like grep -vE '^(#|$)'."""
    with open(path, encoding="utf-8") as handle:
        return [
            line.rstrip("\n")
            for line in handle
            if line.strip() and not line.startswith("#")
        ]


def load_sentences():
    """Return [{english, german}] pairs; lines without a TAB are skipped."""
    pairs = []
    for line in read_lines(CORPUS):
        english, sep, german = line.partition("\t")
        if sep:
            pairs.append({"english": english, "german": german})
    return pairs


def load_verbs(path):
    """Return [{german, english, example}] entries from a verb TSV file."""
    verbs = []
    for line in read_lines(path):
        parts = (line.split("\t") + ["", "", ""])[:3]
        verbs.append({"german": parts[0], "english": parts[1], "example": parts[2]})
    return verbs


def load_data():
    return {
        "sentences": load_sentences(),
        "separable": load_verbs(SEPARABLE_VERBS),
        "inseparable": load_verbs(INSEPARABLE_VERBS),
    }


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/data":
            try:
                body = json.dumps(load_data(), ensure_ascii=False).encode("utf-8")
            except OSError as error:
                self.send_error(500, f"Could not read practice data: {error}")
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, fmt, *args):
        if os.environ.get("GERMAN_PRACTICE_UI_QUIET"):
            return
        super().log_message(fmt, *args)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)

    handler = partial(Handler, directory=UI_DIR)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Deutsch-Lernprogramm UI: http://{args.host}:{args.port}/", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
