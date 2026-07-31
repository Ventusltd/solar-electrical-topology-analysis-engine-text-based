'use strict';

const assert = require('node:assert/strict');
const model = require('../v8-leapfrog/model.js');
const authority = require('../v8-leapfrog/authority-reconciliation.js');

function close(actual, expected, tolerance = 1e-9) {
  return Math.abs(actual - expected) <= tolerance;
}

const golden = model.runGoldenTests();

assert.equal(
  golden.allPassed,
  true,
  JSON.stringify(golden.tests, null, 2)
);

const defaultStudy = model.calculate(model.DEFAULTS);

assert.equal(
  defaultStudy.totals.stringsPerArchetypeInverter,
  24
);
assert.equal(
  defaultStudy.totals.totalSiteStringCount,
  18_918
);
assert.ok(
  close(defaultStudy.geometry.modulePitchM, 1.323)
);
assert.ok(
  close(defaultStudy.geometry.rowSpanM, 39.67)
);
assert.ok(
  close(
    defaultStudy.geometry.requiredLeapfrogReachM,
    2.646
  )
);
assert.equal(
  defaultStudy.feasibility.feasible,
  false
);
assert.equal(
  defaultStudy.totals.availableSiteSavingKm,
  null
);
assert.ok(
  close(
    defaultStudy.totals
      .sequentialExternalMPerArchetypeInverter,
    2_878.20
  )
);
assert.ok(
  close(
    defaultStudy.totals
      .leapfrogExternalMPerArchetypeInverter,
    1_926.12
  )
);
assert.ok(
  close(
    defaultStudy.totals
      .theoreticalSavingMPerArchetypeInverter,
    952.08
  )
);
assert.ok(
  close(
    defaultStudy.totals.theoreticalSiteSavingKm,
    750.47706
  )
);

const feasibleStudy = model.calculate({
  ...model.DEFAULTS,
  positiveFactoryLeadM: 1.4,
  negativeFactoryLeadM: 1.4,
  leadEvidence: 'MANUFACTURER_CUSTOM_DECLARED'
});

assert.equal(
  feasibleStudy.feasibility.feasible,
  true
);
assert.ok(
  close(
    feasibleStudy.totals.availableSiteSavingKm,
    750.47706
  )
);

const shortLeadStudy = model.calculate({
  ...model.DEFAULTS,
  positiveFactoryLeadM: 1.2,
  negativeFactoryLeadM: 1.2
});

assert.equal(
  shortLeadStudy.feasibility.feasible,
  false
);
assert.ok(
  close(shortLeadStudy.feasibility.marginM, -0.246)
);
assert.ok(
  close(
    shortLeadStudy.feasibility.extensionRequiredM,
    0.246
  )
);

const distance30Study = model.calculate({
  ...model.DEFAULTS,
  inverterDistanceM: 30
});

assert.ok(
  close(
    distance30Study.totals
      .theoreticalSavingMPerArchetypeInverter,
    defaultStudy.totals
      .theoreticalSavingMPerArchetypeInverter
  )
);
assert.ok(
  distance30Study.totals
    .leapfrogExternalMPerArchetypeInverter >
  defaultStudy.totals
    .leapfrogExternalMPerArchetypeInverter
);

const west = defaultStudy.strings.find(
  (item) => item.face === 'W'
);

assert.ok(west);
assert.equal(
  west.sequential.positiveM,
  west.farRouteM
);
assert.equal(
  west.sequential.negativeM,
  west.nearRouteM
);
assert.equal(
  west.leapfrog.positiveM,
  west.nearRouteM
);
assert.equal(
  west.leapfrog.negativeM,
  west.nearRouteM
);

const authorityGolden = authority.runGoldenTests();
assert.equal(
  authorityGolden.allPassed,
  true,
  JSON.stringify(authorityGolden.tests, null, 2)
);

const reconciliation = authority.calculate();
assert.ok(close(reconciliation.fieldInstalledReductionM, 798.288));
assert.ok(close(reconciliation.factoryFittedIncreaseM, 845.088));
assert.ok(close(reconciliation.totalCircuitChangeM, 46.8));
assert.ok(
  close(
    reconciliation.absoluteWindingAreaReductionPercent,
    79.801548963,
    1e-9
  )
);
assert.equal(
  authority.BUILD_025_REFERENCE.geometryDimensionality,
  'plan_2d'
);
assert.equal(
  authority.BUILD_025_REFERENCE.terminalGeometryEvidence,
  'generic_unresolved'
);

console.log(
  `V8 regression tests passed: ${golden.passed}/${golden.total}; ` +
  `authority reconciliation ${authorityGolden.passed}/${authorityGolden.total}`
);