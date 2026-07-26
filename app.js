'use strict';

const P = window.SolarPhysics;
const $ = id => document.getElementById(id);
const canvas = $('scene');
const ctx = canvas.getContext('2d');
const section = $('sectionCanvas');
const sctx = section.getContext('2d');
const MU0 = 4 * Math.PI * 1e-7;

const ids = [
  'modulesAlong','ranksUp','faces','tilt','moduleWidth','moduleLength','clampGap','alongGap','structureDrop',
  'eastBands','westBands','modulesPerString','mpptCount','stringsPerInverter','moduleSpacing','returnMode',
  'returnSpacing','coilLength','coilDiameter','trenchSpacing','moduleVmp','moduleVoc','moduleImp','betaVoc',
  'coldTemp','csa','cableOd','conductorTemp','epsilonR','riseTime','wetState','glassThickness','glassEr','wettedPct'
];

const state = {
  zoom: 1, panX: 0, panY: 0, panning: false, lastMouse: null,
  selected: null, inverter: {x: -4, y: 0}, dragInv: false, model: null, study: null
};

const num = id => Number($(id).value);
const fmt = (v, d = 2) => Number.isFinite(v) ? v.toLocaleString('en-GB', {minimumFractionDigits:d, maximumFractionDigits:d}) : '—';
const set = (id, v) => { $(id).textContent = v; };
const distance3 = (a,b) => Math.hypot(b[0]-a[0], b[1]-a[1], b[2]-a[2]);
const polylineLength = pts => pts.slice(1).reduce((sum,p,i)=>sum+distance3(pts[i],p),0);

function parseBands(id) {
  const list = $(id).value.split(',').map(v => Math.round(Number(v.trim()))).filter(v => Number.isFinite(v) && v > 0);
  return list.length ? list : [1];
}

function readInputs() {
  const m = {
    modulesAlong: Math.max(1, Math.round(num('modulesAlong'))),
    ranksUp: Math.max(1, Math.round(num('ranksUp'))),
    faces: Math.max(1, Math.min(2, Math.round(num('faces')))),
    tilt: num('tilt'), moduleWidth: num('moduleWidth'), moduleLength: num('moduleLength'),
    clampGap: num('clampGap'), alongGap: num('alongGap'), structureDrop: num('structureDrop'),
    eastBands: parseBands('eastBands'), westBands: parseBands('westBands'),
    modulesPerString: Math.max(1, Math.round(num('modulesPerString'))),
    mpptCount: Math.max(1, Math.round(num('mpptCount'))),
    stringsPerInverter: Math.max(1, Math.round(num('stringsPerInverter'))),
    moduleSpacing: num('moduleSpacing'), returnMode: $('returnMode').value,
    returnSpacing: num('returnSpacing'), coilLength: num('coilLength'), coilDiameter: num('coilDiameter'),
    trenchSpacing: num('trenchSpacing'), moduleVmp: num('moduleVmp'), moduleVoc: num('moduleVoc'),
    moduleImp: num('moduleImp'), betaVoc: num('betaVoc'), coldTemp: num('coldTemp'), csa: num('csa'),
    cableOd: num('cableOd'), temp: num('conductorTemp'), epsilonR: num('epsilonR'), riseUs: num('riseTime'),
    wetState: $('wetState').value, glassThickness: num('glassThickness'), glassEr: num('glassEr'),
    wettedPct: num('wettedPct') / 100
  };
  const rankPitchSlope = m.moduleLength + m.clampGap;
  if (m.returnMode === 'alongside') m.returnSpacing = Math.max(m.cableOd, 0.1);
  if (m.returnMode === 'rank-away') m.returnSpacing = rankPitchSlope * 1000;
  $('returnSpacing').disabled = m.returnMode !== 'custom';
  $('returnSpacing').value = Number(m.returnSpacing.toFixed(3));
  $('returnProv').textContent = m.returnMode === 'custom' ? 'ASSUMED' : 'PRESET · ASSUMED';
  return m;
}

function pointFeature(id, coordinates, properties={}) {
  return {type:'Feature', id, geometry:{type:'Point', coordinates}, properties:{id,...properties}};
}
function lineFeature(id, coordinates, properties={}) {
  return {type:'Feature', id, geometry:{type:'LineString', coordinates}, properties:{id,...properties}};
}
function polygonFeature(id, ring, properties={}) {
  return {type:'Feature', id, geometry:{type:'Polygon', coordinates:[ring]}, properties:{id,...properties}};
}

