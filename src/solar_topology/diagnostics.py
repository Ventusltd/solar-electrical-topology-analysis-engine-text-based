"""Structured, deterministic diagnostics for V10 engineering studies.

Diagnostics distinguish failed checks from studies that were not performed. Public
payloads deliberately omit internal-only detail while preserving stable codes,
severity, subjects and remediation guidance.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json
from typing import Iterable


DIAGNOSTIC_SCHEMA_VERSION = "globalgrid2050.solar-dc.diagnostics.v10.1"


class DiagnosticSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class DiagnosticCategory(StrEnum):
    INPUT = "input"
    TOPOLOGY = "topology"
    GEOMETRY = "geometry"
    ELECTRICAL = "electrical"
    EVIDENCE = "evidence"
    PUBLICATION = "publication"
    PERSISTENCE = "persistence"
    COVERAGE = "coverage"
    INTERNAL = "internal"


class StudyState(StrEnum):
    NOT_APPLICABLE = "not_applicable"
    NOT_CHECKED = "not_checked"
    BLOCKED = "blocked"
    CHECKED_PASS = "checked_pass"
    CHECKED_WARNING = "checked_warning"
    CHECKED_FAIL = "checked_fail"


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: DiagnosticSeverity
    category: DiagnosticCategory
    message: str
    subject_id: str | None = None
    field: str | None = None
    observed_value: str | int | float | bool | None = None
    expected_constraint: str | None = None
    method_reference: str | None = None
    source_reference: str | None = None
    remediation: str | None = None
    public_detail: str | None = None
    internal_detail: str | None = None
    schema_version: str = DIAGNOSTIC_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.code, str) or not self.code.strip():
            raise ValueError("diagnostic code must be non-empty text")
        if self.code != self.code.upper() or any(
            char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-" for char in self.code
        ):
            raise ValueError("diagnostic code must use uppercase stable-code syntax")
        if not isinstance(self.severity, DiagnosticSeverity):
            raise TypeError("severity must be DiagnosticSeverity")
        if not isinstance(self.category, DiagnosticCategory):
            raise TypeError("category must be DiagnosticCategory")
        if not isinstance(self.message, str) or not self.message.strip():
            raise ValueError("diagnostic message must be non-empty text")

    @property
    def blocking(self) -> bool:
        return self.severity in {
            DiagnosticSeverity.ERROR,
            DiagnosticSeverity.CRITICAL,
        }


@dataclass(frozen=True)
class StudyCoverage:
    study_id: str
    state: StudyState
    subject_id: str | None = None
    method_reference: str | None = None
    evidence_source_ids: tuple[str, ...] = ()
    reason: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.study_id, str) or not self.study_id.strip():
            raise ValueError("study_id must be non-empty text")
        if not isinstance(self.state, StudyState):
            raise TypeError("state must be StudyState")
        if tuple(sorted(set(self.evidence_source_ids))) != self.evidence_source_ids:
            raise ValueError("evidence_source_ids must be unique and sorted")
        if self.state in {StudyState.NOT_CHECKED, StudyState.BLOCKED} and not self.reason:
            raise ValueError("not-checked and blocked studies require a reason")


@dataclass(frozen=True)
class DiagnosticReport:
    report_id: str
    diagnostics: tuple[Diagnostic, ...]
    coverage: tuple[StudyCoverage, ...]
    schema_version: str = DIAGNOSTIC_SCHEMA_VERSION

    @property
    def blocking(self) -> bool:
        return any(item.blocking for item in self.diagnostics) or any(
            item.state in {StudyState.BLOCKED, StudyState.CHECKED_FAIL}
            for item in self.coverage
        )

    @property
    def error_count(self) -> int:
        return sum(item.blocking for item in self.diagnostics)

    @property
    def warning_count(self) -> int:
        return sum(
            item.severity is DiagnosticSeverity.WARNING for item in self.diagnostics
        )


def _diagnostic_key(item: Diagnostic) -> tuple[str, str, str, str]:
    return (
        item.code,
        item.subject_id or "",
        item.field or "",
        item.message,
    )


def _coverage_key(item: StudyCoverage) -> tuple[str, str]:
    return (item.study_id, item.subject_id or "")


def build_diagnostic_report(
    diagnostics: Iterable[Diagnostic] = (),
    coverage: Iterable[StudyCoverage] = (),
    *,
    report_id: str | None = None,
) -> DiagnosticReport:
    ordered_diagnostics = tuple(sorted(diagnostics, key=_diagnostic_key))
    ordered_coverage = tuple(sorted(coverage, key=_coverage_key))
    diagnostic_keys = [_diagnostic_key(item) for item in ordered_diagnostics]
    coverage_keys = [_coverage_key(item) for item in ordered_coverage]
    if len(diagnostic_keys) != len(set(diagnostic_keys)):
        raise ValueError("duplicate diagnostics are not permitted")
    if len(coverage_keys) != len(set(coverage_keys)):
        raise ValueError("duplicate study coverage entries are not permitted")
    payload = {
        "diagnostics": [diagnostic_payload(item, public=False) for item in ordered_diagnostics],
        "coverage": [coverage_payload(item) for item in ordered_coverage],
    }
    generated = "DIAG:" + hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return DiagnosticReport(
        report_id=report_id or generated,
        diagnostics=ordered_diagnostics,
        coverage=ordered_coverage,
    )


def diagnostic_payload(item: Diagnostic, *, public: bool) -> dict[str, object]:
    payload: dict[str, object] = {
        "schema_version": item.schema_version,
        "code": item.code,
        "severity": item.severity.value,
        "category": item.category.value,
        "message": item.message,
        "subject_id": item.subject_id,
        "field": item.field,
        "observed_value": item.observed_value,
        "expected_constraint": item.expected_constraint,
        "method_reference": item.method_reference,
        "source_reference": item.source_reference,
        "remediation": item.remediation,
        "public_detail": item.public_detail,
    }
    if not public:
        payload["internal_detail"] = item.internal_detail
    return payload


def coverage_payload(item: StudyCoverage) -> dict[str, object]:
    return {
        "study_id": item.study_id,
        "state": item.state.value,
        "subject_id": item.subject_id,
        "method_reference": item.method_reference,
        "evidence_source_ids": list(item.evidence_source_ids),
        "reason": item.reason,
    }


def diagnostic_report_payload(
    report: DiagnosticReport,
    *,
    public: bool = False,
) -> dict[str, object]:
    return {
        "schema_version": report.schema_version,
        "report_id": report.report_id,
        "blocking": report.blocking,
        "error_count": report.error_count,
        "warning_count": report.warning_count,
        "diagnostics": [
            diagnostic_payload(item, public=public) for item in report.diagnostics
        ],
        "coverage": [coverage_payload(item) for item in report.coverage],
    }


def diagnostic_report_json(
    report: DiagnosticReport,
    *,
    public: bool = False,
) -> str:
    return json.dumps(
        diagnostic_report_payload(report, public=public),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def diagnostic_report_hash(report: DiagnosticReport) -> str:
    digest = hashlib.sha256(
        diagnostic_report_json(report, public=False).encode("utf-8")
    ).hexdigest()
    return f"sha256:{digest}"


def require_non_blocking(report: DiagnosticReport) -> DiagnosticReport:
    if report.blocking:
        codes = ", ".join(item.code for item in report.diagnostics if item.blocking)
        raise ValueError(f"diagnostic report is blocking: {codes or 'study coverage failed'}")
    return report


def diagnostic_from_exception(
    error: Exception,
    *,
    code: str,
    category: DiagnosticCategory,
    subject_id: str | None = None,
    field: str | None = None,
    public_message: str | None = None,
) -> Diagnostic:
    """Convert a legacy exception without exposing its stack or internal detail."""

    return Diagnostic(
        code=code,
        severity=DiagnosticSeverity.ERROR,
        category=category,
        message=public_message or str(error) or error.__class__.__name__,
        subject_id=subject_id,
        field=field,
        public_detail=public_message,
        internal_detail=f"{error.__class__.__name__}: {error}",
    )
