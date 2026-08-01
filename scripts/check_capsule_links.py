#!/usr/bin/env python3
"""Validate path references inside Quantum Spawn and Trueself capsules."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
CAPSULE_ROOTS = (
    ROOT / "docs" / "quantum-spawn",
    ROOT / "docs" / "trueself",
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BACKTICK_RE = re.compile(r"`([^`\n]+\.md(?:#[^`\n]+)?)`")
TITLE_RE = re.compile(r"^\*\*Title:\*\*\s*(.+?)\s*$", re.MULTILINE)
CANONICAL_TARGET_RE = re.compile(
    r"^\*\*Canonical Target:\*\*\s*\[[^\]]+\]\(([^)]+)\)\s*$",
    re.MULTILINE,
)
PLACEHOLDER_TOKENS = ("YYYY", "...", "<", ">", "{", "}", "*", "?")
ROOT_PREFIXES = (
    "docs/",
    "schemas/",
    "scripts/",
    "tests/",
    "src/",
    "v6-",
    "v7-",
    "v8-",
    "v9-",
    "v10-",
    "restore/",
    "restore_points/",
)


@dataclass(frozen=True)
class LinkIssue:
    source: Path
    reference: str
    resolved: Path | None
    reason: str

    def message(self) -> str:
        source = self.source.relative_to(ROOT).as_posix()
        resolved = (
            self.resolved.relative_to(ROOT).as_posix()
            if self.resolved is not None and self.resolved.is_relative_to(ROOT)
            else str(self.resolved) if self.resolved is not None else "unresolved"
        )
        return f"{source}: {self.reference!r} -> {resolved}: {self.reason}"


def capsule_files() -> tuple[Path, ...]:
    files: list[Path] = []
    for root in CAPSULE_ROOTS:
        if root.is_dir():
            files.extend(root.rglob("*.md"))
    return tuple(sorted(files))


def clean_reference(raw: str) -> str | None:
    value = unquote(raw.strip()).strip("<>")
    if not value or value.startswith(("http://", "https://", "mailto:")):
        return None
    value = value.split("#", 1)[0].strip()
    if not value.lower().endswith(".md"):
        return None
    if any(token in value for token in PLACEHOLDER_TOKENS):
        return None
    return value


def extract_references(text: str) -> tuple[str, ...]:
    references: set[str] = set()
    for match in MARKDOWN_LINK_RE.finditer(text):
        cleaned = clean_reference(match.group(1).split()[0])
        if cleaned is not None:
            references.add(cleaned)
    for match in BACKTICK_RE.finditer(text):
        cleaned = clean_reference(match.group(1))
        if cleaned is not None:
            references.add(cleaned)
    return tuple(sorted(references))


def resolve_reference(source: Path, reference: str) -> Path:
    candidate = Path(reference)
    if candidate.is_absolute():
        return ROOT / str(candidate).lstrip("/")
    if reference.startswith(ROOT_PREFIXES) or candidate.parent == Path(".") and reference in {
        "README.md",
        "BUILD_RECOVERY_INSTRUCTIONS_CHATGPT.md",
    }:
        return ROOT / candidate
    return source.parent / candidate


def canonical_title(path: Path) -> str | None:
    match = TITLE_RE.search(path.read_text(encoding="utf-8"))
    return match.group(1).strip() if match else None


def check_compatibility_pointer(path: Path, text: str) -> tuple[LinkIssue, ...]:
    if not text.startswith("# Quantum Spawn Compatibility Pointer"):
        return ()
    match = CANONICAL_TARGET_RE.search(text)
    if match is None:
        return (
            LinkIssue(path, "Canonical Target", None, "compatibility pointer lacks canonical target"),
        )
    reference = clean_reference(match.group(1))
    if reference is None:
        return (
            LinkIssue(path, match.group(1), None, "canonical target is not a concrete Markdown path"),
        )
    target = resolve_reference(path, reference).resolve()
    if not target.is_file():
        return (
            LinkIssue(path, reference, target, "canonical target does not exist"),
        )
    pointer_title = canonical_title(path) or ""
    target_title = canonical_title(target)
    if target_title is None:
        return (
            LinkIssue(path, reference, target, "canonical target has no Title metadata"),
        )
    if target_title not in pointer_title:
        return (
            LinkIssue(
                path,
                reference,
                target,
                f"pointer title does not contain canonical title {target_title!r}",
            ),
        )
    return ()


def check_capsule_links() -> tuple[LinkIssue, ...]:
    issues: list[LinkIssue] = []
    for source in capsule_files():
        text = source.read_text(encoding="utf-8")
        issues.extend(check_compatibility_pointer(source, text))
        for reference in extract_references(text):
            resolved = resolve_reference(source, reference).resolve()
            if not resolved.is_relative_to(ROOT):
                issues.append(
                    LinkIssue(source, reference, resolved, "reference escapes repository root")
                )
            elif not resolved.is_file():
                issues.append(
                    LinkIssue(source, reference, resolved, "referenced Markdown file does not exist")
                )
    return tuple(issues)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate capsule references")
    parser.parse_args(argv)

    issues = check_capsule_links()
    if issues:
        print("capsule-link integrity failed:", file=sys.stderr)
        for issue in issues:
            print("- " + issue.message(), file=sys.stderr)
        return 1
    print(f"capsule-link integrity passed for {len(capsule_files())} Markdown capsules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
