#!/usr/bin/env python3
"""Validate one Build 026 machine receipt against repository contracts."""

from __future__ import annotations

import argparse
from decimal import Decimal
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "build-plans" / "build-026-continuity-and-model-repair.json"
EXPECTED_SCHEMA = "globalgrid2050.solar-dc.build-026-receipt.v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
UNIT_ID = re.compile(r"^B026-(\d{2})$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), f"{path} must contain one JSON object")
    return payload


def decimal(value: object) -> Decimal:
    return Decimal(str(value))


def validate_receipt(receipt: dict[str, Any], plan: dict[str, Any]) -> None:
    require(receipt.get("schema_version") == EXPECTED_SCHEMA, "wrong receipt schema_version")
    require(receipt.get("programme_id") == plan.get("programme_id"), "receipt programme_id differs from plan")

    unit_id = str(receipt.get("unit_id", ""))
    match = UNIT_ID.fullmatch(unit_id)
    require(match is not None, "invalid Build 026 unit_id")
    ordinal = int(receipt.get("ordinal", -1))
    require(ordinal == int(match.group(1)), "receipt ordinal differs from unit_id")

    units = {str(item["id"]): item for item in plan["units"]}
    require(unit_id in units, "receipt unit_id is absent from machine plan")
    planned = units[unit_id]
    require(receipt.get("title") == planned.get("title"), "receipt title differs from machine plan")
    require(ordinal == int(planned["ordinal"]), "receipt ordinal differs from machine plan")

    origin = receipt["origin"]
    require(SHA40.fullmatch(str(origin["head_sha"])) is not None, "invalid origin head_sha")
    build_pass = receipt["build_pass"]
    test_pass = receipt["test_pass"]
    require(build_pass.get("status") == "passed", "build_pass must be passed")
    require(test_pass.get("status") == "passed", "test_pass must be passed")
    require(decimal(build_pass["elapsed_seconds"]) <= Decimal(300), "build pass exceeded 300 seconds")

    for sha in build_pass["branch_commits"]:
        require(SHA40.fullmatch(str(sha)) is not None, "invalid branch commit SHA")
    require(SHA40.fullmatch(str(receipt["merged_build_commit"])) is not None, "invalid merged_build_commit")

    focused = test_pass["focused_gate"]
    breakdown = focused["case_breakdown"]
    calculated_cases = sum(
        int(breakdown[name])
        for name in (
            "generated_path_checks",
            "tracked_file_integrity_checks",
            "clean_tree_checks",
        )
    )
    require(calculated_cases == int(breakdown["total_collected_tests"]), "focused test breakdown does not sum")

    envelope = test_pass["full_envelope"]
    calculated_duration = sum(
        decimal(envelope[name]["elapsed_seconds"])
        for name in ("python", "v8", "v9", "v10_javascript", "clean_wheel")
    )
    require(calculated_duration == decimal(envelope["elapsed_seconds_sum"]), "suite durations do not sum")
    require(calculated_duration <= Decimal(300), "declared test envelope exceeded 300 seconds")
    require(int(envelope["python"]["passed"]) > 0 and int(envelope["python"]["failed"]) == 0, "Python suite is not passing")
    require(int(envelope["v9"]["passed"]) > 0 and int(envelope["v9"]["failed"]) == 0, "V9 suite is not passing")
    require(envelope["v8"]["passed"] is True, "V8 suite is not passing")
    require(envelope["v10_javascript"]["passed"] is True, "V10 JavaScript suite is not passing")
    require(envelope["clean_wheel"]["passed"] is True, "clean-wheel suite is not passing")

    ci = test_pass["ci"]
    require(int(ci["run_id"]) > 0, "invalid workflow run_id")
    require(int(ci["artifact_id"]) > 0, "invalid artifact_id")
    require(SHA40.fullmatch(str(ci["merge_test_sha"])) is not None, "invalid merge_test_sha")
    require(SHA256.fullmatch(str(ci["artifact_digest"])) is not None, "invalid artifact_digest")
    require(ci.get("result") == "passed", "CI result is not passed")

    review = test_pass["receipt_review"]
    require(review.get("status") == "verified", "receipt review is not verified")
    require(review.get("fresh_execution_performed") is False, "historical receipt review must not claim fresh execution")
    require(int(review.get("discrepancies_found", -1)) == 0, "receipt review records discrepancies")

    acceptance = receipt["acceptance"]
    require(acceptance.get("tracked_files_removed") is False, "receipt records tracked-file removal")
    require(int(acceptance.get("tracked_engineering_files_ignored", -1)) == 0, "receipt records ignored tracked engineering files")
    require(acceptance.get("prohibited_engineering_surfaces_changed") is False, "receipt records prohibited engineering changes")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args(argv)
    receipt_path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    validate_receipt(load_object(receipt_path), load_object(PLAN_PATH))
    print(f"Build 026 receipt validated: {receipt_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
