# Architecture Decision — EMC, Fault Current and SPD Modelling Focus

## Decision

The platform shall not spend engineering effort or browser/GPU compute on ornamental 3D graphics.

The accepted visual language remains the existing V7 overview and V8 detailed connection geometry. Future renderer work may improve scale, picking, layering and responsiveness, but it shall preserve those established 2D engineering views rather than replace them with fabricated three-dimensional scenes.

## Engineering purpose

The platform exists to establish electrical connection integrity and compute electrical behaviour from real, validated conductor geometry.

Priority order:

1. Validate physical objects, terminals, polarity and ordered electrical connections.
2. Derive explicit positive and negative conductor paths from existing accepted topologies and installation geometry.
3. Calculate constructed cable lengths, including documented leads, harnesses, extensions, bends, service loops, trays, ducts and trenches.
4. Derive electromagnetic parameters from the relative geometry of both conductors.
5. Model fault-current paths and surge protective device behaviour with and without installed SPDs.
6. Produce deterministic receipts linking every result to its topology, geometry, installation conditions, equipment data and evidence.
7. Render the results using the V7 overview and V8 detailed connection-map styles.

## No invented topology or cabling

The platform shall build on existing validated sequential, leapfrog, manufacturer-defined and user-supplied topologies. It shall not invent visually convenient conductor routes or arbitrary connection arrangements.

Topology defines which terminals connect.
Geometry defines where the conductors are physically installed.
Installation rules define constructed cable length and separation.
Physics computes on those constructed paths.
The browser renders kernel receipts without modifying them.

## Electromagnetic modelling scope

The kernel shall preserve sufficient conductor geometry to calculate, progressively:

- differential-mode loop area;
- self-inductance of each conductor route;
- mutual inductance between outgoing and return conductors;
- coupling between adjacent strings and harnesses;
- capacitance between conductors and from conductors to frame/earth;
- characteristic impedance and propagation delay where applicable;
- stored magnetic and electric energy;
- common-mode and differential-mode surge paths;
- induced voltages caused by changing current and nearby electromagnetic fields;
- effects of conductor spacing, crossing, bundling, tray, conduit and trench configuration;
- comparative EMC behaviour of sequential and leapfrog routing using the same physical table geometry.

The geometry model may use 3D coordinates where elevation and separation affect physics, but the browser is not required to render photorealistic 3D. Coordinates are engineering data, not a graphics objective.

## Fault-current and SPD modelling scope

The DC model shall support scenarios with and without surge protective devices and shall explicitly represent:

- PV source current and reverse current contributions;
- inverter/PCE backfeed where manufacturer data permits it;
- line-to-line and line-to-earth fault locations;
- positive-to-earth, negative-to-earth and common-mode paths;
- module, string, sub-array, combiner and inverter boundaries;
- protective conductors, bonding conductors, frames and earth paths;
- SPD location, connection topology and conductor lead geometry;
- SPD voltage-protection level, maximum continuous operating voltage, nominal discharge current, maximum discharge current and short-circuit withstand where evidenced;
- lead inductance and the additional dynamic voltage produced by surge-current rate of change;
- operation with the SPD absent, present, degraded, disconnected or failed short/open where supported by the device model;
- coordination between cascaded SPDs and upstream/downstream protective equipment;
- residual voltage at protected equipment terminals;
- prospective current paths before and after SPD conduction;
- thermal and energy stress assigned to the SPD and connected conductors.

An SPD shall never be represented as an ideal voltage clamp. Its model must be evidence-backed and versioned, with clear separation between manufacturer data, standard-derived assumptions and provisional engineering estimates.

## Near-term build sequence

1. Complete canonical topology validation and invariant tests.
2. Freeze conductor-path and installation-length receipt schemas.
3. Add sequential and leapfrog geometry fixtures based on the existing V7/V8 arrangements.
4. Add paired-conductor geometry metrics: separation, orientation, shared length and loop area.
5. Bind existing resistance, inductance, capacitance, energy and propagation calculations to validated constructed geometry.
6. Define fault-source, fault-location, earth/bonding and SPD objects.
7. Implement no-SPD baseline fault-path receipts.
8. Implement evidence-backed SPD conduction and residual-voltage scenarios.
9. Expose comparison overlays in V7/V8 style: topology, current path, loop area, induced voltage, SPD state and equipment stress.

## Acceptance rule

No visual feature is accepted merely because it looks impressive. A feature is accepted only when it improves connection verification, cable-routing accuracy, electromagnetic analysis, fault-path analysis, SPD assessment, evidence traceability or engineering communication.
