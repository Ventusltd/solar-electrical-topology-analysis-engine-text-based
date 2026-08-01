from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from scripts.advance_microbuild import preview_advancement
from scripts.check_microbuild_plan import DEFAULT_PLAN_PATH, load_plan, validate_plan
from scripts.microbuild_evidence import microbuild_evidence_payload


def _passing_evidence() -> dict[str, object]:
    return microbuild_evidence_payload(
        step_id="MB-06",
        manifest_revision=6,
        tested_commit="d" * 40,
        test_id="advancement_preview",
        result="pass",
        workflow_run_id=6006,
        artifact_id=7006,
    )


def test_preview_advancement_changes_only_current_next_and_evidence() -> None:
    source = load_plan()
    original = deepcopy(source)
    preview = preview_advancement(source, _passing_evidence())

    assert source == original
    assert preview["manifest_revision"] == 7
    assert preview["active_step"] == "MB-07"
    assert preview["next_step"] == "MB-08"
    assert preview["steps"][5]["status"] == "passed"
    assert preview["steps"][5]["evidence"]["step_id"] == "MB-06"
    assert preview["steps"][6]["status"] == "active"
    assert preview["steps"][7]["status"] == "planned"
    assert preview["steps"][:5] == original["steps"][:5]
    assert preview["steps"][7:] == original["steps"][7:]
    assert validate_plan(preview)["active_step"] == "MB-07"


def test_preview_never_writes_the_source_manifest() -> None:
    before = DEFAULT_PLAN_PATH.read_bytes()
    preview_advancement(load_plan(), _passing_evidence())
    after = DEFAULT_PLAN_PATH.read_bytes()

    assert after == before
