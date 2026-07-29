# V6–V10 Capability Migration Ledger

## Purpose

This ledger is the control document for recovering engineering capability from historical browser versions, the Python package and sandbox branches into one authoritative V10 engine. It records capability, source, evidence, recovery state and destination. It is not a feature wish list.

## Status codes

- `UNKNOWN` — repository evidence not yet inspected.
- `FOUND` — implementation located but not characterised.
- `TESTED` — implementation runs under an existing test.
- `PARTIAL` — some required behaviour exists.
- `RECOVER` — suitable implementation should be migrated.
- `REWRITE` — concept retained but implementation should be replaced.
- `QUARANTINE` — retain for research only; do not expose as authoritative.
- `AUTHORITATIVE` — selected implementation with passing validation.
- `ABSENT` — no implementation found after inspection.

## Known computation paths

| Path | Present understanding | Initial treatment |
|---|---|---|
| Python package under `src/solar_topology/` | Uses `pint`; contains temperature-corrected formulae; current tests reported as 35 pass and 1 exact-float failure | Leading candidate for authoritative steady-state kernel |
| V10 JavaScript kernel | Current tests reported as 12 pass; lacks temperature correction | Characterise and compare; do not assume authority |
| V9 JavaScript path | Current tests reported as 10 pass | Recover capabilities not present in Python or V10 |
| V8 JavaScript path | Current tests reported as 1 pass | Historical evidence and regression source |
| Terminal-geometry branch | Current tests reported as 17 pass and 1 fail | Recover physical terminal geometry after failure analysis |
| `b9-sandbox` | Legitimate historical sandbox | Preserve and inspect; do not rename as an error |

## Core ledger

