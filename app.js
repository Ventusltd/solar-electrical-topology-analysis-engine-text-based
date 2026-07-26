'use strict';

const MU0 = 4 * Math.PI * 1e-7;
const EPS0 = 8.8541878128e-12;
const RHO20 = 1.724e-8;
const ALPHA_CU = 0.00393;
const MAX_DC_VOLTAGE = 1500;
const FACTORY_POS_LEAD_M = 0.35;
const FACTORY_NEG_LEAD_M = 0.28;

const canvas = document.getElementById('scene');
const ctx = canvas.getContext('2d');
const $ = id => document.getElementById(id);
const inputIds = ['moduleCount','modulesPerTable','moduleLength','moduleWidth','moduleGap','tableGap','rowCount','rowPitch','moduleVmp','moduleVoc','moduleImp','betaVoc','coldTemp','csa','cableOd','spacing','epsilonR','frameCap','conductorTemp','riseTime','routeMode','maintenanceLoop'];

const state = {
  inverter: { x: 27, y: 7 },
  dragging: false,
  dragOffset: { x: 0, y: 0 },
  view: null,
  lastStudy: null
};

function num(id) { return Number($(id).value); }
function fmt(v, d = 2) { return Number.isFinite(v) ? v.toLocaleString('en-GB', {minimumFractionDigits:d, maximumFractionDigits:d}) : '—'; }
function set(id, value) { $(id).textContent = value; }
function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

function model() {
  return {
    moduleCount: Math.max(1, Math.round(num('moduleCount'))),
    modulesPerTable: Math.max(1, Math.round(num('modulesPerTable'))),
    moduleLength: num('moduleLength'),
    moduleWidth: num('moduleWidth'),
    moduleGap: num('moduleGap'),
    tableGap: num('tableGap'),
    rowCount: Math.max(1, Math.round(num('rowCount'))),
    rowPitch: num('rowPitch'),
    moduleVmp: num('moduleVmp'),
    moduleVoc: num('moduleVoc'),
    moduleImp: num('moduleImp'),
    betaVoc: num('betaVoc'),
    coldTemp: num('coldTemp'),
    csaMm2: num('csa'),
    cableOdMm: num('cableOd'),
    spacingMm: num('spacing'),
    epsilonR: num('epsilonR'),
    frameCapNf: num('frameCap'),
    conductorTemp: num('conductorTemp'),
    riseTimeUs: num('riseTime'),
    routeMode: $('routeMode').value,
    maintenanceLoopM: num('maintenanceLoop')
  };
}

function buildGeometry(m) {
  const tablesNeeded = Math.ceil(m.moduleCount / m.modulesPerTable);
  const tablesPerRow = Math.ceil(tablesNeeded / m.rowCount);
  const tableWidth = m.modulesPerTable * m.moduleWidth + (m.modulesPerTable - 1) * m.moduleGap;
  const arrayWidth = tablesPerRow * tableWidth + Math.max(0, tablesPerRow - 1) * m.tableGap;
  const arrayHeight = (m.rowCount - 1) * m.rowPitch + m.moduleLength;
  const modules = [];
  let visibleIndex = 0;

  for (let r = 0; r < m.rowCount; r++) {
    for (let t = 0; t < tablesPerRow; t++) {
      for (let p = 0; p < m.modulesPerTable; p++) {
        const x = t * (tableWidth + m.tableGap) + p * (m.moduleWidth + m.moduleGap);
        const y = r * m.rowPitch;
        modules.push({
          id: `R${String(r+1).padStart(2,'0')}-T${String(t+1).padStart(2,'0')}-M${String(p+1).padStart(2,'0')}`,
          row: r, table: t, posInTable: p, x, y, w: m.moduleWidth, h: m.moduleLength,
          active: visibleIndex < m.moduleCount,
          visibleIndex: visibleIndex++
        });
      }
    }
  }

  const activeByRow = [];
  for (let r = 0; r < m.rowCount; r++) {
    const rowMods = modules.filter(x => x.row === r && x.active).sort((a,b) => a.x-b.x);
    if (r % 2 === 1) rowMods.reverse();
    activeByRow.push(...rowMods);
  }
  const sequence = activeByRow.slice(0, m.moduleCount);
  const first = sequence[0];
  const last = sequence[sequence.length - 1];
  const terminal = (mod, positive) => ({
    x: positive ? mod.x + mod.w : mod.x,
    y: mod.y + mod.h * 0.52
  });
  const negStart = terminal(first, false);
  const posEnd = terminal(last, true);

  return { modules, sequence, tablesNeeded, tablesPerRow, tableWidth, arrayWidth, arrayHeight, negStart, posEnd };
}

