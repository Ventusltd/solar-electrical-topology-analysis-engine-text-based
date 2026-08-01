from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import solar_topology as topology

from scripts.reference_block_command import (
    REFERENCE_BLOCK_COMMAND_VERSION,
    reference_block_json,
)


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reference_block_command.py"


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_reference_block_function_equals_package_authority_exactly() -> None:
    receipt = topology.build_reference_inverter_block()

    assert reference_block_json() == topology.inverter_block_json(receipt)
    assert json.loads(reference_block_json()) == topology.inverter_block_payload(receipt)


def test_reference_block_command_emits_one_canonical_json_line() -> None:
    completed = run_command()

    expected = topology.inverter_block_json(
        topology.build_reference_inverter_block()
    ) + "\n"
    assert completed.returncode == 0
    assert completed.stdout == expected
    assert completed.stderr == ""


def test_reference_block_command_exposes_exact_product_boundary() -> None:
    payload = json.loads(reference_block_json())
    boundary = payload["product_boundary"]

    assert boundary["module_rated_power_wp"] == 660.0
    assert boundary["modules_per_string"] == 30
    assert boundary["string_count"] == 24
    assert boundary["module_count"] == 720
    assert boundary["dc_nameplate_power_kwp"] == 475.2
    assert boundary["inverter_apparent_power_kva"] == 352.0
    assert boundary["dc_ac_nameplate_ratio"] == 1.35
    assert payload["receipt_hash"].startswith("sha256:")


def test_command_contract_declares_stable_version() -> None:
    completed = run_command("--version")

    assert completed.returncode == 0
    assert completed.stdout == REFERENCE_BLOCK_COMMAND_VERSION + "\n"
    assert completed.stderr == ""


def test_command_contract_supports_deterministic_strategy_selection() -> None:
    first = run_command("--strategy", "sequential")
    second = run_command("--strategy", "sequential")
    leapfrog = run_command("--strategy", "leapfrog")

    assert first.returncode == second.returncode == leapfrog.returncode == 0
    assert first.stdout == second.stdout
    assert first.stderr == second.stderr == leapfrog.stderr == ""
    sequential_payload = json.loads(first.stdout)
    leapfrog_payload = json.loads(leapfrog.stdout)
    assert sequential_payload["product_boundary"] == leapfrog_payload["product_boundary"]
    assert sequential_payload["receipt_hash"] != leapfrog_payload["receipt_hash"]


def test_command_contract_fails_without_authoritative_stdout() -> None:
    completed = run_command("--strategy", "invented")

    assert completed.returncode != 0
    assert completed.stdout == ""
    assert "invalid choice" in completed.stderr
    assert '"receipt_hash"' not in completed.stderr
