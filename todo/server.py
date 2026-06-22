import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = json.dumps({
                "status": "ok",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body.encode())
        else:
            body = json.dumps({"error": "Not found"})
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body.encode())

    def log_message(self, format, *args):
        pass


def run_server(port: int = 8080):
    server = HTTPServer(("", port), HealthHandler)
    server.allow_reuse_address = True
    server.serve_forever()
