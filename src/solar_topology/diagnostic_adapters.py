"""Adapters from existing V10 validation results to unified diagnostics."""

from __future__ import annotations

from collections.abc import Iterable

from .circuit_validation import CircuitValidationResult, IssueSeverity
from .diagnostics import (
    Diagnostic,
    DiagnosticCategory,
    DiagnosticReport,
    DiagnosticSeverity,
    StudyCoverage,
    StudyState,
    build_diagnostic_report,
)


DIAGNOSTIC_ADAPTER_VERSION = "globalgrid2050.solar-dc.diagnostic-adapters.v10.1"


def circuit_validation_diagnostics(
    result: CircuitValidationResult,
    *,
    study_id: str = "canonical-circuit-validation",
    subject_id: str | None = None,
) -> DiagnosticReport:
    if not isinstance(result, CircuitValidationResult):
        raise TypeError("result must be CircuitValidationResult")
    diagnostics = []
    for issue in result.issues:
        subject = issue.object_id or issue.terminal_id or issue.connection_id or subject_id
        diagnostics.append(
            Diagnostic(
                code=f"CIRCUIT.{issue.code}",
                severity=(
                    DiagnosticSeverity.ERROR
                    if issue.severity is IssueSeverity.ERROR
                    else DiagnosticSeverity.WARNING
                ),
                category=DiagnosticCategory.TOPOLOGY,
                message=issue.message,
                subject_id=subject,
                method_reference=DIAGNOSTIC_ADAPTER_VERSION,
                public_detail=issue.message,
            )
        )
    if result.valid:
        state = StudyState.CHECKED_WARNING if diagnostics else StudyState.CHECKED_PASS
    else:
        state = StudyState.CHECKED_FAIL
    return build_diagnostic_report(
        diagnostics,
        (
            StudyCoverage(
                study_id=study_id,
                state=state,
                subject_id=subject_id,
                method_reference=DIAGNOSTIC_ADAPTER_VERSION,
            ),
        ),
    )


def coverage_for_unperformed_studies(
    studies: Iterable[tuple[str, str]],
    *,
    subject_id: str | None = None,
) -> tuple[StudyCoverage, ...]:
    """Create explicit NOT_CHECKED records from (study_id, reason) pairs."""

    return tuple(
        StudyCoverage(
            study_id=study_id,
            state=StudyState.NOT_CHECKED,
            subject_id=subject_id,
            reason=reason,
        )
        for study_id, reason in studies
    )