function orthogonalRoute(start, end, mode, polarity, g, m) {
  if (mode === 'paired') {
    const spineY = g.arrayHeight + 1.1;
    const sharedX = Math.max(g.arrayWidth + 1.1, Math.min(end.x - 1, g.arrayWidth + 2.0));
    const offset = polarity === 'pos' ? -m.spacingMm / 1000 / 2 : m.spacingMm / 1000 / 2;
    return [start, {x:start.x,y:spineY+offset}, {x:sharedX,y:spineY+offset}, {x:sharedX,y:end.y+offset}, end];
  }
  const corridorY = polarity === 'pos' ? -1.1 : g.arrayHeight + 1.3;
  return [start, {x:start.x,y:corridorY}, {x:end.x,y:corridorY}, end];
}

function polylineLength(points) {
  let s = 0;
  for (let i=1;i<points.length;i++) s += Math.hypot(points[i].x-points[i-1].x, points[i].y-points[i-1].y);
  return s;
}

function loopArea(pos, neg) {
  const polygon = [...pos, ...neg.slice().reverse()];
  let a = 0;
  for (let i=0;i<polygon.length;i++) {
    const p = polygon[i], q = polygon[(i+1)%polygon.length];
    a += p.x*q.y - q.x*p.y;
  }
  return Math.abs(a)/2;
}

function calculate(m, g) {
  const invPosPort = {x:state.inverter.x, y:state.inverter.y-0.28};
  const invNegPort = {x:state.inverter.x, y:state.inverter.y+0.28};
  const posRoute = orthogonalRoute(g.posEnd, invPosPort, m.routeMode, 'pos', g, m);
  const negRoute = orthogonalRoute(g.negStart, invNegPort, m.routeMode, 'neg', g, m);
  const posHome = polylineLength(posRoute) + 2*m.maintenanceLoopM;
  const negHome = polylineLength(negRoute) + 2*m.maintenanceLoopM;
  const factoryLeadTotal = m.moduleCount * (FACTORY_POS_LEAD_M + FACTORY_NEG_LEAD_M);
  const installed = posHome + negHome + factoryLeadTotal;
  const loopBasis = (posHome + negHome) / 2;
  const area = loopArea(posRoute, negRoute);

  const warnings = [];
  const errors = [];
  if ([m.moduleLength,m.moduleWidth,m.rowPitch,m.csaMm2,m.cableOdMm,m.spacingMm,m.epsilonR,m.moduleVmp,m.moduleVoc,m.moduleImp].some(v => !Number.isFinite(v) || v <= 0)) errors.push('All physical and electrical dimensions must be positive numeric values.');
  if (m.spacingMm <= m.cableOdMm) errors.push(`Conductor centres ${fmt(m.spacingMm,1)} mm do not exceed cable outside diameter ${fmt(m.cableOdMm,1)} mm.`);

  const conductorArea = m.csaMm2 * 1e-6;
  const r20 = RHO20 * installed / conductorArea;
  const loopR = r20 * (1 + ALPHA_CU * (m.conductorTemp - 20));
  const stringVmp = m.moduleCount * m.moduleVmp;
  const stringPower = stringVmp * m.moduleImp;
  const vDrop = m.moduleImp * loopR;
  const vDropPct = 100*vDrop/stringVmp;
  const loss = m.moduleImp*m.moduleImp*loopR;
  const lossPct = 100*loss/stringPower;

  const d = m.cableOdMm/1000;
  const D = m.spacingMm/1000;
  const ratio = D/d;
  const acosh = ratio > 1 ? Math.acosh(ratio) : NaN;
  const lPerM = MU0/Math.PI*acosh;
  const cPerM = Math.PI*EPS0*m.epsilonR/acosh;
  const L = lPerM*loopBasis;
  const Cpair = cPerM*loopBasis;
  const Cframe = m.moduleCount*m.frameCapNf*1e-9;
  const z0 = Math.sqrt(lPerM/cPerM);
  const velocity = 1/Math.sqrt(lPerM*cPerM);
  const delay = loopBasis/velocity;
  const roundTrip = 2*delay;
  const magneticEnergy = 0.5*L*m.moduleImp*m.moduleImp;
  const electricEnergy = 0.5*Cframe*stringVmp*stringVmp;
  const coldVoc = m.moduleCount*m.moduleVoc*(1+(m.betaVoc/100)*(m.coldTemp-25));
  const riseTime = m.riseTimeUs*1e-6;
  const distributed = riseTime < 2*delay;
  const marginal = !distributed && riseTime < 4*delay;

  if (vDropPct > 1) warnings.push(`Voltage drop ${fmt(vDropPct,2)}% exceeds the 1% screening marker.`);
  if (coldVoc > MAX_DC_VOLTAGE) warnings.push(`Cold string Voc ${fmt(coldVoc,1)} V exceeds the declared ${MAX_DC_VOLTAGE} V screening limit.`);
  if (m.routeMode === 'separated') warnings.push(`Separated polarity routing creates ${fmt(area,1)} m² of enclosed loop area and increases inductive/surge exposure.`);
  if (m.frameCapNf === 100) warnings.push('Module-to-frame capacitance remains a defaulted 100 nF/module input; replace with measured or manufacturer evidence for quantitative common-mode studies.');
  if (m.spacingMm/m.cableOdMm < 1.25) warnings.push('Polarity centre spacing is close to physical cable diameter; verify installed formation.');

  return {posRoute,negRoute,posHome,negHome,factoryLeadTotal,installed,loopBasis,area,r20,loopR,stringVmp,stringPower,vDrop,vDropPct,loss,lossPct,lPerM,cPerM,L,Cpair,Cframe,z0,velocity,delay,roundTrip,magneticEnergy,electricEnergy,coldVoc,distributed,marginal,warnings,errors,acosh};
}

