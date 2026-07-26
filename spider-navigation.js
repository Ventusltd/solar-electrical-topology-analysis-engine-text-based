'use strict';

/*
 * Compatibility repair: the current V6/V7 app.js lost the nearest() hit-test
 * function that existed in the last working renderer. Both the canvas pointer
 * handler and Spider-style navigation call it. Keep the fallback here so the
 * selector works without disturbing the calculation engine.
 */
if(typeof window.nearest!=='function'){
  window.nearest=function nearest(wx,wy,g){
    if(!g||!Array.isArray(g.strings))return null;
    return g.strings.find(s=>
      wx>=s.x0&&wx<=s.x1&&
      wy>=Math.min(s.y0,s.y1)&&wy<=Math.max(s.y0,s.y1)
    )||null;
  };
}

(function(){
  const workbench=document.querySelector('.workbench');
  const wrap=document.querySelector('.canvas-wrap');
  const canvas=document.getElementById('scene');
  const zoomIn=document.getElementById('zoomIn');
  const zoomOut=document.getElementById('zoomOut');
  const zoomReset=document.getElementById('zoomReset');
  const zoomPercent=document.getElementById('zoomPercent');
  if(!wrap||!canvas)return;

  function installTechnicalCommentary(){
    if(!workbench||document.getElementById('workbenchTabs'))return;

    const style=document.createElement('style');
    style.textContent=`
      .workbench-tabs{position:sticky;top:0;z-index:20;display:flex;gap:.5rem;padding:.7rem .8rem;background:rgba(7,13,20,.96);border:1px solid #263342;border-radius:10px;margin-bottom:.8rem;backdrop-filter:blur(8px)}
      .workbench-tab{appearance:none;border:1px solid #3a4b5e;background:#111b27;color:#b9c8d8;border-radius:8px;padding:.65rem 1rem;font-weight:800;letter-spacing:.035em;cursor:pointer}
      .workbench-tab[aria-selected="true"]{background:#e9f3ff;color:#07101a;border-color:#e9f3ff}
      .workbench-panel[hidden]{display:none!important}
      .technical-commentary{max-width:1100px;margin:0 auto;padding:clamp(1rem,2vw,2rem)}
      .technical-commentary h2{margin-top:0;font-size:clamp(1.4rem,3vw,2.2rem)}
      .technical-commentary h3{margin-top:1.6rem;color:#dbeaff}
      .technical-commentary p,.technical-commentary li{line-height:1.65;color:#c4d0dc}
      .technical-commentary .technical-lead{font-size:1.08rem;color:#f2f7fb}
      .technical-commentary .technical-rule{border-left:4px solid #ffb347;background:#141d27;padding:1rem 1.1rem;margin:1rem 0;border-radius:0 8px 8px 0}
      .technical-commentary .technical-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem;margin:1rem 0}
      .technical-commentary article{background:#0d1620;border:1px solid #293a4b;border-radius:10px;padding:1rem}
      .technical-commentary code{color:#ffe0ad;background:#101923;padding:.1rem .3rem;border-radius:4px}
      .technical-commentary .evidence{font-size:.9rem;color:#95a9bc;border-top:1px solid #263342;padding-top:1rem;margin-top:2rem}
      @media(max-width:720px){.workbench-tabs{position:relative}.workbench-tab{flex:1;padding:.6rem .4rem;font-size:.78rem}.technical-commentary{padding:.8rem}}
    `;
    document.head.appendChild(style);

    const tabs=document.createElement('div');
    tabs.id='workbenchTabs';
    tabs.className='workbench-tabs';
    tabs.setAttribute('role','tablist');
    tabs.innerHTML=`
      <button class="workbench-tab" id="engineeringTab" role="tab" aria-selected="true" aria-controls="engineeringPanel">ENGINEERING WORKBENCH</button>
      <button class="workbench-tab" id="commentaryTab" role="tab" aria-selected="false" aria-controls="commentaryPanel">TECHNICAL COMMENTARY</button>
    `;

    const engineering=document.createElement('div');
    engineering.id='engineeringPanel';
    engineering.className='workbench-panel';
    engineering.setAttribute('role','tabpanel');
    engineering.setAttribute('aria-labelledby','engineeringTab');

    while(workbench.firstChild)engineering.appendChild(workbench.firstChild);
    workbench.appendChild(tabs);
    workbench.appendChild(engineering);

    const commentary=document.createElement('div');
    commentary.id='commentaryPanel';
    commentary.className='workbench-panel technical-commentary';
    commentary.setAttribute('role','tabpanel');
    commentary.setAttribute('aria-labelledby','commentaryTab');
    commentary.hidden=true;
    commentary.innerHTML=`
      <h2>Technical commentary</h2>
      <p class="technical-lead">This engine studies the electrical consequences of physical PV topology. The standards require designers to control capacitance to earth, insulation monitoring, conductive-loop area, transient overvoltage, cable temperature, voltage drop, reverse current and environmental exposure, but they do not provide one universal geometric calculation engine.</p>

      <div class="technical-rule"><strong>Primary standards-led purpose</strong><br>Topology → module and cable capacitance to earth → IMD compatibility and insulation-fault protection.<br>Geometry → loop area → differential and common-mode inductance → transient overvoltage and SPD assessment.</div>

      <div class="technical-grid">
        <article><h3>Capacitance and IMD</h3><p>For large arrays, capacitance to earth must be treated as a device-selection input. The model must keep <code>C+earth</code>, <code>C−earth</code>, common-mode capacitance and positive-to-negative differential capacitance separate. Capacitance seen by the IMD depends on the actual inverter input and monitoring boundary.</p></article>
        <article><h3>Wet and dry states</h3><p>Wet conditions can increase leakage, lower insulation resistance and change capacitance. No hidden fixed wet multiplier is a standards value. Dry and wet values must be measured, manufacturer-declared, geometry-derived or visibly assumed.</p></article>
        <article><h3>Loop geometry</h3><p>Positive and negative routes must be represented as a closed circuit. Minimum conductive-loop area is a design objective, so local separation, crossings, structure drops and surplus coils matter. One average spacing cannot describe the whole circuit.</p></article>
        <article><h3>Common and differential modes</h3><p>Differential inductance follows the positive/negative loop. Common-mode behaviour follows both poles against frame, bonding network and earth. The bonding-conductor route therefore belongs in the topology.</p></article>
        <article><h3>SPD electrical distance</h3><p>SPD effectiveness depends on routed electrical distance and connection lead inductance. The engine should compare the furthest module route with the applicable critical-length method and include the residual voltage contribution from SPD leads.</p></article>
        <article><h3>Complete circuit loss</h3><p>Voltage drop and power loss must include both external conductors, module factory leads, extension leads, connectors, terminations and series devices. Temperatures should be applied by segment rather than as one whole-string value.</p></article>
      </div>

      <h3>Capacitance model discipline</h3>
      <p>The present geometry-derived dry and wet values are screening scenarios, not universal module constants. Module glass, cell area, frame and rail coupling, cable installation, water films, soil, trays, structure and inverter EMC components all affect the result. The next model shall show input provenance and uncertainty and shall compare total array capacitance with the selected IMD maximum permissible system capacitance.</p>

      <h3>Inverter input topology</h3>
      <p>Independent MPPT inputs with reverse-current blocking and inputs paralleled onto a common DC bus are not electrically equivalent. They change the capacitance aggregation boundary, reverse-current paths, isolation requirements and the array or sub-array definition. Where the inverter architecture is unknown, the engine should display bounding cases rather than choose one silently.</p>

      <h3>Transmission-line studies</h3>
      <p>Propagation delay, characteristic impedance, travelling-wave reflection and stored electric or magnetic energy are advanced engineering layers. They are useful for testing the standards-required outcomes, but must be labelled as research or standards-guided calculations rather than direct normative formulae.</p>

      <h3>Evidence and reliance</h3>
      <p>Every result should identify whether it is a normative criterion, a standards-guided engineering calculation or an advanced model. Manufacturer data, measured geometry and competent-person review remain necessary before equipment selection or a project-specific compliance conclusion.</p>

      <p class="evidence">The detailed next-study work packages are recorded in the repository README. This tab is the browser-facing technical note, not a reproduction of licensed standards text and not a design certificate.</p>
    `;
    workbench.appendChild(commentary);

    const engineeringTab=document.getElementById('engineeringTab');
    const commentaryTab=document.getElementById('commentaryTab');
    function select(which){
      const showEngineering=which==='engineering';
      engineering.hidden=!showEngineering;
      commentary.hidden=showEngineering;
      engineeringTab.setAttribute('aria-selected',String(showEngineering));
      commentaryTab.setAttribute('aria-selected',String(!showEngineering));
      if(showEngineering){
        requestAnimationFrame(()=>{
          if(typeof render==='function')render();
          requestAnimationFrame(centre);
        });
      }
    }
    engineeringTab.addEventListener('click',()=>select('engineering'));
    commentaryTab.addEventListener('click',()=>select('commentary'));
  }

  const BASE_W=2200,BASE_H=1350,MIN=.45,MAX=2.4,STEP=.25;
  let scale=1,down=false,startX=0,startY=0,startLeft=0,startTop=0,moved=false,anim=0;
  const clamp=v=>Math.max(MIN,Math.min(MAX,v));
  function point(e){const r=canvas.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top};}
  function world(e){const p=point(e);const t=state&&state.last&&state.last.t;return t?{x:t.wx(p.x),y:t.wy(p.y)}:null;}
  function label(){if(zoomPercent)zoomPercent.textContent=`${Math.round(scale*100)}%`;const z=document.getElementById('zoomReadout');if(z)z.textContent=`${Math.round(scale*100)}% · DRAG TO MOVE · USE − / + TO ZOOM`;}
  function setSize(s){scale=s;canvas.style.width=`${BASE_W*s}px`;canvas.style.height=`${BASE_H*s}px`;state.zoom=1;state.panX=0;state.panY=0;render();label();}

  function zoomTo(target,clientX,clientY){
    target=clamp(target);if(Math.abs(target-scale)<.001)return;
    cancelAnimationFrame(anim);
    const rect=wrap.getBoundingClientRect();
    const vx=(clientX==null?rect.left+wrap.clientWidth/2:clientX)-rect.left;
    const vy=(clientY==null?rect.top+wrap.clientHeight/2:clientY)-rect.top;
    const anchorX=(wrap.scrollLeft+vx)/(BASE_W*scale);
    const anchorY=(wrap.scrollTop+vy)/(BASE_H*scale);
    const from=scale,start=performance.now(),duration=180;
    function frame(now){
      const p=Math.min(1,(now-start)/duration),ease=1-Math.pow(1-p,3),s=from+(target-from)*ease;
      setSize(s);
      wrap.scrollLeft=anchorX*(BASE_W*s)-vx;
      wrap.scrollTop=anchorY*(BASE_H*s)-vy;
      if(p<1)anim=requestAnimationFrame(frame);else{scale=target;label();}
    }
    anim=requestAnimationFrame(frame);
  }

  wrap.addEventListener('pointerdown',e=>{
    if(e.target.closest('button,input,select,a,.zoom-toolbar'))return;
    e.preventDefault();e.stopImmediatePropagation();
    state.panning=false;state.dragInv=false;state.pinchStart=null;
    if(state.pointers&&state.pointers.clear)state.pointers.clear();
    down=true;moved=false;startX=e.clientX;startY=e.clientY;startLeft=wrap.scrollLeft;startTop=wrap.scrollTop;
    wrap.classList.add('dragging');wrap.setPointerCapture?.(e.pointerId);
  },true);
  wrap.addEventListener('pointermove',e=>{
    if(!down)return;const dx=e.clientX-startX,dy=e.clientY-startY;
    if(Math.abs(dx)+Math.abs(dy)>5)moved=true;
    wrap.scrollLeft=startLeft-dx;wrap.scrollTop=startTop-dy;e.preventDefault();e.stopImmediatePropagation();
  },true);
  function finish(e){
    if(!down)return;down=false;wrap.classList.remove('dragging');state.panning=false;state.dragInv=false;
    try{wrap.releasePointerCapture?.(e.pointerId);}catch(_){ }
    if(moved){e.preventDefault();e.stopImmediatePropagation();return;}
    const w=world(e);if(!w||!state.last){e.stopImmediatePropagation();return;}
    if(state.drawMode){
      if(!state.drawStart){state.drawStart=[w.x,w.y];document.getElementById('drawStatus').innerHTML='Ruler: <strong>CLICK END POINT</strong>';}
      else{addManual(state.drawStart,[w.x,w.y]);state.drawStart=null;document.getElementById('drawStatus').innerHTML='Ruler: <strong>CLICK START POINT</strong>';}
      render();label();e.preventDefault();e.stopImmediatePropagation();return;
    }
    const s=window.nearest(w.x,w.y,state.last.g);if(s){state.selected=s.id;render();label();}
    e.preventDefault();e.stopImmediatePropagation();
  }
  wrap.addEventListener('pointerup',finish,true);
  wrap.addEventListener('pointercancel',e=>{down=false;state.panning=false;state.dragInv=false;wrap.classList.remove('dragging');e.stopImmediatePropagation();},true);
  wrap.addEventListener('wheel',e=>{if(Math.abs(e.deltaY)<1)return;e.preventDefault();e.stopImmediatePropagation();zoomTo(scale*(e.deltaY<0?1.12:.89),e.clientX,e.clientY);},{capture:true,passive:false});

  zoomIn?.addEventListener('click',()=>zoomTo(scale+STEP));
  zoomOut?.addEventListener('click',()=>zoomTo(scale-STEP));
  zoomReset?.addEventListener('click',()=>zoomTo(1));

  function centre(){wrap.scrollLeft=Math.max(0,(canvas.clientWidth-wrap.clientWidth)/2);wrap.scrollTop=Math.max(0,(canvas.clientHeight-wrap.clientHeight)/2);}
  installTechnicalCommentary();
  requestAnimationFrame(()=>{setSize(1);requestAnimationFrame(centre);});
  window.addEventListener('resize',()=>requestAnimationFrame(centre));
})();
