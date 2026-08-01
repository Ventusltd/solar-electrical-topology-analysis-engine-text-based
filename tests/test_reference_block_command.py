from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import solar_topology as topology

from scripts.reference_block_command import reference_block_json


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reference_block_command.py"


def test_reference_block_function_equals_package_authority_exactly() -> None:
    receipt = topology.build_reference_inverter_block()

    assert reference_block_json() == topology.inverter_block_json(receipt)
    assert json.loads(reference_block_json()) == topology.inverter_block_payload(receipt)


def test_reference_block_command_emits_one_canonical_json_line() -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    expected = topology.inverter_block_json(
        topology.build_reference_inverter_block()
    ) + "\n"
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
