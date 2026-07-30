# Build Receipt 004 — Evidence and Complete-Circuit Calculation

## Status

Completed and validated on `main`.

Build slice: V10 evidence reconciliation, immutable calculation receipts and complete-circuit steady-state calculation  
Restore branch: `restore/2026-07-30-pre-v10-evidence-calculation-receipts`  
Restore commit: `afa54a057e0aa02bd264958590dc1782c281fd7d`  
Passing validation source head: `74bb7ba120cad98f6a7e45e4b802287d971b4d34`  
Validation receipt commit: `f28f30d2fd37402aebc6d135e802791b11a21816`

## What was built

### Canonical evidence reconciliation

`src/solar_topology/evidence.py` now preserves and reconciles:

- SegmentRow provenance: measured, OEM-declared, assumed and defaulted;
- V10 JavaScript provenance: measured, datasheet, standards-derived, geometry-derived, inherited, assumed and research hypothesis;
- canonical evidence class;
- separate verification state;
- original source vocabulary and source value;
- weakest-input evidence floor without silently promoting the source.

### Immutable calculation receipt

`src/solar_topology/calculation_receipts.py` now records:

- validated circuit hash;
- traversal schema and ordered terminal, connection and segment identifiers;
- current and its evidence descriptor;
- one result record per ordered source segment;
- conductor and connector resistance separately;
- complete-circuit resistance, voltage drop and resistive loss;
- formula identifiers;
- source warnings and evidence floor;
- deterministic canonical JSON and SHA-256 receipt hash.

The canonical receipt contains no timestamp and is reproducible from the same validated inputs.

### Complete-circuit calculation gate

`src/solar_topology/circuit_calculations.py` now:

1. rejects invalid current or evidence inputs;
2. rejects an invalid ordered traversal;
3. checks traversal boundaries against the canonical model;
4. independently re-derives graph order;
5. obtains a validated circuit hash;
6. reads each source segment from the canonical model in graph-derived order;
7. calculates conductor resistance from declared finished-cable R20, installed length and temperature;
8. calculates connector-contact resistance including its temperature correction;
9. aggregates total R, I×R voltage drop and I²R loss;
10. returns an immutable calculation receipt.

No total cable length, route length or user length is accepted by the calculation API.

## Known-answer canaries

At 17.35 A, 30 modules and 1.4 m positive and negative factory leads per module:

```text
Sequential
R = 0.78836961445 ohm
ΔV = 13.6782128107075 V
P = 237.316992265775 W

Leapfrog
R = 0.627462739 ohm
ΔV = 10.88647852165 V
P = 188.880402350628 W
```

These results include:

- external positive and negative conductors;
- the sequential far-end return where applicable;
- every positive and negative factory lead;
- all connector contacts;
- segment-specific conductor temperatures.

They are generic regression fixtures, not project approvals.

## Cross-language comparison

A shared fixture now tests the common 20 °C conductor-only formula subset in Python and V10 JavaScript:

- `v10-development/fixtures/steady_state_cross_language_v1.json`;
- `tests/test_circuit_calculations.py`;
- `v10-development/tests/cross-language.test.mjs`.

This is comparison evidence only. It does not promote the V10 JavaScript candidate kernel to calculation authority and does not claim comparison of temperature correction, connector resistance or the full physical circuit.

## Final validation receipt

```text
Python:          61 passed
V8:              13/13 regression tests passed
V9:              10 passed, 0 failed
V10 JavaScript:  13 passed, 0 failed
Overall:         PASS
```

Authoritative execution evidence:

- `v10-development/recovery/validation/V10_VALIDATION_LATEST.md`;
- `v10-development/recovery/validation/V10_VALIDATION_LATEST.json`.

## Authority state

This build proves that complete-circuit resistance, voltage drop and resistive loss can be calculated from the validated canonical Python circuit in independently verified graph order, including external conductors, factory leads and connector contacts.

Authority remains provisional and capability-specific:

- canonical circuit objects: provisional Python owner;
- ordered traversal verification: provisional independent Python verifier;
- steady-state R, ΔV and I²R loss: provisional Python authority candidate after known-answer and full-suite validation;
- V10 JavaScript: comparison and evidence-interface source only;
- standards compliance: not implemented by this slice;
- browser: downstream client only.

## Boundaries preserved

- no V6, V7, V8 or V9 implementation changes;
- no browser changes;
- no standards-compliance conclusion;
- no free total-length input;
- no aluminium temperature coefficient;
- no current-carrying-capacity selection;
- no transient or electromagnetic calculation;
- no confidential or project-specific data;
- no calculation after circuit or traversal validation failure.

## Exact next build order

1. Add interval uncertainty propagation for current, R20, length, temperature and connector resistance.
2. Define immutable operating-state inputs including string Vmp and voltage-drop percentage.
3. Persist calculation receipts into deterministic DuckDB/Parquet outputs with independent read-back verification.
4. Define result keys and aggregation laws from segment to string, MPPT, inverter, site and fleet.
5. Reconcile the duplicate Python geometry representations without changing proven cartridge behaviour.
6. Add report-DNA projections only after the result and persistence contracts are stable.
7. Keep standards cartridges and browser consumption downstream.
