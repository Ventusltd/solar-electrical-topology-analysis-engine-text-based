from __future__ import annotations

import json
from pathlib import Path

from scripts.check_microbuild_plan import load_plan, validate_plan
from scripts.run_microbuild import active_command, active_test_id


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_BLOCK_HASH = (
    "sha256:79f3d02a878e4fe6bd700d194c2b29e2500cd9511e23d469c34f3d8472f8a1f8"
)


def test_hostile_amnesia_reload_recovers_ts005_handoff() -> None:
    programme = json.loads(
        (ROOT / "programme-state.json").read_text(encoding="utf-8")
    )
    plan = load_plan()
    summary = validate_plan(plan)

    assert programme["active_gate"] == "TS-005 — First authoritative Studio slice"
    assert programme["next_single_goal"] == "MB-10 — TS-005 hand-off proof"
    assert summary["active_step"] == "MB-10"
    assert summary["active_test_id"] == "ts005_handoff"
    assert summary["next_step"] == "MB-11"
    assert plan["steps"][10]["title"] == "Reference-block command"
    assert plan["steps"][10]["test_id"] == "reference_block_command"

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
    checkpoint = ROOT / programme["current_trueself"]

    assert spawn.is_file()
    assert checkpoint.is_file()
    checkpoint_text = checkpoint.read_text(encoding="utf-8")
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
        "authoritative Studio mode is not yet connected",
    ):
        assert unresolved in limitations


def test_next_command_is_repository_allowlisted_but_not_executed_early() -> None:
    assert active_test_id() == "ts005_handoff"
    assert active_command()[-1] == "tests/test_ts005_handoff.py"

    plan = load_plan()
    next_test_id = plan["steps"][10]["test_id"]
    assert next_test_id == "reference_block_command"
    assert plan["steps"][10]["status"] == "planned"
