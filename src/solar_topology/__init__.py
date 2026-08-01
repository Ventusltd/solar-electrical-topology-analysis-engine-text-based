"""Solar electrical topology physics, cartridges and fleet data core."""

from .public_api import (
    PUBLIC_API_SCHEMA_VERSION,
    ApiStatus,
    PUBLIC_API_CLASSIFICATION,
    build_public_api_inventory,
    explicitly_classified_public_names,
    public_api_status,
)
from .cartridges import (
    INITIAL_CARTRIDGES,
    LeapfrogCartridge,
    SequentialCartridge,
    TopologyCartridge,
    build_fleet_segments,
    validate_cross_cartridge_invariants,
    validate_segment_chains,
)
from .circuit import (
    CIRCUIT_SCHEMA_VERSION,
    CircuitModel,
    Connection,
    ConnectionKind,
    EvidenceClass,
    ObjectKind,
    PhysicalObject,
    Terminal,
    TerminalPolarity,
    canonical_circuit_json,
    canonical_circuit_payload,
)
from .circuit_adapters import (
    CARTRIDGE_ADAPTER_VERSION,
    adapt_segment_chain_to_circuit,
    build_leapfrog_circuit,
    build_sequential_circuit,
    circuit_boundary_terminal_ids,
    segment_chain_hash,
    source_segment_ids,
)
from .circuit_traversal import (
    TRAVERSAL_SCHEMA_VERSION,
    OrderedCircuitTraversal,
    TraversalIssue,
    verify_ordered_circuit,
)
from .circuit_validation import (
    CircuitValidationResult,
    IssueSeverity,
    ValidationIssue,
    validate_circuit_model,
    validated_circuit_hash,
)
from .diagnostics import (
    DIAGNOSTIC_SCHEMA_VERSION,
    Diagnostic,
    DiagnosticCategory,
    DiagnosticReport,
    DiagnosticSeverity,
    StudyCoverage,
    StudyState,
    build_diagnostic_report,
    coverage_payload,
    diagnostic_from_exception,
    diagnostic_payload,
    diagnostic_report_hash,
    diagnostic_report_json,
    diagnostic_report_payload,
    require_non_blocking,
)
from .diagnostic_adapters import (
    DIAGNOSTIC_ADAPTER_VERSION,
    circuit_validation_diagnostics,
    coverage_for_unperformed_studies,
)
from .diagnostic_bridges import (
    DIAGNOSTIC_BRIDGE_VERSION,
    build_validation_diagnostic_report,
    diagnostics_from_circuit_validation,
    diagnostics_from_traversal,
    guarded_diagnostic_call,
)
from .study_applicability import (
    STUDY_APPLICABILITY_SCHEMA_VERSION,
    AcceptanceCriterion,
    CriterionOperator,
    StudyApplicability,
    StudyKind,
    applicability_coverage,
    build_study_applicability,
    evaluate_criterion,
)
from .study_registry import (
    INITIAL_STUDIES,
    STUDY_REGISTRY_SCHEMA_VERSION,
    StudyAssessment,
    StudyCategory,
    StudyDefinition,
    StudyRegistry,
    assess_study,
    build_study_registry,
    study_registry_hash,
    study_registry_json,
    study_registry_payload,
)
from .evidence import (
    EVIDENCE_SCHEMA_VERSION,
    EvidenceDescriptor,
    VerificationState,
    canonical_evidence_descriptor,
    javascript_provenance_descriptor,
    segment_provenance_descriptor,
    weakest_evidence_class,
)
from .evidence_boundary import (
    EVIDENCE_BOUNDARY_SCHEMA_VERSION,
    EvidenceSource,
    PublicationDecision,
    PublicationPermission,
    RightsStatus,
    assess_publication_boundary,
    require_publication_boundary,
)
from .identifiers import (
    IDENTIFIER_SCHEMA_VERSION,
    CanonicalIdentifier,
    EntityLevel,
    parse_identifier,
    project_id,
    require_unique_identifiers,
)
from .public_topology import (
    PUBLIC_TOPOLOGY_SCHEMA_VERSION,
    PublicTopologyManifest,
    PublicTopologyRecord,
    build_public_topology_manifest,
    public_topology_hash,
    public_topology_json,
    public_topology_payload,
)
from .contradictions import (
    CONTRADICTION_SCHEMA_VERSION,
    Claim,
    Contradiction,
    ContradictionRegister,
    ContradictionSeverity,
    ContradictionStatus,
    build_contradiction_register,
    contradiction_register_hash,
    contradiction_register_json,
    contradiction_register_payload,
    unresolved_contradictions,
)
from .persistence import (
    PERSISTENCE_SCHEMA_VERSION,
    DeterministicStore,
    PersistedRecord,
    build_deterministic_record_store,
    canonical_payload_json,
    deterministic_store_hash,
    deterministic_store_json,
    deterministic_store_payload,
    persist_record,
    read_back_store,
)
from .duckdb_segments import (
    DUCKDB_SEGMENT_SCHEMA_VERSION,
    create_segment_table,
    export_segment_parquet,
    read_segment_parquet,
    read_segment_rows,
    segment_rows_hash,
    segment_rows_payload,
    write_segment_rows,
)
from .evidence_register import (
    EVIDENCE_REGISTER_SCHEMA_VERSION,
    EngineeringEvidenceRegister,
    EvidenceMaturity,
    EvidenceRegisterEntry,
    RequirementStatus,
    build_evidence_register,
    evidence_register_hash,
    evidence_register_json,
    evidence_register_payload,
)
from .geometry_receipts import (
    GEOMETRY_METHOD_VERSION,
    GEOMETRY_RECEIPT_SCHEMA_VERSION,
    GeometryReceipt,
    SegmentGeometryResult,
    calculate_geometry_receipt,
    geometry_receipt_hash,
    geometry_receipt_json,
    geometry_receipt_payload,
)
from .calculation_receipts import (
    CALCULATION_RECEIPT_SCHEMA_VERSION,
    COMPLETE_CIRCUIT_METHOD_VERSION,
    OrderedCircuitCalculationReceipt,
    SegmentCalculationResult,
    calculation_receipt_hash,
    calculation_receipt_json,
    calculation_receipt_payload,
)
from .circuit_calculations import ALPHA_CU_20_PER_C, calculate_complete_circuit
from .uncertainty import (
    UNCERTAINTY_METHOD_VERSION,
    UNCERTAINTY_SCHEMA_VERSION,
    Interval,
    OperatingState,
    SegmentInputIntervals,
    SegmentUncertaintyResult,
    UncertainCircuitCalculationReceipt,
    calculate_complete_circuit_with_uncertainty,
    uncertainty_receipt_hash,
    uncertainty_receipt_json,
    uncertainty_receipt_payload,
)
from .fleet_store import build_deterministic_store, build_store
from .formulas import (
    cold_string_voc,
    dc_resistance,
    stored_electric_energy,
    stored_magnetic_energy,
    two_wire_parameters,
)
from .products import ConductorSpec, EXTERNAL_STRING_6MM2, FACTORY_LEAD_4MM2
from .resistance_qualification import (
    RESISTANCE_QUALIFICATION_SCHEMA_VERSION,
    ResistanceSourceAssessment,
    ResistanceSourceStatus,
    assess_resistance_source,
    resistance_source_assessment_hash,
    resistance_source_assessment_json,
    resistance_source_assessment_payload,
)
from .segments import (
    FeasibilityResult,
    Point3D,
    SegmentRow,
    StringDefinition,
    TopologyInputs,
    archetype_strings,
    fleet_string_definitions,
    string_counts_per_inverter,
)
from .topology import (
    FormationConfig,
    GeometryConfig,
    Segment,
    StringTopology,
    build_export,
    build_site_model,
    build_string_segments,
    validate_no_user_route_lengths,
)

__all__ = [name for name in globals() if not name.startswith("_")]
