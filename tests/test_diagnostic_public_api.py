import solar_topology as api


def test_diagnostic_and_applicability_public_api_is_exported():
    required = {
        "Diagnostic",
        "DiagnosticReport",
        "DiagnosticSeverity",
        "StudyCoverage",
        "StudyState",
        "build_diagnostic_report",
        "circuit_validation_diagnostics",
        "AcceptanceCriterion",
        "StudyApplicability",
        "StudyKind",
        "build_study_applicability",
        "evaluate_criterion",
    }
    missing = sorted(name for name in required if not hasattr(api, name))
    assert not missing, missing
