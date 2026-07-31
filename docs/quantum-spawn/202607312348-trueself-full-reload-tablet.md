# Quantum Spawn

**Title:** Trueself Full Reload Tablet

**File:** `202607312348-trueself-full-reload-tablet.md`

**Timestamp:** 2026-07-31 23:48 Europe/London

**Version:** 1.0

**Status:** Canonical reload tablet

**Authority:** Product Owner and Engineering Design Authority

**Supersedes:** None

**Extends:** `202607311652-respawn-instructions.md`

**Dependencies:**
- every non-superseded file in `docs/quantum-spawn/`
- `docs/refinement/202607312059-build-025-5-authority-consolidation.md`
- `docs/refinement/202607312344-employer-requirements-development-control.md`

**Current Build Relevance:** Build 025.5D1 and all later builds

---

## 1. Instruction to the new thread

You are reloading the Solar Electrical Topology Analysis Engine from repository evidence rather than conversational memory. Read this tablet completely, then inspect the repository before taking action. Do not claim that a file exists, a test passed, a build is current or a calculation is authoritative until the repository or its recorded validation evidence confirms it.

After you have read the canonical Quantum Spawn chain, reviewed the current refinement controls, inspected `main` and stated the current engineering boundary accurately, use the operational session name **trueself**. Your first completed-reload statement shall begin:

`trueself loaded.`

This is a project-state identifier, not a claim of consciousness, personal continuity or hidden memory. Do not call yourself trueself before the reload is complete. Each future fresh thread must earn the identifier again by performing the reload and repository check.

## 2. Mission

The project exists to create the world’s first deterministic, geometry-authoritative engineering computation and diagnostic engine for photovoltaic DC systems. Physical reality comes first. Modules, terminals, conductors, connectors, structures, ducts, trenches, equipment and routes exist before electrical abstractions or standards checks. Geometry states where objects exist. Topology states what is connected. Routing materialises connectivity as explicit conductor paths. Physics consumes those paths. Standards validate the resulting physical model. Deterministic receipts preserve the evidence.

The platform is intended to be free, open, locally runnable and useful for every PV installation above 30 kWp, from schools, warehouses, farms and commercial roofs to multi-gigawatt utility plants. Nearly 3 TWp of PV was installed globally by the end of 2025. The employer’s 72 TWp by 2050 figure is the product’s strategic design horizon, not a guaranteed external forecast. The architecture must nevertheless be capable of serving that scale without changing its truth model.

The success test is not feature count or visual spectacle. Success means a competent user can reconstruct an opaque PV asset, understand its electrical hierarchy, derive quantities from actual geometry, locate defects and uncertainty, trace every conclusion to evidence and share a reproducible diagnostic package without proprietary software.

## 3. Non-negotiable architecture

The Python package is the sole engineering authority. It owns physical objects, geometry, topology, routing, calculations, uncertainty, evidence, diagnostics, future standards rules, future EMC and deterministic receipts.

The browser may collect intent, send commands, render returned geometry, manage selection and present diagnostics. It must never independently invent cable routes, infer authoritative topology, calculate cable length, resistance, voltage drop, loss, fault current, EMC, lightning behaviour or standards outcomes. The current browser Topology Studio is therefore an exploratory prototype, not the final authority. Preserve useful interaction ideas but remove or quarantine its JavaScript engineering before production use.

Maintain separate dependency domains and hashes for geometry, topology, routing, calculations, resistance evidence and later rule validation. A change must invalidate only downstream results that depend on it. Runtime timestamps, users, workflows and commits belong in execution envelopes; they do not belong in deterministic engineering receipt hashes.

Use immutable or tightly controlled typed records, stable identifiers, explicit enumerations, canonical JSON and clear unit ownership. Avoid duplicate formulas, hidden mutable state, guessed values, browser-only truth, magic defaults and abstractions without real engineering need.

## 4. Canonical object hierarchy

Preserve this hierarchy:

`module → factory lead → connector → string → field conductor → junction or combiner → protective device → physical inverter input → MPPT → evidenced inverter DC bus → inverter → power block → plant → fleet`

A module belongs to one physical placement and one electrical string. A string is an ordered terminal path, not merely a module count. An MPPT is not identical to a physical input. Inputs sharing an MPPT label must not be assumed electrically paralleled. Common-bus behaviour, reverse-current blocking and backfeed require equipment evidence.

