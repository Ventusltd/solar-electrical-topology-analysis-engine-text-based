# IEC TS 62738:2018 Capability Matrix for the Ventus DC String Engine V10

## Status

Declared standards traceability note for recovery work. This document paraphrases a licensed single-user copy of IEC TS 62738:2018 and does not reproduce the standard. It is not a certificate of compliance and does not replace review of the current applicable edition, national implementation, project specification, manufacturer instructions or approval by the relevant authority.

## Why this document matters

IEC TS 62738 is specifically written for restricted-access, utility-scale, ground-mounted PV power plants. It repeatedly recognises that large plants require engineering analysis beyond the simplified assumptions used for smaller installations. That makes it directly relevant to the recovery of a computation engine based on physical objects, electrical topology, routed conductors, protection boundaries, evidence and project-specific assumptions.

The matrix below maps executable or planned V10 capabilities to the clauses that justify modelling them. A clause reference does not mean the capability has already been implemented or validated. Implementation status must be recorded separately in the migration ledger.

## Capability matrix

| Capability ID | Engine capability | IEC TS 62738 reference | Standards significance | Required engine objects or inputs | Intended output | Current recovery treatment |
|---|---|---|---|---|---|---|
| TS62738-SCOPE-001 | Utility-scale applicability classifier | 1, 4 | Distinguishes restricted-access utility plants from residential, commercial and building-mounted systems; directs general compliance back to IEC 62548 with stated plant-specific exceptions | plant type, grid connection, access regime, monitoring regime | applicability statement and governing-standard set | Implement as project metadata and standards boundary |
| TS62738-TOPO-001 | Array, sub-array, string, PCE and MPPT hierarchy | 5.3.1–5.3.3; Figures 1–4 | Treats plant topology as a hierarchy rather than a single total cable length | module, string, string cable, sub-array, array, PCE, MPPT input, common bus, disconnector, combiner | explicit connectivity graph and hierarchy report | Core V10 recovery capability |
| TS62738-TOPO-002 | Independent MPPT versus common-bus topology | 5.3.2; Figures 2 and 3 | Protection, backfeed and allocation depend on whether DC inputs are electrically independent or internally commoned | inverter DC input architecture, MPPT mapping, common-bus declaration | validated inverter-block connectivity and reverse-current boundary | Must be explicit; never infer from input count alone |
| TS62738-HARNESS-001 | String wiring harness as a first-class object | 3.5; 5.3.4 | Defines harnesses as assemblies aggregating multiple strings along a main conductor and recognises them as an alternative to conventional combiner-box arrangements | branch conductors, aggregation nodes, main harness conductor, connectors, optional fuses | conductor schedule, aggregation topology, resistance and protection boundaries | Add to migration ledger; do not collapse into string or sub-array cable |
| TS62738-SERIES-001 | Series-parallel and unequal-string exception control | 5.3.5 | Permits deviations from uniform string length only under engineering supervision and with suitable voltage-control equipment | module count by string, optimiser/converter presence, manufacturer limits | exception flag, engineering-supervision requirement, compatibility checks | Standards-driven warning, not automatic approval |
| TS62738-EARTH-001 | Unearthed, high-ohmic and functionally earthed array model | 5.2.1–5.2.4 | Separates three materially different DC earthing configurations and their fault behaviour | pole-earth connections, resistance to earth, inverter isolation, residual-current or insulation monitoring | earthing configuration classification and fault-current topology | Required before insulation, capacitance or common-mode calculations |
| TS62738-OCPD-001 | String OCPD requirement from parallel strings | 6.3.2 | Determines whether neighbouring strings can impose reverse current above the module protection rating | parallel-string count, corrected string short-circuit current, module maximum OCPD rating, PCE backfeed limit | OCPD-required decision with equation trace | Implement only with edition-specific formula provenance |
| TS62738-OCPD-002 | Utility-plant string-fuse sizing exception | 6.3.3 | Allows a plant-specific sizing route that omits the IEC 62548 upper multiplier where the stated engineering conditions are satisfied | module Isc, candidate rating, module maximum OCPD rating, group size, failure-mode study, module test evidence, manufacturer approval | candidate range plus unmet-evidence list | Quarantine from automatic compliance until full evidence chain exists |
| TS62738-OCPD-003 | Grouped-string protection | 6.3.3 | Permits multiple strings under one protective device only under defined current and evidence constraints | strings per group, fuse rating, module rating, parallel backfeed, failure duration | grouped-protection feasibility and warnings | Separate protection cartridge candidate |
| TS62738-OCPD-004 | Sub-array and array protection coordination | 6.3.4 | Requires coordination with inverter short-circuit input limits and source-end fault current | sub-array count, array Isc, PCE limits, directional current limits, cable source fault current | coordinated protection result and cable duty | Needs full topology and PCE model |
| TS62738-INS-001 | Large-array insulation-resistance model | 6.4 | Recognises aggregation, wet conditions and inverter-transformer topology as causes of lower measured insulation resistance | module leakage, string count, array area, wet/dry state, topology, inverter isolation | estimated or measured array insulation resistance and validity boundary | Core evidence-aware capability |
| TS62738-INS-002 | Separate insulation warning and trip thresholds | 6.4 | Recommends two thresholds for plants with daily or rain-driven variation | measured history, warning threshold, trip threshold, nuisance-trip tolerance, safety floor | warning/trip policy with evidence and ageing notes | Reporting and monitoring capability; no hidden default values |
| TS62738-INS-003 | Array-size limit from leakage measurements | 6.4 | Supports using module leakage testing to engineer the maximum array size on one DC bus | measured module leakage distribution, bus topology, allowable aggregate leakage | maximum supported strings or modules per DC bus | Measurement-dependent; requires uncertainty propagation |
| TS62738-LP-001 | Site lightning-risk input | 6.5.1 | Directs the detailed design to IEC 62305-2 and links protection scope to site lightning activity | ground flash density, risk study reference, plant layout, structure bonding | risk-source metadata and required downstream checks | Standards interface, not a replacement risk calculation |
| TS62738-LP-002 | Equipotential-bonding mesh geometry | 6.5.1; Figure 8 | Presents an approximately 20 m by 20 m mesh as an example only and states soil study should determine spacing | array geometry, row bonding, buried earth conductors, soil study | mesh geometry, spacing report and evidence status | Geometry capability; never turn 20 m into a universal pass/fail rule |
| TS62738-SPD-001 | SPD electrical-distance assessment | 6.5.1 | States SPD effectiveness depends on resistance, inductance and electrical distance to modules; longer outlying strings reduce effectiveness | ordered route length, conductor geometry, R and L estimate, SPD location, protected module set | electrical-distance screen and least-protected module identification | Strong justification for routed topology and impedance modelling |
| TS62738-SPD-002 | Additional SPDs along string cabling | 6.5.1 | Recognises additional SPDs along long string routes as a possible way to improve protection | string routes, branch points, existing SPD locations, protection objective | candidate additional-SPD locations and assumptions | Recommendation generator only; final selection requires IEC 61643-32 and device data |
| TS62738-SPD-003 | DC SPD selection boundary | 6.5.2 | Requires DC-side suitability and points to IEC 61643-32 selection principles | system Voc, earthing topology, SPD technology, Ucpv, protection mode | standards-reference and device compatibility checks | Protection cartridge, primary-source verification required |
| TS62738-ARC-001 | Arc-risk input model | 6.6.2 | Identifies arcing as a dominant PV fire cause and prioritises installation quality, torque, connectors, cable management, vegetation and rodents | connector state, termination resistance, bend/tension, cable damage, vegetation and fauna exposure | risk factors and degradation scenarios | Deterministic risk-input model, not an arc-detection algorithm |
| TS62738-VOLT-001 | Maximum string-voltage method selector | 7.2.1 | Uses corrected STC Voc and the lowest expected operating-temperature method, while permitting further engineering analysis for marginal cases | module Voc, coefficient or prescribed factor, site temperature data, irradiance threshold, frost condition, module count | maximum string voltage with method and evidence trace | Maintain separate physical and standards-prescribed methods |
| TS62738-VOLT-002 | Minimum MPPT-voltage assessment | 7.2.2 | Requires consideration of Vmp temperature behaviour, cable drop, mismatch and degradation | module Vmp, temperature coefficient, hot ambient/cell relation, cable drop, mismatch and ageing | minimum inverter-terminal voltage and MPPT-margin report | Requires complete series circuit rather than centre-path only |
| TS62738-VOLT-003 | String-length optimisation | 7.2.1–7.2.3 | Recognises trade-offs among maximum voltage, cable losses, cable quantity and inverter efficiency | candidate module counts, full cable model, inverter efficiency maps and voltage window | ranked string-length alternatives with constraints | Optimisation layer after authoritative steady-state engine |
| TS62738-CABLE-001 | String-cable CCC and voltage-drop sizing | 7.3.4.1 | Permits utility-plant current sizing under stated protection analysis and frames voltage drop as a cost-performance decision, not a fixed universal percentage | corrected Isc, installation method, derating, route, area, material, cost and energy model | CCC compliance plus voltage-drop and lifecycle trade-off | Core electrical capability |
| TS62738-CABLE-002 | Cable grouping, spacing and soil derating | 7.3.4.1; 7.3.4.8–7.3.4.9 | Requires cable quantity, spacing, placement and soil thermal resistivity to feed sizing | segment environment, tray/duct/trench geometry, spacing, soil thermal resistivity, load profile | segment derating factors and limiting segment | Route environment must be first-class data |
| TS62738-CABLE-003 | Flexible versus fixed conductor classification | 7.3.4.4; 7.3.4.7 | Links conductor class to connectors and moving tracker sections | cable class, connector standard, fixed/moving segment | permitted-use classification and warning | Product and route compatibility check |
| TS62738-CABLE-004 | Physical-damage and securement assessment | 7.3.4.5–7.3.4.6 | Requires route-specific consideration of pinch points, sharp edges, wind movement, rodents, UV, stress, tension and bend radius | route geometry, support interval, edge proximity, cable OD, bend radius, clip/tie type, exposure | segment risk register and maintenance obligations | Geometry plus evidence; no invented universal slack constant |
| TS62738-CABLE-005 | Tracker transition and movement model | 7.3.4.7 | Requires reliability under repeated motion and manufacturer bend-radius limits | tracker articulation envelope, moving/fixed anchor points, cable length, bend radius, cycle count | swept-route feasibility and minimum usable lead length | Important extension to terminal-geometry branch |
| TS62738-CABLE-006 | Tray configuration model | 7.3.4.8; Figure 9 | Cable arrangement, covers, perforation and spacing affect temperature, water retention, fauna exposure and support loads | tray dimensions, covers, perforation, cable placement, bundle count, supports | tray occupancy, derating and environmental warnings | Route-segment cartridge candidate |
| TS62738-CABLE-007 | Underground route model | 7.3.4.9; Figures 10–12 | Requires soil, spacing and load-profile treatment and provides non-mandatory example trench arrangements | burial depth, ducts, direct burial, spacing, soil, backfill, warning tape, crossings, communications | trench cross-section, thermal inputs and installation evidence | Figures are examples, not universal dimensions |
| TS62738-CABLE-008 | Cyclic solar load profile for underground cables | 7.3.4.9.1 | Allows time-varying PV loading to be considered instead of an assumed continuous 100% load where suitable methods are used | hourly or sub-hourly current profile, soil and cable thermal parameters | cyclic rating and temperature profile | Later thermal cartridge; IEC 60853 method required |
| TS62738-AL-001 | Aluminium DC cable compatibility | 7.3.4.4; 7.3.4.10 | Permits aluminium for fixed installations but identifies expansion, oxide and termination risks | conductor material, terminal type, Cu/Al transition, paste, support, thermal cycling, inspection plan | compatibility checklist and maintenance requirements | Product/installation rule set; not merely a resistance calculation |
| TS62738-CONN-001 | Connector and termination integrity | 7.3.2.1, 7.3.4.6, 7.3.4.11 | Connects thermal cycling, torque, cable support and installation discipline to resistive heating and arcing | connector family, mating compatibility, torque, support force, resistance, IPC instructions | connection evidence and degradation scenario | Connector objects must be included in complete-circuit resistance |
| TS62738-COMM-001 | Commissioning and acceptance trace | 8.1–8.5 | Requires Category 1 commissioning and recommends selected Category 2 and performance tests | test regime, sample plan, I-V and thermal imaging results | acceptance evidence linked to topology objects | Reporting/evidence layer, not calculation only |
| TS62738-DOC-001 | Engineering-justification report | 10.3 | Requires documentation of design criteria, exceptions, alternate standards, unsupported domains, engineering assessments and simulations | every input, equation, standard, exception, evidence item, uncertainty and reviewer | reproducible engineering report and exception register | Governing requirement for V10 report architecture |
| TS62738-INV-001 | Inverter sizing and DC/AC trade-off | Annex A | Requires environmental output analysis, inverter voltage/current/power limits, reactive-power duty and PVIR effects | weather series, array output, inverter maps, thermal derating, reactive duty, PVIR | inverter-block compatibility and optimisation report | Separate from string geometry but composed at kernel level |

