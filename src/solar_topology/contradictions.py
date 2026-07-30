"""Deterministic contradiction register for evidence-bearing V10 claims."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json

from .identifiers import CanonicalIdentifier


CONTRADICTION_SCHEMA_VERSION = "globalgrid2050.solar-dc.contradictions.v10.1"


class ContradictionStatus(StrEnum):
    OPEN = "open"
    RESOLVED = "resolved"
    ACCEPTED_UNCERTAINTY = "accepted_uncertainty"
    REJECTED = "rejected"


class ContradictionSeverity(StrEnum):
    INFORMATIONAL = "informational"
    MATERIAL = "material"
    SAFETY_CRITICAL = "safety_critical"


@dataclass(frozen=True)
class Claim:
    claim_id: str
    subject_identifier: CanonicalIdentifier
    predicate: str
    value: str | int | float | bool | None
    unit: str | None
    source_id: str

    def __post_init__(self) -> None:
        for name, value in (
            ("claim_id", self.claim_id),
            ("predicate", self.predicate),
            ("source_id", self.source_id),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty text")
        if self.unit is not None and (not isinstance(self.unit, str) or not self.unit.strip()):
            raise ValueError("unit must be non-empty text when supplied")


@dataclass(frozen=True)
class Contradiction:
    contradiction_id: str
    left: Claim
    right: Claim
    severity: ContradictionSeverity
    status: ContradictionStatus = ContradictionStatus.OPEN
    resolution_note: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.contradiction_id, str) or not self.contradiction_id.strip():
            raise ValueError("contradiction_id must be non-empty text")
        if self.left.claim_id == self.right.claim_id:
            raise ValueError("a contradiction requires two distinct claims")
        if self.left.subject_identifier != self.right.subject_identifier:
            raise ValueError("contradictory claims must concern the same subject")
        if self.left.predicate != self.right.predicate:
            raise ValueError("contradictory claims must concern the same predicate")
        if self.left.unit != self.right.unit:
            raise ValueError("contradictory claims must use the same unit")
        if self.left.value == self.right.value:
            raise ValueError("equal claim values do not form a contradiction")
        if self.status is not ContradictionStatus.OPEN and not self.resolution_note:
            raise ValueError("closed contradictions require a resolution_note")


@dataclass(frozen=True)
class ContradictionRegister:
    contradictions: tuple[Contradiction, ...]
    schema_version: str = CONTRADICTION_SCHEMA_VERSION


def build_contradiction_register(
    contradictions: tuple[Contradiction, ...] | list[Contradiction],
) -> ContradictionRegister:
    ordered = tuple(sorted(contradictions, key=lambda item: item.contradiction_id))
    ids = [item.contradiction_id for item in ordered]
    if len(ids) != len(set(ids)):
        raise ValueError("contradiction identifiers must be unique")
    claim_pairs = [tuple(sorted((item.left.claim_id, item.right.claim_id))) for item in ordered]
    if len(claim_pairs) != len(set(claim_pairs)):
        raise ValueError("the same claim pair cannot be registered twice")
    return ContradictionRegister(contradictions=ordered)


def contradiction_register_payload(register: ContradictionRegister) -> dict[str, object]:
    def claim_payload(claim: Claim) -> dict[str, object]:
        return {
            "claim_id": claim.claim_id,
            "subject_identifier": claim.subject_identifier.value,
            "predicate": claim.predicate,
            "value": claim.value,
            "unit": claim.unit,
            "source_id": claim.source_id,
        }

    return {
        "schema_version": register.schema_version,
        "contradictions": [
            {
                "contradiction_id": item.contradiction_id,
                "left": claim_payload(item.left),
                "right": claim_payload(item.right),
                "severity": item.severity.value,
                "status": item.status.value,
                "resolution_note": item.resolution_note,
            }
            for item in register.contradictions
        ],
    }


def contradiction_register_json(register: ContradictionRegister) -> str:
    return json.dumps(
        contradiction_register_payload(register),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def contradiction_register_hash(register: ContradictionRegister) -> str:
    digest = hashlib.sha256(contradiction_register_json(register).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def unresolved_contradictions(
    register: ContradictionRegister,
    *,
    minimum_severity: ContradictionSeverity | None = None,
) -> tuple[Contradiction, ...]:
    rank = {
        ContradictionSeverity.INFORMATIONAL: 1,
        ContradictionSeverity.MATERIAL: 2,
        ContradictionSeverity.SAFETY_CRITICAL: 3,
    }
    threshold = rank[minimum_severity] if minimum_severity is not None else 1
    return tuple(
        item
        for item in register.contradictions
        if item.status is ContradictionStatus.OPEN and rank[item.severity] >= threshold
    )
