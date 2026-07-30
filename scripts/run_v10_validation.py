#!/usr/bin/env python3
"""Run all declared V10 recovery baselines and write paired receipts."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "v10-development" / "recovery" / "validation"
JSON_PATH = REPORT_DIR / "V10_VALIDATION_LATEST.json"
MARKDOWN_PATH = REPORT_DIR / "V10_VALIDATION_LATEST.md"
MAX_OUTPUT_CHARS = 30_000

COMMANDS = (
    (
        "python",
        [sys.executable, "-m", "pytest", "-q"],
        ROOT,
    ),
    (
        "v8",
        ["node", "--test", "tests/v8-model.test.js"],
        ROOT,
    ),
    (
        "v9",
        ["node", "v9-sandbox/debug/run-tests.mjs"],
        ROOT,
    ),
    (
        "v10-javascript",
        ["npm", "test"],
        ROOT / "v10-development",
    ),
)


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def run_command(name: str, command: list[str], cwd: Path) -> dict:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        return_code = completed.returncode
        output = completed.stdout or ""
    except OSError as exc:
        return_code = 127
        output = f"unable to execute command: {exc}"

    duration_seconds = round(time.monotonic() - started, 3)
    if len(output) > MAX_OUTPUT_CHARS:
        output = (
            output[:MAX_OUTPUT_CHARS]
            + "\n...[output truncated by validation receipt]...\n"
        )

    return {
        "name": name,
        "command": command,
        "cwd": str(cwd.relative_to(ROOT)),
        "return_code": return_code,
        "pass": return_code == 0,
        "duration_seconds": duration_seconds,
        "output": output,
    }


def markdown_report(payload: dict) -> str:
    lines = [
        "# V10 Validation Receipt",
        "",
        f"Generated UTC: `{payload['generated_utc']}`  ",
        f"Repository head: `{payload['git_sha']}`  ",
        f"Overall result: `{'PASS' if payload['pass'] else 'FAIL'}`  ",
        f"Schema version: `{payload['schema_version']}`",
        "",
        "## Declared suites",
        "",
    ]

    for result in payload["results"]:
        lines.extend(
            [
                f"### {result['name']}",
                "",
                f"Result: `{'PASS' if result['pass'] else 'FAIL'}`  ",
                f"Return code: `{result['return_code']}`  ",
                f"Duration: `{result['duration_seconds']} s`  ",
                f"Working directory: `{result['cwd'] or '.'}`  ",
                "Command:",
                "",
                "```text",
                " ".join(result["command"]),
                "```",
                "",
                "Output:",
                "",
                "```text",
                result["output"].rstrip(),
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Gate",
            "",
            (
                "All declared Python, V8, V9 and V10 JavaScript suites passed."
                if payload["pass"]
                else "One or more declared suites failed; authority promotion is blocked."
            ),
            "",
            "This receipt records execution only. It does not by itself promote an implementation to engineering authority.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    results = [
        run_command(name, list(command), cwd)
        for name, command, cwd in COMMANDS
    ]
    payload = {
        "schema_version": "globalgrid2050.v10-validation-receipt.v1",
        "generated_utc": utc_now(),
        "repository": "Ventusltd/solar-electrical-topology-analysis-engine-text-based",
        "git_sha": os.environ.get("GITHUB_SHA", "local-or-unknown"),
        "pass": all(result["pass"] for result in results),
        "results": results,
    }

    JSON_PATH.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    MARKDOWN_PATH.write_text(markdown_report(payload), encoding="utf-8")
    print(json.dumps({"pass": payload["pass"], "reports": [str(MARKDOWN_PATH), str(JSON_PATH)]}))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
