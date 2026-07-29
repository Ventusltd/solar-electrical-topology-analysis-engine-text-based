import test from 'node:test';
import assert from 'node:assert/strict';
import { buildCompleteInverterDocument } from '../src/inverter-block.mjs';

const base = {
  stringCount: 24,
  modulesPerString: 30,
  mpptCount: 12,
  inputsPerMppt: 2,
  modulePitchMetres: 1.303,
  rowSpacingMetres: 5,
  nearestHomeRunMetres: 10,
  homeRunStepMetres: 2,
  topology: 'leapfrog',
  resistanceOhmPerMetre: 0.00308,
  currentAmps: 17.35,
  moduleVocStcVolts: 45.9,
  betaVocPercentPerKelvin: -0.25,
  minimumCellTemperatureCelsius: -10,
};

test('builds one complete 24-string inverter allocation', () => {
  const result = buildCompleteInverterDocument(base);
  assert.equal(result.inverter.assignedStrings, 24);
  assert.equal(result.inverter.inputCapacity, 24);
  assert.equal(result.strings.length, 24);
  assert.equal(result.totals.conductors, 48);
  assert.equal(result.totals.modules, 720);
  assert.equal(result.strings[0].mpptNumber, 1);
  assert.equal(result.strings[0].inputNumber, 1);
  assert.equal(result.strings[1].mpptNumber, 1);
  assert.equal(result.strings[1].inputNumber, 2);
  assert.equal(result.strings[23].mpptNumber, 12);
  assert.equal(result.strings[23].inputNumber, 2);
});

test('keeps positive and negative field conductors separate', () => {
  const result = buildCompleteInverterDocument(base);
  for (const string of result.strings) {
    assert.ok(string.positiveCableMetres >= 0);
    assert.ok(string.negativeCableMetres >= string.positiveCableMetres);
    assert.equal(string.fieldCableMetres, string.positiveCableMetres + string.negativeCableMetres);
  }
});

test('rejects string allocation beyond MPPT capacity', () => {
  assert.throws(
    () => buildCompleteInverterDocument({ ...base, stringCount: 25 }),
    /exceeds declared MPPT input capacity/,
  );
});
