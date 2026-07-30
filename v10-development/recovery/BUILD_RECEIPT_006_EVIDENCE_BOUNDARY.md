# Build Receipt 006 — Evidence Boundary and Public Export Gate

Date: 2026-07-30

Restore point: `restore/2026-07-30-pre-v10-evidence-boundary`

Build branch: `build/006-evidence-boundary`

## Purpose

Prevent confidential Employer's Requirements, SLDs and other NDA material from entering a public research export while retaining them as authorised internal engineering context.

## Implemented contracts

- Explicit source rights states: public, authorised internal, confidential NDA and unknown.
- Explicit publication permissions: public, internal only and withheld pending review.
- Immutable `EvidenceSource` records linking existing V10 evidence descriptors to source identity, revision, observer metadata and rights controls.
- A conservative publication decision that separates public and restricted source identifiers.
- A hard public-export gate raising `PermissionError` where a result lacks an independently supportable public evidence path.
- A construction-time prohibition against marking confidential NDA evidence as public.

## Cleve Hill boundary

The public model may use publicly observable topology, planning material, press releases, OEM documents, public imagery and original calculations. Employer's Requirements and project SLD material remain internal-only. A confidential source may inform an internal hypothesis only where the eventual public conclusion has an independent public evidence path; restricted source identifiers are not returned as public support.

## Tests added

- Public observation passes.
- Confidential-only evidence fails.
- Confidential NDA evidence cannot be labelled public.
- Confidential context may coexist with independent public support.
- A mixed export is blocked where a restricted essential source lacks public support.

## Deferred

- Source registry persistence.
- Field-level export redaction.
- Canonical project/site/system/equipment/circuit identifiers.
- Public-evidence topology reconstruction.
- DuckDB/Parquet storage and independent read-back verification.

These are the next build slices after this boundary contract is validated.
