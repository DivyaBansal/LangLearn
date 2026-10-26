#!/usr/bin/env python3
"""
Simple HTTP server for the German language practice web app.

Run with: python3 server.py
Then open: http://localhost:8080
"""

import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = "public"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Serve index.html for root path
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Deutsch-Lernprogramm server running at:")
        print(f"  http://localhost:{PORT}")
        print(f"")
        print(f"Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
