# Solar Electrical Topology Analysis Engine

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

## Boundaries

This repository is a calculation and research tool. It does not provide a project-specific design approval, protection coordination study, compliance verdict or engineering warranty.

No confidential project drawings, photographs, site identifiers or commercially restricted source material are to be stored in this repository. Examples must remain generic and reproducible from declared inputs.

## Status

Initial architecture stage.
