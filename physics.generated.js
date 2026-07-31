'use strict';
/* Browser formula library for the V6 complete-string-circuit prototype.
   Formula outputs are screening values with explicit validity limits. */
window.SolarPhysics = (() => {
  const MU0 = 4 * Math.PI * 1e-7;
  const EPS0 = 8.8541878128e-12;
  const RHO_CU20 = 1.724e-8;
  const ALPHA_CU20 = 0.00393;
  const RESISTANCE_MODEL = Object.freeze({
    authorityStatus: 'historical_reference',
    basis: 'ideal_bulk_estimate',
    valueKind: 'lower_bound_estimate',
    sourceReference: 'bulk copper resistivity divided by nominal metallic area',
    sourceRevision: 'complete-circuit-v6-2026-07-26',
    warning: 'Ideal bulk-copper screening calculation using nominal metallic area. Not a finished-cable declared resistance and not an IEC 60228 maximum-resistance calculation.'
  });
  function conductorDiameterFromArea(areaMm2){return Math.sqrt(4*areaMm2/Math.PI);}
  function resistanceAtTemperature(referenceResistance,referenceTemperatureC,targetTemperatureC,alpha=ALPHA_CU20){return referenceResistance*(1+alpha*(targetTemperatureC-referenceTemperatureC));}
  function dcResistance(totalMetalLengthM,areaMm2,temperatureC){return RHO_CU20*totalMetalLengthM/(areaMm2*1e-6)*(1+ALPHA_CU20*(temperatureC-20));}
  function contactResistance(baseOhm,referenceTemperatureC,targetTemperatureC,alpha){return resistanceAtTemperature(baseOhm,referenceTemperatureC,targetTemperatureC,alpha);}
  function twoWire(centreSpacingMm,conductorDiameterMm,epsilonR){
    const D=centreSpacingMm/1000,d=conductorDiameterMm/1000;
    if(!(D>d)) throw new Error('Conductor centre spacing must exceed conductor diameter');
    const g=Math.acosh(D/d);
    const externalL=MU0/Math.PI*g;
    const internalL=MU0/(4*Math.PI);
    const lp=externalL+internalL;
    const cp=Math.PI*EPS0*epsilonR/g;
    return {geometry:g,externalInductancePerM:externalL,internalInductancePerM:internalL,inductancePerM:lp,capacitancePerM:cp,z0:Math.sqrt(lp/cp),velocity:1/Math.sqrt(lp*cp)};
  }
  function polygonArea(points){let sum=0;for(let i=0;i<points.length;i++){const a=points[i],b=points[(i+1)%points.length];sum+=a[0]*b[1]-b[0]*a[1];}return Math.abs(sum)/2;}
  function coldVoc(moduleVoc,moduleCount,betaPctPerC,tempC){return moduleVoc*moduleCount*(1+(betaPctPerC/100)*(tempC-25));}
  function parallelPlateCap(areaM2,thicknessMm,epsilonR){return EPS0*epsilonR*areaM2/(thicknessMm/1000);}
  function storedMagnetic(L,I){return 0.5*L*I*I;}
  function storedElectric(C,V){return 0.5*C*V*V;}
  function installResistanceWarning(){
    if(typeof document==='undefined')return;
    const existing=document.getElementById('legacyResistanceAuthority');
    if(existing)return;
    const host=document.querySelector('.reliance');
    if(!host)return;
    const warning=document.createElement('div');
    warning.id='legacyResistanceAuthority';
    warning.style.marginTop='8px';
    warning.style.paddingTop='8px';
    warning.style.borderTop='1px solid currentColor';
    warning.innerHTML='<strong>RESISTANCE AUTHORITY · HISTORICAL LOWER-BOUND SCREEN</strong> '+RESISTANCE_MODEL.warning;
    host.appendChild(warning);
  }
  if(typeof document!=='undefined'){
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',installResistanceWarning,{once:true});
    else installResistanceWarning();
  }
  return Object.freeze({formulaVersion:'complete-circuit-v6-2026-07-26',constants:{MU0,EPS0,RHO_CU20,ALPHA_CU20},resistanceModel:RESISTANCE_MODEL,conductorDiameterFromArea,resistanceAtTemperature,dcResistance,contactResistance,twoWire,polygonArea,coldVoc,parallelPlateCap,storedMagnetic,storedElectric});
})();