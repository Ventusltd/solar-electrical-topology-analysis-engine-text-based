from dataclasses import replace

import duckdb
import pytest

from solar_topology.cartridges import SequentialCartridge
from solar_topology.circuit import EvidenceClass
from solar_topology.duckdb_segments import (
    export_segment_parquet,
    read_segment_parquet,
    read_segment_rows,
    segment_rows_hash,
    write_segment_rows,
)
from solar_topology.evidence import canonical_evidence_descriptor
from solar_topology.evidence_boundary import (
    EvidenceSource,
    PublicationPermission,
    RightsStatus,
)
from solar_topology.evidence_register import (
    EvidenceMaturity,
    EvidenceRegisterEntry,
    RequirementStatus,
    build_evidence_register,
    evidence_register_hash,
)
from solar_topology.geometry_receipts import (
    calculate_geometry_receipt,
    geometry_receipt_hash,
)
from solar_topology.identifiers import EntityLevel, project_id
from solar_topology.segments import TopologyInputs, archetype_strings


def _rows():
    inputs = TopologyInputs(
        modules_per_string=6,
        inverter_count=1,
        total_site_string_count=24,
        positive_factory_lead_m=1.4,
        negative_factory_lead_m=1.4,
    )
    definition = archetype_strings(inputs)[0]
    return SequentialCartridge().build_segments(inputs, definition)


def _public_source(source_id="public-layout"):
    return EvidenceSource(
        source_id=source_id,
        descriptor=canonical_evidence_descriptor(EvidenceClass.PUBLIC_OBSERVATION),
        rights_status=RightsStatus.PUBLIC,
        publication_permission=PublicationPermission.PUBLIC,
    )


def test_duckdb_round_trip_and_parquet_are_deterministic(tmp_path):
    rows = _rows()
    connection = duckdb.connect(":memory:")
    assert write_segment_rows(connection, reversed(rows)) == len(rows)
    restored = read_segment_rows(connection)
    assert restored == tuple(rows)
    assert segment_rows_hash(restored) == segment_rows_hash(rows)

    path = export_segment_parquet(connection, tmp_path / "segments.parquet")
    from_parquet = read_segment_parquet(path)
    assert from_parquet == tuple(rows)
    assert segment_rows_hash(from_parquet) == segment_rows_hash(rows)


def test_duckdb_primary_key_rejects_duplicate_rows():
    rows = _rows()
    connection = duckdb.connect(":memory:")
    write_segment_rows(connection, rows)
    with pytest.raises(duckdb.ConstraintException):
        write_segment_rows(connection, rows)


def test_evidence_register_requires_strong_evidence_for_satisfied_status():
    project = project_id("public-study")
    site = project.child(EntityLevel.SITE, "site-one")
    source = _public_source()
    entry = EvidenceRegisterEntry(
        requirement_id="ER-E-001",
        subject_identifier=site,
        requirement_text="Record the publicly observable site topology.",
        source_ids=(source.source_id,),
        maturity=EvidenceMaturity.OBSERVED,
        status=RequirementStatus.SATISFIED,
    )
    register = build_evidence_register(
        "register-one", [entry], {source.source_id: source}, public_export=True
    )
    assert evidence_register_hash(register).startswith("sha256:")

    with pytest.raises(ValueError, match="stronger evidence"):
        replace(entry, maturity=EvidenceMaturity.ASSUMED)


def test_public_evidence_register_blocks_restricted_source():
    project = project_id("public-study")
    site = project.child(EntityLevel.SITE, "site-one")
    restricted = EvidenceSource(
        source_id="nda-sld",
        descriptor=canonical_evidence_descriptor(EvidenceClass.EXTERNAL_REFERENCE),
        rights_status=RightsStatus.CONFIDENTIAL_NDA,
        publication_permission=PublicationPermission.INTERNAL_ONLY,
    )
    entry = EvidenceRegisterEntry(
        requirement_id="ER-E-002",
        subject_identifier=site,
        requirement_text="Verify internal single-line diagram details.",
        source_ids=(restricted.source_id,),
        maturity=EvidenceMaturity.OBSERVED,
        status=RequirementStatus.PARTIAL,
        remaining_risk="Not independently supportable from public evidence.",
    )
    with pytest.raises(PermissionError, match="restricted evidence"):
        build_evidence_register(
            "public-register",
            [entry],
            {restricted.source_id: restricted},
            public_export=True,
        )


def test_geometry_receipt_is_deterministic_and_segment_based():
    rows = _rows()
    first = calculate_geometry_receipt(rows)
    second = calculate_geometry_receipt(reversed(rows))
    assert first == second
    assert geometry_receipt_hash(first) == geometry_receipt_hash(second)
    expected = sum(
        row.conductor_length_m * row.separation_mm / 1000 * row.loop_parameter_weight
        for row in rows
    )
    assert first.loop_area_m2 == pytest.approx(expected)
    assert 0 <= first.paired_route_fraction <= 1


def test_geometry_receipt_rejects_mixed_strings_and_index_gaps():
    rows = list(_rows())
    with pytest.raises(ValueError, match="one run, topology and string"):
        calculate_geometry_receipt(
            [rows[0], replace(rows[1], string_id="different-string")]
        )
    with pytest.raises(ValueError, match="contiguous"):
        calculate_geometry_receipt(
            [rows[0], replace(rows[1], segment_index=3)]
        )
