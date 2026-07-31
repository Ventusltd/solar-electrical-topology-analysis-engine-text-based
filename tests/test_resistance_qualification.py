from __future__ import annotations

from dataclasses import replace
import json

import pytest

from solar_topology.products import EXTERNAL_STRING_6MM2, FACTORY_LEAD_4MM2
from solar_topology.resistance_evidence import (
    ResistanceBasis,
    ResistanceValueKind,
    ResolvedConductorResistance,
)
from solar_topology.resistance_qualification import (
    RESISTANCE_QUALIFICATION_SCHEMA_VERSION,
    ResistanceSourceAssessment,
    ResistanceSourceStatus,
    assess_resistance_source,
    resistance_source_assessment_hash,
    resistance_source_assessment_json,
    resistance_source_assessment_payload,
)


def _record(
    *,
    basis: ResistanceBasis,
    value_kind: ResistanceValueKind,
    verification_state: str = "verified",
    source_revision: str = "rev-2026-07-31",
    measurement_conditions: str | None = None,
) -> ResolvedConductorResistance:
    return ResolvedConductorResistance(
        product_id="qualification-test-product",
        r20_ohm_per_m=0.003,
        basis=basis,
        value_kind=value_kind,
        source_reference="revision-controlled-test-source",
        source_revision=source_revision,
        verification_state=verification_state,
        measurement_conditions=measurement_conditions,
    )


def test_current_generic_standard_records_remain_candidates() -> None:
    for product in (FACTORY_LEAD_4MM2, EXTERNAL_STRING_6MM2):
        assessment = assess_resistance_source(product.resolved_resistance)

        assert assessment.status == ResistanceSourceStatus.CANDIDATE
        assert not assessment.promotable
        assert assessment.record_hash is not None
        assert assessment.reasons == (
            "SOURCE_REVISION_PLACEHOLDER",
            "VERIFICATION_NOT_VERIFIED",
        )


def test_revision_controlled_verified_manufacturer_record_is_promotable() -> None:
    record = _record(
        basis=ResistanceBasis.MANUFACTURER_DECLARED,
        value_kind=ResistanceValueKind.MANUFACTURER_MAXIMUM,
    )

    assessment = assess_resistance_source(record)

    assert assessment.status == ResistanceSourceStatus.VERIFIED
    assert assessment.promotable
    assert assessment.reasons == ()
    assessment.require_verified()


def test_measured_record_requires_measurement_conditions() -> None:
    incomplete = _record(
        basis=ResistanceBasis.INDEPENDENTLY_MEASURED,
        value_kind=ResistanceValueKind.MEASURED,
    )
    complete = _record(
        basis=ResistanceBasis.INDEPENDENTLY_MEASURED,
        value_kind=ResistanceValueKind.MEASURED,
        measurement_conditions=(
            "20.0 C conductor temperature; four-wire measurement; calibrated meter"
        ),
    )

    incomplete_assessment = assess_resistance_source(incomplete)
    complete_assessment = assess_resistance_source(complete)

    assert incomplete_assessment.status == ResistanceSourceStatus.CANDIDATE
    assert incomplete_assessment.reasons == (
        "MEASUREMENT_CONDITIONS_MISSING",
    )
    assert complete_assessment.status == ResistanceSourceStatus.VERIFIED


def test_assumed_and_ideal_bulk_records_cannot_be_promoted() -> None:
    for basis, value_kind in (
        (ResistanceBasis.ASSUMED, ResistanceValueKind.ASSUMED),
        (
            ResistanceBasis.IDEAL_BULK_ESTIMATE,
            ResistanceValueKind.LOWER_BOUND_ESTIMATE,
        ),
    ):
        assessment = assess_resistance_source(
            _record(basis=basis, value_kind=value_kind)
        )

        assert assessment.status == ResistanceSourceStatus.CANDIDATE
        assert assessment.reasons == ("BASIS_NOT_PROMOTABLE",)
        with pytest.raises(ValueError, match="not verified"):
            assessment.require_verified()


