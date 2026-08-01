#!/usr/bin/env python3
"""Preview one evidence-bound microbuild advancement without writing files."""

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
from typing import Any

try:
    from scripts.check_microbuild_plan import (
        DEFAULT_PLAN_PATH,
        load_plan,
        validate_plan,
    )
    from scripts.microbuild_evidence import (
        canonical_json,
        microbuild_evidence_hash,
    )
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from check_microbuild_plan import DEFAULT_PLAN_PATH, load_plan, validate_plan
    from microbuild_evidence import canonical_json, microbuild_evidence_hash


class AdvancementError(ValueError):
    """The supplied evidence cannot advance the active step."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AdvancementError(message)


def load_evidence(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), "evidence must be one JSON object")
    return payload


def manifest_evidence_record(evidence: dict[str, Any]) -> dict[str, object]:
    require(set(evidence) == {"core", "evidence_hash", "runtime"}, "evidence fields changed")
    core = evidence["core"]
    runtime = evidence["runtime"]
    require(isinstance(core, dict), "evidence core must be an object")
    require(isinstance(runtime, dict), "evidence runtime must be an object")
    require(
        evidence["evidence_hash"] == microbuild_evidence_hash(core),
        "evidence hash mismatch",
    )
    workflow_run_id = runtime.get("workflow_run_id")
    artifact_id = runtime.get("artifact_id")
    require(
        isinstance(workflow_run_id, int) and workflow_run_id > 0,
        "workflow_run_id is required for advancement",
    )
    require(
        isinstance(artifact_id, int) and artifact_id > 0,
        "artifact_id is required for advancement",
    )
    return {
        "step_id": core["step_id"],
        "manifest_revision": core["manifest_revision"],
        "tested_commit": core["tested_commit"],
        "test_id": core["test_id"],
        "result": core["result"],
        "workflow_run_id": workflow_run_id,
        "artifact_id": artifact_id,
        "evidence_hash": evidence["evidence_hash"],
    }


def preview_advancement(
    plan: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    summary = validate_plan(plan)
    record = manifest_evidence_record(evidence)
    require(record["result"] == "pass", "only passing evidence may advance")
    require(record["step_id"] == summary["active_step"], "evidence step does not match active step")
    require(record["test_id"] == summary["active_test_id"], "evidence test does not match active test")
    require(
        record["manifest_revision"] == summary["manifest_revision"],
        "evidence manifest revision does not match active revision",
    )

    result = deepcopy(plan)
    current_index = next(
        index
        for index, item in enumerate(result["steps"])
        if item["status"] in {"active", "blocked"}
    )
    require(current_index < len(result["steps"]) - 1, "final step has no next step")
    next_index = current_index + 1

    result["steps"][current_index]["status"] = "passed"
    result["steps"][current_index]["evidence"] = record
    result["steps"][next_index]["status"] = "active"
    result["manifest_revision"] += 1
    result["active_step"] = result["steps"][next_index]["id"]
    result["next_step"] = (
        result["steps"][next_index + 1]["id"]
        if next_index + 1 < len(result["steps"])
        else None
    )
    validate_plan(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN_PATH)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()

    preview = preview_advancement(load_plan(args.plan), load_evidence(args.evidence))
    print(canonical_json(preview))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