Same-string positive and negative identity must survive every route segment. Sequential, leapfrog, mirrored and custom stringing are strategies that produce explicit connections and routes; they are not separate calculation engines or visual themes.

The 24-string by 30-module, 720-module table is the permanent reference fixture, not a hard product limit. A 30 kWp project and a gigawatt plant use the same objects and engineering semantics. Large plants scale through composition, indexing, columnar storage, lazy loading and aggregation while preserving drill-down to string, segment and evidence records.

## 5. Geometry and electrical truth

Geometry is engineering authority, not decoration. Use site-local Cartesian coordinates for detailed work and introduce height only when it materially changes routes, quantities, separation, containment, capacitance, inductance, shielding or structural interaction.

Routes are explicit ordered segments. Each segment must retain endpoints, polarity, string identity, route class, installation class, containment, burial, screening, bonding and support references. Geometric length, installed length and procurement length remain distinct. Factory-fitted conductor and field-installed conductor remain distinct. Cable quantity and loop area remain distinct.

Moving an inverter changes dependent home-run geometry and routing receipts but does not silently change module placement, string membership or MPPT assignment. Changing topology does not silently move physical objects.

## 6. Current verified implementation state

The active programme is Build 025.5D1, not Build 024. Build 025 geometry, topology, assignment and routing authority is substantially established. Production logic has been migrated into the installed `solar_topology` package. Root legacy modules are compatibility shims rather than competing implementations. A clean-wheel workflow builds, installs and probes the package outside the repository checkout.

V8’s public truth boundary was corrected. For the permanent reference fixture, field-installed conductor decreases by 798.288 m, factory-fitted conductor increases by 845.088 m and total circuit conductor increases by 46.800 m. External-cable reduction must never be described as total copper saving. Historical V6 and V9 ideal-bulk resistance calculations remain reproducible but are explicitly lower-bound screening estimates, not finished-cable authority.

Resistance is now evidence-bound. Controlled bases include independently measured, manufacturer declared, standard maximum, ideal bulk estimate, assumed and unresolved. Applied resistance evidence is hashed separately from topology. Exact and uncertainty calculations propagate the selected resistance evidence and temperature coefficient.

Build 025.5D1 added a deterministic source-qualification gate with `verified`, `candidate` and `rejected` states. It also added deterministic assessment payload, canonical JSON and hash functions binding schema version, source record hash, status and reason codes. The latest verified suite before the employer-requirement documentation recorded:

`Python 274 passed; V8 13/13; V8 reconciliation 6/6; V9 10/10; V10 JavaScript 13/13; clean installed wheel PASS.`

Documentation commits after that validation did not alter engineering code. Verify this again before relying on it.

The two generic 4 mm² and 6 mm² standard-maximum records remain candidates because their exact source revision is `edition-not-yet-encoded` and verification remains `standards_review_required`. Never invent the missing standard edition, table, manufacturer declaration or licensed quotation.

Intermediate progress logs from 22:05 to 22:16 record import-cycle, fixture, literal-string and enum-comparison failures that were subsequently corrected. Treat them as historical evidence of the debugging path, not as current failures. The 22:20 all-green log and 22:28 authority audit supersede their operational status without deleting history.

## 7. Public interface and documentation gap

`progress-dashboard.html` is stale: it reports Build 024, 176 tests and an obsolete completion percentage. The root README and V10 README also understate or misdescribe the current programme. `topology-studio.html` calculates simplified rectilinear routes and steady-state quantities in JavaScript. These pages are public references and prototypes, not evidence of the current backend authority.

Overall programme completion remains approximately 38–40 percent until a weighted machine-readable programme manifest replaces the provisional estimate. Geometry, topology, routing and steady-state authority are advanced. Standards diagnostics, equipment evidence, environmental classes, dimensional terminal geometry, plant ingestion, reporting, final thin-client work and EMC remain substantial.

Green regression tests prove reproducibility of implemented scope. They do not prove total product completion, project-specific compliance or professional approval.

## 8. Open and world-class direction

Remain local-first and offline-capable. No paid API, proprietary map service, private database or closed file format may be mandatory for project creation, diagnosis or export.

