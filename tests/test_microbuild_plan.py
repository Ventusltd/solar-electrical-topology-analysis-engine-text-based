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


def _active_before_final() -> dict[str, object]:
    plan = deepcopy(load_plan())
    final = plan["steps"][-1]
    final["status"] = "active"
    final["evidence"] = None
    plan["manifest_revision"] = 20
    plan["active_step"] = "MB-20"
    plan["next_step"] = None
    return plan


def test_manifest_contract_has_twenty_ordered_completed_steps() -> None:
    plan = load_plan()
    summary = validate_plan(plan)

    assert summary["pass"] is True
    assert summary["programme_status"] == "completed"
    assert summary["programme_id"] == "twenty-step-autopilot-20260801"
    assert summary["manifest_revision"] == plan["manifest_revision"]
    assert summary["active_step"] is None
    assert summary["active_status"] is None
    assert summary["active_test_id"] is None
    assert summary["next_step"] is None
    assert summary["passed_steps"] == 20
    assert summary["planned_steps"] == 0
    assert summary["total_steps"] == 20
    assert plan["active_step"] is None
    assert plan["next_step"] is None
    assert [item["id"] for item in plan["steps"]] == [
        f"MB-{ordinal:02d}" for ordinal in range(1, 21)
    ]
    assert [item["phase"] for item in plan["steps"][:10]] == ["A"] * 10
    assert [item["phase"] for item in plan["steps"][10:]] == ["B"] * 10
    assert len({item["test_id"] for item in plan["steps"]}) == 20
    assert all(item["status"] == "passed" for item in plan["steps"])
    assert all(item["evidence"]["result"] == "pass" for item in plan["steps"])
    assert all("command" not in item and "run" not in item for item in plan["steps"])


def test_manifest_still_accepts_one_active_final_gate() -> None:
    summary = validate_plan(_active_before_final())

    assert summary["programme_status"] == "active"
    assert summary["active_step"] == "MB-20"
    assert summary["active_test_id"] == "end_to_end_authority_slice"
    assert summary["next_step"] is None
    assert summary["passed_steps"] == 19
    assert summary["planned_steps"] == 0


def test_manifest_rejects_multiple_current_steps() -> None:
    plan = _active_before_final()
    previous = plan["steps"][-2]
    previous["status"] = "active"
    previous["evidence"] = None

    with pytest.raises(PlanValidationError, match="at most one active or blocked"):
        validate_plan(plan)


def test_manifest_rejects_incomplete_plan_without_current_step() -> None:
    plan = deepcopy(load_plan())
    plan["steps"][-1]["status"] = "planned"
    plan["steps"][-1]["evidence"] = None

    with pytest.raises(PlanValidationError, match="must be fully passed"):
        validate_plan(plan)


def test_manifest_rejects_skipped_and_out_of_order_states() -> None:
    plan = _active_before_final()
    plan["steps"][-2]["status"] = "planned"
    plan["steps"][-2]["evidence"] = None

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