function buildGeometry(m) {
  const theta = m.tilt * Math.PI / 180;
  const rankPitchSlope = m.moduleLength + m.clampGap;
  const rankPitchPlan = rankPitchSlope * Math.cos(theta);
  const rankRise = rankPitchSlope * Math.sin(theta);
  const modulePitch = m.moduleWidth + m.alongGap;
  const bandLength = m.modulesAlong * modulePitch - m.alongGap;
  const bandGap = Math.max(0.5, m.alongGap * 5);
  const strings = [];
  const features = [];
  let maxX = 0;
  const faceDefs = [
    {face:'E', sign:-1, bands:m.eastBands},
    {face:'W', sign:1, bands:m.faces === 2 ? m.westBands : []}
  ];

  for (const def of faceDefs) {
    let x0 = 0;
    def.bands.forEach((rankCount, bandIndex) => {
      const x1 = x0 + bandLength;
      const faceExtent = rankCount * rankPitchPlan;
      const tableRing = [[x0,0],[x1,0],[x1,def.sign*faceExtent],[x0,def.sign*faceExtent],[x0,0]];
      features.push(polygonFeature(`${def.face}-B${bandIndex+1}`, tableRing, {layer:'table',face:def.face,band:bandIndex+1,rank_count:rankCount}));
      for (let rankIndex=0; rankIndex<rankCount; rankIndex++) {
        const yNear = def.sign * rankIndex * rankPitchPlan;
        const yFar = def.sign * (rankIndex + 1) * rankPitchPlan;
        const yCentre = (yNear + yFar) / 2;
        const zCentre = (rankIndex + 0.5) * rankRise;
        const id = `${def.face}-B${bandIndex+1}-R${rankIndex+1}`;
        const ring = [[x0,yNear],[x1,yNear],[x1,yFar],[x0,yFar],[x0,yNear]];
        features.push(polygonFeature(id, ring, {layer:'rank',face:def.face,band:bandIndex+1,rank:rankIndex+1,string_id:id}));
        strings.push({
          id, face:def.face, sign:def.sign, band:bandIndex, rank:rankIndex, rankCount,
          x0, x1, y:yCentre, yNear, yFar, z:zCentre,
          series:Array.from({length:m.modulesPerString},(_,i)=>i+1)
        });
      }
      x0 = x1 + bandGap;
      maxX = Math.max(maxX, x1);
    });
  }
  features.push(pointFeature('INV-01',[state.inverter.x,state.inverter.y],{layer:'inverter'}));
  return {
    strings, rankPitchSlope, rankPitchPlan, rankRise, modulePitch, bandLength,
    width:maxX, height:2*Math.max(...m.eastBands,...m.westBands,1)*rankPitchPlan,
    featureCollection:{type:'FeatureCollection',features}
  };
}

function addSegment(list, stringId, sequence, type, points, installedLength, formation, separationMm, provenance, extra={}) {
  const displacement = polylineLength(points);
  list.push({
    segment_id:`${stringId}-S${String(sequence).padStart(3,'0')}`,
    string_id:stringId, sequence_index:sequence, segment_type:type,
    points_3d:points, geometric_displacement_m:displacement,
    installed_conductor_length_m:installedLength == null ? displacement : installedLength,
    formation_type:formation, conductor_separation_mm:separationMm,
    provenance, route_length_source:'derived_from_segment_geometry', ...extra
  });
}

