# Build 022 — Independent Capability Audit

Date: 2026-07-30
Branch: `main`
Repository: `Ventusltd/solar-electrical-topology-analysis-engine-text-based`

## Authority boundary

This audit reviews capabilities added through Builds 006–019. Execution, passing tests and public exports do not by themselves make a capability authoritative. Authority requires a declared engineering role, deterministic behaviour, evidence boundaries, independent validation and compatibility with the canonical build order:

`Physics → Geometry → Objects → Topology → Computation → Evidence → Reporting → Visualisation`

## Decisions

### 1. Evidence boundary and evidence register — ADOPT

Reason:

- Separates source rights, verification state and publication permission from engineering calculations.
- Prevents confidential or unverified material from silently becoming public authority.
- Deterministic payload and hash functions make the boundary auditable.

Conditions:

- Evidence maturity must never substitute for engineering correctness.
- Publication permission must remain independent of calculation pass/fail.
- Standards text and confidential documents must be referenced by provenance, not copied into canonical data.

Authoritative role:

- Canonical evidence and publication gate.

### 2. Canonical identifiers — ADOPT

Reason:

- Stable identifiers are required for cross-file, cross-study and fleet-scale traceability.
- Uniqueness checking is a necessary precondition for deterministic persistence and contradiction handling.

Conditions:

- Identifier grammar must be frozen before browser reconstruction.
- Human labels remain descriptive and must not be used as primary keys.
- Identifier migration must be explicit and receipt-bearing.

Authoritative role:

- Canonical identity layer for projects, systems, objects, terminals, segments, studies and evidence.

### 3. Public topology manifests — ADAPT

Reason:

- A public projection separated from the private engineering model is correct.
- Current capability is useful but must remain downstream of the canonical physical-object and topology schema.

Required adaptation:

- Rebuild manifest generation against the final Build 023 object and terminal contracts.
- Prove that omitted private fields cannot alter public topology meaning.
- Add an explicit source-model hash and projection-method version.

Authoritative role after adaptation:

- Deterministic public projection only; never the source topology.

### 4. Contradiction register — ADOPT

Reason:

- Contradictory evidence and model claims must remain visible rather than being overwritten.
- Explicit status and severity support engineering restraint and review.

Conditions:

- Contradictions must identify the exact claims, evidence descriptors and affected engineering objects.
- Resolution must create a new record; historical contradictions must not be deleted.
- An unresolved blocking contradiction must prevent affected calculations from becoming authoritative.

Authoritative role:

- Canonical conflict ledger.

### 5. Deterministic persistence and DuckDB segments — ADAPT

Reason:

- Deterministic records, read-back checks and Parquet export are suitable for fleet-scale work.
- Persistence currently risks becoming authoritative before the final object and segment schemas are frozen.

Required adaptation:

- Bind every persisted record to schema version, source-model hash and method version.
- Treat DuckDB and Parquet as reproducible stores and projections, not engineering truth.
- Add migration fixtures before changing any canonical table schema.
- Prevent database-generated route lengths or inferred objects from entering authoritative calculations without evidence status.

Authoritative role after adaptation:

- Reproducible persistence and aggregation layer.

### 6. Diagnostics, adapters and bridges — ADAPT

Reason:

- Accumulating diagnostics and explicit study coverage are materially better than exception-only validation.
- Bridges preserve legacy findings while the canonical model is rebuilt.

Required adaptation:

- Freeze diagnostic codes and severity semantics after Build 023.
- Distinguish malformed input, unavailable evidence, failed physics and publication restrictions.
- Ensure adapters cannot convert a failed legacy result into a passing canonical result.
- Require every blocking diagnostic to identify subject, method and remediation path.

Authoritative role after adaptation:

- Canonical reporting of validation and study state; legacy bridges remain compatibility-only.

### 7. Study applicability and electrical studies — REPAIR

Reason:

- Applicability, missing evidence and acceptance-criterion sourcing are the correct architecture.
- The registry import failure showed that static declarations can disable the package.
- Several electrical acceptance studies exist before the final topology and kernel authority decisions.

Required repair:

- Keep study definitions import-safe and independently testable.
- Bind each performed study to an authoritative input model hash and calculation receipt.
- Separate first-principles calculation from acceptance criteria and standards cartridges.
- No study may report pass when required evidence, criterion source or upstream topology validation is absent.
- Revalidate all existing acceptance-study receipts after Builds 023–025.

Authoritative role after repair:

- Canonical study orchestration and coverage registry; current numerical acceptance results remain provisional.

## Capability summary

| Capability | Decision | Current authority |
|---|---|---|
| Evidence boundary/register | ADOPT | Canonical |
| Canonical identifiers | ADOPT | Canonical |
| Public topology | ADAPT | Provisional projection |
| Contradiction register | ADOPT | Canonical ledger |
| Persistence/DuckDB | ADAPT | Provisional storage |
| Diagnostics/bridges | ADAPT | Diagnostics canonical; bridges compatibility-only |
| Study applicability/electrical studies | REPAIR | Provisional |

## Cross-cutting findings

1. No capability added during Builds 006–019 should be rolled back wholesale.
2. The correct action is repair-forward against frozen contracts.
3. Public topology, persistence, diagnostics and studies depend on Build 023 object/topology closure.
4. Numerical electrical-study authority depends on Build 024 kernel authority and Build 025 route/installation physics.
5. Browser code remains downstream and cannot settle engineering disagreements.

## Binding dependency order

```text
Build 021 public API contract
→ Build 022 capability decisions
→ Build 023 canonical object/topology closure
→ rebind public topology + diagnostics + persistence
→ Build 024 kernel authority
→ Build 025 route/installation physics
→ revalidate electrical-study receipts
→ Build 026 distributed/transient boundary
→ Build 027 reporting/browser projection
```

## Build 022 acceptance

- Every capability group has one explicit decision.
- Every non-ADOPT decision has bounded repair/adaptation work.
- No execution result is treated as proof of engineering authority.
- Dependencies into Builds 023–025 are explicit.

Build 022 decision record: COMPLETE.

## Exact next executable task

Start Build 023 by freezing the canonical physical-object, terminal, connection and ordered-traversal contracts. Do not modify numerical physics during the first Build 023 increment.