| ID | Capability | Candidate source | Current state | Required evidence | Intended destination | Next action |
|---|---|---|---|---|---|---|
| MIG-OBJ-001 | Module object | Python/V8/V9/V10 | UNKNOWN | schema, tests, sample model | canonical object schema | inspect all paths |
| MIG-OBJ-002 | Factory positive and negative leads | terminal geometry/V9 | PARTIAL | dimensions, polarity, terminal ordering | canonical lead objects | inspect terminal branch |
| MIG-OBJ-003 | Connector and mating pair | terminal geometry/Python | UNKNOWN | resistance, compatibility, graph behaviour | canonical connector objects | locate implementation |
| MIG-OBJ-004 | String object | all paths | FOUND | complete series traversal test | canonical topology | compare schemas |
| MIG-OBJ-005 | String wiring harness | historical sandboxes | UNKNOWN | branch/trunk graph fixture | canonical harness objects | search repository |
| MIG-OBJ-006 | Field string cable | all paths | FOUND | ordered route and conductor schedule | canonical conductor object | compare data models |
| MIG-OBJ-007 | MPPT input | V9/V10/Python | FOUND | independent-input fixture | canonical topology | confirm boundary rules |
| MIG-OBJ-008 | Common DC bus | Python/research | UNKNOWN | backfeed fixture | canonical topology | locate or implement |
| MIG-OBJ-009 | Tray/duct/trench route segment | sandboxes/research | UNKNOWN | installation environment schema | route cartridge | search repository |
| MIG-OBJ-010 | Tracker moving section | terminal geometry/research | UNKNOWN | swept path and bend test | route cartridge | inspect branch |
| MIG-GEO-001 | Module pitch and placement | browser/terminal branch | FOUND | dimensional fixture | physical geometry service | characterise |
| MIG-GEO-002 | Sequential wiring geometry | browser/terminal branch | FOUND | known-length fixture | topology geometry generator | test against dimensions |
| MIG-GEO-003 | Leapfrog wiring geometry | browser/terminal branch | FOUND | exact identity and known layout | topology geometry generator | recover and validate |
| MIG-GEO-004 | Ordered conductor route | Python/V9 | UNKNOWN | complete positive/negative traversal | canonical topology | locate implementation |
| MIG-GEO-005 | Loop separation geometry | research engine | FOUND | impedance benchmark | distributed cartridge | preserve separately |
| MIG-TOP-001 | Terminal graph | Python/terminal branch | FOUND | graph validation tests | canonical topology kernel | compare implementations |
| MIG-TOP-002 | Series traversal | Python/JS | FOUND | module-to-inverter fixture | canonical topology kernel | select authority |
| MIG-TOP-003 | Parallel aggregation | Python/JS | UNKNOWN | harness/combiner fixture | canonical topology kernel | inspect |
| MIG-TOP-004 | Reverse-current paths | research/standards | UNKNOWN | common-bus and parallel-string fixtures | protection cartridge | implement after topology |
| MIG-TOP-005 | Topology validation | JS/Python | PARTIAL | open, short, polarity and duplicate-terminal tests | canonical topology kernel | inventory current checks |
| MIG-STEADY-001 | Conductor resistance | Python/JS | TESTED | unit and known-answer tests | steady-state kernel | compare numerical results |
| MIG-STEADY-002 | Temperature correction | Python | TESTED | tolerance-based regression | steady-state kernel | retain and validate |
| MIG-STEADY-003 | Connector resistance | Python/research | UNKNOWN | complete-circuit benchmark | steady-state kernel | locate or add |
| MIG-STEADY-004 | Voltage drop | Python/JS | FOUND | segment and circuit benchmarks | steady-state kernel | reconcile formulae |
| MIG-STEADY-005 | Power loss | Python/JS | FOUND | segment and circuit benchmarks | steady-state kernel | reconcile formulae |
| MIG-STEADY-006 | Material totals | browser/JS | UNKNOWN | conductor schedule sum | reporting kernel | inspect |
| MIG-STEADY-007 | Maximum string voltage | Python/JS | UNKNOWN | edition-specific method tests | standards/voltage cartridge | separate physics and compliance |
| MIG-STEADY-008 | Minimum MPPT voltage | Python/JS | UNKNOWN | hot-condition fixture | voltage cartridge | inspect |
| MIG-STEADY-009 | Current-carrying capacity | Python/JS | UNKNOWN | installation-method trace | cable cartridge | inspect provenance |
| MIG-PROT-001 | String OCPD decision | JS/Python | UNKNOWN | parallel-string equation tests | protection cartridge | locate |
| MIG-PROT-002 | Grouped-string protection | absent/research | UNKNOWN | evidence-gated fixture | protection cartridge | implement later |
| MIG-PROT-003 | SPD location objects | research | UNKNOWN | route-linked fixture | protection/topology | implement after route model |
| MIG-PROT-004 | SPD electrical distance | distributed model | PARTIAL | route/impedance benchmark | transient/protection cartridge | recover separately |
| MIG-INS-001 | Insulation resistance | research/Python | UNKNOWN | wet/dry aggregate model | insulation cartridge | locate or design |
| MIG-INS-002 | Capacitance to earth | distributed model | FOUND | geometry and boundary benchmark | transient/common-mode cartridge | recover and validate |
| MIG-TRANS-001 | Per-unit-length RLC | research engine | FOUND | analytical benchmark | distributed kernel | preserve |
| MIG-TRANS-002 | Characteristic impedance | research engine | FOUND | analytical benchmark | distributed kernel | preserve |
| MIG-TRANS-003 | Propagation velocity and delay | research engine | FOUND | round-trip benchmark | distributed kernel | preserve |
| MIG-TRANS-004 | Reflection coefficients | research engine | FOUND | open/matched/capacitive tests | distributed kernel | preserve |
| MIG-TRANS-005 | Arc interruption/restrike scenarios | research engine | FOUND | validity statement and benchmark | research cartridge | QUARANTINE until validated |
| MIG-TRANS-006 | 8/20 µs surge sharing | research engine | FOUND | length sweep regression | research cartridge | QUARANTINE until validated |
| MIG-EVID-001 | Units | Python `pint` | TESTED | dimensional tests | all kernels | retain as mandatory |
| MIG-EVID-002 | Input provenance | partial docs | PARTIAL | schema and report trace | evidence layer | implement canonical enum |
| MIG-EVID-003 | Assumptions | research reports | PARTIAL | machine-readable schema | evidence layer | implement |
| MIG-EVID-004 | Standards references | capability matrix | FOUND | versioned cartridge schema | evidence layer | implement |
| MIG-EVID-005 | Uncertainty | research reports | PARTIAL | propagation method | evidence layer | design |
| MIG-EVID-006 | Validation state | tests/docs | PARTIAL | result schema | evidence layer | implement |
| MIG-REP-001 | Conductor schedule | browser/JS/Python | UNKNOWN | complete circuit report | reporting kernel | inspect |
| MIG-REP-002 | Engineering report | historical outputs | UNKNOWN | reproducible fixture | reporting kernel | inventory |
| MIG-REP-003 | Machine-readable result | Python/JS | UNKNOWN | canonical JSON schema | reporting kernel | define schema |
| MIG-UI-001 | Browser drawing | V10 | TESTED | UI tests | browser client | freeze pending kernel |
| MIG-UI-002 | Browser calculations | V8/V9/V10 | FOUND | capability comparison | remove or call kernel | prevent hidden formulae |

## First repository inspection pass

For each row marked `UNKNOWN`, record:

1. exact file path;
2. symbol or function name;
3. input and output shape;
4. units treatment;
5. tests covering it;
6. known defects;
7. external dependencies;
8. whether it is browser-coupled;
9. recovery decision;
10. destination interface.

## Authority decision rules

A capability may become `AUTHORITATIVE` only when:

- its inputs and outputs are explicit;
- units are enforced;
- topology prerequisites are validated;
- at least one known-answer test passes;
- at least one regression fixture exists;
- numerical tolerance is justified;
- assumptions and validity boundaries are recorded;
- no browser state is required for correct calculation;
- duplicated implementations have been reconciled.

## Immediate defect queue

| Defect | Treatment |
|---|---|
| Python exact-float test failure | inspect expected mathematical identity; replace exact equality with justified tolerance only where appropriate |
| Terminal-geometry single failure | reproduce, classify as implementation or test-fixture fault, then repair without weakening geometry invariants |
| V10 JS temperature correction absent | do not patch browser first; recover authoritative temperature-corrected calculation in kernel and expose through interface |
| Reboot documentation omits Python engine | correct documentation before further architectural decisions |
| Three computation paths undocumented | inventory and compare before deleting or consolidating anything |

## Completion condition

This ledger is complete when every engineering calculation visible anywhere in V6–V10 or the Python package has been assigned one of: recover, rewrite, quarantine, authoritative or deliberately retired, with repository evidence and tests recorded.
