# Refinement 01 — Audit Synthesis and Refinement Order

Timestamp: 2026-07-31 19:26 +0100

## Purpose

This refinement records the reconciled outcome of the independent Claude audit, the authenticated repository review and the subsequent technical corrections. It is a forward engineering instruction, not a claim that the listed refinements are already implemented.

Build 025 is accepted as a substantial and technically real advance. It establishes two-dimensional module geometry, deterministic string membership, authoritative topology traversal, physical input allocation, explicit conductor routes, movable-inverter dependence, separate factory-fitted and field-installed conductor accounting, signed and absolute loop-area metrics, installation classifications, installed-length allowances and deterministic receipts.

The principal conclusion is now stable:

- leapfrog reduces field-installed home-run conductor materially;
- leapfrog may increase total conductor once the longer factory-fitted interconnect path is included;
- leapfrog's strongest justification is reduced loop geometry, conductor separation and exposure to electromagnetic coupling rather than a claim of large total-copper saving;
- all such numerical conclusions remain fixture-specific until module terminal geometry, tilt and route elevations are evidenced.

## Accepted audit findings

The following findings are accepted as actionable:

1. Exact uncertainty intervals can reject the canonical nominal result because mathematically equivalent floating-point sums are accumulated in different orders.
2. Legacy V6 and V9 public calculations use ideal bulk-copper resistivity divided by nominal area and therefore do not represent IEC 60228 Class 5 maximum conductor resistance.
3. Build 025 terminal offsets default to one unresolved point and the present 50 mm route separation is a routing assumption rather than manufacturer geometry.
4. Build 025 is presently a plan-coordinate model without explicit table tilt or route elevation.
5. Build 025 root-level modules are outside the packaged `src/solar_topology` authority path and require an installed-artifact test.
6. The V8 external-cable saving and Build 025 total-conductor result can be read as contradictory unless the ownership boundary is made explicit.
7. Build 025 computes geometry suitable for later EMC analysis but does not yet compute induced voltage, flux linkage, impedance, surge response or fault energy.

## Corrected interpretations

The following qualifications govern future reporting:

- Mean pole separation multiplied by parallel-run distance is not a rigorous decomposition of absolute winding area. It may be used only as a diagnostic indicator.
- Signed loop area represents the uniform-field geometric integral. Absolute winding area is a conservative geometric envelope, not by itself a close-lightning-strike induced-voltage answer.
- A non-uniform magnetic field requires spatial integration of winding number and field over the routed loop.
- Surface area scales from horizontal projection by `1 / cos(tilt)` only for a planar loop whose reported area is a horizontal projection. Individual route lengths require component-wise three-dimensional geometry and do not all scale by the same factor.
- V8 and Build 025 are not intrinsically inconsistent if V8 is explicitly restricted to field-installed external cable. They become inconsistent only when V8 presents that quantity as total copper or total circuit conductor.

## Refinement priority

The next engineering work shall proceed in this order:

1. Repair exact-interval numerical stability and add broad module-count regression coverage.
2. Introduce evidence-bound conductor resistance and annotate or quarantine ideal-bulk legacy outputs.
3. Reconcile V8 field-installed cable language with Build 025 total-conductor accounting.
4. Move the Build 025 authority modules into the installable package and validate a clean wheel or editable installation outside the repository root.
5. Add evidenced terminal coordinates, table-plane tilt and three-dimensional route geometry.
6. Define separate signed-flux, absolute-bound and spatially weighted electromagnetic quantities before Build 027 calculations are exposed.
7. Require visible CI status and release gates for each authoritative calculation change.

## Non-negotiable reporting rules

Every future strategy comparison shall report, separately:

- factory-fitted conductor length;
- field-installed geometric length;
- field-installed installed length;
- procurement length;
- total circuit conductor length;
- signed loop area;
- absolute winding area;
- maximum and mean pole separation;
- terminal-geometry evidence class;
- geometry dimensionality and tilt assumptions;
- resistance evidence basis;
- calculation and source versions.

No single metric may be relabelled as total copper saving, EMC performance or standards compliance without the corresponding authority chain.
