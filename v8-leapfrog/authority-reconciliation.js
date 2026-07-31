(function attachAuthorityReconciliation(root, factory) {
  'use strict';

  const api = factory();

  if (typeof module === 'object' && module.exports) {
    module.exports = api;
  }

  if (root) {
    root.V8AuthorityReconciliation = api;
  }
})(
  typeof window !== 'undefined' ? window : globalThis,
  function buildAuthorityReconciliation() {
    'use strict';

    const VERSION = '1.0.0';

    const BUILD_025_REFERENCE = Object.freeze({
      fixtureId: 'build-025-reference-24-by-30',
      fixtureDescription:
        '24 strings × 30 modules, Build 025 plan-coordinate reference fixture',
      authorityStatus: 'V10_CANONICAL_CANDIDATE_REFERENCE',
      sourceMethod: 'globalgrid2050.solar-dc.strategy-comparison.v1',
      sourceReference:
        'Build 025 compare_reference_24_by_30 deterministic receipt',
      geometryDimensionality: 'plan_2d',
      terminalGeometryEvidence: 'generic_unresolved',
      terminalGeometrySource:
        'build_025_junction_box_centre_reference',
      sequential: Object.freeze({
        fieldInstalledConductorM: 1710.144,
        factoryFittedConductorM: 803.184,
        totalCircuitConductorM: 2513.328,
        signedLoopAreaM2: 420.4362,
        absoluteWindingAreaM2: 420.4362
      }),
      leapfrog: Object.freeze({
        fieldInstalledConductorM: 911.856,
        factoryFittedConductorM: 1648.272,
        totalCircuitConductorM: 2560.128,
        signedLoopAreaM2: 71.5608,
        absoluteWindingAreaM2: 84.9216
      })
    });

    function calculate(reference = BUILD_025_REFERENCE) {
      const fieldInstalledReductionM =
        reference.sequential.fieldInstalledConductorM -
        reference.leapfrog.fieldInstalledConductorM;
      const factoryFittedIncreaseM =
        reference.leapfrog.factoryFittedConductorM -
        reference.sequential.factoryFittedConductorM;
      const totalCircuitChangeM =
        reference.leapfrog.totalCircuitConductorM -
        reference.sequential.totalCircuitConductorM;
      const absoluteWindingAreaReductionM2 =
        reference.sequential.absoluteWindingAreaM2 -
        reference.leapfrog.absoluteWindingAreaM2;
      const absoluteWindingAreaReductionPercent =
        100 * absoluteWindingAreaReductionM2 /
        reference.sequential.absoluteWindingAreaM2;

      return Object.freeze({
        version: VERSION,
        fixtureId: reference.fixtureId,
        fieldInstalledReductionM,
        factoryFittedIncreaseM,
        totalCircuitChangeM,
        absoluteWindingAreaReductionM2,
        absoluteWindingAreaReductionPercent,
        warning:
          'V8 calculates field-installed external-cable reduction only. ' +
          'Build 025 additionally includes factory-fitted interconnect conductor. ' +
          'The Build 025 loop-area result is fixture-specific because terminal ' +
          'geometry is unresolved and geometry is plan_2d.'
      });
    }

    function nearlyEqual(actual, expected, tolerance = 1e-9) {
      return Math.abs(actual - expected) <= tolerance;
    }

    function runGoldenTests() {
      const result = calculate();
      const tests = [
        {
          name: 'Build 025 field-installed reduction is 798.288 m',
          pass: nearlyEqual(result.fieldInstalledReductionM, 798.288),
          actual: result.fieldInstalledReductionM,
          expected: 798.288
        },
        {
          name: 'Build 025 factory-fitted increase is 845.088 m',
          pass: nearlyEqual(result.factoryFittedIncreaseM, 845.088),
          actual: result.factoryFittedIncreaseM,
          expected: 845.088
        },
        {
          name: 'Build 025 total circuit conductor increases by 46.800 m',
          pass: nearlyEqual(result.totalCircuitChangeM, 46.8),
          actual: result.totalCircuitChangeM,
          expected: 46.8
        },
        {
          name: 'Build 025 absolute winding area falls by about 79.8 percent',
          pass: nearlyEqual(
            result.absoluteWindingAreaReductionPercent,
            79.801546,
            1e-6
          ),
          actual: result.absoluteWindingAreaReductionPercent,
          expected: 79.801546
        },
        {
          name: 'Reference declares unresolved terminal geometry',
          pass:
            BUILD_025_REFERENCE.terminalGeometryEvidence ===
            'generic_unresolved',
          actual: BUILD_025_REFERENCE.terminalGeometryEvidence,
          expected: 'generic_unresolved'
        },
        {
          name: 'Reference declares plan-coordinate geometry',
          pass:
            BUILD_025_REFERENCE.geometryDimensionality === 'plan_2d',
          actual: BUILD_025_REFERENCE.geometryDimensionality,
          expected: 'plan_2d'
        }
      ];

      return Object.freeze({
        version: VERSION,
        passed: tests.filter((test) => test.pass).length,
        total: tests.length,
        allPassed: tests.every((test) => test.pass),
        tests
      });
    }

    function format(value, decimals) {
      return Number(value).toLocaleString('en-GB', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
      });
    }

    function renderBrowser() {
      if (typeof document === 'undefined') {
        return;
      }

      const result = calculate();
      const setText = (id, text) => {
        const element = document.getElementById(id);
        if (element) {
          element.textContent = text;
        }
      };

      setText(
        'authorityFieldInstalledReduction',
        `${format(result.fieldInstalledReductionM, 3)} m reduction`
      );
      setText(
        'authorityFactoryFittedIncrease',
        `${format(result.factoryFittedIncreaseM, 3)} m increase`
      );
      setText(
        'authorityTotalCircuitChange',
        `${format(result.totalCircuitChangeM, 3)} m increase`
      );
      setText(
        'authorityLoopAreaReduction',
        `${format(result.absoluteWindingAreaReductionPercent, 1)}% reduction`
      );
      setText(
        'authorityGeometryBasis',
        `${BUILD_025_REFERENCE.geometryDimensionality} · ` +
          `${BUILD_025_REFERENCE.terminalGeometryEvidence}`
      );

      const applySummary = () => {
        const summary = document.getElementById('plainSummary');
        if (!summary) {
          return;
        }
        const marker = 'BUILD 025 AUTHORITY RECONCILIATION';
        const base = summary.value.split(`\n\n${marker}`)[0];
        summary.value = [
          base,
          '',
          marker,
          `Field-installed conductor reduction: ${format(result.fieldInstalledReductionM, 3)} m`,
          `Factory-fitted conductor increase: ${format(result.factoryFittedIncreaseM, 3)} m`,
          `Total circuit conductor change: +${format(result.totalCircuitChangeM, 3)} m`,
          `Absolute winding-area reduction: ${format(result.absoluteWindingAreaReductionPercent, 1)}%`,
          `Geometry basis: ${BUILD_025_REFERENCE.geometryDimensionality}; terminals ${BUILD_025_REFERENCE.terminalGeometryEvidence}.`,
          'V8 resistance, voltage-drop and loss differences apply only to the represented external 6 mm² field-installed portion.'
        ].join('\n');
      };

      applySummary();
      document.querySelectorAll('input,select').forEach((element) => {
        element.addEventListener('input', () => setTimeout(applySummary, 0));
        element.addEventListener('change', () => setTimeout(applySummary, 0));
      });

      root.__V8_AUTHORITY_RECONCILIATION__ = Object.freeze({
        reference: BUILD_025_REFERENCE,
        result,
        tests: runGoldenTests()
      });
    }

    if (typeof document !== 'undefined') {
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', renderBrowser, {
          once: true
        });
      } else {
        renderBrowser();
      }
    }

    return Object.freeze({
      VERSION,
      BUILD_025_REFERENCE,
      calculate,
      runGoldenTests,
      renderBrowser
    });
  }
);