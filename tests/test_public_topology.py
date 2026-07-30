import pytest

from solar_topology.circuit import EvidenceClass
from solar_topology.evidence import VerificationState, canonical_evidence_descriptor
from solar_topology.evidence_boundary import (
    EvidenceSource,
    PublicationPermission,
    RightsStatus,
)
from solar_topology.identifiers import EntityLevel, project_id
from solar_topology.public_topology import (
    PublicTopologyRecord,
    build_public_topology_manifest,
    public_topology_hash,
    public_topology_json,
)


def _source(source_id="planning-layout", public=True):
    return EvidenceSource(
        source_id=source_id,
        descriptor=canonical_evidence_descriptor(
            EvidenceClass.PUBLIC_OBSERVATION,
            verification_state=VerificationState.CANDIDATE,
            source_reference=f"fixture:{source_id}",
        ),
        rights_status=RightsStatus.PUBLIC if public else RightsStatus.CONFIDENTIAL_NDA,
        publication_permission=(
            PublicationPermission.PUBLIC
            if public
            else PublicationPermission.INTERNAL_ONLY
        ),
    )


def _record(project, source_id="planning-layout"):
    site = project.child(EntityLevel.SITE, "site-001")
    system = site.child(EntityLevel.SYSTEM, "dc-array")
    return PublicTopologyRecord(
        identifier=system,
        record_type="array-system",
        source_ids=(source_id,),
        attributes=(("status", "publicly-observed"),),
    )


def test_public_manifest_builds_and_hashes_deterministically():
    project = project_id("public-cleve-hill-study")
    source = _source()
    record = _record(project)
    first = build_public_topology_manifest(project, [record], {source.source_id: source})
    second = build_public_topology_manifest(project, tuple(reversed([record])), {source.source_id: source})
    assert public_topology_json(first) == public_topology_json(second)
    assert public_topology_hash(first) == public_topology_hash(second)


def test_public_manifest_rejects_confidential_source_even_with_public_record_name():
    project = project_id("study")
    source = _source("internal-sld", public=False)
    with pytest.raises(PermissionError, match="blocked"):
        build_public_topology_manifest(
            project,
            [_record(project, "internal-sld")],
            {source.source_id: source},
        )


def test_public_manifest_rejects_unknown_source():
    project = project_id("study")
    with pytest.raises(ValueError, match="unknown evidence sources"):
        build_public_topology_manifest(project, [_record(project)], {})


def test_public_manifest_rejects_record_from_another_project():
    project = project_id("study-a")
    other = project_id("study-b")
    source = _source()
    with pytest.raises(ValueError, match="belong"):
        build_public_topology_manifest(
            project,
            [_record(other)],
            {source.source_id: source},
        )


def test_record_requires_sorted_unique_sources_and_attributes():
    project = project_id("study")
    site = project.child(EntityLevel.SITE, "site-001")
    with pytest.raises(ValueError, match="source_ids"):
        PublicTopologyRecord(site, "site", ("b", "a"))
    with pytest.raises(ValueError, match="attribute keys"):
        PublicTopologyRecord(
            site,
            "site",
            ("a",),
            (("z", 1), ("a", 2)),
        )