function worldBounds(g) {
  const minX = -2.4, minY = -2.7;
  const maxX = Math.max(g.arrayWidth+5, state.inverter.x+3);
  const maxY = Math.max(g.arrayHeight+3.2, state.inverter.y+2.2);
  return {minX,minY,maxX,maxY};
}

function resizeCanvas() {
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.round(rect.width*dpr));
  canvas.height = Math.max(1, Math.round(rect.height*dpr));
  ctx.setTransform(dpr,0,0,dpr,0,0);
}

function makeView(g) {
  const rect = canvas.getBoundingClientRect();
  const b = worldBounds(g), pad = 35;
  const scale = Math.min((rect.width-2*pad)/(b.maxX-b.minX),(rect.height-2*pad)/(b.maxY-b.minY));
  return {
    scale, ox:pad-b.minX*scale, oy:pad-b.minY*scale,
    sx:x=>pad+(x-b.minX)*scale,
    sy:y=>pad+(y-b.minY)*scale,
    wx:x=>(x-pad)/scale+b.minX,
    wy:y=>(y-pad)/scale+b.minY
  };
}

function line(points, colour, width=3, dash=[]) {
  if (!points.length) return;
  ctx.beginPath(); ctx.setLineDash(dash); ctx.strokeStyle=colour; ctx.lineWidth=width;
  ctx.moveTo(state.view.sx(points[0].x),state.view.sy(points[0].y));
  points.slice(1).forEach(p=>ctx.lineTo(state.view.sx(p.x),state.view.sy(p.y)));
  ctx.stroke(); ctx.setLineDash([]);
}

