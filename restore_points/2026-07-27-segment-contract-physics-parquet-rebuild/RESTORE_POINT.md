# Restore point — segment contract, physics and Parquet rebuild

Date: 2026-07-27
Branch: main
Starting commit: `54ffed8d29d799694082e4d60edb3e0e4fa42732`

This restore point was created after the first V8 lead-feasibility and actual-string-count
repair, and before changing the Python physics core, tests, segment architecture or build
pipeline.

## Current file blobs

- `v8-leapfrog/index.html`: `9243abf8cd1c6c7f0cdb79f32c5443ca45beb945`
- `v8-leapfrog/app.js`: `6df4d476d682a34b2ec30408a94bb7d9cdf04a65`
- `v8-leapfrog/model.js`: `93b9745e2be06d90f3a285e19173ee280f3c1390`
- `tests/v8-model.test.js`: `21ee51e1a2d780026e0b9066366d8c8ff4749c85`
- `src/solar_topology/formulas.py`: `5935bfaa900af22863b41786b967ea34948c2461`
- `src/solar_topology/topology.py`: `0c76e2bc7240c359fc33b2c2a5a31acc987c6351`
- `src/solar_topology/__init__.py`: `3bf98b31a46feb7e0169e56c020a8cb49d95d891`
- `tests/test_formulas.py`: `e4c2b1f96c3bf1c3fefdc9519e415d0e23010c80`
- `tests/test_topology.py`: `95be538c9f961de989e507b8dcc97426c6dd9c75`
- `pyproject.toml`: `a98e574f72cf7ca0c4842607128b48e02ca3962d`
- `.github/workflows/test.yml`: `141ee459ab61347937a7438516f7fa2b0dac3de2`
- `.github/workflows/v8-tests.yml`: `c86c5e2513d2d31437fa5d14a2155462176df87a`

## Recovery scope

Restore the above blobs or reset to the starting commit if the new physics, cartridge or
Parquet build fails. V6 and V7 executable files are outside this change and remain untouched.
