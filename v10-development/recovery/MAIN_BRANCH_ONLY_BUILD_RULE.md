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

## Current restore point

Branch: `restore/2026-07-30-pre-v10-canonical-circuit-foundation`
Commit: `a7c20cf65a01832103f46e0a6e1690bc7f727252`

This restore point captures `main` immediately before the V10 canonical circuit foundation was landed.

## Boundaries

Main-only development does not remove the engineering controls:

- physical objects before calculations;
- topology validation before dependent calculation;
- deterministic and reviewable changes;
- no browser-first engineering;
- no copied protected standards or confidential material;
- evidence and provenance remain mandatory;
- no authority promotion without appropriate validation.
