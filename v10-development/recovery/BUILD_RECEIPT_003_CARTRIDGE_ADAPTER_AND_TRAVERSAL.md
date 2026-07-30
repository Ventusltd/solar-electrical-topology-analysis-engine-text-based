# Build Receipt 003 — Cartridge Adapter and Ordered Traversal

## Status

Completed and validated on `main`.

Build slice: V10 cartridge-to-circuit adaptation and independent ordered traversal  
Restore branch: `restore/2026-07-30-pre-v10-cartridge-adapter-traversal`  
Restore commit: `2e14b87db26c6de0ad7d175135a1ef166a8b0717`  
Passing validation source head: `b0f2b8c100a26bad10d22408a8ca6c25a5aa118c`  
Validation receipt commit: `fd55598bd66af88805e041c1b6b8fd84616821ae`

## What was built

### Canonical cartridge adapter

`src/solar_topology/circuit_adapters.py` now converts one validated sequential or leapfrog `SegmentRow` chain into the canonical V10 `CircuitModel`.

The adapter:

- preserves source segment values as object attributes without recalculation;
- creates inverter, MPPT and string hierarchy objects;
- creates explicit source-node objects and terminals;
- creates one physical object and one internal graph edge per source segment;
- preserves geometry, conductor product data, R20, temperature, connector resistance, formation, installation class, feasibility, warnings and source references;
- rejects mixed chains, duplicate source segment identifiers and coordinate disagreement at a shared node;
- records deterministic source-chain identity and hash;
- provides direct sequential and leapfrog circuit builders.

### Independent ordered traversal

`src/solar_topology/circuit_traversal.py` now verifies complete circuit order from the terminal graph rather than trusting array order, segment index, browser order or generator output.

The verifier:

- blocks traversal when canonical circuit validation fails;
- requires one connected simple path between declared boundaries;
- rejects branches, cycles, extra endpoints, disconnected components and excess edges;
- requires each source segment identifier to occur exactly once on an internal connection;
- walks every connection from start to end;
- returns ordered terminal, connection and segment identifiers;
- can compare graph-derived order against an independent expected segment sequence.

### Validation infrastructure

Added:

- `.github/workflows/v10-validation.yml`;
- `scripts/run_v10_validation.py`;
- paired Markdown and JSON validation receipts under `v10-development/recovery/validation/`.

The validation runner executes the complete Python suite, V8 regression suite, V9 deterministic runner and V10 JavaScript suite, then commits the evidence receipt to `main`.

## Negative knowledge preserved

The first complete baseline run produced:

- Python: 52 passed, 1 failed;
- V8: pass;
- V9: pass;
- V10 JavaScript: pass.

The Python failure was the previously identified inappropriate exact floating-point comparison in `tests/test_parquet_store.py`:

```text
84.00000000000004 != 84.0
```

The correction was bounded:

- floating factory-lead aggregation uses `pytest.approx(84.0)`;
- connector counts remain exact at `62`;
- no equation, source data, aggregation logic or expected engineering quantity was changed.

## Final validation receipt

The second complete run passed:

```text
Python:          53 passed
V8:              13/13 regression tests passed
V9:              10 passed, 0 failed
V10 JavaScript:  12 passed, 0 failed
Overall:         PASS
```

Authoritative execution evidence:

- `v10-development/recovery/validation/V10_VALIDATION_LATEST.md`
- `v10-development/recovery/validation/V10_VALIDATION_LATEST.json`

## Authority state

This build proves that the existing sequential and leapfrog cartridge chains can be represented as valid canonical circuits and independently traversed in their declared electrical order.

It does not yet promote any resistance, loss, voltage, inductance, capacitance, standards or browser calculation to V10 authority.

The Python cartridge layer remains the provisional source of sequential and leapfrog numerical behaviour. The circuit model owns objects and connectivity. The traversal verifier owns graph-derived ordering verification.

## Boundaries preserved

- no V6, V7, V8 or V9 implementation changes;
- no browser changes;
- no standards compliance logic;
- no project-specific or confidential data;
- no free total cable-length input;
- no topology-dependent calculation after validation failure;
- no authority promotion from green CI alone.

## Exact next build order

1. Reconcile provenance and evidence vocabularies across `SegmentRow`, canonical Python circuit objects and the V10 JavaScript quantity contract.
2. Define an immutable ordered-circuit result and calculation receipt contract.
3. Attach complete-circuit resistance, voltage drop and resistive loss only to a validated ordered traversal.
4. Add known-answer tests proving inclusion of external conductors, factory leads and connector contacts.
5. Add cross-language comparison receipts without treating V10 JavaScript as calculation authority.
6. Keep reports and browser consumption downstream.