function buildSegments(s,m,g) {
  const segments=[];
  let sequence=1;
  const theta=m.tilt*Math.PI/180;
  const faceY = rank => s.sign * rank * g.rankPitchPlan;
  const faceZ = rank => rank * g.rankRise;
  const moduleY = (faceY(s.rank)+faceY(s.rank+1))/2;
  const moduleZ = (faceZ(s.rank)+faceZ(s.rank+1))/2;

  // Ordered series path: one interconnect between every adjacent module.
  for(let i=0;i<m.modulesPerString-1;i++) {
    const xA=s.x0+(i+0.5)*g.modulePitch;
    const xB=s.x0+(i+1.5)*g.modulePitch;
    addSegment(segments,s.id,sequence++,'module_interconnect',[[xA,moduleY,moduleZ],[xB,moduleY,moduleZ]],null,'rail_mounted_pair',m.moduleSpacing,'manufacturer_and_geometry',{series_from:i+1,series_to:i+2});
  }

  // Two factory-lead surplus coils per module: zero displacement, real conductor length.
  for(let i=0;i<m.modulesPerString;i++) {
    const x=s.x0+(i+0.5)*g.modulePitch;
    addSegment(segments,s.id,sequence++,'coiled_surplus',[[x,moduleY,moduleZ],[x,moduleY,moduleZ]],m.coilLength,'coiled_pair',m.coilDiameter,'defaulted',{module_index:i+1,lead:'positive'});
    addSegment(segments,s.id,sequence++,'coiled_surplus',[[x,moduleY,moduleZ],[x,moduleY,moduleZ]],m.coilLength,'coiled_pair',m.coilDiameter,'defaulted',{module_index:i+1,lead:'negative'});
  }

  // Return from the far module to the near end, following the table rail.
  const returnOffset=m.returnSpacing/1000;
  const returnY=moduleY+s.sign*returnOffset;
  addSegment(segments,s.id,sequence++,'along_rank_return',[[s.x1,moduleY,moduleZ],[s.x1,returnY,moduleZ],[s.x0,returnY,moduleZ]],null,'rail_mounted_return',m.returnSpacing,'assumed');

  // Physical slope transfer to the ridge/collection edge. Length is slope distance; plan is projection.
  const transferSlope=s.rank*g.rankPitchSlope;
  const transferPlan=s.rank*g.rankPitchPlan;
  const transferRise=s.rank*g.rankRise;
  addSegment(segments,s.id,sequence++,'across_table_transfer',[[s.x0,returnY,moduleZ],[s.x0,s.sign*0.08,Math.max(0,moduleZ-transferRise)]],transferSlope,'structure_mounted_pair',m.returnSpacing,'derived',{plan_projection_m:transferPlan,slope_length_m:transferSlope});

  addSegment(segments,s.id,sequence++,'structure_drop',[[s.x0,s.sign*0.08,moduleZ],[s.x0,s.sign*0.08,Math.max(0,moduleZ-m.structureDrop)]],m.structureDrop,'free_air_drop',m.returnSpacing,'assumed');

  const groundZ=0;
  addSegment(segments,s.id,sequence++,'surface_or_trench_run',[[s.x0,s.sign*0.08,groundZ],[state.inverter.x,state.inverter.y,groundZ]],null,'buried_or_surface_pair',m.trenchSpacing,'geometry_and_assumed_formation');

  return segments;
}

function segmentPhysics(segment,m,conductorD) {
  const spacing=Math.max(segment.conductor_separation_mm,conductorD*1.000001);
  const tw=P.twoWire(spacing,conductorD,m.epsilonR);
  const length=segment.installed_conductor_length_m;
  return {
    ...segment,
    resistance_ohm:P.dcResistance(length,m.csa,m.temp),
    external_inductance_H:tw.externalInductancePerM*length,
    internal_inductance_H:tw.internalInductancePerM*length,
    loop_inductance_H:tw.inductancePerM*length,
    capacitance_F:tw.capacitancePerM*length,
    characteristic_impedance_ohm:tw.z0,
    propagation_velocity_m_s:tw.velocity,
    propagation_delay_s:length/tw.velocity
  };
}

