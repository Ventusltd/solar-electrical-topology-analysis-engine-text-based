# Trueself

**Title:** TS-003 Generic Reference Equipment Contract Passed

**File:** `202608010225-ts-003-generic-reference-equipment-contract-pass.md`

**Timestamp:** 2026-08-01 02:25 Europe/London

**Version:** 1.0

**Status:** Verified execution checkpoint

**Authority:** Repository implementation, GitHub Actions run `30677652813` and validation artefact `8811058756`

**Supersedes:** None

**Dependencies:**
- `202608010104-complete-352-kva-inverter-block-plan.md`
- `202608010117-civilisational-consciousness-and-amnesia-covenant.md`
- `202608010154-ts-002-programme-truth-and-capsule-integrity.md`
- `202608010222-build-026-standards-correction-register.md`
- `../quantum-spawn/202608010151-bounded-observation-and-truncation-law.md`

**Current Build:** Build 025.5D1

**Completed Goal:** TS-003 — Freeze the generic reference equipment contract

**Restore Point:** `restore/2026-08-01-0210-pre-ts-003-equipment-contract`

---

## 1. Goal attempted

Create one versioned, generic and evidence-qualified equipment contract for the first complete product boundary without using manufacturer names, project names, client names or confidential site information.

The bounded goal required:

- one generic 660 Wp bifacial module profile;
- one generic 352 kVA inverter profile;
- 24 explicit physical DC input terminal pairs;
- generic connector, factory-lead and field-conductor profiles;
- exact 30-module by 24-string reference arithmetic;
- deterministic payload, canonical JSON and hash;
- explicit missing-evidence states;
- no assumed MPPT mapping, shared DC bus, reverse-current blocking or PCE backfeed;
- no source promotion;
- clean installed-wheel reproduction.

The goal prohibited:

- standards calculations;
- protection conclusions;
- EMC or lightning calculations;
- changes to geometry, topology, routing or calculation receipts;
- confidential or manufacturer-identifying data;
- silent completion of missing equipment evidence.

## 2. Build completed

New provisional module:

```text
src/solar_topology/equipment_profiles.py
```

The module provides versioned types and deterministic serialisation for:

```text
QualifiedValue
ModuleEquipmentProfile
DcInputProfile
InverterEquipmentProfile
ConnectorEquipmentProfile
FactoryLeadSetProfile
FieldConductorProfile
ReferenceEquipmentContract
```

The supported package API now exposes the equipment-contract types, builder, validator, payload, JSON, hash and missing-evidence functions directly through `solar_topology`.

All equipment-contract exports are explicitly classified:

```text
ApiStatus.PROVISIONAL
```

No duplicate package-level implementation exists. Top-level exports resolve to the packaged `solar_topology.equipment_profiles` authority.

## 3. Exact first product boundary

The deterministic generic contract binds:

```text
module technology                    bifacial
module rated power                    660 Wp
modules per string                     30
string rated power                     19.8 kWp
strings                                 24
module count                           720
total DC nameplate power               475.2 kWp
inverter apparent-power rating         352 kVA
DC-to-AC nameplate ratio                 1.35
physical DC input pairs                  24
```

The equipment contract identifier is:

```text
generic_352kva_475_2kwp_reference_equipment
```

Contract revision:

```text
2026-08-01.1
```

Deterministic contract hash:

```text
sha256:103437b129a73c8157a17b39ea96584f87e8e3fe300fa946e746b26a564b6759
```

## 4. Evidence deliberately unresolved

The contract reports 47 missing or candidate evidence items.

The unresolved set includes, without being limited to:

- module `Voc`;
- module `Isc`;
- module `Vmp`;
- module `Imp`;
- module maximum overcurrent-protection rating;
- bifaciality or BNPI current basis;
- module dimensions;
- connector resistance;
- connector current and voltage rating;
- connector mating compatibility;
- positive and negative factory-lead lengths;
- installation class;
- MPPT count;
- mapping of each physical input to an MPPT control channel;
- internal DC topology;
- reverse-current blocking;
- PCE backfeed current;
- maximum DC voltage;
- maximum DC input-power evidence.

The 475.2 kWp value is the reference block nameplate. It is not represented as an inferred inverter maximum-input-power rating.

## 5. Physical input discipline

The contract exposes 24 unique physical input objects.

Each input has:

- one stable input identifier;
- one positive terminal identifier;
- one negative terminal identifier;
- one unresolved MPPT-control relationship.

The contract does not infer internal electrical paralleling from physical-input count or future MPPT labels.

The following remain explicitly `unknown`:

```text
internal DC topology
reverse-current blocking
PCE backfeed
MPPT mapping
```

This preserves the distinction between a physical input, an MPPT control function and any shared inverter DC bus.

## 6. Conductor and connector discipline

The contract references the existing generic conductor products:

```text
factory_module_lead_4mm2_metal_coated_class5
external_string_6mm2_metal_coated_class5
```

Both resistance sources remain:

```text
status: candidate
reasons:
- SOURCE_REVISION_PLACEHOLDER
- VERIFICATION_NOT_VERIFIED
```

No resistance source was promoted.

The connector profile remains generic and unresolved. No manufacturer family, compatibility state or contact-resistance value was invented.

## 7. Files changed

```text
src/solar_topology/equipment_profiles.py
src/solar_topology/__init__.py
src/solar_topology/public_api.py
tests/test_equipment_profiles.py
tests/test_equipment_profiles_public_api.py
scripts/validate_clean_wheel.py
```

Implementation commits on `main`:

```text
7144930  feat: add generic reference equipment contract
2868323  test: bind generic reference equipment contract
c01cc31  api: classify generic equipment contract provisional
678fd33  api: expose generic reference equipment contract
5442cfa  test: bind equipment contract public API
958edb0  test: prove equipment contract from clean wheel
0e6f193  test: match first equipment invariant failure
```

## 8. First validation result and bounded correction

Initial validation-only PR 24 produced:

```text
clean installed wheel              PASS
capsule-link integrity             PASS
programme-state drift              PASS
V8, V9 and V10 JavaScript          PASS
Python                             294 passed / 1 failed
```

The sole failure was in a test assertion.

A deliberately mutated 661 Wp fixture correctly failed the earlier 19.8 kWp string invariant. The test expected the later 475.2 kWp block invariant message.

No production-code, payload, hash, package or electrical result failed.

The test was corrected to require the first violated invariant:

```text
19.8 kWp
```

Commit:

```text
0e6f193  test: match first equipment invariant failure
```

This failure is retained because it demonstrates the Trueself rule: inspect the exact failure, fix only the bounded defect and rerun before expansion.

## 9. Final validation execution

Validation-only draft PR:

```text
PR 25
head branch: agent/ts-003-equipment-contract-validation-r2
head commit: 4297c93db4a7b14f5543fb0f67e950b72c7008b4
base main: 0e6f1938f32db5feed363e9ae5e474acf8f84465
```

GitHub Actions:

```text
run id: 30677652813
workflow: V10 Engine Validation
workflow result: PASS
```

Validation artefact:

```text
artefact id: 8811058756
artefact name: v10-validation-8e7bdd315ed5b1cbd018d755dec62372eff5dfc7
artefact digest: sha256:b38c2681b241a1d35abcdb15e6caf4b07b0a424c4e28da2bfe7318a23a42cd3f
merge-test SHA: 8e7bdd315ed5b1cbd018d755dec62372eff5dfc7
```

## 10. Full validation result

```text
Python                             295 passed / 0 failed
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

The established 24-by-30 geometry and total-conductor comparison remained unchanged:

```text
comparison hash:
sha256:413aa93c98d1b9fd5f9ffee4f577cfe29a6e74f48bd927a3ebe7f541545d6366

sequential total conductor     2513.328 m
leapfrog total conductor       2560.128 m
field-installed reduction       798.288 m
factory-fitted increase          845.088 m
total conductor change           +46.800 m
```

## 11. Authority meaning

TS-003 establishes a supported and deterministic generic equipment-data boundary.

It does not establish:

- a verified manufacturer profile;
- complete module electrical data;
- an evidenced MPPT/input map;
- internal bus topology;
- reverse-current blocking;
- PCE backfeed;
- protection compliance;
- a first-class inverter-block aggregate receipt.

Those missing facts remain visible and block or qualify future studies.

## 12. Standards correction hand-off

The separate register:

```text
docs/trueself/202608010222-build-026-standards-correction-register.md
```

records primary-source corrections that must govern later Build 026 implementation.

Those corrections do not alter TS-003 or current steady-state engineering.

## 13. Goal status

```text
TS-003  COMPLETE
```

## 14. Next single goal

```text
TS-004 — Add the complete inverter-block aggregate and receipt
```

TS-004 shall create a typed aggregate above physical tables or array sections and below the later power-block level.

It shall bind the generic equipment contract to the existing geometry, topology, assignment and routing receipts without changing their historical hashes unless the new aggregate is explicitly requested.

TS-004 shall not add standards, EMC, lightning or browser calculations.
