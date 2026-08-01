from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from scripts.local_authority_bridge import (
    AUTHORITY_BUNDLE_ROUTE,
    STUDIO_ROUTE,
)
from scripts.run_authority_slice import (
    AUTHORITY_SLICE_VERSION,
    BROWSER_MODES,
    run_authority_slice,
)


ROOT = Path(__file__).resolve().parents[1]


def test_end_to_end_authority_slice() -> None:
    summary = run_authority_slice(
        strategy="leapfrog",
        browser_checks=True,
        clean_wheel=True,
    )

    assert summary["schema_version"] == AUTHORITY_SLICE_VERSION
    assert summary["pass"] is True
    assert summary["strategy"] == "leapfrog"
    assert summary["command_equals_bridge"] is True
    assert summary["bridge_equals_committed_bundle"] is True
    assert summary["studio_route"] == STUDIO_ROUTE
    assert summary["authority_bundle_route"] == AUTHORITY_BUNDLE_ROUTE
    assert summary["module_count"] == 720
    assert summary["string_count"] == 24
    assert summary["modules_per_string"] == 30
    assert summary["dc_nameplate_power_kwp"] == 475.2
    assert summary["inverter_apparent_power_kva"] == 352.0
    assert summary["browser_modes"] == list(BROWSER_MODES)
    assert summary["clean_wheel"] is True
    assert summary["equipment_evidence_state"] == "incomplete_evidence"
    assert summary["response_hash"].startswith("sha256:")
    assert summary["response_bytes_sha256"].startswith("sha256:")


def test_authority_slice_cli_can_run_without_heavy_subgates() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_authority_slice.py",
            "--skip-browser-checks",
            "--skip-clean-wheel",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["pass"] is True
    assert payload["command_equals_bridge"] is True
    assert payload["bridge_equals_committed_bundle"] is True
    assert payload["browser_modes"] == []
    assert payload["clean_wheel"] is False


def test_end_to_end_harness_uses_existing_authority_paths() -> None:
    source = (ROOT / "scripts" / "run_authority_slice.py").read_text(
        encoding="utf-8"
    )
    bridge_source = (
        ROOT / "scripts" / "local_authority_bridge.py"
    ).read_text(encoding="utf-8")

    assert "scripts/build_authority_bundle.py" in source
    assert "validate_authority_bundle_payload" in source
    assert "validate_inverter_block_wheel.py" in source
    assert "studio-authority.test.mjs" in source
    assert "studio-authority-evidence.test.mjs" in source
    assert "authority_response_json" in bridge_source
    assert "AUTHORITY_BUNDLE_PATH.read_bytes()" not in bridge_source
    assert "eval(" not in source
    assert "shell=True" not in source
