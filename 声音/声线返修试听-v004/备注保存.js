let queue=Promise.resolve();
const timers={},dirty=new Set();
const endpoint='/api/voice-choice-v004';
function notice(text){document.getElementById('notice').textContent=text}
function render(){for(const e of entries){const c=choices[e.role];document.getElementById('status-'+e.role).textContent=!c||c.candidate==null?(c?.status==='retain_existing_voice'?'已确认：保留现有声音':'待审核'):c.candidate===0?'已标记：需要调整':'已选：候选 '+c.candidate;}}
function saveChoice(role,candidate){
 clearTimeout(timers[role]);
 const note=document.getElementById('note-'+role).value;
 const payload={role,note};if(candidate!==undefined)payload.candidate=candidate;
 dirty.add(role);notice('正在保存：'+role);
 queue=queue.then(async()=>{try{
  const r=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  if(!r.ok)throw new Error('HTTP '+r.status);
  choices=await r.json();
  if(document.getElementById('note-'+role).value===note)dirty.delete(role);
  render();notice(dirty.size?'还有备注等待保存…':'选择和备注已保存到项目');
 }catch(error){notice('保存失败，输入仍保留：请重试保存备注或导出全部选择');}});
 return queue;
}
function exportChoices(){const result=structuredClone(choices);for(const e of entries){const n=document.getElementById('note-'+e.role);if(n)result[e.role]={...result[e.role],note:n.value};}const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(result,null,2)],{type:'application/json'}));a.download='白米饭-全角色声线选择-v004.json';a.click();URL.revokeObjectURL(a.href);}
async function init(){
 for(const e of entries){const n=document.getElementById('note-'+e.role);if(!n)continue;n.value=choices[e.role]?.note||'';
 n.addEventListener('input',()=>{dirty.add(e.role);notice('备注待保存：'+e.role);clearTimeout(timers[e.role]);timers[e.role]=setTimeout(()=>saveChoice(e.role),600);});
 n.addEventListener('blur',()=>{if(dirty.has(e.role))saveChoice(e.role);});}
 render();
 try{const r=await fetch(endpoint);if(!r.ok)throw 0;choices=await r.json();for(const e of entries){const n=document.getElementById('note-'+e.role);if(n&&!dirty.has(e.role))n.value=choices[e.role]?.note||'';}render();if(!dirty.size)notice('选择与备注自动保存，也可点击“保存备注”');}
 catch(error){notice('保存服务未连接：请保留页面并导出选择');}
}
window.addEventListener('beforeunload',event=>{if(dirty.size){event.preventDefault();event.returnValue='';}});
document.querySelectorAll('audio').forEach(a=>a.addEventListener('play',()=>document.querySelectorAll('audio').forEach(b=>{if(a!==b)b.pause()})));
init();
