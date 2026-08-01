# Trueself

**Title:** TS-003 Exact-Arithmetic Equipment Contract Final Pass

**File:** `202608010228-ts-003-exact-arithmetic-final-pass.md`

**Timestamp:** 2026-08-01 02:28 Europe/London

**Version:** 1.0

**Status:** Verified final TS-003 execution checkpoint

**Authority:** Repository implementation, GitHub Actions run `30677811304` and validation artefact `8811110022`

**Supersedes:** `202608010225-ts-003-generic-reference-equipment-contract-pass.md` for the final validated commit, equipment-contract hash and test count only

**Preserves:** The earlier checkpoint's record of the first bounded validation failure and correction history

**Dependencies:**
- `202608010104-complete-352-kva-inverter-block-plan.md`
- `202608010117-civilisational-consciousness-and-amnesia-covenant.md`
- `202608010154-ts-002-programme-truth-and-capsule-integrity.md`
- `202608010222-build-026-standards-correction-register.md`
- `202608010225-ts-003-generic-reference-equipment-contract-pass.md`
- `../quantum-spawn/202608010151-bounded-observation-and-truncation-law.md`

**Current Build:** Build 025.5D1

**Completed Goal:** TS-003 — Freeze the generic reference equipment contract

**Restore Point:** `restore/2026-08-01-0210-pre-ts-003-equipment-contract`

---

## 1. Reason for this successor checkpoint

The corrected TS-003 validation passed, but the clean-wheel summary exposed binary floating-point presentation of the mathematically exact 475.2 kWp reference value as:

```text
475.20000000000005
```

The underlying product boundary was not wrong, but a deterministic public engineering contract should not emit avoidable binary-float artefacts for exact nameplate arithmetic.

The equipment contract arithmetic was therefore changed to use decimal intermediates before returning stable scalar values.

This successor checkpoint records the final validated state rather than silently altering the earlier evidence record.

## 2. Exact-arithmetic correction

Commits:

```text
26d3b0e  fix: preserve exact reference block arithmetic
eb75120  test: bind exact equipment fixture arithmetic
```

The following values now serialise exactly in the equipment contract payload and canonical JSON:

```text
string rated power        19.8 kWp
DC nameplate power        475.2 kWp
DC/AC nameplate ratio     1.35
```

The change is bounded to reference-equipment arithmetic and its tests.

It does not change:

- module placement;
- topology;
- string assignment;
- routing;
- resistance;
- voltage drop;
- loss;
- uncertainty;
- historical geometry, topology or calculation receipt hashes.

## 3. Final validation execution

Validation-only draft PR:

```text
PR 27
head branch: agent/ts-003-exact-arithmetic-validation
head commit: ceac1b059aceeb94060fdbafa9cb4646a19658bd
base main: d0c377b53e5d60b8c716c97c112c7996ba102f8f
```

GitHub Actions:

```text
run id: 30677811304
workflow: V10 Engine Validation
workflow result: PASS
```

Validation artefact:

```text
artefact id: 8811110022
artefact name: v10-validation-1ec15a12be9ca06c7419bc084457964e753fe0bf
artefact digest: sha256:89f8d1ce222d62129b95f4731eb6aa84a1fbc28100fc5bbb807f4142e3cbffb6
merge-test SHA: 1ec15a12be9ca06c7419bc084457964e753fe0bf
```

## 4. Final validation result

```text
Python                             296 passed / 0 failed
V8 model                           13/13
V8 authority reconciliation         6/6
V9 deterministic engine            10/10
V10 JavaScript                     13/13
Clean installed wheel              PASS
Capsule-link integrity             PASS
Programme-state drift              PASS
```

Both workflow jobs passed:

```text
validate                           PASS
Clean installed wheel authority    PASS
```

## 5. Final installed equipment contract

```text
contract id:
generic_352kva_475_2kwp_reference_equipment

revision:
2026-08-01.1

contract hash:
sha256:1482dfd06dda6b5a1765676bf1c98fe6eee78bc7858b378fe8b7acaa00ff32de

module count:
720

strings:
24

modules per string:
30

DC nameplate power:
475.2 kWp

inverter apparent power:
352 kVA

physical DC input pairs:
24

missing evidence items:
47
```

The change from the earlier contract hash is expected because canonical payload content changed from a binary-float artefact to the exact public value.

## 6. Evidence states retained

The following remain unresolved:

```text
MPPT mapping
MPPT count
internal DC topology
reverse-current blocking
PCE backfeed current
module electrical values other than rated power
module dimensions
connector family and compatibility
connector resistance and ratings
factory-lead lengths
installation class
maximum DC voltage
maximum DC input-power evidence
```

The 4 mm² and 6 mm² resistance records remain candidate sources.

No source was promoted.

## 7. Existing engineering comparison retained

```text
comparison hash:
sha256:413aa93c98d1b9fd5f9ffee4f577cfe29a6e74f48bd927a3ebe7f541545d6366

sequential total conductor     2513.328 m
leapfrog total conductor       2560.128 m
field-installed reduction       798.288 m
factory-fitted increase          845.088 m
total conductor change           +46.800 m
```

## 8. Goal status

```text
TS-003  COMPLETE
```

## 9. Next single goal

```text
TS-004 — Add the complete inverter-block aggregate and receipt
```

TS-004 shall bind the generic equipment contract to existing geometry, topology, assignment and routing receipts through a new explicit aggregate.

It shall not add standards, EMC, lightning or browser calculations.
