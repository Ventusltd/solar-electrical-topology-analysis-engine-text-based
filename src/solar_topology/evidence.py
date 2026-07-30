"""Canonical evidence vocabulary and source-vocabulary reconciliation for V10."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .circuit import EvidenceClass


EVIDENCE_SCHEMA_VERSION = "globalgrid2050.solar-dc.evidence.v10.1"


class VerificationState(StrEnum):
    UNKNOWN = "unknown"
    UNVERIFIED = "unverified"
    CANDIDATE = "candidate"
    VERIFIED = "verified"
    REJECTED = "rejected"
    RESEARCH_HYPOTHESIS = "research_hypothesis"
    STANDARDS_REVIEW_REQUIRED = "standards_review_required"


@dataclass(frozen=True)
class EvidenceDescriptor:
    evidence_class: EvidenceClass
    verification_state: VerificationState
    source_reference: str | None
    source_vocabulary: str
    source_value: str
    schema_version: str = EVIDENCE_SCHEMA_VERSION


_SEGMENT_PROVENANCE = {
    "measured": (
        EvidenceClass.FIELD_MEASURED,
        VerificationState.UNVERIFIED,
    ),
    "oem_declared": (
        EvidenceClass.MANUFACTURER_DECLARED,
        VerificationState.UNVERIFIED,
    ),
    "assumed": (
        EvidenceClass.ASSUMED,
        VerificationState.UNVERIFIED,
    ),
    "defaulted": (
        EvidenceClass.ASSUMED,
        VerificationState.UNVERIFIED,
    ),
}

_JAVASCRIPT_PROVENANCE = {
    "measured": (
        EvidenceClass.FIELD_MEASURED,
        VerificationState.UNVERIFIED,
    ),
    "datasheet": (
        EvidenceClass.MANUFACTURER_DECLARED,
        VerificationState.UNVERIFIED,
    ),
    "standardsDerived": (
        EvidenceClass.DERIVED,
        VerificationState.STANDARDS_REVIEW_REQUIRED,
    ),
    "geometryDerived": (
        EvidenceClass.DERIVED,
        VerificationState.CANDIDATE,
    ),
    "inherited": (
        EvidenceClass.EXTERNAL_REFERENCE,
        VerificationState.UNVERIFIED,
    ),
    "assumed": (
        EvidenceClass.ASSUMED,
        VerificationState.UNVERIFIED,
    ),
    "researchHypothesis": (
        EvidenceClass.ASSUMED,
        VerificationState.RESEARCH_HYPOTHESIS,
    ),
}

_EVIDENCE_STRENGTH = {
    EvidenceClass.FIELD_MEASURED: 8,
    EvidenceClass.MANUFACTURER_DECLARED: 7,
    EvidenceClass.USER_CREATED: 6,
    EvidenceClass.PUBLIC_OBSERVATION: 5,
    EvidenceClass.EXTERNAL_REFERENCE: 4,
    EvidenceClass.DERIVED: 3,
    EvidenceClass.GENERIC_EXAMPLE: 2,
    EvidenceClass.ASSUMED: 1,
}


def _descriptor(
    mapping: dict[str, tuple[EvidenceClass, VerificationState]],
    value: str,
    *,
    source_reference: str | None,
    source_vocabulary: str,
) -> EvidenceDescriptor:
    try:
        evidence_class, verification_state = mapping[value]
    except KeyError as exc:
        raise ValueError(
            f"unsupported {source_vocabulary} provenance: {value}"
        ) from exc
    return EvidenceDescriptor(
        evidence_class=evidence_class,
        verification_state=verification_state,
        source_reference=source_reference,
        source_vocabulary=source_vocabulary,
        source_value=value,
    )


def segment_provenance_descriptor(
    value: str,
    *,
    source_reference: str | None = None,
) -> EvidenceDescriptor:
    """Map the SegmentRow provenance vocabulary into canonical V10 evidence."""

    return _descriptor(
        _SEGMENT_PROVENANCE,
        value,
        source_reference=source_reference,
        source_vocabulary="topology_segments_v1",
    )


def javascript_provenance_descriptor(
    value: str,
    *,
    source_reference: str | None = None,
) -> EvidenceDescriptor:
    """Map V10 JavaScript quantity provenance without promoting authority."""

    return _descriptor(
        _JAVASCRIPT_PROVENANCE,
        value,
        source_reference=source_reference,
        source_vocabulary="v10_javascript_quantity_v1",
    )


def canonical_evidence_descriptor(
    evidence_class: EvidenceClass,
    *,
    verification_state: VerificationState = VerificationState.UNVERIFIED,
    source_reference: str | None = None,
) -> EvidenceDescriptor:
    if not isinstance(evidence_class, EvidenceClass):
        raise TypeError("evidence_class must be an EvidenceClass")
    if not isinstance(verification_state, VerificationState):
        raise TypeError("verification_state must be a VerificationState")
    return EvidenceDescriptor(
        evidence_class=evidence_class,
        verification_state=verification_state,
        source_reference=source_reference,
        source_vocabulary="canonical_v10",
        source_value=str(evidence_class),
    )


def weakest_evidence_class(
    evidence_classes: tuple[EvidenceClass, ...] | list[EvidenceClass],
) -> EvidenceClass:
    """Return the least-supported class without rewriting any source class."""

    if not evidence_classes:
        raise ValueError("at least one evidence class is required")
    invalid = [
        value
        for value in evidence_classes
        if not isinstance(value, EvidenceClass)
    ]
    if invalid:
        raise TypeError("all evidence classes must be EvidenceClass values")
    return min(evidence_classes, key=lambda value: _EVIDENCE_STRENGTH[value])
