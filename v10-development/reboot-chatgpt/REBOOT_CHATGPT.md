# ChatGPT Reboot Handover — Ventus DC String Engine V10 Computation Recovery

Status: governing continuity document for a new ChatGPT thread.

Repository: `Ventusltd/solar-electrical-topology-analysis-engine-text-based`

Primary workstream: `v10-development`

Recovery workspace to be created and governed: `v10-debugger`

Date prepared: 29 July 2026

Owner: Ventus Ltd / Vikram Kumar

Purpose: preserve the full technical, architectural, historical and governance context required for ChatGPT to resume work in a new thread without repeating earlier misunderstandings, inventing repository structure, mistaking the current browser workbench for the authoritative engine, or rushing into another monolithic implementation.

# 1. How to use this file in a new ChatGPT thread

The user should ask ChatGPT to read this file from GitHub before discussing, editing or reviewing V10. The new thread should begin with a direct instruction such as: “Read `v10-development/reboot-chatgpt/REBOOT_CHATGPT.md` in the solar electrical topology repository, inspect the current repository state, and continue from the governing handover.” ChatGPT must then inspect the repository rather than relying on this document alone. This file is a continuity map, not a substitute for checking the current commit, current tests, current source tree and any work completed by Claude after this file was written.

The first response in a new thread should identify the current default-branch commit, confirm that this handover has been read, inspect any new `v10-debugger` work, identify changes made after the date above, and state whether the project remains aligned with the architecture in this document. ChatGPT must not immediately propose a fresh architecture without first checking whether Claude has already implemented or revised the proposed structure. It must not repeat generic advice such as “separate the frontend and backend” without grounding that advice in exact repository paths and actual code.

This reboot document is intentionally detailed because the project has accumulated several independent executable versions, overlapping calculations, browser-only logic, kernel-only logic, research notes, correction records, restore points and architectural rules. A short handover would be unsafe. The central problem is not lack of ideas. The problem is preserving engineering truth while consolidating a rapidly developed lineage into one authoritative computation engine.

# 2. Project identity and governing purpose

The repository is an open-source, text-based solar photovoltaic electrical topology analysis engine. Its purpose is not merely to calculate conventional voltage drop. It seeks to model the physical and electrical structure of utility-scale PV direct-current collection circuits from first principles and to determine what conventional lumped design methods omit. The intended model begins with physical objects and actual geometry: modules, junction boxes, factory leads, connectors, field-installed cables, route transitions, mounting structures, frame and protective-earth paths, inverter inputs and surge-protection elements. Electrical quantities are then derived from those objects and their connectivity rather than entered as one assumed total cable length.

The original repository README defines a broad technical scope including positive and negative conductor paths, piecewise cable sections, conductor resistance, loop inductance, conductor-to-conductor capacitance, capacitance from conductors and modules to frame or earth, frame and protective-earth nodes, optional inverter input capacitance and surge protection, steady-state voltage drop and loss, stored magnetic and electric energy, frequency-domain impedance, interruption cases and surge cases. The repository therefore contains both established steady-state calculations and advanced electromagnetic research. These domains must remain distinguishable. The engine must never present a research model, assumed parameter or provisional screening calculation as if it were a standards-certified project design.

The governing conceptual chain is:

physical objects → geometry → terminals and connectivity → ordered current paths → routed conductor objects → electrical parameters → operating and event models → evidence status → validation gates → reports and development feedback.

This chain is not decorative architecture. It is the core engineering principle. A calculation should be traceable backwards from the reported result to the exact physical path, topology decision, parameter, equation, source, assumption and validation state that produced it.

# 3. Owner’s operating preferences and non-negotiable working style

The owner prefers direct work on `main` unless a branch is explicitly requested or a risky experimental change genuinely requires isolation. Do not create branches and pull requests as a reflex. Do not turn a simple documentation or source change into an elaborate Git workflow. Before every structural or risky change, create or confirm a restore point. Preserve historical versions as addressable references.

Use British English. Avoid inflated marketing language, vague consultancy prose and unsupported certainty. The owner values numbers, exact paths, formulas, evidence and working code. When a repository fact is not verified, say so. Never describe a branch, file, function, test result or commit as existing merely because another AI mentioned it. Inspect it.

The user may use strong language when frustrated. Respond to the technical issue rather than becoming defensive. A previous failure mode was repeatedly saying that repository inspection was needed instead of actually using the GitHub connector. In a new thread, inspect first when asked.

Confidential project details must not be introduced into the public engine. Genericise engineering cases. Do not name private clients, sites or confidential artefacts in public code, comments or tests. Public reference cases should use generic module, inverter, string, route and environmental parameters. Source provenance may identify public manufacturer documents and standards references where licensing permits, but licensed standards text must not be copied into the repository.

# 4. Version lineage that must remain intact

The repository’s versions are not ordinary sequential releases where the latest automatically supersedes everything before it. Each version represents an independent technical workstream and must be studied as evidence.

## 4.1 V6

V6 is the stable complete-circuit reference located at the root application. It should be treated as a historical executable benchmark, not casually edited during V10 recovery. The repository describes it as the root complete-circuit workbench. Its actual executable calculations must be inventoried. Do not assume every item in the root README is fully implemented in V6; distinguish executable code from declared scope. Determine exactly how V6 represents circuit length, positive and negative conductors, resistance, voltage drop, capacitance, inductance, stored energy, frequency response and event cases. Record every input, formula, constant, warning and output.

## 4.2 V7

V7 is the independent electromagnetic FEED development stream under `v7-development`, with executable FEED I work isolated from the root application. The repository says V7 establishes dimensional and unit safety; evidence and epistemic status; closed-form two-wire differential parameters for long straight route sections; separate low-frequency and high-frequency inductance; separate differential and common-mode networks; event rise-time versus propagation-delay classification; capacitance aggregation by module, string, MPPT and inverter; and explicit validation gates for uncertain module capacitance, wet-surface participation, inverter termination and irregular coil geometry.

