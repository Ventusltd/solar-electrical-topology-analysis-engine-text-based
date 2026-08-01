from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
from threading import Thread
from typing import Iterator
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from scripts.build_authority_bundle import (
    AUTHORITY_BUNDLE_PATH,
    authority_response_json,
)
from scripts.local_authority_bridge import (
    AUTHORITY_BUNDLE_ROUTE,
    HEALTH_ROUTE,
    LOCAL_AUTHORITY_BRIDGE_VERSION,
    STUDIO_ROUTE,
    create_server,
)


ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def running_bridge(*, strategy: str = "leapfrog") -> Iterator[str]:
    server = create_server(host="127.0.0.1", port=0, strategy=strategy)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[:2]
    try:
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def fetch(url: str, *, method: str = "GET") -> tuple[bytes, object]:
    request = Request(url, method=method)
    with urlopen(request, timeout=10) as response:
        return response.read(), response.headers


def test_bridge_serves_exact_python_authority_response() -> None:
    expected = (authority_response_json("leapfrog") + "\n").encode("utf-8")
    committed = AUTHORITY_BUNDLE_PATH.read_bytes()

    with running_bridge() as base:
        body, headers = fetch(base + AUTHORITY_BUNDLE_ROUTE)

    payload = json.loads(body)
    assert body == expected == committed
    assert headers["Content-Type"] == "application/json; charset=utf-8"
    assert headers["Cache-Control"] == "no-store"
    assert headers["X-Authority-Response-Hash"] == payload["response_hash"]
    assert headers["X-Authority-Strategy"] == "leapfrog"


def test_bridge_serves_existing_studio_without_browser_recalculation_fork() -> None:
    with running_bridge() as base:
        index, _ = fetch(base + STUDIO_ROUTE)
        authority_view, _ = fetch(
            base + "/v10-development/authority/authority-view.js"
        )
        authority_evidence, _ = fetch(
            base + "/v10-development/authority/authority-evidence.js"
        )
        playground, _ = fetch(base + "/v10-development/topology-studio.html")

    assert index == (
        ROOT / "v10-development" / "authority" / "index.html"
    ).read_bytes()
    assert authority_view == (
        ROOT / "v10-development" / "authority" / "authority-view.js"
    ).read_bytes()
    assert authority_evidence == (
        ROOT / "v10-development" / "authority" / "authority-evidence.js"
    ).read_bytes()
    assert playground == (
        ROOT / "v10-development" / "topology-studio.html"
    ).read_bytes()


def test_root_redirect_and_health_contract() -> None:
    with running_bridge(strategy="sequential") as base:
        redirected, _ = fetch(base + "/")
        health, _ = fetch(base + HEALTH_ROUTE)

    assert b"SOLAR DC TOPOLOGY STUDIO" in redirected
    assert json.loads(health) == {
        "authority_bundle_route": AUTHORITY_BUNDLE_ROUTE,
        "bridge_version": LOCAL_AUTHORITY_BRIDGE_VERSION,
        "status": "ready",
        "strategy": "sequential",
        "studio_route": STUDIO_ROUTE,
    }


def test_head_returns_headers_without_body() -> None:
    with running_bridge() as base:
        body, headers = fetch(base + AUTHORITY_BUNDLE_ROUTE, method="HEAD")

    assert body == b""
    assert int(headers["Content-Length"]) > 1000
    assert headers["X-Authority-Strategy"] == "leapfrog"


def test_unknown_route_is_rejected() -> None:
    with running_bridge() as base:
        with pytest.raises(HTTPError) as caught:
            fetch(base + "/not-an-authority-path")

    assert caught.value.code == 404


def test_bridge_rejects_invalid_strategy_and_port() -> None:
    with pytest.raises(ValueError, match="unsupported authority strategy"):
        create_server(strategy="invented")
    with pytest.raises(ValueError, match="port must be between"):
        create_server(port=70000)
