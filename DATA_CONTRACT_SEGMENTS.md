# Topology Segment Data Contract

Status: binding contract for topology cartridges, shared physics and the
Parquet/DuckDB fleet store.

Schema version: `topology_segments_v1`

## Purpose

Every topology cartridge emits the same ordered conductor-segment table.
Sequential, leapfrog, mirrored, balanced-return and custom cartridges may create
different paths, but every downstream calculation consumes segments only.

No resistance, inductance, capacitance, loop-area, propagation or aggregation
function may branch on the topology name. If a calculation asks whether a string
is leapfrog, the cartridge boundary is wrong.

## Product and authoritative output

Product: ordered conductor-segment store for photovoltaic direct-current string
topologies.

Authoritative table: `segments.parquet`

Fleet data is built in Python, written as zstd-compressed Parquet and queried with
DuckDB. The browser may consume small aggregates or one selected string. It is
not the authoritative fleet store.

## Grain and key

Grain: one row per physical conductor segment, per string, per topology
cartridge, per model run.

Logical key:

`topology + string_id + segment_index`

The production row also carries `run_id`, `inverter_id`, `mppt_id` and a stable
`segment_id`. `segment_index` begins at one and is contiguous within every
string and topology.

A segment may have zero spatial displacement and positive conductor length. A
coiled surplus lead is the defining example.

## Hive partitioning

The current fleet store is partitioned by:

- `topology`
- `band`

Two initial cartridges across three bands create six useful partitions. Five
future cartridges across three bands create fifteen. Do not partition by
inverter or string because that would create thousands of small files.
`inverter_id` remains a queryable column.

Expected paths include:

`data/topology/current/segments/topology=sequential/band=1/data_0.parquet`

`data/topology/current/segments/topology=leapfrog/band=1/data_0.parquet`

## Required identity fields

| Field | Type | Meaning |
|---|---|---|
| `run_id` | string | Deterministic identifier for canonical inputs. |
| `schema_version` | string | Segment-contract version. |
| `topology` | string | Cartridge name and partition key. |
| `band` | integer | One-based distance band and partition key. |
| `cartridge_version` | string | Cartridge semantic version. |
| `inverter_id` | integer | One-based fleet inverter identifier. |
| `mppt_id` | integer | One-based tracker-input identifier. |
| `string_id` | string | Stable string identifier within a topology. |
| `segment_index` | integer | One-based ordered position in the circuit. |
| `segment_id` | string | Stable topology/string/index identifier. |

## Required electrical-role fields

| Field | Type | Meaning |
|---|---|---|
| `segment_type` | string | Controlled segment type. |
| `polarity` | string | `positive`, `negative`, `series` or `none`. |
| `from_node_id` | string | Electrical start node. |
| `to_node_id` | string | Electrical end node. |
| `module_id` | string or null | Associated module where applicable. |

## Required geometry fields

All coordinate and length values are stored in metres.

| Field | Type | Meaning |
|---|---|---|
| `from_x` | double | Start x in slope/world coordinates. |
| `from_y` | double | Start y in slope/world coordinates. |
| `from_z` | double | Start z in slope/world coordinates. |
| `to_x` | double | End x in slope/world coordinates. |
| `to_y` | double | End y in slope/world coordinates. |
| `to_z` | double | End z in slope/world coordinates. |
| `displacement_m` | double | Geometric start-to-end displacement. |
| `conductor_length_m` | double | Actual conductor represented by the row. |

`displacement_m` and `conductor_length_m` are deliberately separate. Route
summaries use displacement. Resistance and conductor-energy calculations use
conductor length.

## Required formation fields

| Field | Type | Meaning |
|---|---|---|
| `separation_mm` | double | Centre spacing to the returning conductor. |
| `formation` | string | Controlled conductor formation. |
| `installation_class` | string | Controlled installation environment. |
| `loop_parameter_weight` | double | Row share of one two-wire loop model. |
| `effective_epsilon_r` | double | Effective dielectric value for that model. |

`loop_parameter_weight` is between zero and one. A positive and negative
home-run row normally carry 0.5 each so the pair is counted once. A row with
unresolved return geometry carries zero and a warning; it must not silently
enter the closed-form two-wire sum.

Initial formations are:

- `touching_pair`
- `spaced_pair`
- `single_pole`
- `bundled`

## Required conductor fields

| Field | Type | Meaning |
|---|---|---|
| `conductor_product_id` | string | Controlled generic product identifier. |
| `conductor_csa_mm2` | double | Nominal identifying size only. |
| `conductor_diameter_mm` | double | Declared stranded envelope diameter. |
| `cable_od_mm` | double | Declared complete cable outside diameter. |
| `r20_ohm_per_m` | double | Declared finished-cable resistance at 20 C. |
| `temperature_c` | double | Segment operating temperature. |

Nominal cross-sectional area must never be used to invent conductor diameter or
finished-cable resistance. Those are independent declared or measured fields.

## Coil and connector fields

| Field | Type | Meaning |
|---|---|---|
| `coil_turns` | double or null | Coil turns where modelled. |
| `coil_diameter_mm` | double or null | Coil diameter where modelled. |
| `connector_count` | integer | Series contacts attributed to the row. |
| `connector_resistance_ohm_each` | double | Resistance per contact before temperature correction. |

Connector resistance belongs to the row that owns the contacts. A global
connector multiplier is not an authoritative substitute.

## Evidence and feasibility fields