function studyString(s,m,g) {
  const conductorD=P.conductorDiameterFromArea(m.csa);
  const segments=buildSegments(s,m,g).map(seg=>segmentPhysics(seg,m,conductorD));
  const installed=segments.reduce((a,x)=>a+x.installed_conductor_length_m,0);
  const R=segments.reduce((a,x)=>a+x.resistance_ohm,0);
  const L=segments.reduce((a,x)=>a+x.loop_inductance_H,0);
  const Cpair=segments.reduce((a,x)=>a+x.capacitance_F,0);
  const delay=segments.reduce((a,x)=>a+x.propagation_delay_s,0);
  const area=m.moduleWidth*m.moduleLength*m.wettedPct;
  const dielectric=m.wetState==='wet'?m.glassThickness:Math.max(m.glassThickness,4);
  const er=m.wetState==='wet'?m.glassEr:Math.max(2.5,m.glassEr/2);
  const cModule=P.parallelPlateCap(area,dielectric,er);
  const Cframe=cModule*m.modulesPerString;
  const V=m.modulesPerString*m.moduleVmp;
  const rise=m.riseUs*1e-6;
  const criterion=2*delay;
  const margin=rise/criterion;
  const firstZ=segments[0]?.characteristic_impedance_ohm || 0;
  const discontinuities=segments.slice(1).map((seg,i)=>({
    from_segment:segments[i].segment_id,to_segment:seg.segment_id,
    reflection_coefficient:(seg.characteristic_impedance_ohm-segments[i].characteristic_impedance_ohm)/(seg.characteristic_impedance_ohm+segments[i].characteristic_impedance_ohm)
  }));
  return {
    s,segments,conductorD,installed,R,L,Cpair,Cframe,cModule,V,delay,criterion,margin,
    distributed:rise<criterion,firstZ,wave:m.moduleImp*firstZ,
    mag:P.storedMagnetic(L,m.moduleImp),elec:P.storedElectric(Cframe,V),
    coldVoc:P.coldVoc(m.moduleVoc,m.modulesPerString,m.betaVoc,m.coldTemp),discontinuities,
    route_length:{value_m:installed,source:'segment_list',provenance:'derived'}
  };
}

function pairMppts(strings) {
  const pairs=[],left=[];
  const grouped=new Map();
  strings.forEach(s=>{const k=`${s.face}-${s.band}`;if(!grouped.has(k))grouped.set(k,[]);grouped.get(k).push(s);});
  grouped.forEach(group=>{
    group.sort((a,b)=>a.rank-b.rank);
    while(group.length>=2)pairs.push([group.shift(),group.shift()]);
    if(group.length)left.push(group.shift());
  });
  while(left.length>=2)pairs.push([left.shift(),left.shift()]);
  while(left.length)pairs.push([left.shift()]);
  return pairs.map((strings,i)=>({mppt:i+1,strings,crossBand:strings.length===2&&(strings[0].face!==strings[1].face||strings[0].band!==strings[1].band)}));
}

function bounds(g){return{minX:Math.min(-8,state.inverter.x-2),maxX:g.width+2,minY:-g.height/2-2,maxY:g.height/2+2};}
function resize(){const r=canvas.getBoundingClientRect(),d=devicePixelRatio||1;canvas.width=Math.round(r.width*d);canvas.height=Math.round(r.height*d);ctx.setTransform(d,0,0,d,0,0);}
function transform(g){const r=canvas.getBoundingClientRect(),b=bounds(g),pad=35,fit=Math.min((r.width-2*pad)/(b.maxX-b.minX),(r.height-2*pad)/(b.maxY-b.minY));const sc=fit*state.zoom,ox=pad-b.minX*fit+state.panX,oy=r.height/2+state.panY;return{sc,ox,oy,sx:x=>ox+x*sc,sy:y=>oy+y*sc,wx:x=>(x-ox)/sc,wy:y=>(y-oy)/sc};}
function drawPath(points,t,colour,width=2){ctx.beginPath();ctx.strokeStyle=colour;ctx.lineWidth=width;points.forEach((p,i)=>(i?ctx.lineTo(t.sx(p[0]),t.sy(p[1])):ctx.moveTo(t.sx(p[0]),t.sy(p[1]))));ctx.stroke();}

function drawSection(m,g){
  const w=section.width,h=section.height;sctx.clearRect(0,0,w,h);
  const theta=m.tilt*Math.PI/180, slope=m.ranksUp*g.rankPitchSlope, run=slope*Math.cos(theta), rise=slope*Math.sin(theta);
  const scale=Math.min(170/Math.max(run,1),120/Math.max(rise,1),8),cx=235,base=h-28;
  const dx=run*scale,dy=rise*scale;
  sctx.strokeStyle='#263342';sctx.beginPath();sctx.moveTo(12,base);sctx.lineTo(w-12,base);sctx.stroke();
  sctx.lineWidth=4;sctx.strokeStyle='#27d8ff';sctx.beginPath();sctx.moveTo(cx-dx,base);sctx.lineTo(cx,base-dy);sctx.lineTo(cx+dx,base);sctx.stroke();
  for(let side=-1;side<=1;side+=2){for(let r=0;r<m.ranksUp;r++){const f=(r+.5)/m.ranksUp,x=cx+side*dx*f,y=base-dy*(1-f);sctx.fillStyle=side<0?'#1a7895':'#51458c';sctx.fillRect(x-7,y-4,14,8);}}
  sctx.fillStyle='#ecf5ff';sctx.font='12px sans-serif';
  sctx.fillText(`${fmt(m.tilt,1)}° tilt · ${m.ranksUp} portrait ranks/face`,12,18);
  sctx.fillText(`Slope ${fmt(slope,3)} m · plan ${fmt(run,3)} m · rise ${fmt(rise,3)} m`,12,36);
}

