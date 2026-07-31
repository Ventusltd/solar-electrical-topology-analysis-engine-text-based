"""Deterministic promotion gate for conductor-resistance evidence sources.

This module assesses source qualification only. It does not modify conductor
values, calculation arithmetic, topology hashes or existing evidence records.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json

from .resistance_evidence import (
    ResistanceBasis,
    ResistanceValueKind,
    ResolvedConductorResistance,
    resistance_evidence_hash,
)


RESISTANCE_QUALIFICATION_SCHEMA_VERSION = (
    "globalgrid2050.solar-dc.resistance-source-qualification.v10.1"
)


class ResistanceSourceStatus(StrEnum):
    VERIFIED = "verified"
    CANDIDATE = "candidate"
    REJECTED = "rejected"


@dataclass(frozen=True)
class ResistanceSourceAssessment:
    status: ResistanceSourceStatus
    record_hash: str | None
    reasons: tuple[str, ...]
    schema_version: str = RESISTANCE_QUALIFICATION_SCHEMA_VERSION

    @property
    def promotable(self) -> bool:
        return self.status is ResistanceSourceStatus.VERIFIED

    def require_verified(self) -> None:
        if not self.promotable:
            raise ValueError(
                "resistance source is not verified: "
                + ", ".join(self.reasons)
            )


def resistance_source_assessment_payload(
    assessment: ResistanceSourceAssessment,
) -> dict[str, object]:
    """Return the deterministic machine-readable assessment payload."""

    if not isinstance(assessment, ResistanceSourceAssessment):
        raise TypeError("assessment must be a ResistanceSourceAssessment")
    return {
        "schema_version": assessment.schema_version,
        "record_hash": assessment.record_hash,
        "status": str(assessment.status),
        "reasons": list(assessment.reasons),
    }


def resistance_source_assessment_json(
    assessment: ResistanceSourceAssessment,
) -> str:
    """Return canonical JSON without runtime-dependent metadata."""

    return json.dumps(
        resistance_source_assessment_payload(assessment),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def resistance_source_assessment_hash(
    assessment: ResistanceSourceAssessment,
) -> str:
    """Hash schema, source record, status and deterministic reason codes."""

    digest = hashlib.sha256(
        resistance_source_assessment_json(assessment).encode("utf-8")
    ).hexdigest()
    return f"sha256:{digest}"


_PLACEHOLDER_REVISIONS = {
    "edition-not-yet-encoded",
    "legacy-unversioned",
    "unknown",
    "unresolved",
}

_VERIFIABLE_BASES = {
    ResistanceBasis.INDEPENDENTLY_MEASURED,
    ResistanceBasis.MANUFACTURER_DECLARED,
    ResistanceBasis.STANDARD_MAXIMUM,
}


def assess_resistance_source(
    record: ResolvedConductorResistance,
) -> ResistanceSourceAssessment:
    """Assess whether a resistance source may be promoted as verified.

    Candidate records remain usable in visibly provisional calculations. This
    gate controls evidence promotion only and never invents missing source data.
    """

    if not isinstance(record, ResolvedConductorResistance):
        return ResistanceSourceAssessment(
            status=ResistanceSourceStatus.REJECTED,
            record_hash=None,
            reasons=("INVALID_RESISTANCE_RECORD_TYPE",),
        )

    rejected: set[str] = set()
    candidate: set[str] = set()
    verification_state = str(record.verification_state)
    revision = record.source_revision.strip().lower()

    if record.basis is ResistanceBasis.UNRESOLVED:
        rejected.add("UNRESOLVED_RESISTANCE_BASIS")
    if record.value_kind is ResistanceValueKind.UNRESOLVED:
        rejected.add("UNRESOLVED_RESISTANCE_VALUE_KIND")
    if verification_state == "rejected":
        rejected.add("SOURCE_EXPLICITLY_REJECTED")

    if record.basis not in _VERIFIABLE_BASES:
        candidate.add("BASIS_NOT_PROMOTABLE")
    if verification_state != "verified":
        candidate.add("VERIFICATION_NOT_VERIFIED")
    if revision in _PLACEHOLDER_REVISIONS or revision.startswith("override-of:"):
        candidate.add("SOURCE_REVISION_PLACEHOLDER")
    if (
        record.basis is ResistanceBasis.INDEPENDENTLY_MEASURED
        and record.measurement_conditions is None
    ):
        candidate.add("MEASUREMENT_CONDITIONS_MISSING")

    record_hash = resistance_evidence_hash(record)
    if rejected:
        return ResistanceSourceAssessment(
            status=ResistanceSourceStatus.REJECTED,
            record_hash=record_hash,
            reasons=tuple(sorted(rejected | candidate)),
        )
    if candidate:
        return ResistanceSourceAssessment(
            status=ResistanceSourceStatus.CANDIDATE,
            record_hash=record_hash,
            reasons=tuple(sorted(candidate)),
        )
    return ResistanceSourceAssessment(
        status=ResistanceSourceStatus.VERIFIED,
        record_hash=record_hash,
        reasons=(),
    )
