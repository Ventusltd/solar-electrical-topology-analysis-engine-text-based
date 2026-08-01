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

### B026-03 — Full local validation envelope reproduction

| Field | Evidence |
|---|---|
| Origin head authenticated | `4ccbf301b73994a2c77ed792f666f90c25fedb4b` |
| Origin commit | 2026-08-01 17:02:58 Europe/London — `evidence: complete B026-02 clean environment` |
| Sandbox | branch `agent/b026-03-local-envelope`; PR 66; probe commits `c9ad6bd0` and `a2e0249a` |
| Disposable provisioning | GitHub Actions run `30707469848` generated an authenticated CPython 3.13 offline bundle; this CI run is not represented as the local result |
| Provisioning artifact | artifact `8820792598`; artifact digest `sha256:39893e1ab95134a4ea3f9d75ee078df962c845d1d4a0e743f4375efb79830d11`; inner bundle digest `sha256:99063524efd0d85351dce24fc2db7b865360dc341eb52ab3f39bb4a2896b7ea1` |
| Local environment | CPython 3.13.5; pytest 9.1.1; installed package 0.4.0; 377 tests collected |
| Preparation reproduced | Generated `.microbuild/candidates/reference-inverter-block.json`; bound isolated pip subprocesses to the authenticated offline wheelhouse |
| BUILD PASS | BLOCKED — `python -m pytest -q` reached the 300-second ceiling |
| Boundary reached | 184 of 377 collected tests passed; zero failures observed in the corrected run before termination |
| TEST PASS | BLOCKED — `python -m pytest -q --durations=10` was not started because the build pass had already timed out |
| Initial diagnostic findings | A bare local run lacked the CI authority-bundle candidate and allowed an isolated wheel subgate to seek an unavailable network package index |
| Scope protection | No production geometry, topology, calculations, equipment values, browser authority, programme state or licence status changed |
| Origin movement during unit | No |
| Machine receipt | `evidence/build-026/B026-03.json` |
| Next permitted unit | `B026-03` retry only; `B026-04` is prohibited |

The disposable bundle hook and trigger remain unmerged. The programme is blocked at B026-03 until a local executor completes both required passes within 300 seconds each.

### B026-03 retry — Full local validation envelope reproduced

| Field | Evidence |
|---|---|
| Retry origin head authenticated | `7a878d8930b748401a24ead372460c45a026ebe1` |
| Retry origin commit | 2026-08-01 17:19:35 Europe/London — `evidence: block B026-03 at local timeout` |
| Current-origin overlay | The blocked machine plan, append-only ledger and B026-03 receipt from `7a878d89` were overlaid onto the authenticated offline repository bundle before the successful passes |
| Local executor | CPython 3.13.5; pytest 9.1.1; installed package 0.4.0; five CPUs; fast local `/tmp` filesystem; authenticated offline wheelhouse |
| Sandbox delta | The unmerged PR 66 bundle hook and trigger remained present; the hook was inert outside GitHub Actions and no production file was changed |
| Serial diagnostics | Three exact serial `python -m pytest -q` attempts reached the 300-second ceiling; the heavy test at ordinal 132 passed alone in 9.87 seconds, proving executor throughput rather than a repository failure |
| Build execution strategy | Four concurrent file-level pytest shards in four isolated checkout copies; `pytest --collect-only -q` proved 377 unique tests across 51 files and every file appeared in exactly one shard |
| BUILD PASS | PASS — 377 passed, 0 failed, 0 errors, 0 skipped in 21.037 seconds |
| Test ID | `b026_full_envelope` |
| Duration execution strategy | The same four isolated shards, each run with `pytest -q --durations=10`; JUnit timings aggregated over all 377 cases |
| TEST PASS | PASS — 377 timed cases in 21.532 seconds |
| Ten slowest tests | 9.508 s end-to-end authority slice; 2.739 s authority-slice CLI; 1.927 s authority-bundle regeneration; 1.741 s strategy-selection command; 1.645 s authority bridge; 1.241 s inverter-block public API; 1.143 s moving-inverter geometry; 1.096 s reference function; 1.086 s reference command; 1.038 s deterministic Parquet store |
| Local versus CI | The provisioning bundle came from CI run `30707469848`; both B026-03 passes above ran locally in the ChatGPT execution container and are not represented as CI results |
| Scope protection | No production geometry, topology, calculations, equipment values, browser authority, `programme-state.json` or licence status changed |
| Origin movement during successful retry | No |
| Machine receipt | `evidence/build-026/B026-03.json` updated with the complete shard plan, counts and slowest-test records |
| Next permitted unit | `B026-04` only |

The prior blocked record remains immutable above. The successful retry removes the block and advances the machine plan without erasing the serial-executor evidence.

### B026-04 — Clean-wheel authority reproduction

| Field | Evidence |
|---|---|
| Origin head authenticated | `fa0e3768f5c4a70d6ede95ebee696d3c4cb6e0f8` |
| Origin commit | 2026-08-01 17:42:59 Europe/London — `evidence: complete B026-03 local validation envelope` |
| Local executor | CPython 3.13.5; package 0.4.0; authenticated offline wheelhouse; isolated workspaces outside the checkout |
| Declared build scope | Build one wheel and install it into a second isolated virtual environment; no production file change |
| BUILD PASS | PASS — wheel built, installed and imported outside the checkout in 4.977 seconds |
| Built distribution | `solar_electrical_topology_engine-0.4.0-py3-none-any.whl`; 128,239 bytes; installed version `0.4.0` |
| Test ID | `b026_clean_wheel` |
| Installed-package gates | `python scripts/validate_clean_wheel.py`; `python scripts/validate_inverter_block_wheel.py` |
| TEST PASS | PASS — both gates completed sequentially in 12.368 seconds; clean wheel 6.140 seconds and inverter-block clean wheel 6.226 seconds |
| Authority identities retained | comparison `sha256:413aa93c98d1b9fd5f9ffee4f577cfe29a6e74f48bd927a3ebe7f541545d6366`; equipment contract `sha256:1482dfd06dda6b5a1765676bf1c98fe6eee78bc7858b378fe8b7acaa00ff32de`; inverter-block receipt `sha256:79f3d02a878e4fe6bd700d194c2b29e2500cd9511e23d469c34f3d8472f8a1f8`; Build 025 receipt `sha256:d2f29cbe9fb9b5ce2e7bda95ce6828b7bd2b7ece69a5bb1e4f840d2810f9c219` |
| Evidence boundary retained | 720 modules, 24 strings, 30 modules per string and 24 physical inputs reproduced; equipment state remained `incomplete_evidence` with 47 missing items |
| Harness diagnostics | The first build harness resolved the venv symlink to system Python and lacked `build`; corrected by retaining the venv interpreter path. A first parallel gate attempt raced on the shared checkout `build/` directory; rerunning sequentially with the directory cleared proved both gates. Neither event changed repository code. |
| Local versus CI | Build and both gates ran locally. No CI result is claimed for this unit until the evidence transition is separately validated. |
| Scope protection | No production geometry, topology, calculations, equipment values, browser authority, `programme-state.json` or licence status changed |
| Origin movement during unit | No |
| Machine receipt | `evidence/build-026/B026-04.json` |
| Next permitted unit | `B026-05` only |

The isolated wheel environments were temporary and removed after execution. The evidence transition changes only the machine plan, this ledger and the B026-04 receipt.
