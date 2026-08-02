from __future__ import annotations

import json
from pathlib import Path

from scripts.check_microbuild_plan import load_plan, validate_plan
from scripts.run_microbuild import active_command, active_test_id


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_BLOCK_HASH = (
    "sha256:79f3d02a878e4fe6bd700d194c2b29e2500cd9511e23d469c34f3d8472f8a1f8"
)
TS005_CLOSURE = ROOT / "docs/trueself/20260801-ts-005-authoritative-slice-closure.md"


def test_hostile_amnesia_reload_recovers_ts005_handoff() -> None:
    programme = json.loads(
        (ROOT / "programme-state.json").read_text(encoding="utf-8")
    )
    plan = load_plan()
    summary = validate_plan(plan)
    handoff = plan["steps"][9]
    reference_command = plan["steps"][10]

    assert programme["active_gate"].startswith("TS-005")
    assert summary["programme_status"] == "completed"
    assert plan["active_step"] is None
    assert plan["next_step"] is None

    assert handoff["id"] == "MB-10"
    assert handoff["status"] == "passed"
    assert handoff["test_id"] == "ts005_handoff"
    assert handoff["evidence"]["result"] == "pass"
    assert handoff["evidence"]["test_id"] == "ts005_handoff"

    assert reference_command["title"] == "Reference-block command"
    assert reference_command["test_id"] == "reference_block_command"
    assert reference_command["status"] == "passed"

    block = programme["reference_inverter_block"]
    assert block["module_rated_power_wp"] == 660
    assert block["modules_per_string"] == 30
    assert block["strings"] == 24
    assert block["module_count"] == 720
    assert block["dc_nameplate_power_kwp"] == 475.2
    assert block["inverter_apparent_power_kva"] == 352
    assert block["dc_ac_nameplate_ratio"] == 1.35


def test_handoff_files_exist_and_bind_validated_receipt() -> None:
    programme = json.loads(
        (ROOT / "programme-state.json").read_text(encoding="utf-8")
    )
    spawn = ROOT / programme["current_quantum_spawn"]
    current_trueself = ROOT / programme["current_trueself"]

    assert spawn.is_file()
    assert current_trueself.is_file()
    assert TS005_CLOSURE.is_file()
    checkpoint_text = TS005_CLOSURE.read_text(encoding="utf-8")
    assert EXPECTED_BLOCK_HASH in checkpoint_text
    assert "Forty-seven equipment evidence items remain unresolved" in checkpoint_text
    assert "MB-10 — TS-005 hand-off proof" in checkpoint_text
    assert "TS-005 — First authoritative Studio slice" in checkpoint_text


def test_handoff_exposes_unresolved_authority_without_inference() -> None:
    programme = json.loads(
        (ROOT / "programme-state.json").read_text(encoding="utf-8")
    )
    limitations = "\n".join(programme["known_limitations"])

    for unresolved in (
        "47 unresolved",
        "Internal DC topology",
        "reverse-current blocking",
        "PCE backfeed",
    ):
        assert unresolved in limitations


def test_completed_programme_exposes_no_active_command() -> None:
    plan = load_plan()
    summary = validate_plan(plan)

    assert active_test_id() is None
    assert active_command() == ()
    assert plan["active_step"] == summary["active_step"] is None
    assert plan["steps"][9]["status"] == "passed"
    assert plan["steps"][9]["evidence"]["test_id"] == "ts005_handoff"
    assert plan["steps"][19]["status"] == "passed"
    assert plan["steps"][19]["evidence"]["test_id"] == (
        "end_to_end_authority_slice"
    )
