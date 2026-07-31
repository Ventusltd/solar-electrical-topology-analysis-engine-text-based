# Refinement 06 — Build 025.5 Authority Consolidation

Timestamp: 2026-07-31 20:59 +0100

## Purpose

Build 025 has completed the first authoritative geometry, topology and routing boundary. The next task is not to add more physics immediately. The next task is to consolidate the authority chain so Builds 026 and 027 do not inherit ambiguous public claims, competing code paths, weak evidence vocabularies or packaging assumptions.

Build 025.5 is therefore an authority-consolidation phase between the completed Build 025 foundation and the future standards and electromagnetic engines.

## Current position

The following capabilities are accepted as implemented:

- deterministic whole-table module geometry;
- explicit string membership and electrical traversal;
- physical inverter-input and MPPT allocation;
- separate positive, negative and series-interconnect routes;
- movable-inverter routing dependency;
- field-installed, factory-fitted, installed and procurement length layers;
- signed and absolute winding-area metrics;
- terminal-geometry provenance fields;
- deterministic geometry, topology, routing and calculation receipts;
- exact-input numerical stability across the permanent regression range;
- pull-request validation before authoritative calculation changes are merged.

The numerical-stability refinement is complete. The remaining refinements are active.

## Refined dependency model

The system is not one inflexible serial pipeline. Geometry, topology, equipment data and evidence form a dependency graph.

```text
physical geometry + design intent + equipment constraints
                         ↓
                  validated topology
                         ↓
                 explicit routing
             ↙           ↓            ↘
steady-state physics   standards     EMC and surge physics
```

Each calculation or validation rule shall declare its required upstream receipts and evidence. A rule shall run only when its dependency set is satisfied.

Standards validation does not always require the complete electromagnetic engine. Voltage scope, SPD route-length checks, conductor pairing and topology-derived overcurrent rules may proceed when their specific dependencies are available.

## Browser command contract

The browser may create user intent but may not create engineering authority.

Accepted interaction flow:

```text
browser command or edit request
→ kernel validation
→ authoritative object mutation
→ new deterministic receipt
→ browser rendering
```

Examples of browser commands include moving an inverter, selecting a wiring strategy or assigning a string to an input. The browser shall not independently generate the resulting route, cable length, topology or validation result.

## Deterministic receipt and execution envelope

A deterministic engineering receipt shall exclude runtime-dependent metadata.

```text
EngineeringReceipt
- deterministic content
- method and schema versions
- source receipt hashes
- engineering inputs and outputs
- content hash

ExecutionEnvelope
- timestamp
- actor or workflow
- repository commit
- execution environment
- engineering receipt hash
```

Routine CI runs should preserve execution evidence as GitHub checks or workflow artifacts. A repository receipt commit should represent a meaningful release, restore point or approved authority transition rather than every unchanged validation execution.

## Build 025.5 sequence

### 025.5A — V8 truth boundary

V8 shall remain reproducible but shall no longer present field-installed external-cable reduction as total cable or total copper saving.

For the current 24 by 30 reference fixture, the public comparison shall present together:

```text
field-installed conductor reduction    798.288 m
factory-fitted conductor increase       845.088 m
total circuit conductor increase         46.800 m
absolute winding-area reduction           79.8 percent
```

The exact values remain fixture-specific and shall be generated from the current authority where possible rather than duplicated as hidden constants.

Required public wording:

- `field-installed external cable reduction` instead of unqualified `cable saving`;
- factory-fitted interconnect length is excluded from the V8 external-cable quantity;
- total-conductor reconciliation is visible beside the V8 result;
- resistance and loss reductions apply only to the represented external-cable portion;
- loop-area results identify unresolved terminal geometry and plan-coordinate assumptions;
- passing legacy tests means reproducibility, not current canonical authority.

### 025.5B — Installable Build 025 authority

Move Build 025 production logic into the installable `src/solar_topology` package.

Target structure:

```text
src/solar_topology/array/
    geometry.py
    assignment.py
    topology.py
    input_allocation.py
    route_types.py
    route_geometry.py
    routing.py
    installed_length.py
    engine.py
```

Root-level modules may remain temporarily as compatibility shims. They shall contain no independent formulas or authority logic.

### 025.5C — Clean wheel gate

CI shall build and install the wheel in a clean environment outside the repository, import the public array API, execute the 24 by 30 comparison, verify deterministic results and prove that no authoritative import resolves from the repository root.

### 025.5D — Resistance evidence authority

Replace loose resistance provenance strings with a controlled, versioned resistance-evidence object.

Minimum fields:

```text
product_id
r20_ohm_per_m
resistance_basis
manufacturer nominal or maximum state
source reference and revision
verification state
temperature coefficient basis
measurement conditions where applicable
```

Controlled resistance bases:

```text
independently_measured
manufacturer_declared
standard_maximum
ideal_bulk_estimate
assumed
unresolved
```

Legacy ideal-bulk calculations shall remain reproducible but visibly classified as lower-bound screening estimates.

### 025.5E — Evidenced dimensional geometry

Add independently evidenced module-terminal coordinates, table-plane tilt and site-three-dimensional route support. Geometry receipts shall declare `plan_2d`, `table_plane_2d` or `site_3d`.

No universal `1 / cos(tilt)` adjustment shall be applied to all route lengths. Lengths shall arise from explicit three-dimensional vertices.

### 025.5F — Electromagnetic quantity boundary

Keep separate:

- signed area in a declared plane;
- absolute winding area;
- oriented signed area vector;
- projected area normal to a declared field;
- spatially weighted magnetic flux;
- induced voltage derived from time-varying flux.

Build 027 shall not multiply one loop-area number by a generic lightning factor and call the result authoritative.

## Version-status matrix

The public repository shall expose a version-status matrix:

```text
V6   historical reference — ideal-bulk complete-string prototype
V7   historical reference — array and electromagnetic visualisation
V8   historical/reference — field-installed external-cable comparison
V9   reference/candidate — deterministic inverter-block sandbox
V10  canonical candidate — evidence-bound Python kernel and receipts
```

A passing test suite proves that a version remains reproducible. It does not make that version canonical.

## Plant scaling refinement

Large plants shall be formed by deterministic composition of validated tables, inverter blocks and power blocks. Identical assemblies may be deduplicated by receipt hash, but the engine shall not assume that every plant is composed solely of identical replicated units.

## Build 026 entry gate

Build 026 standards implementation may begin only after:

1. V8 publicly distinguishes field-installed reduction from total conductor;
2. Build 025 is importable from a clean installed wheel;
3. root-level modules no longer contain independent authority logic;
4. the resistance basis is controlled and visible in authoritative receipts;
5. required GitHub checks are visible on authoritative changes.

After these gates, Build 026 should proceed through rule schemas and dependency declarations, validation states, current and backfeed evidence, overcurrent rules, protection inequalities, SPD route-length checks, voltage scope and edition-conflict reporting.

## Immediate implementation order

1. implement the V8 truth boundary and regression tests;
2. package Build 025 under `src/solar_topology/array`;
3. add the clean-wheel CI gate;
4. implement resistance-evidence authority;
5. add terminal and three-dimensional geometry;
6. begin Build 026;
7. begin Build 027 only after field-source models and applicability limits are defined.

## Acceptance

Build 025.5 is complete only when the public outputs, installable artifact, evidence vocabularies, CI gates and authority labels all identify one coherent production path from geometry through routing into later standards and physics.