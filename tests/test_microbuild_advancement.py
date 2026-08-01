from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.advance_microbuild import AdvancementError, preview_advancement
from scripts.check_microbuild_plan import DEFAULT_PLAN_PATH, load_plan, validate_plan
from scripts.microbuild_evidence import microbuild_evidence_payload


def _current_evidence(**overrides: object) -> dict[str, object]:
    plan = load_plan()
    current = next(
        item for item in plan["steps"] if item["status"] in {"active", "blocked"}
    )
    values: dict[str, object] = {
        "step_id": current["id"],
        "manifest_revision": plan["manifest_revision"],
        "tested_commit": "d" * 40,
        "test_id": current["test_id"],
        "result": "pass",
        "workflow_run_id": 6000 + current["ordinal"],
        "artifact_id": 7000 + current["ordinal"],
    }
    values.update(overrides)
    return microbuild_evidence_payload(**values)


def test_preview_advancement_changes_only_current_next_and_evidence() -> None:
    source = load_plan()
    original = deepcopy(source)
    current_index = next(
        index
        for index, item in enumerate(source["steps"])
        if item["status"] in {"active", "blocked"}
    )
    assert current_index < 19

    preview = preview_advancement(source, _current_evidence())

    assert source == original
    assert preview["manifest_revision"] == original["manifest_revision"] + 1
    assert preview["active_step"] == original["steps"][current_index + 1]["id"]
    assert preview["steps"][current_index]["status"] == "passed"
    assert preview["steps"][current_index]["evidence"]["step_id"] == (
        original["active_step"]
    )
    assert preview["steps"][current_index + 1]["status"] == "active"
    assert preview["steps"][:current_index] == original["steps"][:current_index]
    assert preview["steps"][current_index + 2 :] == original["steps"][current_index + 2 :]
    assert validate_plan(preview)["active_step"] == preview["active_step"]


def test_preview_never_writes_the_source_manifest() -> None:
    before = DEFAULT_PLAN_PATH.read_bytes()
    preview_advancement(load_plan(), _current_evidence())
    after = DEFAULT_PLAN_PATH.read_bytes()

    assert after == before


@pytest.mark.parametrize(
    ("overrides", "message"),
    (
        ({"result": "fail"}, "only passing evidence"),
        ({"manifest_revision": 1}, "manifest revision"),
        ({"step_id": "MB-06"}, "evidence step"),
        ({"test_id": "advancement_preview"}, "evidence test"),
        ({"workflow_run_id": None}, "workflow_run_id is required"),
        ({"artifact_id": None}, "artifact_id is required"),
    ),
)
def test_refusal_rejects_failed_stale_mismatched_or_incomplete_evidence(
    overrides: dict[str, object],
    message: str,
) -> None:
    source = load_plan()
    original = deepcopy(source)
    before = DEFAULT_PLAN_PATH.read_bytes()

    with pytest.raises(AdvancementError, match=message):
        preview_advancement(source, _current_evidence(**overrides))

    assert source == original
    assert DEFAULT_PLAN_PATH.read_bytes() == before


def test_refusal_rejects_tampered_evidence_hash() -> None:
    source = load_plan()
    original = deepcopy(source)
    evidence = _current_evidence()
    evidence["evidence_hash"] = "sha256:" + "0" * 64

    with pytest.raises(AdvancementError, match="evidence hash mismatch"):
        preview_advancement(source, evidence)

    assert source == original


def test_refusal_rejects_skipped_step_even_with_plausible_evidence() -> None:
    source = load_plan()
    current_index = next(
        index
        for index, item in enumerate(source["steps"])
        if item["status"] in {"active", "blocked"}
    )
    skipped = source["steps"][current_index + 1]
    evidence = _current_evidence(
        step_id=skipped["id"],
        test_id=skipped["test_id"],
    )

    with pytest.raises(AdvancementError, match="evidence step"):
        preview_advancement(source, evidence)
