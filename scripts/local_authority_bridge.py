#!/usr/bin/env python3
"""Serve the Python-owned authority response and existing Studio locally."""

from __future__ import annotations

import argparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
from typing import Final
from urllib.parse import urlsplit

try:
    from scripts.build_authority_bundle import authority_response_json
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from build_authority_bundle import authority_response_json


ROOT: Final = Path(__file__).resolve().parents[1]
LOCAL_AUTHORITY_BRIDGE_VERSION: Final = (
    "globalgrid2050.solar-dc.local-authority-bridge.v1"
)
DEFAULT_HOST: Final = "127.0.0.1"
DEFAULT_PORT: Final = 8765
HEALTH_ROUTE: Final = "/health"
STUDIO_ROUTE: Final = "/v10-development/authority/index.html"
AUTHORITY_BUNDLE_ROUTE: Final = (
    "/authority-bundles/reference-inverter-block.json"
)

STATIC_ROUTES: Final[dict[str, Path]] = {
    STUDIO_ROUTE: ROOT / "v10-development" / "authority" / "index.html",
    "/v10-development/authority/authority-view.js": (
        ROOT / "v10-development" / "authority" / "authority-view.js"
    ),
    "/v10-development/authority/authority-evidence.js": (
        ROOT / "v10-development" / "authority" / "authority-evidence.js"
    ),
    "/v10-development/topology-studio.html": (
        ROOT / "v10-development" / "topology-studio.html"
    ),
}


def authority_response_bytes(strategy: str = "leapfrog") -> bytes:
    """Return the exact newline-terminated response served by the bridge."""

    return (authority_response_json(strategy) + "\n").encode("utf-8")


def _json_bytes(payload: object) -> bytes:
    return (
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def _content_type(path: Path) -> str:
    guessed, _ = mimetypes.guess_type(path.name)
    if guessed is None:
        return "application/octet-stream"
    if guessed.startswith("text/") or guessed in {
        "application/javascript",
        "application/json",
    }:
        return f"{guessed}; charset=utf-8"
    return guessed


def make_handler(
    *,
    strategy: str = "leapfrog",
    root: Path = ROOT,
) -> type[BaseHTTPRequestHandler]:
    """Create a request handler bound to one strategy and repository root."""

    static_routes = {
        route: root / path.relative_to(ROOT)
        for route, path in STATIC_ROUTES.items()
    }

    class AuthorityBridgeHandler(BaseHTTPRequestHandler):
        server_version = "GlobalGrid2050AuthorityBridge/1"

        def log_message(self, format: str, *args: object) -> None:
            return

        def do_HEAD(self) -> None:  # noqa: N802 - required HTTP handler name
            self._handle(send_body=False)

        def do_GET(self) -> None:  # noqa: N802 - required HTTP handler name
            self._handle(send_body=True)

        def _send(
            self,
            status: HTTPStatus,
            body: bytes,
            *,
            content_type: str,
            send_body: bool,
            extra_headers: dict[str, str] | None = None,
        ) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Access-Control-Allow-Origin", "*")
            for name, value in (extra_headers or {}).items():
                self.send_header(name, value)
            self.end_headers()
            if send_body:
                self.wfile.write(body)

        def _redirect(self, location: str, *, send_body: bool) -> None:
            body = _json_bytes({"location": location})
            self._send(
                HTTPStatus.FOUND,
                body,
                content_type="application/json; charset=utf-8",
                send_body=send_body,
                extra_headers={"Location": location},
            )

        def _handle(self, *, send_body: bool) -> None:
            route = urlsplit(self.path).path

            if route in {"/", "/v10-development/authority/"}:
                self._redirect(STUDIO_ROUTE, send_body=send_body)
                return

            if route == HEALTH_ROUTE:
                body = _json_bytes(
                    {
                        "bridge_version": LOCAL_AUTHORITY_BRIDGE_VERSION,
                        "strategy": strategy,
                        "studio_route": STUDIO_ROUTE,
                        "authority_bundle_route": AUTHORITY_BUNDLE_ROUTE,
                        "status": "ready",
                    }
                )
                self._send(
                    HTTPStatus.OK,
                    body,
                    content_type="application/json; charset=utf-8",
                    send_body=send_body,
                )
                return

            if route == AUTHORITY_BUNDLE_ROUTE:
                body = authority_response_bytes(strategy)
                payload = json.loads(body)
                self._send(
                    HTTPStatus.OK,
                    body,
                    content_type="application/json; charset=utf-8",
                    send_body=send_body,
                    extra_headers={
                        "X-Authority-Response-Hash": str(payload["response_hash"]),
                        "X-Authority-Strategy": strategy,
                    },
                )
                return

            static_path = static_routes.get(route)
            if static_path is not None and static_path.is_file():
                body = static_path.read_bytes()
                self._send(
                    HTTPStatus.OK,
                    body,
                    content_type=_content_type(static_path),
                    send_body=send_body,
                )
                return

            body = _json_bytes({"error": "not_found", "path": route})
            self._send(
                HTTPStatus.NOT_FOUND,
                body,
                content_type="application/json; charset=utf-8",
                send_body=send_body,
            )

    return AuthorityBridgeHandler


def create_server(
    *,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    strategy: str = "leapfrog",
    root: Path = ROOT,
) -> ThreadingHTTPServer:
    """Create, but do not start, a local authority bridge server."""

    if strategy not in {"leapfrog", "sequential"}:
        raise ValueError(f"unsupported authority strategy: {strategy}")
    if not 0 <= port <= 65535:
        raise ValueError("port must be between 0 and 65535")
    return ThreadingHTTPServer(
        (host, port),
        make_handler(strategy=strategy, root=root),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Serve the authoritative reference inverter block locally.",
    )
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument(
        "--strategy",
        choices=("leapfrog", "sequential"),
        default="leapfrog",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Handle one request and exit.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=LOCAL_AUTHORITY_BRIDGE_VERSION,
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    server = create_server(
        host=args.host,
        port=args.port,
        strategy=args.strategy,
    )
    try:
        host, port = server.server_address[:2]
        print(
            json.dumps(
                {
                    "bridge_version": LOCAL_AUTHORITY_BRIDGE_VERSION,
                    "host": host,
                    "port": port,
                    "strategy": args.strategy,
                    "studio_url": f"http://{host}:{port}{STUDIO_ROUTE}",
                },
                sort_keys=True,
            ),
            flush=True,
        )
        if args.once:
            server.handle_request()
        else:
            server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
