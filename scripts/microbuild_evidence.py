#!/usr/bin/env python3
"""Create deterministic microbuild evidence with separate runtime metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any

try:
    from scripts.check_microbuild_plan import DEFAULT_PLAN_PATH, load_plan, validate_plan
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from check_microbuild_plan import DEFAULT_PLAN_PATH, load_plan, validate_plan


MICROBUILD_EVIDENCE_SCHEMA_VERSION = (
    "globalgrid2050.solar-dc.microbuild-evidence.v1"
)
STEP_ID = re.compile(r"^MB-(0[1-9]|1[0-9]|20)$")
TEST_ID = re.compile(r"^[a-z][a-z0-9_]*$")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
RESULTS = {"pass", "fail"}


class EvidenceValidationError(ValueError):
    """Microbuild evidence is incomplete or malformed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise EvidenceValidationError(message)


def canonical_json(payload: object) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def evidence_core_payload(
    *,
    step_id: str,
    manifest_revision: int,
    tested_commit: str,
    test_id: str,
    result: str,
) -> dict[str, object]:
    require(STEP_ID.fullmatch(step_id) is not None, "invalid step_id")
    require(
        isinstance(manifest_revision, int) and manifest_revision > 0,
        "manifest_revision must be positive",
    )
    require(SHA40.fullmatch(tested_commit) is not None, "invalid tested_commit")
    require(TEST_ID.fullmatch(test_id) is not None, "invalid test_id")
    require(result in RESULTS, "result must be pass or fail")
    return {
        "schema_version": MICROBUILD_EVIDENCE_SCHEMA_VERSION,
        "step_id": step_id,
        "manifest_revision": manifest_revision,
        "tested_commit": tested_commit,
        "test_id": test_id,
        "result": result,
    }


def microbuild_evidence_hash(core: dict[str, object]) -> str:
    expected = {
        "schema_version",
        "step_id",
        "manifest_revision",
        "tested_commit",
        "test_id",
        "result",
    }
    require(set(core) == expected, "evidence core fields changed")
    digest = hashlib.sha256(canonical_json(core).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def _runtime_id(value: int | None, name: str) -> int | None:
    if value is None:
        return None
    require(isinstance(value, int) and value > 0, f"{name} must be positive")
    return value


def microbuild_evidence_payload(
    *,
    step_id: str,
    manifest_revision: int,
    tested_commit: str,
    test_id: str,
    result: str,
    workflow_run_id: int | None = None,
    artifact_id: int | None = None,
) -> dict[str, object]:
    core = evidence_core_payload(
        step_id=step_id,
        manifest_revision=manifest_revision,
        tested_commit=tested_commit,
        test_id=test_id,
        result=result,
    )
    return {
        "core": core,
        "evidence_hash": microbuild_evidence_hash(core),
        "runtime": {
            "workflow_run_id": _runtime_id(workflow_run_id, "workflow_run_id"),
            "artifact_id": _runtime_id(artifact_id, "artifact_id"),
        },
    }


def microbuild_evidence_json(**kwargs: Any) -> str:
    return canonical_json(microbuild_evidence_payload(**kwargs))


def evidence_from_active_plan(
    *,
    tested_commit: str,
    result: str,
    workflow_run_id: int | None = None,
    artifact_id: int | None = None,
    plan_path: Path = DEFAULT_PLAN_PATH,
) -> dict[str, object]:
    summary = validate_plan(load_plan(plan_path))
    require(
        summary["programme_status"] != "completed",
        "completed programme has no active step",
    )
    step_id = summary["active_step"]
    test_id = summary["active_test_id"]
    require(isinstance(step_id, str), "active step identifier must be text")
    require(isinstance(test_id, str), "active test identifier must be text")
    return microbuild_evidence_payload(
        step_id=step_id,
        manifest_revision=int(summary["manifest_revision"]),
        tested_commit=tested_commit,
        test_id=test_id,
        result=result,
        workflow_run_id=workflow_run_id,
        artifact_id=artifact_id,
    )


def write_evidence(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json(payload) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN_PATH)
    parser.add_argument("--tested-commit", required=True)
    parser.add_argument("--result", choices=sorted(RESULTS), required=True)
    parser.add_argument("--workflow-run-id", type=int)
    parser.add_argument("--artifact-id", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = evidence_from_active_plan(
        tested_commit=args.tested_commit,
        result=args.result,
        workflow_run_id=args.workflow_run_id,
        artifact_id=args.artifact_id,
        plan_path=args.plan,
    )
    if args.output is not None:
        write_evidence(args.output, payload)
    print(canonical_json(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
