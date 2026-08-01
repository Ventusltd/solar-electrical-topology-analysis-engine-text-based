#!/usr/bin/env python3
"""Select and optionally execute one repository-controlled microbuild test."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Sequence

try:
    from scripts.check_microbuild_plan import (
        DEFAULT_PLAN_PATH,
        load_plan,
        validate_plan,
    )
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from check_microbuild_plan import DEFAULT_PLAN_PATH, load_plan, validate_plan


ROOT = Path(__file__).resolve().parents[1]

# Manifest data may select these identifiers, but may never supply commands.
TEST_COMMANDS: dict[str, tuple[str, ...]] = {
    "manifest_contract": (sys.executable, "-m", "pytest", "-q", "tests/test_microbuild_plan.py"),
    "runner_contract": (sys.executable, "-m", "pytest", "-q", "tests/test_microbuild_runner.py"),
    "workflow_contract": (sys.executable, "-m", "pytest", "-q", "tests/test_microbuild_workflow.py"),
    "clean_wheel_inverter_block": (sys.executable, "scripts/validate_inverter_block_wheel.py"),
    "microbuild_evidence": (sys.executable, "-m", "pytest", "-q", "tests/test_microbuild_evidence.py"),
    "advancement_preview": (sys.executable, "-m", "pytest", "-q", "tests/test_microbuild_advancement.py", "-k", "preview"),
    "advancement_refusal": (sys.executable, "-m", "pytest", "-q", "tests/test_microbuild_advancement.py", "-k", "refus"),
    "ts004_integration": (sys.executable, "scripts/run_ts004_integration.py"),
    "ts004_programme_projection": (sys.executable, "-m", "pytest", "-q", "tests/test_programme_state.py"),
    "ts005_handoff": (sys.executable, "-m", "pytest", "-q", "tests/test_ts005_handoff.py"),
    "reference_block_command": (sys.executable, "-m", "pytest", "-q", "tests/test_reference_block_command.py", "-k", "reference_block"),
    "command_contract": (sys.executable, "-m", "pytest", "-q", "tests/test_reference_block_command.py", "-k", "contract"),
    "authority_bundle": (sys.executable, "-m", "pytest", "-q", "tests/test_authority_bundle.py", "-k", "regeneration"),
    "bundle_schema": (sys.executable, "-m", "pytest", "-q", "tests/test_authority_bundle.py", "-k", "schema"),
    "studio_mode_separation": ("node", "v10-development/tests/studio-authority.test.mjs", "mode"),
    "authority_bundle_render": ("node", "v10-development/tests/studio-authority.test.mjs", "bundle"),
    "authority_geometry_render": ("node", "v10-development/tests/studio-authority.test.mjs", "geometry"),
    "authority_evidence_render": ("node", "v10-development/tests/studio-authority.test.mjs", "evidence"),
    "local_authority_bridge": (sys.executable, "-m", "pytest", "-q", "tests/test_local_authority_bridge.py"),
    "end_to_end_authority_slice": (sys.executable, "-m", "pytest", "-q", "tests/test_end_to_end_authority_slice.py"),
}


class UnknownTestIdentifier(ValueError):
    """The manifest requested a test outside the repository allowlist."""


def command_for_test(test_id: str) -> tuple[str, ...]:
    try:
        return TEST_COMMANDS[test_id]
    except KeyError as exc:
        raise UnknownTestIdentifier(f"unknown microbuild test id: {test_id}") from exc


def active_test_id(plan_path: Path = DEFAULT_PLAN_PATH) -> str:
    plan = load_plan(plan_path)
    summary = validate_plan(plan)
    test_id = summary["active_test_id"]
    if not isinstance(test_id, str):
        raise TypeError("active test identifier must be text")
    return test_id


def active_command(plan_path: Path = DEFAULT_PLAN_PATH) -> tuple[str, ...]:
    return command_for_test(active_test_id(plan_path))


def execute(command: Sequence[str]) -> int:
    completed = subprocess.run(tuple(command), cwd=ROOT, check=False)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN_PATH)
    parser.add_argument("--test-id")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    test_id = args.test_id or active_test_id(args.plan)
    command = command_for_test(test_id)
    if not args.execute:
        print(json.dumps({"test_id": test_id, "command": list(command)}, sort_keys=True))
        return 0
    return execute(command)


if __name__ == "__main__":
    raise SystemExit(main())