function draw(m,g,s) {
  resizeCanvas();
  state.view = makeView(g);
  const rect=canvas.getBoundingClientRect();
  ctx.clearRect(0,0,rect.width,rect.height);

  ctx.strokeStyle='#132131';ctx.lineWidth=1;
  const grid=1;
  for(let x=Math.floor(worldBounds(g).minX);x<worldBounds(g).maxX;x+=grid){ctx.beginPath();ctx.moveTo(state.view.sx(x),0);ctx.lineTo(state.view.sx(x),rect.height);ctx.stroke()}
  for(let y=Math.floor(worldBounds(g).minY);y<worldBounds(g).maxY;y+=grid){ctx.beginPath();ctx.moveTo(0,state.view.sy(y));ctx.lineTo(rect.width,state.view.sy(y));ctx.stroke()}

  g.modules.forEach(mod=>{
    const x=state.view.sx(mod.x),y=state.view.sy(mod.y),w=mod.w*state.view.scale,h=mod.h*state.view.scale;
    ctx.fillStyle=mod.active?'#102d43':'#12161b';ctx.strokeStyle=mod.active?'#2a9ed0':'#333b43';ctx.lineWidth=1;
    ctx.fillRect(x,y,w,h);ctx.strokeRect(x,y,w,h);
    ctx.strokeStyle=mod.active?'#1a5a7a':'#262c32';
    for(let c=1;c<4;c++){ctx.beginPath();ctx.moveTo(x+w*c/4,y);ctx.lineTo(x+w*c/4,y+h);ctx.stroke()}
    ctx.fillStyle=mod.active?'#9fdfff':'#53606b';ctx.font='9px ui-monospace,monospace';ctx.fillText(mod.active?String(mod.visibleIndex+1):'UNUSED',x+3,y+12);
  });

  const frameY=g.arrayHeight+0.35;
  line([{x:0,y:frameY},{x:g.arrayWidth,y:frameY}], '#44e18a',2,[5,4]);
  line(s.posRoute,'#ff5964',4);
  line(s.negRoute,'#27d8ff',4);

  g.sequence.forEach((mod,i)=>{
    if(i===0)return;
    const prev=g.sequence[i-1];
    const a={x:prev.x+prev.w,y:prev.y+prev.h*.52};
    const b={x:mod.x,y:mod.y+mod.h*.52};
    line([a,b],'#b891ff',1.5,[3,3]);
  });

  const ix=state.view.sx(state.inverter.x),iy=state.view.sy(state.inverter.y),iw=2.1*state.view.scale,ih=1.35*state.view.scale;
  ctx.fillStyle='#2b2008';ctx.strokeStyle='#ffb347';ctx.lineWidth=2;ctx.fillRect(ix-iw/2,iy-ih/2,iw,ih);ctx.strokeRect(ix-iw/2,iy-ih/2,iw,ih);
  ctx.fillStyle='#ffe0a5';ctx.textAlign='center';ctx.font='bold 12px ui-monospace,monospace';ctx.fillText('INVERTER',ix,iy-4);ctx.font='10px ui-monospace,monospace';ctx.fillText('MPPT 01',ix,iy+13);ctx.textAlign='left';
  ctx.fillStyle='#ff5964';ctx.beginPath();ctx.arc(state.view.sx(state.inverter.x),state.view.sy(state.inverter.y-.28),5,0,2*Math.PI);ctx.fill();
  ctx.fillStyle='#27d8ff';ctx.beginPath();ctx.arc(state.view.sx(state.inverter.x),state.view.sy(state.inverter.y+.28),5,0,2*Math.PI);ctx.fill();

  ctx.fillStyle='#73889d';ctx.font='11px ui-monospace,monospace';
  ctx.fillText(`${m.moduleCount} active modules · ${g.tablesNeeded} tables · planned geometry`,16,rect.height-16);
}

