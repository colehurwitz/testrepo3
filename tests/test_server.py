import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

from todo.server import HealthHandler


def test_health_endpoint_returns_200_with_valid_json():
    server = HTTPServer(("127.0.0.1", 0), HealthHandler)
    server.allow_reuse_address = True
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        url = f"http://127.0.0.1:{port}/health"
        with urllib.request.urlopen(url, timeout=5) as response:
            assert response.status == 200
            body = json.loads(response.read().decode())
            assert "status" in body
            assert body["status"] == "ok"
            assert "timestamp" in body
    finally:
        server.shutdown()


def test_unknown_route_returns_404():
    server = HTTPServer(("127.0.0.1", 0), HealthHandler)
    server.allow_reuse_address = True
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        url = f"http://127.0.0.1:{port}/unknown"
        try:
            urllib.request.urlopen(url, timeout=5)
            assert False, "Expected 404 error"
        except urllib.error.HTTPError as e:
            assert e.code == 404
            body = json.loads(e.read().decode())
            assert "error" in body
            assert body["error"] == "Not found"
    finally:
        server.shutdown()


def test_server_starts_and_shuts_down_cleanly():
    server = HTTPServer(("127.0.0.1", 0), HealthHandler)
    server.allow_reuse_address = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    assert thread.is_alive()
    server.shutdown()
    thread.join(timeout=2)
    assert not thread.is_alive()
