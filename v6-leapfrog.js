"use strict";
(()=>{
  const baseInput=input;
  const baseExternalLengths=externalLengths;
  const baseStudy=study;
  const basePaths=paths;

  input=function(){
    const m=baseInput();
    const modeEl=$("wiringMode");
    const spacingEl=$("leapfrogSpacing");
    m.wiringMode=modeEl?modeEl.value:"sequential";
    m.leapfrogSpacing=Math.max(0.1,spacingEl?Number(spacingEl.value):40);
    return m;
  };

  externalLengths=function(s){
    const ext=baseExternalLengths(s);
    const mode=$("wiringMode")?.value||"sequential";
    if(mode==="leapfrog"){
      return{positive:ext.near,negative:ext.near,near:ext.near,far:ext.far};
    }
    return ext;
  };

  study=function(s,m){
    const st=baseStudy(s,m);
    st.wiringMode=m.wiringMode;
    st.rowSpan=Math.abs(s.x1-s.x0);
    st.externalCableAvoided=m.wiringMode==="leapfrog"?Math.max(0,st.ext.far-st.ext.near):0;
    if(m.wiringMode==="leapfrog"){
      const dExt=P.conductorDiameterFromArea(m.csa);
      const dLead=P.conductorDiameterFromArea(m.leadCsa);
      const twExt=safeTwoWire(m.externalSpacing,dExt,m.epsilonR);
      const twModule=safeTwoWire(m.leapfrogSpacing,dLead,m.epsilonR);
      st.L=twExt.inductancePerM*st.externalTotal+twModule.inductancePerM*st.moduleLeadTotal;
      st.Cdiff=twExt.capacitancePerM*st.externalTotal+twModule.capacitancePerM*st.moduleLeadTotal;
      st.area=st.ext.near*(m.externalSpacing/1000)+st.rowSpan*(m.leapfrogSpacing/1000);
      st.delay=Math.max(st.ext.positive,st.ext.negative)/twExt.velocity+st.moduleLeadTotal/(2*twModule.velocity);
      st.criterion=2*st.delay;
      const rise=m.riseUs*1e-6;
      st.distributed=rise<st.criterion;
      st.margin=rise/st.criterion;
    }
    return st;
  };

  paths=function(st,m){
    if(m.wiringMode!=="leapfrog")return basePaths(st,m);
    const s=st.s;
    const displayOff=Math.max(.045,Math.min(.12,m.moduleLength*.025));
    const plusY=s.y-displayOff,minusY=s.y+displayOff,nearX=s.x0,farX=s.x1;
    return{
      plus:[[state.inverter.x,plusY],[nearX,plusY]],
      module:[[nearX,s.y],[farX,s.y]],
      minus:[[nearX,minusY],[state.inverter.x,minusY]],
      polygon:[[state.inverter.x,plusY],[nearX,plusY],[farX,s.y-displayOff*.3],[farX,s.y+displayOff*.3],[nearX,minusY],[state.inverter.x,minusY]]
    };
  };

  function cable(ctx,points,width=4){
    ctx.save();
    ctx.lineJoin="round";ctx.lineCap="round";
    ctx.strokeStyle="rgba(232,244,252,.72)";ctx.lineWidth=width+2;
    ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();
    ctx.strokeStyle="#000";ctx.lineWidth=width;
    ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.stroke();
    ctx.restore();
  }

  function drawModuleRow(ctx,y,title,leap,m){
    const c=$("wiringComparison"),W=c.width;
    const invX=62,rowX=170,rowRight=W-48,count=Math.max(2,m.modulesPerString);
    const pitch=(rowRight-rowX)/count,moduleW=Math.max(5,pitch-2),moduleH=54;
    ctx.fillStyle="#d9f4ff";ctx.font="800 20px ui-monospace,monospace";ctx.fillText(title,20,y+34);
    ctx.fillStyle="#ffb347";ctx.fillRect(invX,y+4,36,112);
    ctx.fillStyle="#ffd79b";ctx.font="700 12px ui-monospace,monospace";ctx.fillText("INV",invX+5,y-5);
    for(let i=0;i<count;i++){
      const x=rowX+i*pitch;
      ctx.fillStyle=i%2?"#18394b":"#154a61";ctx.fillRect(x,y,moduleW,moduleH);
      ctx.strokeStyle="#66dcff";ctx.lineWidth=1;ctx.strokeRect(x,y,moduleW,moduleH);
      ctx.fillStyle="#000";ctx.fillRect(x+moduleW/2-2.5,y+11,5,4);
    }
    ctx.font="800 15px ui-monospace,monospace";
    if(!leap){
      cable(ctx,[[invX+36,y+20],[rowX,y+20]],4);
      cable(ctx,[[rowRight-pitch/2,y+42],[rowRight-pitch/2,y+92],[invX+36,y+92]],4);
      ctx.fillStyle="#fff";ctx.fillText("+",invX+46,y+17);ctx.fillText("−",rowRight-pitch/2+8,y+45);
      ctx.fillStyle="#ff6d79";ctx.fillText("one far-end return ≈ one complete row span",rowX,y+116);
    }else{
      cable(ctx,[[invX+36,y+19],[rowX,y+19]],4);
      cable(ctx,[[invX+36,y+43],[rowX+pitch,y+43]],4);
      ctx.fillStyle="#fff";ctx.fillText("+",invX+46,y+16);ctx.fillText("−",invX+46,y+48);
      for(let i=0;i<count-2;i+=2){
        const a=rowX+i*pitch+moduleW/2,b=rowX+(i+2)*pitch+moduleW/2;
        cable(ctx,[[a,y+14],[b,y+14]],2);
      }
      for(let i=1;i<count-2;i+=2){
        const a=rowX+i*pitch+moduleW/2,b=rowX+(i+2)*pitch+moduleW/2;
        cable(ctx,[[a,y+48],[b,y+48]],2);
      }
      const a=rowX+(count-2)*pitch+moduleW/2,b=rowX+(count-1)*pitch+moduleW/2;
      cable(ctx,[[a,y+14],[b,y+48]],2);
      ctx.fillStyle="#53e28b";ctx.fillText("both free terminals emerge at inverter end",rowX,y+88);
    }
  }

  function drawImpact(){
    const c=$("wiringComparison"),summary=$("wiringImpactSummary");
    if(!c||!summary)return;
    const m=input(),g=geometry(m),ctx=c.getContext("2d");
    ctx.clearRect(0,0,c.width,c.height);ctx.fillStyle="#03070b";ctx.fillRect(0,0,c.width,c.height);
    drawModuleRow(ctx,62,"Sequential",false,m);
    drawModuleRow(ctx,254,"Leapfrog",true,m);
    const savingPerString=g.rowLength;
    const savingPerInverter=savingPerString*g.strings.length;
    summary.innerHTML=`<strong>${m.wiringMode==="leapfrog"?"LEAPFROG ACTIVE":"SEQUENTIAL ACTIVE"}</strong><br>`+
      `Distance to nearest terminals: ${fmt(m.nearAllowance,2)} m.<br>`+
      `Derived row span: ${fmt(g.rowLength,2)} m.<br>`+
      `Leapfrog removes approximately ${fmt(savingPerString,2)} m of external 6 mm² cable per string, or ${fmt(savingPerInverter/1000,3)} km across this ${g.strings.length}-string inverter archetype.`;
  }

  const redraw=()=>{render();drawImpact();};
  ["wiringMode","leapfrogSpacing"].forEach(id=>$(id)?.addEventListener("input",redraw));
  ids.forEach(id=>$(id)?.addEventListener("input",drawImpact));
  window.addEventListener("resize",drawImpact);
  redraw();
})();
