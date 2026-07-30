# Build Receipt 010 — Deterministic Persistence and Read-Back

Date: 2026-07-30
Branch: `main`
Pre-build recovery commit: `3906d35e6955d7608207b4fd6ed879ed5995d338`

## Scope

Create the storage-neutral persistence contract before adding DuckDB or Parquet adapters.

## Delivered

- immutable persisted-record envelopes;
- canonical JSON payload encoding;
- SHA-256 payload integrity checks;
- deterministic record ordering and store hashing;
- duplicate identifier rejection;
- independent deserialisation and read-back verification;
- rejection of tampered payloads, unsupported schemas and non-canonical stores;
- focused contract tests;
- public package exports.

## Engineering boundary

This build establishes the authoritative interchange and integrity layer. It does not yet claim that a particular database engine is authoritative. DuckDB and Parquet adapters must preserve this canonical payload and pass independent read-back verification.

## Validation status

Focused tests were authored but not executed by the GitHub connector. No fresh test pass is claimed in this receipt.
