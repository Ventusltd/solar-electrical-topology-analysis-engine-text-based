from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.check_microbuild_plan import load_plan, validate_plan
from scripts.run_microbuild import (
    TEST_COMMANDS,
    UnknownTestIdentifier,
    active_command,
    active_test_id,
    command_for_test,
)


ROOT = Path(__file__).resolve().parents[1]


def test_active_manifest_selects_only_its_allowlisted_command() -> None:
    summary = validate_plan(load_plan())
    test_id = str(summary["active_test_id"])

    assert active_test_id() == test_id
    assert active_command() == TEST_COMMANDS[test_id]
    assert isinstance(active_command(), tuple)
    assert active_command()


def test_all_twenty_manifest_test_identifiers_are_allowlisted() -> None:
    plan = json.loads((ROOT / "microbuild-plan.json").read_text(encoding="utf-8"))
    manifest_ids = {item["test_id"] for item in plan["steps"]}

    assert manifest_ids == set(TEST_COMMANDS)
    assert len(TEST_COMMANDS) == 20
    assert all(isinstance(command, tuple) and command for command in TEST_COMMANDS.values())


def test_unknown_identifier_is_rejected_without_shell_execution() -> None:
    with pytest.raises(UnknownTestIdentifier, match="unknown microbuild test id"):
        command_for_test("rm_rf_repository")


def test_cli_prints_current_selected_command_without_executing_it() -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/run_microbuild.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["test_id"] == active_test_id()
    assert payload["command"] == list(active_command())
