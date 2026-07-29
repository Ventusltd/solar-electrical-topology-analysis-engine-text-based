# Ventus DC String Engine — Intelligence Log

This file is the permanent text log for intelligence that may affect the Ventus DC String Engine.

It records findings. It does not itself authorise formula, schema or standards changes.

## Entry template

```text
Date:
Scan ID:
Source type:
Source title:
Source location:
Source version or date:
Area affected:
Finding:
Evidence status:
Potential computation impact:
Validation required:
Licence or quotation restriction:
Decision: accepted | rejected | uncertain | duplicate | measurement required
Decision owner:
Linked issue or commit:
Next review date:
```

## 2026-07-29 — V10 preparation baseline

```text
Date: 2026-07-29
Scan ID: V10-PREP-0001
Source type: repository lineage and owner-provided engineering context
Source title: V6, V7, V8 and V9 workbenches; federation-map operating discipline; supplied manufacturer and standards material
Source location: this repository, the GlobalGrid2050 federation-map repository and owner-provided source documents
Source version or date: current at preparation date
Area affected: complete V10 architecture
Finding: the existing work is no longer one calculator. It contains stable, experimental and topology-specific branches that must be inventoried before integration. V10 should use graph-based traceability, evidence status, validation gates and monthly intelligence reports rather than merge all formulas into one opaque page.
Evidence status: repository-derived engineering requirement
Potential computation impact: architecture, provenance, testing, release governance and all later calculation domains
Validation required: complete V6–V9 inventory, duplicate-formula comparison, independently calculated reference cases and regression suite
Licence or quotation restriction: do not reproduce licensed IEC text; store only clause references, engineering interpretation and user-owned derived calculations
Decision: accepted for preparation
Decision owner: Vikram Kumar
Linked issue or commit: V10 preparation branch
Next review date: on receipt of Claude deep-research output
```

```text
Date: 2026-07-29
Scan ID: V10-PREP-0002
Source type: manufacturer connector data
Source title: Stäubli Original MC4-Evo 2 cable coupler data
Source version or date: 2025 catalogue material supplied by owner
Area affected: connector objects, current rating, contact resistance, cable range and inverter interface
Finding: connector family, conductor size, cable outer diameter, field or panel interface and assembly status must be explicit objects. A generic connector-count assumption is insufficient. Declared plug-connector contact resistance is a component input, not proof of installed-joint resistance.
Evidence status: manufacturer-declared input requiring exact part-number and installation verification
Potential computation impact: complete-series resistance, voltage drop, loss, thermal risk, compatibility checks and uncertainty reporting
Validation required: exact installed part numbers, mating pairs, tooling, conductor class, cable diameter and field workmanship data
Licence or quotation restriction: summarise data and cite source; do not republish catalogue pages
Decision: accepted as a V10 object-model requirement
Decision owner: Vikram Kumar
Linked issue or commit: V10 preparation branch
Next review date: during connector schema design
```

```text
Date: 2026-07-29
Scan ID: V10-PREP-0003
Source type: inverter manufacturer data
Source title: Sungrow SG350HX datasheet
Source version or date: Version 19, 2023
Area affected: MPPT boundaries, connector limits, current limits, surge protection and unknown internal topology
Finding: the public datasheet provides input counts, current limits, DC voltage range, connector family and DC Type II SPD declaration, but it does not fully disclose the transient-frequency DC input network or prove how all inputs couple at relevant frequencies. V10 must therefore support declared topology, unknown-topology and bounding-case modes.
Evidence status: manufacturer-declared ratings plus unresolved internal-model gap
Potential computation impact: reverse current, backfeed, capacitance aggregation, surge sharing, common-bus coupling and insulation-monitoring boundary
Validation required: OEM clarification, circuit evidence or measurement; until then show alternative cases
Licence or quotation restriction: summarise manufacturer data and retain source reference
Decision: accepted
Decision owner: Vikram Kumar
Linked issue or commit: V10 preparation branch
Next review date: during inverter topology schema design
```

```text
Date: 2026-07-29
Scan ID: V10-PREP-0004
Source type: engineering governance framework
Source title: Employer's Competence Requirements
Source version or date: July 2026 living document
Area affected: evidence output and acceptance gates
Finding: V10 outputs should map directly to evidence requirements for cable sizing, voltage drop and loss, connector compatibility, DC string electrical behaviour, transient assessment, assumptions control, independent review and configuration management.
Evidence status: owner-authored engineering governance requirement
Potential computation impact: report structure, missing-evidence findings, review workflow and change control
Validation required: create a requirements-to-output matrix before V10 release
Licence or quotation restriction: owner-controlled material
Decision: accepted
Decision owner: Vikram Kumar
Linked issue or commit: V10 preparation branch
Next review date: during report schema design
```
