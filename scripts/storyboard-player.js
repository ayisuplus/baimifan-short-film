(() => {
"use strict";
const shots=JSON.parse(document.getElementById("shot-data").textContent);
const $=id=>document.getElementById(id), total=shots.at(-1).end_second;
const audio=new Audio(); audio.preload="auto";
let playing=false, position=0, last=performance.now(), current=-1, cueKey="", lastError="";
const tc=n=>String(Math.floor(n/60)).padStart(2,"0")+":"+String(Math.floor(n%60)).padStart(2,"0");
function stopAudio(){audio.pause();cueKey="";}
function paint(){
 const idx=shots.findIndex(s=>position>=s.start_second && position<s.end_second);
 const n=idx<0?shots.length-1:idx,s=shots[n],local=position-s.start_second;
 if(n!==current){
  current=n; const r=s.panel_region,img=$("stage-image");
  img.src=s.image_url;img.alt=s.presentation.visible;
  Object.assign(img.style,{width:(100/r.w)+"%",height:(100/r.h)+"%",left:(-100*r.x/r.w)+"%",top:(-100*r.y/r.h)+"%"});
  const panelAspect=(r.w*s.page_size[0])/(r.h*s.page_size[1]);
  const canvasAspect=16/9;
  Object.assign($("stage").style,{aspectRatio:"auto",width:(panelAspect>=canvasAspect?100:100*panelAspect/canvasAspect)+"%",height:(panelAspect>=canvasAspect?100*canvasAspect/panelAspect:100)+"%"});
  $("stage-scene").textContent=s.scene+" · "+s.scene_title;
  $("stage-title").textContent=s.id+" · "+s.title;
  $("quick-shot").value=s.id;$("quick-current-shot").textContent=s.scene+" / "+s.id+" · "+s.title;
  document.querySelectorAll(".shot-play").forEach(b=>{const active=+b.dataset.start===s.start_second;b.setAttribute("aria-pressed",String(active));b.closest(".shot").classList.toggle("is-current",active);});
  $("stage-action").textContent=s.action;
  $("stage-sound").textContent=s.sound;
  $("shot-link").href="#"+s.id;$("shot-link").textContent="查看 "+s.id;
  document.querySelectorAll(".scene-jump").forEach(b=>b.classList.toggle("active",+b.dataset.start===shots.find(x=>x.scene===s.scene).start_second));
  stopAudio();
 }
 const reveal=s.split_screen_reveal,stage=$("stage");
 const stateFrame=(s.state_references||[]).filter(v=>local>=v.offset).at(-1);
 if(stateFrame){
  const img=$("stage-image");
  if(img.getAttribute('src')!==stateFrame.url)img.src=stateFrame.url;
  img.alt=stateFrame.label+'；同镜状态示意，非已生成动画';
  $("stage-title").textContent=s.id+" · "+s.title+" · "+stateFrame.label+"（静帧示意）";
 }
 const cap=s.time_caption;
 $("time-caption").textContent=cap && local>=cap.offset && local<cap.offset+cap.duration ? cap.text : "";
 if(reveal){
  const count=reveal.offsets.filter(t=>local>=t).length;
  stage.style.clipPath=`inset(0 ${100*(1-count/reveal.columns)}% 0 0)`;
  stage.dataset.revealed=String(count);
 }else{
  stage.style.clipPath="none";
  delete stage.dataset.revealed;
 }
 $("clock").textContent=tc(position)+" / "+tc(total);$("seek").value=position;
 const c=s.audio.find(c=>local>=c.offset && local<c.offset+c.duration+0.65);
 const silentCue=(s.subtitle_cues||[]).find(c=>local>=c.offset && local<c.offset+c.duration);
 const caption=c||silentCue;
 $("subtitle").textContent=caption?caption.speaker+"："+caption.text:"";
 const active=s.audio.find(c=>local>=c.offset && local<c.offset+c.duration);
 if(playing && $("voice").checked && active){
  const k=s.id+":"+active.offset;
  if(k!==cueKey){
   cueKey=k;audio.src=active.url;const offset=Math.max(0,local-active.offset);
   audio.currentTime=offset;
   audio.play().then(()=>{if(playing && $("voice").checked && cueKey===k) $("audio-status").textContent="临时读稿播放中；BGM可在下方选择试听，音效仍为设计说明。";}).catch(err=>{
    if(err.name!=="AbortError" && lastError!==k){lastError=k;$("audio-status").textContent="本次读稿未能播放："+err.message+"；画面预演继续，可取消再勾选“临时读稿”重试。";}
   });
  }
 }else {
  stopAudio();
  $("audio-status").textContent=$("voice").checked
   ?(playing?"本时段暂无读稿；现行台词与时点见下方。":"预演已暂停；点击播放继续临时读稿。")
   :"临时读稿已关闭；可以一边听BGM，一边手动切镜。";
 }
 document.dispatchEvent(new CustomEvent("previs:tick",{detail:{shot:s,position,playing}}));
}
function setPlaying(value){
 if(value && position>=total){position=0;current=-1;}
 playing=value;last=performance.now();
 $("play").textContent=playing?"暂停画面":"播放画面";
 $("play-status").textContent=playing?"画面播放中":"画面已暂停";
 if(!playing){stopAudio();}paint();
}
function seek(value){document.dispatchEvent(new Event("previs:seek"));position=Math.max(0,Math.min(total,value));stopAudio();last=performance.now();paint();}
$("quick-shot").addEventListener("change",event=>{const shot=shots.find(s=>s.id===event.target.value);if(shot){setPlaying(false);seek(shot.start_second);}});
$("play").addEventListener("click",()=>setPlaying(!playing));
$("seek").addEventListener("input",ev=>seek(+ev.target.value));
$("prev").addEventListener("click",()=>seek(shots[Math.max(0,current-1)].start_second));
$("next").addEventListener("click",()=>seek(shots[Math.min(shots.length-1,current+1)].start_second));
$("voice").addEventListener("change",()=>{stopAudio();paint();});
document.querySelectorAll("[data-start]").forEach(b=>b.addEventListener("click",()=>{
 setPlaying(false);seek(+b.dataset.start);
 if(b.classList.contains("shot-play")) $("previs").scrollIntoView({behavior:"smooth"});
}));
setInterval(()=>{
 if(playing){const now=performance.now();position=Math.min(total,position+(now-last)/1000);last=now;paint();if(position>=total)setPlaying(false);}
},80);
document.addEventListener("visibilitychange",()=>{if(document.hidden && playing)setPlaying(false);});
window.__storyboard={shots,get position(){return position;},get playing(){return playing;},seek,setPlaying};
paint();
})();
