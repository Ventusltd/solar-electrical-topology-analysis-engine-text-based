from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.advance_microbuild import AdvancementError, preview_advancement
from scripts.check_microbuild_plan import DEFAULT_PLAN_PATH, load_plan, validate_plan
from scripts.microbuild_evidence import microbuild_evidence_payload


def _active_plan(step_index: int) -> dict[str, object]:
    plan = deepcopy(load_plan())
    assert step_index in {18, 19}
    for index, step in enumerate(plan["steps"]):
        if index < step_index:
            step["status"] = "passed"
        elif index == step_index:
            step["status"] = "active"
            step["evidence"] = None
        else:
            step["status"] = "planned"
            step["evidence"] = None
    plan["manifest_revision"] = step_index + 1
    plan["active_step"] = plan["steps"][step_index]["id"]
    plan["next_step"] = (
        plan["steps"][step_index + 1]["id"] if step_index < 19 else None
    )
    validate_plan(plan)
    return plan


def _current_evidence(
    plan: dict[str, object],
    **overrides: object,
) -> dict[str, object]:
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
    source = _active_plan(18)
    original = deepcopy(source)
    preview = preview_advancement(source, _current_evidence(source))

    assert source == original
    assert preview["manifest_revision"] == 20
    assert preview["active_step"] == "MB-20"
    assert preview["next_step"] is None
    assert preview["steps"][18]["status"] == "passed"
    assert preview["steps"][18]["evidence"]["step_id"] == "MB-19"
    assert preview["steps"][19]["status"] == "active"
    assert validate_plan(preview)["programme_status"] == "active"


def test_final_advancement_closes_the_programme() -> None:
    source = _active_plan(19)
    preview = preview_advancement(source, _current_evidence(source))
    summary = validate_plan(preview)

    assert preview["manifest_revision"] == 21
    assert preview["active_step"] is None
    assert preview["next_step"] is None
    assert preview["steps"][19]["status"] == "passed"
    assert preview["steps"][19]["evidence"]["step_id"] == "MB-20"
    assert summary["programme_status"] == "completed"
    assert summary["passed_steps"] == 20


def test_preview_never_writes_the_source_manifest() -> None:
    before = DEFAULT_PLAN_PATH.read_bytes()
    source = _active_plan(19)
    preview_advancement(source, _current_evidence(source))
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
    source = _active_plan(19)
    original = deepcopy(source)
    before = DEFAULT_PLAN_PATH.read_bytes()

    with pytest.raises(AdvancementError, match=message):
        preview_advancement(source, _current_evidence(source, **overrides))

    assert source == original
    assert DEFAULT_PLAN_PATH.read_bytes() == before


def test_refusal_rejects_tampered_evidence_hash() -> None:
    source = _active_plan(19)
    original = deepcopy(source)
    evidence = _current_evidence(source)
    evidence["evidence_hash"] = "sha256:" + "0" * 64

    with pytest.raises(AdvancementError, match="evidence hash mismatch"):
        preview_advancement(source, evidence)

    assert source == original


def test_refusal_rejects_skipped_step_even_with_plausible_evidence() -> None:
    source = _active_plan(18)
    skipped = source["steps"][19]
    evidence = _current_evidence(
        source,
        step_id=skipped["id"],
        test_id=skipped["test_id"],
    )

    with pytest.raises(AdvancementError, match="evidence step"):
        preview_advancement(source, evidence)


def test_completed_programme_cannot_advance_again() -> None:
    completed = load_plan()
    active = _active_plan(19)

    with pytest.raises(AdvancementError, match="completed programme cannot advance"):
        preview_advancement(completed, _current_evidence(active))
