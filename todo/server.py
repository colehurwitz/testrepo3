import json
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "status": "ok",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())

    def log_message(self, format: str, *args) -> None:
        pass


def run_server(port: int = 8080) -> HTTPServer:
    server = HTTPServer(("", port), HealthHandler)
    print(f"Server running on port {port}")
    server.serve_forever()
    return server
