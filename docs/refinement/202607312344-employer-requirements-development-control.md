# Refinement 07 — Employer Requirements Development Control

Timestamp: 2026-07-31 23:44 Europe/London

Status: Active programme control

Authority: Product Owner requirements interpreted through the existing Engineering Design Authority

Dependencies:
- `docs/quantum-spawn/202607311609-mission-and-philosophy.md`
- `docs/quantum-spawn/202607311615-system-architecture.md`
- `docs/refinement/202607312059-build-025-5-authority-consolidation.md`
- `docs/quantum-spawn/202607312336-employer-requirements-part-1-mission-public-value.md`
- `docs/quantum-spawn/202607312338-employer-requirements-part-2-architecture-open-standards.md`
- `docs/quantum-spawn/202607312340-employer-requirements-part-3-electrical-diagnosis.md`
- `docs/quantum-spawn/202607312342-employer-requirements-part-4-interface-reporting-quality.md`

## 1. Purpose

This refinement converts the four canonical employer-requirement modules into an executable development-control framework. It does not replace the Quantum Spawn architecture, reopen settled authority rules or authorise broad simultaneous implementation.

The employer requirements define the destination and user value. The existing mission, system architecture, geometry authority, array engine, physics boundary, standards philosophy and Build 025.5 refinement define how that destination may be reached safely.

When a desired feature conflicts with an architectural invariant, the feature must be redesigned rather than weakening the invariant.

## 2. Current verified position

The current authoritative programme remains Build 025.5D1. The package provides deterministic geometry, topology, assignment, routing, steady-state calculation receipts, evidence-bound conductor resistance, source qualification and deterministic qualification-assessment serialisation.

The latest declared green validation before these documentation-only requirements comprised:

```text
Python                             274 passed
V8 model                           13/13
V8 authority reconciliation         6/6
V9 deterministic engine            10/10
V10 JavaScript                     13/13
Clean installed wheel              PASS
```

The public `progress-dashboard.html`, root README and V10 README do not accurately describe this state. The Topology Studio remains an exploratory browser calculator rather than the final thin client.

The overall programme shall continue to be described as approximately 38–40 percent complete until a weighted programme manifest replaces this provisional estimate. Green tests prove implemented scope; they do not prove completion of standards, EMC, plant ingestion, reporting or final interface work.

## 3. Controlling architecture

All development arising from the employer requirements shall obey these controls:

1. Python is the sole engineering authority.
2. Geometry, topology, routing, physics, evidence and validation remain separate dependency domains.
3. The browser issues commands and renders results; it does not calculate engineering.
4. Missing evidence remains missing and blocks or qualifies downstream authority.
5. Deterministic engineering receipts exclude runtime metadata.
6. Open standards support interchange but do not dictate internal engineering semantics.
7. Local and offline execution is a release requirement.
8. A 24-by-30 fixture is a regression case, not a product limit.
9. Plant scale is achieved by composition, indexing and aggregation without loss of string-level traceability.
10. Each material tranche requires a restore point, bounded implementation, tests, full validation and a Quantum Spawn checkpoint.

## 4. Development goals register

### Goal ER-01 — Complete the resistance-qualification public contract

Expose the three assessment serialisation functions through the supported `solar_topology` package API and classify them explicitly as provisional. Extend the clean-wheel probe to calculate the same payload, canonical JSON and hash outside the repository.

Acceptance:
- top-level import identity is tested;
- explicit public classification exists;
- clean wheel reproduces the hash;
- no calculation receipt changes;
- no source is promoted.

This remains the immediate next bounded step.

### Goal ER-02 — Establish a machine-readable programme manifest

Create one versioned manifest containing current build, programme stage weights, package version, validated commit, test counts, restore point, current Quantum Spawn, canonical capabilities, provisional capabilities, historical workbenches, active gates and next bounded step.

Generate or validate the dashboard and README status sections from this manifest.

Acceptance:
- dashboard no longer reports Build 024 or 176 tests;
- manual completion percentages are removed;
- CI fails on manifest-to-page drift;
- historical test success is not presented as canonical authority.

### Goal ER-03 — Define backend command and response schemas

Create JSON Schema 2020-12 contracts for project creation, object mutation, equipment movement, string assignment, topology selection, route request, steady-state request and diagnostic request.

Acceptance:
- all commands are versioned;
- identifiers, units, evidence and dependency receipts are explicit;
- schema round-trip and invalid-input tests pass;
- transport remains replaceable;
- no browser calculation is introduced.

### Goal ER-04 — Implement one local authority bridge

