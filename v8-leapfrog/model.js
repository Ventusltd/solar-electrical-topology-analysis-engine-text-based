(function (root, factory) {
  'use strict';
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.V8LeapfrogModel = api;
})(typeof window !== 'undefined' ? window : globalThis, function () {
  'use strict';

  const VERSION = '8.1.0';
  const COPPER_ALPHA_20 = 0.00393;

  const DEFAULTS = Object.freeze({
    modulesPerString: 30,
    moduleWidthM: 1.303,
    alongRowGapM: 0.020,
    bandGapM: 0.500,
    eastBands: [5, 5, 2],
    westBands: [5, 5, 2],
    inverterDistanceM: 10,
    scenarioDistancesM: [10, 20, 30],
    polarityConvention: 'mirrored',
    cableR20MilliOhmPerM: 3.39,
    cableTemperatureC: 70,
    stringCurrentA: 17.35,
    moduleVmpV: 38.1,
    inverterCount: 795,
    installedCableRatePerM: 0,
    positiveFactoryLeadM: 0.350,
    negativeFactoryLeadM: 0.280,
    measuredLeapfrogSpanM: 0,
    leadEvidence: 'MANUFACTURER_STANDARD_NOT_AS_BUILT'
  });

  function asNumber(value, fallback) {
    const number = Number(value);
    return Number.isFinite(number) ? number : fallback;
  }

  function clampMin(value, minimum, fallback) {
    return Math.max(minimum, asNumber(value, fallback));
  }

  function parseNumberList(value, fallback) {
    const source = Array.isArray(value) ? value : String(value ?? '').split(',');
    const numbers = source
      .map((item) => Number(String(item).trim()))
      .filter((item) => Number.isFinite(item) && item >= 0);
    return numbers.length ? numbers : fallback.slice();
  }

  function parseBands(value, fallback) {
    return parseNumberList(value, fallback)
      .map((item) => Math.max(0, Math.round(item)))
      .filter((item) => item > 0);
  }

  function normalise(raw) {
    const input = raw || {};
    return {
      modulesPerString: Math.max(1, Math.round(asNumber(input.modulesPerString, DEFAULTS.modulesPerString))),
      moduleWidthM: clampMin(input.moduleWidthM, 0.001, DEFAULTS.moduleWidthM),
      alongRowGapM: clampMin(input.alongRowGapM, 0, DEFAULTS.alongRowGapM),
      bandGapM: clampMin(input.bandGapM, 0, DEFAULTS.bandGapM),
      eastBands: parseBands(input.eastBands, DEFAULTS.eastBands),
      westBands: parseBands(input.westBands, DEFAULTS.westBands),
      inverterDistanceM: clampMin(input.inverterDistanceM, 0, DEFAULTS.inverterDistanceM),
      scenarioDistancesM: parseNumberList(input.scenarioDistancesM, DEFAULTS.scenarioDistancesM),
      polarityConvention: input.polarityConvention === 'positive_near_both' ? 'positive_near_both' : 'mirrored',
      cableR20MilliOhmPerM: clampMin(input.cableR20MilliOhmPerM, 0, DEFAULTS.cableR20MilliOhmPerM),
      cableTemperatureC: asNumber(input.cableTemperatureC, DEFAULTS.cableTemperatureC),
      stringCurrentA: clampMin(input.stringCurrentA, 0, DEFAULTS.stringCurrentA),
      moduleVmpV: clampMin(input.moduleVmpV, 0.001, DEFAULTS.moduleVmpV),
      inverterCount: Math.max(1, Math.round(asNumber(input.inverterCount, DEFAULTS.inverterCount))),
      installedCableRatePerM: clampMin(input.installedCableRatePerM, 0, DEFAULTS.installedCableRatePerM),
      positiveFactoryLeadM: clampMin(input.positiveFactoryLeadM, 0, DEFAULTS.positiveFactoryLeadM),
      negativeFactoryLeadM: clampMin(input.negativeFactoryLeadM, 0, DEFAULTS.negativeFactoryLeadM),
      measuredLeapfrogSpanM: clampMin(input.measuredLeapfrogSpanM, 0, DEFAULTS.measuredLeapfrogSpanM),
      leadEvidence: String(input.leadEvidence || DEFAULTS.leadEvidence)
    };
  }

  function rowSpanM(input) {
    return input.modulesPerString * input.moduleWidthM +
      Math.max(0, input.modulesPerString - 1) * input.alongRowGapM;
  }

  function cableResistancePerM(input) {
    return input.cableR20MilliOhmPerM / 1000 *
      (1 + COPPER_ALPHA_20 * (input.cableTemperatureC - 20));
  }

  function sequentialPolarities(face, nearM, farM, convention) {
    if (convention === 'mirrored' && face === 'W') {
      return { positiveM: farM, negativeM: nearM };
    }
    return { positiveM: nearM, negativeM: farM };
  }

  function buildStrings(input, distanceOverrideM) {
    const rowM = rowSpanM(input);
    const bandPitchM = rowM + input.bandGapM;
    const distanceM = distanceOverrideM == null
      ? input.inverterDistanceM
      : Math.max(0, Number(distanceOverrideM));
    const faces = [
      { face: 'E', bands: input.eastBands },
      { face: 'W', bands: input.westBands }
    ];
    const strings = [];
    let number = 1;

    for (const definition of faces) {
      definition.bands.forEach((count, bandIndex) => {
        const bandOffsetM = bandIndex * bandPitchM;
        const nearM = distanceM + bandOffsetM;
        const farM = nearM + rowM;
        const seq = sequentialPolarities(
          definition.face,
          nearM,
          farM,
          input.polarityConvention
        );

        for (let rank = 1; rank <= count; rank += 1) {
          const resistanceSavedOhm = rowM * cableResistancePerM(input);
          const voltageDropSavedV = input.stringCurrentA * resistanceSavedOhm;
          const stringVmpV = input.modulesPerString * input.moduleVmpV;
          strings.push({
            number,
            stringId: `${definition.face}${bandIndex + 1}-${String(rank).padStart(2, '0')}`,
            positiveId: `${number}+`,
            negativeId: `${number}−`,
            face: definition.face,
            band: bandIndex + 1,
            rank,
            bandOffsetM,
            inverterDistanceM: distanceM,
            nearRouteM: nearM,
            farRouteM: farM,
            rowSpanM: rowM,
            basePairM: 2 * nearM,
            sequential: {
              positiveM: seq.positiveM,
              negativeM: seq.negativeM,
              totalExternalM: seq.positiveM + seq.negativeM,
              additionalRowReturnM: rowM
            },
            leapfrog: {
              positiveM: nearM,
              negativeM: nearM,
              totalExternalM: 2 * nearM,
              additionalRowReturnM: 0
            },
            saving: {
              externalCableM: rowM,
              resistanceOhmPerString: resistanceSavedOhm,
              voltageDropVPerString: voltageDropSavedV,
              voltageDropPercentOfStringVmp: stringVmpV > 0 ? 100 * voltageDropSavedV / stringVmpV : 0,
              powerLossWPerString: input.stringCurrentA * input.stringCurrentA * resistanceSavedOhm,
              installedCostPerString: rowM * input.installedCableRatePerM
            }
          });
          number += 1;
        }
      });
    }
    return strings;
  }

  function leadFeasibility(input) {
    const availableCombinedLeadM = input.positiveFactoryLeadM + input.negativeFactoryLeadM;
    if (!(input.measuredLeapfrogSpanM > 0)) {
      return {
        status: 'UNRESOLVED',
        availableCombinedLeadM,
        requiredMeasuredSpanM: null,
        marginM: null,
        evidence: input.leadEvidence,
        message: 'Enter the measured connector-to-connector leapfrog span before making a feasibility verdict.'
      };
    }
    const marginM = availableCombinedLeadM - input.measuredLeapfrogSpanM;
    return {
      status: marginM >= 0 ? 'PASSES_LENGTH_SCREEN' : 'FAILS_LENGTH_SCREEN',
      availableCombinedLeadM,
      requiredMeasuredSpanM: input.measuredLeapfrogSpanM,
      marginM,
      evidence: input.leadEvidence,
      message: marginM >= 0
        ? 'Combined lead length exceeds the entered routed span. Bend radius, support and slack still require review.'
        : 'Combined lead length is shorter than the entered routed span.'
    };
  }

  function calculate(raw, distanceOverrideM) {
    const input = normalise(raw);
    const strings = buildStrings(input, distanceOverrideM);
    const rowM = rowSpanM(input);
    const rPerM = cableResistancePerM(input);
    const totals = strings.reduce((acc, string) => {
      acc.sequentialExternalM += string.sequential.totalExternalM;
      acc.leapfrogExternalM += string.leapfrog.totalExternalM;
      acc.externalCableSavingM += string.saving.externalCableM;
      acc.powerLossSavingW += string.saving.powerLossWPerString;
      acc.installedCostSaving += string.saving.installedCostPerString;
      return acc;
    }, {
      sequentialExternalM: 0,
      leapfrogExternalM: 0,
      externalCableSavingM: 0,
      powerLossSavingW: 0,
      installedCostSaving: 0
    });

    const exemplar = strings[0] || null;
    return {
      modelVersion: VERSION,
      formulaId: 'v8-1-sequential-versus-leapfrog-external-cable',
      input,
      geometry: {
        modulePitchM: input.moduleWidthM + input.alongRowGapM,
        rowSpanM: rowM,
        bandPitchM: rowM + input.bandGapM
      },
      electrical: {
        cableResistance20OhmPerM: input.cableR20MilliOhmPerM / 1000,
        cableResistanceOperatingOhmPerM: rPerM,
        stringVmpV: input.modulesPerString * input.moduleVmpV,
        resistanceSavingOhmPerString: exemplar ? exemplar.saving.resistanceOhmPerString : 0,
        voltageDropSavingVPerString: exemplar ? exemplar.saving.voltageDropVPerString : 0,
        voltageDropSavingPercentOfStringVmp: exemplar ? exemplar.saving.voltageDropPercentOfStringVmp : 0,
        powerLossSavingWPerString: exemplar ? exemplar.saving.powerLossWPerString : 0
      },
      totals: {
        stringsPerInverter: strings.length,
        ...totals,
        fleetSequentialExternalKm: totals.sequentialExternalM * input.inverterCount / 1000,
        fleetLeapfrogExternalKm: totals.leapfrogExternalM * input.inverterCount / 1000,
        fleetExternalCableSavingKm: totals.externalCableSavingM * input.inverterCount / 1000,
        fleetPowerLossSavingKWAtEnteredCurrent: totals.powerLossSavingW * input.inverterCount / 1000,
        fleetInstalledCostSaving: totals.installedCostSaving * input.inverterCount
      },
      leadFeasibility: leadFeasibility(input),
      strings
    };
  }

  function scenarioStudies(raw) {
    const input = normalise(raw);
    return input.scenarioDistancesM.map((distanceM) => {
      const study = calculate(input, distanceM);
      return {
        distanceM,
        stringsPerInverter: study.totals.stringsPerInverter,
        sequentialExternalM: study.totals.sequentialExternalM,
        leapfrogExternalM: study.totals.leapfrogExternalM,
        externalCableSavingM: study.totals.externalCableSavingM,
        fleetExternalCableSavingKm: study.totals.fleetExternalCableSavingKm,
        inverterPowerLossSavingKW: study.totals.powerLossSavingW / 1000,
        fleetPowerLossSavingKW: study.totals.fleetPowerLossSavingKWAtEnteredCurrent
      };
    });
  }

  function nearlyEqual(actual, expected, tolerance) {
    return Math.abs(actual - expected) <= tolerance;
  }

  function runGoldenTests() {
    const study = calculate(DEFAULTS);
    const study30 = calculate({ ...DEFAULTS, inverterDistanceM: 30 });
    const west = study.strings.find((string) => string.face === 'W');
    const tests = [
      {
        name: 'Default row span is 39.67 m',
        pass: nearlyEqual(study.geometry.rowSpanM, 39.67, 1e-9),
        actual: study.geometry.rowSpanM,
        expected: 39.67
      },
      {
        name: 'Default topology contains 24 strings',
        pass: study.totals.stringsPerInverter === 24,
        actual: study.totals.stringsPerInverter,
        expected: 24
      },
      {
        name: 'Saving is one row span per string',
        pass: study.strings.every((string) => nearlyEqual(string.saving.externalCableM, study.geometry.rowSpanM, 1e-9)),
        actual: study.strings[0]?.saving.externalCableM,
        expected: study.geometry.rowSpanM
      },
      {
        name: 'Default saving is 952.08 m per inverter',
        pass: nearlyEqual(study.totals.externalCableSavingM, 952.08, 1e-6),
        actual: study.totals.externalCableSavingM,
        expected: 952.08
      },
      {
        name: 'Saving is independent of inverter distance',
        pass: nearlyEqual(study.totals.externalCableSavingM, study30.totals.externalCableSavingM, 1e-9),
        actual: study30.totals.externalCableSavingM,
        expected: study.totals.externalCableSavingM
      },
      {
        name: 'West sequential polarity is mirrored',
        pass: Boolean(west && west.sequential.positiveM === west.farRouteM && west.sequential.negativeM === west.nearRouteM),
        actual: west ? `${west.sequential.positiveM}/${west.sequential.negativeM}` : 'missing',
        expected: west ? `${west.farRouteM}/${west.nearRouteM}` : 'west string'
      },
      {
        name: 'Leapfrog places both external terminals at the near route',
        pass: study.strings.every((string) => string.leapfrog.positiveM === string.nearRouteM && string.leapfrog.negativeM === string.nearRouteM),
        actual: study.strings[0] ? `${study.strings[0].leapfrog.positiveM}/${study.strings[0].leapfrog.negativeM}` : 'missing',
        expected: study.strings[0]?.nearRouteM
      }
    ];
    return {
      version: VERSION,
      passed: tests.filter((test) => test.pass).length,
      total: tests.length,
      allPassed: tests.every((test) => test.pass),
      tests
    };
  }

  return Object.freeze({
    VERSION,
    DEFAULTS,
    COPPER_ALPHA_20,
    normalise,
    rowSpanM,
    cableResistancePerM,
    buildStrings,
    calculate,
    scenarioStudies,
    leadFeasibility,
    runGoldenTests
  });
});
