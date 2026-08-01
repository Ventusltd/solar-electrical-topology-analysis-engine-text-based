# Trueself

**Title:** TS-001 Resistance Assessment Public Contract Passed

**File:** `202608010129-ts-001-resistance-assessment-api-pass.md`

**Timestamp:** 2026-08-01 01:29 Europe/London

**Version:** 1.0

**Status:** Verified execution checkpoint

**Authority:** Repository implementation, GitHub Actions run `30675585601` and validation artefact `8810319603`

**Supersedes:** None

**Dependencies:**
- `202608010104-complete-352-kva-inverter-block-plan.md`
- `202608010117-civilisational-consciousness-and-amnesia-covenant.md`
- `../quantum-spawn/202608010120-amnesia-resilience-and-continuity-law.md`
- `../quantum-spawn/202607312309-build-025-5-d1-assessment-serialisation.md`

**Current Build:** Build 025.5D1

**Completed Goal:** TS-001 — Close the current resistance public contract

**Restore Point:** `restore/2026-08-01-0124-pre-ts-001-resistance-api`

---

## 1. Goal attempted

Expose the existing deterministic resistance-source assessment serialisation functions through the supported top-level `solar_topology` package API, classify them explicitly as provisional and prove identical payload, canonical JSON and hash behaviour from a clean installed wheel outside the repository checkout.

The bounded goal prohibited:

- resistance-value changes;
- source promotion;
- electrical-calculation changes;
- calculation-receipt integration;
- topology or geometry changes;
- removal of compatibility paths or historical workbenches.

## 2. Build completed

The following existing functions are now available directly from `solar_topology`:

```text
resistance_source_assessment_payload
resistance_source_assessment_json
resistance_source_assessment_hash
```

All three are explicitly classified as:

```text
ApiStatus.PROVISIONAL
```

The top-level functions are the same Python objects as the authority functions in:

```text
solar_topology.resistance_qualification
```

No duplicate implementation was created.

## 3. Files changed

```text
src/solar_topology/__init__.py
src/solar_topology/public_api.py
tests/test_resistance_qualification_public_api.py
scripts/validate_clean_wheel.py
```

Implementation commits on `main`:

```text
20bff93  api: expose resistance assessment serialisation
ff54ad7  api: classify assessment serialisation provisional
17e49ad  test: bind assessment serialisation public API
a239aae  test: prove assessment serialisation from clean wheel
```

## 4. Public authority classification

The following public names remain provisional:

```text
RESISTANCE_QUALIFICATION_SCHEMA_VERSION
ResistanceSourceAssessment
ResistanceSourceStatus
assess_resistance_source
resistance_source_assessment_payload
resistance_source_assessment_json
resistance_source_assessment_hash
```

This step closes the supported consumer contract without promoting qualification assessment into canonical calculation authority.

## 5. Focused contract proved

For both current generic conductor records, the test and clean-wheel probe reconstruct the exact expected assessment payload:

```text
schema_version
record_hash
status
reasons
```

They independently reconstruct canonical JSON using:

```text
sort_keys = true
compact separators
UTF-8
no runtime metadata
```

They independently reconstruct the SHA-256 assessment hash and require exact equality with both:

- the top-level package functions;
- the packaged authority-module functions.

The public API tests also prove:

- import identity;
- membership in `solar_topology.__all__`;
- explicit provisional classification;
- unchanged candidate status;
- unchanged source reason codes.

## 6. Validation execution

Validation-only draft PR:

```text
PR 18
head branch: agent/ts-001-resistance-api-validation
head commit: 9cf1680cded4a4f32fb77f352ba2db3e3680eea1
base main: a239aae2de32daf19bbb00c4bda7095ab7780623
```

The branch differs from `main` only by a non-mergeable marker under `tests/` used to trigger the pull-request workflow.

GitHub Actions:

```text
run id: 30675585601
workflow: V10 Engine Validation
workflow result: PASS
```

Validation artefact:

```text
artefact id: 8810319603
artefact name: v10-validation-58cc79934684dd7753371ea8cd247825ebd0914e
artefact digest: sha256:b459f03fed4b10870dc3b42b587f682894f285d29027709468eb96b4a98a0003
merge-test SHA: 58cc79934684dd7753371ea8cd247825ebd0914e
```

## 7. Full validation result

```text
Python                             275 passed / 0 failed
V8 model                           13/13
V8 authority reconciliation         6/6
V9 deterministic engine            10/10
V10 JavaScript                     13/13
Clean installed wheel              PASS
```

Both workflow jobs passed:

```text
validate                           PASS
Clean installed wheel authority    PASS
```

## 8. Clean-wheel authority result

The clean wheel was built, installed into a fresh virtual environment and executed outside the repository checkout.

It reported:

```text
distribution version     0.4.0
authority status         canonical_candidate
migration stage          build-025.5-package-authority
comparison hash          sha256:413aa93c98d1b9fd5f9ffee4f577cfe29a6e74f48bd927a3ebe7f541545d6366
```

The established 24-by-30 comparison remained unchanged:

```text
sequential total conductor     2513.328 m
leapfrog total conductor       2560.128 m
field-installed reduction       798.288 m
factory-fitted increase          845.088 m
total conductor change           +46.800 m
```

## 9. Exact assessment outputs

### External field conductor record

```text
product id:
external_string_6mm2_metal_coated_class5

source record hash:
sha256:55f92314523145ee56d937e5e12935b9b1f1311582a1e3e299de06588096dd2b

assessment hash:
sha256:d1138f679b0b28c9759b337f010b81487c2da9906d300a92f4dedcd7f800a9dd

status:
candidate

reasons:
SOURCE_REVISION_PLACEHOLDER
VERIFICATION_NOT_VERIFIED
```

### Factory module-lead record

```text
product id:
factory_module_lead_4mm2_metal_coated_class5

source record hash:
sha256:61b55e8afdb0c490575c01dc9340a87bcfa9283d945586aaad90f48c128586c8

assessment hash:
sha256:7396da4829cec4d33f6622a46d637f8e7edce19948a87305caf7638b525f8ccd

status:
candidate

reasons:
SOURCE_REVISION_PLACEHOLDER
VERIFICATION_NOT_VERIFIED
```

No source was promoted.

## 10. Known limitations retained

The two current generic resistance records remain candidate-grade because their exact edition and revision-controlled source locators are not yet encoded and their verification state is not `verified`.

This passing result proves deterministic source-assessment publication through the installed package.

It does not prove:

- the numerical standard source has been fully qualified;
- a standards conclusion;
- calculation-receipt integration;
- protection, EMC or lightning authority;
- completion of the inverter-block product.

## 11. Goal status

```text
ER-01   COMPLETE
TS-001  COMPLETE
```

The completed step is small but important: internal deterministic qualification assessment is now a supported, externally reproducible and visibly provisional package contract.

## 12. Next single goal

```text
TS-002 — Establish one programme truth manifest
```

TS-002 shall create one versioned machine-readable programme-state authority containing the current build, validated commit, package version, suite results, restore point, complete reference inverter-block fixture, capability classifications, active gate, next single goal and known limitations.

It shall generate or validate public status statements and eliminate the stale Build 024, 176-test and manually maintained progress claims.

TS-002 shall not change engineering calculations, equipment evidence or receipt semantics.
