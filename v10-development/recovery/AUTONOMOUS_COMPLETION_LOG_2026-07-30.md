# V10 Autonomous Completion Log — Diagnostics and Study Control

Date: 2026-07-30  
Repository rule: direct commits to `main`; immutable commit recovery points; no build branches.

## Recovery and bandwidth position

Pre-batch validated recovery commit: `0d2ac903163bf6b65b211bec0973ca078fd5eb04`.

The batch was allocated as one bounded architecture block rather than repeated small approvals. Earlier V6–V9 workbenches remain untouched. V10 Python remains the headless authority candidate.

## External review absorbed

The Claude review was treated as a partial and temporally stale external inspection. Its valid remaining criticism was adopted:

- diagnostics require stable codes, severities, subjects and fields;
- independent validation findings should accumulate;
- not checked must never be presented as passed;
- public output must omit internal and confidential details;
- acceptance thresholds must carry a declared source rather than being invented.

Its claims that main was empty, validation was limited to scalar JavaScript guards, and graph validation was absent were rejected against the current repository evidence.

## Build 014 — Unified diagnostics

File: `src/solar_topology/diagnostics.py`

Provides immutable deterministic diagnostics with:

- stable code;
- severity and category;
- subject and field;
- observed value and expected constraint;
- method and source references;
- remediation;
- separate public and internal detail;
- deterministic report JSON and hash;
- blocking state and counts.

## Build 015 — Explicit study coverage

The same diagnostics contract represents:

- not applicable;
- not checked;
- blocked;
- checked pass;
- checked warning;
- checked fail.

This removes the dangerous inference that an absent warning means an engineering study passed.

## Build 016 — Acceptance-criterion control

File: `src/solar_topology/study_applicability.py`

Acceptance criteria carry study kind, operator, threshold, unit, source and method. Calculation and compliance verdict remain separate. Voltage-drop and ampacity thresholds are not hard-coded without an evidence-bearing basis.

## Build 017 — Existing validator adapters

Files:

- `src/solar_topology/diagnostic_adapters.py`
- `src/solar_topology/diagnostic_bridges.py`

The adapters preserve all accumulated canonical-circuit and ordered-traversal findings and convert legacy throw-based boundaries into public-safe diagnostics without exposing stack traces or internal paths.

## Build 018 — Public-safe diagnostic payload

Public diagnostic JSON retains stable codes, severity, subject, remediation and study coverage while omitting `internal_detail`. Confidential source locations and raw exception text remain internal.

## Build 019 — Electrical study registry

File: `src/solar_topology/study_registry.py`

The initial controlled studies cover:

- complete-circuit resistance;
- voltage-drop acceptance;
- cold string Voc limit;
- differential loop geometry;
- conductor ampacity acceptance.

Each study declares required inputs, evidence roles, method and whether a sourced acceptance criterion is mandatory. Missing inputs, evidence or criteria produce a blocked coverage state rather than a fabricated result.

## Tests

Files include:

- `tests/test_diagnostics.py`
- `tests/test_diagnostic_adapters.py`
- `tests/test_study_applicability.py`
- `tests/test_diagnostics_and_studies.py`

Coverage includes deterministic ordering and hashing, duplicate rejection, accumulated findings, public/internal separation, explicit not-checked states, legacy exception sanitisation, missing-input blocking, missing-criterion blocking and pass/warning/fail distinctions.

## Architecture decision

`study_applicability.py` owns one study instance and its evidence-bearing criterion. `study_registry.py` owns the catalogue and fleet/project-wide coverage view. They are complementary rather than competing authorities.

`diagnostic_adapters.py` remains the small canonical-circuit adapter. `diagnostic_bridges.py` is the broader orchestration layer that combines circuit, traversal and legacy exception boundaries into one report.

## Remaining programme

The foundation and assurance chassis are now substantially complete. Remaining engineering work is domain cartridges and evidence datasets, not another architecture rewrite:

1. cold-Voc diagnostic cartridge using existing formula and sourced system maximum;
2. voltage-drop criterion evaluation against the uncertainty receipt;
3. ampacity input and evidence cartridge without invented limits;
4. loop inductance and transmission-line receipts downstream of geometry;
5. capacitance-to-earth and insulation-monitoring boundary models;
6. SPD electrical-distance study;
7. public Cleve Hill evidence manifest populated only from public sources;
8. final report assembly joining evidence, calculations, diagnostics and coverage.

## Validation rule

A build is not described as passed until the repository workflow writes a fresh validation receipt. Documentation commits after a validated source head do not alter the tested code but remain separately identifiable.
