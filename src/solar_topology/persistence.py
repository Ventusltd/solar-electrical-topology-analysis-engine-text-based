"""Deterministic persistence envelopes and independent read-back verification."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Mapping


PERSISTENCE_SCHEMA_VERSION = "globalgrid2050.solar-dc.persistence.v10.1"


@dataclass(frozen=True)
class PersistedRecord:
    record_id: str
    record_type: str
    source_schema_version: str
    payload_json: str
    payload_hash: str

    def __post_init__(self) -> None:
        for name, value in (
            ("record_id", self.record_id),
            ("record_type", self.record_type),
            ("source_schema_version", self.source_schema_version),
            ("payload_json", self.payload_json),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty text")
        expected = "sha256:" + hashlib.sha256(self.payload_json.encode("utf-8")).hexdigest()
        if self.payload_hash != expected:
            raise ValueError("payload_hash does not match payload_json")
        try:
            decoded = json.loads(self.payload_json)
        except json.JSONDecodeError as exc:
            raise ValueError("payload_json must contain valid JSON") from exc
        canonical = json.dumps(decoded, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        if canonical != self.payload_json:
            raise ValueError("payload_json must be canonical JSON")


@dataclass(frozen=True)
class DeterministicStore:
    records: tuple[PersistedRecord, ...]
    schema_version: str = PERSISTENCE_SCHEMA_VERSION


def canonical_payload_json(payload: Mapping[str, object]) -> str:
    if not isinstance(payload, Mapping):
        raise TypeError("payload must be a mapping")
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def persist_record(
    record_id: str,
    record_type: str,
    source_schema_version: str,
    payload: Mapping[str, object],
) -> PersistedRecord:
    payload_json = canonical_payload_json(payload)
    payload_hash = "sha256:" + hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
    return PersistedRecord(
        record_id=record_id,
        record_type=record_type,
        source_schema_version=source_schema_version,
        payload_json=payload_json,
        payload_hash=payload_hash,
    )


def build_deterministic_record_store(
    records: tuple[PersistedRecord, ...] | list[PersistedRecord],
) -> DeterministicStore:
    ordered = tuple(sorted(records, key=lambda item: item.record_id))
    ids = [item.record_id for item in ordered]
    if len(ids) != len(set(ids)):
        raise ValueError("persisted record identifiers must be unique")
    return DeterministicStore(records=ordered)


def deterministic_store_payload(store: DeterministicStore) -> dict[str, object]:
    return {
        "schema_version": store.schema_version,
        "records": [
            {
                "record_id": item.record_id,
                "record_type": item.record_type,
                "source_schema_version": item.source_schema_version,
                "payload": json.loads(item.payload_json),
                "payload_hash": item.payload_hash,
            }
            for item in store.records
        ],
    }


def deterministic_store_json(store: DeterministicStore) -> str:
    return json.dumps(
        deterministic_store_payload(store),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def deterministic_store_hash(store: DeterministicStore) -> str:
    digest = hashlib.sha256(deterministic_store_json(store).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def read_back_store(serialised: str) -> DeterministicStore:
    if not isinstance(serialised, str) or not serialised:
        raise ValueError("serialised store must be non-empty text")
    try:
        raw = json.loads(serialised)
    except json.JSONDecodeError as exc:
        raise ValueError("serialised store must be valid JSON") from exc
    if raw.get("schema_version") != PERSISTENCE_SCHEMA_VERSION:
        raise ValueError("unsupported persistence schema version")
    records: list[PersistedRecord] = []
    for item in raw.get("records", []):
        payload_json = canonical_payload_json(item["payload"])
        records.append(
            PersistedRecord(
                record_id=item["record_id"],
                record_type=item["record_type"],
                source_schema_version=item["source_schema_version"],
                payload_json=payload_json,
                payload_hash=item["payload_hash"],
            )
        )
    store = build_deterministic_record_store(records)
    if deterministic_store_json(store) != serialised:
        raise ValueError("serialised store is not canonical or changed during read-back")
    return store
