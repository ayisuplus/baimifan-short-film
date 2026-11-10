(() => {
"use strict";
const $=id=>document.getElementById(id), player=window.__storyboard, shots=player.shots;
const music=JSON.parse($("music-data").textContent), key="chuanyun.bgm-marks.v1";
const adoptedNode=$("adopted-music-data"), adoptedMarks=adoptedNode?JSON.parse(adoptedNode.textContent):{};
const options=[...$("quick-shot").options].map(option=>({option,label:option.textContent}));
const scenes=[...new Set(shots.map(s=>s.scene))];
let marks={}, current=shots[0], storageError="", undo=null;
const name=id=>music[id]?[music[id].display_title,music[id].title].filter((x,i,a)=>x&&a.indexOf(x)===i).join(" / "):id?"来源暂不可用（"+id+"）":"未选定";
const known=()=>shots.filter(s=>marks[s.id]);
const group=scene=>shots.filter(s=>s.scene===scene);
function selectedRanges(sceneShots,id){
 const runs=[];
 for(const s of sceneShots){
  if(marks[s.id]!==id)continue;
  const previous=runs[runs.length-1],index=sceneShots.indexOf(s);
  if(previous&&previous.endIndex===index-1){previous.last=s.id;previous.endIndex=index;}
  else runs.push({first:s.id,last:s.id,endIndex:index});
 }
 return runs.map(r=>r.first===r.last?r.first:r.first+" → "+r.last).join("；");
}
function el(tag,value,cls){const e=document.createElement(tag);e.textContent=value;if(cls)e.className=cls;return e;}
function button(label,fn,cls){const b=el("button",label,cls);b.type="button";b.addEventListener("click",fn);return b;}
function readMarks(){
 try{
  const raw=localStorage.getItem(key);
  // A missing browser record uses the frozen author choices. Existing edits,
  // including an explicitly empty map, always take precedence.
  const stored=raw===null?{...adoptedMarks}:JSON.parse(raw);
  if(!stored||Array.isArray(stored)||typeof stored!=="object")throw Error("invalid");
  // Preserve historical and unknown IDs; refreshing candidates must not erase choices.
  marks=stored;storageError="";return true;
 }catch{storageError="选曲记录读取失败。为保护已有选择，暂不写入；请先检查浏览器存储。";return false;}
}
function save(change){
 if(!readMarks()){paint(true);return;}
 const before=JSON.stringify(marks),next={...marks};change(next);
 try{
  const after=JSON.stringify(next);localStorage.setItem(key,after);
  marks=next;undo={before,after};storageError="";
 }catch{storageError="保存失败，已有选择保持不变。";}
 paint(true);
}
function jump(s){player.setPlaying(false);player.seek(s.start_second);$("music-library").scrollIntoView({behavior:"auto",block:"start"});}
function overview(){
 const grid=$("selection-scenes");grid.replaceChildren();
 for(const scene of scenes){
  const ss=group(scene),chosen=ss.filter(s=>marks[s.id]);
  const card=el("section","","selection-scene");card.dataset.selectionScene=scene;
  card.classList.toggle("is-current",scene===current.scene);
  card.append(el("h4",scene+" · "+ss[0].scene_title));
  const ids=[...new Set(chosen.map(s=>marks[s.id]))];
  card.append(el("span",!chosen.length?"待选曲":chosen.length===ss.length&&ids.length===1?"整段已选定":"已标记 "+chosen.length+" / "+ss.length+" 镜","selection-badge"));
  if(!chosen.length)card.append(el("p","这一段还没有选定 BGM。","muted"));
  for(const id of ids){
   const matched=chosen.filter(s=>marks[s.id]===id);
   card.append(el("strong",name(id),"selection-title"));
   card.append(el("p",matched.length===ss.length?"覆盖本段全部 "+ss.length+" 镜":"共 "+matched.length+" 镜 · "+selectedRanges(ss,id)+"（按播放顺序，逐镜明细见下方）","selection-origin"));
   const actions=el("div","","selection-actions");
   actions.append(button("查看已选镜头",()=>jump(matched[0])));
   if(music[id]){
    const listen=button("试听已选曲",()=>{});listen.className="music-audition";listen.dataset.music=id;actions.append(listen);
    if(matched.length!==ss.length)actions.append(button("整段使用此曲（"+ss.length+"镜）",()=>save(next=>ss.forEach(s=>{next[s.id]=id;})),"apply-scene"));
   }
   card.append(actions);
  }
  if(!chosen.length)card.append(button("去挑选本段",()=>jump(ss[0])));
  grid.append(card);
 }
 $("selection-count").textContent=scenes.filter(sc=>group(sc).some(s=>marks[s.id])).length+" / "+scenes.length+" 段有选曲标记 · "+known().length+" / "+shots.length+" 镜已标记";
 const tbody=$("selection-rows");tbody.replaceChildren();
 const only=$("selection-only-marked").checked;
 for(const s of shots){
  const id=marks[s.id];if(only&&!id)continue;
  const row=el("tr","");row.append(el("td",s.scene),el("td",s.id+" · "+s.title),el("td",name(id)));
  const actions=el("td","");actions.append(button("查看",()=>jump(s)));row.append(actions);tbody.append(row);
 }
 for(const s of shots){
  const node=document.querySelector("#"+s.id+" .shot-choice");
  if(node){node.textContent="本镜已选："+name(marks[s.id]);node.classList.toggle("has-choice",Boolean(marks[s.id]));}
 }
 for(const {option,label} of options)option.textContent=(marks[option.value]?"✓ ":"")+label+" · "+name(marks[option.value]);
}
function paint(refresh=false){
 if(refresh)overview();
 const chosen=marks[current.id], ss=group(current.scene),others=ss.filter(s=>marks[s.id]);
 $("quick-marked-music").textContent="本镜已选："+name(chosen);
 $("music-mark-summary").textContent=current.scene+" / "+current.id+" · 本镜已选："+name(chosen);
 const choices=[...new Set(others.map(s=>marks[s.id]))];
 $("music-scene-choice").textContent=chosen?"本镜已明确标记。"+current.scene+" 段内已有 "+others.length+" / "+ss.length+" 镜标记。":choices.length?current.scene+" 段内已有选择："+choices.map(name).join("；")+"。本镜尚未单独标记，可在选曲总览里应用到整段。":current.scene+" 整段尚未选曲。下面均为试听候选。";
 $("music-mark-storage").textContent=storageError||(adoptedNode?"作者确认用曲已存入项目；本机后续修改优先。播放、暂停和切镜不改变选择。":"选择自动保存在本机；播放、暂停和切镜均不改变选定结果。");
 $("selection-undo").disabled=!undo;
 for(const card of document.querySelectorAll("[data-music-card]")){
  const active=card.dataset.musicCard===chosen,b=card.querySelector(".music-mark");
  card.classList.toggle("is-marked",active);
  b.textContent=active?"✓ "+current.id+" 已选定 · 取消本镜标记":"为 "+current.id+" 选定此曲";
  b.setAttribute("aria-pressed",String(active));
 }
 for(const card of $("selection-scenes").children)card.classList.toggle("is-current",card.dataset.selectionScene===current.scene);
 document.dispatchEvent(new CustomEvent("previs:marks",{detail:{shot:current,id:chosen||""}}));
}
for(const card of document.querySelectorAll("[data-music-card]")){
 const b=button("选定此曲",()=>{
  const id=card.dataset.musicCard;
  save(next=>{if(next[current.id]===id)delete next[current.id];else next[current.id]=id;});
 },"music-mark");card.append(b);
}
$("selection-undo").addEventListener("click",()=>{
 if(!undo)return;
 try{
  if(localStorage.getItem(key)!==undo.after){undo=null;readMarks();storageError="记录已被其他页面更新，未撤销，以免覆盖新选择。";}
  else{localStorage.setItem(key,undo.before);marks=JSON.parse(undo.before);undo=null;storageError="";}
 }catch{storageError="撤销未能保存，现有记录保持。";}
 paint(true);
});
$("selection-only-marked").addEventListener("change",overview);
$("selection-export").addEventListener("click",()=>{
 if(!readMarks()){paint(true);return;}
 const data={exported_at:new Date().toISOString(),marks,shots:known().map(s=>({scene:s.scene,shot:s.id,title:s.title,music_id:marks[s.id],music:name(marks[s.id])}))};
 const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:"application/json"}));
 const a=document.createElement("a");a.href=url;a.download=(document.title.match(/《([^》]+)》/)?.[1]||"白米饭")+"-当前选曲.json";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
document.addEventListener("previs:tick",event=>{if(current.id!==event.detail.shot.id){current=event.detail.shot;paint();}});
window.addEventListener("storage",event=>{if(event.key===key||event.key===null){undo=null;readMarks();paint(true);}});
readMarks();paint(true);
})();
