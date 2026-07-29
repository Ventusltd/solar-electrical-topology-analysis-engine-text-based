# Ventus DC String Engine — Development Goals

Status: preparation register. Priorities will be revised after the Claude deep-research output is received and independently checked.

## P0 — Do not damage the proven versions

- Freeze V6, V7, V8 and V9 as separately addressable reference states.
- Record commit SHAs and create restore points before V10 implementation.
- Do not silently merge experimental equations into stable calculations.
- Build V10 in a separate directory and branch until its regression gates pass.

## P1 — Inventory the existing engine

- Catalogue every input, output, formula, constant, assumption and warning in V6–V9.
- Identify repeated formulas and differences between versions.
- Mark each method as active, superseded, experimental, wrong, unverified or measurement-dependent.
- Produce a feature matrix for V6, V7, V8, V9 and proposed V10.
- Map each current UI output to the exact computation function that produces it.

## P2 — Establish calculation truth and unit safety

- Introduce a canonical units layer using SI base units internally.
- Reject ambiguous cable length, one-way length, loop length and conductor-length inputs.
- Separate per-module, per-string, per-MPPT, per-inverter and per-plant quantities.
- Add dimensional checks for every formula.
- Add numerical tolerances and significant-figure rules.
- Prevent nF, µF, mF and F aggregation errors.
- Prevent confusion between conductor resistance, loop resistance and complete-series-circuit resistance.

## P3 — Build the topology graph

- Represent modules, junction boxes, factory leads, connectors, field cables, coils, trays, structures, earth, SPDs and inverter terminals as typed objects.
- Represent positive, negative, frame, protective-earth and remote-earth nodes separately.
- Generate ordered current paths from connectivity rather than from assumed total length.
- Detect open circuits, accidental shorts, polarity reversals, duplicate terminal use and impossible series sequences.
- Support sequential, leapfrog, mirrored, serpentine and custom topologies.
- Preserve physical route geometry independently from electrical connectivity.

## P4 — Create the evidence and provenance layer

- Give every input a source, date, version, evidence class and uncertainty.
- Distinguish manufacturer-declared, measured, geometry-derived, standards-derived, assumed and research values.
- Make missing critical evidence an explicit output.
- Store clause references and engineering interpretations without copying licensed standards text.
- Add source ageing and review-date warnings.

## P5 — Acid-test the core DC calculations

- Verify resistance against hand calculations and independent scripts.
- Verify temperature correction for copper and aluminium.
- Verify connector and termination series resistance.
- Verify voltage drop against complete current path and string Vmp.
- Verify power loss and energy-loss aggregation.
- Verify string open-circuit and operating voltage limits under temperature cases.
- Verify current, reverse-current and backfeed bounding cases.
- Verify fuse applicability logic without assuming all inverter inputs are equivalent.

## P6 — Strengthen electromagnetic modelling

- Derive loop area from actual ordered geometry.
- Calculate differential inductance by segment.
- Calculate common-mode inductance against frame and earth using declared approximations.
- Calculate conductor-to-conductor and conductor-to-earth capacitance separately.
- Model dry capacitance as the floor and environmental participation as a frequency-dependent branch where justified.
- Classify lumped versus distributed behaviour from rise time and propagation delay.
- Add transmission-line characteristic impedance and reflection cases only where the model inputs support them.
- Expose model limitations and sensitivity ranges.

## P7 — Add lightning, surge and insulation coordination

- Calculate routed electrical distance to the furthest module connection point.
- Add lightning-density provenance and critical-length calculations.
- Represent SPD locations, protection levels and lead lengths.
- Add SPD lead-inductance residual-voltage contribution.
- Compare equipment impulse withstand with calculated or bounded stress.
- Support additional-SPD scenarios for long outlying strings.
- Keep normative requirements, guidance and research hypotheses visibly separate.

## P8 — Model inverter input boundaries honestly

- Represent independent MPPT converters, reverse-current-blocked inputs and common-DC-bus architectures.
- Add an unknown-topology state.
- In unknown mode, calculate explicit bounding cases rather than selecting one hidden assumption.
- Represent insulation-monitoring boundaries and maximum permissible system capacitance.
- Separate low-frequency operating connectivity from high-frequency coupling assumptions.

## P9 — Build engineering-grade tests

- Create invariant tests for series continuity, current conservation, polarity and unit consistency.
- Create golden reference cases for sequential and leapfrog strings.
- Add property-based tests over module count, pitch, lead length, route length and conductor size.
- Add regression tests for every corrected historical error.
- Compare browser calculations against an independent non-browser reference implementation.
- Require tests to pass before promotion from sandbox to stable V10.

## P10 — Build reports that explain themselves

- Export text, JSON and CSV with inputs, formulas, provenance, uncertainty and warnings.
- Produce cable schedules separated into factory leads, extension leads and EPC-installed home runs.
- Produce component counts and connector schedules.
- Produce string, MPPT, inverter and plant aggregation.
- Produce an assumptions register and missing-evidence register.
- Produce a standards and evidence matrix without claiming unsupported compliance.
- Provide a calculation trace from final result back to topology object and source.

## P11 — Monthly intelligence and self-healing discipline

- Scan designated repositories and canonical public sources at least monthly.
- Write a dated intelligence report even where no change is recommended.
- Compare new findings against the current source registry and development goals.
- Open issues for accepted or unresolved findings.
- Never auto-edit engineering formulas from internet findings without tests and owner approval.
- Run regression tests after approved changes.
- Record rejected findings so they are not repeatedly rediscovered.
- Track stale manufacturer data, broken source links and superseded assumptions.

## P12 — Release governance

- Define sandbox, candidate and stable release states.
- Require a calculation-change note for every altered result.
- Require source and test evidence for every new constant.
- Record model version in every exported report.
- Keep a migration note explaining changes from V9 to V10.
- Preserve the ability to reproduce historical results from earlier engine versions.

## Immediate preparation tasks

1. Receive and archive the Claude deep-research output as a research input, not as automatic truth.
2. Compare its findings with the existing V6–V9 source code and owner-provided evidence.
3. Create the V6–V9 formula and feature inventory.
4. Create the reference-case test catalogue.
5. Draft the V10 canonical schema.
6. Draft the monthly scanner scope and source registry.
7. Agree the first implementation purchase order before modifying computation code.
