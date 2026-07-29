# V10 Restore Points

## 2026-07-29 — Main baseline before complete inverter workbench

- Repository state: `42fdd2896a409117f99d1fb64064cd2dc3c63956`
- Meaning: first V10 kernel, tests, governance files and browser workbench on `main`.

## 2026-07-29 — V10 browser snapshot before 24-string build

- Snapshot commit: `0e2cff82016b770d844d2f13ad61abc155a2a13a`
- Preserved file: `restore-points/2026-07-29-before-24-string-v10/index.html`
- Original live path: `v10-development/index.html`
- Meaning: the original one-string V10 browser shell can be restored without moving branches.

All continuing V10 work is committed directly to `main`. A restore is performed by copying the preserved file back to its original path or reverting to the recorded commit SHA.
