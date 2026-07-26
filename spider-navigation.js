'use strict';
(function(){
  const wrap=document.querySelector('.canvas-wrap');
  const canvas=document.getElementById('scene');
  if(!wrap||!canvas)return;

  let down=false,startX=0,startY=0,startLeft=0,startTop=0,moved=false;

  function point(e){const r=canvas.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top};}
  function world(e){const p=point(e);const t=state&&state.last&&state.last.t;return t?{x:t.wx(p.x),y:t.wy(p.y)}:null;}

  wrap.addEventListener('pointerdown',e=>{
    if(e.target.closest('button,input,select,a'))return;
    e.preventDefault();e.stopImmediatePropagation();
    state.panning=false;state.dragInv=false;state.pinchStart=null;
    if(state.pointers&&state.pointers.clear)state.pointers.clear();
    down=true;moved=false;startX=e.clientX;startY=e.clientY;startLeft=wrap.scrollLeft;startTop=wrap.scrollTop;
    wrap.classList.add('dragging');wrap.setPointerCapture?.(e.pointerId);
  },true);

  wrap.addEventListener('pointermove',e=>{
    if(!down)return;
    const dx=e.clientX-startX,dy=e.clientY-startY;
    if(Math.abs(dx)+Math.abs(dy)>5)moved=true;
    wrap.scrollLeft=startLeft-dx;wrap.scrollTop=startTop-dy;
    e.preventDefault();e.stopImmediatePropagation();
  },true);

  function finish(e){
    if(!down)return;
    down=false;wrap.classList.remove('dragging');state.panning=false;state.dragInv=false;
    try{wrap.releasePointerCapture?.(e.pointerId);}catch(_){ }
    if(moved){e.preventDefault();e.stopImmediatePropagation();return;}
    const w=world(e);if(!w||!state.last){e.stopImmediatePropagation();return;}
    if(state.drawMode){
      if(!state.drawStart){state.drawStart=[w.x,w.y];document.getElementById('drawStatus').innerHTML='Ruler: <strong>CLICK END POINT</strong>';}
      else{addManual(state.drawStart,[w.x,w.y]);state.drawStart=null;document.getElementById('drawStatus').innerHTML='Ruler: <strong>CLICK START POINT</strong>';}
      render();e.preventDefault();e.stopImmediatePropagation();return;
    }
    const s=nearest(w.x,w.y,state.last.g);if(s){state.selected=s.id;render();}
    e.preventDefault();e.stopImmediatePropagation();
  }
  wrap.addEventListener('pointerup',finish,true);
  wrap.addEventListener('pointercancel',e=>{down=false;state.panning=false;state.dragInv=false;wrap.classList.remove('dragging');e.stopImmediatePropagation();},true);

  wrap.addEventListener('wheel',e=>{e.stopImmediatePropagation();},{capture:true,passive:true});

  function centre(){
    wrap.scrollLeft=Math.max(0,(canvas.clientWidth-wrap.clientWidth)/2);
    wrap.scrollTop=Math.max(0,(canvas.clientHeight-wrap.clientHeight)/2);
  }
  requestAnimationFrame(()=>{state.zoom=1;state.panX=0;state.panY=0;render();requestAnimationFrame(centre);});
  window.addEventListener('resize',()=>requestAnimationFrame(centre));
})();
