# Claude Feed Technical Audit Reconciliation

Date: 2026-07-30
Branch: `main`
Repository: `Ventusltd/solar-electrical-topology-analysis-engine-text-based`

## Decision

The feed is useful as a review of the obsolete draft branch `v10-terminal-geometry-and-leads`, but it is not an audit of the current authoritative `main` branch and must not drive a rollback or duplicate implementation.

## Confirmed useful findings

The following observations remain useful as engineering requirements:

- route length must be geometry-derived and must distinguish direct span from routed conductor length;
- resistance, voltage drop and power loss must use full circuit length and declared conductor temperature;
- operating current for loss must remain separate from design current used for ampacity and protection studies;
- cold string Voc must retain an explicit temperature basis and system-voltage criterion source;
- transient studies require a declared lumped-versus-distributed validity boundary;
- browser warnings must never be the sole enforcement mechanism for blocking engineering findings.

These requirements are already represented in the current build order through Builds 023–026 and the study/evidence architecture.

## Feed claims superseded by current `main`

### R/L/C and stored energy are not missing

Current authoritative Python source `src/solar_topology/formulas.py` already contains guarded, unit-bearing implementations for:

- temperature-corrected finished-cable DC resistance;
- two-wire external inductance per unit length;
- internal loop inductance per unit length;
- total low-frequency inductance per unit length;
- conductor-to-conductor capacitance per unit length;
- characteristic impedance;
- propagation velocity;
- indicative module-to-frame capacitance;
- cold string Voc;
- stored magnetic energy;
- stored electric energy.

The implementation explicitly separates external inductance used for TEM propagation from low-frequency internal inductance used for stored-energy and lumped `L di/dt` studies.

### Temperature correction is not missing from the current physics layer

`dc_resistance()` accepts finished-cable resistance per metre at 20 °C and applies the copper coefficient `0.00393 / K` against declared conductor temperature. The current canonical calculation architecture therefore does not depend on the obsolete flat-resistance arithmetic in `v10-development/src/inverter-block.mjs`.

### The two-conductor factor is not an implicit constant

The current architecture represents ordered physical segments and complete-circuit traversal. Positive and negative conductor segments are explicit physical records. Complete-circuit resistance is calculated over the ordered segment set rather than by applying an unexplained global factor of two. A factor of two is valid only when one route length is known to represent one pole and the return route is identical; it must not replace physical segment geometry for unequal routes.

### Cold Voc is implemented in the authoritative formula layer

`cold_string_voc()` applies the declared module count, module Voc, beta coefficient in percent per degree Celsius and cell temperature relative to 25 °C. Acceptance against a maximum system voltage remains a separate sourced criterion and study receipt, which is the intended evidence architecture.

### Current main is not the draft PR branch

The feed repeatedly states that the repository contains only a README on `main` and that the engine exists only in draft PR #5. That is stale. Current `main` contains the recovered Python engine, V8 and V9 references, V10 JavaScript candidate, diagnostics, evidence, persistence, circuit validation, traversal, studies, tests, validation receipts and recovery records.

## Items retained for later bounded builds

The feed raises legitimate requirements that are intentionally not implemented during Build 023:

1. explicit route-polylines, bend/slack/service-loop rules and evidence status — Build 025;
2. separate operating, short-circuit, design and protective-device current quantities — Builds 025 and 030;
3. acceptance criteria for voltage drop, ampacity and system maximum voltage — Build 030;
4. conductor-to-frame/earth capacitance refinement and measured calibration — Builds 026 and 031;
5. automatic electrical-length validity gate and distributed model selection — Build 026;
6. surge-sharing, interruption and arc-restrike study implementations — Builds 026, 031 and 032;
7. browser presentation of blocking diagnostics — Build 027 and Build 035.

## Build-order consequence

Do not divert Build 023 into formula changes based on this feed. Continue the frozen order:

```text
Build 023  close canonical object/topology contracts
Build 024  decide authoritative steady-state kernel
Build 025  close route and installation physics
Build 026  declare and implement distributed/transient boundary
Build 030  implement sourced electrical acceptance studies
Build 031  EMC, lightning and SPD studies
Build 032  arc-fault and rapid-shutdown studies
```

## Exact next action

Continue Build 023 structural verification. Treat the Claude feed as an external review input whose valid requirements are mapped to later bounded builds, not as evidence that current physics is absent.
