# Main-Branch-Only Build Rule

Status: Binding repository operating instruction
Owner and approver: Vikram Kumar, Ventus Ltd
Effective date: 2026-07-30

## Rule

All further V10 build work shall be committed directly to `main`.

Do not create feature branches, restore branches or pull requests for V10 work unless Vikram Kumar explicitly overrides this instruction.

## Restore discipline

Before each material V10 build slice:

1. record the exact current `main` commit as the pre-build restore point;
2. describe the bounded build and affected files in a recovery receipt;
3. apply the bounded build directly to `main`;
4. run and record the relevant validation when execution is available;
5. record the completed build commit and preserve all earlier commit restore points.

A Git commit is the restore point. Recovery is performed by inspecting, reverting or restoring from that exact commit. No branch is required.

## Restore-point register

### Evidence boundary and publication gate

Pre-build commit: `2136014adfbca5f886c2cc69040eae73480fe043`

This commit is the merged Build 006 position before package-level evidence-boundary exports and subsequent main-only work.

### Uncertainty and operating state

Pre-build commit: `074c5743f82b867f05abb46927e8facdc5fbb84a`

This restore point captures `main` immediately before conservative interval uncertainty propagation, immutable current and string-Vmp operating-state inputs, voltage-drop percentage and deterministic uncertainty receipts were added.

### Evidence and complete-circuit calculation

Pre-build commit: `afa54a057e0aa02bd264958590dc1782c281fd7d`

This restore point captures `main` immediately before evidence vocabulary reconciliation, immutable calculation receipts and validated complete-circuit resistance, voltage-drop and loss calculations were added.

### Cartridge adapter and ordered traversal

Pre-build commit: `2e14b87db26c6de0ad7d175135a1ef166a8b0717`

This restore point captures `main` immediately before sequential and leapfrog cartridge output was adapted into the canonical circuit model and independently traversed.

### Canonical circuit foundation

Pre-build commit: `a7c20cf65a01832103f46e0a6e1690bc7f727252`

This restore point captures `main` immediately before the V10 canonical circuit foundation was landed.

## Current build position

Build receipt:

`v10-development/recovery/BUILD_RECEIPT_006_EVIDENCE_BOUNDARY.md`

Latest main commit after package export:

`40b008f82dbaf12d6ff49fffc5f1685dfdc41639`

The last fully recorded validation remains:

```text
Python:          66 passed
V8:              13/13 passed
V9:              10 passed, 0 failed
V10 JavaScript:  13 passed, 0 failed
Overall:         PASS
```

Build 006 and the package export require a fresh validation receipt when a test runner is available.

## Boundaries

Main-only development does not remove the engineering controls:

- physical objects before calculations;
- topology validation before dependent calculation;
- deterministic and reviewable changes;
- no browser-first engineering;
- no copied protected standards or confidential material;
- evidence and provenance remain mandatory;
- no authority promotion without appropriate validation.