## High-priority implications for V10 recovery

### 1. Complete topology is mandatory

The engine must distinguish physical and electrical objects at module, string, harness, sub-array, MPPT, common-bus and PCE levels. The figures in Clauses 5.3.2 and 5.3.3 show why visually similar inverter inputs can have fundamentally different protection and backfeed behaviour.

### 2. Route geometry is engineering data

Cable route, spacing, support, movement, tray placement, burial geometry and environment affect resistance, current rating, degradation, lightning protection and maintenance. They cannot remain decorative browser geometry.

### 3. Harnesses must not be hidden inside a total length

A wiring harness has branch conductors, aggregation points, a main conductor, connectors and possibly group protection. It therefore needs an explicit electrical graph and conductor schedule.

### 4. Insulation and capacitance require the inverter boundary

Large-array leakage, wet conditions and inverter-transformer topology alter the effective insulation behaviour. Any future capacitance-to-earth or IMD calculation must identify the electrical boundary at which the quantity is seen.

### 5. SPD effectiveness depends on the actual route

IEC TS 62738 directly connects protection effectiveness to electrical distance, resistance and inductance. The engine should identify the most remote or least protected modules rather than reporting one undifferentiated array-level SPD status.

### 6. Standards rules and engineering exceptions must remain separate

The document permits utility-plant exceptions only with appropriate analysis, evidence, tests, manufacturer approval or authority acceptance. V10 must never convert an available exception into an automatic compliance result.