V7 also contains or proposes FEED II extensions for sequential, leapfrog, mirrored and custom wiring patterns; loop-area and induced-voltage comparison; module-lead feasibility; environmental layer stacks involving cell, encapsulant, glass, water film, frame, rail, pile, soil and remote earth; salt, humidity and contamination as state variables; module and connector parasitics; standards classification; asset identities; and EMC and measurement hooks. In recovery, inspect which of these are executable, which are documentation, which are hypotheses and which are corrected or obsolete. Do not merge electromagnetic logic into the basic steady-state engine merely because it exists.

## 4.3 V8

V8 is the independent leapfrog cable-schedule workbench under `v8-leapfrog`. It was deliberately narrow. Its principal engineering question is the difference in externally installed DC string cable between a conventional sequential 30-module string and a leapfrog arrangement. Its governing qualitative rule is that sequential wiring leaves the two free string terminals at opposite physical ends of the row, while a properly configured leapfrog string brings both free terminals toward the inverter-side end. The external cable saving is approximately one row span, subject to the actual terminal and lead geometry. Inverter distance is common to both arrangements and therefore does not itself alter the per-string topology saving. Leapfrog does not eliminate both home runs; it eliminates the extra far-end return component.

V8 adds editable inverter distance, east and west band lists, row-span derivation from module width and gap, sequential and leapfrog schedules, comparison of external cable, resistance, voltage drop and loss, an explanatory diagram and JSON export. Recover its actual formulas and distinguish field-installed external cable from factory-fitted leads. Verify the leapfrog identity independently. Do not perpetuate a centre-to-centre simplification where terminal geometry is available.

## 4.4 V9

V9 is the most important immediate recovery source because it already re-established a canonical computation-engine pattern. The root `CLAUDE.md` directs all V9 work to `v9-sandbox/debug/CLAUDE.md`, identifies `v9-sandbox/debug/engine.js` as the canonical engineering logic, and identifies `v9-sandbox/debug/tests.js` as the deterministic review suite. It explicitly prohibits V9 engineering mathematics, topology decisions, cable calculations and warnings from being placed in browser rendering code. The browser should collect inputs and display the computation report.

The V9 debug instructions require reviewers to ask whether the mathematics is physically correct, whether the input is the right physical quantity, whether each topology creates a valid series path through every module exactly once, whether factory leads, extensions, home runs and connector interfaces are represented separately, whether estimates are labelled as estimates, whether results are deterministic, whether warnings come from the engine, and which physical objects remain absent. These questions should govern V10 recovery too.

The V9 engine contains useful executable logic that is broader than the current modular V10 kernel. It defines limits for MPPTs, inputs per MPPT, 24 active strings and 30 modules per string. It supports sequential, mirrored sequential, alternating-return, leapfrog and custom topologies. It validates custom orders. It allocates strings across MPPT inputs and truncates requests beyond the active-string cap. It performs cold Voc correction using cell temperature. It computes conductor resistance from copper resistivity, cross-sectional area, length and conductor temperature. It builds module objects with positive and negative terminal identities. It creates negative and positive home-run segments and module-interconnect segments. It estimates whether extension cable is required using module-centre separation minus the sum of positive and negative lead lengths. It calculates separate home-run and provisional extension lengths, external resistance, voltage drop and loss per string. It builds MPPT and string records, project totals and warnings.

V9’s limitations are explicit. Exact terminal coordinates are absent. Interconnect reach is a centre-to-centre screening estimate, not a construction quantity. Both positive and negative home-run lengths are assumed equal to one user-entered route distance. Resistance is copper-only in that stage. All strings share one module count and topology. These limitations should not lead to rejection of V9; they define the work V10 must complete.

## 4.5 V10 modular foundation

The V10 foundation under `v10-development/src` is a genuine modular computation kernel. It must not be discarded. The inspected files include at least `kernel.mjs`, `topology.mjs`, `electrical.mjs`, `quantity.mjs` and associated schemas and tests. The kernel computes topology geometry, wraps values in evidence-aware quantity objects, computes conductor resistance, voltage drop, resistive power loss and optional cold Voc results. Its output has a schema version and warnings. It propagates uncertainty intervals and provenance.

The V10 topology module supports sequential, mirrored sequential, canonical leapfrog and custom ordering. It validates custom permutations, creates linear module-centre coordinates, derives ordered straight-line segments and calculates path length and terminal separation at the module-centre level. It is deterministic and tested. It does not yet model exact junction-box terminals, lead exits, field routes, connector objects or the full inverter block.

The V10 tests use Node’s built-in test runner. Inspected tests cover unsupported-unit rejection, weakest-provenance propagation, a simple geometry-derived resistance/voltage-drop/loss example, uncertainty propagation, cold Voc and deterministic repeatability. These are useful foundations but do not prove full-circuit or inverter-block capability.

## 4.6 V10 browser workbench

The current `v10-development/index.html` is a rich standalone 24-string inverter workbench. It contains inline engineering logic rather than importing the modular kernel. It displays 24 strings and 48 conductors, terminal geometry, mirroring, leapfrog or sequential arrangements, cable schedules, electrical results, findings, diagnostics, project scaling and drawing output. It is visually and functionally ahead of the modular kernel in several respects. However, because it computes independently, it violates the governing architecture and creates a second source of truth.

The browser is therefore a placeholder and a source to mine for recoverable logic, not the final implementation. Do not continue adding engineering calculations to it. Do not delete it until the recovered engine and rebuilt thin client are ready. Do not treat its outputs as verified merely because the page renders.

# 5. The central architectural failure

