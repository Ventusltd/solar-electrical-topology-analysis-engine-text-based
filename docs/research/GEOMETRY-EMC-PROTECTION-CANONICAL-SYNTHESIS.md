# Geometry, EMC and Protection — Canonical Research Synthesis

## Purpose

This document is the canonical synthesis guiding the whole-table array engine, later standards validation, and later EMC/fault modelling. It contains no confidential client or site-identifying project detail.

## Architectural decision

The Python kernel is authoritative for:

- physical module and equipment placement;
- electrical topology and connection integrity;
- explicit positive and negative conductor polylines;
- geometric and installed cable length;
- standards validation;
- later electrical, fault, surge and EMC calculations;
- immutable, content-addressed receipts.

The browser is a thin V7/V8-style renderer. It receives explicit geometry and scalar results. It shall not invent routes, estimate lengths, infer topology, or execute authoritative physics.

The scalable browser path remains orthographic 2D rendering with typed/binary arrays and local coordinate origins. Graph layout engines and ornamental 3D are out of scope because geometry is already authoritative.

## Immediate engineering boundary

The first complete engineering object is one physical table with:

- 24 strings;
- 30 modules in series per string;
- 720 total modules;
- configurable table arrangement;
- configurable MPPT/input assignment within equipment limits;
- one movable inverter;
- sequential and leapfrog alternatives over identical module placement;
- explicit module leads, string free ends and inverter home runs;
- deterministic cable lengths and loop geometry.

Large plants are deterministic replication of validated table and inverter-block assemblies. There shall not be separate small-plant and GW-plant electrical algorithms.

## Equipment-profile rule

MPPT count, input count and active-input use must come from an equipment/project profile rather than model-name assumptions. Different variants or installations can expose different MPPT counts or leave inputs unused.

The kernel must distinguish:

- rated AC power from permitted DC oversizing;
- apparent-power and active-power ratings;
- ambient-dependent derating curves;
- physical string inputs;
- MPPT channels;
- isolated inputs versus inputs internally paralleled to a common bus.

## Geometry required for later EMC analysis

Every conductor segment must retain:

- stable segment, string and polarity identifiers;
- ordered vertices in physical coordinates;
- route and support classification;
- installation method;
- buried, screened, armoured and bonded-containment state;
- conductor-to-conductor separation;
- nearby bonded-structure references;
- geometric length;
- installed-length allowances as separate fields.

Positive and negative conductors must remain separate geometric objects. Cable length and enclosed loop area are independent outputs.

## Sequential and leapfrog comparison

The comparison receipt must report at least:

- positive conductor length;
- negative conductor length;
- total circuit length;
- maximum and mean pole separation;
- signed and absolute enclosed loop area;
- crossings;
- parallel-run distance;
- home-run length;
- route hash.

A shorter route is not automatically the better EMC route. Sequential routing with a distant return can enclose a much larger area than leapfrog routing. The engine must calculate the actual geometry rather than attach a generic multiplier to a strategy name.

## Duct and containment allocation

Specifications must allocate complete same-string pole pairs, not merely equal counts of positive and negative conductors.

Pairing each string's positive and negative conductors within the same route or duct collapses the differential loop. Separating like polarities into different ducts can create a much larger loop and allows a first conductor-to-earth fault to remain latent until a second fault closes a destructive earth path.

The future validator must therefore understand:

- which positive and negative belong to the same string;
- whether they share a route/duct;
- whether a route crosses or encircles bonded metallic structures;
- duct-to-duct separation;
- cross-table routing;
- route sections protected by burial, bonded metallic containment or bonded screening.

## Standards model reserved for Build 026

Rules must be versioned by standard, edition, amendment and clause. IEC 62548-1:2023 and IEC TS 62738:2018 must not be silently blended because the latter references an older IEC 62548 edition.

### String maximum current

Reserve the model:

- `I_STRING_MAX = K_I × I_SC_MOD`
- `K_I = 1.25 × K_Corr`

`K_Corr` must be provenance tracked. It may be geometry-derived for qualifying non-optimal monofacial layouts, but bifacial or unusual environmental conditions can require a cited simulation result. The engine must not silently use 1.0 where simulation is required.

### String overcurrent requirement

Reserve the current-edition check:

- `I_F_STRING + I_BF_TOTAL > I_MOD_MAX_OCPR`
- `I_F_STRING = (N_S - 1) × I_STRING_MAX`
- `I_BF_TOTAL = I_BF_PCE + I_BF_EXT_BAT`

