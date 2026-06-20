import json
import threading
import urllib.request
import urllib.error
from http.server import HTTPServer

from todo.server import HealthHandler


def test_health_endpoint_returns_200_and_valid_json():
    server = HTTPServer(("127.0.0.1", 0), HealthHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/health") as resp:
            assert resp.status == 200
            data = json.loads(resp.read().decode())
            assert data["status"] == "ok"
            assert "timestamp" in data
    finally:
        thread.join(timeout=5)
        server.server_close()


def test_unknown_route_returns_404():
    server = HTTPServer(("127.0.0.1", 0), HealthHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/unknown")
        with urllib.request.urlopen(req):
            pass
    except urllib.error.HTTPError as e:
        assert e.code == 404
        data = json.loads(e.read().decode())
        assert "error" in data
    finally:
        thread.join(timeout=5)
        server.server_close()


def test_server_starts_and_stops_cleanly():
    server = HTTPServer(("127.0.0.1", 0), HealthHandler)
    port = server.server_address[1]
    assert port > 0
    server.server_close()
