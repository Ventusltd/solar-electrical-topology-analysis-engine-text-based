from __future__ import annotations

import hashlib
import json

import pytest

import solar_topology as api
import solar_topology.resistance_qualification as qualification
from solar_topology.products import EXTERNAL_STRING_6MM2, FACTORY_LEAD_4MM2


PUBLIC_NAMES = (
    "RESISTANCE_QUALIFICATION_SCHEMA_VERSION",
    "ResistanceSourceAssessment",
    "ResistanceSourceStatus",
    "assess_resistance_source",
    "resistance_source_assessment_hash",
    "resistance_source_assessment_json",
    "resistance_source_assessment_payload",
)


def test_resistance_qualification_is_exposed_by_supported_package_api() -> None:
    assert api.RESISTANCE_QUALIFICATION_SCHEMA_VERSION == (
        qualification.RESISTANCE_QUALIFICATION_SCHEMA_VERSION
    )
    assert api.ResistanceSourceAssessment is qualification.ResistanceSourceAssessment
    assert api.ResistanceSourceStatus is qualification.ResistanceSourceStatus
    assert api.assess_resistance_source is qualification.assess_resistance_source
    assert (
        api.resistance_source_assessment_payload
        is qualification.resistance_source_assessment_payload
    )
    assert (
        api.resistance_source_assessment_json
        is qualification.resistance_source_assessment_json
    )
    assert (
        api.resistance_source_assessment_hash
        is qualification.resistance_source_assessment_hash
    )
    assert all(name in api.__all__ for name in PUBLIC_NAMES)


def test_resistance_qualification_exports_are_explicitly_provisional() -> None:
    for name in PUBLIC_NAMES:
        assert api.public_api_status(name) == api.ApiStatus.PROVISIONAL
        assert name in api.explicitly_classified_public_names()


def test_generic_standard_records_remain_candidate_through_public_api() -> None:
    for product in (FACTORY_LEAD_4MM2, EXTERNAL_STRING_6MM2):
        assessment = api.assess_resistance_source(product.resolved_resistance)

        assert assessment.status == api.ResistanceSourceStatus.CANDIDATE
        assert not assessment.promotable
        assert assessment.record_hash is not None
        assert assessment.record_hash.startswith("sha256:")
        assert assessment.reasons == (
            "SOURCE_REVISION_PLACEHOLDER",
            "VERIFICATION_NOT_VERIFIED",
        )
        with pytest.raises(ValueError, match="not verified"):
            assessment.require_verified()


def test_assessment_serialisation_is_exact_through_public_api() -> None:
    for product in (FACTORY_LEAD_4MM2, EXTERNAL_STRING_6MM2):
        assessment = api.assess_resistance_source(product.resolved_resistance)
        expected_payload = {
            "schema_version": assessment.schema_version,
            "record_hash": assessment.record_hash,
            "status": str(assessment.status),
            "reasons": list(assessment.reasons),
        }
        expected_json = json.dumps(
            expected_payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        expected_hash = "sha256:" + hashlib.sha256(
            expected_json.encode("utf-8")
        ).hexdigest()

        assert api.resistance_source_assessment_payload(assessment) == expected_payload
        assert api.resistance_source_assessment_json(assessment) == expected_json
        assert api.resistance_source_assessment_hash(assessment) == expected_hash
        assert qualification.resistance_source_assessment_payload(
            assessment
        ) == expected_payload
        assert qualification.resistance_source_assessment_json(
            assessment
        ) == expected_json
        assert qualification.resistance_source_assessment_hash(
            assessment
        ) == expected_hash