function draw(m,g,study){
  resize();const t=transform(g);state.last={m,g,t};const r=canvas.getBoundingClientRect();ctx.clearRect(0,0,r.width,r.height);
  ctx.strokeStyle='#101a24';ctx.lineWidth=1;for(let x=0;x<=g.width;x+=10){ctx.beginPath();ctx.moveTo(t.sx(x),0);ctx.lineTo(t.sx(x),r.height);ctx.stroke();}
  ctx.strokeStyle='#44e18a';ctx.beginPath();ctx.moveTo(t.sx(0),t.sy(0));ctx.lineTo(t.sx(g.width),t.sy(0));ctx.stroke();

  // The canvas is only a readout of the generated feature collection.
  for(const f of g.featureCollection.features){
    if(f.properties.layer!=='rank') continue;
    const ring=f.geometry.coordinates[0],selected=study&&study.s.id===f.properties.string_id;
    ctx.fillStyle=selected?'#704d12':f.properties.face==='E'?'#0f3d50':'#302653';
    ctx.strokeStyle=selected?'#ffb347':f.properties.face==='E'?'#27d8ff':'#b891ff';
    ctx.beginPath();ring.forEach((p,i)=>(i?ctx.lineTo(t.sx(p[0]),t.sy(p[1])):ctx.moveTo(t.sx(p[0]),t.sy(p[1]))));ctx.closePath();ctx.fill();ctx.stroke();
    const x0=ring[0][0],x1=ring[1][0],y0=ring[0][1],y1=ring[2][1];
    if(t.sc>8){for(let i=1;i<m.modulesAlong;i++){const x=x0+i*g.modulePitch;ctx.beginPath();ctx.moveTo(t.sx(x),t.sy(y0));ctx.lineTo(t.sx(x),t.sy(y1));ctx.stroke();}}
    if(t.sc>12){ctx.fillStyle='#dcecff';ctx.font='10px ui-monospace,monospace';ctx.fillText(f.properties.string_id,t.sx(x0)+3,t.sy((y0+y1)/2)+3);}
    else if(t.sc>5){ctx.fillStyle='#dcecff';ctx.font='10px ui-monospace,monospace';ctx.fillText(`B${f.properties.band} R${f.properties.rank}`,t.sx(x0)+3,t.sy((y0+y1)/2)+3);}
  }
  if(study){
    for(const seg of study.segments){
      if(seg.segment_type==='coiled_surplus') continue;
      const colour=seg.segment_type==='along_rank_return'?'#27d8ff':'#ff5964';
      drawPath(seg.points_3d,t,colour,seg.segment_type==='surface_or_trench_run'?3:2);
    }
  }
  ctx.fillStyle='#ffb347';ctx.fillRect(t.sx(state.inverter.x)-8,t.sy(state.inverter.y)-16,16,32);
  ctx.fillStyle='#ffe1ad';ctx.font='11px sans-serif';ctx.fillText('INVERTER',t.sx(state.inverter.x)-28,t.sy(state.inverter.y)-22);
  set('zoomReadout',`${Math.round(state.zoom*100)}%`);drawSection(m,g);
}

function nearestString(wx,wy,g){return g.strings.find(s=>wx>=s.x0&&wx<=s.x1&&wy>=Math.min(s.yNear,s.yFar)&&wy<=Math.max(s.yNear,s.yFar))||null;}

