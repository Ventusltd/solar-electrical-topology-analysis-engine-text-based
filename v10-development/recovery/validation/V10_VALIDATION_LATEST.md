# V10 Validation Execution Evidence

## Repository pointer

This file is no longer the latest validation execution receipt.

Routine validation evidence is now produced by `.github/workflows/v10-validation.yml` and retained as a commit-specific GitHub Actions artifact named:

```text
v10-validation-<commit-sha>
```

Each artifact contains:

```text
V10_VALIDATION_LATEST.json
V10_VALIDATION_LATEST.md
```

The GitHub Actions check is the execution gate. The artifact is the execution envelope. Runtime timestamps, runner details and command output are intentionally no longer committed to deterministic source history.

## Migration

Workflow authority changed in commit:

```text
17e761bd191e10284ee18aabf9f195ec658a83fb
```

The previously committed failing receipt represented commit:

```text
4375b4e2e70d722f5dafbf5df174f5a490d3b605
```

That execution failed only because the V8 absolute winding-area percentage expectation used an over-tight rounded value. The authority calculation and regression expectation were corrected in:

```text
26bb0bc9ee1e1e97d0782aa76455605bb5d242f4
```

This pointer does not assert the outcome of a later workflow execution. Consult the check and artifact attached to the exact commit being reviewed.

## Governing distinction

```text
Engineering receipt
- deterministic source and calculation content
- content-addressed hashes
- method and schema versions

Execution envelope
- timestamp
- workflow and runner
- repository commit
- command output
- pass or fail result
```

A routine execution envelope is evidence about a run. It is not itself a source-code change and must not create repetitive GridBot commits on `main`.
