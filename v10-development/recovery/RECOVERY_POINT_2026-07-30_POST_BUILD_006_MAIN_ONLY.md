# Post-Build 006 Main-Only Recovery Point

Date: 2026-07-30

## Instruction

All further V10 work is performed directly on `main`. No feature, pull-request or restore branches are to be created unless Vikram Kumar explicitly changes the instruction.

## Recovery commits

Pre-Build 006 merged main position:

`2136014adfbca5f886c2cc69040eae73480fe043`

Evidence-boundary package export completed at:

`40b008f82dbaf12d6ff49fffc5f1685dfdc41639`

Main-only restore discipline updated at:

`ee540ff951b48fd3b975b1885fb382d5bb3754f6`

## Recovery method

Use the exact commit required as the immutable recovery source. Inspect or restore the affected files from that commit, or revert the bounded later commit. Do not create a recovery branch as part of the normal V10 workflow.

## Build 006 files

- `src/solar_topology/evidence_boundary.py`
- `tests/test_evidence_boundary.py`
- `v10-development/recovery/BUILD_RECEIPT_006_EVIDENCE_BOUNDARY.md`
- `src/solar_topology/__init__.py` package export

## Validation status

The last fully recorded repository validation predates Build 006. Build 006 and its package export remain pending a fresh complete test execution and validation receipt. No unexecuted test result is claimed here.
