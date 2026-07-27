# FEED I vs FEED II — engineering comparison

## Purpose

This comparison prevents the two research feeds from being blended into one undifferentiated implementation. FEED I establishes the electromagnetic calculation discipline. FEED II adds wiring topology, the environmental layer stack, module frequency response, standards classification and asset/EMC practice.

## Separation rule

The working root engine remains unchanged. The existing `/v7-development/` page remains the previous V7 comparison reference. New executable work begins under `/v7-development/feed-i/` and is extended only after each feed has its own acceptance record.

## Capability comparison

| Topic | FEED I contribution | FEED II contribution | Build consequence |
|---|---|---|---|
| Dimensional integrity | Corrects capacitance aggregation and requires explicit units | Adds module impedance values spanning nH, nF and µF domains | Typed units and dimensional checks are mandatory |
| Epistemic status | Establishes measured/OEM/literature/derived/assumed/unknown states | Adds source-quality distinctions between standards, application notes, simulations and field measurements | Every input and output carries evidence status |
| Differential inductance | Closed-form two-wire route model plus PEEC for irregular geometry | Makes sequential, leapfrog, mirrored and crossover topology first-class | Geometry generates the differential circuit; topology is not merely a label |
| Common mode | Separate common-mode path and frequency-dependent inverter coupling | Adds cell-to-frame-to-rail-to-pile-to-soil layer stack and saline-soil behaviour | Common mode becomes a network, not one scalar inductance or capacitance |
| Water film | RC-sheet direction corrected; participation remains unvalidated | Adds measured salt/humidity evidence and multi-layer RC analogues | Film model remains research mode until measured or simulated |
| Module model | Requires measured module capacitance and OEM inverter data | Adds wide-frequency Rs–Rp–Cp, bypass-diode and cell-inductance evidence | Module is represented by frequency bands, not one capacitance |
| Transmission-line boundary | Rise time compared with propagation delay | Adds evidence that cable geometry dominates above roughly 100 kHz | Event classifier controls solver choice |
| String topology | Notes coil and route irregularity | Establishes leapfrog/sequential as an electrical design variable | Renderer and route generator must expose both patterns |
| Standards | Current IEC array, SPD, IMD and arc standards mapped | Distinguishes normative duties from qualitative guidance and designer-left quantities | Standards claims stored separately from engineering calculations |
| Validation | Impedance spectroscopy, TDR/SSTDR, leakage and controlled wetting | Adds side-by-side topology EMC tests and full-string inverter-terminal impedance measurement | Validation plan becomes a repository artefact |
| Asset register | Not central | Adds string-segment, connector and module-level digital-twin scope | Export schema must retain object identity and provenance |
| EMC | Common-mode impedance and resonance | Adds generic EMC framework and magnetic-field measurement gap | EMC outputs remain research/measurement-led, not compliance verdicts |

## Conflicts and corrections that govern the build

1. Capacitance multiplication must be unit-safe. A per-kW value multiplied by hundreds of kW yields microfarads, not nanofarads.
2. RC-sheet participation increases with conductivity and decreases with frequency. The characteristic scale is proportional to approximately `sqrt(conductivity / frequency)` for a fixed geometry and dielectric loading.
3. Fast sub-microsecond events strengthen, rather than weaken, the need for distributed modelling.
4. Strings sharing a DC link are not assumed to be identically paralleled at every frequency; coupling is represented by a frequency-dependent inverter termination.
5. The dry capacitance path remains present when wet. Any film contribution is additive and frequency dependent.
6. No fixed full-area wet capacitance may be presented as validated for the specific glass-glass bifacial module.
7. The 0.5 m² loop-area number is not to be presented as a PV-standard limit.
8. Application-note lead-length and copper-saving figures are evidence for feasibility and economics, not normative requirements.
9. Module internal differential capacitance and module-to-earth common-mode capacitance remain separate.
10. A complete utility string is not assigned one universal self-resonant frequency or characteristic impedance across all frequencies.

## Build order

### Stage A — FEED I foundation

- typed quantities and unit conversions;
- epistemic status registry;
- two-wire differential parameters using conductor diameter;
- low- and high-frequency inductance distinction;
- event rise-time/propagation-delay classifier;
- capacitance aggregation by module, string, MPPT and inverter;
- explicit common-mode/differential separation;
- unresolved-data and validation gates.

### Stage B — FEED II topology and layer stack

- sequential, leapfrog, mirrored and custom route generators;
- loop-area comparison by ordered segment;
- module lead-length feasibility check;
- cell/encapsulant/glass/film/frame/rail/pile/soil network schema;
- module frequency-band equivalent circuit;
- bypass-diode and junction-box objects;
- standards classification matrix;
- asset-register identities and EMC measurement hooks.

### Stage C — measurement-backed solver

- measured glass-glass wet/dry impedance;
- full-string inverter-terminal impedance sweep;
- controlled water conductivity dataset;
- PEEC reference for coils and transitions;
- SSTDR and leakage-current validation;
- inverter OEM common-mode termination data.

## Acceptance condition

No FEED II claim may silently overwrite a FEED I foundation. Where the feeds disagree, the repository records the conflict, governing correction, evidence source and acceptance test before executable behaviour changes.