Expose the command boundary through a deterministic CLI, file protocol or minimal local service. HTTP may use OpenAPI 3.1, but the core package must remain transport-independent.

Acceptance:
- complete reference workflow operates offline;
- clean installation can submit a project command and receive deterministic objects and receipts;
- repeated commands produce identical engineering payloads;
- runtime metadata is isolated in an execution envelope.

### Goal ER-05 — Create the first real thin-client vertical slice

Replace one Topology Studio workflow with commands to the Python authority. The browser shall render returned hierarchy, geometry, diagnostics and receipts.

Acceptance:
- no route, resistance, voltage-drop or loss formula remains in the production browser path;
- GitHub Pages uses clearly labelled precomputed example bundles;
- local interactive mode connects to the authority bridge;
- Playwright verifies command-to-render behaviour;
- the old browser calculator is retained only as historical reference or removed through an explicit migration.

### Goal ER-06 — Deliver the professional diagnostic workspace

Implement the hierarchy navigator, kernel-supplied canvas, context inspector, diagnostics drawer and evidence/receipt panel using progressive disclosure.

Acceptance:
- keyboard navigation and WCAG 2.2 AA checks;
- no authoritative `contenteditable` data entry;
- values show units and evidence;
- selecting diagnostics highlights affected objects;
- blocked and provisional results are distinguishable without colour alone.

### Goal ER-07 — Prove the 30 kWp-to-plant scale model

Create deterministic fixtures for approximately 30 kWp, 1 MWp, 100 MWp and 1 GWp projects using the same object and calculation semantics.

Acceptance:
- one engineering algorithm across all fixtures;
- measured execution time and memory;
- lazy loading or columnar aggregation where required;
- plant summaries retain drill-down to string and evidence records;
- no hidden fixed MPPT, input, string or module limit.

### Goal ER-08 — Complete evidenced dimensional geometry

Resume Build 025.5E only after the authority bridge foundations are stable. Add evidenced terminal coordinates, table-plane orientation and explicit site-three-dimensional routes.

Acceptance:
- geometry class states are explicit;
- no universal tilt multiplier;
- terminal reach and lead feasibility consume versioned evidence;
- stale JavaScript PR geometry is not resurrected as authority.

### Goal ER-09 — Begin Build 026 standards diagnostics

Implement rule schemas, statuses and deterministic receipts before individual standards calculations. Then add `K_I`, `K_Corr`, backfeed, overcurrent, fuse, grouped-protection, voltage-scope and SPD critical-length rules in separate tranches.

Acceptance:
- standard, edition and clause provenance;
- incomplete evidence and outside-scope states;
- no automatic design mutation;
- conflicts remain visible;
- no general compliance certificate.

### Goal ER-10 — Preserve the Build 027 physics boundary

Do not start mind-blowing EMC graphics before spatial field inputs and model applicability exist. Loop geometry, capacitance, inductance, surge and distributed-line functions must remain geometry-derived and evidence-qualified.

Acceptance:
- signed area, absolute area, area vector, flux and induced voltage remain distinct;
- same-string pairing and bonded structures are explicit;
- lumped versus distributed applicability is reported;
- no generic lightning multiplier is promoted.

## 5. Priority order

The governing order is:

```text
ER-01 qualification API completion
ER-02 programme truth manifest
ER-03 command and response schemas
ER-04 local authority bridge
ER-05 first thin-client vertical slice
ER-06 professional workspace
ER-07 scale fixtures
ER-08 dimensional geometry
ER-09 Build 026 standards diagnostics
ER-10 Build 027 physics progression
```

This order may be changed only by a later explicit employer instruction or a verified dependency finding. Interface design may be prototyped earlier, but no prototype may acquire engineering authority.

## 6. Free and open control

No goal may make a paid API, private map service, proprietary database or closed file format mandatory. Optional integrations must have documented open substitutes.

Project import, calculation, diagnosis and export must remain possible through the local open-source distribution. Public example data must respect licensing, confidentiality and evidence boundaries.

## 7. Completion and reporting control

Every goal shall report:

```text
scope attempted
scope completed
files and schemas changed
authority classification
tests and performance
known limitations
public-page consequences
next bounded step
```

The progress dashboard shall eventually derive its completion state from these controlled goals. Until then, documentation shall avoid false precision.

## 8. Final control statement

The employer requirements are ambitious by design, but implementation shall remain incremental. “Mind-blowing” means a user can understand a vast solar asset through one truthful model, not that the project accumulates unverified features.

The controlling development rule is:

**Advance one authoritative vertical slice at a time, preserve the architecture, prove the evidence, expose the limitations and make every improvement available freely to the solar engineering community.**
