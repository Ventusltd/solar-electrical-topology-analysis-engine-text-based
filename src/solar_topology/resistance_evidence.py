"""Evidence-bound finished-conductor resistance records for V10 calculations.

This module deliberately has no import-time dependency on the circuit or segment
models. Product records are created while ``segments`` is importing; importing
``circuit`` here would therefore create a cycle. Circuit evidence enums are
resolved lazily only when downstream calculation code asks for them.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
import hashlib
import json
import math
from typing import Iterable


RESISTANCE_EVIDENCE_SCHEMA_VERSION = (
    "globalgrid2050.solar-dc.resistance-evidence.v10.1"
)
RESISTANCE_REGISTRY_VERSION = (
    "globalgrid2050.solar-dc.resistance-registry.v10.1"
)


class ResistanceBasis(StrEnum):
    INDEPENDENTLY_MEASURED = "independently_measured"
    MANUFACTURER_DECLARED = "manufacturer_declared"
    STANDARD_MAXIMUM = "standard_maximum"
    IDEAL_BULK_ESTIMATE = "ideal_bulk_estimate"
    ASSUMED = "assumed"
    UNRESOLVED = "unresolved"


class ResistanceValueKind(StrEnum):
    MEASURED = "measured"
    MANUFACTURER_NOMINAL = "manufacturer_nominal"
    MANUFACTURER_MAXIMUM = "manufacturer_maximum"
    STANDARD_MAXIMUM = "standard_maximum"
    LOWER_BOUND_ESTIMATE = "lower_bound_estimate"
    ASSUMED = "assumed"
    UNRESOLVED = "unresolved"


_BASIS_EVIDENCE_CLASS_VALUE = {
    ResistanceBasis.INDEPENDENTLY_MEASURED: "field_measured",
    ResistanceBasis.MANUFACTURER_DECLARED: "manufacturer_declared",
    ResistanceBasis.STANDARD_MAXIMUM: "external_reference",
    ResistanceBasis.IDEAL_BULK_ESTIMATE: "assumed",
    ResistanceBasis.ASSUMED: "assumed",
    ResistanceBasis.UNRESOLVED: "assumed",
}

_ALLOWED_VALUE_KINDS = {
    ResistanceBasis.INDEPENDENTLY_MEASURED: {
        ResistanceValueKind.MEASURED,
    },
    ResistanceBasis.MANUFACTURER_DECLARED: {
        ResistanceValueKind.MANUFACTURER_NOMINAL,
        ResistanceValueKind.MANUFACTURER_MAXIMUM,
    },
    ResistanceBasis.STANDARD_MAXIMUM: {
        ResistanceValueKind.STANDARD_MAXIMUM,
    },
    ResistanceBasis.IDEAL_BULK_ESTIMATE: {
        ResistanceValueKind.LOWER_BOUND_ESTIMATE,
    },
    ResistanceBasis.ASSUMED: {
        ResistanceValueKind.ASSUMED,
    },
    ResistanceBasis.UNRESOLVED: {
        ResistanceValueKind.UNRESOLVED,
    },
}


@dataclass(frozen=True)
class ResolvedConductorResistance:
    product_id: str
    r20_ohm_per_m: float
    basis: ResistanceBasis
    value_kind: ResistanceValueKind
    source_reference: str
    source_revision: str
    verification_state: str
    temperature_coefficient_per_c: float = 0.00393
    temperature_coefficient_basis: str = "copper_linear_20c"
    measurement_conditions: str | None = None
    warnings: tuple[str, ...] = ()
    schema_version: str = RESISTANCE_EVIDENCE_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not self.product_id.strip():
            raise ValueError("resistance evidence requires product_id")
        if (
            not isinstance(self.r20_ohm_per_m, (int, float))
            or isinstance(self.r20_ohm_per_m, bool)
            or not math.isfinite(float(self.r20_ohm_per_m))
            or self.r20_ohm_per_m <= 0
        ):
            raise ValueError("r20_ohm_per_m must be finite and positive")
        if not isinstance(self.basis, ResistanceBasis):
            raise TypeError("basis must be a ResistanceBasis")
        if not isinstance(self.value_kind, ResistanceValueKind):
            raise TypeError("value_kind must be a ResistanceValueKind")
        if self.value_kind not in _ALLOWED_VALUE_KINDS[self.basis]:
            raise ValueError(
                f"{self.value_kind} is incompatible with resistance basis {self.basis}"
            )
        if not self.source_reference.strip():
            raise ValueError("resistance evidence requires source_reference")
        if not self.source_revision.strip():
            raise ValueError("resistance evidence requires source_revision")
        if not isinstance(self.verification_state, str) or not str(
            self.verification_state
        ).strip():
            raise ValueError("verification_state must be non-empty text")
        if (
            not isinstance(self.temperature_coefficient_per_c, (int, float))
            or isinstance(self.temperature_coefficient_per_c, bool)
            or not math.isfinite(float(self.temperature_coefficient_per_c))
            or self.temperature_coefficient_per_c <= 0
        ):
            raise ValueError(
                "temperature_coefficient_per_c must be finite and positive"
            )
        if not self.temperature_coefficient_basis.strip():
            raise ValueError(
                "temperature_coefficient_basis must be non-empty text"
            )
        if self.measurement_conditions is not None and not (
            isinstance(self.measurement_conditions, str)
            and self.measurement_conditions.strip()
        ):
            raise ValueError(
                "measurement_conditions must be non-empty text when supplied"
            )
        if any(not isinstance(warning, str) or not warning for warning in self.warnings):
            raise ValueError("resistance warnings must be non-empty text")

    @property
    def evidence_class(self):
        """Return the circuit EvidenceClass without creating an import cycle."""

        from .circuit import EvidenceClass

        return EvidenceClass(_BASIS_EVIDENCE_CLASS_VALUE[self.basis])

    @property
    def legacy_provenance(self) -> str:
        if self.basis is ResistanceBasis.INDEPENDENTLY_MEASURED:
            return "measured"
        if self.basis is ResistanceBasis.MANUFACTURER_DECLARED:
            return "oem_declared"
        return "assumed"


def resistance_evidence_payload(
    record: ResolvedConductorResistance,
) -> dict[str, object]:
    return {
        "schema_version": record.schema_version,
        "product_id": record.product_id,
        "r20_ohm_per_m": record.r20_ohm_per_m,
        "basis": str(record.basis),
        "value_kind": str(record.value_kind),
        "evidence_class": str(record.evidence_class),
        "source_reference": record.source_reference,
        "source_revision": record.source_revision,
        "verification_state": str(record.verification_state),
        "temperature_coefficient_per_c": (
            record.temperature_coefficient_per_c
        ),
        "temperature_coefficient_basis": (
            record.temperature_coefficient_basis
        ),
        "measurement_conditions": record.measurement_conditions,
        "warnings": list(record.warnings),
    }


def resistance_evidence_json(
    record: ResolvedConductorResistance,
) -> str:
    return json.dumps(
        resistance_evidence_payload(record),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def resistance_evidence_hash(
    record: ResolvedConductorResistance,
) -> str:
    digest = hashlib.sha256(
        resistance_evidence_json(record).encode("utf-8")
    ).hexdigest()
    return f"sha256:{digest}"


def resistance_records_payload(
    records: Iterable[ResolvedConductorResistance],
) -> dict[str, object]:
    unique = {
        resistance_evidence_hash(record): record
        for record in records
    }
    return {
        "registry_version": RESISTANCE_REGISTRY_VERSION,
        "scope": "applied_records_only",
        "records": [
            resistance_evidence_payload(unique[record_hash])
            for record_hash in sorted(unique)
        ],
    }


def resistance_records_hash(
    records: Iterable[ResolvedConductorResistance],
) -> str:
    encoded = json.dumps(
        resistance_records_payload(records),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


_REGISTRY: dict[str, ResolvedConductorResistance] = {}


def register_conductor_resistance(
    record: ResolvedConductorResistance,
) -> ResolvedConductorResistance:
    existing = _REGISTRY.get(record.product_id)
    if existing is not None and existing != record:
        raise ValueError(
            f"resistance registry already contains a different record for {record.product_id!r}"
        )
    _REGISTRY[record.product_id] = record
    return record


def registered_conductor_resistance(
    product_id: str,
) -> ResolvedConductorResistance | None:
    return _REGISTRY.get(product_id)


def resistance_registry_payload() -> dict[str, object]:
    return {
        "registry_version": RESISTANCE_REGISTRY_VERSION,
        "scope": "all_registered_records",
        "records": [
            resistance_evidence_payload(_REGISTRY[product_id])
            for product_id in sorted(_REGISTRY)
        ],
    }


def resistance_registry_hash() -> str:
    encoded = json.dumps(
        resistance_registry_payload(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _fallback_basis(
    provenance: str,
) -> tuple[ResistanceBasis, ResistanceValueKind, str]:
    if provenance == "measured":
        return (
            ResistanceBasis.INDEPENDENTLY_MEASURED,
            ResistanceValueKind.MEASURED,
            "unverified",
        )
    if provenance == "oem_declared":
        return (
            ResistanceBasis.MANUFACTURER_DECLARED,
            ResistanceValueKind.MANUFACTURER_NOMINAL,
            "unverified",
        )
    return (
        ResistanceBasis.ASSUMED,
        ResistanceValueKind.ASSUMED,
        "unverified",
    )


def resolve_conductor_resistance(
    *,
    product_id: str,
    r20_ohm_per_m: float,
    legacy_provenance: str,
    legacy_source_reference: str,
) -> ResolvedConductorResistance:
    registered = registered_conductor_resistance(product_id)
    if registered is not None and math.isclose(
        registered.r20_ohm_per_m,
        r20_ohm_per_m,
        rel_tol=0.0,
        abs_tol=1e-15,
    ):
        return registered

    basis, value_kind, verification_state = _fallback_basis(
        legacy_provenance
    )
    warnings: tuple[str, ...] = ()
    source_reference = legacy_source_reference or "legacy_segment_value"
    source_revision = "legacy-unversioned"
    if registered is not None:
        basis = ResistanceBasis.ASSUMED
        value_kind = ResistanceValueKind.ASSUMED
        verification_state = "unverified"
        source_reference = (
            f"{source_reference};override-of:{registered.source_reference}"
        )
        source_revision = f"override-of:{registered.source_revision}"
        warnings = (
            "R20 differs from the registered product value; resistance authority downgraded to assumed.",
        )

    return ResolvedConductorResistance(
        product_id=product_id,
        r20_ohm_per_m=float(r20_ohm_per_m),
        basis=basis,
        value_kind=value_kind,
        source_reference=source_reference,
        source_revision=source_revision,
        verification_state=verification_state,
        warnings=warnings,
    )


def strongest_resistance_record(
    records: Iterable[ResolvedConductorResistance],
) -> ResolvedConductorResistance:
    materialised = tuple(records)
    if not materialised:
        raise ValueError("at least one resistance record is required")
    strength = {
        ResistanceBasis.INDEPENDENTLY_MEASURED: 6,
        ResistanceBasis.MANUFACTURER_DECLARED: 5,
        ResistanceBasis.STANDARD_MAXIMUM: 4,
        ResistanceBasis.IDEAL_BULK_ESTIMATE: 3,
        ResistanceBasis.ASSUMED: 2,
        ResistanceBasis.UNRESOLVED: 1,
    }
    return max(materialised, key=lambda record: strength[record.basis])


def with_resistance_warning(
    record: ResolvedConductorResistance,
    warning: str,
) -> ResolvedConductorResistance:
    if not warning:
        raise ValueError("warning must be non-empty text")
    return replace(
        record,
        warnings=tuple(sorted(set((*record.warnings, warning)))),
    )
