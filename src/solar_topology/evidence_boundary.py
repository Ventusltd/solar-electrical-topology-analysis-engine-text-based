"""Publication-boundary controls for V10 engineering evidence.

The boundary is intentionally conservative: confidential evidence may remain in
an authorised internal model, but a public result must have independent public,
observed, manufacturer, external-reference or original-derived support.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .circuit import EvidenceClass
from .evidence import EvidenceDescriptor


EVIDENCE_BOUNDARY_SCHEMA_VERSION = (
    "globalgrid2050.solar-dc.evidence-boundary.v10.1"
)


class RightsStatus(StrEnum):
    PUBLIC = "public"
    AUTHORISED_INTERNAL = "authorised_internal"
    CONFIDENTIAL_NDA = "confidential_nda"
    UNKNOWN = "unknown"


class PublicationPermission(StrEnum):
    PUBLIC = "public"
    INTERNAL_ONLY = "internal_only"
    WITHHELD_PENDING_REVIEW = "withheld_pending_review"


@dataclass(frozen=True)
class EvidenceSource:
    source_id: str
    descriptor: EvidenceDescriptor
    rights_status: RightsStatus
    publication_permission: PublicationPermission
    source_revision: str | None = None
    observation_date: str | None = None
    observer: str | None = None
    independent_public_support: bool = False
    notes: str | None = None
    schema_version: str = EVIDENCE_BOUNDARY_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not isinstance(self.source_id, str) or not self.source_id.strip():
            raise ValueError("source_id must be non-empty text")
        if not isinstance(self.descriptor, EvidenceDescriptor):
            raise TypeError("descriptor must be an EvidenceDescriptor")
        if not isinstance(self.rights_status, RightsStatus):
            raise TypeError("rights_status must be a RightsStatus")
        if not isinstance(self.publication_permission, PublicationPermission):
            raise TypeError(
                "publication_permission must be a PublicationPermission"
            )
        if (
            self.rights_status is RightsStatus.CONFIDENTIAL_NDA
            and self.publication_permission is PublicationPermission.PUBLIC
        ):
            raise ValueError("confidential NDA evidence cannot be marked public")


@dataclass(frozen=True)
class PublicationDecision:
    publishable: bool
    public_source_ids: tuple[str, ...]
    restricted_source_ids: tuple[str, ...]
    reasons: tuple[str, ...]
    schema_version: str = EVIDENCE_BOUNDARY_SCHEMA_VERSION


_PUBLIC_SUPPORT_CLASSES = {
    EvidenceClass.MANUFACTURER_DECLARED,
    EvidenceClass.FIELD_MEASURED,
    EvidenceClass.PUBLIC_OBSERVATION,
    EvidenceClass.USER_CREATED,
    EvidenceClass.DERIVED,
    EvidenceClass.EXTERNAL_REFERENCE,
}


def assess_publication_boundary(
    sources: tuple[EvidenceSource, ...] | list[EvidenceSource],
) -> PublicationDecision:
    """Return whether a result has a defensible public evidence path.

    A result is publishable only when at least one source is explicitly public
    and all sources essential to the public claim are either public themselves
    or declare independent public support. Confidential material is never
    included in the public source list.
    """

    if not sources:
        return PublicationDecision(
            publishable=False,
            public_source_ids=(),
            restricted_source_ids=(),
            reasons=("no evidence sources supplied",),
        )
    if any(not isinstance(source, EvidenceSource) for source in sources):
        raise TypeError("all sources must be EvidenceSource values")

    public_ids: list[str] = []
    restricted_ids: list[str] = []
    reasons: list[str] = []

    for source in sources:
        is_public = (
            source.rights_status is RightsStatus.PUBLIC
            and source.publication_permission is PublicationPermission.PUBLIC
            and source.descriptor.evidence_class in _PUBLIC_SUPPORT_CLASSES
        )
        if is_public:
            public_ids.append(source.source_id)
        else:
            restricted_ids.append(source.source_id)
            if not source.independent_public_support:
                reasons.append(
                    f"source {source.source_id!r} lacks an independent public support path"
                )

    if not public_ids:
        reasons.append("no explicitly public evidence source supports the result")

    return PublicationDecision(
        publishable=bool(public_ids) and not reasons,
        public_source_ids=tuple(sorted(public_ids)),
        restricted_source_ids=tuple(sorted(restricted_ids)),
        reasons=tuple(reasons),
    )


def require_publication_boundary(
    sources: tuple[EvidenceSource, ...] | list[EvidenceSource],
) -> PublicationDecision:
    """Return a passing decision or reject the public export."""

    decision = assess_publication_boundary(sources)
    if not decision.publishable:
        detail = "; ".join(decision.reasons)
        raise PermissionError(f"public export blocked: {detail}")
    return decision
