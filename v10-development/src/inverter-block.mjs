import { runKernel } from './kernel.mjs';

export const INVERTER_BLOCK_SCHEMA = 'globalgrid2050.solar-dc-computation.v10.inverter-block.1';

function positiveInteger(value, name) {
  if (!Number.isInteger(value) || value < 1) throw new TypeError(`${name} must be a positive integer`);
}

function finiteNonNegative(value, name) {
  if (!Number.isFinite(value) || value < 0) throw new TypeError(`${name} must be finite and non-negative`);
}

function finitePositive(value, name) {
  if (!Number.isFinite(value) || value <= 0) throw new TypeError(`${name} must be finite and positive`);
}

export function buildCompleteInverterDocument(input) {
  positiveInteger(input.stringCount, 'stringCount');
  positiveInteger(input.modulesPerString, 'modulesPerString');
  positiveInteger(input.mpptCount, 'mpptCount');
  positiveInteger(input.inputsPerMppt, 'inputsPerMppt');
  if (input.stringCount > input.mpptCount * input.inputsPerMppt) {
    throw new RangeError('stringCount exceeds declared MPPT input capacity');
  }
  finitePositive(input.modulePitchMetres, 'modulePitchMetres');
  finiteNonNegative(input.rowSpacingMetres, 'rowSpacingMetres');
  finiteNonNegative(input.nearestHomeRunMetres, 'nearestHomeRunMetres');
  finiteNonNegative(input.homeRunStepMetres, 'homeRunStepMetres');
  finitePositive(input.resistanceOhmPerMetre, 'resistanceOhmPerMetre');
  finiteNonNegative(input.currentAmps, 'currentAmps');

  const strings = Array.from({ length: input.stringCount }, (_, index) => {
    const stringNumber = index + 1;
    const mpptNumber = Math.floor(index / input.inputsPerMppt) + 1;
    const inputNumber = (index % input.inputsPerMppt) + 1;
    const yMetres = index * input.rowSpacingMetres;
    const homeRunMetres = input.nearestHomeRunMetres + index * input.homeRunStepMetres;
    const kernel = runKernel({
      documentId: `string-${String(stringNumber).padStart(2, '0')}`,
      layout: {
        moduleCount: input.modulesPerString,
        pitchMetres: input.modulePitchMetres,
        topology: input.topology,
      },
      electrical: {
        resistanceOhmPerMetre: input.resistanceOhmPerMetre,
        resistanceProvenance: 'datasheet',
        resistanceEvidenceStatus: 'candidate',
        currentAmps: input.currentAmps,
        currentProvenance: 'datasheet',
        currentEvidenceStatus: 'candidate',
        circuitFactor: 1,
        vocStcVolts: input.moduleVocStcVolts,
        betaVocPercentPerKelvin: input.betaVocPercentPerKelvin,
        minimumCellTemperatureKelvin: input.minimumCellTemperatureCelsius + 273.15,
        temperatureProvenance: 'assumed',
        temperatureEvidenceStatus: 'candidate',
      },
    });

    const internalSeriesPathMetres = kernel.geometry.pathLengthMetres;
    const terminalSeparationMetres = kernel.geometry.terminalSeparationMetres;
    const positiveCableMetres = homeRunMetres;
    const negativeCableMetres = homeRunMetres + terminalSeparationMetres;
    const fieldCableMetres = positiveCableMetres + negativeCableMetres;
    const totalConductorMetres = internalSeriesPathMetres + fieldCableMetres;
    const totalResistanceOhms = totalConductorMetres * input.resistanceOhmPerMetre;
    const voltageDropVolts = input.currentAmps * totalResistanceOhms;
    const powerLossWatts = input.currentAmps ** 2 * totalResistanceOhms;

    return {
      id: `STR-${String(stringNumber).padStart(2, '0')}`,
      stringNumber,
      mpptNumber,
      inputNumber,
      yMetres,
      modulesPerString: input.modulesPerString,
      topology: input.topology,
      moduleOrder: kernel.geometry.order,
      moduleCoordinates: kernel.geometry.coordinates.map((module) => ({
        ...module,
        yMetres,
      })),
      internalSeriesPathMetres,
      terminalSeparationMetres,
      positiveCableMetres,
      negativeCableMetres,
      fieldCableMetres,
      totalConductorMetres,
      totalResistanceOhms,
      voltageDropVolts,
      powerLossWatts,
      coldStringVocVolts: kernel.results.voltageLimits?.stringVocCold.value ?? null,
      evidenceStatus: 'candidate',
      warning: 'Field cable lengths are geometry candidates until actual routes and terminal positions are drawn.',
    };
  });

  const totals = strings.reduce((acc, string) => {
    acc.modules += string.modulesPerString;
    acc.positiveCableMetres += string.positiveCableMetres;
    acc.negativeCableMetres += string.negativeCableMetres;
    acc.fieldCableMetres += string.fieldCableMetres;
    acc.internalSeriesPathMetres += string.internalSeriesPathMetres;
    acc.totalConductorMetres += string.totalConductorMetres;
    acc.powerLossWatts += string.powerLossWatts;
    return acc;
  }, {
    strings: input.stringCount,
    conductors: input.stringCount * 2,
    modules: 0,
    positiveCableMetres: 0,
    negativeCableMetres: 0,
    fieldCableMetres: 0,
    internalSeriesPathMetres: 0,
    totalConductorMetres: 0,
    powerLossWatts: 0,
  });

  return {
    schemaVersion: INVERTER_BLOCK_SCHEMA,
    inverter: {
      id: 'INV-01',
      mpptCount: input.mpptCount,
      inputsPerMppt: input.inputsPerMppt,
      inputCapacity: input.mpptCount * input.inputsPerMppt,
      assignedStrings: input.stringCount,
    },
    strings,
    totals,
    warnings: [
      'Candidate drawing model: not a construction design or compliance conclusion.',
      'Home-run lengths are generated from editable geometric assumptions until the routes are explicitly drawn.',
      'Protection, insulation monitoring and transient calculations are intentionally excluded until independently proven.',
    ],
  };
}
