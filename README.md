# Solar Electrical Topology Analysis Engine

<!-- PROGRAMME-STATE:START -->
## Current programme state

This block is generated from [`programme-state.json`](programme-state.json). CI fails if the manifest, this status block or [`progress-dashboard.html`](progress-dashboard.html) drift apart.

| Field | Current authority |
|---|---|
| Build | **Build 025.5D1** |
| Stage | Generic equipment contract established; inverter-block aggregate active |
| Package | `0.4.0` |
| Last validated engineering commit | `d0c377b53e5d60b8c716c97c112c7996ba102f8f` |
| Active gate | **TS-004 — Add the complete inverter-block aggregate and receipt** |
| Next single goal | **TS-005 — Complete physical input and MPPT authority** |

### First complete product boundary

```text
660 Wp bifacial modules × 30 modules/string × 24 strings
= 720 modules
= 475.2 kWp DC
= one 352 kVA inverter block
DC/AC nameplate ratio = 1.35
```

### Latest declared validation envelope

| Suite | Result | State |
|---|---:|---|
| Python | 296 / 296 | PASS |
| V8 model | 13 / 13 | PASS |
| V8 authority reconciliation | 6 / 6 | PASS |
| V9 deterministic engine | 10 / 10 | PASS |
| V10 JavaScript | 13 / 13 | PASS |
| Clean installed wheel | 1 / 1 | PASS |

Comparison hash: `sha256:413aa93c98d1b9fd5f9ffee4f577cfe29a6e74f48bd927a3ebe7f541545d6366`

**Progress policy:** No numerical programme-completion percentage is claimed until explicit stage weights and acceptance evidence are encoded in this manifest.
<!-- PROGRAMME-STATE:END -->


An open-source, text-based engineering engine for modelling solar PV electrical topology from physical geometry and electrical parameters.

The purpose of this repository is to test whether conventional solar DC string design methods based mainly on conductor resistance, voltage drop and current carrying capacity omit electrical behaviour that becomes important in large systems.

The engine will model the electrical network from first principles using editable text inputs rather than GIS.

## Initial scope

The first version will model:

- PV modules connected in series as a string
- one or two strings connected to one MPPT input
- positive and negative conductor paths
- piecewise cable sections with different lengths and conductor spacing
- conductor resistance
- loop inductance
- conductor-to-conductor capacitance
- module and conductor capacitance to frame or earth
- frame and protective earth nodes
- inverter input capacitance and surge protection as optional elements
- steady-state voltage drop and power loss
- stored magnetic and electric energy
- frequency-domain impedance
- interruption and surge cases

## Modelling principle

The text model is the source of truth.

Physical inputs are entered first:

- module count
- module electrical data
- cable length
- conductor material and cross-sectional area
- positive-to-negative conductor spacing
- conductor-to-frame distance
- dielectric material
- frame bonding
- equipment connection points

The engine then derives the electrical model:

- R
- L
- C
- G where applicable
- propagation delay
- characteristic impedance
- stored energy
- network response

## Development sequence

1. Define a human-readable text schema.
2. Build a parser and validation layer.
3. Build a single-string 30-section ladder model.
4. Verify resistance, inductance and capacitance calculations independently.
5. Add two-string MPPT pairing.
6. Add frequency-domain and event analysis.
7. Add a simple browser dashboard.
8. Add JSON, CSV and text report export.

## Current public workbenches

- Root V6 complete-circuit workbench: [`index.html`](index.html)
- Independent V7 electromagnetic FEED I workbench: [`v7-development/feed-i/`](v7-development/feed-i/)
- Independent V8 leapfrog cable-schedule workbench: [`v8-leapfrog/`](v8-leapfrog/)

## Independent V7 electromagnetic build

The working root engine is frozen as the stable comparison reference. The earlier V7 page remains available under `/v7-development/`. New FEED I executable work is isolated under `/v7-development/feed-i/`; it must not import, overwrite or modify the root application.

The detailed plans are:

- [`v7-development/comparisons/BUILD_PLAN_FEEDS_I_II.md`](v7-development/comparisons/BUILD_PLAN_FEEDS_I_II.md)
- [`v7-development/comparisons/FEED_I_VS_FEED_II.md`](v7-development/comparisons/FEED_I_VS_FEED_II.md)
- [`v7-development/COMPARISON.md`](v7-development/COMPARISON.md)
- [`technical-commentary/leapfrog-v6-v7-notes.md`](technical-commentary/leapfrog-v6-v7-notes.md)