The current V10 contains two non-composed implementations. The modular kernel knows how to produce an ordered module-centre path and evidence-aware electrical quantities. The browser knows how to construct a 24-string visual block, place terminals, choose mirrored arrangements, route home runs, generate conductor schedules, compute cable quantities and display results. The browser imports none of the modular source files. As a result, topology and electrical rules are duplicated and maintained manually.

This creates several engineering risks. A future correction to leapfrog ordering may be applied to one implementation and not the other. A unit or temperature correction may exist in the kernel while the page continues using an older formula. Browser warnings may diverge from engine validation. The page may report a complete-looking result while omitting the kernel’s in-string path. The kernel may report a traceable result while omitting the page’s home-run routing. Neither is complete, and there is no contract test proving parity.

The problem is not solved by moving all inline browser logic into one new `engine.js`. That would simply replace one monolith with another. The recovery must identify coherent engineering domains, independently validate them, expose stable contracts and compose them through one orchestrator.

# 6. Current strategic decision

Freeze the present V10 browser as a placeholder. Create `v10-debugger` as a computation-engine integration laboratory. Recover all useful logic from V6, V7, V8, V9, the modular V10 foundation, the V10 browser and any relevant V10 branches. Break the computation engine into engineering cartridges. Independently sandbox-model every domain. Test each cartridge. Compose them into one canonical report. Perform feature-parity assessment. Rebuild the public V10 browser only when the engine is authoritative and both Claude and ChatGPT agree that it represents meaningful progress.

`v10-debugger` is not another UI version. It is not to become a public marketing page during recovery. A minimal diagnostic interface is acceptable only if it displays canonical engine results without performing engineering calculations.

# 7. Claude’s governing commission

Claude has been commissioned to undertake the repository recovery. Claude must inspect before coding. Its first response should be a repository inspection plan and execution feed identifying exact directories, files, branches, commands, uncertainties and initial test vectors. Claude must independently sandbox-model everything rather than trusting historical AI output or simply reproducing existing values.

Claude must treat every historical formula or rule as a claim requiring classification. A claim may be verified, useful but incomplete, duplicated, conflicting, obsolete, wrong, research-only, measurement-dependent or not yet assessable. Claude must not silently choose between conflicting implementations. It must present the conflict, independent model, test vector and recommended disposition.

Claude must not extend the current browser during recovery. It must not declare success based on a larger test count, an attractive debugger or a working cable schedule. Success means one independent, modular, deterministic, evidence-aware computation engine with complete traceability and no duplicated engineering mathematics in the renderer.

# 8. Required `v10-debugger` structure

The exact final structure must be derived from repository inspection, but the following organisation is the governing starting point:

`v10-debugger/README.md` — purpose, status, boundaries and entry instructions.

`v10-debugger/CLAUDE.md` — governing Claude instructions for this recovery workspace.

`v10-debugger/CHATGPT.md` — instructions for independent ChatGPT review and parity assessment.

`v10-debugger/package.json` — minimal deterministic test and report commands.

`v10-debugger/src/compose.mjs` — the single composition layer that validates a canonical request, invokes cartridges in explicit order and returns a canonical report.

`v10-debugger/cartridges/` — independently versioned engineering components.

`v10-debugger/independent-models/` — isolated reference calculations, notebooks, scripts and hand derivations that challenge production cartridges and are never imported at runtime.

`v10-debugger/inventory/` — V6–V10 feature, formula, object, warning and test inventories.

`v10-debugger/migration-ledger/` — machine-readable and human-readable records of every recovered or rejected calculation.

`v10-debugger/schemas/` — canonical request, result, object, route, evidence and cartridge schemas.

`v10-debugger/reference-cases/` — accepted numeric cases with independent expected results.

`v10-debugger/tests/` — integration, contract, invariant, property and historical regression tests.

`v10-debugger/reports/` — generated audit, parity, conflict, missing-evidence and test reports.

`v10-debugger/CHANGELOG.md` — changes to the overall composition engine.

This is not a licence to create empty folders. Every folder should appear only when it has real content and purpose.

# 9. Migration ledger requirements

The migration ledger is the first authoritative deliverable. For every calculation, rule, object, warning or output discovered in V6 through V10, record:

- unique ledger ID;
- version and exact source path;
- function, variable, code block or documentation heading;
- engineering domain;
- physical interpretation;
- inputs and units;
- outputs and units;
- formula or algorithm summary;
- assumptions;
- evidence status;
- whether executable or documentation-only;
- whether duplicated elsewhere;
- known conflicts;
- current tests;
- independent reference status;
- validity range;
- known omissions;
- intended cartridge;
- migration state;
- decision and decision owner;
- linked commit;
- next review date.

The ledger must distinguish code from aspiration. The root README, V7 plans and V10 development goals contain extensive intended scope that may not yet be executable. Do not mark a documented objective as implemented. Conversely, browser-only logic must not be ignored simply because it violates architecture; it must be catalogued and either recovered, corrected or rejected.

Migration states should include at least: discovered, under review, independently modelled, conflict identified, accepted for migration, migrated, tested, integrated, rejected, superseded, measurement required, deferred research and presentation-only.

# 10. Cartridge definition and governance

A cartridge is a coherent engineering computation component. It is not a browser panel, not a microservice and not an arbitrary file-size split. Each cartridge must have a stable schema or API version, README, CHANGELOG, tests, reference cases and known-limitations section. A cartridge owns one engineering responsibility and should not mutate global state.

Each cartridge result should include:

- cartridge schema version;
- canonical input references;
- computed values with units;
- evidence and provenance;
- uncertainty or bounds;
- equation or rule identifiers;
- warnings and validation findings;
- assumptions used;
- missing evidence;
- deterministic hash where useful.

Cartridges must not freely call downstream cartridges. The composition layer owns dependency order. Shared primitives such as quantities, evidence records, object IDs and validation result types may be imported from carefully governed foundation modules.

Likely cartridge domains are described below, but Claude may revise boundaries after inventory if it explains the evidence.

