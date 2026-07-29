import assert from 'node:assert/strict';
import test from 'node:test';

import { canonicalLeapfrogOrder, sequentialOrder } from '../src/topology.mjs';
import {
  buildLinearTerminalModules,
  buildModuleTerminalGeometry,
  deriveSeriesLeadConnections,
  validateLeadReach,
} from '../src/terminals.mjs';

const closeTo = (actual, expected, tolerance = 1e-9) => assert.ok(Math.abs(actual - expected) <= tolerance, `${actual} != ${expected}`);

test('terminal offsets rotate with the module', () => {
  const module = buildModuleTerminalGeometry({
    moduleNumber: 1,
    centreXMetres: 10,
    centreYMetres: 20,
    widthMetres: 1.3,
    heightMetres: 2.4,
    rotationDegrees: 90,
    junctionBoxOffsetXMetres: 0.2,
    junctionBoxOffsetYMetres: 0,
    positiveExitOffsetXMetres: 0.1,
    positiveExitOffsetYMetres: 0,
    negativeExitOffsetXMetres: -0.1,
    negativeExitOffsetYMetres: 0,
    positiveLeadLengthMetres: 1.4,
    negativeLeadLengthMetres: 1.4,
  });
  closeTo(module.terminals.positive.xMetres, 10);
  closeTo(module.terminals.positive.yMetres, 20.3);
  closeTo(module.terminals.negative.yMetres, 20.1);
});

test('lead reach passes at equality and fails below it', () => {
  const from = { xMetres: 0, yMetres: 0, leadLengthMetres: 0.6 };
  const to = { xMetres: 1, yMetres: 0, leadLengthMetres: 0.4 };
  assert.equal(validateLeadReach({ fromTerminal: from, toTerminal: to }).status, 'PASS');
  assert.equal(validateLeadReach({ fromTerminal: from, toTerminal: to, routingAllowanceMetres: 0.01 }).status, 'FAIL');
});

test('sequential and leapfrog are checked from terminal geometry, not centre-only totals', () => {
  const modules = buildLinearTerminalModules({
    moduleCount: 6,
    pitchMetres: 1.3,
    widthMetres: 1.3,
    heightMetres: 2.4,
    positiveLeadLengthMetres: 1.4,
    negativeLeadLengthMetres: 1.4,
    junctionBoxOffsetXMetres: 0,
    junctionBoxOffsetYMetres: 0,
    positiveExitOffsetXMetres: 0,
    positiveExitOffsetYMetres: 0,
    negativeExitOffsetXMetres: 0,
    negativeExitOffsetYMetres: 0,
  });
  const sequential = deriveSeriesLeadConnections(sequentialOrder(6), modules);
  const leapfrog = deriveSeriesLeadConnections(canonicalLeapfrogOrder(6), modules);
  assert.ok(sequential.every(item => item.feasible));
  assert.ok(leapfrog.some(item => !item.feasible));
  assert.equal(sequential.length, 5);
  assert.equal(leapfrog.length, 5);
});