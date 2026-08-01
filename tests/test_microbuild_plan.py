from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from scripts.check_microbuild_plan import (
    DEFAULT_PLAN_PATH,
    PlanValidationError,
    load_plan,
    validate_plan,
)


def test_manifest_contract_has_twenty_ordered_steps_and_one_active_gate() -> None:
    plan = load_plan()
    summary = validate_plan(plan)

    assert summary == {
        "pass": True,
        "programme_id": "twenty-step-autopilot-20260801",
        "manifest_revision": 1,
        "active_step": "MB-01",
        "active_status": "active",
        "active_test_id": "manifest_contract",
        "next_step": "MB-02",
        "passed_steps": 0,
        "planned_steps": 19,
        "total_steps": 20,
    }
    assert [item["id"] for item in plan["steps"]] == [
        f"MB-{ordinal:02d}" for ordinal in range(1, 21)
    ]
    assert [item["phase"] for item in plan["steps"][:10]] == ["A"] * 10
    assert [item["phase"] for item in plan["steps"][10:]] == ["B"] * 10
    assert len({item["test_id"] for item in plan["steps"]}) == 20
    assert all("command" not in item and "run" not in item for item in plan["steps"])


def test_manifest_rejects_multiple_current_steps() -> None:
    plan = deepcopy(load_plan())
    plan["steps"][1]["status"] = "active"

    with pytest.raises(PlanValidationError, match="exactly one active or blocked"):
        validate_plan(plan)


def test_manifest_rejects_skipped_and_out_of_order_states() -> None:
    plan = deepcopy(load_plan())
    plan["active_step"] = "MB-03"
    plan["next_step"] = "MB-04"
    plan["steps"][0]["status"] = "planned"
    plan["steps"][1]["status"] = "planned"
    plan["steps"][2]["status"] = "active"

    with pytest.raises(PlanValidationError, match="before current step must be passed"):
        validate_plan(plan)


def test_manifest_rejects_unknown_test_identifiers_and_missing_spawn(tmp_path: Path) -> None:
    plan = deepcopy(load_plan())
    plan["steps"][0]["test_id"] = "shell: rm -rf"

    with pytest.raises(PlanValidationError, match="test id invalid"):
        validate_plan(plan)

    plan = deepcopy(load_plan())
    plan["quantum_spawn"] = "docs/quantum-spawn/missing.md"
    with pytest.raises(PlanValidationError, match="Quantum Spawn path does not exist"):
        validate_plan(plan)


def test_manifest_file_is_canonical_json_object() -> None:
    text = DEFAULT_PLAN_PATH.read_text(encoding="utf-8")
    payload = json.loads(text)

    assert isinstance(payload, dict)
    assert text.endswith("\n")
