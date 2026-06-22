import json
import threading
import urllib.request
from http.server import HTTPServer

from todo.server import HealthHandler


def _start_server():
    server = HTTPServer(("127.0.0.1", 0), HealthHandler)
    server.allow_reuse_address = True
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, port


def test_health_returns_200_with_json():
    server, port = _start_server()
    try:
        url = f"http://127.0.0.1:{port}/health"
        with urllib.request.urlopen(url) as resp:
            assert resp.status == 200
            body = json.loads(resp.read())
            assert body["status"] == "ok"
            assert "timestamp" in body
    finally:
        server.shutdown()


def test_unknown_route_returns_404():
    server, port = _start_server()
    try:
        url = f"http://127.0.0.1:{port}/nonexistent"
        try:
            urllib.request.urlopen(url)
            assert False, "Expected 404"
        except urllib.error.HTTPError as e:
            assert e.code == 404
            body = json.loads(e.read())
            assert body["error"] == "Not found"
    finally:
        server.shutdown()