function buildExport(m,g,pairs,selectedStudy){
  const studies=g.strings.map(s=>studyString(s,m,g));
  return {
    schema_version:'2.0.0-segment-chain',engine_version:P.formulaVersion,
    reliance:'Indicative topology and route-length study basis; competent-person review required.',
    inputs:{
      geometry:{modules_along_row:m.modulesAlong,ranks_per_face:m.ranksUp,faces_per_table:m.faces,tilt_deg:{value:m.tilt,provenance:'assumed'},module_width_m:{value:m.moduleWidth,provenance:'manufacturer'},module_length_m:{value:m.moduleLength,provenance:'manufacturer'},clamp_gap_m:{value:m.clampGap,provenance:'field_observed'},east_bands:m.eastBands,west_bands:m.westBands,inverter_position_m:{value:[state.inverter.x,state.inverter.y],provenance:'user_overridden_or_defaulted'}},
      formations:{module_interconnect_spacing_mm:{value:m.moduleSpacing,provenance:'assumed'},return_mode:{value:m.returnMode,provenance:'assumed'},return_spacing_mm:{value:m.returnSpacing,provenance:'assumed'},coil_length_m:{value:m.coilLength,provenance:'defaulted'},coil_diameter_mm:{value:m.coilDiameter,provenance:'defaulted'},trench_spacing_mm:{value:m.trenchSpacing,provenance:'assumed'}},
      analysis:{rise_time_us:{value:m.riseUs,provenance:'defaulted_standard_impulse_front'}}
    },
    feature_collection:g.featureCollection,
    mppt_allocations:pairs.map(p=>({mppt:p.mppt,string_ids:p.strings.map(s=>s.id),cross_band:p.crossBand})),
    strings:studies.map(st=>({string_id:st.s.id,route_length:st.route_length,segment_count:st.segments.length,segments:st.segments,results:{resistance_ohm:st.R,loop_inductance_H:st.L,distributed_capacitance_F:st.Cpair,module_frame_capacitance_F:st.Cframe,delay_s:st.delay,cold_voc_V:st.coldVoc}})),
    selected_string:selectedStudy?.s.id||null,
    aggregates:{string_count:studies.length,mppt_count:pairs.length,inverter_count:Math.ceil(studies.length/m.stringsPerInverter),site_installed_conductor_m:studies.reduce((a,s)=>a+s.installed,0)}
  };
}

