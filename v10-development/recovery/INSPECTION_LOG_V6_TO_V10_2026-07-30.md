# V6–V10 Inspection Log

Date: 2026-07-30
Pre-batch recovery commit: `76a5e42cfea0c92d0b8624e442a9270d322764a7`
Operating mode: direct commits to `main`; immutable commit recovery points; no feature branches.

## Version roles

### V6 — complete-circuit browser reference

V6 is the broadest interactive calculator. It contains physical table geometry, sequential and leapfrog states, complete-series-circuit resistance, voltage drop, loss, loop-area screening, differential/common-mode separation, capacitance-to-earth scenarios, IMD inputs and manual route segments. Its strength is breadth and visual explanation. Its weakness is browser ownership of too much engineering logic and a mixture of assumed values with presentation-state calculations.

### V7 — electromagnetic and evidence-discipline reference

V7 isolates electromagnetic foundations: unit discipline, evidence state, low- and high-frequency inductance, differential and common-mode networks, propagation classification and explicit validation gates. It remains a screening workbench rather than an authoritative fleet engine. Its strongest contribution to V10 is epistemic discipline, not its browser implementation.

### V8 — narrow cable-schedule and topology invariant reference

V8 resolves the sequential-versus-leapfrog external-cable question. It establishes the one-row-span identity, lead-reach feasibility gate, actual site-string aggregation, the copper invariant and regression fixtures. Its strongest contribution to V10 is the cartridge/segment data law and the separation of external EPC cable from factory-fitted lead conductor.

### V9 — multi-array interaction and state reference

V9 defines the common architecture chain: mechanical cartridge → electrical cartridge → ordered segments → physics studies → export. It provides typed browser state, history and multi-array interaction, but remains transitional and partly dependent on earlier renderer assets. Its strongest contribution to V10 is interaction/state design, not numerical authority.

### V10 — headless authority candidate

V10 now contains canonical circuit objects, independent validation and traversal, complete-circuit calculation receipts, evidence vocabularies, uncertainty propagation, publication boundaries, canonical identifiers, public topology manifests, contradiction records and deterministic persistence. It is the only version being extended as the durable engineering core.

## Consolidation decisions

1. V6–V9 remain frozen evidence and comparison workbenches.
2. V10 Python remains the sole authority candidate for new physics and fleet-scale data.
3. Browser versions may consume V10 outputs later; they shall not independently reimplement authoritative calculations.
4. Public topology and confidential project evidence remain separate at the data boundary.
5. Fleet work shall use DuckDB and Parquet rather than browser JSON.
6. Every longer batch shall record one pre-batch commit, bounded build receipts, tests and a post-batch recovery position.

## Current validated baseline

Validation at source head `fe4ded583efe098a0d9838f6ca2e4849154fca20` passed:

- Python: 93 passed
- V8: 13/13
- V9: 10 passed, 0 failed
- V10 JavaScript: 13 passed, 0 failed

## Autonomous batch 011–013

This batch implements:

- DuckDB segment persistence and deterministic read-back;
- an engineering evidence register linking requirements, evidence and status;
- geometry-derived loop-area receipts with explicit approximation status.

No Cleve Hill confidential SLD or Employer’s Requirements content is introduced.