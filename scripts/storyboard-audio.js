(() => {
"use strict";
const $=id=>document.getElementById(id), player=window.__storyboard;
const music=JSON.parse($("music-data").textContent), track=$("music-audio"), cards=new Map(), positions=new Map();
let selected="", loadedId="", shownShot="", shownSection="", currentSection=null, currentMarked="", dragging=false, pendingSeek=0;
const visibleIds=()=>[...new Set([...(currentSection?.candidates||[]),...(music[currentMarked]?[currentMarked]:[])])];
const tc=n=>`${Math.floor(n/60).toString().padStart(2,"0")}:${Math.floor(n%60).toString().padStart(2,"0")}`;
const put=(id,value)=>{const e=$(id);if(e.textContent!==value)e.textContent=value;};
function text(tag,value,cls){const e=document.createElement(tag);e.textContent=value;if(cls)e.className=cls;return e;}
function makeAudio(url,label){const a=document.createElement("audio");a.controls=true;a.preload="none";a.src=url;a.setAttribute("aria-label",label);return a;}
function updateClock(){
 const duration=selected?music[selected].duration:0;
 const time=dragging?Number($("music-seek").value):(loadedId===selected?track.currentTime:pendingSeek);
 if(!dragging)$("music-seek").value=Number.isFinite(time)?time:0;
 put("music-clock",`${tc(time||0)} / ${tc(duration)}`);
 if(selected&&loadedId===selected&&!dragging)positions.set(selected,track.ended?0:track.currentTime);
}
function updateSelect(){
 const list=$("music-select"),options=[];
 const placeholder=text("option","选择本镜候选");placeholder.value="";options.push(placeholder);
 if(selected&&!visibleIds().includes(selected)){
  const o=text("option",`当前试听（其他镜头）：${music[selected].title}`);o.value=selected;options.push(o);
 }
 visibleIds().forEach((id,index)=>{const m=music[id],o=text("option",`${id===currentMarked?"✓ 本镜已选":String.fromCharCode(65+index)+" · 候选"} · ${m.display_title||m.title} · ${m.work||"葬送的芙莉莲"}`);o.value=id;options.push(o);});
 list.replaceChildren(...options);list.value=selected;
}
function status(){
 const state=!selected?"尚未选择":track.error?"加载失败":track.ended?"已播完":track.paused?"已暂停":track.readyState<3?"加载中":"正在试听";
 const title=selected?`${music[selected].display_title?music[selected].display_title+" / ":""}${music[selected].title}`:"尚未选择音乐";
 put("music-current",title);put("quick-current-music",selected?`试听播放器 · ${state}：${title}`:"试听播放器 · 尚未播放");
 put("music-status",selected?`${state} · 仅试听，不代表选定。切镜不停乐；拖动进度可跳转。`:"先试听候选；确定后点击带镜号的选定按钮。");
 $("music-resume").disabled=!selected;$("music-stop").disabled=!selected;
 $("music-seek").disabled=!selected||loadedId!==selected;
 for(const [id,card] of cards){
  const active=id===selected;card.classList.toggle("is-selected",active);
  const b=card.querySelector(".music-audition");b.setAttribute("aria-pressed",String(active));
  const label=active?(track.paused?"继续试听":"当前试听"):"试听此曲";
  if(b.textContent!==label)b.textContent=label;
 }
}
function playMusic(id,restart=false){
 if(!music[id])return;
 if(selected!==id){
  if(selected&&loadedId===selected)positions.set(selected,track.ended?0:track.currentTime);
  track.pause();selected=id;loadedId="";pendingSeek=restart?0:(positions.get(id)||0);dragging=false;
  $("music-seek").max=music[id].duration;track.src=music[id].url;
 }else if(restart||track.ended){pendingSeek=0;if(loadedId===id)track.currentTime=0;}
 updateSelect();status();updateClock();
 track.play().then(status).catch(err=>{if(err.name!=="AbortError"&&selected===id)put("music-status",err.name==="NotAllowedError"?"已选好音乐，点击“继续当前音乐”开始播放。":"音频未能播放："+err.message);});
}
// One persistent audio element. Candidate cards are only selection controls.
for(const [id,m] of Object.entries(music)){
 const card=text("div","","music-card");card.dataset.musicCard=id;card.id="music-"+id;
 card.append(text("strong",m.title),text("span",[m.display_title,m.work||"葬送的芙莉莲"].filter(Boolean).join(" · "),"muted"),text("span","","music-match"),text("span",`来源完整音轨 ${tc(m.duration)} · 待作者比较`,"muted"));
 const actions=text("div","","music-actions"),resume=text("button","试听此曲","music-audition"),restart=text("button","从头播放","music-audition");
 resume.dataset.music=id;resume.setAttribute("aria-pressed","false");restart.dataset.music=id;restart.dataset.restart="true";
 const link=text("a","来源视频 ↗");link.href=m.source;link.target="_blank";link.rel="noopener";
 actions.append(resume,restart,link);card.append(actions);cards.set(id,card);$("deck-bgm-list").append(card);
}
function render(s){
 if(shownShot!==s.id){
  shownShot=s.id;$("deck-action").textContent=s.action;$("deck-dialogue").textContent=s.dialogue;
  $("deck-effects").textContent=s.effect_design;$("deck-source-sound").textContent=s.sound;
  const timing=$("deck-dialogue-timing");timing.replaceChildren();
  for(const c of s.subtitle_cues||[])timing.append(text("p",`${c.speaker} · 镜内 ${c.offset.toFixed(1)}–${(c.offset+c.duration).toFixed(1)}秒 · ${c.text}`,"muted"));
  $("deck-voice-state").textContent=s.dialogue==="无对白"?"本镜无对白。":s.audio.length?"已有临时读稿；新台词若无音频则只显示字幕。":"本镜暂无读稿音频；台词与字幕仍按当前分镜展示。";
  const samples=$("deck-dialogue-audio");samples.querySelectorAll("audio").forEach(a=>a.pause());samples.replaceChildren();
  for(const c of s.audio)samples.append(text("p",`临时读稿 · ${c.speaker}`,"muted"),makeAudio(c.url,`${s.id} ${c.speaker} 临时读稿`));
 }
 const section=s.bgm_section;
 put("deck-bgm-note",`${s.id} · ${tc(section.start)}–${tc(section.end)} · ${section.note}。${section.candidates.length?"以下为当前画面的候选，可逐首对比。":"本段建议留白，暂无候选BGM。"}`);
 if(shownSection===section.id)return;
 shownSection=section.id;currentSection=section;
 currentMarked="";
 refreshCandidates();
}
function refreshCandidates(){
 const ids=visibleIds();
 $("deck-bgm-list").classList.toggle("single-candidate",ids.length===1);
 for(const [id,card] of cards){
  const index=ids.indexOf(id);card.hidden=index<0;card.style.order=id===currentMarked?-1:index;
  card.querySelector(".music-match").textContent=id===currentMarked?"✓ 本镜已选定":index>=0?`${String.fromCharCode(65+index)} · 备选，尚未选定`:"";
 }
 updateSelect();status();
}
document.addEventListener("click",event=>{const b=event.target.closest(".music-audition");if(b)playMusic(b.dataset.music,b.dataset.restart==="true");});
document.addEventListener("previs:tick",event=>render(event.detail.shot));
document.addEventListener("previs:marks",event=>{currentMarked=event.detail.id;refreshCandidates();});
$("music-select").addEventListener("change",event=>{if(event.target.value)playMusic(event.target.value);});
$("music-resume").addEventListener("click",()=>{if(selected)playMusic(selected);});
$("music-stop").addEventListener("click",()=>track.pause());
track.volume=Number($("music-volume").value);
$("music-volume").addEventListener("input",event=>{track.volume=Number(event.target.value);});
$("music-seek").addEventListener("input",()=>{dragging=true;updateClock();});
$("music-seek").addEventListener("change",event=>{
 const value=Number(event.target.value);dragging=false;
 if(loadedId===selected&&Number.isFinite(track.duration))track.currentTime=Math.min(Math.max(0,value),track.duration);
 updateClock();
});
$("music-seek").addEventListener("pointercancel",()=>{dragging=false;updateClock();});
track.addEventListener("loadedmetadata",()=>{
 loadedId=selected;track.currentTime=Math.min(pendingSeek,Math.max(0,track.duration-.05));status();updateClock();
});
track.addEventListener("timeupdate",updateClock);
for(const event of ["play","pause","ended","waiting","playing","error"])track.addEventListener(event,status);
render(player.shots[0]);updateClock();
})();
