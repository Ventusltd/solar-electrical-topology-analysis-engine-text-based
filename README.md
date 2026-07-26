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

No confidential project drawings, photographs, site identifiers or commercially restricted source material are to be stored in this repository. Examples must remain generic and reproducible from declared inputs.

## Status

Active development. The browser is an engineering workbench for topology, complete-circuit resistance, voltage drop, differential and common-mode inductance, capacitance to earth, insulation-monitoring screening and transient-study preparation.