### 7. Reporting is part of the engine

Clause 10.3 expects explicit documentation when standards are not fully used, when alternatives are adopted, where no standard basis exists, and where engineering assessment is used instead. The canonical result schema therefore needs standards references, evidence, uncertainty, validity boundaries, exceptions and reviewer status.

## Proposed migration-ledger entries

At minimum, the following capability groups should be entered into the V6–V10 migration ledger:

- utility-scale topology hierarchy;
- MPPT-isolated versus common-bus inverter architecture;
- string wiring harness modelling;
- complete-series conductor schedule;
- reverse-current and grouped-string protection;
- large-array insulation and wet-condition behaviour;
- SPD electrical distance and additional-SPD screening;
- maximum and minimum string-voltage methods;
- route-specific derating;
- tracker moving-cable geometry;
- tray, duct and direct-burial route segments;
- aluminium termination and maintenance checks;
- connector resistance and mechanical loading;
- engineering-exception and standards-trace reporting.

## Prohibitions

- Do not reproduce licensed IEC figures or clause text in the public repository.
- Do not treat recommendations or example dimensions as universal mandatory limits.
- Do not claim compliance merely because a calculation references a clause.
- Do not use IEC TS 62738:2018 without checking whether a later edition, amendment or national adoption governs the project.
- Do not apply utility-plant exceptions to publicly accessible, rooftop, BIPV or BAPV installations outside the document scope.
- Do not encode a protective-device exception without the required failure-mode, test and manufacturer evidence.

## Source record

Primary source reviewed: IEC TS 62738:2018, Edition 1.0, *Ground-mounted photovoltaic power plants — Design guidelines and recommendations*, licensed Ventus single-user copy. Review date: 2026-07-29.
