# Build Receipt 005 — Uncertainty and Operating State

## Status

Completed and validated on `main`.

Build slice: conservative interval uncertainty propagation, immutable operating-state inputs and voltage-drop percentage  
Restore branch: `restore/2026-07-30-pre-v10-uncertainty-operating-state`  
Restore commit: `074c5743f82b867f05abb46927e8facdc5fbb84a`  
Passing validation source head: `80057fe4bdfbbafc97ee6fa3cf8082f9e02ae598`  
Validation receipt commit: `8ddc8f340e3f2b6cd88aa19836d7af0de1aceb1c`

## What was built

### Immutable interval contract

`src/solar_topology/uncertainty.py` adds a closed finite `Interval` contract with:

- lower, nominal and upper values;
- mandatory units;
- deterministic validation that `lower <= nominal <= upper`;
- exact intervals for known values;
- no implied probability distribution or confidence level.

### Immutable operating state

`OperatingState` now records:

- bounded string current in amperes;
- current evidence;
- bounded string Vmp in volts;
- Vmp evidence;
- stable operating-state identity.

Current cannot be negative and Vmp must remain strictly positive.

### Segment input uncertainty

`SegmentInputIntervals` permits declared bounds for:

- installed conductor length;
- finished-cable R20 per metre;
- conductor temperature;
- connector resistance per contact.

The declared nominal value must exactly match the value already stored in the canonical circuit model. The uncertainty layer cannot silently alter the canonical nominal model.

### Conservative propagation

`calculate_complete_circuit_with_uncertainty`:

1. invokes the existing validated complete-circuit calculation gate;
2. therefore requires valid canonical circuit and independently verified traversal;
3. rejects uncertainty for unknown segments;
4. applies monotonic copper resistance correction across declared bounds;
5. preserves conductor and connector resistance separately;
6. aggregates bounded complete-circuit resistance;
7. calculates bounded voltage drop and I²R loss;
8. calculates voltage-drop percentage using bounded string Vmp;
9. returns a deterministic immutable uncertainty receipt.

The bounds are conservative combinations of declared extrema. Correlation and probability are not inferred.

### Deterministic receipt

The new receipt records:

- validated circuit hash;
- nominal calculation receipt identity;
- operating-state identity;
- ordered segment uncertainty results;
- complete-circuit resistance interval;
- voltage-drop interval;
- resistive-loss interval;
- voltage-drop percentage interval;
- explicit warnings;
- canonical JSON and SHA-256 hash.

### Public API

The uncertainty and operating-state contracts are exported through `solar_topology.__init__`.

## Tests added

`tests/test_uncertainty.py` proves:

- interval ordering, finiteness and unit requirements;
- nominal results remain inside propagated bounds;
- voltage-drop percentage uses string Vmp;
- deterministic receipts under source-row reordering;
- rejection of unknown segment uncertainty;
- rejection of a declared nominal that differs from the canonical model;
- rejection of invalid operating-state voltage.

## Final validation receipt

```text
Python:          66 passed
V8:              13/13 regression tests passed
V9:              10 passed, 0 failed
V10 JavaScript:  13 passed, 0 failed
Overall:         PASS
```

Authoritative execution evidence:

- `v10-development/recovery/validation/V10_VALIDATION_LATEST.md`;
- `v10-development/recovery/validation/V10_VALIDATION_LATEST.json`.

## Authority state

This build establishes a validated candidate contract for declared interval propagation and operating-state evidence. It does not establish statistical confidence, stochastic correlation, standards compliance or transient behaviour.

Authority remains provisional and capability-specific:

- canonical circuit objects: provisional Python owner;
- ordered traversal verification: provisional independent Python verifier;
- nominal steady-state R, ΔV and I²R loss: provisional Python authority candidate;
- interval propagation and voltage-drop percentage: provisional Python authority candidate after full-suite validation;
- V10 JavaScript: comparison and evidence-interface source only;
- browser: downstream client only.

## Boundaries preserved

- no V6, V7, V8 or V9 implementation changes;
- no browser changes;
- no standards-compliance conclusion;
- no free total-length input;
- no probabilistic or confidence claim;
- no automatic correlation assumption;
- no aluminium temperature coefficient;
- no transient or electromagnetic calculation;
- no project-specific data;
- no calculation after circuit or traversal validation failure.

## Exact next build order

1. Persist nominal and uncertainty receipts into deterministic DuckDB and Parquet outputs.
2. Add independent read-back verification against canonical JSON and receipt hashes.
3. Define immutable result keys and aggregation laws from segment to string, MPPT, inverter, site and fleet.
4. Reconcile the duplicate Python geometry representations without changing proven cartridge behaviour.
5. Add report-DNA projections only after result and persistence contracts are stable.
6. Keep standards cartridges, electromagnetic research and browser consumption downstream.
