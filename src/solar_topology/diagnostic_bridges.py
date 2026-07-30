"""Adapters from existing V10 validators into the unified diagnostic contract."""

from __future__ import annotations

from collections.abc import Iterable

from .circuit_traversal import OrderedCircuitTraversal
from .circuit_validation import CircuitValidationResult, IssueSeverity
from .diagnostics import (
    Diagnostic,
    DiagnosticCategory,
    DiagnosticReport,
    DiagnosticSeverity,
    StudyCoverage,
    StudyState,
    build_diagnostic_report,
    diagnostic_from_exception,
)

DIAGNOSTIC_BRIDGE_VERSION = "globalgrid2050.solar-dc.diagnostic-bridges.v10.1"


def _severity(value: IssueSeverity) -> DiagnosticSeverity:
    return (
        DiagnosticSeverity.ERROR
        if value is IssueSeverity.ERROR
        else DiagnosticSeverity.WARNING
    )


def diagnostics_from_circuit_validation(
    result: CircuitValidationResult,
    *,
    subject_id: str | None = None,
) -> tuple[Diagnostic, ...]:
    """Convert every circuit issue without losing the accumulating behaviour."""

    if not isinstance(result, CircuitValidationResult):
        raise TypeError("result must be CircuitValidationResult")
    converted = []
    for issue in result.issues:
        local_subject = (
            issue.object_id
            or issue.terminal_id
            or issue.connection_id
            or subject_id
        )
        converted.append(
            Diagnostic(
                code=f"CIRCUIT.{issue.code}",
                severity=_severity(issue.severity),
                category=DiagnosticCategory.TOPOLOGY,
                message=issue.message,
                subject_id=local_subject,
                method_reference=DIAGNOSTIC_BRIDGE_VERSION,
            )
        )
    return tuple(converted)


def diagnostics_from_traversal(
    traversal: OrderedCircuitTraversal,
    *,
    subject_id: str | None = None,
) -> tuple[Diagnostic, ...]:
    if not isinstance(traversal, OrderedCircuitTraversal):
        raise TypeError("traversal must be OrderedCircuitTraversal")
    return tuple(
        Diagnostic(
            code=f"TRAVERSAL.{issue.code}",
            severity=DiagnosticSeverity.ERROR,
            category=DiagnosticCategory.TOPOLOGY,
            message=issue.message,
            subject_id=issue.terminal_id or issue.connection_id or subject_id,
            method_reference=DIAGNOSTIC_BRIDGE_VERSION,
        )
        for issue in traversal.issues
    )


def guarded_diagnostic_call(
    function,
    *args,
    code: str,
    category: DiagnosticCategory,
    subject_id: str | None = None,
    field: str | None = None,
    public_message: str | None = None,
    **kwargs,
):
    """Run legacy throw-based code and return a value plus zero/one diagnostics."""

    try:
        return function(*args, **kwargs), ()
    except Exception as error:  # deliberate boundary around legacy validators
        return None, (
            diagnostic_from_exception(
                error,
                code=code,
                category=category,
                subject_id=subject_id,
                field=field,
                public_message=public_message,
            ),
        )


def build_validation_diagnostic_report(
    *,
    circuit: CircuitValidationResult | None = None,
    traversal: OrderedCircuitTraversal | None = None,
    extra_diagnostics: Iterable[Diagnostic] = (),
    coverage: Iterable[StudyCoverage] = (),
    subject_id: str | None = None,
) -> DiagnosticReport:
    diagnostics = list(extra_diagnostics)
    coverage_items = list(coverage)
    if circuit is None:
        coverage_items.append(
            StudyCoverage(
                study_id="circuit-validation",
                state=StudyState.NOT_CHECKED,
                subject_id=subject_id,
                reason="circuit validation result was not supplied",
            )
        )
    else:
        diagnostics.extend(
            diagnostics_from_circuit_validation(circuit, subject_id=subject_id)
        )
        coverage_items.append(
            StudyCoverage(
                study_id="circuit-validation",
                state=(
                    StudyState.CHECKED_PASS
                    if circuit.valid
                    else StudyState.CHECKED_FAIL
                ),
                subject_id=subject_id,
                method_reference=DIAGNOSTIC_BRIDGE_VERSION,
            )
        )
    if traversal is None:
        coverage_items.append(
            StudyCoverage(
                study_id="ordered-traversal",
                state=StudyState.NOT_CHECKED,
                subject_id=subject_id,
                reason="ordered traversal result was not supplied",
            )
        )
    else:
        diagnostics.extend(diagnostics_from_traversal(traversal, subject_id=subject_id))
        coverage_items.append(
            StudyCoverage(
                study_id="ordered-traversal",
                state=(
                    StudyState.CHECKED_PASS
                    if traversal.valid
                    else StudyState.CHECKED_FAIL
                ),
                subject_id=subject_id,
                method_reference=DIAGNOSTIC_BRIDGE_VERSION,
            )
        )
    return build_diagnostic_report(diagnostics, coverage_items)
