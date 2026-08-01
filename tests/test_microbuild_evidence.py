from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.check_microbuild_plan import load_plan, validate_plan
from scripts.microbuild_evidence import (
    EvidenceValidationError,
    canonical_json,
    evidence_from_active_plan,
    microbuild_evidence_hash,
    microbuild_evidence_payload,
)


ROOT = Path(__file__).resolve().parents[1]


def _base(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "step_id": "MB-05",
        "manifest_revision": 5,
        "tested_commit": "a" * 40,
        "test_id": "microbuild_evidence",
        "result": "pass",
        "workflow_run_id": 123,
        "artifact_id": 456,
    }
    values.update(overrides)
    return values


def test_evidence_hash_is_deterministic_and_excludes_runtime_metadata() -> None:
    first = microbuild_evidence_payload(**_base())
    second = microbuild_evidence_payload(
        **_base(workflow_run_id=999, artifact_id=1000)
    )

    assert first["core"] == second["core"]
    assert first["evidence_hash"] == second["evidence_hash"]
    assert first["runtime"] != second["runtime"]
    assert canonical_json(first) == canonical_json(
        microbuild_evidence_payload(**_base())
    )
    assert first["evidence_hash"] == microbuild_evidence_hash(first["core"])


def test_engineering_core_changes_evidence_hash() -> None:
    first = microbuild_evidence_payload(**_base())
    changed = microbuild_evidence_payload(**_base(tested_commit="b" * 40))

    assert first["evidence_hash"] != changed["evidence_hash"]


def test_active_plan_evidence_uses_current_step_and_test() -> None:
    summary = validate_plan(load_plan())
    payload = evidence_from_active_plan(
        tested_commit="c" * 40,
        result="pass",
        workflow_run_id=12,
    )

    assert payload["core"]["step_id"] == summary["active_step"]
    assert payload["core"]["manifest_revision"] == summary["manifest_revision"]
    assert payload["core"]["test_id"] == summary["active_test_id"]
    assert payload["runtime"]["workflow_run_id"] == 12
    assert payload["runtime"]["artifact_id"] is None


def test_invalid_core_and_runtime_values_are_rejected() -> None:
    with pytest.raises(EvidenceValidationError, match="invalid tested_commit"):
        microbuild_evidence_payload(**_base(tested_commit="not-a-sha"))
    with pytest.raises(EvidenceValidationError, match="result must be pass or fail"):
        microbuild_evidence_payload(**_base(result="maybe"))
    with pytest.raises(EvidenceValidationError, match="artifact_id must be positive"):
        microbuild_evidence_payload(**_base(artifact_id=0))


def test_worker_uses_canonical_evidence_writer() -> None:
    workflow = (ROOT / ".github/workflows/microbuild-worker.yml").read_text(
        encoding="utf-8"
    )

    assert "python scripts/microbuild_evidence.py" in workflow
    assert '--tested-commit "$GITHUB_SHA"' in workflow
    assert '--workflow-run-id "$GITHUB_RUN_ID"' in workflow
    assert "Path(\".microbuild/evidence/latest.json\")" not in workflow
