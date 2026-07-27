# How We Solved the Topology Issues

Newest entries appear first. Each entry records what changed, what was added, why,
how it is verified and what remains unresolved.

## 2026-07-27 — Segment cartridges and a deterministic Parquet fleet store

### What changed

The topology mode is no longer allowed to leak into downstream calculations.
Sequential and leapfrog are now cartridges that emit the same ordered segment
rows. Resistance, inductance, capacitance, delay, aggregation and export operate
on those rows rather than asking which topology created them.

The fleet model moved out of the browser. Python generates segments and DuckDB
writes a zstd-compressed Hive-partitioned Parquet store by topology and band.
The browser contract is reduced to site aggregates and one selected string.

### What was added

- `DATA_CONTRACT_SEGMENTS.md`
- `src/solar_topology/segments.py`
- `src/solar_topology/cartridges.py`
- `src/solar_topology/parquet_store.py`
- `scripts/build_topology_store.py`
- cartridge, physics and Parquet tests
- deterministic double-build and SHA-256 comparison
- string, MPPT, inverter, site and topology-comparison aggregates

### Why

A browser JSON blob is suitable for 24 strings but not for approximately two
million or more segment rows. Partitioned Parquet keeps the row grain while
allowing fleet aggregation by SQL. The cartridge boundary also prevents every
new topology from monkey-patching the physics and renderer.

### Verification

The data law checks keys, segment order, node continuity, non-negative lengths,
provenance, declared conductor envelopes, pair geometry, factory-lead equality,
connector equality and feasibility-gated savings.

The complete candidate store is generated twice into separate temporary
directories. Relative paths and file hashes must be byte-identical before an
output is published.

### Known gap

The current factory-lead coordinates are not a measured three-dimensional lead
route. Factory lead rows therefore carry real conductor length and resistance but
are excluded from closed-form pair L/C totals until geometry is measured or a
validated higher-order model is provided.

The sequential far-end return is represented as a real single-pole conductor
segment, but its full loop inductance and pickup area still require a matching
return-path geometry. It is not silently forced through a two-wire formula.

## 2026-07-27 — The physics snapshots were wrong

### What changed

Two existing tests were deleted as authorities:

- the test that derived a 6 mm² conductor diameter from nominal area;
- the test that derived finished-cable resistance from bulk copper resistivity.

The tests were wrong because they pinned synthetic values rather than declared
finished-cable properties. Fixing the code was supposed to make them fail.

### What was added

- declared 4 mm² and 6 mm² conductor records;
- an envelope-fill validation;
- a velocity identity invariant;
- a declared complete-circuit canary;
- explicit separation of external and internal inductance.

### Why

Nominal cross-sectional area identifies a conductor size. It is not a measured
metallic disk from which the stranded envelope diameter or finished-cable
resistance should be recreated.

Characteristic impedance and propagation velocity are high-frequency external
field properties. Including the low-frequency internal inductance violates the
TEM identity and makes the calculated velocity slower than the dielectric permits.

### Verification

For every valid two-wire geometry:

`v = 1 / sqrt(L_external_per_length * C_per_length)`

must equal:

`1 / sqrt(mu0 * epsilon0 * epsilon_r)`

The geometry term cancels exactly. Internal inductance remains separate for
low-frequency stored energy and lumped `L di/dt` work.

The complete-circuit canary uses declared per-metre resistances, separate cable
temperatures and 62 connector contacts. It is labelled as a worst-case compliant
budget rather than a prediction of a field resistance measurement.

### Known gap

Frequency-dependent conductor resistance and proximity effect remain future
work. They shall be added after the segment store is stable and must not restore
internal inductance to the propagation calculation.

## 2026-07-27 — Leapfrog savings became feasibility-gated

### What changed

V8 now distinguishes theoretical savings from physically available savings.
Leapfrog no longer assumes factory leads are long enough.

### What was added

- positive and negative factory-lead inputs;
- optional measured routed span;
- required reach, available reach, margin and extension shortfall;
- refusal to display an available saving when the length screen fails;
- actual site string count as the fleet multiplier.

### Why

The topology can save one external row-return conductor only when the factory
leads can make the skip connection without added extensions. Factory copper is
already in the complete series circuit whether it is coiled or deployed, so it
must remain invariant across cartridges.

Multiplying a per-inverter saving by inverter count silently assumes every
inverter is full. The fleet saving must be the per-string saving multiplied by the
actual number of strings.

### Verification

With a 1.323 m module pitch, the default conservative screen requires 2.646 m of
combined lead reach. Two 1.2 m leads fail by 0.246 m. Two 1.4 m leads pass by
0.154 m.

The cartridge invariant asserts identical factory-lead conductor totals and
ordinary connector counts under sequential and leapfrog modes. Only external or
explicit extension segments may differ.

### Known gap

The two-module-pitch rule is a screening geometry, not an as-built measurement.
A measured routed connector-to-connector span overrides it with provenance.

## 2026-07-27 — Line width was identified as the editing failure

### What changed

V8 was split into normal-width HTML, CSS, model and application files. Active new
Python, JavaScript, HTML, CSS, tests and workflows are checked against a
100-character line limit.

### Why

A line containing several thousand characters turns a one-number edit into a
whole-block replacement and makes human review impossible. The failure was code
shape, not the difficulty of the electrical model.

### Verification

`scripts/check_line_lengths.py` fails continuous integration when an active source
line exceeds the declared limit.

### Known gap

The root V6 and V7 comparison applications still contain legacy wide-line code.
They are deliberately frozen rather than reformatted and risked during this
rebuild. New work must not copy that style.

## 2026-07-27 — Python became authoritative without breaking V6 and V7

### What changed

The corrected shared physics and fleet calculations live in Python and DuckDB.
V6 and V7 remain comparison deployments while the browser-result interface is
built.

### Why

Deleting the JavaScript physics immediately would break working comparison pages
before they can consume generated Python artefacts. Maintaining two evolving
physics implementations would be worse.

### Verification

New segment and fleet work imports the Python package. V8 fleet outputs are built
from the Parquet store. Existing V6 and V7 files are not the authority for new
physics.

### Known gap

The legacy JavaScript physics is not yet deleted. Its removal is gated on V6/V7
reading a versioned generated result artefact or being formally retired. No new
formula correction may be implemented independently in both languages.

## Research gates retained

The following remain non-executable research until measured or otherwise
validated:

- frequency-dependent water-film participation;
- device selection from unmeasured glass-glass wet capacitance;
- full common-mode earth-return impedance at high frequency;
- PEEC treatment of irregular coils and transitions;
- OEM inverter termination impedance versus frequency;
- quantitative mutual coupling across dense string groups.

A warning label is not an adequate gate. A research-only model must refuse to
emit a device specification or compliance conclusion.
