#!/usr/bin/env python3
"""Validate the ordered twenty-step microbuild programme."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN_PATH = ROOT / "microbuild-plan.json"
SCHEMA_VERSION = "globalgrid2050.solar-dc.microbuild-plan.v1"
PROGRAMME_ID = "twenty-step-autopilot-20260801"
ALLOWED_STATES = {"planned", "active", "passed", "blocked"}
CURRENT_STATES = {"active", "blocked"}
STEP_ID = re.compile(r"^MB-(0[1-9]|1[0-9]|20)$")
TEST_ID = re.compile(r"^[a-z][a-z0-9_]*$")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
EVIDENCE_FIELDS = {
    "step_id",
    "manifest_revision",
    "tested_commit",
    "test_id",
    "result",
    "workflow_run_id",
    "artifact_id",
    "evidence_hash",
}


class PlanValidationError(ValueError):
    """The machine-readable programme violates its sequencing contract."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PlanValidationError(message)


def load_plan(path: Path = DEFAULT_PLAN_PATH) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), "microbuild plan must contain one JSON object")
    return payload


def validate_evidence(
    evidence: object,
    *,
    step_id: str,
    test_id: str,
    manifest_revision: int,
) -> None:
    require(isinstance(evidence, dict), f"{step_id} passed evidence must be an object")
    assert isinstance(evidence, dict)
    require(set(evidence) == EVIDENCE_FIELDS, f"{step_id} evidence fields changed")
    require(evidence["step_id"] == step_id, f"{step_id} evidence step mismatch")
    require(evidence["test_id"] == test_id, f"{step_id} evidence test mismatch")
    require(evidence["result"] == "pass", f"{step_id} evidence must record pass")
    require(
        isinstance(evidence["manifest_revision"], int)
        and 1 <= evidence["manifest_revision"] <= manifest_revision,
        f"{step_id} evidence manifest revision is invalid",
    )
    require(
        isinstance(evidence["tested_commit"], str)
        and SHA40.fullmatch(evidence["tested_commit"]) is not None,
        f"{step_id} tested commit is invalid",
    )
    for field in ("workflow_run_id", "artifact_id"):
        require(
            isinstance(evidence[field], int) and evidence[field] > 0,
            f"{step_id} evidence {field} must be positive",
        )
    require(
        isinstance(evidence["evidence_hash"], str)
        and SHA256.fullmatch(evidence["evidence_hash"]) is not None,
        f"{step_id} evidence hash is invalid",
    )


def validate_plan(plan: dict[str, Any], *, root: Path = ROOT) -> dict[str, object]:
    required_top = {
        "schema_version",
        "programme_id",
        "manifest_revision",
        "quantum_spawn",
        "restore_point",
        "active_step",
        "next_step",
        "steps",
    }
    require(set(plan) == required_top, "microbuild plan top-level fields changed")
    require(plan["schema_version"] == SCHEMA_VERSION, "wrong microbuild schema version")
    require(plan["programme_id"] == PROGRAMME_ID, "wrong microbuild programme id")
    require(
        isinstance(plan["manifest_revision"], int) and plan["manifest_revision"] > 0,
        "manifest revision must be a positive integer",
    )
    require(
        isinstance(plan["quantum_spawn"], str)
        and (root / plan["quantum_spawn"]).is_file(),
        "Quantum Spawn path does not exist",
    )
    require(
        isinstance(plan["restore_point"], str) and bool(plan["restore_point"].strip()),
        "restore point must be present",
    )

    steps = plan["steps"]
    require(isinstance(steps, list), "steps must be a list")
    require(len(steps) == 20, "microbuild plan must contain exactly twenty steps")

    expected_ids = [f"MB-{ordinal:02d}" for ordinal in range(1, 21)]
    current_indexes: list[int] = []
    test_ids: list[str] = []
    passed_count = 0

    for index, raw_step in enumerate(steps):
        require(isinstance(raw_step, dict), f"step {index + 1} must be an object")
        step = raw_step
        required_step = {
            "id",
            "ordinal",
            "phase",
            "title",
            "status",
            "test_id",
            "evidence",
        }
        require(set(step) == required_step, f"{expected_ids[index]} fields changed")
        require(step["id"] == expected_ids[index], f"step id order failed at {index + 1}")
        require(STEP_ID.fullmatch(step["id"]) is not None, f"invalid step id {step['id']}")
        require(step["ordinal"] == index + 1, f"{step['id']} ordinal mismatch")
        require(step["phase"] == ("A" if index < 10 else "B"), f"{step['id']} phase mismatch")
        require(isinstance(step["title"], str) and bool(step["title"].strip()), f"{step['id']} title missing")
        require(step["status"] in ALLOWED_STATES, f"{step['id']} status invalid")
        require(
            isinstance(step["test_id"], str)
            and TEST_ID.fullmatch(step["test_id"]) is not None,
            f"{step['id']} test id invalid",
        )
        test_ids.append(step["test_id"])

        if step["status"] in CURRENT_STATES:
            current_indexes.append(index)
        if step["status"] == "passed":
            passed_count += 1
            validate_evidence(
                step["evidence"],
                step_id=step["id"],
                test_id=step["test_id"],
                manifest_revision=plan["manifest_revision"],
            )
        else:
            require(step["evidence"] is None, f"{step['id']} may not have evidence before pass")

    require(len(set(test_ids)) == 20, "every step must have one unique test id")
    require(len(current_indexes) <= 1, "at most one active or blocked step is permitted")

    if not current_indexes:
        require(passed_count == 20, "a programme without an active step must be fully passed")
        require(plan["active_step"] is None, "completed programme active_step must be null")
        require(plan["next_step"] is None, "completed programme next_step must be null")
        return {
            "pass": True,
            "programme_status": "completed",
            "programme_id": plan["programme_id"],
            "manifest_revision": plan["manifest_revision"],
            "active_step": None,
            "active_status": None,
            "active_test_id": None,
            "next_step": None,
            "passed_steps": 20,
            "planned_steps": 0,
            "total_steps": 20,
        }

    current_index = current_indexes[0]
    current = steps[current_index]
    require(plan["active_step"] == current["id"], "active_step pointer mismatch")

    for index, step in enumerate(steps):
        if index < current_index:
            require(step["status"] == "passed", f"{step['id']} before current step must be passed")
        elif index > current_index:
            require(step["status"] == "planned", f"{step['id']} after current step must be planned")

    expected_next = expected_ids[current_index + 1] if current_index < 19 else None
    require(plan["next_step"] == expected_next, "next_step pointer mismatch")
    require(passed_count == current_index, "passed-step count does not match current position")

    return {
        "pass": True,
        "programme_status": "active" if current["status"] == "active" else "blocked",
        "programme_id": plan["programme_id"],
        "manifest_revision": plan["manifest_revision"],
        "active_step": plan["active_step"],
        "active_status": current["status"],
        "active_test_id": current["test_id"],
        "next_step": plan["next_step"],
        "passed_steps": passed_count,
        "planned_steps": 19 - current_index,
        "total_steps": 20,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, default=DEFAULT_PLAN_PATH)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        summary = validate_plan(load_plan(args.path))
    except (OSError, json.JSONDecodeError, PlanValidationError) as exc:
        raise SystemExit(f"microbuild plan invalid: {exc}") from exc
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
