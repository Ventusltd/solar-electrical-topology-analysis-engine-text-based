# V10 Recovery Point After Study Registry Repair

Date: 2026-07-30
Branch: `main`
Repository: `Ventusltd/solar-electrical-topology-analysis-engine-text-based`

## Executive state

The repository has been recovered to a fully passing validation state.

The failure shown by GitHub Actions at commit `811c3d65ce2b2a698b46a7400112a4d6bab10a16` was caused by one invalid ordering declaration in `src/solar_topology/study_registry.py`.

The `loop-geometry` study declared:

```text
("route-geometry", "pole-separation")
```

The `StudyDefinition` contract requires evidence-role tuples to be unique and lexicographically sorted. The correct declaration is:

```text
("pole-separation", "route-geometry")
```

The repair was committed directly to `main` at:

`8a5f84677104defc57002b2f798c3cebc4201764`

The automated validation receipt was committed at:

`206429eae0829a46e51b7706059a92e63ff6ddae`

## Current proven validation

Validation source commit:

`8a5f84677104defc57002b2f798c3cebc4201764`

Result:

```text
Python             117 passed
V8 regression       13 passed
V9 debug             10 passed
V10 JavaScript       13 passed
Overall              PASS
```

The canonical machine-readable receipt is:

`v10-development/recovery/validation/V10_VALIDATION_LATEST.json`

## Build-history recovery ladder

### Historical recovery and authority foundations

- `d134ef032c54b962b5dfb9b40238ded5848c65f1` — IEC TS 62738 capability matrix.
- `2319103cab969cee7ef00372e1ef80ae65015413` — V10 authoritative engine recovery plan.
- `0cb2fab8e1258912e18f41441b85a95931f4f2d3` — detailed ChatGPT reboot handover.

### V8 recovery points

- `7d85079cfc8c1a9b53687b5689f970135fbda572` — restore point before V8 leapfrog build.
- `28f40770b29bf51f6e4f6f3f297f2eefe381f26a` — restore point before V8 lead and fleet recovery.
- `61dc79896a065b6b40bc31384efeb0863b6eb99b` — restore point before segment-contract physics and Parquet rebuild.
- `f5126d556b395831846a85bcf5b1b350056d3823` — restore point before V8 physical module geometry repair.

### V9 recovery points

- `9e6df0d94e85eb19c6df3f1b8dc4a8440c7a17cb` — restore point before B9 sandbox scope.
- `faf8da8aa45a16cabf526e5c714413f810243527` — restore point before first working B9 sandbox.
- `ba6b4f6587c98688167aee3ce6734e8d43078c0a` — restore point before V9 extraction.
- `b1f0d3e22aaeb55fd62221f0bf77ef148477eebe` — restore point before V9 MPPT build.
- `254be20f6c86415d8be9768acc47722cdebca1a6` — V9 east-west full inverter-block circuit sandbox.
- `589bee2e9d687b8d6e89818423a93cdc397126d9` — restore point before V9 computation-engine rebuild.

### V10 calculation recovery points

- `afa54a057e0aa02bd264958590dc1782c281fd7d` — V10 traversal restore point and validation.
- `074c5743f82b867f05abb46927e8facdc5fbb84a` — V10 calculation restore point and validation.
- `be4a80233603b9848cb7118f74ce225f640df75a` — V10 uncertainty restore point and validation.
- `80057fe4bdfbbafc97ee6fa3cf8082f9e02ae598` — earlier fully proven green source: Python 66, V8 13, V9 10 and V10 JavaScript 13.

### Main-only Build 006 recovery points

- `2136014adfbca5f886c2cc69040eae73480fe043` — pre-Build 006 merged main position.
- `40b008f82dbaf12d6ff49fffc5f1685dfdc41639` — evidence-boundary package export.
- `ee540ff951b48fd3b975b1885fb382d5bb3754f6` — main-only restore discipline update.
- `acb66f3fae11ba7e451ce724a6f40327c6577a71` — post-Build 006 main-only recovery record.

### Autonomous diagnostics and study batch

The later batch added:

- evidence boundary and evidence register;
- canonical identifiers;
- public topology manifests;
- contradiction registration;
- deterministic persistence;
- diagnostics, adapters and bridges;
- study applicability;
- electrical-study registry and acceptance-study receipts;
- public package exports;
- expanded tests.

The batch was not discarded. It was retained and repaired forward.

