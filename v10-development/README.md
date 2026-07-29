# V10 Development — Ventus DC String Engine

Status: preparation only. No V6, V7, V8 or V9 computation code is changed by this workstream until the owner gives the explicit instruction to proceed.

## Purpose

V10 will turn the current solar electrical topology workbenches into a stronger, wider and continuously auditable PV DC computation engine called the **Ventus DC String Engine**.

The engine must preserve the existing development lineage:

- V6 remains the stable complete-circuit reference.
- V7 remains the independent electromagnetic FEED development branch.
- V8 remains the independent leapfrog cable-schedule workbench.
- V9 remains the sandbox for integration and experimentation.
- V10 must be built only after the existing versions have been independently acid-tested and their useful methods, corrections and evidence states have been mapped.

## Governing architecture

The engine shall behave like a small engineering federation rather than one opaque calculator.

Its core chain is:

```text
physical objects
→ geometry
→ terminals and connectivity
→ ordered current paths
→ electrical parameters
→ operating and event models
→ evidence status
→ validation gates
→ reports and development feedback
```

The computation engine must not silently replace unknowns with confident constants. Every important input and output shall carry:

- value and unit;
- source and evidence path;
- manufacturer-declared, measured, geometry-derived, standards-derived, assumed or research status;
- uncertainty or bounding case where applicable;
- model version;
- validation state;
- date last reviewed.

## Spider behaviour

V10 shall borrow the federation-map discipline without copying its UI blindly.

The engine should maintain a graph of:

- physical component nodes;
- electrical terminal nodes;
- conductor and connector edges;
- module, string, MPPT and inverter boundaries;
- evidence-source nodes;
- standards and manufacturer-data dependencies;
- calculation-method dependencies;
- validation and test dependencies.

A calculation result must be traceable backwards through this graph to the physical topology, assumptions, formulas and evidence that produced it.

## Monthly learning cycle

At least once per month, an automated or manually triggered process should:

1. inspect this repository and designated related Ventus repositories;
2. identify changed formulas, schemas, standards notes, data sources and open engineering questions;
3. check designated public manufacturer, standards-preview, research and industry sources without copying licensed material into the repository;
4. record candidate intelligence in a dated text log;
5. classify each finding as accepted, rejected, uncertain, duplicate or requiring measurement;
6. create development goals from accepted or unresolved findings;
7. run regression and invariant tests before any calculation change is promoted;
8. commit only verified reports and approved changes.

The monthly process is an intelligence and quality-assurance loop. It must not autonomously alter engineering formulas merely because a web source changed.

## Initial V10 computation domains

V10 should eventually unify and extend:

- sequential, leapfrog, mirrored and custom string topology;
- exact module-lead and external home-run geometry;
- complete-series-circuit resistance and voltage drop;
- connector and termination resistance;
- cable current-carrying capacity and thermal environments;
- differential and common-mode inductance;
- conductor-to-conductor and conductor-to-earth capacitance;
- insulation resistance and insulation-monitoring boundaries;
- distributed-line classification by event rise time and propagation delay;
- lightning and induced-voltage loop-area assessment;
- SPD critical length, placement, protection level and lead inductance;
- inverter input topology, reverse current, backfeed and common-bus alternatives;
- fuse and overcurrent-protection applicability;
- arc, interruption, restrike and stored-energy cases;
- module, connector, cable and inverter impulse coordination;
- plant-scale aggregation of cable length, copper, loss, uncertainty and exposure;
- standards-linked evidence reports without issuing an unsupported compliance verdict.

## Required preparation outputs

Before V10 computation code starts, the workstream shall produce:

- a complete V6–V9 feature and formula inventory;
- a dependency map showing duplicated and conflicting methods;
- a formal input and output schema;
- a units and dimensional-analysis policy;
- a provenance and epistemic-status schema;
- an invariant and regression-test catalogue;
- accepted reference cases with independently calculated expected results;
- a source registry and licence boundary;
- a monthly intelligence log;
- a prioritised development-goals register;
- a promotion process from sandbox to stable release.

## Safety boundary

This is an engineering calculation and research engine. It shall support competent professional judgement but shall not represent itself as a project-specific design approval, standards certification, protection-coordination study, construction release or engineering warranty.
