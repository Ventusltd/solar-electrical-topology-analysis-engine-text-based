import pytest

from solar_topology.circuit import EvidenceClass
from solar_topology.evidence import canonical_evidence_descriptor
from solar_topology.evidence_boundary import (
    EvidenceSource,
    PublicationPermission,
    RightsStatus,
    assess_publication_boundary,
    require_publication_boundary,
)


def _source(
    source_id,
    evidence_class,
    rights_status,
    permission,
    *,
    independent_public_support=False,
):
    return EvidenceSource(
        source_id=source_id,
        descriptor=canonical_evidence_descriptor(evidence_class),
        rights_status=rights_status,
        publication_permission=permission,
        independent_public_support=independent_public_support,
    )


def test_public_observation_is_publishable():
    decision = assess_publication_boundary(
        [
            _source(
                "public:aerial-imagery",
                EvidenceClass.PUBLIC_OBSERVATION,
                RightsStatus.PUBLIC,
                PublicationPermission.PUBLIC,
            )
        ]
    )

    assert decision.publishable
    assert decision.public_source_ids == ("public:aerial-imagery",)
    assert decision.restricted_source_ids == ()


def test_confidential_source_cannot_be_marked_public():
    with pytest.raises(ValueError, match="confidential NDA"):
        _source(
            "nda:sld",
            EvidenceClass.EXTERNAL_REFERENCE,
            RightsStatus.CONFIDENTIAL_NDA,
            PublicationPermission.PUBLIC,
        )


def test_confidential_only_result_is_blocked():
    source = _source(
        "nda:employers-requirements",
        EvidenceClass.EXTERNAL_REFERENCE,
        RightsStatus.CONFIDENTIAL_NDA,
        PublicationPermission.INTERNAL_ONLY,
    )

    decision = assess_publication_boundary([source])

    assert not decision.publishable
    assert decision.public_source_ids == ()
    assert decision.restricted_source_ids == ("nda:employers-requirements",)
    with pytest.raises(PermissionError, match="public export blocked"):
        require_publication_boundary([source])


def test_confidential_context_can_coexist_with_independent_public_support():
    sources = [
        _source(
            "public:planning-layout",
            EvidenceClass.PUBLIC_OBSERVATION,
            RightsStatus.PUBLIC,
            PublicationPermission.PUBLIC,
        ),
        _source(
            "nda:sld",
            EvidenceClass.EXTERNAL_REFERENCE,
            RightsStatus.CONFIDENTIAL_NDA,
            PublicationPermission.INTERNAL_ONLY,
            independent_public_support=True,
        ),
        _source(
            "derived:loop-geometry",
            EvidenceClass.DERIVED,
            RightsStatus.PUBLIC,
            PublicationPermission.PUBLIC,
        ),
    ]

    decision = require_publication_boundary(sources)

    assert decision.publishable
    assert decision.public_source_ids == (
        "derived:loop-geometry",
        "public:planning-layout",
    )
    assert decision.restricted_source_ids == ("nda:sld",)


def test_restricted_source_without_public_path_blocks_mixed_export():
    sources = [
        _source(
            "public:press-release",
            EvidenceClass.EXTERNAL_REFERENCE,
            RightsStatus.PUBLIC,
            PublicationPermission.PUBLIC,
        ),
        _source(
            "nda:exact-rating",
            EvidenceClass.EXTERNAL_REFERENCE,
            RightsStatus.CONFIDENTIAL_NDA,
            PublicationPermission.INTERNAL_ONLY,
        ),
    ]

    decision = assess_publication_boundary(sources)

    assert not decision.publishable
    assert any("nda:exact-rating" in reason for reason in decision.reasons)
