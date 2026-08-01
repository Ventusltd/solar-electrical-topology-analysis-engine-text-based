# Trueself

**Title:** TS-003 Exact Generic Equipment Contract Authority

**File:** `202608010226-ts-003-exact-equipment-contract-authority.md`

**Timestamp:** 2026-08-01 02:26 Europe/London

**Version:** 1.0

**Status:** Verified execution checkpoint

**Authority:** Repository implementation, GitHub Actions run `30677811304` and validation artefact `8811110022`

**Supersedes In Part:**
- `202608010225-ts-003-generic-reference-equipment-contract-pass.md`

The earlier file remains authoritative for TS-003 purpose, scope, data model, unresolved evidence and bounded failure history. This file supersedes its equipment-contract hash and final validation evidence because exact decimal serialisation was added afterwards.

**Dependencies:**
- `202608010225-ts-003-generic-reference-equipment-contract-pass.md`
- `202608010154-ts-002-programme-truth-and-capsule-integrity.md`
- `../quantum-spawn/202608010151-bounded-observation-and-truncation-law.md`

**Current Build:** Build 025.5D1

**Completed Goal:** TS-003 — Freeze the generic reference equipment contract

**Restore Point:** `restore/2026-08-01-0210-pre-ts-003-equipment-contract`

---

## 1. Reason for this successor capsule

The first corrected TS-003 validation was green, but its clean-wheel summary serialised the mathematically exact 475.2 kWp reference value using a binary-float representation:

```text
475.20000000000005
```

The numerical result was within the validated tolerance and no engineering calculation was wrong.

However, the reference equipment contract is a programme-truth object. Its deterministic payload and JSON should preserve the declared decimal values exactly rather than expose a binary representation artefact.

The fix therefore changed only the reference-fixture arithmetic implementation to use decimal-derived values before JSON serialisation.

## 2. Exact values now bound

The installed package now serialises exactly:

```text
string rated power                 19.8 kWp
DC nameplate power                475.2 kWp
inverter apparent power           352.0 kVA
DC-to-AC nameplate ratio            1.35
```

The string count, module count and physical input count remain:

```text
modules per string                  30
strings                              24
modules                             720
physical DC input pairs              24
```

## 3. Final deterministic equipment-contract hash

```text
sha256:1482dfd06dda6b5a1765676bf1c98fe6eee78bc7858b378fe8b7acaa00ff32de
```

This hash supersedes the pre-normalisation hash recorded in the preceding TS-003 capsule.

## 4. Unresolved equipment evidence retained

The final contract still reports:

```text
missing evidence items              47
internal DC topology                unknown
reverse-current blocking            unknown
PCE backfeed current                unresolved
MPPT count and mapping              unresolved
connector family and compatibility unresolved
factory-lead lengths                unresolved
module electrical values            unresolved except 660 Wp and bifacial technology
module dimensions                    unresolved
installation class                   unresolved
```

The two referenced conductor resistance sources remain candidate-grade.

No source was promoted and no equipment fact was invented.

## 5. Exact-arithmetic implementation

Files added or changed after the earlier TS-003 pass capsule:

```text
src/solar_topology/equipment_profiles.py
tests/test_equipment_profile_exact_arithmetic.py
```

Commits:

```text
26d3b0e  fix: preserve exact reference block arithmetic
eb75120  test: bind exact equipment fixture arithmetic
```

The new test requires the canonical equipment JSON to contain:

```text
"dc_nameplate_power_kwp":475.2
```

and rejects:

```text
475.20000000000005
```

## 6. Final validation execution

Validation-only draft PR:

```text
PR 27
head branch: agent/ts-003-exact-arithmetic-validation
head commit: ceac1b059aceeb94060fdbafa9cb4646a19658bd
base main: d0c377b53e5d60b8c716c97c112c7996ba102f8f
merge-test SHA: 1ec15a12be9ca06c7419bc084457964e753fe0bf
```

GitHub Actions:

```text
run id: 30677811304
workflow result: PASS
```

Validation artefact:

```text
artefact id: 8811110022
artefact digest: sha256:89f8d1ce222d62129b95f4731eb6aa84a1fbc28100fc5bbb807f4142e3cbffb6
```

## 7. Final validation result

```text
capsule-link integrity                PASS
programme-state drift                 PASS
Python                                296 / 296
V8 model                               13 / 13
V8 authority reconciliation             6 / 6
V9 deterministic engine                10 / 10
V10 JavaScript                         13 / 13
Clean installed wheel                 PASS
```

Both workflow jobs passed.

## 8. Existing engineering authority unchanged

The established geometry and conductor comparison remains:

```text
comparison hash:
sha256:413aa93c98d1b9fd5f9ffee4f577cfe29a6e74f48bd927a3ebe7f541545d6366

sequential total conductor     2513.328 m
leapfrog total conductor       2560.128 m
field-installed reduction       798.288 m
factory-fitted increase          845.088 m
total conductor change           +46.800 m
```

No historical geometry, topology, assignment, routing or calculation receipt changed.

## 9. Goal status

```text
TS-003  COMPLETE
```

## 10. Next single goal

```text
TS-004 — Add the complete inverter-block aggregate and receipt
```

TS-004 shall bind the exact generic equipment contract to the existing geometry, topology, assignment and routing authorities through one new explicitly requested aggregate receipt.

It shall not add standards, EMC, lightning or browser calculations.
