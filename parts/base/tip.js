/* tooltip */
var tip=document.getElementById("tip");
function showTip(el){tip.textContent=el.getAttribute("data-tip");tip.hidden=false;var r=el.getBoundingClientRect(),tw=tip.offsetWidth,th=tip.offsetHeight;
  var x=Math.min(window.innerWidth-tw-8,Math.max(8,r.left+r.width/2-tw/2)),y=r.top-th-10; if(y<8)y=r.bottom+10; tip.style.left=x+"px";tip.style.top=y+"px";tip.style.whiteSpace="pre-line"}
document.addEventListener("pointerover",function(e){var d=e.target.closest&&e.target.closest("[data-tip]");if(d)showTip(d)});
document.addEventListener("pointerout",function(e){if(e.target.closest&&e.target.closest("[data-tip]"))tip.hidden=true});
document.addEventListener("focusin",function(e){if(e.target.matches&&e.target.matches("[data-tip]"))showTip(e.target)});
document.addEventListener("focusout",function(){tip.hidden=true});

