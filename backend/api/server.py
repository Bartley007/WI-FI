"""HTTP server: turns requests into routes.dispatch calls. Standard library only."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import routes


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status, body = routes.dispatch("GET", self.path)
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  # the website runs on another port
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} {fmt % args}")


def serve(port: int = 8000, host: str = "127.0.0.1") -> None:
    print(f"Serving {len(routes.MODULES)} modules on http://{host}:{port}: {', '.join(sorted(routes.MODULES))}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
