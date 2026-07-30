"""Evidence-bearing public topology manifests for V10.

This layer records only publicly supportable topology facts. It does not ingest,
encode or reproduce Employer's Requirements, SLDs or other NDA material.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Mapping

from .evidence_boundary import EvidenceSource, assess_publication_boundary
from .identifiers import CanonicalIdentifier, EntityLevel, require_unique_identifiers


PUBLIC_TOPOLOGY_SCHEMA_VERSION = "globalgrid2050.solar-dc.public-topology.v10.1"


@dataclass(frozen=True)
class PublicTopologyRecord:
    identifier: CanonicalIdentifier
    record_type: str
    source_ids: tuple[str, ...]
    attributes: tuple[tuple[str, str | int | float | bool | None], ...] = ()

    def __post_init__(self) -> None:
        if self.identifier.level is EntityLevel.PROJECT:
            raise ValueError("topology records must sit below project level")
        if not isinstance(self.record_type, str) or not self.record_type.strip():
            raise ValueError("record_type must be non-empty text")
        if not self.source_ids or any(
            not isinstance(source_id, str) or not source_id.strip()
            for source_id in self.source_ids
        ):
            raise ValueError("source_ids must contain non-empty text")
        if tuple(sorted(set(self.source_ids))) != self.source_ids:
            raise ValueError("source_ids must be unique and sorted")
        keys = [key for key, _ in self.attributes]
        if keys != sorted(keys) or len(keys) != len(set(keys)):
            raise ValueError("attribute keys must be unique and sorted")


@dataclass(frozen=True)
class PublicTopologyManifest:
    project_identifier: CanonicalIdentifier
    records: tuple[PublicTopologyRecord, ...]
    public_source_ids: tuple[str, ...]
    schema_version: str = PUBLIC_TOPOLOGY_SCHEMA_VERSION


def build_public_topology_manifest(
    project_identifier: CanonicalIdentifier,
    records: tuple[PublicTopologyRecord, ...] | list[PublicTopologyRecord],
    sources: Mapping[str, EvidenceSource],
) -> PublicTopologyManifest:
    if project_identifier.level is not EntityLevel.PROJECT:
        raise ValueError("project_identifier must be project level")
    ordered_records = tuple(sorted(records, key=lambda record: record.identifier.value))
    require_unique_identifiers([record.identifier for record in ordered_records])
    source_ids = sorted({source_id for record in ordered_records for source_id in record.source_ids})
    missing = [source_id for source_id in source_ids if source_id not in sources]
    if missing:
        raise ValueError(f"manifest references unknown evidence sources: {missing}")
    for record in ordered_records:
        if not record.identifier.value.startswith(project_identifier.value + "/"):
            raise ValueError("all topology records must belong to the manifest project")
        decision = assess_publication_boundary([sources[source_id] for source_id in record.source_ids])
        if not decision.publishable or decision.restricted_source_ids:
            detail = "; ".join(decision.reasons) or "restricted evidence present"
            raise PermissionError(
                f"public topology record {record.identifier.value!r} blocked: {detail}"
            )
    return PublicTopologyManifest(
        project_identifier=project_identifier,
        records=ordered_records,
        public_source_ids=tuple(source_ids),
    )


def public_topology_payload(manifest: PublicTopologyManifest) -> dict[str, object]:
    return {
        "schema_version": manifest.schema_version,
        "project_identifier": manifest.project_identifier.value,
        "public_source_ids": list(manifest.public_source_ids),
        "records": [
            {
                "identifier": record.identifier.value,
                "record_type": record.record_type,
                "source_ids": list(record.source_ids),
                "attributes": {key: value for key, value in record.attributes},
            }
            for record in manifest.records
        ],
    }


def public_topology_json(manifest: PublicTopologyManifest) -> str:
    return json.dumps(
        public_topology_payload(manifest),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def public_topology_hash(manifest: PublicTopologyManifest) -> str:
    digest = hashlib.sha256(public_topology_json(manifest).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"
