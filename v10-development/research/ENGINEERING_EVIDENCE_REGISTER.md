# Engineering Evidence and Provenance Register

## Purpose

This register defines how the V10 engine distinguishes first-principles engineering, independently developed methods, measurements, public observations, manufacturer data, standards constraints and project-specific requirements.

The engine is not an implementation of any one standard. Its engineering models remain independently defined. Standards cartridges describe recognised constraints, recommendations and evidence requirements applicable to those models.

## Evidence hierarchy

### E0 — Physical law and mathematics

Examples:

- circuit theory;
- field theory;
- transmission-line equations;
- heat transfer;
- geometry;
- statistics and uncertainty propagation.

These are not attributed to a project or standards document. The implementation must still identify its formula, assumptions and numerical method.

### E1 — Ventus independently developed engineering method

Examples:

- physical DC object model;
- ordered conductor topology;
- sequential and leapfrog geometry algorithms;
- complete conductor schedule;
- distributed string-circuit model;
- loss-allocation method;
- engineering report architecture.

The record must identify author, implementation version, validation evidence and any earlier internal artefact from which the method was recovered.

### E2 — Direct measurement or site observation

Examples:

- measured lead length;
- measured route length;
- field resistance;
- thermal image;
- observed tray arrangement;
- site visit from authorised access or lawful public observation;
- photographs taken by the contributor.

The record should identify date, method, accuracy, observer and access/provenance status.

### E3 — Publicly observable or publicly declared fact

Examples:

- module physical dimensions from a public datasheet;
- inverter input count and MPPT architecture from manufacturer literature;
- publicly visible row arrangement;
- planning-layout geometry;
- aerially observable plant arrangement;
- equipment ratings published by the manufacturer.

Public facts may be used to construct a new engineering model. Manufacturer artwork, protected imagery and third-party drawings must not be reproduced merely because the facts shown by them are public.

### E4 — Manufacturer instruction or product evidence

Examples:

- maximum system voltage;
- connector compatibility;
- bend radius;
- torque;
- current rating;
- inverter backfeed limit;
- MPPT voltage window;
- module maximum series-fuse rating.

Store the declared value and source reference. Do not reproduce proprietary manuals beyond what is necessary and lawfully permitted.

### E5 — Standards constraint or recognised practice

Examples:

- IEC 62548 rule;
- IEC TS 62738 utility-scale exception;
- IEC 63027 arc-detection requirement;
- IEC 63112 earth-fault protection principle;
- IEC 61643-32 SPD-selection method.

Store:

- publication identity;
- edition;
- clause reference;
- paraphrased engineering meaning;
- normative strength where confirmed;
- required input;
- engine test;
- exception route;
- validity boundary.

Do not store copied paragraphs, protected tables, protected figures or reconstructed substitutes for the publication.

### E6 — Project-specific contractual or confidential requirement

Examples:

- Employer's Requirements;
- EPC design basis;
- cable schedule;
- confidential inverter allocation;
- construction drawing;
- site test data supplied under contractual restrictions.

These inputs must remain access-controlled. Generic examples derived from them must be independently redrawn and stripped of confidential identifiers, dimensions and combinations unless publication rights are confirmed.

## Provenance codes

| Code | Meaning |
|---|---|
| `physics` | physical law or mathematical derivation |
| `ventus_original` | independently developed Ventus method or artefact |
| `user_created` | geometry, assumption or model created by the current user |
| `field_measured` | direct measurement |
| `site_observed` | direct visual observation |
| `public_observation` | fact derived from lawful public observation |
| `manufacturer_declared` | public or licensed manufacturer data |
| `standard_referenced` | paraphrased standards constraint with clause reference |
| `project_supplied` | project input supplied for the calculation |
| `confidential_project` | access-controlled project information |
| `generic_example` | invented illustrative arrangement |
| `assumed` | engineering assumption requiring sensitivity or confirmation |
| `derived` | computed from identified upstream inputs |

## Geometry provenance

Every layout object should state one of the following:

- `generic_example` — invented to demonstrate a topology or calculation;
- `user_created` — drawn from the user's own design decision;
- `field_measured` — based on direct measurement;
- `site_observed` — based on lawful site observation;
- `public_observation` — reconstructed from publicly observable features;
- `manufacturer_declared` — based on public product dimensions or terminal arrangement;
- `project_supplied` — supplied for a specific project;
- `confidential_project` — derived from restricted project material.

A layout can combine sources. Provenance therefore belongs at object and attribute level, not only at whole-project level.

## Copyright and source-use control

The following are acceptable engine inputs or outputs when independently expressed:

- physical laws;
- engineering facts;
- dimensions and ratings;
- observed physical arrangements;
- original vector drawings;
- original topology models;
- original algorithms;
- original calculations;
- original comparisons of alternative layouts;
- clause references and paraphrased standards implications.

The following must not be published without confirmed rights or permission:

- copied standards text beyond legally justified limited quotation;
- standards figures and tables;
- manufacturer artwork copied as engine diagrams;
- EPC CAD drawings;
- confidential construction layouts;
- third-party aerial imagery or screenshots outside licence terms;
- a reconstruction so complete that it substitutes for a copyrighted standard or manual.

## Public-site reconstruction rule

A new layout may be created from public facts, public observations, planning information, public product specifications, lawful field observation and the engineer's own design reasoning.

The resulting model must:

- use original drawing geometry and styling;
- identify observed versus assumed dimensions;
- avoid embedding third-party imagery unless licensed;
- avoid claiming survey-grade accuracy where none exists;
- avoid publishing restricted project information learned through a confidential relationship;
- record the engineering purpose, such as loss comparison, loop-area comparison, route study or protection study.

## Minimum evidence record

Each important input or rule should support:

```text
id
value or statement
units where applicable
provenance code
source title or artefact
source version or date
source locator
licence or confidentiality status
accuracy or uncertainty
entered by
reviewed by
validation state
notes
```

## Calculation provenance

Each result must link to:

- source objects;
- input values;
- formula or method identifier;
- kernel version;
- assumptions;
- unit conversions;
- numerical tolerance;
- standards cartridges applied;
- warnings and exceptions;
- validation evidence.

## Standards notice

IEC and other standards publications remain the copyright property of their respective owners. Clause references in this repository are provided for engineering traceability. Users must obtain authorised copies of the normative publications where required. Repository documents paraphrase engineering implications and do not reproduce or replace the publications.

## Engineering principle

A standard may confirm, constrain or require evidence for an engineering phenomenon. It does not acquire ownership of independently developed physics, topology, algorithms, measurements, layouts or calculations merely because it addresses the same subject.