PCE and battery backfeed are required evidence inputs. An assumed zero may be allowed only as a visible, qualified assumption; absent evidence cannot produce an unqualified clean receipt.

The topology must distinguish two strings on isolated MPPT inputs from three or more strings paralleled ahead of an input or common DC bus.

### Grouped-string protection

Grouped strings under one OCPD require both lower and upper sizing inequalities to have a solution. The validator must not use a crude universal string-count rule. Module technology, maximum overcurrent protection rating, parallel contribution, external backfeed and manufacturer approval all matter.

Any restricted-access engineering relaxation must retain its evidence burden, including documented failure-mode analysis, equipment/module withstand evidence and applicable manufacturer/client/site approval.

### SPD and route-length checks

Reserve a geometry-derived `L` versus `L_crit` check using site ground-flash density and installation category. Counted route length must exclude only those segments legitimately excluded by the applicable rule, with each excluded segment itemised by burial, bonded screen, armour or bonded metallic containment.

The presence of an SPD must not erase the calculation. A receipt should show both the normative trigger and the installed protection choice.

### Voltage scope

Do not certify a design above 1500 V DC under the IEC 62548-1 low-voltage envelope. Above 1500 V must be represented as a separate evidence regime with explicit component certifications, adopted standards and client/site approval. Do not label it casually as conventional medium voltage DC.

## Fault and EMC interpretation reserved for Build 027

The array is not only a DC current source. It is also a spatially distributed, capacitively earth-referenced, electrically long structure.

Future modelling must cover:

- first and second earth-fault states;
- line-to-line and line-to-earth paths;
- reverse current from parallel strings;
- PCE and battery backfeed;
- common-mode and differential-mode paths;
- conductor-to-earth and module-to-structure capacitance;
- loop inductance and mutual inductance;
- induced surge from lightning current steepness and loop area;
- coupling to bonded torque tubes and other metallic structures;
- SPD lead inductance, residual voltage, coordination and energy stress;
- transition from lumped to distributed/transmission-line treatment on electrically long routes.

The engine must preserve uncertainty and model-validity ranges. Simple loop-area calculations can establish ordering and identify dangerous geometry even where long-route magnitude requires a distributed model.

## Protection placement

The baseline model follows existing plant topology: SPDs are represented at string/harness combiner boxes and/or inverter DC inputs according to approved equipment and project design. Distributed module-side or pre-connector protection is a future optional topology and shall not contaminate the baseline model.

## Commercial and contractual discipline

The engine may expose deficiencies and compare alternatives, but it must not silently redesign an approved plant.

Workflow:

1. reproduce the approved/as-built topology and routing;
2. validate and model it;
3. quantify cable, loop, fault, surge, EMC, loss and evidence consequences;
4. generate an alternative only as a separate proposal;
5. require explicit client, designer and site approval before treating a material change as adopted.

This is essential for contractual relevance, warranty defensibility and confidential-project separation.

## Product framing

The strongest commercial proposition is not ornamental visualisation and not an abstract safety claim. It is evidence that real routing geometry can repeatedly impose significant impulse stress on modules and equipment, potentially approaching or exceeding certified impulse withstand, while warranty claims otherwise appear to be component failures.

The platform provides an auditable method to distinguish:

- component defect;
- connector/installation defect;
- protection-coordination failure;
- routing-induced EMC or surge stress;
- unsupported design assumption;
- approved but suboptimal client/site configuration.

Use precise calculated voltage ranges and evidence classes. Prefer `fail-safe`, `local autonomous action` and `communications-independent` over marketing labels such as `nuclear grade`.

## Build order

1. Build 025A: table geometry primitives and deterministic 720-module placement.
2. Build 025B: 24 explicit ordered strings of 30 modules.
3. Build 025C: terminal and conductor geometry for sequential and leapfrog.
4. Build 025D: movable inverter and explicit home runs.
5. Build 025E: MPPT/input topology and equipment limits.
6. Build 025F: installation classifications and installed-length layers.
7. Build 025G: geometry comparison and physics hand-off receipt.
8. Build 026: versioned standards validation and protection coordination.
9. Build 027: EMC, surge, distributed capacitance and fault-path physics.

## Non-negotiable rule

Do not calculate authoritative electrical physics on an abstract string count.

All later standards and physics calculations must operate on an evidenced topology whose actual conductor geometry, installation method, equipment limits and provenance are already known.
