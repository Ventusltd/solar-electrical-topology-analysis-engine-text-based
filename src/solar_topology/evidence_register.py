"""Engineering requirement-to-evidence register for V10 assurance outputs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json
from typing import Mapping

from .evidence_boundary import EvidenceSource, assess_publication_boundary
from .identifiers import CanonicalIdentifier


EVIDENCE_REGISTER_SCHEMA_VERSION = "globalgrid2050.solar-dc.evidence-register.v10.1"


class EvidenceMaturity(StrEnum):
    PROVEN = "proven"
    CALCULATED = "calculated"
    MEASURED = "measured"
    OBSERVED = "observed"
    MANUFACTURER_SUPPLIED = "manufacturer_supplied"
    ASSUMED = "assumed"
    HYPOTHESIS = "hypothesis"
    NOT_EVIDENCED = "not_evidenced"


class RequirementStatus(StrEnum):
    SATISFIED = "satisfied"
    PARTIAL = "partial"
    OPEN = "open"
    BLOCKED = "blocked"
    NOT_APPLICABLE = "not_applicable"


@dataclass(frozen=True)
class EvidenceRegisterEntry:
    requirement_id: str
    subject_identifier: CanonicalIdentifier
    requirement_text: str
    source_ids: tuple[str, ...]
    maturity: EvidenceMaturity
    status: RequirementStatus
    method_reference: str | None = None
    verification_reference: str | None = None
    remaining_risk: str | None = None

    def __post_init__(self) -> None:
        for name, value in (
            ("requirement_id", self.requirement_id),
            ("requirement_text", self.requirement_text),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty text")
        if not isinstance(self.subject_identifier, CanonicalIdentifier):
            raise TypeError("subject_identifier must be a CanonicalIdentifier")
        if tuple(sorted(set(self.source_ids))) != self.source_ids:
            raise ValueError("source_ids must be unique and sorted")
        if not isinstance(self.maturity, EvidenceMaturity):
            raise TypeError("maturity must be EvidenceMaturity")
        if not isinstance(self.status, RequirementStatus):
            raise TypeError("status must be RequirementStatus")
        if self.status is RequirementStatus.SATISFIED:
            if self.maturity in {
                EvidenceMaturity.ASSUMED,
                EvidenceMaturity.HYPOTHESIS,
                EvidenceMaturity.NOT_EVIDENCED,
            }:
                raise ValueError("satisfied requirements require stronger evidence maturity")
            if not self.source_ids:
                raise ValueError("satisfied requirements require evidence sources")
        if self.status is RequirementStatus.OPEN and not self.remaining_risk:
            raise ValueError("open requirements must state remaining risk")


@dataclass(frozen=True)
class EngineeringEvidenceRegister:
    register_id: str
    entries: tuple[EvidenceRegisterEntry, ...]
    schema_version: str = EVIDENCE_REGISTER_SCHEMA_VERSION


def build_evidence_register(
    register_id: str,
    entries: tuple[EvidenceRegisterEntry, ...] | list[EvidenceRegisterEntry],
    sources: Mapping[str, EvidenceSource],
    *,
    public_export: bool = False,
) -> EngineeringEvidenceRegister:
    if not isinstance(register_id, str) or not register_id.strip():
        raise ValueError("register_id must be non-empty text")
    ordered = tuple(sorted(entries, key=lambda item: item.requirement_id))
    ids = [entry.requirement_id for entry in ordered]
    if len(ids) != len(set(ids)):
        raise ValueError("requirement_id values must be unique")
    for entry in ordered:
        missing = [source_id for source_id in entry.source_ids if source_id not in sources]
        if missing:
            raise ValueError(f"entry references unknown sources: {missing}")
        if public_export and entry.source_ids:
            decision = assess_publication_boundary(
                [sources[source_id] for source_id in entry.source_ids]
            )
            if not decision.publishable or decision.restricted_source_ids:
                raise PermissionError(
                    f"public evidence entry {entry.requirement_id!r} contains restricted evidence"
                )
    return EngineeringEvidenceRegister(register_id=register_id, entries=ordered)


def evidence_register_payload(register: EngineeringEvidenceRegister) -> dict[str, object]:
    return {
        "schema_version": register.schema_version,
        "register_id": register.register_id,
        "entries": [
            {
                "requirement_id": entry.requirement_id,
                "subject_identifier": entry.subject_identifier.value,
                "requirement_text": entry.requirement_text,
                "source_ids": list(entry.source_ids),
                "maturity": entry.maturity.value,
                "status": entry.status.value,
                "method_reference": entry.method_reference,
                "verification_reference": entry.verification_reference,
                "remaining_risk": entry.remaining_risk,
            }
            for entry in register.entries
        ],
    }


def evidence_register_json(register: EngineeringEvidenceRegister) -> str:
    return json.dumps(
        evidence_register_payload(register),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def evidence_register_hash(register: EngineeringEvidenceRegister) -> str:
    digest = hashlib.sha256(evidence_register_json(register).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"
