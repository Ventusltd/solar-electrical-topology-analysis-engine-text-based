'use strict';
const assert = require('node:assert/strict');
const model = require('../v8-leapfrog/model.js');

const tests = model.runGoldenTests();
assert.equal(tests.allPassed, true, JSON.stringify(tests.tests, null, 2));

const study = model.calculate(model.DEFAULTS);
assert.equal(study.totals.stringsPerInverter, 24);
assert.ok(Math.abs(study.geometry.rowSpanM - 39.67) < 1e-9);
assert.ok(Math.abs(study.totals.sequentialExternalM - 2878.2) < 1e-9);
assert.ok(Math.abs(study.totals.leapfrogExternalM - 1926.12) < 1e-9);
assert.ok(Math.abs(study.totals.externalCableSavingM - 952.08) < 1e-9);
assert.ok(Math.abs(study.totals.fleetExternalCableSavingKm - 756.9036) < 1e-9);

const at30m = model.calculate({ ...model.DEFAULTS, inverterDistanceM: 30 });
assert.ok(Math.abs(at30m.totals.externalCableSavingM - study.totals.externalCableSavingM) < 1e-9);
assert.ok(at30m.totals.leapfrogExternalM > study.totals.leapfrogExternalM);

const west = study.strings.find((item) => item.face === 'W');
assert.ok(west);
assert.equal(west.sequential.positiveM, west.farRouteM);
assert.equal(west.sequential.negativeM, west.nearRouteM);
assert.equal(west.leapfrog.positiveM, west.nearRouteM);
assert.equal(west.leapfrog.negativeM, west.nearRouteM);

console.log(`V8 regression tests passed: ${tests.passed}/${tests.total}`);