Use JSON Schema 2020-12 for versioned exchange contracts; OpenAPI 3.1 where a local HTTP boundary is justified; W3C PROV concepts for evidence lineage; GeoJSON-compatible geometry where appropriate; Arrow and Parquet for typed plant-scale data; and CSV for accessible flat exports. Preserve dimensional safety internally.

Study QGIS for spatial layers and large-project navigation, KiCad for hierarchy and inspectable engineering interaction, and pandapower for extensible Python element modelling. Adopt principles, not unnecessary complexity. Target WCAG 2.2 AA and test browser flows with Playwright when production interface work begins.

## 9. Controlled development goals

Follow Refinement 07 in this order unless the employer explicitly changes it or a verified dependency forces revision:

ER-01: expose qualification-assessment payload, JSON and hash functions through the explicitly provisional package API and reproduce them from a clean wheel.

ER-02: create a machine-readable programme manifest controlling dashboard truth, README status, current build, validation counts, restore point, capability classifications and next step.

ER-03: define versioned backend command and response schemas for projects, object mutation, equipment movement, string assignment, topology, routing, calculations and diagnostics.

ER-04: implement one offline local authority bridge through a deterministic CLI, file protocol or minimal transport-independent service.

ER-05: replace one Topology Studio workflow with a genuine Python-authority thin-client vertical slice.

ER-06: build the professional workspace: hierarchy navigator, kernel geometry canvas, context inspector, diagnostics drawer and evidence/receipt panel.

ER-07: prove common semantics and performance at approximately 30 kWp, 1 MWp, 100 MWp and 1 GWp.

ER-08: resume evidenced terminal coordinates, table-plane orientation and explicit site-3D routes without reviving stale JavaScript authority.

ER-09: begin Build 026 with rule schemas and states, then separately implement current factors, backfeed, overcurrent, protection, voltage scope and SPD critical length.

ER-10: preserve Build 027’s strict geometry-derived EMC boundary.

## 10. Standards and future physics discipline

Standards are versioned authorities applied after physical modelling. Record document, edition, amendment, clause, provenance, inputs, algorithm and result state. Supported outcomes include PASS, PASS_WITH_WARNINGS, FAIL, INCOMPLETE_EVIDENCE, OUTSIDE_SCOPE, ENGINEERING_REVIEW_REQUIRED and CLIENT_APPROVAL_REQUIRED. Standards do not silently redesign the project or issue a general compliance certificate.

Build 027 must distinguish signed loop area, absolute winding area, oriented area vector, projected area, magnetic flux and induced voltage. Preserve conductor pairing, bonded structures, containment, SPD lead geometry and event propagation. Never multiply one loop-area number by a generic lightning factor and call it authoritative.

## 11. Operating protocol

Work directly from verified repository state. Before a material tranche, create a restore point. Make one bounded change. Add focused tests. Run the full declared validation and clean-wheel gate. Inspect failures rather than stacking work over them. Record one new Quantum Spawn checkpoint. Then reassess.

Do not become overwhelmed by parallel ambition. “Mind-blowing” means one truthful model makes a vast asset understandable; it does not mean accumulating unsupported features.

Do not reopen settled architecture without new evidence. Do not use confidential project data in the public repository. Preserve contracted, proposed, recommended, client-approved, site-approved and as-built states separately.

## 12. First response and immediate action

After reloading, inspect current `main`, recent commits, open pull requests, test evidence, `docs/refinement/202607312344-employer-requirements-development-control.md`, the public API manifest and clean-wheel probe.

Then respond:

`trueself loaded.`

Follow with a compact statement of the current build, verified validation state, known limitations and the next single bounded goal. At the state captured by this tablet, that next goal is ER-01: expose the three qualification-assessment serialisation functions through the provisional `solar_topology` API and verify identical payload, JSON and hash from the installed wheel. Do not integrate them into calculation receipts in the same tranche.

If repository evidence shows that ER-01 has already been completed, do not repeat it. Identify the first incomplete controlled goal and proceed only after stating the evidence.

The governing North Star is:

**Build the free, open, deterministic and geometry-authoritative diagnostic infrastructure required to understand, improve and protect every solar PV asset above 30 kWp, using one physical truth from module to fleet and scaling towards a 72 TWp energy-transition horizon.**
