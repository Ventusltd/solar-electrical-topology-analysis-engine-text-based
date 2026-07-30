# Autonomous Respawn and Forward Build Order

Timestamp: 2026-07-30 15:22 Europe/London
Repository: `Ventusltd/solar-electrical-topology-analysis-engine-text-based`
Branch: `main`
Operating rule: work directly on `main`; no branches or pull requests unless Vikram Kumar explicitly changes this instruction.

## Read this first after a thread reset

Do not inspect the whole repository before acting.

1. Read this file.
2. Read `v10-development/recovery/validation/V10_VALIDATION_LATEST.json`.
3. Read only the receipt for the active build.
4. If the latest receipt is green for the active build head, begin the next numbered build.
5. If it is red or stale, repair or wait for the exact active build only.
6. Do not re-audit V6, V7, V8, V9 or unrelated repositories unless the active build explicitly requires it.

Target recovery time: one minute or less.

## Current authority state

- Python package: strongest provisional computation authority.
- V10 JavaScript: evidence-aware and uncertainty-aware comparison implementation.
- V8 and V9: regression and historical recovery sources.
- Browser: downstream client, never engineering authority.

## Proven build sequence

- Build 020: validation-gate hardening. Complete and green.
- Build 021: public API consolidation. Source work complete; final validation receipt for the last test commit is pending at the time of this snapshot.

Build 021 source commits:

- `bd811683c296dcdae4543697ee19a7bdb410502f` — public API classification manifest.
- `d3cc8416dc0d8b4254dc1a282632d5334079f31c` — total deterministic inventory.
- `640b7391a8ef32acee0934fd058bb74fcdae9917` — package exports.
- `67fb5a2e72dd1146432c11d2154654a93242af63` — deterministic inventory tests.

Latest known green receipt before the final Build 021 test commit:

- `8952627142b9655a83a54ab9938ac335a13eb0b6` validating source `640b7391a8ef32acee0934fd058bb74fcdae9917` with Python 123 passed, V8 13, V9 10 and V10 JavaScript 13.

## Exact resume decision

Check whether a later validation receipt validates `67fb5a2e72dd1146432c11d2154654a93242af63` or this snapshot commit.

If green:

1. Record Build 021 as complete.
2. Start Build 022 — independent audit of Builds 006–019.

If red:

1. Read only the failing test output.
2. Repair Build 021.
3. Revalidate completely.
4. Do not start Build 022.

## Forward work purchase order

### Build 022 — Independent audit of Builds 006–019

Audit these capability groups separately:

1. evidence boundary and evidence register;
2. canonical identifiers;
3. public topology;
4. contradiction register;
5. deterministic persistence and DuckDB segments;
6. diagnostics, adapters and bridges;
7. study applicability and electrical studies.

For every group record exactly one decision: `ADOPT`, `ADAPT`, `REPAIR`, `DEFER` or `REJECT`.

Required output:

- machine-readable audit register;
- human-readable audit receipt;
- tests for deterministic ordering, complete coverage and legal decisions;
- no authority promotion merely because code executes.

### Build 023 — Canonical object and topology closure

- freeze canonical physical-object schema;
- freeze terminal and connectivity contracts;
- prove ordered traversal;
- prove sequential and leapfrog invariants;
- make topology validation block calculations;
- add independent verifier distinct from builder.

### Build 024 — Steady-state kernel authority decision

- shared Python/JavaScript fixtures;
- resistance, voltage drop, power loss and cold Voc parity;
- uncertainty and provenance parity;
- explicit authority declaration;
- compatibility role for non-authoritative implementation.

### Build 025 — Route and installation physics

- route-derived lengths only;
- positive/negative formation;
- product versus conductor properties;
- temperature and installation conditions;
- complete-circuit resistance and loss receipts.

### Build 026 — Distributed and transient boundary

- two-wire distributed parameters;
- loop geometry and formation;
- capacitance to frame and earth;
- surge sharing;
- arc restrike;
- declared frequency and validity ranges;
- standards cartridges separate from physics.

### Build 027 — Reporting and browser projection

- deterministic report projections;
- CSV, text and HTML first;
- PDF/DOCX as rendered outputs;
- browser rebuilt last;
- no hidden engineering mathematics.

## Extended builds after 027

### Build 028 — Standards cartridge registry

Clause references, edition, applicability, evidence and implementation status only. Do not reproduce protected standards text.

### Build 029 — Fleet aggregation and data laws

String, MPPT, inverter and site aggregation; DuckDB/Parquet contracts; additive versus non-additive measures; deterministic hashes.

### Build 030 — Electrical acceptance studies

Cold Voc, voltage drop, ampacity, insulation coordination and declared acceptance criteria. Physics result and acceptance decision remain separate.

### Build 031 — EMC, lightning and SPD studies

Study applicability, electrical distance, cable formation, screen/bonding assumptions, surge paths and SPD placement evidence.

### Build 032 — Arc fault and rapid shutdown studies

Arc interruption/restrike boundary, capacitance and stored energy, rapid-shutdown architecture and explicit unsupported-study states.

### Build 033 — Uncertainty and Monte Carlo

Interval propagation, scenario ensembles, sensitivity ranking, deterministic seeds and evidence-aware confidence statements.

### Build 034 — Investor-grade report DNA

Atomic claim/evidence/method/limitation structure, independent verification receipt, contradiction disclosure and controlled publication boundary.

### Build 035 — Final thin client

Browser reads canonical outputs and never recalculates hidden engineering quantities.

## Mandatory discipline for every build

```text
bounded scope
→ implementation
→ focused tests
→ complete validation
→ validation receipt
→ restore point
→ next build
```

A red or stale validation receipt blocks the next build.
