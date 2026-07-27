# Restore point — before FEED I electromagnetic build

Created: 27 July 2026

Purpose: preserve the working root engine and the current independent V7 development workspace before beginning the FEED I electrical and electronics engineering implementation.

## Separation law

The working root application must not be altered by the FEED I build. New executable work begins under `v7-development/feed-i/`.

## Exact pre-build file identities

- `README.md` blob SHA: `81d989ca92a65ab590c2416748c0f1e48dd7ca20`
- `v7-development/index.html` blob SHA: `e55babbdf44c8c5a911ee01fce3ad36931bbe3ed`
- `v7-development/COMPARISON.md` blob SHA: `cb38404d5c107edaeff8296623b1ba6e57b17329`

These blob identities are the authoritative recovery references for the files that may be documented or compared during this phase.

## Recovery objective

If the FEED I build becomes inconsistent, remove or revert only the new `v7-development/feed-i/` files and restore the three files above to the recorded blob contents. Do not change the root application as part of recovery.

## FEED I boundary

FEED I introduces foundations only:

- dimensional and unit discipline;
- epistemic status attached to inputs and outputs;
- closed-form two-wire differential parameters;
- separate common-mode representation;
- frequency-aware event classification;
- corrected RC-sheet conductivity direction;
- capacitance aggregation with explicit units;
- validation gates and unresolved OEM/measurement dependencies.

It does not claim measured glass-glass module capacitance, validated water-film participation, validated inverter impedance, or standards compliance.
