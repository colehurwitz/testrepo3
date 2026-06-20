import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            body = {
                "status": "ok",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self.wfile.write(json.dumps(body).encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            body = {"error": "Not found"}
            self.wfile.write(json.dumps(body).encode())

    def log_message(self, format, *args):
        pass


class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


def run_server(port: int = 8080) -> None:
    if not 1 <= port <= 65535:
        raise ValueError(f"Port must be between 1 and 65535, got {port}")
    server_address = ("", port)
    httpd = ReusableHTTPServer(server_address, HealthHandler)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()