# 11. Quantities and units cartridge

The existing V10 quantity model is the preferred foundation. Important engineering values must not be passed as ambiguous naked numbers. Every quantity should carry value, unit, provenance, uncertainty, source and evidence status. The units policy must distinguish one-way route length, physical displacement, routed cable-centreline length, installed conductor length, positive-plus-negative conductor length, loop length, module-interconnect path and complete-series-circuit length.

Temperatures must be explicit: ambient temperature, cell temperature, conductor temperature, connector temperature and reference temperature are different physical quantities. Resistance must distinguish resistance per metre, segment resistance, one-pole resistance, loop resistance, contact resistance and total series resistance. Capacitance must identify terminals and mode: conductor-to-conductor differential capacitance is not interchangeable with conductor-to-frame or array-to-earth common-mode capacitance.

The units cartridge must reject incompatible operations and test conversions. Internally use SI where practical. Engineering display units may be preserved in reports, but conversion must be explicit and tested. Historical nF, µF, mF and F aggregation errors must become regression tests.

# 12. Evidence, provenance and uncertainty cartridge

Every important input and output must record whether it is manufacturer-declared, measured, geometry-derived, standards-derived, first-principles derived, assumed, research hypothesis or unknown. Add source identifiers, source dates, model versions, review dates and validation status. Do not copy licensed standards text. Store clause references and engineering interpretations.

Evidence must weaken through calculations. A precise arithmetic result derived from an assumed terminal position remains assumption-dependent. The engine must not convert numerical precision into epistemic certainty. Where data are uncertain, support intervals, distributions where justified, named scenarios or explicit bounding cases. Do not invent a probability distribution merely because an interval exists.

The evidence cartridge should produce missing-evidence and stale-evidence findings. A calculation may proceed as a provisional screen while clearly stating the missing inputs needed for a construction quantity or compliance assessment.

# 13. Physical objects cartridge

Create typed identities for modules, junction boxes, terminals, factory leads, connector halves, mated connector interfaces, extension leads, field string cables, harness sections, coils, route segments, trays, conduits, trenches, structures, frames, rails, piles, protective-earth conductors, SPDs, isolators, inverter input terminals, MPPTs and inverter boundaries.

Do not require full detail for every object in the first implementation, but create an extensible taxonomy with stable IDs. Physical adjacency must remain separate from electrical connectivity. A module can sit next to another module without being electrically connected to it. A module’s physical index can differ from its electrical order. Objects should retain identity when moved, mirrored or reassigned.

Every conductor-like object should eventually record ownership or class, polarity where applicable, start and end terminals, material, cross-sectional area, insulation or cable family reference, environment, route and evidence.

# 14. Geometry cartridge

The geometry cartridge starts with linear rows but must not be hard-coded permanently to one dimension. It should support coordinates, orientation and transforms in a way that can later extend to two-dimensional tables and terrain.

Model module centre, module edges, junction-box location, positive and negative lead origins, lead exit directions and connector-terminal positions. Module dimensions and junction-box separations should be explicit inputs with provenance. Mirroring must be an explicit state, not a hidden result chosen solely to minimise length.

Route geometry should use ordered points or typed segments. Distinguish plan displacement, surface distance, cable-centreline distance, vertical drops, bends, service loops, slack and termination allowance. The geometry cartridge should calculate physical facts but not electrical resistance.

# 15. Terminals and leads cartridge

This cartridge closes a central historical gap. V9 screens interconnect reach using centre-to-centre module separation and the combined positive and negative lead lengths. The V10 browser appears to include richer terminal geometry, but that logic is untested and browser-bound.

Model positive and negative terminal positions independently. Model each factory lead independently. Lead length is not automatically usable straight-line reach. Include origin, exit direction, permitted dressing assumptions and connector-terminal endpoint. Produce an interconnection feasibility result for every adjacent pair in electrical order.

Possible statuses include: direct reach geometrically proven; direct reach impossible; extension required; uncertain because orientation is missing; uncertain because terminal positions are assumed; or invalid connector/polarity configuration. Report available lead length, required routed separation, margin and evidence status.

Factory lead length, utilised reach, unused slack and field extension cable are different quantities. Preserve them separately.

# 16. Topology and connectivity cartridge

Consolidate all topology-order implementations into one authoritative source. Support sequential, mirrored sequential, canonical leapfrog, alternating-return or serpentine where physically defined, and custom order. Validate custom permutations.

Ordering alone is insufficient. Build an explicit terminal connectivity graph. Validate that a string forms one continuous series path, each module is traversed exactly once, polarity is consistent, no terminal is illegally reused, no accidental short exists, and all required components are connected. Separate graph connectivity from physical geometry.

Use stable typed nodes and edges. Explain whether the implementation uses a directed multigraph, property graph or another model. Add invariants for continuity, uniqueness, source-to-sink traversal and absence of unintended cycles.

Leapfrog must be independently derived for odd and even module counts. Test the canonical 30-module sequence and path-length identity. Do not preserve any earlier unproven 58-pitch claim if independent geometry confirms 57 pitches at the centre level. Terminal geometry may alter actual lead-path lengths but not the discrete order identity.

# 17. Routing and conductor-schedule cartridge

Recover V9’s home-run segment concept and the V10 browser’s richer routing, but replace assumptions with explicit routes where possible. Positive and negative conductors must be separate scheduled objects. Do not assume equal paths unless that is an input or route definition.

Each scheduled conductor should include ID, string, MPPT, input, polarity, conductor class, start terminal, end terminal, route segments, installed length, material, cross-sectional area, environment, evidence status and any slack or allowance basis.

Separate factory leads, field extensions, EPC-installed home runs, harnesses and protective-earth conductors. The project total must sum individual objects. Multiplication of one representative or worst-case string is allowed only as a labelled estimate or scenario.

