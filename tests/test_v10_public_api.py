import solar_topology as engine


def test_v10_evidence_and_calculation_public_api_is_exported():
    required = (
        "EVIDENCE_SCHEMA_VERSION",
        "EvidenceDescriptor",
        "VerificationState",
        "canonical_evidence_descriptor",
        "javascript_provenance_descriptor",
        "segment_provenance_descriptor",
        "weakest_evidence_class",
        "CALCULATION_RECEIPT_SCHEMA_VERSION",
        "COMPLETE_CIRCUIT_METHOD_VERSION",
        "OrderedCircuitCalculationReceipt",
        "SegmentCalculationResult",
        "calculation_receipt_hash",
        "calculation_receipt_json",
        "calculation_receipt_payload",
        "ALPHA_CU_20_PER_C",
        "calculate_complete_circuit",
    )

    missing = [name for name in required if not hasattr(engine, name)]
    assert missing == []
    assert all(name in engine.__all__ for name in required)
