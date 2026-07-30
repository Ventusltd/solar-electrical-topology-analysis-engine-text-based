import importlib

import pytest

from solar_topology.study_registry import (
    INITIAL_STUDIES,
    StudyCategory,
    StudyDefinition,
)


def test_package_import_smoke():
    package = importlib.import_module("solar_topology")
    assert package is not None


def test_initial_studies_have_sorted_unique_contract_fields():
    for definition in INITIAL_STUDIES:
        assert definition.required_input_ids == tuple(
            sorted(set(definition.required_input_ids))
        ), definition.study_id
        assert definition.required_evidence_roles == tuple(
            sorted(set(definition.required_evidence_roles))
        ), definition.study_id


@pytest.mark.parametrize(
    ("field_name", "values"),
    [
        ("required_input_ids", ("z-input", "a-input")),
        ("required_input_ids", ("a-input", "a-input")),
        ("required_evidence_roles", ("z-role", "a-role")),
        ("required_evidence_roles", ("a-role", "a-role")),
    ],
)
def test_malformed_definition_reports_study_and_field(field_name, values):
    kwargs = {field_name: values}
    with pytest.raises(ValueError) as exc_info:
        StudyDefinition(
            study_id="malformed-study",
            category=StudyCategory.EVIDENCE,
            title="Malformed study fixture",
            method_reference="test:build-020",
            **kwargs,
        )

    message = str(exc_info.value)
    assert "malformed-study" in message
    assert field_name in message
    assert "expected=" in message
