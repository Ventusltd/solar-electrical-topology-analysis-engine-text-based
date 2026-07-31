from __future__ import annotations

import pytest

import solar_topology as api
import solar_topology.resistance_qualification as qualification
from solar_topology.products import EXTERNAL_STRING_6MM2, FACTORY_LEAD_4MM2


PUBLIC_NAMES = (
    "RESISTANCE_QUALIFICATION_SCHEMA_VERSION",
    "ResistanceSourceAssessment",
    "ResistanceSourceStatus",
    "assess_resistance_source",
)


def test_resistance_qualification_is_exposed_by_supported_package_api() -> None:
    assert api.RESISTANCE_QUALIFICATION_SCHEMA_VERSION == (
        qualification.RESISTANCE_QUALIFICATION_SCHEMA_VERSION
    )
    assert api.ResistanceSourceAssessment is qualification.ResistanceSourceAssessment
    assert api.ResistanceSourceStatus is qualification.ResistanceSourceStatus
    assert api.assess_resistance_source is qualification.assess_resistance_source
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
