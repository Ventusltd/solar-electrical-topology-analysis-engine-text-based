# Quantum Spawn

**Title:** Employer Requirements Part 2 — Architecture, Open Standards and Software Simplicity

**File:** `202607312338-employer-requirements-part-2-architecture-open-standards.md`

**Timestamp:** 2026-07-31 23:38 Europe/London

**Version:** 1.0

**Status:** Canonical employer requirement

**Authority:** Product Owner and Engineering Design Authority

**Supersedes:** None

**Superseded By:** None

**Dependencies:**
- `202607311609-mission-and-philosophy.md`
- `202607311615-system-architecture.md`
- `202607312336-employer-requirements-part-1-mission-public-value.md`

**Current Build Relevance:** Build 025.5, backend-to-studio authority bridge and all later interfaces

---

## 1. Purpose

This module defines the employer’s requirements for software architecture, simplicity, interoperability, open standards and long-term maintainability. The platform shall pursue exceptional capability without becoming an opaque monolith. Its sophistication must emerge from clear objects, explicit dependencies, deterministic transformations and small replaceable components.

The architecture shall be understandable by a competent engineer who did not participate in its creation.

## 2. Single engineering authority

The Python package remains the only engineering authority. It owns physical objects, geometry, topology, routing, electrical calculations, evidence qualification, diagnostics, standards rules, future optimisation and deterministic receipts.

The browser may collect user intent, issue commands, display results and manage ordinary interface state. It must not independently route cables, infer topology, calculate resistance, voltage drop, loss, electromagnetic quantities or standards outcomes.

The current Topology Studio is therefore a useful interaction prototype but not the final architecture. Its browser-side calculations must eventually be removed or quarantined as historical demonstration logic. Useful interaction ideas may be retained only when the same commands are validated and materialised by the kernel.

## 3. Simplicity requirement

Simplicity means one concept has one authoritative representation. There shall not be separate browser, Python, report and export versions of the same engineering truth.

A string shall have one stable identity. A conductor route shall be an ordered set of explicit segments. An evidence source shall have one versioned record. A calculation shall reference its exact upstream hashes. A displayed metric shall be a projection of a kernel result rather than a second implementation.

The codebase shall prefer small typed functions, immutable records, explicit enumerations and deterministic serialisation. Hidden mutable global state, implicit unit conversion, magic defaults and duplicated formulas are prohibited in authoritative paths.

Abstractions must earn their place. Generalisation shall be introduced when at least two real engineering cases require it, not merely because a framework permits it.

## 4. Command and response boundary

The next major architectural bridge shall define versioned commands and responses for creating projects, importing data, placing or updating objects, assigning strings, changing topology, moving equipment, requesting routes, running calculations and requesting diagnostics.

Every command must declare the expected input schema, actor intent, target identifiers and optimistic concurrency or source receipt where required. Every response must declare result status, created or changed identifiers, diagnostics, evidence state, dependency hashes and deterministic receipt references.

A command shall never return a bare number when the engineering meaning depends on units, evidence or applicability.

The initial boundary may be a deterministic CLI, file protocol, local HTTP service or combination. The core calculation package shall remain independent from transport.

## 5. Open schema standards

Engineering objects and exchange payloads shall use JSON Schema Draft 2020-12 or a later explicitly adopted compatible version. Schemas shall be versioned, testable and capable of validating required fields, enumerations, units, identifiers and extension boundaries.

Where HTTP is used, the interface shall follow OpenAPI 3.1 or a later explicitly approved version. The specification shall be generated or checked from the real implementation so documentation cannot drift silently.

Provenance shall align conceptually with W3C PROV: entities, activities, agents, derivations and responsibility relationships must be expressible even where the internal representation remains simpler.

Site and route exchange shall use GeoJSON-compatible geometry where appropriate, while retaining engineering-specific identifiers and dimensional metadata outside ambiguous free-form properties.

Plant-scale tabular outputs shall support Apache Arrow and Parquet for efficient typed interchange. CSV may remain an accessible export, but it shall not be the only format for hierarchical or high-volume data.

## 6. Units and identifiers

All authoritative numerical values shall have explicit units or belong to a schema field whose unit is unambiguous and immutable. Internal calculations shall preserve dimensional safety using Pint or the existing verified unit policy.

Identifiers must remain stable across rendering, export and re-import. Human labels may change without changing identity. External identifiers shall be stored as aliases.

Hashes shall identify deterministic engineering payloads, not runtime envelopes. Timestamps, actors, environments and commits belong in execution envelopes linked to engineering hashes.

## 7. Local-first and offline operation

A complete reference workflow must run locally and offline after dependencies are installed. Users must be able to inspect schemas, execute calculations, validate projects and export reports without an internet connection.

Hosted deployment may provide collaboration or public demonstrations, but it shall remain replaceable and shall not make paid services mandatory.

Static GitHub Pages demonstrations shall use committed example response bundles and clearly state that they are projections of precomputed authority. They shall not pretend to provide live authoritative calculations where no Python service exists.

## 8. World-class software references

The product shall study QGIS for layer management, project persistence, spatial editing and large-dataset navigation; KiCad for hierarchy, inspectability, selection, net-aware workflows and professional information density; and pandapower for extensible Python element models and reproducible analysis.

These references are patterns, not templates. Adopt their strongest ideas without copying unnecessary complexity.

Testing shall include deterministic fixtures, invariants, schema round trips, public API contracts, clean-wheel installation, browser end-to-end checks and accessibility checks. Performance fixtures shall represent at least 30 kWp, 1 MWp, 100 MWp and 1 GWp systems.

## 9. Replaceability and longevity

Presentation, storage and deployment technologies are replaceable. Canonical schemas, semantics and receipts must outlive libraries.

Migrations shall be explicit and reversible. Deprecated fields shall have documented replacement paths. Public API names shall remain classified as canonical, provisional or compatibility surfaces.

## 10. Architectural success

This requirement is satisfied when a project created through any supported interface produces the same authoritative objects, diagnostics and hashes; when the browser contains no competing engineering formulas; when a clean installed package can reproduce reference cases offline; and when another implementation can consume the published schemas without reverse-engineering the code.

The governing software principle is:

**Maximum engineering capability through minimum duplication, explicit contracts, open standards and one authoritative computational path.**
