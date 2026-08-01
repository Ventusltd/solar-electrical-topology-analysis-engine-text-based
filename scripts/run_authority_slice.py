#!/usr/bin/env python3
"""Exercise the complete command-to-bridge-to-Studio authority slice."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from threading import Thread
from typing import Iterator
from urllib.parse import urljoin
from urllib.request import urlopen

try:
    from scripts.build_authority_bundle import AUTHORITY_BUNDLE_PATH, canonical_json
    from scripts.local_authority_bridge import (
        AUTHORITY_BUNDLE_ROUTE,
        STUDIO_ROUTE,
        create_server,
    )
    from scripts.validate_authority_bundle import validate_authority_bundle_payload
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from build_authority_bundle import AUTHORITY_BUNDLE_PATH, canonical_json
    from local_authority_bridge import (
        AUTHORITY_BUNDLE_ROUTE,
        STUDIO_ROUTE,
        create_server,
    )
    from validate_authority_bundle import validate_authority_bundle_payload


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_SLICE_VERSION = "globalgrid2050.solar-dc.authority-slice.v1"
STUDIO_AUTHORITY_TEST = (
    ROOT / "v10-development" / "tests" / "studio-authority.test.mjs"
)
STUDIO_EVIDENCE_TEST = (
    ROOT / "v10-development" / "tests" / "studio-authority-evidence.test.mjs"
)
BROWSER_MODES = ("mode", "bundle", "geometry", "evidence")


class AuthoritySliceError(RuntimeError):
    """The end-to-end authority slice is incomplete or inconsistent."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuthoritySliceError(message)


def _sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def command_response_bytes(strategy: str = "leapfrog") -> bytes:
    """Run the repository command rather than calling its implementation directly."""

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/build_authority_bundle.py",
            "--strategy",
            strategy,
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    require(not completed.stderr, "authority command wrote unexpected stderr")
    return completed.stdout


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


def fetch_bytes(url: str) -> bytes:
    with urlopen(url, timeout=15) as response:
        return response.read()


def run_browser_checks() -> tuple[str, ...]:
    completed_modes: list[str] = []
    for mode in BROWSER_MODES:
        command = (
            ["node", str(STUDIO_EVIDENCE_TEST)]
            if mode == "evidence"
            else ["node", str(STUDIO_AUTHORITY_TEST), mode]
        )
        subprocess.run(command, cwd=ROOT, check=True)
        completed_modes.append(mode)
    return tuple(completed_modes)


def run_clean_wheel_check() -> None:
    subprocess.run(
        [sys.executable, "scripts/validate_inverter_block_wheel.py"],
        cwd=ROOT,
        check=True,
    )


def run_authority_slice(
    *,
    strategy: str = "leapfrog",
    browser_checks: bool = True,
    clean_wheel: bool = True,
) -> dict[str, object]:
    """Run one complete reference authority journey and return its evidence summary."""

    require(strategy == "leapfrog", "the committed reference slice is leapfrog")
    command_bytes = command_response_bytes(strategy)
    committed_bytes = AUTHORITY_BUNDLE_PATH.read_bytes()
    require(
        command_bytes == committed_bytes,
        "command response differs from the committed authority bundle",
    )

    with running_bridge(strategy=strategy) as base:
        bridge_bundle_url = base + AUTHORITY_BUNDLE_ROUTE
        resolved_bundle_url = urljoin(
            base + STUDIO_ROUTE,
            "../../authority-bundles/reference-inverter-block.json",
        )
        require(
            resolved_bundle_url == bridge_bundle_url,
            "Studio relative authority-bundle URL does not resolve to the bridge",
        )
        bridge_bytes = fetch_bytes(bridge_bundle_url)
        studio_html = fetch_bytes(base + STUDIO_ROUTE)
        authority_view = fetch_bytes(
            base + "/v10-development/authority/authority-view.js"
        )
        authority_evidence = fetch_bytes(
            base + "/v10-development/authority/authority-evidence.js"
        )

    require(
        bridge_bytes == command_bytes,
        "bridge response differs from the command response",
    )
    require(
        b"SOLAR DC TOPOLOGY STUDIO" in studio_html,
        "Studio shell was not served by the bridge",
    )
    require(
        b"AUTHORITY_BUNDLE_URL" in authority_view,
        "Studio authority projection does not declare its bundle source",
    )
    require(
        b"authorityEvidence" in authority_evidence,
        "Studio evidence projection was not served by the bridge",
    )

    payload = json.loads(bridge_bytes)
    validation = validate_authority_bundle_payload(payload)
    require(validation["pass"] is True, "authority bundle validation did not pass")

    completed_browser_modes: tuple[str, ...] = ()
    if browser_checks:
        completed_browser_modes = run_browser_checks()
    if clean_wheel:
        run_clean_wheel_check()

    boundary = payload["inverter_block"]["product_boundary"]
    return {
        "schema_version": AUTHORITY_SLICE_VERSION,
        "pass": True,
        "strategy": strategy,
        "response_hash": payload["response_hash"],
        "response_bytes_sha256": _sha256(bridge_bytes),
        "command_equals_bridge": command_bytes == bridge_bytes,
        "bridge_equals_committed_bundle": bridge_bytes == committed_bytes,
        "studio_route": STUDIO_ROUTE,
        "authority_bundle_route": AUTHORITY_BUNDLE_ROUTE,
        "module_count": boundary["module_count"],
        "string_count": boundary["string_count"],
        "modules_per_string": boundary["modules_per_string"],
        "dc_nameplate_power_kwp": boundary["dc_nameplate_power_kwp"],
        "inverter_apparent_power_kva": boundary["inverter_apparent_power_kva"],
        "browser_modes": list(completed_browser_modes),
        "clean_wheel": clean_wheel,
        "equipment_evidence_state": payload["inverter_block"][
            "equipment_evidence"
        ]["state"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the complete authoritative reference-block slice.",
    )
    parser.add_argument(
        "--strategy",
        choices=("leapfrog",),
        default="leapfrog",
    )
    parser.add_argument("--skip-browser-checks", action="store_true")
    parser.add_argument("--skip-clean-wheel", action="store_true")
    parser.add_argument(
        "--version",
        action="version",
        version=AUTHORITY_SLICE_VERSION,
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        summary = run_authority_slice(
            strategy=args.strategy,
            browser_checks=not args.skip_browser_checks,
            clean_wheel=not args.skip_clean_wheel,
        )
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError, AuthoritySliceError) as exc:
        raise SystemExit(f"authority slice failed: {exc}") from exc
    print(canonical_json(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
