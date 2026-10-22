#!/usr/bin/env python3
"""Tests for the browser UI server (ui/server.py)."""

import importlib.util
import json
import os
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_PATH = os.path.join(REPO_DIR, "ui", "server.py")

spec = importlib.util.spec_from_file_location("ui_server", SERVER_PATH)
ui_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ui_server)


class ParsingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def write(self, name, content):
        path = os.path.join(self.tmp.name, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
        return path

    def test_sentences_skip_lines_without_tab(self):
        path = self.write("s.tsv", "Hello.\tHallo.\nNo tab here\n")
        self.assertEqual(
            ui_server.load_sentences(path),
            [{"english": "Hello.", "german": "Hallo."}],
        )

    def test_verbs_skip_comments_and_blank_lines(self):
        path = self.write("v.tsv", "# comment\n\nanrufen\tcall up\tIch rufe an.\n")
        self.assertEqual(
            ui_server.load_verbs(path),
            [{"german": "anrufen", "english": "call up", "example": "Ich rufe an."}],
        )

    def test_verbs_tolerate_missing_example(self):
        path = self.write("v.tsv", "fahren\tdrive\n")
        self.assertEqual(
            ui_server.load_verbs(path),
            [{"german": "fahren", "english": "drive", "example": ""}],
        )


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), ui_server.Handler)
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.base = "http://127.0.0.1:%d" % self.server.server_address[1]

    def get(self, path):
        with urllib.request.urlopen(self.base + path, timeout=5) as response:
            return response.status, response.headers, response.read()

    def test_api_data_matches_repo_files(self):
        status, headers, body = self.get("/api/data")
        self.assertEqual(status, 200)
        self.assertIn("application/json", headers["Content-Type"])
        payload = json.loads(body.decode("utf-8"))
        self.assertEqual(len(payload["sentences"]), len(ui_server.load_sentences(ui_server.CORPUS)))
        self.assertEqual(
            len(payload["separableVerbs"]), len(ui_server.load_verbs(ui_server.SEPARABLE_VERBS))
        )
        self.assertEqual(
            len(payload["inseparableVerbs"]), len(ui_server.load_verbs(ui_server.INSEPARABLE_VERBS))
        )
        self.assertTrue(payload["sentences"])

    def test_index_page_is_served(self):
        status, _, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn(b"Deutsch-Lernprogramm", body)

    def test_static_assets_are_served(self):
        for path in ("/app.js", "/style.css"):
            status, _, _ = self.get(path)
            self.assertEqual(status, 200, path)


if __name__ == "__main__":
    unittest.main()
