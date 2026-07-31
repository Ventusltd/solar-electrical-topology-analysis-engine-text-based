# Refinement 02 — Uncertainty and Numerical Stability

Timestamp: 2026-07-31 19:27 +0100

## Defect statement

`calculate_complete_circuit_with_uncertainty` can raise `ValueError` for exact inputs with no declared uncertainty. The failure occurs when the nominal total resistance and the exact interval boundary are mathematically equal but differ by one floating-point unit because they are accumulated in different orders.

The canonical steady-state calculation currently derives total resistance as:

```text
fsum(all conductor resistances) + fsum(all connector resistances)
```

The uncertainty layer derives an exact lower and upper boundary as:

```text
fsum(each segment conductor resistance + each segment connector resistance)
```

Floating-point addition is not associative. The two expressions can therefore differ by an ulp even though they represent the same physical quantity. The interval constructor then correctly enforces `lower <= nominal <= upper` and exposes the inconsistency.

This is a numerical-authority defect, not a legitimate uncertainty failure.

## Required correction

There shall be one authoritative ordered accumulation path for total circuit resistance.

Recommended implementation:

1. Calculate each segment's conductor resistance, connector resistance and total resistance once.
2. Preserve the independently reported conductor and connector subtotals.
3. Derive authoritative total resistance with:

```python
math.fsum(result.total_resistance_ohm for result in segment_results)
```

4. Use that same ordered segment-total accumulation in both the nominal and uncertainty engines.
5. For exact intervals, derive lower, nominal and upper through the same function and from the same ordered values.
6. Do not fix this defect by silently widening exact intervals or by applying an arbitrary decimal tolerance to the physical result.

The reported identity:

```text
total resistance = conductor subtotal + connector subtotal
```

may differ at machine precision if the two subtotals are separately accumulated. The receipt shall either:

- report the authoritative segment-total sum and treat the subtotal recombination difference as numerical residue; or
- canonicalise all three quantities through one documented decimal or binary quantisation rule before receipt hashing.

The first option is preferred because it preserves maximum numeric information.

## Interval construction rule

An exact interval means that the declared engineering input has zero stated uncertainty. It does not mean that separate floating-point algorithms may produce different nominal values.

`Interval.exact(value, unit)` shall continue to return identical lower, nominal and upper values.

Derived intervals shall satisfy the invariant structurally before construction. The interval class should not conceal inconsistent upstream accumulation.

Where conservative interval arithmetic produces an endpoint that differs from the independently calculated nominal only by representational residue, the calculation layer may normalise using a documented ulp-aware helper, for example:

```text
lower = min(calculated_lower, nominal)
upper = max(calculated_upper, nominal)
```

This fallback is permitted only after the common accumulation path is implemented and only when the difference is bounded by a small declared number of ulps. Any larger violation remains an error.

## Regression coverage

Add permanent tests over at least module counts 1 through 60, including the previously observed failing counts:

```text
10, 12, 14, 16, 25, 28, 29, 32, 36, 37, 43, 45, 57, 61
```

Where the current fixture or software limit prevents a listed count, create an equivalent deterministic circuit fixture with that number of repeated source segments.

Test both:

- exact operating current and exact string voltage;
- exact segment inputs with no `segment_intervals` overrides;
- sequential and leapfrog-compatible ordered circuit fixtures where applicable;
- zero connector resistance;
- non-zero connector resistance;
- mixed segment lengths and temperatures;
- large repeated segment counts sufficient to exercise cancellation and ulp boundaries.

## Required invariants

For every valid exact-input circuit:

```text
uncertain.nominal_receipt.total_resistance_ohm
    == uncertain.total_resistance_ohm.nominal

uncertain.total_resistance_ohm.lower
    <= uncertain.total_resistance_ohm.nominal
    <= uncertain.total_resistance_ohm.upper

uncertain.total_resistance_ohm.lower
    == uncertain.total_resistance_ohm.upper

uncertain.voltage_drop_v.lower
    == uncertain.voltage_drop_v.nominal
    == uncertain.voltage_drop_v.upper

uncertain.resistive_loss_w.lower
    == uncertain.resistive_loss_w.nominal
    == uncertain.resistive_loss_w.upper
```

For non-exact intervals:

- all nominal values must lie within their bounds;
- increasing any monotonic positive resistance input must not reduce an upper resistance bound;
- increasing current bounds must not reduce voltage-drop or loss bounds;
- receipt hashes must remain deterministic across repeated runs.

## Acceptance gate

The refinement is complete only when:

1. the formerly failing segment or module counts execute without exception;
2. the complete Python suite remains green;
3. a dedicated regression test proves that nominal and exact-interval totals use the same accumulation authority;
4. the numerical method is recorded in the uncertainty method version;
5. any changed receipt hashes are acknowledged as an intentional calculation-authority change.
