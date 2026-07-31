# Quantum Spawn

**Title:** Employer Requirements Part 4 — User Interface, Reporting, Quality and Programme Legibility

**File:** `202607312342-employer-requirements-part-4-interface-reporting-quality.md`

**Timestamp:** 2026-07-31 23:42 Europe/London

**Version:** 1.0

**Status:** Canonical employer requirement

**Authority:** Product Owner and Engineering Design Authority

**Supersedes:** None

**Superseded By:** None

**Dependencies:**
- `202607311615-system-architecture.md`
- `202607312336-employer-requirements-part-1-mission-public-value.md`
- `202607312338-employer-requirements-part-2-architecture-open-standards.md`
- `202607312340-employer-requirements-part-3-electrical-diagnosis.md`

**Current Build Relevance:** Backend-to-studio authority bridge, reporting programme and final thin client

---

## 1. Purpose

This module defines the employer’s requirements for interface legibility, professional workflow, diagnostic reporting, accessibility, public programme truth and software quality. The finished product shall make a complex electrical model understandable without hiding its engineering depth.

The interface is the disciplined projection through which users inspect reality, evidence, calculations and limitations. Legibility includes correctness, hierarchy and traceability.

## 2. Current public-interface correction

The existing Topology Studio demonstrates useful ideas: arbitrary string counts, MPPT assignment, topology choice, a central spatial view and string-level inspection. It also calculates geometry and electrical quantities directly in JavaScript. That calculation path is exploratory and must not become the production truth.

The final Studio shall send commands to Python and render returned objects, diagnostics and receipts. Static demonstrations must identify precomputed outputs clearly.

The progress dashboard is also stale. It currently reports an older build, old test counts and an obsolete completion percentage. Public progress claims shall be generated from machine-readable repository state or rejected by CI when they drift.

## 3. Professional workspace

The principal interface shall use a clear professional workspace with five cooperating regions:

```text
project and electrical hierarchy navigator
central geometry and topology canvas
context-sensitive inspector
diagnostics and required-actions drawer
evidence and receipt panel
```

The hierarchy navigator shall allow movement from plant to power block, inverter, MPPT, physical input, string, module, route segment, connector and evidence record.

The central canvas shall visualise kernel-supplied geometry. It shall support selection, zoom, filtering, layering, comparison states and navigation to associated electrical objects. It shall not invent vertices or routes.

The inspector shall show editable command inputs separately from computed outputs. Every value shall display its unit, source state and applicability. Unsupported editing shall be disabled rather than silently ignored.

## 4. Progressive disclosure

The default view shall answer ordinary questions without presenting every engineering field simultaneously. Advanced parameters, hashes, formula identifiers and provenance graphs shall remain accessible through progressive disclosure.

Plant-level users should first see capacity, object counts, blocked diagnostics, worst strings, loss, cable quantities and evidence completeness. Engineers shall be able to drill into segment calculations, temperature basis, resistance evidence, topology traversal and deterministic payloads.

Simplification shall arrange information without removing traceability.

## 5. Diagnostic communication

Every diagnostic shall use plain technical language and a stable code. It shall state condition, location, consequence, confidence, evidence and next action.

Severity colour may assist scanning but shall never be the only encoding. Status must also use text, icons or patterns. Warnings shall distinguish blocked calculations, provisional results, engineering review, client approval and informational observations.

A user shall be able to select a finding and highlight every affected object on the canvas and in the hierarchy. Conversely, selecting an object shall reveal all relevant diagnostics and evidence gaps.

## 6. Accessibility and legibility

The interface shall target WCAG 2.2 AA. Keyboard operation, visible focus, semantic headings, accessible names, screen-reader relationships and high-contrast presentation are mandatory.

SVG and canvas content shall have accessible summaries and selected-object descriptions. Tables shall retain headers and support horizontal complexity without destroying mobile usability.

Ambiguous `contenteditable` cells are prohibited for authoritative commands. Use labelled controls with validation, units and controlled value types.

Typography shall distinguish identifiers, values, units, status and explanatory text. Dense engineering information is acceptable when alignment and hierarchy remain clear. Important numbers shall not depend on tiny type or excessive decimal precision.

## 7. Project workflow

A user shall be able to create or import a project, establish the hierarchy, add equipment profiles, place objects, define topology, request routes, run supported calculations, review diagnostics and export evidence.

Edits shall be commands with visible consequences. Before-and-after states shall remain comparable. Undo or revision history shall operate through deterministic project states rather than browser-only mutation.

The interface shall identify unsaved commands, invalid inputs, stale downstream receipts and blocked calculations. A geometry change shall visibly invalidate only dependent routing and calculation outputs.

## 8. Reporting and exchange

The engine shall produce a compact reproducible diagnostic package containing project metadata, object inventory, geometry, topology, routes, equipment references, evidence register, calculations, diagnostics, limitations and receipt hashes.

Human-readable reports shall include an executive summary, scope, model state, key findings, highest-priority actions, engineering tables and appendices for evidence and deterministic identifiers.

Machine exports shall use documented JSON, GeoJSON, Arrow or Parquet as appropriate. CSV shall remain available for accessible tables. Reports shall not require proprietary software to open.

Different stakeholder views shall reference the same canonical objects and findings.

## 9. Programme dashboard

A machine-readable programme manifest shall control the public dashboard, README status sections and current-build indicators.

The manifest shall record build identity, status, validated commit, package version, suite counts, restore point, canonical and provisional capabilities, open gates, latest Quantum Spawn entry and next bounded step.

Completion percentage shall be derived from explicitly weighted programme stages, not manually chosen optimism. Historical, active, blocked and queued work shall be visually distinct.

The dashboard shall explain that green regression tests prove reproducibility of implemented scope; they do not prove total product completion or project-specific compliance.

## 10. Quality gates

Each material tranche shall follow:

```text
restore point
bounded implementation
focused tests
full declared validation
clean-wheel verification
public or interface contract checks where relevant
Quantum Spawn checkpoint
```

Browser work shall include Playwright tests, accessibility automation and deterministic fixtures. Schemas require round trips; scale work requires performance budgets.

No visual change may weaken engineering authority, and no backend capability may be called complete until a user can understand its status and limitation.

## 11. Definition of interface success

The interface succeeds when a new competent user can open a project, understand its hierarchy, find the most important problems, inspect the responsible geometry and evidence, distinguish facts from assumptions and export a reproducible package without learning the repository internals.

The governing presentation principle is:

**Make the engineering mind-blowing through clarity, traceability and usefulness, not through visual spectacle or duplicated calculation.**
