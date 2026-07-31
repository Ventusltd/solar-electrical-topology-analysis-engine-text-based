# Refinement 03 — Resistance Evidence and Legacy Calculations

Timestamp: 2026-07-31 19:28 +0100

## Defect statement

The legacy browser engines calculate conductor resistance from ideal copper bulk resistivity divided by nominal cross-sectional area:

```text
R = rho × length / nominal area
```

The current constants are approximately:

```text
1.724 × 10^-8 ohm metre
0.017241 ohm millimetre squared per metre
```

This is a legitimate ideal-material estimate. It is not an authoritative representation of a finished stranded, flexible, compacted, tinned or manufacturer-specific cable. It can therefore produce optimistic voltage-drop and resistive-loss results when compared with a declared product resistance or a standards maximum.

The correction is not to replace one universal constant with a different universal constant. The correction is to make resistance an evidence-bound product property.

## Required resistance authority

Every conductor segment used for an authoritative electrical calculation shall carry a resistance basis selected from an explicit controlled vocabulary:

```text
manufacturer_declared
independently_measured
standard_maximum
ideal_bulk_estimate
assumed
unresolved
```

The segment shall preserve at least:

```text
conductor_product_id
material
nominal_cross_section_mm2
conductor_class_or_construction
plating_or_coating
r20_ohm_per_m
resistance_basis
source_reference
source_edition_or_revision
source_value_and_unit
verification_state
measurement_conditions_if_applicable
temperature_coefficient_basis
```

The engine must never infer that nominal area alone identifies the finished conductor resistance.

## Precedence rule

Unless the user deliberately selects another engineering case, the default precedence for a product-specific calculation shall be:

1. independently measured value for the represented product and condition;
2. current manufacturer-declared maximum or nominal value, clearly distinguished;
3. applicable standard maximum for the declared conductor class and material;
4. ideal bulk estimate, visibly marked as a lower-bound screening estimate;
5. unresolved result when none of the above is evidenced.

A manufacturer nominal and manufacturer maximum are not interchangeable. The receipt shall preserve which one was supplied.

## Standards data rule

IEC 60228 or any equivalent conductor table shall be represented as a versioned data source, not copied into dispersed formula constants.

The standards-backed lookup shall require:

```text
standard
edition
material
conductor class
nominal area
temperature basis
maximum resistance
```

Unsupported combinations shall return an incomplete-evidence diagnostic. They shall not silently fall back to ideal copper.

Licensed standards text shall not be reproduced. Numeric values used by the engine shall retain clause or table provenance and licensing status.

## Temperature correction

The temperature correction remains a separate operation from the 20 degree Celsius resistance basis:

```text
R(T) = R20 × [1 + alpha × (T - 20)]
```

The receipt shall identify the selected `alpha` basis. Copper, aluminium, alloy, plated and measured-product cases may require different evidence handling.

Connector and termination resistance shall remain separate from conductor resistance. Applying the conductor temperature coefficient to a connector is permitted only when the connector model explicitly declares that approximation.

## Legacy V6 and V9 treatment

The existing V6 and V9 calculations may remain available for reproducibility, but they shall be labelled accurately:

```text
Ideal bulk-copper screening calculation using nominal metallic area.
Not a finished-cable declared resistance and not an IEC 60228 maximum-resistance calculation.
```

Required actions:

- expose the resistance basis beside every displayed resistance, voltage-drop and loss output;
- prevent public pages from describing ideal-bulk outputs as cable-product results;
- add a visible comparison mode showing ideal bulk, standard maximum and manufacturer-declared cases when evidence exists;
- retain historical formula versions so earlier outputs remain reproducible;
- ensure V10 authoritative receipts never inherit a legacy resistance constant without provenance.

## Calculation API refinement

The authoritative circuit API should accept a resolved resistance record rather than derive resistance invisibly from area:

```python
ResolvedConductorResistance(
    product_id=...,
    r20_ohm_per_m=...,
    basis=...,
    evidence=...,
)
```

Nominal area may remain an independent physical attribute for mass, current density, geometry and validation. It shall not substitute for `r20_ohm_per_m`.

## Required tests

Add deterministic tests proving:

- manufacturer, measured, standard-maximum and ideal-bulk cases remain distinguishable;
- the same area can produce different valid resistance values when the evidence basis differs;
- voltage drop and `I²R` loss track the selected resistance case exactly;
- a weaker evidence case cannot silently override a stronger product-specific case;
- missing class or source information prevents a standards-maximum claim;
- legacy ideal-bulk results remain reproducible after the authority migration;
- receipt hashes change when the resistance value, basis, source edition or verification state changes.

## Reporting rule

Every authoritative resistance-derived output shall show or export:

```text
R20 value
R20 unit
resistance basis
source reference
source revision
operating temperature
temperature coefficient basis
final corrected resistance
```

Percent differences between ideal bulk and a standard or product value shall be calculated from the actual evidenced values in the receipt. They shall not be hard-coded as universal percentages across conductor sizes.

## Acceptance gate

This refinement is complete only when:

1. no authoritative V10 segment derives finished-cable resistance from nominal area alone;
2. V6 and V9 publicly identify their ideal-bulk limitation;
3. a versioned standards or product resistance registry exists;
4. the selected evidence basis appears in calculation receipts and exported reports;
5. tests demonstrate that resistance, voltage drop and loss change correctly with the selected evidence case.
