# Work Card 004 — Evidence and Complete-Circuit Calculation

## Status

Third executable V10 build slice after the canonical circuit foundation and cartridge traversal.

Restore point created before this slice:

- branch: `restore/2026-07-30-pre-v10-evidence-calculation-receipts`
- commit: `afa54a057e0aa02bd264958590dc1782c281fd7d`

All implementation work is committed directly to `main` under the binding main-branch-only rule.

## Objective

Attach complete-circuit resistance, voltage drop and resistive loss to the already validated canonical circuit and independently derived ordered traversal. Preserve the evidence vocabulary and produce an immutable deterministic calculation receipt.

## Governing sequence

```text
canonical objects and terminals
→ circuit validation
→ independent graph traversal
→ ordered source segments
→ segment-level resistance
→ complete-circuit aggregation
→ immutable calculation receipt
```

No calculation may accept a free total cable length or bypass circuit/traversal validation.

## Deliverables

### Evidence vocabulary

`src/solar_topology/evidence.py`

- preserves the original source vocabulary and value;
- maps SegmentRow provenance into canonical evidence classes;
- maps V10 JavaScript quantity provenance without promoting JavaScript authority;
- separates evidence class from verification state;
- calculates an explicit weakest-input evidence floor.

### Calculation receipt

`src/solar_topology/calculation_receipts.py`

- immutable segment and complete-circuit result records;
- circuit hash and traversal identity;
- ordered terminal, connection and segment identifiers;
- source evidence for every segment;
- formula identifiers;
- deterministic JSON and SHA-256 receipt hash;
- no timestamp inside canonical evidence.

### Complete-circuit calculator

`src/solar_topology/circuit_calculations.py`

- refuses an invalid traversal;
- independently re-derives the graph order before calculating;
- reads every source segment from the canonical circuit model;
- uses declared finished-cable R20, installed conductor length and segment temperature;
- includes connector contacts and their temperature correction;
- reports conductor resistance and connector resistance separately;
- aggregates complete-circuit R, I×R voltage drop and I²R loss;
- carries source warnings and the weakest input evidence class;
- accepts no user-entered total route length.

### Cross-language comparison

- shared fixture: `v10-development/fixtures/steady_state_cross_language_v1.json`;
- Python and JavaScript independently execute the common 20 °C conductor-only formula subset;
- comparison is evidence only and does not promote the JavaScript candidate kernel.

## Known-answer canaries

At 17.35 A, with 30 modules and 1.4 m positive and negative factory leads per module:

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

The canaries include external conductors, all factory leads and all connector contacts. They are generic regression fixtures, not project approvals.

## Explicit boundaries

- no standards-compliance conclusion;
- no current-carrying-capacity or derating selection;
- no aluminium temperature coefficient;
- no uncertainty propagation beyond evidence-state preservation;
- no transient, inductive or capacitive calculation;
- no browser or report renderer changes;
- no changes to V6, V7, V8 or V9 implementations;
- no project-specific or confidential data.

## Acceptance criteria

- complete Python suite passes;
- V8, V9 and V10 JavaScript regression suites pass;
- sequential and leapfrog known-answer canaries pass;
- calculations fail after invalid or forged traversal;
- canonical receipt and hash are deterministic;
- shared Python–JavaScript fixture passes in both languages;
- the restore point and final validation receipt are recorded.

## Exact next work after this slice

1. Add interval uncertainty propagation for current, R20, length, temperature and connector resistance.
2. Define operating-state inputs including string Vmp and voltage-drop percentage.
3. Add calculation-receipt persistence and deterministic DuckDB/Parquet read-back verification.
4. Reconcile the duplicate Python geometry representations without changing proven cartridge behaviour.
5. Keep standards cartridges, reports and browser consumption downstream.
