from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sync_programme_state.py"


def load_sync_module():
    spec = importlib.util.spec_from_file_location("sync_programme_state", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_programme_state_schema_arithmetic_and_capability_boundaries() -> None:
    sync = load_sync_module()
    state = json.loads((ROOT / "programme-state.json").read_text(encoding="utf-8"))

    sync.validate_state(state)

    block = state["reference_inverter_block"]
    assert block == {
        "module_technology": "bifacial",
        "module_rated_power_wp": 660,
        "modules_per_string": 30,
        "string_rated_power_kwp": 19.8,
        "strings": 24,
        "module_count": 720,
        "dc_nameplate_power_kwp": 475.2,
        "inverter_apparent_power_kva": 352,
        "dc_ac_nameplate_ratio": 1.35,
    }
    assert state["current_build"] == "Build 025.5D1"
    assert state["active_gate"].startswith("TS-005")
    assert state["next_single_goal"].startswith("MB-10")
    assert state["validation"]["suites"][0] == {
        "name": "Python",
        "passed": 334,
        "total": 334,
    }
    assert any(
        item["name"] == "Inverter-block clean wheel"
        and item["passed"] == item["total"] == 1
        for item in state["validation"]["suites"]
    )
    assert "weighted_programme_progress" not in state
    assert "progress_percent" not in state


def test_readme_and_dashboard_are_exact_manifest_projections() -> None:
    sync = load_sync_module()
    state = sync.load_json(sync.MANIFEST_PATH)
    sync.validate_state(state)
    sync.check_outputs(state)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    dashboard = (ROOT / "progress-dashboard.html").read_text(encoding="utf-8")
    assert readme.count(sync.README_START) == 1
    assert readme.count(sync.README_END) == 1
    assert dashboard == sync.render_dashboard(state)


def test_stale_manual_status_claims_are_absent() -> None:
    public_state = (
        (ROOT / "README.md").read_text(encoding="utf-8")
        + (ROOT / "progress-dashboard.html").read_text(encoding="utf-8")
    )
    for stale in (
        "BUILD 024 ACTIVE",
        "Total validated tests</small><strong>176",
        "31.25%",
        "width:31.25%",
        "Current programme: Build 024",
        "Python authority suite</small><strong>140",
    ):
        assert stale not in public_state


def test_programme_state_check_command_passes() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert "generated outputs are in sync" in completed.stdout
