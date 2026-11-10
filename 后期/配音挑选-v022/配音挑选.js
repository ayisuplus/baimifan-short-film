/* Comparison auditions are separate from the existing, immutable v021 mix. */
(() => {
  'use strict';
  let manifest=null, choices={schema:1,cue_choices:{},group_choices:{}}, sample=null, renderedShot='';
  const verified=new Map();
  const container=document.getElementById('voice-options');
  const status=document.getElementById('choice-status');
  const counter=document.getElementById('choice-count');
  const el=(tag,cls,text)=>{const n=document.createElement(tag);n.className=cls||'';if(text!==undefined)n.textContent=text;return n;};
  const keyFor=o=>o.id+':'+o.sha256;
  const savedIsValid=(item,saved)=>Boolean(saved && item.options.some(o=>o.id===saved.option_id && o.sha256===saved.sha256 && verified.get(keyFor(o))===true));
  async function verifyFile(option){
    const file=await fetch(option.url);if(!file.ok)throw new Error('候选音频文件无法读取');
    const bytes=await file.arrayBuffer();const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('');
    verified.set(keyFor(option),hash===option.sha256);return hash===option.sha256;
  }
  async function verifySaved(){
    const todo=[];
    for(const [items,bucket] of [[manifest.cues,choices.cue_choices],[manifest.groups,choices.group_choices]]){
      for(const item of items){const saved=bucket[item.id];if(!saved)continue;const option=item.options.find(o=>o.id===saved.option_id && o.sha256===saved.sha256);if(option && !verified.has(keyFor(option)))todo.push(option);}
    }
    for(let i=0;i<todo.length;i+=4)await Promise.all(todo.slice(i,i+4).map(o=>verifyFile(o).catch(()=>verified.set(keyFor(o),false))));
  }
  function stopSample(){if(sample){sample.pause();sample.currentTime=0;sample=null;}document.querySelectorAll('.voice-option .listen').forEach(b=>b.textContent='▶ 试听');}
  A.addEventListener('play',stopSample);
  async function listen(option,button){
    A.pause();
    if(sample && sample.dataset.option===option.id && !sample.paused){stopSample();button.textContent='▶ 试听';return;}
    stopSample();
    document.querySelectorAll('.voice-option .listen').forEach(b=>b.textContent='▶ 试听');
    sample=new Audio(option.url);sample.dataset.option=option.id;button.textContent='■ 停止';
    sample.addEventListener('ended',()=>{button.textContent='▶ 试听';sample=null;},{once:true});
    sample.addEventListener('error',()=>{button.textContent='▶ 试听';status.textContent='该音频未能加载，请检查本地文件和预览服务。';},{once:true});
    try{await sample.play();}catch(e){button.textContent='▶ 试听';status.textContent='无法播放候选：'+e.message;}
  }
  async function choose(kind,key,option,button){
    button.disabled=true;
    try{
      if(option){
        if(!await verifyFile(option))throw new Error('候选文件已变化，请更新索引后重新试听');
      }
      const res=await fetch('/api/voice-choices-v022',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({kind,key,option_id:option?.id||null})});
      const result=await res.json();if(!res.ok)throw new Error(result.error||'保存失败');
      choices=result;await verifySaved();status.textContent=option ? '已保存：'+option.label+'。整片混音尚未更新。' : '已清除这个选择。';
      draw();
    }catch(e){button.disabled=false;status.textContent='保存失败：'+e.message+'。请使用项目预览服务打开本页。';}
  }
  function choiceRow(option,kind,key,current){
    const saved=(kind==='cue'?choices.cue_choices:choices.group_choices)[key];
    const selected=Boolean(saved && saved.option_id===option.id && saved.sha256===option.sha256 && verified.get(keyFor(option))===true);
    const row=el('div','voice-option'+(selected?' is-chosen':''));
    const text=el('div','voice-copy');text.append(el('strong','',option.label+' · '+option.seconds.toFixed(2)+'秒'));
    const note=[option.note];if(current===option.path)note.unshift('当前整片混音使用');
    text.append(el('small','',note.join(' · ')));row.append(text);
    const actions=el('div','voice-actions');const play=el('button','listen','▶ 试听');play.type='button';play.onclick=()=>listen(option,play);actions.append(play);
    if(selected){const flag=el('span','selected','✓ 已选');actions.append(flag);const clear=el('button','clear','取消');clear.type='button';clear.onclick=()=>choose(kind,key,null,clear);actions.append(clear);}
    else if(option.selectable){const pick=el('button','pick',kind==='group'?'标记整段意向':'选这版');pick.type='button';pick.onclick=()=>choose(kind,key,option,pick);actions.append(pick);}
    else actions.append(el('span','current','仅供对照'));
    row.append(actions);return row;
  }
  function draw(){
    if(!manifest || index<0)return;
    const shot=D.shots[index];renderedShot=shot.id;
    const cues=manifest.cues.filter(c=>c.visual_shots.includes(shot.id) || (c.start<shot.end && c.end>shot.start));
    container.replaceChildren();
    const validCount=manifest.cues.filter(c=>savedIsValid(c,choices.cue_choices[c.id])).length;
    counter.textContent='已选择 '+validCount+' / '+manifest.cues.length+' 句';
    if(!cues.length){container.append(el('div','picker-empty','这幅画面没有对白；用上方“上一镜 / 下一镜”继续。'));return;}
    for(const cue of cues){
      const line=el('article','voice-line');
      line.append(el('h3','',cue.role+' · '+cue.id),el('div','voice-jp',cue.ja));
      const source=D.cues.find(x=>x.id===cue.id);if(source)line.append(el('p','voice-zh',source.zh));
      if(cue.shot!==shot.id)line.append(el('p','voice-context','这句对白从相邻镜头延续过来，选择与原镜头共用。'));
      const saved=choices.cue_choices[cue.id];if(saved && !savedIsValid(cue,saved))line.append(el('p','picker-warning','此前所选文件或索引已变化，请重新试听选择。'));
      const options=[...cue.options].sort((a,b)=>Number(b.path===cue.current_path)-Number(a.path===cue.current_path));
      for(const option of options.filter(o=>!o.raw))line.append(choiceRow(option,'cue',cue.id,cue.current_path));
      const raw=options.filter(o=>o.raw);
      if(raw.length){const detail=el('details','group-details');detail.open=raw.some(o=>saved?.option_id===o.id);detail.append(el('summary','','同次表演的原生 / 处理前文件（'+raw.length+'）'));detail.append(el('p','','与上面的干声属于同次表演，留白、声道和音量可能不同。'));for(const option of raw)detail.append(choiceRow(option,'cue',cue.id,cue.current_path));line.append(detail);}
      container.append(line);
    }
    const groups=manifest.groups.filter(g=>cues.some(c=>g.members.includes(c.id)));
    for(const group of groups){
      const box=el('details','group-details');box.append(el('summary','',group.title+' · 整段版本试听'));
      const saved=choices.group_choices[group.id];if(saved)box.open=true;if(saved && !savedIsValid(group,saved))box.append(el('p','picker-warning','此前所选整段文件或索引已变化，请重新试听选择。'));
      box.append(el('p','','整段意向单独保存，不会覆盖逐句选择；部分版本只有前段或后段，选定后需人工切分并重新对位。'));
      for(const option of group.options)box.append(choiceRow(option,'group',group.id,null));
      container.append(box);
    }
  }
  const originalRender=render;
  render=function(t=A.currentTime){originalRender(t);if(manifest && index>=0 && D.shots[index].id!==renderedShot){stopSample();draw();}};
  document.getElementById('prev-voice').onclick=()=>{if(!manifest)return;const list=manifest.cues.filter(c=>c.start<A.currentTime-.05);seek((list.at(-1)||manifest.cues[0]).start);};
  document.getElementById('next-voice').onclick=()=>{if(!manifest)return;const next=manifest.cues.find(c=>c.start>A.currentTime+.05);seek((next||manifest.cues.at(-1)).start);};
  document.getElementById('next-unpicked').onclick=()=>{if(!manifest)return;const unpicked=manifest.cues.filter(c=>!savedIsValid(c,choices.cue_choices[c.id]));if(!unpicked.length){status.textContent='所有对白都已选择。';return;}const next=unpicked.find(c=>c.start>A.currentTime+.05)||unpicked[0];seek(next.start);};
  Promise.all([fetch('候选索引.json').then(r=>{if(!r.ok)throw new Error('候选索引读取失败');return r.json();}),fetch('/api/voice-choices-v022').then(r=>{if(!r.ok)throw new Error('选择记录读取失败');return r.json();})])
    .then(async ([m,c])=>{manifest=m;choices=c;status.textContent='正在校验已选择的音频…';await verifySaved();status.textContent='点击试听，再选喜欢的版本。';draw();})
    .catch(e=>{status.textContent=e.message+'。请通过项目预览服务打开。';});
})();
