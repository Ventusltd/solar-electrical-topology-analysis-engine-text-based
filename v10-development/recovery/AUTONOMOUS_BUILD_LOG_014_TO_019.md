# Autonomous Build Log 014–019

Date: 2026-07-30
Owner: Vikram Kumar, Ventus Ltd
Execution mode: direct to `main`; no feature branch or pull request
Pre-batch recovery commit: `0d2ac903163bf6b65b211bec0973ca078fd5eb04`

## Token and bandwidth stock take

The build was started with ample working context for a long bounded batch. The work was therefore grouped into one coherent diagnostic architecture rather than split into repeated approval cycles. Repository inspection, implementation, tests, API export and recovery documentation were all included in the same batch.

## External-review intake

Claude's review was retained as a useful but temporally stale review of an early JavaScript fragment. The following recommendations were adopted:

- stable diagnostic codes;
- severity and category;
- accumulating reports;
- subject and field localisation;
- public-safe and internal detail separation;
- explicit `not_checked`, `blocked`, `checked_pass`, `checked_warning` and `checked_fail` states;
- bridges from existing validation results;
- acceptance criteria that cannot exist without a declared source and method.

The recommendation to hard-code generic ampacity or voltage-drop limits was not adopted. V10 now requires an evidence-bearing acceptance criterion before a calculation can be treated as a verdict.

## Build 014 — Unified diagnostic record

Added `src/solar_topology/diagnostics.py`.

The immutable `Diagnostic` record carries:

- stable code;
- severity;
- category;
- message;
- subject identifier;
- field;
- observed value;
- expected constraint;
- method and source references;
- remediation;
- public-safe detail;
- internal detail.

## Build 015 — Accumulating diagnostic report

`DiagnosticReport` accumulates independently detectable findings, sorts them deterministically, rejects duplicate diagnostics, counts warnings and errors, exposes a blocking gate and produces canonical JSON and SHA-256 receipts.

## Build 016 — Study coverage state

`StudyCoverage` prevents silence from being interpreted as a pass. Every registered study can state:

- `not_applicable`;
- `not_checked`;
- `blocked`;
- `checked_pass`;
- `checked_warning`;
- `checked_fail`.

Blocked and not-checked studies require an explicit reason.

## Build 017 — Existing-validator bridge

Added `src/solar_topology/diagnostic_adapters.py`.

Canonical circuit validation issues are converted into the common diagnostic vocabulary without discarding their existing codes, subjects or warning/error distinction. Legacy exceptions can also be wrapped without publishing stack traces or private source paths.

## Build 018 — Public-safe diagnostic export

Public diagnostic payloads omit `internal_detail`. This permits internal NDA context to remain available to authorised engineering workflows while public reports expose only controlled messages and public-safe detail.

## Build 019 — Electrical study applicability and criteria

Added `src/solar_topology/study_applicability.py`.

Initial controlled studies include:

- cold string Voc;
- voltage drop;
- ampacity;
- loop geometry;
- transient response;
- capacitance to earth;
- insulation monitoring;
- SPD critical length;
- reverse current.

A study records applicability, required inputs, missing inputs and any acceptance criterion. An acceptance criterion must carry a source ID, method reference, operator, threshold and unit. Unit mismatch is rejected. A calculation can be executable without being verdict-capable.

## Tests

Added:

- `tests/test_diagnostics.py`;
- `tests/test_diagnostic_public_api.py`.

Coverage includes accumulation, deterministic ordering, duplicate rejection, blocking gates, public redaction, exception bridging, circuit-validation adaptation, explicit not-checked states, missing-input blocking, criterion provenance and unit-safe evaluation.

## Recovery and authority position

This batch does not rewrite V6–V9 and does not add project-confidential data. It establishes one common diagnostic chassis for later electrical cartridges and public reporting.

The exact pre-batch restore point is the immutable commit listed above. Later automated validation receipts are authoritative for executed test status; this log does not claim a pass until the workflow records one against the completed source head.