### FEED I foundation

FEED I establishes the calculation discipline:

- dimensional and unit safety;
- evidence and epistemic status on every input and output;
- closed-form two-wire differential parameters for long straight route sections;
- separate low-frequency and high-frequency inductance;
- separate differential and common-mode networks;
- event rise-time versus propagation-delay classification;
- capacitance aggregation by module, string, MPPT and inverter;
- explicit validation gates for glass-glass module capacitance, water-film participation, inverter termination and irregular coils.

### FEED II extension

FEED II extends the model into topology, environment, frequency response and asset practice:

- sequential, leapfrog, mirrored and custom wiring patterns;
- loop-area and induced-voltage comparison from generated geometry;
- module-lead feasibility as a procurement input, not a standards limit;
- cell, encapsulant, glass, water film, frame, rail, pile, soil and remote-earth layer stack;
- salt, humidity and contamination as electrical state variables;
- module `Rs–Rp–Cp`, cell/interconnect inductance, bypass-diode and junction-box parasitics;
- standards classification separating normative duties from application guidance and research hypotheses;
- string-segment, connector and module-level asset identities;
- EMC and measurement hooks without claiming a PV-specific emission limit.

## Independent V8 leapfrog cable-schedule build

V8 is a new independent workbench under [`v8-leapfrog/`](v8-leapfrog/). It does not modify V6 or V7. It isolates the cable-schedule consequence of leapfrog wiring before deeper electromagnetic calculations are merged back into any later core model.

The V8 question is deliberately narrow:

What is the external EPC-installed DC string cable difference between a conventional sequential 30-module string and a leapfrog 30-module string?

The governing rule is:

- sequential wiring places the two free string terminals at opposite physical ends of the row;
- leapfrog wiring brings both free terminals to the inverter-side end of the row;
- saving per string is approximately one full row span of external 6 mm² cable;
- inverter distance affects both modes, so it does not change the per-string saving;
- leapfrog does not remove both home-runs, it removes the extra far-end return conductor.

V8 adds:

- editable inverter distance;
- editable distance scenarios such as 10 m, 20 m and 30 m;
- east and west band lists;
- derived row span from module width and inter-module gap;
- sequential cable schedule;
- leapfrog cable schedule;
- comparison box showing external cable, resistance, voltage drop and loss difference;
- diagram showing why the free positive and negative terminals are no longer one row span apart;
- JSON export.

Default manufacturer inputs are treated as editable hypotheses. The module geometry, factory cable data, inverter input configuration, cable resistance and connector data are useful starting points, but final values require measured lead lengths, actual connector family, actual route, as-built string sequence and competent-person review.

A restore point was created before this build at [`restore_points/2026-07-27-v8-leapfrog/`](restore_points/2026-07-27-v8-leapfrog/).

### Governing corrections

The build is governed by the following corrections:

1. Capacitance aggregation is unit-safe. Per-kW nanofarads multiplied by hundreds of kilowatts produce microfarads, not nanofarads.
2. In an RC-sheet model, participating distance increases with conductivity and decreases with frequency.
3. Faster sub-microsecond events increase the need for distributed modelling.
4. Common-DC-link coupling is frequency dependent and cannot be reduced to a binary all-strings-paralleled rule.
5. Dry capacitance remains as the floor when the surface is wet: `Ctotal(f) = Cdry(f) + Cfilm(f, conductivity)`.
6. No fixed full-area wet capacitance is treated as measured for the selected glass-glass bifacial module.
7. Differential module capacitance and module-to-earth common-mode capacitance are never merged.
8. The 0.5 m² loop-area figure is not represented as a PV-standard numerical limit.
9. A complete utility string is treated as a distributed network where event bandwidth and route delay require it, not assigned one universal resonance.
10. Every standards statement records whether it is normative, guidance, first-principles engineering, research or measurement-dependent.
11. Leapfrog and sequential stringing must be separate topology states because the external cable schedule and differential loop area are different.
12. External EPC-installed DC string cable and factory-fitted module leads must remain separate length classes.

## Next standards-led studies

The next changes shall be studied as explicit engineering work packages rather than silently introduced as constants.

