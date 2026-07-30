"""Canonical classification manifest for the package-level public API.

The manifest is deliberately declarative.  It makes package exports reviewable
without importing optional implementation modules and gives tests a stable
contract against accidental export drift.
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
    ApiStatus.PROVISIONAL: (
        "AcceptanceCriterion",
        "CanonicalIdentifier",
        "Claim",
        "Contradiction",
        "ContradictionRegister",
        "ContradictionSeverity",
        "ContradictionStatus",
        "CriterionOperator",
        "Diagnostic",
        "DiagnosticCategory",
        "DiagnosticReport",
        "DiagnosticSeverity",
        "EngineeringEvidenceRegister",
        "EntityLevel",
        "EvidenceMaturity",
        "EvidenceRegisterEntry",
        "EvidenceSource",
        "PersistedRecord",
        "PublicationDecision",
        "PublicationPermission",
        "PublicTopologyManifest",
        "PublicTopologyRecord",
        "RequirementStatus",
        "RightsStatus",
        "StudyApplicability",
        "StudyAssessment",
        "StudyCategory",
        "StudyCoverage",
        "StudyDefinition",
        "StudyKind",
        "StudyRegistry",
        "StudyState",
        "build_contradiction_register",
        "build_diagnostic_report",
        "build_evidence_register",
        "build_public_topology_manifest",
        "build_study_applicability",
        "build_study_registry",
        "evaluate_criterion",
        "public_topology_hash",
        "public_topology_json",
        "public_topology_payload",
        "study_registry_hash",
        "study_registry_json",
        "study_registry_payload",
    ),
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


def classified_public_names() -> tuple[str, ...]:
    """Return all classified names in deterministic sorted order."""

    names = [name for group in PUBLIC_API_CLASSIFICATION.values() for name in group]
    if len(names) != len(set(names)):
        raise ValueError("public API classification contains duplicate symbols")
    return tuple(sorted(names))


def public_api_status(name: str) -> ApiStatus | None:
    """Return the declared status for one package-level symbol."""

    for status, names in PUBLIC_API_CLASSIFICATION.items():
        if name in names:
            return status
    return None
