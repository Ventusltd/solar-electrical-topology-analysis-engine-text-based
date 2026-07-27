# FEED I Comparison — Working Root, Current V7 and New Isolated Build

## Purpose

This file prevents development drift by making the three code lines explicit.

| Area | Working root engine | Current V7 development page | FEED I isolated build |
|---|---|---|---|
| Path | `/` | `/v7-development/` | `/v7-development/feed-i/` |
| Role | Stable live regression reference | Existing independent graphical prototype | Electrical and electronics engineering foundation build |
| Root-file dependency | Native root files | Self-contained current V7 page | No root imports; independent files only |
| Geometry | Proven working array geometry | Reuses proven physical array arrangement | No replacement renderer in Phase 0 |
| Capacitance | Earlier screening implementation | Fixed dry/full-area wet screen; one revision stale | Dry floor plus frequency-dependent film architecture, with unvalidated status |
| Water film | Not frequency resolved | Pending | Conductivity/frequency scaling scaffold only; no claim of validation |
| Inductance | Segmented screening | Closed-form differential and common-mode screens | Two-tier method formalised: closed form plus PEEC-required flags |
| Lumped/distributed | Existing rise-time banner | Rise time versus delay screen | Corrected configurable classification with explicit ratio |
| Multi-MPPT common mode | Simplified | Simplified common-link interpretation | Frequency-dependent coupling state, including unknown bounding cases |
| Units | Browser values | Browser values | Unit-bearing result objects and dimensional self-checks |
| Provenance | Visible warnings | Visible warnings | Formal epistemic-status propagation |
| Validation | Manual engineering review | Manual engineering review | Built-in self-tests and future measurement records |
| Standards status | Screening commentary | Screening commentary | Normative, standards-guided and research classifications kept separate |
| Replacement authority | Current stable reference | Experimental only | Cannot replace either version until acceptance gates pass |

## Specific differences introduced by FEED I

### 1. Capacitance is not a naked scalar

Every capacitance result contains:

- numeric value;
- declared unit;
- frequency basis;
- environmental state;
- aggregation boundary;
- epistemic status;
- method;
- dependencies.

### 2. Wet does not replace dry

The model rule becomes:

`C_total(f, environment) = C_dry(f) + C_film(f, environment)`

The film contribution may collapse with frequency while the dry contribution remains as the floor.

### 3. Conductivity direction is explicit

Higher film conductivity increases the characteristic participating distance; higher frequency reduces it. The exact coefficient remains unvalidated.

### 4. Event model selection is ratio based

The model reports the ratio of event rise time to one-way propagation delay and classifies the case as lumped, transitional or distributed.

### 5. Common-mode coupling is not binary

The inverter input boundary is represented by a coupling state and frequency band rather than a universal statement that strings are always isolated or always paralleled.

## Non-regression rule

No FEED I commit may alter:

- root `index.html`;
- root `styles.css`;
- root `app.js`;
- root `physics.generated.js`;
- root navigation files;
- current `v7-development/index.html` during Phase 0.

The isolated build may later inform the current V7 page, but only after explicit comparison and acceptance.