The schedule should support a 24-string, 48-home-run inverter example but not hard-code 24 as universal. It should also support one string, two strings per MPPT and inactive inputs.

# 18. Inverter and MPPT allocation cartridge

Recover V9’s allocation logic. Represent MPPT count, string inputs per MPPT, active-string limits, current limits, voltage windows and other inverter parameters as evidence-aware inputs. Defaults are examples, not universal facts.

Each string must have explicit MPPT and input identities. Allocation overrides should be validated. Requests beyond hardware or scenario limits should generate engine findings. Unknown internal inverter topology must remain unknown.

Provide explicit modes for independent MPPT conversion, reverse-current-blocked inputs, common DC bus or unknown topology. Unknown mode should return alternative bounding cases where relevant rather than silently choosing one architecture.

# 19. Complete-series-circuit electrical cartridge

The steady-state engine must calculate the complete current path. Include positive and negative external conductors, extensions, factory leads, connector contacts, terminations and optional series devices. Each segment may have different material, cross-sectional area, temperature and evidence.

Calculate resistance per segment and aggregate resistance. Preserve cable-only and complete-circuit outputs. Calculate voltage drop at a declared operating current and percentage against a declared string operating voltage. Calculate power loss per segment and total. Aggregate by string, MPPT, inverter and project.

Energy loss requires an operating profile. Do not multiply instantaneous loss by arbitrary annual hours without an explicit profile and evidence. Temperature correction should support copper and later aluminium where relevant. Connector resistance must be a separate evidence-aware input, not hidden in cable resistance.

# 20. Voltage and operating-case cartridge

Recover cold Voc logic and distinguish cell temperature from ambient temperature. Inputs include module Voc at STC, voltage temperature coefficient, governing minimum cell temperature, module count and system or inverter voltage limit. Produce module and string corrected voltage, utilisation, margin, uncertainty and evidence status.

Later include hot Vmp and MPPT operating-window checks. Use named cases. Do not issue a compliance verdict where manufacturer data, design temperatures or standards interpretation are incomplete. Warnings should come from the engine.

# 21. Protection, reverse-current and inverter-boundary cartridge

Represent inverter input boundaries explicitly. Model strings or sub-arrays that can share reverse current, inverter backfeed current, isolation devices and overcurrent protection inputs. Do not assume that two strings per MPPT automatically require or do not require fuses without evaluating the applicable current paths and equipment data.

Unknown inverter architecture should produce bounding cases. Keep low-frequency operating connectivity separate from high-frequency coupling assumptions. Protection outputs should be engineering studies and evidence matrices, not unsupported certification.

# 22. Electromagnetic geometry cartridge

Derive differential loop geometry from actual ordered positive and negative paths. Calculate local separation, segment contribution, maximum local loop width, signed or absolute area as appropriate, and the proportion of route with paired conductors. Represent coils explicitly with diameter, turns, conductor pairing and orientation.

The cartridge should initially produce geometry and applicability screens. It must not jump directly to precise transient overvoltages without validated electrical parameters. Loop area is not itself a universal standards limit. Preserve route detail so later inductance and induced-voltage models can use it.

# 23. Inductance, capacitance and distributed-line cartridges

Recover useful V7 and V6 work independently. Separate differential and common-mode quantities. For long straight two-wire sections, closed-form approximations may be used within stated validity ranges. Low-frequency internal inductance and high-frequency external inductance should not be conflated. Irregular coils and structure routes may require bounds or numerical models.

Conductor-to-conductor capacitance, conductor-to-frame capacitance, module-to-frame capacitance and aggregate array-to-earth capacitance are different networks. Dry capacitance remains a floor where a wet-surface branch is modelled. Wet participation should not be one fixed full-area multiplier unless measured or justified.

Classify lumped versus distributed behaviour using disturbance rise time and route propagation delay. Characteristic impedance, propagation velocity and reflection cases require declared geometry and dielectric assumptions. Do not assign one universal resonance to a complete utility string.

# 24. Insulation monitoring cartridge

Aggregate capacitance and insulation resistance at the actual monitoring boundary. Represent independent MPPT, reverse-current-blocked and common-bus alternatives. Distinguish positive-to-earth, negative-to-earth and common-mode networks. Keep leakage resistance and capacitance as separate branches.

Inputs may include IMD permissible system capacitance, warning threshold, trip threshold and response-time characteristics. Where inverter topology or OEM data are unknown, calculate alternative cases or report that the assessment is incomplete.

# 25. Lightning, SPD and impulse-coordination cartridge

Calculate maximum routed electrical distance from PCE to the furthest module connection point using topology and routes, not straight-line site distance. Add lightning-density input and provenance. Implement critical-length calculations only with the correct standard interpretation and source reference.

Represent SPD locations, protection levels, surge-current cases and lead lengths. Calculate or bound lead-inductance contribution. Compare calculated or bounded stress with equipment impulse withstand where data exist. Support additional-SPD scenarios for long outlying strings. Separate normative requirements, guidance, first-principles models and research hypotheses.

# 26. Arc, interruption, restrike and stored-energy sandbox

Historical research includes interruption and surge cases, distributed-line effects and stored energy. These must be independently sandboxed before production promotion. Record event waveform or rise time, initial current, termination assumptions, route delay, characteristic impedance and capacitance. Compare lumped and distributed models. Do not state one precise overvoltage where the inverter termination, module capacitance, arc dynamics or conductor geometry are unknown.

Arc and restrike models are research tools, not project protection studies. Outputs should be ranges, sensitivity results and applicability warnings until validated against measurement or authoritative models.

# 27. Independent modelling requirement

Every engineering domain must be independently modelled in `v10-debugger/independent-models`. Production cartridges must not import these models. Their purpose is adversarial validation.

For simple formulas, provide hand calculations. For geometry, graphs and route aggregation, provide separate scripts. For electromagnetic cases, provide derivations, limiting cases and sensitivity sweeps. Each independent model should state:

