from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_build026_receipt.py"
RECEIPT = ROOT / "evidence" / "build-026" / "B026-07.json"
PLAN = ROOT / "build-plans" / "build-026-continuity-and-model-repair.json"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_build026_receipt", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_b026_07_receipt_matches_repository_contracts() -> None:
    validator = load_validator()
    validator.validate_receipt(load_json(RECEIPT), load_json(PLAN))


def test_receipt_rejects_inconsistent_focused_test_count() -> None:
    validator = load_validator()
    receipt = copy.deepcopy(load_json(RECEIPT))
    receipt["test_pass"]["focused_gate"]["case_breakdown"]["total_collected_tests"] = 14
    with pytest.raises(ValueError, match="focused test breakdown does not sum"):
        validator.validate_receipt(receipt, load_json(PLAN))


def test_receipt_rejects_inconsistent_suite_duration_total() -> None:
    validator = load_validator()
    receipt = copy.deepcopy(load_json(RECEIPT))
    receipt["test_pass"]["full_envelope"]["elapsed_seconds_sum"] = 100.599
    with pytest.raises(ValueError, match="suite durations do not sum"):
        validator.validate_receipt(receipt, load_json(PLAN))


def test_receipt_rejects_false_fresh_execution_claim() -> None:
    validator = load_validator()
    receipt = copy.deepcopy(load_json(RECEIPT))
    receipt["test_pass"]["receipt_review"]["fresh_execution_performed"] = True
    with pytest.raises(ValueError, match="must not claim fresh execution"):
        validator.validate_receipt(receipt, load_json(PLAN))