function renderOutputs(m,g,s){
  set('positiveLength',`${fmt(s.posHome,2)} m`); set('negativeLength',`${fmt(s.negHome,2)} m`); set('installedLength',`${fmt(s.installed,2)} m`); set('loopArea',`${fmt(s.area,2)} m²`);
  set('loopResistance',`${fmt(s.loopR,4)} Ω`); set('voltageDrop',`${fmt(s.vDrop,2)} V`); set('voltageDropPct',`${fmt(s.vDropPct,2)}% of string Vmp`);
  set('cableLoss',`${fmt(s.loss,1)} W`); set('cableLossPct',`${fmt(s.lossPct,2)}% of operating power`);
  set('loopInductance',`${fmt(s.L*1e6,2)} µH`); set('inductancePerM',`${fmt(s.lPerM*1e6,4)} µH/m`);
  set('pairCapacitance',`${fmt(s.Cpair*1e9,2)} nF`); set('capacitancePerM',`${fmt(s.cPerM*1e12,2)} pF/m`); set('frameCapacitance',`${fmt(s.Cframe*1e9,1)} nF`);
  set('z0',`${fmt(s.z0,1)} Ω`); set('delay',`${fmt(s.delay*1e6,3)} µs`); set('roundTrip',`${fmt(s.roundTrip*1e6,3)} µs round trip`);
  set('magneticEnergy',`${fmt(s.magneticEnergy*1000,3)} mJ`); set('electricEnergy',`${fmt(s.electricEnergy,3)} J`);
  set('stringVmp',`${fmt(s.stringVmp,1)} V`); set('stringPower',`${fmt(s.stringPower/1000,2)} kW at Imp`); set('coldVoc',`${fmt(s.coldVoc,1)} V`);

  const d=$('modelDecision');
  d.className='decision'+(s.distributed?' distributed':'');
  if(s.distributed) d.innerHTML=`<strong>DISTRIBUTED MODEL REQUIRED.</strong> One-way propagation delay ${fmt(s.delay*1e6,3)} µs; round-trip ${fmt(s.roundTrip*1e6,3)} µs; disturbance rise time ${fmt(m.riseTimeUs,3)} µs. The disturbance changes before the line can settle, so reflections and unequal electrical distances may affect peak voltage and current.`;
  else if(s.marginal) d.innerHTML=`<strong>MODEL SELECTION MARGINAL.</strong> Rise time ${fmt(m.riseTimeUs,3)} µs is only moderately longer than the ${fmt(s.roundTrip*1e6,3)} µs round-trip delay. Compare lumped and distributed representations.`;
  else d.innerHTML=`<strong>LUMPED MODEL ACCEPTABLE FOR THIS DECLARED DISTURBANCE.</strong> Rise time ${fmt(m.riseTimeUs,3)} µs is long relative to the ${fmt(s.roundTrip*1e6,3)} µs round-trip delay. Distributed parameters remain reported for study traceability.`;

  $('warningBox').innerHTML=[...s.errors.map(x=>`<div class="warning error">HARD ERROR · ${x}</div>`),...s.warnings.map(x=>`<div class="warning">REVIEW · ${x}</div>`)].join('');
  $('trace').textContent=buildTrace(m,g,s);
}

function buildTrace(m,g,s){
  return `SOLAR DC STRING TOPOLOGY ENGINE · TIER 1 TRACE

GEOMETRY
Modules in electrical series     ${m.moduleCount}
Modules per visible table        ${m.modulesPerTable}
Positive home run                ${fmt(s.posHome,4)} m
Negative home run                ${fmt(s.negHome,4)} m
Factory module leads             ${fmt(s.factoryLeadTotal,4)} m (${FACTORY_POS_LEAD_M} m + ${FACTORY_NEG_LEAD_M} m per module)
Total installed conductor        ${fmt(s.installed,4)} m
Differential line-length basis   ${fmt(s.loopBasis,4)} m
Enclosed 2D loop area            ${fmt(s.area,4)} m²

STEADY STATE
String Vmp                       ${fmt(s.stringVmp,3)} V
String Imp                       ${fmt(m.moduleImp,3)} A
Operating power                  ${fmt(s.stringPower,3)} W
R20                              ${fmt(s.r20,6)} Ω
R at ${fmt(m.conductorTemp,1)} °C                   ${fmt(s.loopR,6)} Ω
Voltage drop                     ${fmt(s.vDrop,4)} V (${fmt(s.vDropPct,3)}%)
I²R loss                         ${fmt(s.loss,4)} W (${fmt(s.lossPct,3)}%)
Cold Voc at ${fmt(m.coldTemp,1)} °C                 ${fmt(s.coldVoc,3)} V

DISTRIBUTED PARAMETERS
Exact geometry term acosh(D/d)   ${fmt(s.acosh,7)}
L′ loop                          ${fmt(s.lPerM*1e6,7)} µH/m
C′ conductor pair                ${fmt(s.cPerM*1e12,7)} pF/m
Loop inductance                  ${fmt(s.L*1e6,5)} µH
Pair capacitance                 ${fmt(s.Cpair*1e9,5)} nF
Declared frame capacitance       ${fmt(s.Cframe*1e9,5)} nF
Characteristic impedance         ${fmt(s.z0,5)} Ω
Propagation velocity             ${fmt(s.velocity/1e6,5)} Mm/s
One-way delay                    ${fmt(s.delay*1e6,6)} µs
Round-trip delay                 ${fmt(s.roundTrip*1e6,6)} µs

STORED ENERGY
Magnetic ½LI²                    ${fmt(s.magneticEnergy*1000,6)} mJ
Electric ½CV² frame basis        ${fmt(s.electricEnergy,6)} J

FORMULA BASIS
R(T) = ρ20·l/A·[1 + α20(T−20 °C)]
L′ = μ0/π·acosh(D/d)
C′ = πε0εr/acosh(D/d)
Z0 ≈ √(L′/C′)
v = 1/√(L′C′)
W_L = ½LI²; W_C = ½CV²
Cold Voc = N·Voc_STC·[1 + βVoc(T−25 °C)]

PROVENANCE
Geometry                        user-edited / drawing-derived basis
Module electrical data          manufacturer-style generic default
Factory leads                   defaulted public-datasheet anchor
Module-frame capacitance         assumed until measured/OEM evidence
Inverter internal capacitance    unresolved and excluded

BOUNDARY
The present release calculates a geometry-derived Tier 1 study basis. It does not yet solve impulse waveforms, frequency-dependent losses, SPD residual voltage, mutual coupling matrices or inverter internal transients.`;
}