- question;
- physical system;
- assumptions;
- equations;
- units;
- input vector;
- expected result;
- tolerances;
- limiting cases;
- sensitivity;
- known limitations;
- comparison with each historical implementation;
- disposition.

Do not write an “independent” script by copying the production function line for line. Use a different formulation where possible. For example, compare a graph traversal against an explicit expected edge list; compare conductor totals by summing schedule rows in an independent script; compare geometry-derived path length against a hand-derived pitch identity; compare resistance from resistivity and area against a datasheet resistance-per-kilometre case.

# 28. Required reference and discriminating test cases

At minimum create the following cases:

A one-module string to test zero inter-module links and two external conductors.

A two-module sequential string to test one interconnect and opposite-end terminal behaviour.

Three- and four-module sequential, mirrored and leapfrog strings to expose odd/even ordering errors.

A 30-module sequential string using explicit pitch, terminal spacing and 1.4 m positive and negative leads.

A 30-module canonical leapfrog string proving the order, centre-path pitch count, terminal locations and extension feasibility.

A custom invalid order with a duplicate module.

A custom invalid order with a missing module.

A polarity reversal and accidental short case.

A 12-MPPT, two-input, 24-string inverter block.

An over-requested allocation case that exceeds the active-string cap.

A case with unequal positive and negative home-run routes.

A case with one route containing a vertical drop, trench run, service loop and termination allowance.

A case where factory leads just reach, just fail and are uncertain due to terminal orientation.

A copper resistance case at 20°C and 70°C with independent expected values.

A complete-circuit case separating 6 mm² field cable, 4 mm² factory leads and connector resistances.

A cold Voc case using cell temperature and an uncertainty interval.

A project aggregation case where totals are verified by independent schedule summation.

A loop-geometry case with perfectly paired conductors producing minimal area.

A divergent-route case producing known rectangular loop area.

A propagation-delay versus rise-time case clearly lumped, clearly distributed and borderline.

A capacitance aggregation case that catches nF-to-µF mistakes.

An unknown inverter topology case returning multiple bounds.

# 29. Test architecture

Use Node’s built-in test runner unless a dependency provides substantial value. Tests should include:

Unit tests for every cartridge.

Invariant tests for physical and graph rules.

Property-based tests or systematic sweeps over module count, pitch, topology, lead length, route length, conductor size, temperature and allocation.

Golden reference tests using independently calculated expected results.

Historical regression tests for every known correction.

Integration tests for one string, MPPT, inverter and project.

Contract tests for canonical request and result schemas.

Determinism tests for identical input and canonical hashes.

Browser-boundary tests proving the renderer does not calculate engineering results.

Do not weaken tests to make new code pass. If a test is wrong, document the independent proof and change it through a calculation-change note.

# 30. Historical corrections that must become regression tests

The repository records several important corrections. Ensure tests cover them:

Capacitance aggregation must remain unit-safe. Nanofarads per kilowatt multiplied by hundreds of kilowatts can become microfarads.

In an RC-sheet model, participating distance increases with conductivity and decreases with frequency under the stated formulation.

Faster sub-microsecond events make distributed modelling more relevant, not less.

Common-DC-link coupling is frequency-dependent and cannot be reduced to a binary statement that all strings are simply paralleled at every frequency.

Dry capacitance remains as a floor when environmental surface participation is added.

Differential module capacitance and module-to-earth common-mode capacitance must remain separate.

No fixed 0.5 m² loop-area figure is a universal PV-standard limit.

A complete string may require a distributed model, but it does not have one universal resonance independent of termination and geometry.

Standards statements must be classified as normative, guidance, first-principles engineering, research or measurement-dependent.

Sequential and leapfrog are separate topology states.

External field cable and factory module leads are separate length classes.

Cell temperature must not be replaced by ambient temperature in cold Voc correction.

One-way route, two-pole external conductor length and complete-series-circuit length must not be confused.

The canonical 30-module leapfrog centre-path is 57 pitches under the current order definition, not an unsupported 58-pitch assertion.

# 31. Canonical request schema

Before a new browser is built, define a canonical engine request. It should include:

schema version; document ID; model metadata; requested calculations; physical objects; stable terminals; coordinates and orientation; route polylines; electrical edges; component references; module electrical data; cable properties; connector properties; inverter and MPPT definition; operating cases; environmental cases; protection data; evidence records; uncertainty; and user-selected assumptions.

The request must distinguish user input from derived geometry. It should allow calculated geometry to be serialised for reproducibility but prevent ambiguous duplication. Define precedence rules.

# 32. Canonical result schema

The result should include:

schema version; engine version; cartridge versions; canonical input hash; validation errors; warnings; assumptions; missing evidence; physical object graph; connectivity graph; ordered current paths; interconnection feasibility; conductor schedule; electrical segment results; string results; MPPT results; inverter results; project totals; voltage cases; protection bounds; electromagnetic screens; equation traces; source dependencies; uncertainty; and report-generation metadata.

Timestamps must not affect deterministic hashes. Every result should be reproducible from the canonical request and versioned engine.

# 33. Composition engine

Create one composition layer, tentatively `v10-debugger/src/compose.mjs`. It validates the request, calls cartridges in explicit dependency order and assembles the report. Cartridges should not arbitrarily import one another in cycles.

A likely order is: schema validation; quantities and evidence; physical objects; geometry; terminals and leads; topology and connectivity; ordered paths; routing and schedules; inverter allocation; steady-state electrical calculations; voltage cases; protection boundaries; electromagnetic geometry; advanced electromagnetic screens; validation; aggregation; reporting.

The composition engine should support requested-calculation flags so basic schedule work does not require uncertain advanced inputs. However, dependencies must remain explicit. A missing optional domain should be reported as not requested or insufficient evidence, not silently omitted.

# 34. Browser boundary

