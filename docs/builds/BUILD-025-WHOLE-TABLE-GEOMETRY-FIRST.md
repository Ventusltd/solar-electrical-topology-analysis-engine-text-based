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
10. Cable length and enclosed loop area are independent outputs; neither may substitute for the other.
11. Standards arithmetic must operate on an evidenced electrical topology and physical route geometry, never on an abstract string count alone.

## Standards-ready geometry contract

Every conductor route segment shall preserve enough information for later standards, fault-current and EMC calculations:

```text
segment_id
string_id
polarity
start_xyz
end_xyz
route_class
installation_method
buried
screened
earthed_metallic_containment
bonded_screen
support_path_id
geometric_length_m
```

The initial default installation classification may be `exposed_unshielded`, but the assumption must be explicit in the receipt.

This segment model must later support:

- positive/negative conductor separation;
- signed and absolute enclosed loop area;
- parallel-run distance;
- buried and screened length exclusions;
- effective route length for SPD checks;
- self and mutual inductance;
- capacitive and common-mode coupling;
- line-to-line and line-to-earth fault paths.

## Topology nodes reserved now

The array schema must distinguish physical and electrical junctions. It shall reserve explicit node types for:

- module positive and negative terminals;
- string free ends;
- connector pairs;
- parallel junctions;
- string fuses;
- group overcurrent devices;
- combiner buses;
- MPPT physical inputs;
- inverter DC bus;
- SPD connection points;
- protective-earth and bonding nodes.

Two strings assigned to isolated inverter inputs are not equivalent to strings paralleled ahead of one input or protective device.

## Build sequence

### 025A — Geometry primitives

Create immutable, validated objects for:

- Point2D / Point3D-ready coordinates;
- ModuleDimensions;
- ModulePlacement;
- TableLayoutRequest;
- TableGeometryReceipt;
- InverterPlacement.

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
- terminal polarity and ordered traversal are explicit;
- assignment hash is deterministic.

### 025C — Sequential and leapfrog conductor geometry

Generate explicit module-to-module conductor polylines for both strategies, including module leads, row transitions, string exits and free ends.

Acceptance:

- all required terminal-to-terminal links exist;
- no invented branches;
- route vertices are deterministic;
- positive and negative free ends are explicit;
- sequential and leapfrog route hashes differ where geometry requires them to differ;
- both strategies produce separate positive and negative route objects.

### 025D — Movable inverter and home runs

Add inverter coordinates and explicit positive/negative routes from every string free end to its assigned inverter input.

Acceptance:

- inverter movement changes home-run vertices, lengths and route hash;
- module placement and string topology hashes remain unchanged;
- only affected home-run geometry is recomputed;
- total cable length is the sum of explicit route-segment lengths, not a browser estimate.

### 025E — Geometry comparison receipt

For sequential and leapfrog strategies report independently:

- positive conductor length;
- negative conductor length;
- total circuit length;
- inverter home-run length;
- maximum conductor separation;
- mean conductor separation;
- signed enclosed loop area;
- absolute enclosed loop area;
- crossings;
- parallel-run distance;
- route and geometry hashes.

A shorter route may still have worse electromagnetic geometry.

### 025F — MPPT/input allocation

Support equipment-profile-driven MPPT and input limits. The initial table target remains 24 strings, but the schema must permit at least 32 string inputs and 16 MPPTs for current large utility string-inverter profiles.

Acceptance:

- no duplicate physical input allocation;
- limits are read from equipment data;
- unused MPPTs are valid and visible;
- isolated inputs and shared parallel nodes are distinguishable;
- invalid assignments fail before physics.

### 025G — Installation classifications and installed length

Add separately receipted route properties and installation allowances:

- exposed, buried, screened and bonded-metallic route classes;
- connector approach;
- bend allowance;
- support offsets;
- service loops;
- termination allowance;
- construction tolerance.

Geometric length, installed length and procurement length remain separate quantities.

### 025H — Physics and standards hand-off

Only after the geometry and topology receipts are validated, expose them to later engines for:

- conductor resistance and voltage drop;
- loop area and inductance;
- mutual inductance and capacitance;
- common-mode and differential-mode behaviour;
- line-to-line and line-to-earth faults;
- reverse-current and backfeed calculations;
- SPD requirement and surge-path calculations.

## Reserved IEC 62548-1 validation model

These rules are not to be implemented as authoritative physics inside Build 025, but the geometry and topology schemas must support them without redesign.

### String overcurrent requirement

Reserve the 2023-edition system-level form:

```text
I_F_STRING + I_BF_TOTAL > I_MOD_MAX_OCPR

I_F_STRING = (N_S - 1) × I_STRING_MAX
I_STRING_MAX = K_I × I_SC_MOD
K_I = 1.25 × K_Corr
I_BF_TOTAL = I_BF_PCE + I_BF_EXT_BAT
```

`I_BF_PCE` and `I_BF_EXT_BAT` shall be explicit evidence-backed inputs. Missing values must later produce an incomplete-evidence result, not an unqualified pass. A zero-backfeed value must retain manufacturer/manual provenance or be visibly marked as an assumption.

### K_Corr provenance

Reserve site and geometry inputs for later K_Corr derivation:

- latitude;
- tilt and azimuth;
- module technology and bifaciality;
- row spacing and ground-cover ratio;
- albedo and ground cover;
- rear irradiance or simulation result;
- minimum annual beam-to-array-normal angle;
- cell-temperature envelope;
- air-mass envelope.

For non-optimally oriented monofacial arrays, reserve support for:

```text
K_Corr = 0.1 + 0.9 cos(alpha)
```

Bifacial cases requiring simulation must not silently default to 1.0.

### Grouped strings and protection

The later protection engine must evaluate the actual electrical node structure and module technology. It must not infer parallel grouping from MPPT labels alone. Grouped-string overcurrent-device sizing and crystalline/thin-film applicability shall be standards-versioned and evidenced.

### Wiring loops

Positive and negative conductors of the same string must be geometrically comparable so the engine can evaluate the requirement to minimise conductive loop area. Associated bonding and earth conductors must be capable of inclusion in later route analysis.

### SPD route-length check

Reserve a later computed check using:

```text
L_crit = 115 / N_g   building-attached
L_crit = 200 / N_g   free-standing
```

The effective counted length `L` must be calculated segment by segment and exclude qualifying buried, screened, armoured or bonded-metallic portions. `N_g` is a site input with provenance. Fitting an SPD by default does not remove the need to record the normative calculation.

### Voltage scope

The later validation engine shall not certify designs above 1500 V DC under IEC 62548-1 without an explicit alternate standards route and evidence set.

## Standards-version authority

Every future rule result shall identify its source, edition and clause, for example:

```json
{
  "standard": "IEC 62548-1",
  "edition": "2023",
  "amendment": "AMD1:2025",
  "clause": "6.5.3.1",
  "rule_id": "string_overcurrent_requirement"
}
```

IEC TS 62738:2018 must remain a separate rule source because it references an older IEC 62548 edition. Conflicts between rule sources shall be surfaced in the ValidationReceipt rather than silently merged.

## Subsequent builds

### Build 026 — Standards validation

After Build 025 is complete, implement:

- K_I and K_Corr derivation/provenance;
- string, sub-array and array fault-current families;
- string overcurrent requirement;
- OCPD sizing and grouped-string validation;
- missing backfeed evidence handling;
- voltage-scope boundaries;
- SPD L versus L_crit;
- standards-edition conflict reporting.

### Build 027 — EMC and fault physics

Only after geometry and standards inputs are evidenced, implement:

- loop inductance;
- mutual inductance;
- capacitive coupling;
- common-mode paths;
- surge current paths;
- SPD lead inductance and residual voltage;
- fault energy and clearing behaviour.

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
  "schema_version": "0.2.0",
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
  "default_installation_method": "exposed_unshielded",
  "geometry_hash": "sha256:..."
}
```

## Definition of done for the first milestone

A kernel caller can request a complete 24-string, 30-module-per-string table, receive 720 deterministic module placements, move the inverter, select sequential or leapfrog routing, and receive explicit positive and negative conductor polylines with recomputed geometric cable lengths and loop-geometry metrics. No electrical physics is required for this milestone.