### Capacitance to earth and insulation monitoring

The engine shall distinguish positive-to-earth, negative-to-earth, common-mode and differential capacitance. Array capacitance to earth shall be aggregated at the actual insulation-monitoring boundary, not merely multiplied by strings per inverter without checking the inverter input topology.

The study shall add:

- dry and wet module-to-frame or earth capacitance
- positive and negative cable-to-earth capacitance by route segment
- manufacturer-declared, measured, geometry-derived and assumed provenance states
- inverter or MPPT monitoring-boundary selection
- independent MPPT, reverse-current-blocking and common-DC-bus cases
- total capacitance seen by the insulation monitoring device
- insulation resistance warning and trip thresholds
- IMD maximum permissible system capacitance and margin
- warning and trip response-time studies
- separate Riso and capacitance branches rather than treating leakage resistance and capacitance as interchangeable

No universal module capacitance, wet multiplier or cable-to-earth capacitance shall be described as an IEC value unless directly supported by a cited source. Assumed values shall remain visible and replaceable.

### Loop geometry, inductance and transient overvoltage

The topology shall remain the source of loop-area evidence. The study shall derive loop area by ordered segment, including local conductor separation, coils, structure drops, crossings, trench routes and the return path.

The study shall add:

- differential inductance by segment
- common-mode inductance against frame and earth
- bonding-conductor route and separation
- concentrated coil geometry, diameter, turns and whether both poles are coiled together
- maximum local loop width and percentage of route with paired conductors
- SPD lead inductance and residual voltage contribution
- comparison of lumped and distributed models using propagation delay and disturbance rise time

### SPD critical length and electrical distance

The engine shall calculate the maximum routed electrical distance from the PCE to the furthest module connection point and compare it with the applicable critical-length method. Straight-line site distance shall not replace routed conductor length where topology is available.

The study shall add:

- site lightning-density input with provenance
- critical length and route-length ratio
- SPD location along the string route
- module, connector, cable accessory and inverter impulse-withstand values
- SPD protection level at the relevant surge current
- voltage contribution from connection lead inductance
- additional-SPD scenarios for long outlying strings

### Complete-series-circuit resistance and voltage drop

Voltage drop shall be calculated across the complete current path, including both external conductors, module factory leads, extension leads, connector contacts, terminations and any series protective or isolation devices.

The study shall add:

- cable-only and complete-circuit results
- separate temperatures for module-adjacent cable, home runs, buried sections, leads and connectors
- voltage-drop percentage against string Vmp
- energy-loss aggregation by string, MPPT, inverter and plant
- uncertainty and evidence status for connector resistance and lead lengths

### Inverter input topology, backfeed and reverse current

The engine shall explicitly model whether inverter inputs are independently converted, reverse-current blocking, or internally connected to a common DC bus.

The study shall add:

- MPPT and DC-input connectivity graph
- strings and sub-arrays sharing a current path
- PCE backfeed-current rating
- PV reverse current from parallel strings or sub-arrays
- isolation boundaries
- overcurrent-protection study inputs
- unknown-topology mode that displays alternative bounding cases instead of choosing one silently

### Environmental and installation classes

Every route segment shall carry an installation environment because temperature, capacitance, insulation resistance, corrosion, mechanical risk and maintenance exposure depend on the physical route.

Initial classes shall include:

- under-module
- open air
- metallic tray
- insulating tray
- conduit
- duct
- direct buried
- wet trench
- floodable
- structure transition
- enclosure entry

### Connector and termination objects

Connector interfaces shall become topology objects rather than only a count multiplied by a resistance assumption.

The study shall include:

- positive or negative pole
- manufacturer and connector family
- factory-fitted or field-fitted status
- mating compatibility
- location and environmental exposure
- contact-resistance provenance
- installation tool, torque and inspection state where available

### Standards and evidence presentation

Every result shall identify whether it is:

- a normative requirement
- a standards-guided engineering calculation
- an advanced or research model

Every calculated output shall carry its inputs, method, provenance, uncertainty and status. The engine shall not present a standards compliance verdict where required manufacturer data, measured geometry or competent-person review is absent.

## Boundaries

This repository is a calculation and research tool. It does not provide a project-specific design approval, protection coordination study, compliance verdict or engineering warranty.
