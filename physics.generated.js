'use strict';
/* Browser formula artefact aligned with src/solar_topology/formulas.py.
   All outputs are screening values with explicit provenance and validity limits. */
window.SolarPhysics = (() => {
  const MU0 = 4 * Math.PI * 1e-7;
  const EPS0 = 8.8541878128e-12;
  const ALPHA_CU20 = 0.00393;
  const STANDARD_R20_OHM_PER_M = Object.freeze({
    'cu_tinned_class5_4': 5.09e-3,
    'cu_tinned_class5_6': 3.39e-3,
    'cu_plain_class5_4': 4.95e-3,
    'cu_plain_class5_6': 3.30e-3
  });

  function conductorDiameterFromArea(areaMm2){
    if (!(areaMm2 > 0)) throw new Error('Metallic conductor area must be positive');
    return Math.sqrt(4 * areaMm2 / Math.PI);
  }

  function resistanceAtTemperature(referenceResistance, referenceTemperatureC, targetTemperatureC, alpha = ALPHA_CU20){
    return referenceResistance * (1 + alpha * (targetTemperatureC - referenceTemperatureC));
  }

  function standardResistance(totalMetalLengthM, key, temperatureC){
    const r20 = STANDARD_R20_OHM_PER_M[key];
    if (!Number.isFinite(r20)) throw new Error(`Unknown conductor resistance key: ${key}`);
    return resistanceAtTemperature(r20 * totalMetalLengthM, 20, temperatureC, ALPHA_CU20);
  }

  function contactResistance(baseOhm, referenceTemperatureC, targetTemperatureC, alpha){
    return resistanceAtTemperature(baseOhm, referenceTemperatureC, targetTemperatureC, alpha);
  }

  function twoWire(centreSpacingMm, conductorDiameterMm, epsilonR){
    const D = centreSpacingMm / 1000;
    const d = conductorDiameterMm / 1000;
    if (!(D > d)) throw new Error('Conductor centre spacing must exceed metallic conductor diameter');
    if (!(epsilonR > 0)) throw new Error('Effective relative permittivity must be positive');
    const geometry = Math.acosh(D / d);
    const externalL = MU0 / Math.PI * geometry;
    const internalL = MU0 / (4 * Math.PI);
    const lowFrequencyL = externalL + internalL;
    const highFrequencyL = externalL;
    const capacitancePerM = Math.PI * EPS0 * epsilonR / geometry;
    const z0Low = Math.sqrt(lowFrequencyL / capacitancePerM);
    const z0High = Math.sqrt(highFrequencyL / capacitancePerM);
    const velocityLow = 1 / Math.sqrt(lowFrequencyL * capacitancePerM);
    const velocityHigh = 1 / Math.sqrt(highFrequencyL * capacitancePerM);
    return {
      geometry,
      externalInductancePerM: externalL,
      internalInductancePerM: internalL,
      lowFrequencyInductancePerM: lowFrequencyL,
      highFrequencyInductancePerM: highFrequencyL,
      capacitancePerM,
      z0Low,
      z0High,
      velocityLow,
      velocityHigh
    };
  }

  function commonModeInductancePerM(heightM, conductorRadiusMm, centreSpacingMm){
    if (!(heightM > 0)) throw new Error('Height above reference plane must be positive');
    const r = conductorRadiusMm / 1000;
    const s = centreSpacingMm / 1000;
    const req = Math.sqrt(Math.max(r * s, Number.EPSILON));
    const ratio = 2 * heightM / req;
    if (!(ratio > 1)) throw new Error('Common-mode image geometry is outside the valid screening domain');
    return MU0 / (2 * Math.PI) * Math.log(ratio);
  }

  function coilInductance(turns, meanDiameterMm, conductorDiameterMm){
    if (!(turns > 0) || !(meanDiameterMm > conductorDiameterMm)) return 0;
    const R = meanDiameterMm / 2000;
    const a = conductorDiameterMm / 2000;
    return MU0 * turns * turns * R * (Math.log(8 * R / a) - 2);
  }

  function coilArea(turns, meanDiameterMm){
    if (!(turns > 0) || !(meanDiameterMm > 0)) return 0;
    const R = meanDiameterMm / 2000;
    return Math.PI * R * R * turns;
  }

  function polygonArea(points){
    if (!Array.isArray(points) || points.length < 3) return 0;
    let sum = 0;
    for (let i = 0; i < points.length; i++){
      const a = points[i], b = points[(i + 1) % points.length];
      sum += a[0] * b[1] - b[0] * a[1];
    }
    return Math.abs(sum) / 2;
  }

  function coldVoc(moduleVoc, moduleCount, betaPctPerC, tempC){
    return moduleVoc * moduleCount * (1 + (betaPctPerC / 100) * (tempC - 25));
  }

  function parallelPlateCap(areaM2, thicknessMm, epsilonR){
    if (!(areaM2 >= 0) || !(thicknessMm > 0) || !(epsilonR > 0)) throw new Error('Invalid parallel-plate capacitance inputs');
    return EPS0 * epsilonR * areaM2 / (thicknessMm / 1000);
  }

  function cableToGroundCapacitancePerM(cableOdMm, conductorDiameterMm, epsilonR, wettedFraction){
    const od = cableOdMm / 1000;
    const d = conductorDiameterMm / 1000;
    const f = Math.max(0, Math.min(1, wettedFraction));
    if (!(od > d) || !(epsilonR > 0)) return 0;
    return 2 * Math.PI * EPS0 * epsilonR / Math.log(od / d) * f;
  }

  function storedMagnetic(L, I){ return 0.5 * L * I * I; }
  function storedElectric(C, V){ return 0.5 * C * V * V; }
  function parallelPair(a, b){
    if (!(a > 0)) return b;
    if (!(b > 0)) return a;
    return 1 / (1 / a + 1 / b);
  }

  return Object.freeze({
    formulaVersion: 'complete-circuit-v7-development-2026-07-26',
    constants: { MU0, EPS0, ALPHA_CU20, STANDARD_R20_OHM_PER_M },
    conductorDiameterFromArea,
    resistanceAtTemperature,
    standardResistance,
    contactResistance,
    twoWire,
    commonModeInductancePerM,
    coilInductance,
    coilArea,
    polygonArea,
    coldVoc,
    parallelPlateCap,
    cableToGroundCapacitancePerM,
    storedMagnetic,
    storedElectric,
    parallelPair
  });
})();