function render(){
  const m=readInputs(),g=buildGeometry(m),pairs=pairMppts(g.strings);
  if(!state.selected||!g.strings.some(s=>s.id===state.selected))state.selected=g.strings[0]?.id||null;
  const selected=g.strings.find(s=>s.id===state.selected),st=selected?studyString(selected,m,g):null;
  state.model={m,g,pairs};state.study=st;draw(m,g,st);
  set('totalStrings',String(g.strings.length));set('footprint',`${fmt(g.width,1)} × ${fmt(g.height,1)} m`);
  if(st){
    set('routeLength',`${fmt(st.installed,2)} m`);set('segmentCount',String(st.segments.length));set('loopResistance',`${fmt(st.R,4)} Ω`);
    set('loopInductance',`${fmt(st.L*1e6,2)} µH`);set('frameCapacitance',`${fmt(st.Cframe*1e9,1)} nF`);
    set('z0',`${fmt(st.firstZ,1)} Ω`);set('waveAmplitude',`${fmt(st.wave,0)} V`);set('delay',`${fmt(st.delay*1e6,3)} µs`);
    set('roundTrip',`${fmt(2*st.delay*1e6,3)} µs round trip`);set('magneticEnergy',`${fmt(st.mag*1000,2)} mJ`);
    set('electricEnergy',`${fmt(st.elec,3)} J`);set('coldVoc',`${fmt(st.coldVoc,1)} V`);
    $('selectedSummary').innerHTML=`<strong>${st.s.id}</strong> · ${st.s.face==='E'?'east':'west'} face · band ${st.s.band+1} · rank ${st.s.rank+1} · ${m.modulesPerString} modules in series`;
    $('modelDecision').className='decision '+(st.distributed?'distributed':'');
    $('modelDecision').innerHTML=`<strong>${st.distributed?'DISTRIBUTED MODEL REQUIRED':'LUMPED MODEL ACCEPTABLE FOR THIS INPUT'}</strong><br>Rise time ${fmt(m.riseUs,3)} µs; criterion 2t<sub>d</sub> = ${fmt(st.criterion*1e6,3)} µs; margin t<sub>r</sub>/(2t<sub>d</sub>) = ${fmt(st.margin,2)}. The verdict is conditional on the displayed, provenance-tagged rise time.`;
  }
  const warnings=[];
  if(m.modulesPerString!==m.modulesAlong)warnings.push(`Modules per string (${m.modulesPerString}) differs from modules along row (${m.modulesAlong}); one rank is no longer one complete string.`);
  if(g.strings.length>m.mpptCount*2)warnings.push(`${g.strings.length} strings exceed ${m.mpptCount} MPPTs at two strings per MPPT.`);
  if(g.strings.length!==m.stringsPerInverter)warnings.push(`Generated ${g.strings.length} strings differs from declared strings per inverter ${m.stringsPerInverter}.`);
  pairs.filter(p=>p.crossBand).forEach(p=>{const a=studyString(p.strings[0],m,g).installed,b=studyString(p.strings[1],m,g).installed;warnings.push(`MPPT ${p.mppt}: forced cross-band pair ${p.strings[0].id}/${p.strings[1].id}; installed-length ratio ${fmt(Math.max(a,b)/Math.max(.001,Math.min(a,b)),2)}.`);});
  $('warningBox').innerHTML=warnings.map(w=>`<div class="warning">${w}</div>`).join('');
  if(st){
    const segmentLines=st.segments.map(seg=>`${String(seg.sequence_index).padStart(3,'0')}  ${seg.segment_type.padEnd(24)} ${fmt(seg.installed_conductor_length_m,3).padStart(10)} m  D=${fmt(seg.conductor_separation_mm,1).padStart(7)} mm  L=${fmt(seg.loop_inductance_H*1e6,3).padStart(9)} µH  Z0=${fmt(seg.characteristic_impedance_ohm,1).padStart(7)} Ω  ${seg.provenance}`);
    const mpptLines=pairs.map(p=>`MPPT ${String(p.mppt).padStart(2,'0')}  ${p.strings.map(x=>x.id).join(' + ')}${p.crossBand?'  [CROSS-BAND]':''}`);
    $('trace').textContent=[
      `FORMULA ARTEFACT ${P.formulaVersion}`,
      `A-FRAME: ${m.modulesAlong} modules along × ${m.ranksUp} portrait ranks × ${m.faces} faces; tilt ${m.tilt}°`,
      `SLOPE RANK PITCH = ${m.moduleLength} + ${m.clampGap} = ${fmt(g.rankPitchSlope,3)} m; PLAN PROJECTION = ${fmt(g.rankPitchPlan,3)} m`,
      `CONDUCTOR DIAMETER FROM CSA = ${fmt(st.conductorD,3)} mm; cable OD ${m.cableOd} mm is not used in acosh geometry.`,
      `INTERNAL LOOP INDUCTANCE = μ0/(4π) per metre at low frequency; high-frequency reduction remains a validity warning.`,
      `ROUTE LENGTH = Σ segment installed lengths = ${fmt(st.installed,3)} m; no final string-length input exists.`,
      '', 'SEGMENTS', ...segmentLines, '', 'MPPT ALLOCATION', ...mpptLines
    ].join('\n');
  }
}

ids.forEach(id=>$(id).addEventListener('input',render));
$('returnMode').addEventListener('change',render);
$('wetState').addEventListener('change',render);
$('reset').onclick=()=>location.reload();
$('export').onclick=()=>{
  const {m,g,pairs}=state.model;
  const payload=buildExport(m,g,pairs,state.study);
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));
  a.download='dc-string-segment-study-basis.json';a.click();URL.revokeObjectURL(a.href);
};
canvas.addEventListener('wheel',e=>{e.preventDefault();state.zoom=Math.max(.25,Math.min(16,state.zoom*Math.exp(-e.deltaY*.001)));render();},{passive:false});
canvas.addEventListener('mousedown',e=>{
  const {t,g}=state.last,wx=t.wx(e.offsetX),wy=t.wy(e.offsetY);
  if(Math.hypot(wx-state.inverter.x,wy-state.inverter.y)<1.5)state.dragInv=true;
  else{const s=nearestString(wx,wy,g);if(s){state.selected=s.id;render();}else{state.panning=true;state.lastMouse={x:e.clientX,y:e.clientY};}}
});
window.addEventListener('mousemove',e=>{
  if(state.dragInv){const rect=canvas.getBoundingClientRect();state.inverter.x=state.last.t.wx(e.clientX-rect.left);state.inverter.y=state.last.t.wy(e.clientY-rect.top);render();}
  else if(state.panning){state.panX+=e.clientX-state.lastMouse.x;state.panY+=e.clientY-state.lastMouse.y;state.lastMouse={x:e.clientX,y:e.clientY};render();}
});
window.addEventListener('mouseup',()=>{state.dragInv=false;state.panning=false;});
window.addEventListener('resize',render);
render();
