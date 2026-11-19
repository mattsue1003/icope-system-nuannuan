/* ---------- calculator ---------- */
(function(){
  var ids=["n","new","a0","rev","a1","iv","act","old","due","pt"];
  var NN={n:646,new:471,a0:110,rev:108,a1:95,iv:88,act:25,old:72,due:39,pt:29};
  var CITY={n:9454,new:"",a0:1414,rev:1175,a1:1073,iv:959,act:"",old:"",due:324,pt:187};
  var src=document.getElementById("calcSrc"),out=document.getElementById("calcOut");
  function g(k){var v=document.getElementById("c_"+k).value;return v===""?null:Number(v)}
  function set(o){ids.forEach(function(k){document.getElementById("c_"+k).value=o[k]==null?"":o[k]});calc()}
  function r(a,b){return (a==null||b==null||b===0)?null:a/b*100}
  function rn(a,b){return a/b*100}
  var NNV={new:rn(471,646),a0:rn(110,646),rev:rn(108,110),a1:rn(95,646),iv:rn(88,95),act:rn(25,95),old:rn(72,646),pt:rn(29,39)};
  function calc(){
    var R=[
      ["首篩比","首次評估 ÷ 評估",r(g("new"),g("n")),null,"new"],
      ["75 歲以上比例","75+ ÷ 評估",r(g("old"),g("n")),null,"old"],
      ["初評異常率","初評異常 ÷ 評估",r(g("a0"),g("n")),null,"a0"],
      ["複評完成率","完成複評 ÷ 初評異常",r(g("rev"),g("a0")),null,"rev"],
      ["異常率","確認異常 ÷ 評估",r(g("a1"),g("n")),"ab","a1"],
      ["介入率","有紀錄 ÷ 確認異常",r(g("iv"),g("a1")),"iv","iv"],
      ["實際介入率","衛教轉介 ÷ 確認異常",r(g("act"),g("a1")),null,"act"],
      ["後測率","完成後測 ÷ 到期應後測",r(g("pt"),g("due")),"pt","pt"]
    ];
    var h="";
    R.forEach(function(x){
      var v=x[2],st="<span class=\"pill\">參考</span>";
      if(v==null)st="<span class=\"pill\">待填</span>";
      else if(v>100)st="<span class=\"pill wn\">超過 100%，檢查分母</span>";
      else if(x[3]){ if(v<THR[x[3]])st="<span class=\"pill sr\">觸及篩選線</span>"; else st="<span class=\"pill ok\">未觸及</span>";}
      else if(x[4]==="act"&&v<50)st="<span class=\"pill wn\">低於一半</span>";
      h+="<div class=orow><div><b>"+x[0]+"</b>　<span class=of>"+x[1]+"・暖暖 "+NNV[x[4]].toFixed(1)+"%</span></div><div class=ov>"+(v==null?"—":v.toFixed(1)+"%")+"</div><div>"+st+"</div></div>";
    });
    out.innerHTML=h;
  }
  ids.forEach(function(k){document.getElementById("c_"+k).addEventListener("input",function(){src.textContent="自行輸入中。";calc()})});
  document.querySelectorAll("[data-fill]").forEach(function(b){b.addEventListener("click",function(){
    var f=b.getAttribute("data-fill");
    if(f==="nn"){set(NN);src.textContent="目前是暖暖衛生所 2026/01–08 數據。"}
    else if(f==="city"){set(CITY);src.textContent="全市 30 單位加總（10 月篩選表；沒有首次評估、實際介入、75 歲以上欄位，留白）。"}
    else{set({});src.textContent="已清空，請輸入你們單位的人數。"}
  })});
  set(NN);
})();
