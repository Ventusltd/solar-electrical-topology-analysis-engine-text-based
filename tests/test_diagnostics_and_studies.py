import json

import pytest

from solar_topology.circuit import CircuitModel
from solar_topology.circuit_traversal import OrderedCircuitTraversal, TraversalIssue
from solar_topology.circuit_validation import (
    CircuitValidationResult,
    IssueSeverity,
    ValidationIssue,
)
from solar_topology.diagnostic_bridges import (
    build_validation_diagnostic_report,
    guarded_diagnostic_call,
)
from solar_topology.diagnostics import (
    Diagnostic,
    DiagnosticCategory,
    DiagnosticSeverity,
    StudyCoverage,
    StudyState,
    build_diagnostic_report,
    diagnostic_report_hash,
    diagnostic_report_json,
)
from solar_topology.study_registry import (
    INITIAL_STUDIES,
    StudyCategory,
    StudyDefinition,
    assess_study,
    build_study_registry,
    study_registry_hash,
    study_registry_json,
)


def test_diagnostic_report_accumulates_and_sorts_all_findings():
    report = build_diagnostic_report(
        [
            Diagnostic(
                code="Z.TEST",
                severity=DiagnosticSeverity.WARNING,
                category=DiagnosticCategory.INPUT,
                message="second",
            ),
            Diagnostic(
                code="A.TEST",
                severity=DiagnosticSeverity.ERROR,
                category=DiagnosticCategory.TOPOLOGY,
                message="first",
            ),
        ],
        [
            StudyCoverage(
                study_id="b-study",
                state=StudyState.NOT_CHECKED,
                reason="not run",
            ),
            StudyCoverage(
                study_id="a-study",
                state=StudyState.CHECKED_PASS,
            ),
        ],
    )
    assert [item.code for item in report.diagnostics] == ["A.TEST", "Z.TEST"]
    assert [item.study_id for item in report.coverage] == ["a-study", "b-study"]
    assert report.blocking
    assert report.error_count == 1
    assert report.warning_count == 1
    assert diagnostic_report_hash(report).startswith("sha256:")


def test_public_payload_omits_internal_detail_and_is_deterministic():
    report = build_diagnostic_report(
        [
            Diagnostic(
                code="PUBLIC.SAFE",
                severity=DiagnosticSeverity.ERROR,
                category=DiagnosticCategory.PUBLICATION,
                message="public message",
                public_detail="safe",
                internal_detail="NDA document location",
            )
        ]
    )
    public_payload = json.loads(diagnostic_report_json(report, public=True))
    assert "internal_detail" not in public_payload["diagnostics"][0]
    assert diagnostic_report_json(report, public=True) == diagnostic_report_json(
        report, public=True
    )


def test_validation_bridge_preserves_multiple_circuit_and_traversal_issues():
    circuit = CircuitValidationResult(
        (
            ValidationIssue("DUPLICATE_OBJECT_ID", "duplicate", object_id="o-1"),
            ValidationIssue(
                "ASSUMED_GEOMETRY",
                "assumed",
                severity=IssueSeverity.WARNING,
                object_id="o-2",
            ),
        )
    )
    traversal = OrderedCircuitTraversal(
        start_terminal_id="a",
        end_terminal_id="b",
        ordered_terminal_ids=(),
        ordered_connection_ids=(),
        ordered_segment_ids=(),
        issues=(TraversalIssue("BRANCH", "ambiguous branch", terminal_id="t-1"),),
    )
    report = build_validation_diagnostic_report(
        circuit=circuit, traversal=traversal, subject_id="model-1"
    )
    assert {item.code for item in report.diagnostics} == {
        "CIRCUIT.DUPLICATE_OBJECT_ID",
        "CIRCUIT.ASSUMED_GEOMETRY",
        "TRAVERSAL.BRANCH",
    }
    assert report.blocking
    assert all(item.state == StudyState.CHECKED_FAIL for item in report.coverage)


