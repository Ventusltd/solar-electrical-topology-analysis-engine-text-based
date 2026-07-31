# Installed Cable Length Research — Parallel Track

Status: active in parallel with Build 023 engine recovery
Tracking issue: #8

## Authority boundary

1. Topology determines which terminals connect.
2. Geometry determines the minimum valid route.
3. Installation rules transform the minimum route into the constructed route.
4. Physics uses constructed length.
5. Procurement uses constructed length plus explicit procurement policy.
6. Browser renders authoritative results; it does not invent route length.

## Canonical length stack

```text
minimum_geometric_length
+ topology_route_delta
+ factory_lead_deficit
+ support_path_delta
+ bend_allowance
+ strain_relief_allowance
+ service_loop_allowance
+ termination_allowance
+ movement_allowance
+ installation_tolerance
= constructed_length

constructed_length
+ procurement_spare
+ drum_or_cut_rounding
= procurement_length
```

Every term shall be independently reported and may be zero. Percentage-only blanket factors are prohibited unless the evidence profile explicitly requires one.

## Measurement modes

### Sequential

Connect adjacent modules in electrical order. Measure terminal-to-terminal through the selected support path, accounting for connector orientation and available positive/negative factory leads. Row-end transitions are independent route segments.

### Leapfrog

Connect alternating modules, then return through the skipped sequence. Measure every actual terminal pair rather than multiplying module pitch. The model must capture long spans, reverse-direction runs, crossings, support changes and unequal lead utilization.

### Harnessed

Represent a harness as a trunk plus tap objects. Measure trunk route once, each tap separately, and include branch connector/termination allowances. Harness aggregation shall not duplicate shared trunk length.

### Loose cable

Represent each conductor route independently. Positive and negative conductors may share a support path but can have different terminal offsets, service loops or termination allowances.

## Installation-condition profile

Each route segment shall carry a versioned profile containing, where applicable:

- mounting system: fixed tilt, tracker, floating, rooftop;
- support medium: module frame, rail, torque tube, tray, conduit, duct or trench;
- clip/support spacing and maximum unsupported span;
- permitted sag and cable clearance;
- minimum bend radius and bend count;
- connector orientation and mating axis;
- UV, water, abrasion and mechanical-protection constraints;
- thermal expansion range;
- tracker articulation envelope;
- trench depth, duct occupancy and separation;
- installation and survey tolerance;
- termination and maintenance access rules.

## Data contract candidates

```text
CableRoute
  route_id
  connection_id
  conductor_role
  topology_mode
  ordered_route_points
  segment_profiles
  minimum_geometric_length_m
  constructed_length_m
  procurement_length_m
  receipt_id

LengthAdjustment
  adjustment_id
  category
  basis
  value_m
  evidence_ref
  profile_version

FactoryLead
  object_id
  terminal_id
  polarity
  available_length_m
  usable_length_m
  connector_type
  exit_vector

Harness
  harness_id
  trunk_route_id
  tap_route_ids
  connector_map
  current_limit
  fuse_map
```

## Initial deterministic rules

1. Never use module-centre distance as cable length when terminal coordinates exist.
2. Never treat leapfrog length as sequential length multiplied by a constant.
3. Factory lead length offsets only the route portion physically supplied by that lead.
4. Shared harness trunk length is counted once.
5. Bend allowance is geometry-derived where bend radii and route points are known.
6. Tracker movement allowance is based on swept geometry, not a generic percentage.
7. Service loops and termination allowances are endpoint-specific.
8. Construction tolerance and procurement spare are separate quantities.
9. Electrical voltage-drop, loss and impedance calculations use constructed length, not procurement length.
10. Every fallback assumption must produce a warning and evidence receipt.

## Research work packages

### R1 — Field measurement taxonomy

Define how installers measure sequential, leapfrog, harness and loose-cable routes from module terminals through supports to inverter/combiner endpoints.

### R2 — Factory lead utilization

Model asymmetric positive/negative leads, connector positions, portrait/landscape orientation, module rotation and extension-lead triggers.

### R3 — Precise laying conditions

Create profiles for frame-clipped, rail-clipped, tracker torque-tube, tray, conduit, duct and trench routes.

### R4 — Allowance derivation

Separate geometry-derived allowances from rule-based allowances: bends, strain relief, drip loops, service loops, glands, terminations, movement and tolerances.

### R5 — Fixtures

Create paired fixtures with identical module geometry but different topology and laying profiles. Required cases:

- sequential portrait modules;
- sequential landscape modules;
- leapfrog portrait modules;
- leapfrog with reversed connector orientation;
- harness trunk with unequal taps;
- loose positive/negative conductors;
- fixed-tilt frame route;
- single-axis tracker articulation;
- tray-to-conduit transition;
- conduit-to-trench transition.

### R6 — Receipt

For every final cable quantity report:

- terminal pair and topology edge;
- route point sequence;
- minimum geometric length;
- each adjustment and evidence basis;
- constructed length;
- procurement policy and final quantity;
- warnings and unresolved assumptions;
- canonical topology and geometry hashes.

## Supporting evidence already supplied

- Beilen cable report: differentiates buried conduit, perforated tray, direct burial, trench depth, duct spacing and crossing thermal conditions.
- ERA 69-30 Part V: installation conditions, spacing, ducts, direct burial, air installation, ambient conditions and current-rating implications.
- IEC 60364-7-712: PV string/array cable definitions, wiring-system requirements, voltage-drop and maintainability context.
- IEC 62548-1: current PV array design requirements, cable and wiring-system clauses, mechanical design and minimum loop-area treatment.
- IEC TS 62738: utility-scale routing, string wiring harness definition, combiner/harness arrangements, tracker and cable-management considerations.

## Parallel execution rule

This research track shall produce contracts, evidence profiles and fixtures without blocking Build 023. Engine recovery continues independently. Integration occurs only through versioned canonical objects and tests.