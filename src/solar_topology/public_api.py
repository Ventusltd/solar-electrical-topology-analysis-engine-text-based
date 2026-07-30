"""Canonical classification manifest for the package-level public API.

The manifest makes package exports reviewable and gives tests a stable contract
against accidental export drift. Symbols not yet explicitly adjudicated remain
PROVISIONAL rather than silently becoming canonical.
"""

from __future__ import annotations

from enum import StrEnum


PUBLIC_API_SCHEMA_VERSION = "globalgrid2050.solar-dc.public-api.v10.1"


class ApiStatus(StrEnum):
    CANONICAL = "canonical"
    PROVISIONAL = "provisional"
    COMPATIBILITY = "compatibility"


PUBLIC_API_CLASSIFICATION: dict[ApiStatus, tuple[str, ...]] = {
    ApiStatus.CANONICAL: (
        "ALPHA_CU_20_PER_C",
        "CIRCUIT_SCHEMA_VERSION",
        "CALCULATION_RECEIPT_SCHEMA_VERSION",
        "COMPLETE_CIRCUIT_METHOD_VERSION",
        "CircuitModel",
        "CircuitValidationResult",
        "Connection",
        "ConnectionKind",
        "ConductorSpec",
        "EvidenceClass",
        "EvidenceDescriptor",
        "FormationConfig",
        "GeometryConfig",
        "GeometryReceipt",
        "Interval",
        "IssueSeverity",
        "ObjectKind",
        "OperatingState",
        "OrderedCircuitCalculationReceipt",
        "OrderedCircuitTraversal",
        "PhysicalObject",
        "Point3D",
        "Segment",
        "SegmentCalculationResult",
        "SegmentGeometryResult",
        "SegmentInputIntervals",
        "SegmentRow",
        "StringDefinition",
        "StringTopology",
        "Terminal",
        "TerminalPolarity",
        "TopologyInputs",
        "UncertainCircuitCalculationReceipt",
        "ValidationIssue",
        "VerificationState",
        "adapt_segment_chain_to_circuit",
        "build_export",
        "build_leapfrog_circuit",
        "build_sequential_circuit",
        "build_site_model",
        "build_string_segments",
        "calculate_complete_circuit",
        "calculate_complete_circuit_with_uncertainty",
        "calculate_geometry_receipt",
        "canonical_circuit_json",
        "canonical_circuit_payload",
        "canonical_evidence_descriptor",
        "cold_string_voc",
        "dc_resistance",
        "geometry_receipt_hash",
        "geometry_receipt_json",
        "geometry_receipt_payload",
        "stored_electric_energy",
        "stored_magnetic_energy",
        "two_wire_parameters",
        "uncertainty_receipt_hash",
        "uncertainty_receipt_json",
        "uncertainty_receipt_payload",
        "validate_circuit_model",
        "validate_no_user_route_lengths",
        "validated_circuit_hash",
        "verify_ordered_circuit",
    ),
    ApiStatus.PROVISIONAL: (),
    ApiStatus.COMPATIBILITY: (
        "EXTERNAL_STRING_6MM2",
        "FACTORY_LEAD_4MM2",
        "INITIAL_CARTRIDGES",
        "INITIAL_STUDIES",
        "LeapfrogCartridge",
        "SequentialCartridge",
        "TopologyCartridge",
        "build_deterministic_store",
        "build_fleet_segments",
        "build_store",
        "javascript_provenance_descriptor",
        "segment_provenance_descriptor",
        "validate_cross_cartridge_invariants",
        "validate_segment_chains",
    ),
}


def explicitly_classified_public_names() -> tuple[str, ...]:
    """Return explicitly adjudicated names in deterministic order."""

    names = [name for group in PUBLIC_API_CLASSIFICATION.values() for name in group]
    if len(names) != len(set(names)):
        raise ValueError("public API classification contains duplicate symbols")
    return tuple(sorted(names))


def public_api_status(name: str) -> ApiStatus:
    """Return status for a package symbol; unknown names remain provisional."""

    for status, names in PUBLIC_API_CLASSIFICATION.items():
        if name in names:
            return status
    return ApiStatus.PROVISIONAL


def build_public_api_inventory(
    exported_names: tuple[str, ...] | list[str],
) -> tuple[tuple[str, ApiStatus], ...]:
    """Build a deterministic total inventory for supplied package exports."""

    names = tuple(exported_names)
    if len(names) != len(set(names)):
        raise ValueError("package exports contain duplicate symbols")
    return tuple((name, public_api_status(name)) for name in sorted(names))
