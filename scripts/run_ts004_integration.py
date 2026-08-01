#!/usr/bin/env python3
"""Run the complete TS-004 integration envelope from repository authority."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
TS004_INTEGRATION_SCHEMA_VERSION = (
    "globalgrid2050.solar-dc.ts004-integration.v1"
)
V10_RESULT = (
    ROOT
    / "v10-development"
    / "recovery"
    / "validation"
    / "V10_VALIDATION_LATEST.json"
)

GATES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "capsule_links",
        (sys.executable, "scripts/check_capsule_links.py", "--check"),
    ),
    (
        "programme_state",
        (sys.executable, "scripts/sync_programme_state.py", "--check"),
    ),
    (
        "declared_suites",
        (sys.executable, "scripts/run_v10_validation.py"),
    ),
    (
        "established_clean_wheel",
        (sys.executable, "scripts/validate_clean_wheel.py"),
    ),
    (
        "inverter_block_clean_wheel",
        (sys.executable, "scripts/validate_inverter_block_wheel.py"),
    ),
)


def _print_declared_suite_failures() -> None:
    if not V10_RESULT.is_file():
        print("declared-suite receipt was not written", file=sys.stderr)
        return
    payload = json.loads(V10_RESULT.read_text(encoding="utf-8"))
    for result in payload.get("results", []):
        if result.get("pass"):
            continue
        print(
            f"DECLARED SUITE FAILURE: {result.get('name')} "
            f"return_code={result.get('return_code')}",
            file=sys.stderr,
        )
        print(str(result.get("output", "")).rstrip(), file=sys.stderr)


def run_gate(name: str, command: tuple[str, ...]) -> dict[str, object]:
    completed = subprocess.run(command, cwd=ROOT, check=False)
    if completed.returncode != 0:
        if name == "declared_suites":
            _print_declared_suite_failures()
        raise RuntimeError(f"TS-004 integration gate failed: {name}")
    return {"name": name, "pass": True}


def main() -> int:
    results = [run_gate(name, command) for name, command in GATES]
    payload = {
        "schema_version": TS004_INTEGRATION_SCHEMA_VERSION,
        "pass": True,
        "gates": results,
    }
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
