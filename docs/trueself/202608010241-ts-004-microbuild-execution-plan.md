# Trueself

**Title:** TS-004 Microbuild Execution Plan

**File:** `202608010241-ts-004-microbuild-execution-plan.md`

**Timestamp:** 2026-08-01 02:41 Europe/London

**Version:** 1.0

**Status:** Active execution control

**Authority:** Current repository state plus `../quantum-spawn/202608010240-microbuild-continuity-and-product-visibility-law.md`

**Supersedes For Execution:**
- the unbounded continuation of TS-004

**Does Not Supersede:**
- `202608010226-ts-003-exact-equipment-contract-authority.md`
- prior geometry, topology, routing, receipt or evidence authority

**Restore Point:** `restore/2026-08-01-0240-pre-microbuild-law`

---

## Goal

Finish the partially implemented inverter-block aggregate as one provisional, installed and validated package contract.

Do not begin the Studio bridge until TS-004 is green.

## Verified starting point

TS-003 is complete.

The first product boundary remains:

```text
660 Wp × 30 modules × 24 strings = 475.2 kWp DC
one 352 kVA inverter block
720 modules
24 physical DC input pairs
```

The following TS-004 work exists on `main` but is not yet validated as a completed integration goal:

```text
d5affb6  feat: add inverter-block aggregate receipt
dbda809  test: bind inverter-block aggregate receipt
c5d392b  api: expose inverter-block aggregate receipt
```

The implementation deliberately retains unresolved equipment evidence and does not treat routing-fixture MPPT labels as manufacturer evidence.

## TS-004.1 — Public API classification

### Build

Add the inverter-block public names to `ApiStatus.PROVISIONAL`.

Add or extend one focused public-API test proving:

- every exported name is in `solar_topology.__all__`;
- every name is explicitly provisional;
- top-level objects are identical to `solar_topology.inverter_block` authority objects.

### Files allowed

```text
src/solar_topology/public_api.py
tests/test_inverter_block_public_api.py
```

### Files prohibited

```text
src/solar_topology/inverter_block.py
src/solar_topology/array/**
src/solar_topology/equipment_profiles.py
browser files
programme-state.json
```

### Test

Run only the focused inverter-block and public-API tests.

### Stop condition

Commit the green microbuild. Do not continue if the focused contract fails.

## TS-004.2 — Clean-wheel contract

### Build

Extend the existing clean-wheel probe to build the reference inverter block through the top-level installed package API and verify:

- exact 720 / 24 / 30 / 475.2 / 352 / 1.35 product boundary;
- deterministic payload, JSON and receipt hash;
- child Build 025 receipt identity remains bound;
- equipment evidence state remains incomplete;
- MPPT mapping, internal DC topology, reverse-current blocking and PCE backfeed remain unresolved;
- routing-fixture MPPT labels are not declared equipment evidence;
- established strategy-comparison hash remains unchanged.

### Files allowed

```text
scripts/validate_clean_wheel.py
```

### Test

Run the clean-wheel probe.

### Stop condition

Commit the green microbuild. Do not add programme documentation yet.

## TS-004.3 — Integration closure

### Build

No new engineering feature.

Run:

- focused inverter-block tests;
- full Python suite;
- V8 and reconciliation suites;
- V9 suite;
- V10 JavaScript suite;
- capsule-link gate;
- programme-state drift gate;
- clean installed wheel.

### Pass result

Write one concise Trueself checkpoint containing:

```text
Goal
Build
Test
Result
Unresolved
Next
```

Update programme truth to make TS-005 active and regenerate README/dashboard.

### Failure result

Record only the failure category and exact next repair. Do not start TS-005.

## Next material goal after pass

```text
TS-005 — First authoritative Studio slice
```

Its first microbuild will be one local command returning the existing reference inverter-block JSON.

## Current pointer

```text
ACTIVE: TS-004.1 — explicit provisional public-API classification
```
