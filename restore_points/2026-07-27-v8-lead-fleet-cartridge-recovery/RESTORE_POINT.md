# Restore point — V8 lead, fleet and cartridge recovery

Date: 2026-07-27
Branch: main

Created before applying the recovery order agreed after comparing V6, V7, V8, the federation repository and `data-gb-electricity`.

## Current pre-change references

- `v8-leapfrog/index.html` blob: `b9d0ffbc52a15524da0a03c8b911d6d87b54bf8d`
- `v8-leapfrog/app.js` blob: `812fcde5f71b42519a22704b5d4c80570c475656`
- `v8-leapfrog/model.js` blob: `cb05d7f9ffc7ca146ece4c599c40c7086aea3ccc`
- Binding recovery instructions commit: `529085eaca7319c7947e787180e80658609bf49f`

## Recovery scope

The next changes are limited to V8 and its tests/documentation:

1. reformat V8 source into human-readable normal-width code;
2. derive leapfrog reach from two module pitches unless measured route evidence overrides it;
3. gate all claimed leapfrog savings when the factory leads fail;
4. calculate fleet quantities from actual total site string count rather than archetype inverter count;
5. preserve V6 and V7 untouched;
6. prepare, but do not yet pretend to complete, the Parquet/DuckDB cartridge migration.
