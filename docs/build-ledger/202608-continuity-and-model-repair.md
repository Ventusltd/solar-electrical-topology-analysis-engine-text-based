# Build 026 execution ledger

**Programme:** `build-026-continuity-and-model-repair-20260801`

**Governing Quantum Spawn:** [`../quantum-spawn/202608011536-build-026-forty-pass-small-step-law.md`](../quantum-spawn/202608011536-build-026-forty-pass-small-step-law.md)

**Machine plan:** [`../../build-plans/build-026-continuity-and-model-repair.json`](../../build-plans/build-026-continuity-and-model-repair.json)

**Nature:** Append-only execution evidence. This ledger is not constitutional law, programme activation or proof beyond the exact commands and boundaries recorded in each entry.

## Preparation record

| Field | Value |
|---|---|
| Prepared | 2026-08-01 15:36 Europe/London |
| Product Owner instruction head observed | `eb1e2c7db5c85306e476b6fa912ccc31a0148602` |
| Last fully validated engineering commit | `747381f6c3c3325a680a80a17e516268541c8548` |
| Programme status | Defined, pending activation |
| Next permitted unit | `B026-01` only |
| Required receipts | 20 BUILD PASS + 20 TEST PASS = 40 |
| Compute ceiling | 300 seconds per build pass and 300 seconds per test pass |
| Sandbox boundary | B026-01 through B026-05: no production changes; evidence-only records permitted |
| Build boundary | B026-06 through B026-20: one coherent repository change per unit |
| Quantum Spawn policy | One governing spawn now; two closing law spawns after B026-10 and B026-13 are proven; no capsule per routine unit |

## Required entry format

Each unit appends one section containing:

- unit identifier and title;
- origin head authenticated before work;
- branch or disposable sandbox identity;
- declared build scope and prohibited surfaces;
- BUILD PASS result and elapsed seconds;
- exact files changed or `none`;
- exact test identifier and command;
- TEST PASS result and elapsed seconds;
- local result versus CI result stated separately;
- resulting commit or patch hash where applicable;
- defects discovered or deferred;
- unresolved access or evidence;
- next permitted unit;
- explicit statement whether origin moved during the unit.

A failed or timed-out unit is recorded in the same format and blocks advancement.

## Unit records

### B026-01 — Mirror integrity and drift detection

| Field | Evidence |
|---|---|
| Origin head authenticated before successful repeat | `e4d5cb4dd185a5e596b37493d8715595c00c0209` |
| Origin commit | 2026-08-01 16:39:54 Europe/London — `test: restore TS-005 governance validation` |
| Mirror inventory | 363 tracked files; 97 branches; repository size 1,624 KB |
| Tracked-file method | 362 recorded at `37b00106`; `49ac61d7` added one file; later commits through the authenticated head renamed or modified files only |
| Sandbox | branch `agent/b026-01-mirror-integrity`; PR 61; marker `ecf176abcc94c690580be065f57c0583b7b8447a` |
| Declared build scope | Authenticate mirror identity and create one disposable non-merge validation marker |
| Prohibited surfaces | Production geometry, topology, calculations, equipment values, browser authority, `programme-state.json` and licence status |
| BUILD PASS | PASS — 35 seconds, conservatively measured from authenticated origin commit timestamp to marker commit timestamp |
| Sandbox files changed | `tests/b026-01-validation-marker.txt` only; production engineering files changed: none |
| Test ID | `b026_mirror_integrity` |
| Repository-controlled commands | `python scripts/check_capsule_links.py --check`; `python scripts/sync_programme_state.py --check` |
| TEST PASS | PASS — 123 seconds, GitHub Actions validate-job wall clock rounded up |
| Required gate result | Capsule-link integrity passed for 55 Markdown capsules; programme state and generated public outputs were in sync |
| Wider envelope | 377 Python tests passed; V8, V9, V10 JavaScript/Studio and clean installed-wheel gates passed |
| Workflow evidence | run `30706456207`; artifact `8820491476`; merge-test SHA `eae46e950dc97a626ce35539031b940ca4b2b67f`; artifact digest `sha256:c820661c1c167566549a68f3a82c954407cad86e4aa6211a8baae288430f90c8` |
| Local versus CI | No local result: the ChatGPT execution container could not resolve GitHub. CI result: PASS. No local result is represented as CI. |
| Abandoned first attempt | Run `30706087559` from `70ec8057` exposed two governance defects. Repair PR 62 passed run `30706296694` and merged as `e4d5cb4`; the first attempt was abandoned because origin moved. |
| Defects repaired | Stale terminal TS-005 assertions; missing validated receipt and MB-10 hand-off binding in the TS-005 closure |
| Origin movement during successful repeat | No |
| Machine receipt | `evidence/build-026/B026-01.json` |
| Next permitted unit | `B026-02` only |

The validation marker remains unmerged. The evidence transition changes only the machine plan, this ledger and the B026-01 receipt.

### B026-02 — Clean environment provisioning

| Field | Evidence |
|---|---|
| Origin head authenticated | `8b94aea9ba254acc837ed64fca6fafdb7b5a2339` |
| Origin commit | 2026-08-01 16:52:32 Europe/London — `evidence: complete B026-01 mirror integrity` |
| Sandbox | branch `agent/b026-02-clean-environment`; PR 64; probe commit `4c71b0a0ffb71fb696968773687f526b5e259f26` |
| Declared build scope | Create a fresh virtual environment outside the checkout and install the repository package through Python and pip |
| Prohibited surfaces | Production geometry, topology, calculations, equipment values, browser authority, `programme-state.json` and licence status |
| BUILD PASS | PASS — 99 seconds, measured from authenticated origin commit timestamp to disposable probe commit timestamp |
| Installation commands | `python -m venv <temporary>/venv`; `<temporary>/venv/bin/python -m pip install --disable-pip-version-check <repository-root>` |
| Sandbox files changed | `tests/test_b026_clean_environment.py` only; production engineering files changed: none |
| Test ID | `b026_clean_environment` |
| TEST PASS | PASS — 131 seconds, GitHub Actions validate-job wall clock rounded up |
| Probe result | Fresh environment created; package installed; `solar_topology` imported outside the checkout; installed distribution version `0.4.0` matched `pyproject.toml` version `0.4.0` |
| Hidden prerequisites | None discovered |
| Wider envelope | 378 Python tests passed in 96.03 seconds; V8, V9, V10 JavaScript/Studio and clean installed-wheel gates passed |
| Workflow evidence | run `30706950874`; artifact `8820641386`; merge-test SHA `5ec0f0275906a8a7a4fe2a3e27623c7de368d933`; artifact digest `sha256:2b0ce13f0cb830c68ef1a0fdf66bcf02a7221cf75cdc97ee2fe2495171efcad5` |
| Local versus CI | No independent local result was available from the ChatGPT execution container. CI result: PASS. No CI result is described as local. |
| Origin movement during unit | No |
| Machine receipt | `evidence/build-026/B026-02.json` |
| Next permitted unit | `B026-03` only |

The disposable clean-environment probe remains unmerged. The evidence transition changes only the machine plan, this ledger and the B026-02 receipt.