The eventual browser is a thin renderer. It may perform screen-coordinate scaling, zoom, pan, selection, drag interactions, formatting and drawing. It may not determine electrical topology, terminal reach, routed engineering length, resistance, voltage, loss, warnings, protection status or evidence status.

Do not enforce the simplistic rule that browser files contain no arithmetic. Presentation needs arithmetic. Instead add tests or static checks for prohibited engineering function duplication and ensure the browser consumes canonical results. Use a mock result test to prove rendering works without the real engine.

The current V10 `index.html` remains a placeholder. No further engineering features should be added during recovery.

# 35. Branch and commit recovery

Inspect all V10-related branches through a fresh clone or reliable branch API. Previous connector branch search did not return results, so claims about branch names and test counts remain unverified until inspected. Record each branch head, unique commits, unique files and relevance.

A reported branch named `v10-terminal-geometry-and-leads` may contain `terminals.mjs`, `inverter-block.mjs` and a nearly passing test suite, but this must be verified. Recover unique work through traceable commits. Do not merge a branch wholesale until its calculations are independently assessed.

Do not mass-delete branches. Propose archival or deletion only after unique work is recovered and the owner approves.

# 36. Clean-clone discipline

Run from a fresh Linux clone. Record:

repository URL; branch; commit SHA; Node version; Python version where used; installation commands; test commands; generated reports; failures; and environment assumptions.

Avoid hidden local files and uncommitted dependencies. The engine should work from a clean clone with documented commands. Generated reports should either be reproducible and committed intentionally or excluded explicitly.

# 37. Commit discipline

Use small commits. Each commit should close a clear ledger item, establish a test framework, migrate one coherent calculation or correct one verified issue. Commit messages should describe engineering consequence, not merely “update files.”

Create restore points before structural changes. Preserve V6–V9. Do not overwrite historical results. Every changed engineering result requires a calculation-change note and linked tests.

Direct work on `main` is preferred when authorised. Do not create unnecessary PRs. If Claude is operating in a sandbox branch, the owner should approve promotion after review.

# 38. Phased execution plan

## Phase 1 — Repository inventory

Inspect V6 through V10, documentation, tests, workflows, branches and restore points. Produce the migration ledger, feature matrix, duplicate map, conflict register and branch report. No production migration until this is credible.

## Phase 2 — Foundations

Establish canonical units, quantities, evidence, uncertainty, IDs, validation result types, request schema and result schema. Migrate useful V10 quantity logic. Add deterministic tests.

## Phase 3 — Physical model and topology

Implement physical objects, geometry, terminals, leads, topology, connectivity and ordered paths. Independently validate leapfrog and sequential cases. Recover unique branch work only after assessment.

## Phase 4 — Routing and schedules

Implement explicit routes, positive and negative conductor objects, extensions, home runs and conductor schedules. Reproduce V8 and V10 schedule capabilities with traceability.

## Phase 5 — Inverter block and steady-state electrical engine

Recover MPPT allocation, string construction, complete-series resistance, voltage drop, power loss, cold Voc and project totals. Replace V9’s centre-screen limitations with terminal geometry where supported.

## Phase 6 — Electromagnetic and protection sandbox

Inventory and independently model V6/V7 advanced calculations. Promote only those with clear assumptions, units, tests and validity. Keep uncertain models sandboxed and visible.

## Phase 7 — Integration and feature parity

Compose all accepted cartridges. Generate canonical reports. Compare every historical capability. Record implemented, rejected, superseded, measurement-required and deferred items.

## Phase 8 — Independent AI review

Claude produces a parity and limitation report. ChatGPT independently inspects the repository, reruns or reviews tests and reports agreement or disagreement. Resolve disagreements before UI work.

## Phase 9 — New V10 renderer

Build a new thin client against the canonical request/result contract. Reuse visual design where useful, but do not incrementally mutate the placeholder into the final engine. Archive or replace the placeholder only after full integration tests.

# 39. Definition of feature parity

Feature parity is capability-based, not file-based. For every useful historical calculation, rule, output or diagnostic, the report must state whether it is:

implemented and independently validated; implemented but provisional; sandboxed research; measurement-required; rejected as incorrect; superseded by a better method; intentionally deferred; or presentation-only.

A historical feature is not “preserved” merely because a screenshot resembles it. The engine must represent the underlying physical and electrical meaning. Conversely, not every historical formula must be promoted. Incorrect or unsupported logic should be rejected with evidence.

# 40. Definition of success

Success is achieved when:

there is one authoritative computation engine;

the browser contains no engineering truth of its own;

all useful V6–V10 logic is accounted for;

important formulas are independently validated;

every cartridge is tested and versioned;

results are traceable to objects, paths, equations and evidence;

unknowns remain visible;

complete conductor schedules and electrical calculations are possible;

advanced research remains separated from standards-backed calculations;

a clean clone reproduces tests and reports;

Claude and ChatGPT independently agree that the engine is materially stronger than the historical lineage;

and a new browser can be built as a renderer rather than a calculator.

# 41. What must not happen

Do not patch the current browser as the primary recovery strategy.

Do not copy its `compute()` function into one large engine file and call that modularisation.

Do not delete V6–V9.

Do not trust old AI statements without repository inspection.

Do not confuse documentation with executable capability.

Do not treat a manufacturer default as a universal constant.

Do not use ambient temperature where cell temperature is required.

Do not mix factory leads with EPC-installed cable.

Do not mix differential and common-mode capacitance.

Do not issue unsupported compliance conclusions.

Do not hide missing evidence.

Do not weaken tests to obtain green status.

Do not create an attractive debugger that still duplicates engineering logic.

Do not rebuild the public V10 UI before parity approval.

# 42. Known current commits and repository events

The following commits were observed during the preceding ChatGPT thread and provide useful historical anchors. Reconfirm them in a new thread because the repository may have advanced.

