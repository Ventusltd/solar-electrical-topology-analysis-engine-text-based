# Quantum Spawn Progress Log

**Title:** Build 025.5D1 Qualification Assessment Serialisation

**File:** `202607312309-build-025-5-d1-assessment-serialisation.md`

**Timestamp:** 2026-07-31 23:09 Europe/London

**Version:** 1.0

**Status:** Verified checkpoint

**Authority:** GitHub Actions run 30668896818 and artifact 8808037377

**Current Build:** Build 025.5D1 — Resistance Source Qualification Gate

## Scope completed

This step added deterministic serialisation for `ResistanceSourceAssessment` only. It did not alter source qualification decisions, resistance values, electrical calculations, topology hashes, public API classification or calculation receipts.

New functions in `src/solar_topology/resistance_qualification.py`:

```text
resistance_source_assessment_payload
resistance_source_assessment_json
resistance_source_assessment_hash
```

## Deterministic payload

The serialised assessment binds exactly:

```text
schema_version
record_hash
status
reasons
```

Runtime timestamps, actors, workflow identifiers and repository commits are excluded from the engineering payload.

Canonical JSON uses:

```text
sorted keys
compact separators
UTF-8
no runtime metadata
```

The content hash is:

```text
sha256:<64 hexadecimal characters>
```

A change to the qualification schema, source record hash, status or reason codes changes the assessment hash.

## Test coverage

Focused tests verify:

- exact payload shape;
- exact canonical JSON output;
- repeated hash determinism;
- hash sensitivity to every bound field;
- rejection of invalid serialisation input types;
- valid serialisation of a rejected assessment whose source record hash is absent.

## Validation result

Both GitHub Actions jobs passed:

```text
validate                           PASS
Clean installed wheel authority    PASS
```

Artifact `8808037377` records:

```text
Python                             274 passed / 0 failed
V8 model                           13/13
V8 authority reconciliation         6/6
V9 deterministic engine            10/10
V10 JavaScript                     13/13
Clean installed wheel              PASS
```

The wheel includes the updated `solar_topology/resistance_qualification.py` module.

## Commits

```text
b8f11a7  feat: serialise resistance source assessments deterministically
e8b7be0  test: bind resistance qualification assessment serialisation
```

## Repository hygiene

Restore point:

```text
restore/2026-07-31-2302-pre-build-025-5-d1-serialisation
```

Validation PR 16 contained one effective branch-only Markdown marker. It was closed without merge after the green result. The marker is not part of `main`.

## Working rule retained

Continue in bounded steps:

1. one material change;
2. one validation result;
3. one Quantum Spawn progress entry;
4. no next material step until the current evidence is understood.

## Next single step

Expose the three serialisation functions through the supported `solar_topology` package API and classify them explicitly as provisional. Extend the clean-wheel consumer probe to call the top-level payload, JSON and hash functions and confirm that the same assessment produces the same hash outside the repository checkout.

Do not integrate qualification assessments into calculation receipts in that step. Receipt integration remains a later, separately restored and validated change.
