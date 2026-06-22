import json
import threading
import urllib.request

import pytest

from todo.server import HealthHandler, run_server
from http.server import HTTPServer


@pytest.fixture()
def server_url():
    server = HTTPServer(("127.0.0.1", 0), HealthHandler)
    server.allow_reuse_address = True
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


def test_health_returns_200(server_url):
    resp = urllib.request.urlopen(f"{server_url}/health")
    assert resp.status == 200
    body = json.loads(resp.read())
    assert body["status"] == "ok"
    assert "timestamp" in body


def test_unknown_route_returns_404(server_url):
    req = urllib.request.Request(f"{server_url}/nonexistent")
    with pytest.raises(urllib.error.HTTPError) as exc_info:
        urllib.request.urlopen(req)
    assert exc_info.value.code == 404
    body = json.loads(exc_info.value.read())
    assert body["error"] == "Not found"
