# Build 025 — Whole-Table Array Engine, Geometry First

## Decision

Build the authoritative geometry and array-layout engine before adding electrical physics.

The first usable calculation boundary is one complete PV table supporting up to 24 strings of 30 modules in series (720 modules), while retaining equipment-driven optionality for other sensible string and MPPT counts.

The browser remains a presentation/editor surface. The Python kernel owns geometry, routes, lengths, topology validation and later physics.

## Immediate target

Produce one complete table that can be configured with:

- 1 to 24 strings initially;
- 1 to 30 modules per string initially;
- arbitrary row and column arrangement sufficient to place all modules;
- portrait or landscape module orientation;
- configurable module dimensions and gaps;
- configurable table origin and rotation;
- movable inverter position;
- configurable MPPT count and string-to-MPPT assignment;
- sequential or leapfrog wiring strategy;
- explicit positive and negative conductor paths;
- deterministic geometric cable lengths that change when the inverter moves;
- deterministic geometry and route hashes.

The initial acceptance fixture is 24 strings × 30 modules = 720 modules.

## Governing rules

1. Geometry is authoritative.
2. Topology identifies what connects; geometry identifies where each connected conductor runs.
3. Sequential and leapfrog are route-generation strategies over the same module placement, not separate physics engines.
4. The inverter may be moved without changing string membership or MPPT assignments.
5. Moving the inverter must recompute only affected home-run geometry and lengths.
6. Positive and negative routes must remain separate objects so later EMC modelling can derive conductor separation, loop area and coupling.
7. No voltage-drop, resistance, inductance, capacitance, fault-current or SPD calculation is authoritative until the array geometry and route receipts are established.
8. No project-specific or confidential site data is embedded in the public engine.
9. Large projects are deterministic replications of validated table and inverter-block assemblies.

## Build sequence

### 025A — Geometry primitives

Create immutable, validated objects for:

- Point2D
- ModuleDimensions
- ModulePlacement
- TableLayoutRequest
- TableGeometryReceipt
- InverterPlacement

Generate deterministic rectangular module placement for an arbitrary module count, row count, column count, spacing, orientation, origin and rotation.

Acceptance:

- exactly 720 unique module placements for the 24 × 30 fixture;
- no overlapping module identifiers;
- deterministic coordinates and hash;
- moving the table origin or rotating the table gives a different geometry hash;
- repeated execution gives the same hash.

### 025B — String allocation on geometry

Map ordered modules to strings without changing module coordinates.

Acceptance:

- every module belongs to exactly one string;
- each string has exactly 30 ordered modules in the reference fixture;
- no duplicate or omitted module;
- assignment hash is deterministic.

### 025C — Sequential and leapfrog routes

Generate explicit module-to-module conductor polylines for both strategies.

Acceptance:

- all required terminal-to-terminal links exist;
- no invented branches;
- route vertices are deterministic;
- positive and negative free ends are explicit;
- sequential and leapfrog route hashes and lengths differ where geometry requires them to differ.

### 025D — Movable inverter and home runs

Add inverter coordinates and explicit positive/negative routes from every string free end to its assigned inverter input.

Acceptance:

- inverter movement changes home-run vertices, lengths and route hash;
- module placement and string topology hashes remain unchanged;
- total cable length is the sum of explicit route-segment lengths, not a browser estimate.

### 025E — MPPT/input allocation

Support equipment-profile-driven MPPT and input limits. The initial table target remains 24 strings, but the schema must permit at least 32 string inputs and 16 MPPTs for current large utility string-inverter profiles.

Acceptance:

- no duplicate physical input allocation;
- limits are read from equipment data;
- unused MPPTs are valid and visible;
- invalid assignments fail before physics.

### 025F — Installed-length layers

Add separately receipted installation allowances after pure geometric routes are stable:

- connector approach;
- bend allowance;
- support offsets;
- service loops;
- termination allowance;
- construction tolerance.

Geometric length, installed length and procurement length remain separate quantities.

### 025G — Physics hand-off

Only after 025A–F are validated, expose geometry/topology receipts to the physics engine for:

- conductor resistance and voltage drop;
- positive/negative loop geometry;
- loop area;
- self and mutual inductance;
- capacitance and coupling;
- common-mode and differential-mode behaviour;
- line-to-line and line-to-earth fault paths;
- SPD scenarios at inverter or combiner locations when supported by approved equipment data.

## Initial software limits

Application test limits, not universal electrical limits:

- modules per table: 2,000;
- strings per table: 64;
- modules per string: 60;
- MPPTs per inverter: 32;
- physical inputs per inverter: 64;
- inverters associated with a table: 8.

The first validated production fixture is limited to 24 strings × 30 modules and one movable inverter. Equipment profiles impose the real electrical limits.

## Required geometry receipt

```json
{
  "schema_version": "0.1.0",
  "table_id": "TABLE-001",
  "module_count": 720,
  "string_count_target": 24,
  "modules_per_string_target": 30,
  "rows": 24,
  "columns": 30,
  "orientation": "portrait",
  "origin_m": [0.0, 0.0],
  "rotation_deg": 0.0,
  "bounds_m": [0.0, 0.0, 35.9, 52.7],
  "geometry_hash": "sha256:..."
}
```

## Definition of done for the first milestone

A kernel caller can request a complete 24-string, 30-module-per-string table, receive 720 deterministic module placements, move the inverter, select sequential or leapfrog routing, and receive explicit conductor polylines with recomputed geometric cable lengths. No electrical physics is required for this milestone.