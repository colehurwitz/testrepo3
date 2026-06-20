import json
import threading
import time
import urllib.request
from http.server import HTTPServer

from todo.server import HealthHandler


def start_test_server(port: int) -> HTTPServer:
    server = HTTPServer(("", port), HealthHandler)
    server.allow_reuse_address = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.1)
    return server


def test_health_returns_200_with_valid_json() -> None:
    port = 18080
    server = start_test_server(port)
    try:
        with urllib.request.urlopen(f"http://localhost:{port}/health") as resp:
            assert resp.status == 200
            data = json.loads(resp.read().decode())
            assert "status" in data
            assert data["status"] == "ok"
            assert "timestamp" in data
    finally:
        server.shutdown()


def test_unknown_route_returns_404() -> None:
    port = 18081
    server = start_test_server(port)
    try:
        req = urllib.request.Request(f"http://localhost:{port}/unknown")
        try:
            urllib.request.urlopen(req)
            assert False, "Expected 404"
        except urllib.error.HTTPError as e:
            assert e.code == 404
            data = json.loads(e.read().decode())
            assert "error" in data
    finally:
        server.shutdown()