`42fdd2896a409117f99d1fb64064cd2dc3c63956` — Build V10 Ventus DC String Engine foundation. This added the initial kernel, evidence model, tests, governance and browser workbench while preserving V6–V9.

`0e2cff82016b770d844d2f13ad61abc155a2a13a` — restore snapshot before the 24-string V10 browser build.

`867ae32387a85b56d3979c2ef3af89d0302349c6` — restore register recording V10 main restore points.

`fe1b7cc883742f89729057b3aba8f90b7485bac4` — Build V10 complete 24-string inverter workbench on main.

Earlier V9 commits include the pure computation engine, deterministic tests, computation console, thin shell and CI-related fixes. Inspect commit history rather than relying solely on this list.

# 43. Homepage context

GlobalGrid2050’s homepage was updated to expose the V10 public application and later reordered. The latest observed homepage ordering commit was `82fb69e9285986dcee18efe80d5f71a7c75202c9`. This is context only. The homepage repository is separate. Do not modify it during computation recovery unless explicitly asked. The public V10 link should continue to point to the placeholder until a replacement is approved.

# 44. Engineering defaults currently used in examples

Historical examples commonly use a 30-module string, approximately 1.303 m module width or pitch basis, 1.4 m positive and 1.4 m negative factory leads, 4 mm² factory lead conductors, 6 mm² external copper string cable, operating current around 17.31 A, 12 MPPTs, two strings per MPPT and 24 active strings. Module Voc examples around 50 V, negative Voc temperature coefficients and a 1,500 V system limit appear in the code.

These are example inputs, not universal truths. Preserve provenance. Exact module terminal geometry, lead usable reach, connector family, route, conductor temperature and inverter internal topology require evidence or explicit assumption.

# 45. Relationship to broader Ventus engineering work

The engine is intended to support utility-scale PV design, procurement, risk analysis, repowering, measurement planning and advanced DC behaviour research. It should eventually scale from one module connection to a complete inverter and plant. It may support public education and open-source development, but it must preserve engineering integrity.

The owner has extensive practical cable-design and utility-scale solar experience. The engine’s value is not a generic calculator UI. Its value is representing the physical DC layer that conventional models frequently compress into a single length and resistance. Preserve that purpose.

# 46. Review protocol for ChatGPT in a new thread

After reading this file, ChatGPT should:

1. Fetch repository metadata and current default branch.
2. Fetch this handover directly from GitHub.
3. Inspect current `v10-development` and any `v10-debugger` entry files.
4. Search recent commits after this file’s commit.
5. Inspect Claude’s reports, ledgers, tests and source changes.
6. State what is verified, what changed and what remains uncertain.
7. Review architecture against this handover and repository doctrine.
8. Avoid changing code until the user asks or a clearly authorised task is present.
9. When asked to edit, use small commits and verify the resulting file.
10. Preserve citations or exact paths when describing repository facts.

# 47. Questions ChatGPT should continually ask

Is this result computed by one authoritative engine or duplicated?

What physical object does this number describe?

Is this distance displacement, route length, conductor length or loop length?

What are the start and end terminals?

What is the conductor class and ownership?

What evidence supports the input?

What uncertainty or bounding case applies?

Does the topology form one valid series path?

Are positive and negative paths represented separately?

Are factory leads, extensions, home runs and contacts separate?

Is temperature physically the correct temperature?

Is the result steady-state, standards-guided, advanced research or measurement-dependent?

Can an independent model reproduce it?

Does a clean clone pass the tests?

Is the browser rendering the result or recreating it?

# 48. Expected Claude outputs before implementation is considered mature

Claude should eventually produce:

A full V6–V10 inventory.

A duplicate and conflict map.

A branch recovery report.

A migration ledger in JSON or CSV and Markdown.

Canonical request and result schemas.

Cartridge READMEs and changelogs.

Independent reference models.

Deterministic test catalogue.

Golden numeric cases.

Historical regression suite.

Clean-clone execution report.

Feature-parity report.

Known-limitations report.

Missing-evidence register.

Calculation-change notes.

A recommendation on whether the public browser may be rebuilt.

# 49. Expected ChatGPT role after reboot

ChatGPT is not merely a second coder. Its role is independent auditor, architecture reviewer, calculation challenger, repository operator when asked, continuity keeper and translator between the owner’s engineering intent and the implementation. It should inspect Claude’s work critically rather than endorsing it automatically.

When Claude claims a formula is validated, ChatGPT should inspect the derivation and test vector. When Claude claims a branch is recovered, ChatGPT should inspect the branch report and commits. When Claude claims feature parity, ChatGPT should compare the ledger and historical versions. When browser rebuilding is proposed, ChatGPT should confirm that the canonical engine is the sole source of engineering results.

# 50. Final governing statement

The project must not produce another V10 by haste. The current work demonstrated that a sophisticated browser can overtake an incomplete kernel and recreate the very architecture the repository had already rejected. The recovery is an opportunity to correct that without discarding useful work.

The stable target is one computation platform assembled from tested engineering cartridges, built from physical objects and actual topology, with explicit routes, terminals, conductors, electrical boundaries, evidence and uncertainty. V6, V7, V8, V9 and the current V10 are evidence sources. None is automatically the final truth. Each useful method must be inventoried, independently challenged, migrated deliberately and tested.

The browser comes last. It should be a powerful visual instrument, but its power must come from a trusted engine. A user should be able to draw or describe a PV DC system, submit a canonical model, receive deterministic engineering results and trace every figure back to the physical circuit and its evidence. The same engine should support a text report, JSON export, CSV schedule, command-line test, future API and future optimisation process without reproducing the mathematics.

Until that condition is achieved, keep the present V10 public page as a placeholder, keep the historical versions intact, work in `v10-debugger`, model independently, test adversarially, state uncertainty honestly and do not claim completion.
