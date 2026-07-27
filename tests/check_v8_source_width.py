#!/usr/bin/env python3
"""Fail CI when editable V8 source returns to mega-line formatting."""

from __future__ import annotations

from pathlib import Path

MAX_WIDTH = 120
ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ROOT / "v8-leapfrog" / "index.html",
    ROOT / "v8-leapfrog" / "app.js",
    ROOT / "v8-leapfrog" / "model.js",
    ROOT / "v8-leapfrog" / "styles.css",
    ROOT / "v8-leapfrog" / "tests.html",
    ROOT / "tests" / "v8-model.test.js",
)


def main() -> int:
    failures: list[str] = []

    for path in FILES:
        if not path.exists():
            failures.append(f"missing source file: {path.relative_to(ROOT)}")
            continue

        text = path.read_text(encoding="utf-8")

        for line_number, line in enumerate(text.splitlines(), start=1):
            width = len(line.expandtabs(4))

            if width <= MAX_WIDTH:
                continue

            failures.append(
                f"{path.relative_to(ROOT)}:{line_number} "
                f"width={width} limit={MAX_WIDTH}"
            )

    if failures:
        print("V8 source-width law failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "V8 source-width law passed: "
        f"all editable lines are <= {MAX_WIDTH} characters"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
