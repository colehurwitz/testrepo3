import json
import threading
import urllib.request
from http.server import HTTPServer

from todo.server import HealthHandler


def test_health_endpoint_returns_200_and_valid_json():
    server = HTTPServer(("", 0), HealthHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    url = f"http://localhost:{port}/health"
    response = urllib.request.urlopen(url)

    assert response.status == 200
    data = json.loads(response.read().decode())
    assert data["status"] == "ok"
    assert "timestamp" in data

    thread.join()
    server.server_close()


def test_unknown_route_returns_404():
    server = HTTPServer(("", 0), HealthHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    url = f"http://localhost:{port}/unknown"
    try:
        urllib.request.urlopen(url)
        assert False, "Expected 404"
    except urllib.error.HTTPError as e:
        assert e.code == 404
        data = json.loads(e.read().decode())
        assert "error" in data

    thread.join()
    server.server_close()


def test_server_starts_and_stops():
    server = HTTPServer(("", 0), HealthHandler)
    port = server.server_address[1]
    assert port > 0
    server.server_close()
