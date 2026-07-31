# Quantum Spawn

**Title:** Employer Requirements Part 1 — Mission, Public Value and Global Scale

**File:** `202607312336-employer-requirements-part-1-mission-public-value.md`

**Timestamp:** 2026-07-31 23:36 Europe/London

**Version:** 1.0

**Status:** Canonical employer requirement

**Authority:** Product Owner and Engineering Design Authority

**Supersedes:** None

**Superseded By:** None

**Dependencies:**
- `202607311609-mission-and-philosophy.md`
- `202607311615-system-architecture.md`
- `202607311624-array-engine.md`
- `202607312309-build-025-5-d1-assessment-serialisation.md`

**Current Build Relevance:** Build 025.5 and all later builds

---

## 1. Purpose

This module records the employer’s product mission, public-interest obligation, scale requirement and intended user outcomes for the Solar Electrical Topology Analysis Engine. It converts the strategic brief into canonical requirements that future engineers, contributors and AI development agents must preserve.

The engine is not being created as another private calculator, limited demonstration or single-project design spreadsheet. It is intended to become an open engineering infrastructure layer for the global solar energy transition: free to inspect, free to run, free to adapt and capable of diagnosing photovoltaic systems from commercial-scale arrays above 30 kWp through the largest utility plants.

## 2. Public mission

The platform shall provide a credible engineering route from physical site reality to reproducible electrical diagnosis. A user shall be able to understand what exists, what is connected, how conductors are routed, which calculations are supported, where evidence is incomplete and what action is required next.

The public mission is broader than producing numerical answers. The software shall reduce dependence on undocumented assumptions, opaque vendor tools, inaccessible consultants and disconnected spreadsheets. It shall make good engineering method visible and teachable while preserving the distinction between calculation assistance, engineering judgement, standards assessment and formal design approval.

The platform shall remain useful to engineers, asset owners, investors, developers, EPC contractors, operations teams, researchers, educators, insurers, public authorities and technically competent community users. No group shall require a proprietary data subscription merely to understand its own installation.

## 3. Global scale context

IEA PVPS reported that cumulative global photovoltaic capacity approached 3 TW by the end of 2025. This installed base already contains millions of individual strings, enormous conductor quantities and a large diversity of module, inverter, connector, mounting, environmental and protection arrangements.

The employer sets 72 TWp by 2050 as the platform’s strategic design horizon. This is an internal scale target and product-planning assumption, not a claim that an external forecasting authority has guaranteed that exact deployment level. The software architecture must nevertheless be capable of serving a world in which solar becomes one of the dominant physical infrastructures of civilisation.

The engine must therefore avoid hidden limits derived from one reference table, one inverter, one country, one standard edition or one programming environment. The 24-string by 30-module fixture remains a permanent validation case, but it is not the product boundary.

## 4. Minimum addressable installation

The intended diagnostic scope begins at arrays above 30 kWp. This threshold includes schools, warehouses, farms, retail buildings, hospitals, public estates, industrial roofs, car parks, behind-the-meter installations and community energy systems, as well as ground-mounted plants.

A 30 kWp project and a 3 GWp project shall use the same engineering concepts and object hierarchy. Scale may change storage, rendering and aggregation methods, but it shall not require a different truth model. Every plant shall be composed from explicit modules, strings, array sections or tables, inverter inputs, MPPTs, inverters, power blocks and plant-level parents.

The engine shall support incomplete records because operational assets often lack clean design files. It must permit progressive reconstruction from drawings, schedules, photographs, measurements, exports and site observations while retaining uncertainty and provenance.

## 5. Required user outcomes

The final platform shall allow a user to establish an electrical hierarchy, locate physical objects, connect terminals, assign strings to real inverter inputs, define conductor routes, associate products and evidence, run supported calculations and receive deterministic diagnostic outputs.

The interface and reports shall answer five questions plainly:

1. What is wrong or potentially wrong?
2. Where is the condition located?
3. Why does it matter electrically, operationally or commercially?
4. How certain is the conclusion?
5. What evidence, measurement or engineering action is required next?

The platform shall identify missing geometry, impossible assignments, duplicate input occupation, open or branched strings, unsupported resistance values, incomplete equipment evidence, high voltage drop, elevated loss, unusual route separation and other conditions supported by the current calculation authority.

It shall never convert missing evidence into a confident clean bill of health.

## 6. Free and open requirement

The core engine, schemas, reference interfaces, test fixtures and diagnostic methods shall remain available under an open-source licence compatible with broad public and commercial use. A contributor must be able to clone the repository, build the package, run the tests and execute the reference workflows without paying for a mandatory cloud service.

The core workflow shall operate locally and offline. Optional hosted services may improve convenience, but no authoritative calculation shall depend exclusively on a private endpoint. Project data shall be exportable in documented formats. Users shall not be trapped by inaccessible databases, undocumented binary files or vendor-specific identifiers.

Free does not mean ungoverned. Contributions must satisfy evidence, testing, security, licensing and architectural requirements before becoming authoritative.

## 7. Trust and safety boundary

The engine shall support competent engineering judgement but shall not falsely represent itself as a project-specific design approval, construction release, standards certificate, protection study, warranty or professional indemnity product.

Every output shall identify the model version, input evidence, calculation status, limitations and missing dependencies. Historical and provisional tools shall remain visibly separated from canonical authority. A visually impressive page must never imply that unsupported engineering has been completed.

## 8. Success definition

The mission succeeds when a competent user can take a previously opaque PV installation, reconstruct its electrical and physical model, reproduce the calculations, trace every significant conclusion to geometry and evidence, identify unresolved risks and share the complete diagnostic package with another engineer without proprietary software.

The project shall be judged by public engineering usefulness, determinism, transparency, scalability, legibility and the quality of decisions it enables. Feature count alone is not success.

The governing ambition is therefore:

**Build the free, open and geometry-authoritative diagnostic infrastructure required to understand, improve and protect the world’s solar PV assets above 30 kWp, at a scale compatible with a 72 TWp energy-transition horizon.**
