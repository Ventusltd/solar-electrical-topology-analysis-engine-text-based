(function attachModel(root, factory) {
  'use strict';

  const api = factory();

  if (typeof module === 'object' && module.exports) {
    module.exports = api;
  }

  if (root) {
    root.V8LeapfrogModel = api;
  }
})(
  typeof window !== 'undefined' ? window : globalThis,
  function buildModel() {
    'use strict';

    const VERSION = '8.2.0';
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
      totalSiteStringCount: 18_918,
      installedCableRatePerM: 0,
      positiveFactoryLeadM: 0.350,
      negativeFactoryLeadM: 0.280,
      measuredLeapfrogSpanM: 0,
      leadEvidence: 'MANUFACTURER_STANDARD_NOT_AS_BUILT'
    });

    function asNumber(value, fallback) {
      const parsed = Number(value);
      return Number.isFinite(parsed) ? parsed : fallback;
    }

    function atLeast(value, minimum, fallback) {
      return Math.max(minimum, asNumber(value, fallback));
    }

    function parseNumberList(value, fallback) {
      const source = Array.isArray(value)
        ? value
        : String(value ?? '').split(',');

      const values = source
        .map((item) => Number(String(item).trim()))
        .filter((item) => Number.isFinite(item) && item >= 0);

      return values.length ? values : fallback.slice();
    }

    function parseBands(value, fallback) {
      return parseNumberList(value, fallback)
        .map((item) => Math.max(0, Math.round(item)))
        .filter((item) => item > 0);
    }

    function normalise(raw = {}) {
      return {
        modulesPerString: Math.max(
          1,
          Math.round(
            asNumber(
              raw.modulesPerString,
              DEFAULTS.modulesPerString
            )
          )
        ),
        moduleWidthM: atLeast(
          raw.moduleWidthM,
          0.001,
          DEFAULTS.moduleWidthM
        ),
        alongRowGapM: atLeast(
          raw.alongRowGapM,
          0,
          DEFAULTS.alongRowGapM
        ),
        bandGapM: atLeast(
          raw.bandGapM,
          0,
          DEFAULTS.bandGapM
        ),
        eastBands: parseBands(
          raw.eastBands,
          DEFAULTS.eastBands
        ),
        westBands: parseBands(
          raw.westBands,
          DEFAULTS.westBands
        ),
        inverterDistanceM: atLeast(
          raw.inverterDistanceM,
          0,
          DEFAULTS.inverterDistanceM
        ),
        scenarioDistancesM: parseNumberList(
          raw.scenarioDistancesM,
          DEFAULTS.scenarioDistancesM
        ),
        polarityConvention:
          raw.polarityConvention === 'positive_near_both'
            ? 'positive_near_both'
            : 'mirrored',
        cableR20MilliOhmPerM: atLeast(
          raw.cableR20MilliOhmPerM,
          0,
          DEFAULTS.cableR20MilliOhmPerM
        ),
        cableTemperatureC: asNumber(
          raw.cableTemperatureC,
          DEFAULTS.cableTemperatureC
        ),
        stringCurrentA: atLeast(
          raw.stringCurrentA,
          0,
          DEFAULTS.stringCurrentA
        ),
        moduleVmpV: atLeast(
          raw.moduleVmpV,
          0.001,
          DEFAULTS.moduleVmpV
        ),
        inverterCount: Math.max(
          1,
          Math.round(
            asNumber(raw.inverterCount, DEFAULTS.inverterCount)
          )
        ),
        totalSiteStringCount: Math.max(
          1,
          Math.round(
            asNumber(
              raw.totalSiteStringCount,
              DEFAULTS.totalSiteStringCount
            )
          )
        ),
        installedCableRatePerM: atLeast(
          raw.installedCableRatePerM,
          0,
          DEFAULTS.installedCableRatePerM
        ),
        positiveFactoryLeadM: atLeast(
          raw.positiveFactoryLeadM,
          0,
          DEFAULTS.positiveFactoryLeadM
        ),
        negativeFactoryLeadM: atLeast(
          raw.negativeFactoryLeadM,
          0,
          DEFAULTS.negativeFactoryLeadM
        ),
        measuredLeapfrogSpanM: atLeast(
          raw.measuredLeapfrogSpanM,
          0,
          DEFAULTS.measuredLeapfrogSpanM
        ),
        leadEvidence: String(
          raw.leadEvidence || DEFAULTS.leadEvidence
        )
      };
    }

    function modulePitchM(input) {
      return input.moduleWidthM + input.alongRowGapM;
    }

    function rowSpanM(input) {
      return (
        input.modulesPerString * input.moduleWidthM +
        Math.max(0, input.modulesPerString - 1) *
          input.alongRowGapM
      );
    }

    function cableResistancePerM(input) {
      const r20 = input.cableR20MilliOhmPerM / 1000;
      const temperatureFactor =
        1 + COPPER_ALPHA_20 * (input.cableTemperatureC - 20);

      return r20 * temperatureFactor;
    }

    function sequentialPolarities(
      face,
      nearRouteM,
      farRouteM,
      convention
    ) {
      if (convention === 'mirrored' && face === 'W') {
        return {
          positiveM: farRouteM,
          negativeM: nearRouteM
        };
      }

      return {
        positiveM: nearRouteM,
        negativeM: farRouteM
      };
    }

    function leadFeasibility(raw = {}) {
      const input = normalise(raw);
      const geometricReachM = 2 * modulePitchM(input);
      const measuredOverride = input.measuredLeapfrogSpanM > 0;
      const requiredReachM = measuredOverride
        ? input.measuredLeapfrogSpanM
        : geometricReachM;
      const availableLeadReachM =
        input.positiveFactoryLeadM +
        input.negativeFactoryLeadM;
      const marginM = availableLeadReachM - requiredReachM;
      const feasible = marginM >= 0;
      const extensionRequiredM = Math.max(0, -marginM);

      return {
        status: feasible
          ? 'FEASIBLE_LENGTH_SCREEN'
          : 'INFEASIBLE_LENGTH_SCREEN',
        feasible,
        basis: measuredOverride
          ? 'MEASURED_ROUTED_SPAN'
          : 'TWO_MODULE_PITCH_SCREEN',
        geometricReachM,
        requiredReachM,
        availableLeadReachM,
        marginM,
        extensionRequiredM,
        evidence: input.leadEvidence,
        message: feasible
          ? (
              'Factory leads pass the length screen. ' +
              'Bend radius, connector orientation, support and slack ' +
              'still require verification.'
            )
          : (
              'Factory leads fail the length screen. ' +
              `Shortfall: ${extensionRequiredM.toFixed(3)} m. ` +
              'Any extension would add connector interfaces and must ' +
              'be engineered separately.'
            )
      };
    }

    function buildStrings(raw = {}, distanceOverrideM) {
      const input = normalise(raw);
      const rowM = rowSpanM(input);
      const bandPitchM = rowM + input.bandGapM;
      const distanceM = distanceOverrideM == null
        ? input.inverterDistanceM
        : Math.max(
            0,
            asNumber(
              distanceOverrideM,
              input.inverterDistanceM
            )
          );
      const rPerM = cableResistancePerM(input);
      const lead = leadFeasibility(input);
      const strings = [];
      const faces = [
        {
          face: 'E',
          bands: input.eastBands
        },
        {
          face: 'W',
          bands: input.westBands
        }
      ];
      let number = 1;

      for (const definition of faces) {
        definition.bands.forEach((count, bandIndex) => {
          const bandOffsetM = bandIndex * bandPitchM;
          const nearRouteM = distanceM + bandOffsetM;
          const farRouteM = nearRouteM + rowM;
          const sequential = sequentialPolarities(
            definition.face,
            nearRouteM,
            farRouteM,
            input.polarityConvention
          );

          for (let rank = 1; rank <= count; rank += 1) {
            const resistanceSavingOhm = rowM * rPerM;
            const voltageDropSavingV =
              input.stringCurrentA * resistanceSavingOhm;
            const stringVmpV =
              input.modulesPerString * input.moduleVmpV;
            const powerLossSavingW =
              input.stringCurrentA *
              input.stringCurrentA *
              resistanceSavingOhm;

            strings.push({
              number,
              stringId:
                `${definition.face}${bandIndex + 1}-` +
                String(rank).padStart(2, '0'),
              positiveId: `${number}+`,
              negativeId: `${number}−`,
              face: definition.face,
              band: bandIndex + 1,
              rank,
              bandOffsetM,
              inverterDistanceM: distanceM,
              nearRouteM,
              farRouteM,
              rowSpanM: rowM,
              basePairM: 2 * nearRouteM,
              sequential: {
                positiveM: sequential.positiveM,
                negativeM: sequential.negativeM,
                totalExternalM:
                  sequential.positiveM +
                  sequential.negativeM,
                additionalRowReturnM: rowM
              },
              leapfrog: {
                positiveM: nearRouteM,
                negativeM: nearRouteM,
                totalExternalM: 2 * nearRouteM,
                additionalRowReturnM: 0,
                feasible: lead.feasible
              },
              saving: {
                theoreticalExternalCableM: rowM,
                availableExternalCableM:
                  lead.feasible ? rowM : null,
                theoreticalResistanceOhmPerString:
                  resistanceSavingOhm,
                availableResistanceOhmPerString:
                  lead.feasible ? resistanceSavingOhm : null,
                theoreticalVoltageDropVPerString:
                  voltageDropSavingV,
                availableVoltageDropVPerString:
                  lead.feasible ? voltageDropSavingV : null,
                voltageDropPercentOfStringVmp:
                  stringVmpV > 0
                    ? 100 * voltageDropSavingV / stringVmpV
                    : 0,
                theoreticalPowerLossWPerString:
                  powerLossSavingW,
                availablePowerLossWPerString:
                  lead.feasible ? powerLossSavingW : null,
                theoreticalInstalledCostPerString:
                  rowM * input.installedCableRatePerM,
                availableInstalledCostPerString:
                  lead.feasible
                    ? rowM * input.installedCableRatePerM
                    : null
              }
            });

            number += 1;
          }
        });
      }

      return strings;
    }

    function sumStrings(strings) {
      return strings.reduce(
        (totals, string) => {
          totals.sequentialExternalM +=
            string.sequential.totalExternalM;
          totals.leapfrogExternalM +=
            string.leapfrog.totalExternalM;
          totals.theoreticalSavingM +=
            string.saving.theoreticalExternalCableM;
          totals.theoreticalPowerLossSavingW +=
            string.saving.theoreticalPowerLossWPerString;
          totals.theoreticalInstalledCostSaving +=
            string.saving.theoreticalInstalledCostPerString;

          return totals;
        },
        {
          sequentialExternalM: 0,
          leapfrogExternalM: 0,
          theoreticalSavingM: 0,
          theoreticalPowerLossSavingW: 0,
          theoreticalInstalledCostSaving: 0
        }
      );
    }

    function calculate(raw = {}, distanceOverrideM) {
      const input = normalise(raw);
      const lead = leadFeasibility(input);
      const strings = buildStrings(input, distanceOverrideM);
      const rowM = rowSpanM(input);
      const rPerM = cableResistancePerM(input);
      const archetype = sumStrings(strings);
      const firstString = strings[0] || null;
      const siteSavingM =
        rowM * input.totalSiteStringCount;
      const sitePowerLossSavingW =
        (firstString
          ? firstString.saving.theoreticalPowerLossWPerString
          : 0) * input.totalSiteStringCount;
      const siteInstalledCostSaving =
        rowM *
        input.totalSiteStringCount *
        input.installedCableRatePerM;

      return {
        modelVersion: VERSION,
        formulaId:
          'v8-2-sequential-versus-leapfrog-external-cable',
        input,
        feasibility: lead,
        geometry: {
          modulePitchM: modulePitchM(input),
          rowSpanM: rowM,
          bandPitchM: rowM + input.bandGapM,
          requiredLeapfrogReachM: lead.requiredReachM
        },
        electrical: {
          cableResistance20OhmPerM:
            input.cableR20MilliOhmPerM / 1000,
          cableResistanceOperatingOhmPerM: rPerM,
          stringVmpV:
            input.modulesPerString * input.moduleVmpV,
          theoreticalResistanceSavingOhmPerString:
            firstString
              ? firstString.saving
                  .theoreticalResistanceOhmPerString
              : 0,
          availableResistanceSavingOhmPerString:
            lead.feasible && firstString
              ? firstString.saving
                  .theoreticalResistanceOhmPerString
              : null,
          theoreticalVoltageDropSavingVPerString:
            firstString
              ? firstString.saving
                  .theoreticalVoltageDropVPerString
              : 0,
          availableVoltageDropSavingVPerString:
            lead.feasible && firstString
              ? firstString.saving
                  .theoreticalVoltageDropVPerString
              : null,
          voltageDropSavingPercentOfStringVmp:
            firstString
              ? firstString.saving
                  .voltageDropPercentOfStringVmp
              : 0,
          theoreticalPowerLossSavingWPerString:
            firstString
              ? firstString.saving
                  .theoreticalPowerLossWPerString
              : 0,
          availablePowerLossSavingWPerString:
            lead.feasible && firstString
              ? firstString.saving
                  .theoreticalPowerLossWPerString
              : null
        },
        totals: {
          stringsPerArchetypeInverter: strings.length,
          totalSiteStringCount: input.totalSiteStringCount,
          averageSiteStringsPerInverter:
            input.totalSiteStringCount / input.inverterCount,
          sequentialExternalMPerArchetypeInverter:
            archetype.sequentialExternalM,
          leapfrogExternalMPerArchetypeInverter:
            archetype.leapfrogExternalM,
          theoreticalSavingMPerArchetypeInverter:
            archetype.theoreticalSavingM,
          availableSavingMPerArchetypeInverter:
            lead.feasible
              ? archetype.theoreticalSavingM
              : null,
          theoreticalSiteSavingKm:
            siteSavingM / 1000,
          availableSiteSavingKm:
            lead.feasible
              ? siteSavingM / 1000
              : null,
          theoreticalPowerLossSavingWPerArchetypeInverter:
            archetype.theoreticalPowerLossSavingW,
          availablePowerLossSavingWPerArchetypeInverter:
            lead.feasible
              ? archetype.theoreticalPowerLossSavingW
              : null,
          theoreticalSitePowerLossSavingKW:
            sitePowerLossSavingW / 1000,
          availableSitePowerLossSavingKW:
            lead.feasible
              ? sitePowerLossSavingW / 1000
              : null,
          theoreticalSiteInstalledCostSaving:
            siteInstalledCostSaving,
          availableSiteInstalledCostSaving:
            lead.feasible
              ? siteInstalledCostSaving
              : null
        },
        strings
      };
    }

    function scenarioStudies(raw = {}) {
      const input = normalise(raw);

      return input.scenarioDistancesM.map((distanceM) => {
        const study = calculate(input, distanceM);

        return {
          distanceM,
          feasible: study.feasibility.feasible,
          basePairMPerArchetypeInverter:
            study.totals
              .leapfrogExternalMPerArchetypeInverter,
          sequentialExternalMPerArchetypeInverter:
            study.totals
              .sequentialExternalMPerArchetypeInverter,
          leapfrogExternalMPerArchetypeInverter:
            study.totals
              .leapfrogExternalMPerArchetypeInverter,
          theoreticalSavingMPerArchetypeInverter:
            study.totals
              .theoreticalSavingMPerArchetypeInverter,
          availableSavingMPerArchetypeInverter:
            study.totals
              .availableSavingMPerArchetypeInverter,
          theoreticalSiteSavingKm:
            study.totals.theoreticalSiteSavingKm,
          availableSiteSavingKm:
            study.totals.availableSiteSavingKm,
          theoreticalPowerLossSavingKWPerArchetypeInverter:
            study.totals
              .theoreticalPowerLossSavingWPerArchetypeInverter /
            1000,
          availablePowerLossSavingKWPerArchetypeInverter:
            study.totals
              .availablePowerLossSavingWPerArchetypeInverter ==
            null
              ? null
              : study.totals
                  .availablePowerLossSavingWPerArchetypeInverter /
                1000
        };
      });
    }

    function nearlyEqual(actual, expected, tolerance = 1e-9) {
      return Math.abs(actual - expected) <= tolerance;
    }

    function testResult(name, pass, actual, expected) {
      return {
        name,
        pass,
        actual,
        expected
      };
    }

    function runGoldenTests() {
      const defaultStudy = calculate(DEFAULTS);
      const distance30Study = calculate({
        ...DEFAULTS,
        inverterDistanceM: 30
      });
      const leads12Study = calculate({
        ...DEFAULTS,
        positiveFactoryLeadM: 1.2,
        negativeFactoryLeadM: 1.2
      });
      const leads14Study = calculate({
        ...DEFAULTS,
        positiveFactoryLeadM: 1.4,
        negativeFactoryLeadM: 1.4
      });
      const westString = defaultStudy.strings.find(
        (string) => string.face === 'W'
      );
      const tests = [
        testResult(
          'Default module pitch is 1.323 m',
          nearlyEqual(defaultStudy.geometry.modulePitchM, 1.323),
          defaultStudy.geometry.modulePitchM,
          1.323
        ),
        testResult(
          'Default row span is 39.67 m',
          nearlyEqual(defaultStudy.geometry.rowSpanM, 39.67),
          defaultStudy.geometry.rowSpanM,
          39.67
        ),
        testResult(
          'Default leapfrog reach is two module pitches',
          nearlyEqual(
            defaultStudy.geometry.requiredLeapfrogReachM,
            2.646
          ),
          defaultStudy.geometry.requiredLeapfrogReachM,
          2.646
        ),
        testResult(
          'Default catalogue leads fail the reach screen',
          !defaultStudy.feasibility.feasible,
          defaultStudy.feasibility.status,
          'INFEASIBLE_LENGTH_SCREEN'
        ),
        testResult(
          'Two 1.2 m leads fail by 0.246 m',
          nearlyEqual(
            leads12Study.feasibility.marginM,
            -0.246
          ),
          leads12Study.feasibility.marginM,
          -0.246
        ),
        testResult(
          'Two 1.4 m leads pass the reach screen',
          leads14Study.feasibility.feasible,
          leads14Study.feasibility.status,
          'FEASIBLE_LENGTH_SCREEN'
        ),
        testResult(
          'Default archetype contains 24 strings',
          defaultStudy.totals.stringsPerArchetypeInverter === 24,
          defaultStudy.totals.stringsPerArchetypeInverter,
          24
        ),
        testResult(
          'Theoretical saving is 952.08 m per archetype inverter',
          nearlyEqual(
            defaultStudy.totals
              .theoreticalSavingMPerArchetypeInverter,
            952.08,
            1e-6
          ),
          defaultStudy.totals
            .theoreticalSavingMPerArchetypeInverter,
          952.08
        ),
        testResult(
          'Fleet saving uses 18,918 strings',
          nearlyEqual(
            defaultStudy.totals.theoreticalSiteSavingKm,
            750.47706,
            1e-8
          ),
          defaultStudy.totals.theoreticalSiteSavingKm,
          750.47706
        ),
        testResult(
          'Saving is independent of inverter distance',
          nearlyEqual(
            defaultStudy.totals
              .theoreticalSavingMPerArchetypeInverter,
            distance30Study.totals
              .theoreticalSavingMPerArchetypeInverter
          ),
          distance30Study.totals
            .theoreticalSavingMPerArchetypeInverter,
          defaultStudy.totals
            .theoreticalSavingMPerArchetypeInverter
        ),
        testResult(
          'West sequential polarity remains mirrored',
          Boolean(
            westString &&
            westString.sequential.positiveM ===
              westString.farRouteM &&
            westString.sequential.negativeM ===
              westString.nearRouteM
          ),
          westString
            ? `${westString.sequential.positiveM}/` +
              `${westString.sequential.negativeM}`
            : 'missing',
          westString
            ? `${westString.farRouteM}/` +
              `${westString.nearRouteM}`
            : 'west string'
        ),
        testResult(
          'Leapfrog terminals share the near route',
          defaultStudy.strings.every(
            (string) =>
              string.leapfrog.positiveM ===
                string.nearRouteM &&
              string.leapfrog.negativeM ===
                string.nearRouteM
          ),
          defaultStudy.strings[0]
            ? `${defaultStudy.strings[0].leapfrog.positiveM}/` +
              `${defaultStudy.strings[0].leapfrog.negativeM}`
            : 'missing',
          defaultStudy.strings[0]
            ? defaultStudy.strings[0].nearRouteM
            : 'near route'
        ),
        testResult(
          'Infeasible default does not claim available saving',
          defaultStudy.totals.availableSiteSavingKm === null,
          defaultStudy.totals.availableSiteSavingKm,
          null
        )
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
      modulePitchM,
      rowSpanM,
      cableResistancePerM,
      leadFeasibility,
      buildStrings,
      calculate,
      scenarioStudies,
      runGoldenTests
    });
  }
);
