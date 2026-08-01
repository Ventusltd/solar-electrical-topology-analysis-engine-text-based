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


def test_manifest_contract_has_twenty_ordered_steps_and_one_current_gate() -> None:
    plan = load_plan()
    summary = validate_plan(plan)
    current = next(
        item for item in plan["steps"] if item["status"] in {"active", "blocked"}
    )
    current_index = current["ordinal"] - 1

    assert summary["pass"] is True
    assert summary["programme_id"] == "twenty-step-autopilot-20260801"
    assert summary["manifest_revision"] == plan["manifest_revision"]
    assert summary["active_step"] == plan["active_step"] == current["id"]
    assert summary["active_status"] == current["status"]
    assert summary["active_test_id"] == current["test_id"]
    assert summary["next_step"] == plan["next_step"]
    assert summary["passed_steps"] == current_index
    assert summary["planned_steps"] == 19 - current_index
    assert summary["total_steps"] == 20
    assert [item["id"] for item in plan["steps"]] == [
        f"MB-{ordinal:02d}" for ordinal in range(1, 21)
    ]
    assert [item["phase"] for item in plan["steps"][:10]] == ["A"] * 10
    assert [item["phase"] for item in plan["steps"][10:]] == ["B"] * 10
    assert len({item["test_id"] for item in plan["steps"]}) == 20
    assert all("command" not in item and "run" not in item for item in plan["steps"])


def test_manifest_rejects_multiple_current_steps() -> None:
    plan = deepcopy(load_plan())
    current_index = next(
        index
        for index, item in enumerate(plan["steps"])
        if item["status"] in {"active", "blocked"}
    )
    later_index = min(current_index + 1, 19)
    if later_index == current_index:
        later_index = current_index - 1
    plan["steps"][later_index]["status"] = "active"
    plan["steps"][later_index]["evidence"] = None

    with pytest.raises(PlanValidationError, match="exactly one active or blocked"):
        validate_plan(plan)


def test_manifest_rejects_skipped_and_out_of_order_states() -> None:
    plan = deepcopy(load_plan())
    current_index = next(
        index
        for index, item in enumerate(plan["steps"])
        if item["status"] in {"active", "blocked"}
    )
    assert current_index < 19
    next_index = current_index + 1
    plan["steps"][current_index]["status"] = "planned"
    plan["steps"][next_index]["status"] = "active"
    plan["active_step"] = plan["steps"][next_index]["id"]
    plan["next_step"] = (
        plan["steps"][next_index + 1]["id"] if next_index < 19 else None
    )

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
