# Main-Branch-Only Build Rule

Status: Binding repository operating instruction
Owner and approver: Vikram Kumar, Ventus Ltd
Effective date: 2026-07-30

## Rule

All further V10 build work shall be committed directly to `main`.

Do not create feature branches or pull requests for V10 work unless Vikram Kumar explicitly overrides this instruction.

## Restore discipline

Before each material V10 build slice:

1. create a dated restore branch from the current `main` head;
2. record the exact restore commit;
3. apply the bounded build directly to `main`;
4. run and record the relevant validation;
5. preserve earlier versions and restore points.

## Restore-point register

### Uncertainty and operating state

Branch: `restore/2026-07-30-pre-v10-uncertainty-operating-state`  
Commit: `074c5743f82b867f05abb46927e8facdc5fbb84a`

This restore point captures `main` immediately before conservative interval uncertainty propagation, immutable current and string-Vmp operating-state inputs, voltage-drop percentage and deterministic uncertainty receipts were added.

### Evidence and complete-circuit calculation

Branch: `restore/2026-07-30-pre-v10-evidence-calculation-receipts`  
Commit: `afa54a057e0aa02bd264958590dc1782c281fd7d`

This restore point captures `main` immediately before evidence vocabulary reconciliation, immutable calculation receipts and validated complete-circuit resistance, voltage-drop and loss calculations were added.

### Cartridge adapter and ordered traversal

Branch: `restore/2026-07-30-pre-v10-cartridge-adapter-traversal`  
Commit: `2e14b87db26c6de0ad7d175135a1ef166a8b0717`

This restore point captures `main` immediately before sequential and leapfrog cartridge output was adapted into the canonical circuit model and independently traversed.

### Canonical circuit foundation

Branch: `restore/2026-07-30-pre-v10-canonical-circuit-foundation`  
Commit: `a7c20cf65a01832103f46e0a6e1690bc7f727252`

This restore point captures `main` immediately before the V10 canonical circuit foundation was landed.

## Current validated position

Build receipt:

`v10-development/recovery/BUILD_RECEIPT_005_UNCERTAINTY_AND_OPERATING_STATE.md`

Validation receipt:

`v10-development/recovery/validation/V10_VALIDATION_LATEST.md`

The declared suites passed at validation source head `80057fe4bdfbbafc97ee6fa3cf8082f9e02ae598`:

```text
Python:          66 passed
V8:              13/13 passed
V9:              10 passed, 0 failed
V10 JavaScript:  13 passed, 0 failed
Overall:         PASS
```

## Boundaries

Main-only development does not remove the engineering controls:

- physical objects before calculations;
- topology validation before dependent calculation;
- deterministic and reviewable changes;
- no browser-first engineering;
- no copied protected standards or confidential material;
- evidence and provenance remain mandatory;
- no authority promotion without appropriate validation.
