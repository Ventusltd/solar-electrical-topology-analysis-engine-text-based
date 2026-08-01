# Trueself

**Title:** TS-004 Inverter-Block Aggregate Pass

**File:** `202608010343-ts-004-inverter-block-aggregate-pass.md`

**Timestamp:** 2026-08-01 03:43 Europe/London

**Status:** Verified integration checkpoint

**Authority:** Microbuild Worker run `30680420035`, artefact `8812013685`

**Dependencies:**
- `202608010241-ts-004-microbuild-execution-plan.md`
- `../quantum-spawn/202608010303-twenty-step-github-actions-autopilot.md`

## Goal

Make the complete reference inverter block one deterministic package receipt.

## Build

The aggregate binds the evidence-qualified equipment contract to the existing geometry, assignment, topology, input-allocation, routing, installed-length and Build 025 receipt hashes.

## Test

```text
Python                              334 / 334
V8 model                              13 / 13
V8 authority reconciliation            6 / 6
V9 deterministic engine               10 / 10
V10 JavaScript                        13 / 13
Capsule links                         PASS
Programme-state drift                 PASS
Established clean wheel               PASS
Inverter-block clean wheel            PASS
```

## Result

```text
modules                               720
strings                                24
modules per string                     30
DC nameplate                         475.2 kWp
inverter apparent power              352.0 kVA
DC/AC ratio                           1.35
physical inputs allocated               24
inverter-block receipt hash  sha256:79f3d02a878e4fe6bd700d194c2b29e2500cd9511e23d469c34f3d8472f8a1f8
Build 025 child hash         sha256:d2f29cbe9fb9b5ce2e7bda95ce6828b7bd2b7ece69a5bb1e4f840d2810f9c219
equipment contract hash      sha256:1482dfd06dda6b5a1765676bf1c98fe6eee78bc7858b378fe8b7acaa00ff32de
comparison hash              sha256:413aa93c98d1b9fd5f9ffee4f577cfe29a6e74f48bd927a3ebe7f541545d6366
```

## Unresolved

Forty-seven equipment evidence items remain unresolved or candidate, including MPPT mapping, internal DC topology, reverse-current blocking, PCE backfeed, module electrical values, dimensions, connector data, factory-lead lengths and installation class.

## Next

```text
MB-10 — TS-005 hand-off proof
TS-005 — First authoritative Studio slice
```
