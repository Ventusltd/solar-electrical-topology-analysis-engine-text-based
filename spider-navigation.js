'use strict';
(function(){
  const wrap=document.querySelector('.canvas-wrap');
  const canvas=document.getElementById('scene');
  const zoomIn=document.getElementById('zoomIn');
  const zoomOut=document.getElementById('zoomOut');
  const zoomReset=document.getElementById('zoomReset');
  const zoomPercent=document.getElementById('zoomPercent');
  if(!wrap||!canvas)return;

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
    const s=nearest(w.x,w.y,state.last.g);if(s){state.selected=s.id;render();label();}
    e.preventDefault();e.stopImmediatePropagation();
  }
  wrap.addEventListener('pointerup',finish,true);
  wrap.addEventListener('pointercancel',e=>{down=false;state.panning=false;state.dragInv=false;wrap.classList.remove('dragging');e.stopImmediatePropagation();},true);
  wrap.addEventListener('wheel',e=>{if(Math.abs(e.deltaY)<1)return;e.preventDefault();e.stopImmediatePropagation();zoomTo(scale*(e.deltaY<0?1.12:.89),e.clientX,e.clientY);},{capture:true,passive:false});

  zoomIn?.addEventListener('click',()=>zoomTo(scale+STEP));
  zoomOut?.addEventListener('click',()=>zoomTo(scale-STEP));
  zoomReset?.addEventListener('click',()=>zoomTo(1));

  function centre(){wrap.scrollLeft=Math.max(0,(canvas.clientWidth-wrap.clientWidth)/2);wrap.scrollTop=Math.max(0,(canvas.clientHeight-wrap.clientHeight)/2);}
  requestAnimationFrame(()=>{setSize(1);requestAnimationFrame(centre);});
  window.addEventListener('resize',()=>requestAnimationFrame(centre));
})();