def test_missing_validator_results_are_explicitly_not_checked():
    report = build_validation_diagnostic_report(subject_id="model-1")
    assert not report.diagnostics
    assert {item.state for item in report.coverage} == {StudyState.NOT_CHECKED}
    assert not report.blocking


def test_legacy_exception_is_public_safe():
    def fail():
        raise RuntimeError("internal path /secret/file")

    result, diagnostics = guarded_diagnostic_call(
        fail,
        code="LEGACY.FAIL",
        category=DiagnosticCategory.INTERNAL,
        public_message="calculation could not be completed",
    )
    assert result is None
    assert diagnostics[0].message == "calculation could not be completed"
    assert "/secret/file" in diagnostics[0].internal_detail


def test_study_registry_blocks_missing_inputs_and_undeclared_criteria():
    definition = StudyDefinition(
        study_id="limit-study",
        category=StudyCategory.STEADY_STATE,
        title="Limit study",
        method_reference="method:v1",
        required_input_ids=("a", "b"),
        required_evidence_roles=("basis",),
        acceptance_criterion_required=True,
    )
    missing = assess_study(
        definition,
        subject_id="circuit-1",
        available_input_ids=("a",),
        available_evidence_roles=(),
    )
    assert missing.coverage.state == StudyState.BLOCKED
    assert missing.missing_input_ids == ("b",)
    assert missing.missing_evidence_roles == ("basis",)

    no_criterion = assess_study(
        definition,
        subject_id="circuit-1",
        available_input_ids=("a", "b"),
        available_evidence_roles=("basis",),
    )
    assert no_criterion.coverage.state == StudyState.BLOCKED
    assert "criterion" in no_criterion.coverage.reason


def test_study_states_distinguish_ready_not_run_pass_warning_and_fail():
    definition = StudyDefinition(
        study_id="study",
        category=StudyCategory.ELECTRICAL if hasattr(StudyCategory, "ELECTRICAL") else StudyCategory.STEADY_STATE,
        title="Study",
        method_reference="method:v1",
    )
    ready = assess_study(
        definition,
        subject_id=None,
        available_input_ids=(),
        available_evidence_roles=(),
    )
    passed = assess_study(
        definition,
        subject_id=None,
        available_input_ids=(),
        available_evidence_roles=(),
        performed=True,
        passed=True,
    )
    warning = assess_study(
        definition,
        subject_id=None,
        available_input_ids=(),
        available_evidence_roles=(),
        performed=True,
        passed=True,
        warning=True,
    )
    failed = assess_study(
        definition,
        subject_id=None,
        available_input_ids=(),
        available_evidence_roles=(),
        performed=True,
        passed=False,
    )
    assert ready.coverage.state == StudyState.NOT_CHECKED
    assert passed.coverage.state == StudyState.CHECKED_PASS
    assert warning.coverage.state == StudyState.CHECKED_WARNING
    assert failed.coverage.state == StudyState.CHECKED_FAIL


def test_initial_registry_is_unique_and_deterministic():
    assessments = [
        assess_study(
            definition,
            subject_id="generic-circuit",
            available_input_ids=(),
            available_evidence_roles=(),
        )
        for definition in reversed(INITIAL_STUDIES)
    ]
    registry = build_study_registry(assessments)
    assert len(registry.definitions) == len(INITIAL_STUDIES)
    assert study_registry_hash(registry).startswith("sha256:")
    assert study_registry_json(registry) == study_registry_json(registry)


def test_duplicate_diagnostics_and_coverage_are_rejected():
    diagnostic = Diagnostic(
        code="DUP.TEST",
        severity=DiagnosticSeverity.ERROR,
        category=DiagnosticCategory.INPUT,
        message="duplicate",
    )
    with pytest.raises(ValueError, match="duplicate diagnostics"):
        build_diagnostic_report([diagnostic, diagnostic])
    coverage = StudyCoverage("study", StudyState.CHECKED_PASS)
    with pytest.raises(ValueError, match="duplicate study coverage"):
        build_diagnostic_report(coverage=[coverage, coverage])
