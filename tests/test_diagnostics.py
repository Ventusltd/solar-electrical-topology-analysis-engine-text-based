import json

import pytest

from solar_topology.circuit_validation import (
    CircuitValidationResult,
    IssueSeverity,
    ValidationIssue,
)
from solar_topology.diagnostic_adapters import (
    circuit_validation_diagnostics,
    coverage_for_unperformed_studies,
)
from solar_topology.diagnostics import (
    Diagnostic,
    DiagnosticCategory,
    DiagnosticSeverity,
    StudyCoverage,
    StudyState,
    build_diagnostic_report,
    diagnostic_from_exception,
    diagnostic_report_hash,
    diagnostic_report_json,
    require_non_blocking,
)
from solar_topology.study_applicability import (
    AcceptanceCriterion,
    CriterionOperator,
    StudyKind,
    applicability_coverage,
    build_study_applicability,
    evaluate_criterion,
)


def test_accumulates_sorts_and_counts_diagnostics():
    report = build_diagnostic_report(
        [
            Diagnostic(
                code="Z.WARNING",
                severity=DiagnosticSeverity.WARNING,
                category=DiagnosticCategory.EVIDENCE,
                message="candidate evidence",
            ),
            Diagnostic(
                code="A.ERROR",
                severity=DiagnosticSeverity.ERROR,
                category=DiagnosticCategory.TOPOLOGY,
                message="broken topology",
            ),
        ]
    )
    assert [item.code for item in report.diagnostics] == ["A.ERROR", "Z.WARNING"]
    assert report.blocking
    assert report.error_count == 1
    assert report.warning_count == 1
    assert diagnostic_report_hash(report).startswith("sha256:")
    with pytest.raises(ValueError, match="A.ERROR"):
        require_non_blocking(report)


def test_public_payload_omits_internal_detail_and_is_deterministic():
    diagnostic = Diagnostic(
        code="PUBLIC.SAFE",
        severity=DiagnosticSeverity.INFO,
        category=DiagnosticCategory.PUBLICATION,
        message="public message",
        public_detail="safe detail",
        internal_detail="NDA source path must not escape",
    )
    first = build_diagnostic_report([diagnostic])
    second = build_diagnostic_report(reversed(first.diagnostics))
    public_payload = json.loads(diagnostic_report_json(first, public=True))
    assert "internal_detail" not in public_payload["diagnostics"][0]
    assert diagnostic_report_json(first) == diagnostic_report_json(second)


def test_not_checked_and_blocked_require_reasons():
    with pytest.raises(ValueError, match="require a reason"):
        StudyCoverage("ampacity", StudyState.NOT_CHECKED)
    entries = coverage_for_unperformed_studies(
        [("ampacity", "no current-carrying-capacity criterion supplied")]
    )
    assert entries[0].state is StudyState.NOT_CHECKED


def test_exception_bridge_does_not_publish_internal_exception_detail():
    item = diagnostic_from_exception(
        ValueError("private/path/source.xlsx"),
        code="LEGACY.FAIL",
        category=DiagnosticCategory.INTERNAL,
        public_message="legacy calculation failed",
    )
    report = build_diagnostic_report([item])
    public_json = diagnostic_report_json(report, public=True)
    assert "private/path" not in public_json
    assert "legacy calculation failed" in public_json


def test_circuit_validation_adapter_preserves_all_issues():
    result = CircuitValidationResult(
        (
            ValidationIssue("DUPLICATE_OBJECT_ID", "duplicate", object_id="o1"),
            ValidationIssue(
                "ASSUMED_GEOMETRY",
                "geometry is assumed",
                severity=IssueSeverity.WARNING,
                object_id="o2",
            ),
        )
    )
    report = circuit_validation_diagnostics(result, subject_id="model-1")
    assert len(report.diagnostics) == 2
    assert report.coverage[0].state is StudyState.CHECKED_FAIL
    assert report.blocking


def _criterion():
    return AcceptanceCriterion(
        criterion_id="criterion:string-voltage",
        study_kind=StudyKind.COLD_VOC,
        operator=CriterionOperator.MAXIMUM,
        threshold=1500.0,
        unit="V",
        source_id="public:system-voltage-basis",
        method_reference="cold-voc-method-v1",
        public_support=True,
    )


def test_applicability_distinguishes_missing_inputs_from_no_criterion():
    blocked = build_study_applicability(
        StudyKind.COLD_VOC,
        required_input_ids=("beta_voc", "cold_temperature", "module_voc"),
        available_input_ids=("module_voc",),
        criterion=_criterion(),
    )
    assert not blocked.executable
    assert applicability_coverage(blocked).state is StudyState.BLOCKED

    ready_without_verdict = build_study_applicability(
        StudyKind.LOOP_GEOMETRY,
        required_input_ids=("ordered_segments",),
        available_input_ids=("ordered_segments",),
    )
    assert ready_without_verdict.executable
    assert not ready_without_verdict.verdict_capable
    assert applicability_coverage(ready_without_verdict).state is StudyState.NOT_CHECKED


def test_criterion_evaluation_is_unit_safe_and_source_declared():
    criterion = _criterion()
    assert evaluate_criterion(1499.0, "V", criterion)
    assert not evaluate_criterion(1501.0, "V", criterion)
    with pytest.raises(ValueError, match="unit"):
        evaluate_criterion(1.5, "kV", criterion)
    with pytest.raises(ValueError, match="source_id"):
        AcceptanceCriterion(
            criterion_id="bad",
            study_kind=StudyKind.AMPACITY,
            operator=CriterionOperator.MINIMUM,
            threshold=20.0,
            unit="A",
            source_id="",
            method_reference="method",
        )


def test_duplicate_diagnostics_and_coverage_are_rejected():
    item = Diagnostic(
        code="DUP.TEST",
        severity=DiagnosticSeverity.WARNING,
        category=DiagnosticCategory.INPUT,
        message="same",
    )
    with pytest.raises(ValueError, match="duplicate diagnostics"):
        build_diagnostic_report([item, item])
    coverage = StudyCoverage("study", StudyState.CHECKED_PASS)
    with pytest.raises(ValueError, match="duplicate study coverage"):
        build_diagnostic_report(coverage=[coverage, coverage])
