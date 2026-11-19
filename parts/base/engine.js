/* ---------- reveal & timers ---------- */
document.querySelectorAll("[data-reveal]").forEach(function(b){b.addEventListener("click",function(){var t=document.getElementById(b.getAttribute("data-reveal"));t.hidden=!t.hidden;b.textContent=t.hidden?(b.dataset.lab||b.textContent):"收起答案";if(!b.dataset.lab)b.dataset.lab=b.textContent==="收起答案"?"顯示答案":b.textContent})});
document.querySelectorAll("[data-reveal]").forEach(function(b){b.dataset.lab=b.textContent});
document.querySelectorAll(".timer").forEach(function(t){
  var total=Number(t.dataset.min)*60,left=total,iv=null,tv=t.querySelector(".tv");
  function show(){var m=Math.floor(left/60),s=left%60;tv.textContent=(m<10?"0":"")+m+":"+(s<10?"0":"")+s;t.classList.toggle("done",left===0)}
  t.addEventListener("click",function(e){var a=e.target.getAttribute("data-t");if(!a)return;
    if(a==="go"&&!iv&&left>0){iv=setInterval(function(){left=Math.max(0,left-1);show();if(!left){clearInterval(iv);iv=null}},1000)}
    if(a==="pause"){clearInterval(iv);iv=null}
    if(a==="reset"){clearInterval(iv);iv=null;left=total}
    show()});
  show();
});

/* ---------- commitment card (per-viewer storage) ---------- */
(function(){
  var f=document.getElementById("pdca"); if(!f)return; var KEY="icope-pdca-v1";
  var els=f.querySelectorAll("input,textarea");
  try{var d=JSON.parse(localStorage.getItem(KEY)||"{}");els.forEach(function(e){if(d[e.id])e.value=d[e.id]})}catch(e){}
  f.addEventListener("input",function(){var d={};els.forEach(function(e){d[e.id]=e.value});try{localStorage.setItem(KEY,JSON.stringify(d))}catch(e){}});
  f.addEventListener("submit",function(e){e.preventDefault()});
  document.getElementById("pdcaClear").addEventListener("click",function(){els.forEach(function(e){e.value=""});try{localStorage.removeItem(KEY)}catch(e){}});
})();

/* ---------- deck engine ---------- */
var slides=[].slice.call(document.querySelectorAll(".slide")),N=slides.length,cur=0;
var body=document.body,mq=window.matchMedia("(max-width: 820px), (max-height: 500px)");
slides.forEach(function(s,i){var p=s.querySelector(".pg");if(p)p.textContent=String(i+1).padStart(2,"0")+" / "+N});
function sizeIt(){
  var W=window.innerWidth,H=window.innerHeight,u;
  if(mq.matches){body.classList.add("scroll");u=Math.max(0.6,Math.min(1,W/640))}
  else{body.classList.remove("scroll");u=Math.min(W/1300,(H-46)/736)}
  document.documentElement.style.setProperty("--u",u.toFixed(4)+"px");
}
function go(i,push){
  cur=Math.max(0,Math.min(N-1,i));
  slides.forEach(function(s,k){s.classList.toggle("on",k===cur)});
  document.getElementById("count").textContent=(cur+1)+" / "+N;
  document.getElementById("progi").style.width=((cur+1)/N*100)+"%";
  if(body.classList.contains("shownotes"))fillNotes();
  tip.hidden=true;
  try{history.replaceState(null,"","#s"+(cur+1))}catch(e){}
}
function fillNotes(){var n=slides[cur].querySelector("aside.notes"),p=document.getElementById("notesPanel");p.innerHTML=n?n.innerHTML:"<h4>講者備註</h4><p>本頁沒有備註。</p>"}
function toggleNotes(){body.classList.toggle("shownotes");var on=body.classList.contains("shownotes");var p=document.getElementById("notesPanel");
  if(body.classList.contains("scroll")){p.hidden=true}else{p.hidden=!on;if(on)fillNotes()}}
function buildToc(){var l=document.getElementById("tocList"),h="";slides.forEach(function(s,i){h+="<button type=button data-i=\""+i+"\""+(i===cur?" class=on":"")+"><span class=n>"+(i+1)+"</span><span>"+esc(s.dataset.title||"")+"</span></button>"});l.innerHTML=h}
function openToc(){buildToc();document.getElementById("toc").hidden=false;var b=document.querySelector("#tocList .on")||document.querySelector("#tocList button");if(b)b.focus()}
function closeToc(){document.getElementById("toc").hidden=true}
document.getElementById("tocList").addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;var i=Number(b.dataset.i);closeToc();
  if(body.classList.contains("scroll"))slides[i].scrollIntoView({behavior:"smooth",block:"start"});else go(i)});
document.getElementById("toc").addEventListener("click",function(e){if(e.target.id==="toc")closeToc()});
document.getElementById("prev").onclick=function(){go(cur-1)};
document.getElementById("next").onclick=function(){go(cur+1)};
document.getElementById("tocBtn").onclick=openToc;document.getElementById("tocFab").onclick=openToc;
document.getElementById("notesBtn").onclick=toggleNotes;document.getElementById("notesFab").onclick=toggleNotes;
document.getElementById("fsBtn").onclick=function(){try{if(document.fullscreenElement)document.exitFullscreen();else{var p=document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen();if(p&&p.catch)p.catch(function(){})}}catch(e){}};
document.addEventListener("keydown",function(e){
  var t=e.target; if(t&&(t.tagName==="INPUT"||t.tagName==="TEXTAREA"))return;
  if(!document.getElementById("toc").hidden){if(e.key==="Escape"||e.key==="t"||e.key==="T"){closeToc();e.preventDefault()}return}
  if(body.classList.contains("scroll")){if(e.key==="t"||e.key==="T")openToc();if(e.key==="n"||e.key==="N")toggleNotes();return}
  var k=e.key;
  if(k==="ArrowRight"||k==="PageDown"||(k===" "&&!(t&&t.tagName==="BUTTON"))){go(cur+1);e.preventDefault()}
  else if(k==="ArrowLeft"||k==="PageUp"){go(cur-1);e.preventDefault()}
  else if(k==="Home"){go(0)}else if(k==="End"){go(N-1)}
  else if(k==="t"||k==="T"){openToc()}
  else if(k==="n"||k==="N"){toggleNotes()}
  else if(k==="f"||k==="F"){document.getElementById("fsBtn").click()}
});
var tx=null;document.addEventListener("touchstart",function(e){if(!body.classList.contains("scroll")&&e.touches.length===1)tx=e.touches[0].clientX},{passive:true});
document.addEventListener("touchend",function(e){if(tx==null)return;var dx=e.changedTouches[0].clientX-tx;tx=null;if(Math.abs(dx)>60)go(cur+(dx<0?1:-1))},{passive:true});
window.addEventListener("resize",function(){sizeIt();if(body.classList.contains("scroll")){document.getElementById("notesPanel").hidden=true}});
sizeIt();
var m=/^#s(\d+)$/.exec(location.hash||"");go(m?Number(m[1])-1:0);
if(body.classList.contains("scroll")&&m){setTimeout(function(){slides[cur].scrollIntoView({block:"start"})},50)}
window.__deck={go:go,N:N};
})();
</script>
