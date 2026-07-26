'use strict';
(function(){
  const canvas=document.getElementById('scene');
  const buttons=[...document.querySelectorAll('[data-view-zoom]')];
  if(!canvas||typeof state==='undefined'||typeof render!=='function')return;

  function applyView(zoom){
    state.zoom=zoom;
    state.panX=0;
    state.panY=0;
    state.panning=false;
    state.dragInv=false;
    state.pinchStart=null;
    if(state.pointers&&state.pointers.clear)state.pointers.clear();
    buttons.forEach(b=>b.classList.toggle('active',Number(b.dataset.viewZoom)===zoom));
    render();
  }

  buttons.forEach(button=>button.addEventListener('click',()=>applyView(Number(button.dataset.viewZoom))));

  // Disable canvas gesture navigation while preserving ordinary page scrolling.
  canvas.style.touchAction='pan-y';
  canvas.addEventListener('wheel',event=>{event.preventDefault();event.stopImmediatePropagation();},{capture:true,passive:false});
  canvas.addEventListener('pointermove',event=>{event.stopImmediatePropagation();},{capture:true});
  canvas.addEventListener('gesturestart',event=>{event.preventDefault();event.stopImmediatePropagation();},{capture:true,passive:false});
  canvas.addEventListener('gesturechange',event=>{event.preventDefault();event.stopImmediatePropagation();},{capture:true,passive:false});

  applyView(1.6);
})();