### Failure and repair

- `811c3d65ce2b2a698b46a7400112a4d6bab10a16` — sourced electrical acceptance-study receipts; introduced the unsorted registry tuple.
- `a23bba031dd971d2df2b01c382be67ed5dc2feef` — validation receipt recording the import-time failure.
- `8a5f84677104defc57002b2f798c3cebc4201764` — registry-order repair.
- `206429eae0829a46e51b7706059a92e63ff6ddae` — green validation receipt after repair.

## Recovery decision

No rollback is required.

The 64-commit development batch after the earlier green uncertainty restore point is retained because the failure was local, deterministic and corrected without exposing wider regression failures.

The current recovery authority is the repaired source commit plus its green validation receipt.

## Binding build discipline from this point

All work remains directly on `main` unless Vikram Kumar explicitly changes that instruction.

Every bounded build must use this sequence:

```text
Declare bounded scope
→ implement
→ run focused tests
→ run complete validation
→ commit validation receipt
→ record recovery point
→ begin next build
```

A failed complete validation blocks new feature work.

Do not generate repeated receipt commits against a known failing source without first repairing or reverting the bounded defect.

The browser remains downstream and is not engineering authority.

## Next build order

### Build 020 — Validation-gate hardening

Purpose: prevent one malformed static registry declaration from disabling the entire package during test collection.

Required work:

1. Add an explicit test that every item in `INITIAL_STUDIES` has sorted, unique `required_input_ids` and `required_evidence_roles`.
2. Add a minimal package-import smoke test.
3. Decide whether package import should eagerly instantiate all registries or expose them through a safer bounded import path.
4. Preserve fail-fast validation for invalid definitions, but ensure the failure points directly to the offending `study_id` and field.
5. Run complete validation and record a restore point.

Acceptance:

```text
Malformed registry fixtures fail with the offending study identifier.
Valid package import succeeds.
Complete validation remains green.
```

### Build 021 — Public API consolidation

Purpose: stabilise `src/solar_topology/__init__.py` after repeated export additions.

Required work:

1. Inventory every exported symbol.
2. Classify each export as canonical, provisional, internal or compatibility-only.
3. Remove accidental duplicate or circular export paths.
4. Add deterministic public-API snapshot coverage.
5. Keep optional study/report layers from destabilising core physics imports.

### Build 022 — Independent audit of Builds 006–019

Audit by capability group:

1. evidence boundary and evidence register;
2. canonical identifiers;
3. public topology;
4. contradiction register;
5. persistence and DuckDB segments;
6. diagnostics and bridges;
7. study applicability and electrical studies.

Each group receives one decision:

```text
ADOPT
ADAPT
REPAIR
DEFER
REJECT
```

No capability becomes authoritative merely because it executes or has a receipt.

### Build 023 — Canonical object and topology closure

1. Confirm the canonical physical-object schema.
2. Confirm terminals and connectivity.
3. Confirm ordered circuit traversal.
4. Confirm sequential and leapfrog cartridge invariants.
5. Ensure topology validation blocks dependent calculations.
6. Establish independent topology verification distinct from the builder.

### Build 024 — Steady-state kernel authority decision

1. Compare the Python physical engine with the V10 JavaScript candidate.
2. Use shared fixtures for resistance, voltage drop, power loss and cold Voc.
3. Preserve uncertainty and provenance interfaces.
4. Declare the authoritative computation kernel and the compatibility role of the other implementation.

### Build 025 — Route and installation physics

1. Route-derived conductor lengths.
2. Positive and negative conductor formation.
3. product versus bare-conductor properties.
4. temperature and installation conditions.
5. complete-circuit resistance and loss receipts.

### Build 026 — Distributed and transient study boundary

Only after the steady-state kernel and topology authority are proven:

1. two-wire distributed parameters;
2. loop geometry and formation;
3. capacitance to frame and earth;
4. surge-sharing models;
5. arc-restrike models;
6. declared frequency and validity ranges;
7. standards cartridges kept separate from first-principles physics.

### Build 027 — Reporting and browser projection

1. reports as deterministic projections over evidence;
2. CSV, text and HTML first;
3. PDF and DOCX as rendered outputs, not truth stores;
4. browser rebuilt last as a thin client;
5. no hidden engineering mathematics in the interface.

## Exact next executable task

Start Build 020 only.

Do not add another engineering capability before validation-gate hardening is complete and green.