function run(){
  const m=model();const g=buildGeometry(m);
  if(!Number.isFinite(state.inverter.x)||state.inverter.x<g.arrayWidth+1){state.inverter.x=g.arrayWidth+5;state.inverter.y=Math.max(1,g.arrayHeight/2)}
  const s=calculate(m,g);state.lastStudy={m,g,s};draw(m,g,s);renderOutputs(m,g,s);
}

function pointerWorld(ev){const r=canvas.getBoundingClientRect();return{x:state.view.wx(ev.clientX-r.left),y:state.view.wy(ev.clientY-r.top)}}
canvas.addEventListener('pointerdown',ev=>{if(!state.view)return;const p=pointerWorld(ev);if(Math.abs(p.x-state.inverter.x)<1.4&&Math.abs(p.y-state.inverter.y)<1){state.dragging=true;state.dragOffset={x:p.x-state.inverter.x,y:p.y-state.inverter.y};canvas.setPointerCapture(ev.pointerId);canvas.style.cursor='grabbing'}});
canvas.addEventListener('pointermove',ev=>{if(!state.dragging)return;const p=pointerWorld(ev);state.inverter.x=p.x-state.dragOffset.x;state.inverter.y=p.y-state.dragOffset.y;run()});
canvas.addEventListener('pointerup',ev=>{state.dragging=false;canvas.releasePointerCapture(ev.pointerId);canvas.style.cursor='crosshair'});

inputIds.forEach(id=>$(id).addEventListener('input',run));
$('reset').addEventListener('click',()=>{state.inverter={x:27,y:7};document.querySelectorAll('input').forEach(i=>i.value=i.defaultValue);$('routeMode').value='paired';run()});
$('export').addEventListener('click',()=>{if(!state.lastStudy)return;const {m,g,s}=state.lastStudy;const payload={schema_version:'0.2.0',generated_at:new Date().toISOString(),reliance_statement:'This tool produces an indicative topology and route-length study basis. It does not warrant installed cable quantities, prove routing feasibility, replace a survey, complete electrical design or certify compliance. Outputs must be reviewed by a competent person before use in procurement, construction or formal engineering studies.',inputs:m,objects:{inverter:state.inverter,modules:g.modules.map(({id,row,table,x,y,w,h,active})=>({id,row,table,x_m:x,y_m:y,width_m:w,height_m:h,active}))},routes:{positive:s.posRoute,negative:s.negRoute},results:{positive_length_m:s.posHome,negative_length_m:s.negHome,total_installed_conductor_m:s.installed,loop_area_m2:s.area,loop_resistance_ohm:s.loopR,loop_inductance_h:s.L,pair_capacitance_f:s.Cpair,frame_capacitance_f:s.Cframe,characteristic_impedance_ohm:s.z0,one_way_delay_s:s.delay,cold_voc_v:s.coldVoc},warnings:s.warnings,errors:s.errors};const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='solar-dc-string-study-basis.json';a.click();URL.revokeObjectURL(a.href)});
window.addEventListener('resize',run);
run();