def test_unresolved_or_explicitly_rejected_source_is_rejected() -> None:
    unresolved = _record(
        basis=ResistanceBasis.UNRESOLVED,
        value_kind=ResistanceValueKind.UNRESOLVED,
        verification_state="unknown",
        source_revision="unresolved",
    )
    rejected = _record(
        basis=ResistanceBasis.MANUFACTURER_DECLARED,
        value_kind=ResistanceValueKind.MANUFACTURER_NOMINAL,
        verification_state="rejected",
    )

    unresolved_assessment = assess_resistance_source(unresolved)
    rejected_assessment = assess_resistance_source(rejected)

    assert unresolved_assessment.status == ResistanceSourceStatus.REJECTED
    assert "UNRESOLVED_RESISTANCE_BASIS" in unresolved_assessment.reasons
    assert "UNRESOLVED_RESISTANCE_VALUE_KIND" in unresolved_assessment.reasons
    assert rejected_assessment.status == ResistanceSourceStatus.REJECTED
    assert "SOURCE_EXPLICITLY_REJECTED" in rejected_assessment.reasons


def test_invalid_object_is_rejected_without_hash() -> None:
    assessment = assess_resistance_source(object())  # type: ignore[arg-type]

    assert assessment.status == ResistanceSourceStatus.REJECTED
    assert assessment.record_hash is None
    assert assessment.reasons == ("INVALID_RESISTANCE_RECORD_TYPE",)


def test_assessment_payload_json_and_hash_are_deterministic() -> None:
    assessment = assess_resistance_source(
        EXTERNAL_STRING_6MM2.resolved_resistance
    )
    expected = {
        "schema_version": RESISTANCE_QUALIFICATION_SCHEMA_VERSION,
        "record_hash": assessment.record_hash,
        "status": "candidate",
        "reasons": [
            "SOURCE_REVISION_PLACEHOLDER",
            "VERIFICATION_NOT_VERIFIED",
        ],
    }

    assert resistance_source_assessment_payload(assessment) == expected
    assert resistance_source_assessment_json(assessment) == json.dumps(
        expected,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    first_hash = resistance_source_assessment_hash(assessment)
    second_hash = resistance_source_assessment_hash(assessment)
    assert first_hash == second_hash
    assert first_hash.startswith("sha256:")
    assert len(first_hash) == len("sha256:") + 64


def test_assessment_hash_binds_all_qualification_fields() -> None:
    base = assess_resistance_source(
        _record(
            basis=ResistanceBasis.MANUFACTURER_DECLARED,
            value_kind=ResistanceValueKind.MANUFACTURER_MAXIMUM,
        )
    )
    variants = (
        base,
        replace(base, schema_version="qualification-schema-test-v2"),
        replace(base, record_hash="sha256:" + "a" * 64),
        replace(base, status=ResistanceSourceStatus.CANDIDATE),
        replace(base, reasons=("VERIFICATION_NOT_VERIFIED",)),
    )

    assert len(
        {resistance_source_assessment_hash(item) for item in variants}
    ) == len(variants)


@pytest.mark.parametrize(
    "function",
    (
        resistance_source_assessment_payload,
        resistance_source_assessment_json,
        resistance_source_assessment_hash,
    ),
)
def test_assessment_serialisation_rejects_invalid_type(function) -> None:
    with pytest.raises(
        TypeError,
        match="assessment must be a ResistanceSourceAssessment",
    ):
        function(object())  # type: ignore[arg-type]


def test_assessment_dataclass_can_be_serialised_directly() -> None:
    assessment = ResistanceSourceAssessment(
        status=ResistanceSourceStatus.REJECTED,
        record_hash=None,
        reasons=("INVALID_RESISTANCE_RECORD_TYPE",),
    )

    assert resistance_source_assessment_payload(assessment)["record_hash"] is None
    assert resistance_source_assessment_hash(assessment).startswith("sha256:")
