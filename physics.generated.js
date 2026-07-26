'use strict';
/* Generated browser artefact matching src/solar_topology/formulas.py.
   Do not hand-edit formulae in app.js. */
window.SolarPhysics = (() => {
  const MU0 = 4 * Math.PI * 1e-7;
  const EPS0 = 8.8541878128e-12;
  const RHO_CU20 = 1.724e-8;
  const ALPHA_CU20 = 0.00393;
  function conductorDiameterFromArea(areaMm2){return Math.sqrt(4*areaMm2/Math.PI);}
  function dcResistance(totalMetalLengthM, areaMm2, temperatureC){
    return RHO_CU20*totalMetalLengthM/(areaMm2*1e-6)*(1+ALPHA_CU20*(temperatureC-20));
  }
  function twoWire(centreSpacingMm, conductorDiameterMm, epsilonR){
    const D=centreSpacingMm/1000,d=conductorDiameterMm/1000;
    if(!(D>d)) throw new Error('Conductor centre spacing must exceed conductor diameter');
    const g=Math.acosh(D/d);
    const externalL=MU0/Math.PI*g;
    const internalL=MU0/(4*Math.PI); // μ0/8π per conductor, two conductors in loop
    const lp=externalL+internalL;
    const cp=Math.PI*EPS0*epsilonR/g;
    return {geometry:g,externalInductancePerM:externalL,internalInductancePerM:internalL,inductancePerM:lp,capacitancePerM:cp,z0:Math.sqrt(lp/cp),velocity:1/Math.sqrt(lp*cp)};
  }
  function coldVoc(moduleVoc,moduleCount,betaPctPerC,tempC){return moduleVoc*moduleCount*(1+(betaPctPerC/100)*(tempC-25));}
  function parallelPlateCap(areaM2,thicknessMm,epsilonR){return EPS0*epsilonR*areaM2/(thicknessMm/1000);}
  function storedMagnetic(L,I){return 0.5*L*I*I;}
  function storedElectric(C,V){return 0.5*C*V*V;}
  return Object.freeze({formulaVersion:'tier1-2026-07-26',conductorDiameterFromArea,dcResistance,twoWire,coldVoc,parallelPlateCap,storedMagnetic,storedElectric});
})();