| Field | Type | Meaning |
|---|---|---|
| `provenance` | string | Origin of the row's governing evidence. |
| `source_reference` | string | Generic evidence identifier. |
| `user_override` | boolean | Whether a generated or declared value changed. |
| `feasibility_status` | string | Cartridge feasibility result. |
| `saving_available` | boolean | Whether savings may be presented. |
| `warnings` | string | Deterministic warning-code list. |

Allowed provenance values are:

- `measured`
- `oem_declared`
- `assumed`
- `defaulted`

Provenance describes where a value came from. It does not describe whether a
standard requires it or whether a field solver is needed. Those are separate
method-status fields in later result schemas.

## Controlled segment types

Initial segment types are:

- `module_factory_positive_lead`
- `module_factory_negative_lead`
- `module_interconnect`
- `string_turnaround`
- `external_positive_home_run`
- `external_negative_home_run`
- `external_sequential_row_return`
- `extension_lead`
- `coiled_surplus`
- `structure_drop`
- `surface_route`
- `trench_route`
- `inverter_approach`
- `termination_allowance`

New segment types require a schema revision and fixtures.

## Installation classes

Initial classes are:

- `under_module`
- `frame_adjacent`
- `open_air`
- `metallic_tray`
- `insulating_tray`
- `conduit`
- `duct`
- `direct_buried`
- `wet_trench`
- `floodable`
- `structure_transition`
- `enclosure_entry`
- `unknown`

`unknown` is permitted only with an explicit warning.

## Cartridge interface

Every cartridge exposes:

1. `name`
2. `version`
3. `feasibility(inputs)`
4. `build_segments(inputs, string_definition)`
5. `manifest(inputs, segments)`

Cartridges emit segments and no electrical totals.

Initial cartridges are:

- `sequential`
- `leapfrog`

Future cartridges are:

- `mirrored`
- `balanced_return`
- `custom`

## Cross-cartridge invariants

For identical module and fleet inputs, every cartridge preserves:

- module count;
- string-voltage basis;
- factory positive-lead conductor total;
- factory negative-lead conductor total;
- ordinary module connector count;
- conductor material and declared product values.

Only topology-dependent external and explicit extension segments may differ.

The following data laws are hard failures:

1. Null or empty key fields.
2. Duplicate logical keys.
3. Non-contiguous segment indices.
4. Discontinuous electrical node chains.
5. Negative conductor lengths.
6. Invalid provenance values.
7. Invalid loop weights or connector resistance.
8. Final route lengths not reproduced by segment sums.
9. User-supplied final route lengths.
10. Factory-lead mismatch between cartridges.
11. Connector mismatch without explicit extension segments.
12. Savings emitted for an infeasible leapfrog cartridge.
13. Nondeterministic file hashes from identical inputs.

## Conductor-envelope validation

The nominal envelope fill is:

`fill = nominal_csa / (pi * declared_diameter^2 / 4)`

It must lie between 70% and 95%. A value outside that range indicates a likely
units mistake or incompatible datasheet input.

## Physics boundary

Shared physics may derive segment or aggregate results for:

- operating resistance;
- voltage-drop contribution;
- I-squared-R loss contribution;
- external differential inductance;
- low-frequency internal inductance;
- differential capacitance;
- common-mode capacitance estimate;
- loop-area contribution;
- propagation-delay contribution;
- evidence and validity flags.

Characteristic impedance and propagation velocity use external inductance only.
Internal inductance remains available separately for low-frequency energy and
lumped `L di/dt` work.

The current cartridge store deliberately excludes unresolved factory-lead and
single-pole return geometry from closed-form pair L/C totals. Those rows still
carry real conductor length and resistance. Their inductance, pickup area and
mutual coupling require measured geometry or a validated higher-order model.

## Manifest contract

Every topology manifest contains:

- `schema_version`
- `cartridge_name`
- `cartridge_version`
- `method_version`
- `source_commit`
- `input_hash`
- `segment_row_count`
- `distinct_string_count`
- `first_segment_key`
- `last_segment_key`
- `parquet_files`
- `parquet_sha256`
- `feasibility_status`
- `warning_count`
- `data_law_result`

Deterministic manifests exclude uncontrolled wall-clock timestamps.

## Aggregates and browser slices

The build writes:

- `data/topology/current/aggregates/strings.parquet`
- `data/topology/current/aggregates/mppts.parquet`
- `data/topology/current/aggregates/inverters.parquet`
- `data/topology/current/aggregates/site.parquet`
- `data/topology/current/aggregates/comparison.parquet`
- `data/topology/current/browser/site-summary.json`
- `data/topology/current/browser/selected-string.json`

The JSON files are small presentation artefacts generated from the Parquet truth
store. They are not a second calculation implementation.

## Test classification

Every check is classified as one of:

- **Invariant:** a law that holds for every valid input.
- **Canary:** one settled worked example with a declared tolerance.
- **Floor:** a growing quantity that may rise but must not fall below a baseline.

Segment rows, Parquet file count, store size, string count and inverter count are
floors, not permanent snapshot equalities.

## Overwrite and determinism law

A rebuild rewrites each complete touched topology partition. It never appends
blindly. Rows are sorted before DuckDB `COPY`, output uses zstd compression, and
the complete build is produced twice in temporary directories. Relative paths and
SHA-256 hashes must be byte-identical.

## Versioning obligation

Any browser, report or asset register consuming this contract creates a public
interface obligation. Breaking field changes require a schema-version increment,
a decision-log entry and an explicit migration note.
