from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "microbuild-worker.yml"


def test_microbuild_worker_runs_only_manifest_and_allowlisted_runner() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "name: Microbuild Worker" in text
    assert "fetch-depth: 0" in text
    assert "python scripts/check_microbuild_plan.py --check" in text
    assert "python scripts/run_microbuild.py --execute" in text
    assert "actions/upload-artifact@v4" in text
    assert "microbuild-evidence-${{ github.sha }}" in text
    assert "permissions:\n  contents: read" in text
    assert "cancel-in-progress: false" in text


def test_worker_is_triggerable_by_marker_and_future_authority_files() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    for required_path in (
        '".microbuild/**"',
        '"microbuild-plan.json"',
        '"scripts/microbuild_*.py"',
        '"authority-bundles/**"',
        '"v10-development/tests/studio-authority.test.mjs"',
    ):
        assert required_path in text


def test_worker_never_interpolates_manifest_text_into_shell() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "steps[].command" not in text
    active_block = text.split("Run active allowlisted test", 1)[1].split(
        "Write canonical microbuild evidence", 1
    )[0]
    assert "active_test_id" not in active_block
    assert "run: ${{" not in text
    assert "python scripts/run_microbuild.py --execute" in text


def test_execution_envelope_uses_canonical_writer_and_github_state() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "python scripts/microbuild_evidence.py" in text
    assert '--tested-commit "$GITHUB_SHA"' in text
    assert '--workflow-run-id "$GITHUB_RUN_ID"' in text
    assert "--result pass" in text
    assert "--output .microbuild/evidence/latest.json" in text
