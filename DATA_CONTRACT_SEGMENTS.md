# Topology Segment Data Contract

Status: binding contract for topology cartridges, shared physics and the
Parquet/DuckDB fleet store.

Schema version: `topology_segments_v1`

## Purpose

Every topology cartridge emits the same ordered conductor-segment table.
Sequential, leapfrog, mirrored, balanced-return and custom cartridges may create
different paths, but downstream calculations consume segments only.

No resistance, inductance, capacitance, loop-area, propagation or aggregation
function may branch on the topology name. If a calculation asks whether a string
is leapfrog, the cartridge boundary is wrong.

## Product

Ordered conductor-segment store for photovoltaic direct-current string
topologies.

## Authoritative output

`segments.parquet`

Fleet data is built in Python, written as zstd-compressed Parquet and queried with
DuckDB. The browser may consume small aggregates or one selected string. It is
not the authoritative fleet store.

## Grain

One row represents one physical conductor segment, for one string, under one
topology, in one model run.

A segment may have zero spatial displacement and positive conductor length. A
coiled surplus lead is the defining example.

## Key

The logical key is:

`topology + string_id + segment_index`

The production row also carries `run_id`, `inverter_id`, `mppt_id` and a stable
`segment_id` for snapshot and fleet auditability.

`segment_index` begins at one and is contiguous within each topology/string.

## Hive partitioning

The current segment store is partitioned by:

- `topology`
- `band`

Two initial cartridges across three bands create six useful partitions. Five
future cartridges across three bands create fifteen. Do not partition by inverter
or string: that would create thousands of small files. `inverter_id` remains a
queryable column.

Expected physical paths are:

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

`displacement_m` and `conductor_length_m` are intentionally separate. Route
summaries use displacement. Resistance and conductor-energy calculations use
conductor length.

## Required formation fields

| Field | Type | Meaning |
|---|---|---|
| `separation_mm` | double | Centre spacing to the returning conductor. |
| `formation` | string | Controlled conductor formation. |
| `installation_class` | string | Controlled installation environment. |

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

## Evidence and feasibility fields

| Field | Type | Meaning |
|---|---|---|
| `provenance` | string | Origin of the row's governing evidence. |
| `source_reference` | string | Generic evidence identifier. |
| `user_override` | boolean | Whether a generated/declared value changed. |
| `feasibility_status` | string | Cartridge feasibility result. |
| `saving_available` | boolean | Whether savings may be presented. |
| `warnings` | string | Deterministic warning-code list. |

Allowed provenance values are:

- `measured`
- `oem_declared`
- `assumed`
- `defaulted`

Provenance describes origin. It does not describe whether a standard requires a
value or whether a field solver is needed. Those belong to separate result fields.

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

For identical module and fleet inputs, every cartridge must preserve:

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
7. Final route lengths not reproduced by segment sums.
8. User-supplied final route lengths.
9. Factory-lead mismatch between cartridges.
10. Connector mismatch without explicit extension segments.
11. Savings emitted for an infeasible leapfrog cartridge.
12. Nondeterministic file hashes from identical inputs.

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

## Aggregates

The build writes:

- `data/topology/current/aggregates/strings.parquet`
- `data/topology/current/aggregates/mppts.parquet`
- `data/topology/current/aggregates/inverters.parquet`
- `data/topology/current/aggregates/site.parquet`
- `data/topology/current/aggregates/comparison.parquet`

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
