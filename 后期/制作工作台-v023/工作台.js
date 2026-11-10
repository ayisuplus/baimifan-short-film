/* One shot view; original choices are authoritative and never replaced by defaults. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const el = (tag, cls, text) => { const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n; };
  const btn = (text, fn, cls='') => {const b=el('button',cls,text);b.type='button';b.onclick=()=>fn(b);return b;};
  const details = (title, ...nodes) => {const d=el('details');d.append(el('summary','',title),...nodes);return d;};
  const fmt = t => `${String(Math.floor(t/60)).padStart(2,'0')}:${(t%60).toFixed(2).padStart(5,'0')}`;
  const asset = path => '../../'+path.split('/').map(encodeURIComponent).join('/');
  const A=$('timeline');
  let D=null, choices=null, index=-1, sample=null, sampleButton=null, pendingTime=0, mode='bgm', saving=false;
  const verified=new Map();
  const cueById=new Map();
  const status=text=>{$('voice-status').textContent=text;};
  const fingerprint=o=>o.id+':'+o.sha256;
  const matchesText=(c,o)=>Boolean(o && (c.revision?o.text_ja===c.revision.ja:(!o.text_ja||o.text_ja===c.ja)));
  const newOptions=c=>c.options.filter(o=>o.delivery_version==='v005' && matchesText(c,o));
  const selectedOption=c=>{
    const saved=choices?.cue_choices[c.id];
    return saved && c.options.find(o=>o.id===saved.option_id && o.path===saved.path && o.sha256===saved.sha256 && verified.get(fingerprint(o))===true);
  };
  async function verifyFile(o){
    const r=await fetch(o.url);if(!r.ok)throw new Error('录音文件无法读取');
    const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',await r.arrayBuffer()))).map(v=>v.toString(16).padStart(2,'0')).join('');
    verified.set(fingerprint(o),hash===o.sha256);return hash===o.sha256;
  }
  async function verifyChoices(){
    const todo=[];
    for(const c of D.cues){const saved=choices.cue_choices[c.id];if(!saved)continue;const o=c.options.find(o=>o.id===saved.option_id && o.path===saved.path && o.sha256===saved.sha256);if(o && !verified.has(fingerprint(o)))todo.push(o);}
    for(let i=0;i<todo.length;i+=4)await Promise.all(todo.slice(i,i+4).map(o=>verifyFile(o).catch(()=>verified.set(fingerprint(o),false))));
  }
  function audioState(c){
    if(choices?.cue_choices[c.id] && !selectedOption(c))return ['已选文件需核验','danger'];
    if(newOptions(c).length && !matchesText(c,selectedOption(c)))return ['新录已到位 · 待试听选择','warn'];
    if(!selectedOption(c))return ['旧音色全部不采用','danger'];
    if(c.revision && !matchesText(c,selectedOption(c)))return ['旧文录音已选 · 新词待录','warn'];
    if(selectedOption(c)?.delivery_version==='v005')return ['新稿已选 · 待对位',''];
    return ['已选 · 待重新对位',''];
  }
  function stopSample(){
    if(sample){sample.pause();sample=null;}
    if(sampleButton){sampleButton.textContent=sampleButton.dataset.label||'▶ 试听';sampleButton=null;}
  }
  async function listen(url, button, start=0, end=null){
    A.pause();
    if(sample && sampleButton===button){stopSample();return;}
    stopSample();
    const audio=new Audio(url);sample=audio;sampleButton=button;
    button.dataset.label=button.textContent;button.textContent='■ 停止';
    audio.addEventListener('loadedmetadata',()=>{if(sample===audio)audio.currentTime=start;},{once:true});
    audio.addEventListener('timeupdate',()=>{if(end!==null && audio.currentTime>=end && sample===audio)stopSample();});
    audio.addEventListener('ended',()=>{if(sample===audio)stopSample();},{once:true});
    audio.addEventListener('error',()=>{if(sample===audio){status('试听文件加载失败，请检查项目媒体。');stopSample();}},{once:true});
    try{await audio.play();}catch(e){if(sample===audio){status('试听未能开始：'+e.message);stopSample();}}
  }
  async function save(c,o,button){
    if(saving)return;saving=true;button.disabled=true;
    try{
      if(o && !await verifyFile(o))throw new Error('音频已变化，不能保存旧索引，请重新核验');
      const r=await fetch(D.choice_api,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({kind:'cue',key:c.id,option_id:o?.id||null})});
      const result=await r.json();if(!r.ok)throw new Error(result.error||'保存失败');
      choices=result;await verifyChoices();
      status(o ? (c.revision && !matchesText(c,o)?'已保存旧文录音参考；新稿录音仍待选择。':'已保存这版配音；整片时码与混音待重排。') : '已清除选择；新录候选仍保留供试听，不自动采用。');
      drawDialogue();drawSummary();
    }catch(e){status('保存失败：'+e.message);button.disabled=false;}finally{saving=false;}
  }
  function optionRow(c,o,chosen){
    const row=el('div','option'+(chosen?' chosen':''));
    const copy=el('div','option-copy');copy.append(el('strong','',`${o.label} · ${o.seconds.toFixed(2)}秒`));
    const oldText=c.revision && !matchesText(c,o);
    const hint=[oldText?'旧文录音，只能比较声音；不是上方修订稿。':'',o.note,...(o.review_flags||[])].filter(Boolean).join(' ');
    copy.append(el('small','',hint));
    const actions=el('div','option-actions');actions.append(btn('▶ 试听',b=>listen(o.url,b)));
    if(chosen){actions.append(el('span','selected',oldText?'✓ 已选旧稿':'✓ 已选'),btn('取消选择',b=>save(c,null,b),'clear'));}
    else if(o.selectable){actions.append(btn(oldText?'选作旧稿声音参考':o.delivery_version==='v005'?'选这版新录音':'重新选择此版',b=>save(c,o,b),'pick'));}
    else actions.append(el('span','small','旧术名 · 仅对照'));
    row.append(copy,actions);return row;
  }
  function drawDialogue(){
    const shot=D.shots[index], root=$('dialogue');root.replaceChildren();
    $('line-count').textContent=shot.cue_ids.length?shot.cue_ids.length+'句关联台词':'无对白';
    if(!shot.cue_ids.length){root.append(el('p','muted','这一镜没有对白，留给动作、音乐与环境声。'));return;}
    for(const id of shot.cue_ids){
      const c=cueById.get(id), chosen=selectedOption(c), [label,kind]=audioState(c);
      const line=el('article','voice-line');line.dataset.cue=id;
      const heading=el('div','line-heading');heading.append(el('h3','',c.role),el('span','badge '+kind,label));line.append(heading);
      if(c.shot!==shot.id)line.append(el('p','small','这句从 '+c.location+' 延续到本镜；各镜共用同一条录音选择。'));
      line.append(el('span','detail-label',c.revision?'旧稿原句':'当前台词'),el('div','line-text',c.zh),el('div','jp',c.ja));
      if(c.revision){
        const p=c.revision, box=el('div','proposal');
        const hasV005=newOptions(c).length>0;
        box.append(el('span','badge '+(hasV005?'ok':'warn'),hasV005?'修订新词 · v005已录（下方可试听）':'修订候选 · 尚未录音'),el('div','line-text',p.zh),el('div','jp',(p.ja_display?p.ja_display+' / ':'')+p.ja),el('p','small',p.direction),el('p','warning',p.timing));line.append(box);
      }
      if(chosen){
        line.append(optionRow(c,chosen,true));
        const delta=chosen.seconds-(c.end-c.start);
        line.append(el('p','small',`所选录音 ${chosen.seconds.toFixed(2)}秒 · 旧对白窗口 ${(c.end-c.start).toFixed(2)}秒${Math.abs(delta)>.02?` · 相差 ${delta>0?'+':''}${delta.toFixed(2)}秒，待重新安排镜长与音乐`:''}`));
      }else if(choices?.cue_choices[id])line.append(el('p','warning','保存的文件与当前索引或实际文件不一致，不能视为有效选择；请重新核验。'));
      else {
        const hasV005=newOptions(c).length>0;
        line.append(el('p','warning',hasV005?'你已判定现有音色全不采用；v005重录候选已在下方选项中，可试听选择。':'你已完成挑选，这句没有合适版本，已列入重配清单。不会自动使用原混音里的声音。'));
      }
      const fresh=newOptions(c).filter(o=>!o.raw && (!chosen || chosen.id!==o.id));
      if(fresh.length){line.append(el('h3','small','新交付 · 先听这一版'));for(const o of fresh)line.append(optionRow(c,o,false));}
      const regular=c.options.filter(o=>!o.raw && !fresh.includes(o) && (!chosen || chosen.id!==o.id));
      if(regular.length){const all=details(`其他逐句版本 · ${regular.length}个`,...regular.map(o=>optionRow(c,o,false)));if(!chosen)all.open=true;line.append(all);}
      const raw=c.options.filter(o=>o.raw && (!chosen || chosen.id!==o.id));
      if(raw.length)line.append(details(`同次表演的原生 / 处理前文件 · ${raw.length}个`,el('p','small','属于同次表演，首尾、音量和声道可能不同；全部保留。'),...raw.map(o=>optionRow(c,o,false))));
      root.append(line);
    }
    for(const g of D.groups.filter(g=>g.members.some(id=>shot.cue_ids.includes(id)))){
      const box=details(g.title+' · 连续版本对照',el('p','small','你本轮未选整段版本。这里仅供试听，逐句已选结果保持；整段不能自动代替或覆盖逐句。'));
      for(const o of g.options){const row=el('div','option');const copy=el('div','option-copy');copy.append(el('strong','',`${o.label} · ${o.seconds.toFixed(2)}秒`),el('small','',o.note));row.append(copy,btn('▶ 试听',b=>listen(o.url,b)));box.append(row);}
      root.append(box);
    }
  }
  function drawSummary(){
    const selected=D.cues.filter(c=>selectedOption(c)).length;
    const rejected=D.cues.filter(c=>!choices?.cue_choices[c.id]);
    const invalid=D.cues.filter(c=>choices?.cue_choices[c.id] && !selectedOption(c));
    const revised=D.cues.filter(c=>c.revision);
    const pendingNew=D.cues.filter(c=>newOptions(c).length && selectedOption(c)?.delivery_version!=='v005').length;
    $('overview').replaceChildren(...[[D.shots.length,'画面'],[selected,'有效声音选择'],[pendingNew,'新录待选择'],[revised.length,'改词候选']].map(([n,t])=>{const s=el('div','stat');s.append(el('strong','',n),el('span','',t));return s;}));
    const todo=$('todo');todo.replaceChildren();
    const v005Done=D.cues.filter(c=>newOptions(c).length).length;
    todo.append(el('p','warning',`v005已交付${v005Done}句，${pendingNew}句待试听选择${invalid.length?`，另有${invalid.length}条选择文件需核验`:''}。月背分工长句需重点听审尾音。旧文已选录音保留；选定新录后再重新安排词尾、镜长与BGM卡点。`));
    for(const c of D.cues.filter(c=>c.revision||!selectedOption(c))){
      const row=el('div','todo-item'),copy=el('div');
      copy.append(el('strong','small',`${c.location} · ${c.role}`),el('p','',c.revision?c.revision.zh:c.zh),el('span','badge warn',audioState(c)[0]));
      row.append(copy,btn('定位画面',()=>{seek(D.shots.find(s=>s.id===c.shot).start);$('shot-name').scrollIntoView({block:'start'});}));todo.append(row);
    }
  }
  function drawMusic(shot,batch){
    const root=$('music');root.replaceChildren();
    root.append(el('p','small','以下为原配乐安排；所选配音与新台词实测后重新卡点。'));
    const music=D.music.filter(m=>m.timeline_start<shot.end && m.timeline_end>shot.start);
    for(const m of music){
      const a=Math.max(shot.start,m.timeline_start),b=Math.min(shot.end,m.timeline_end),source=m.source_in+a-m.timeline_start;
      const box=el('div','music-item');box.append(el('strong','music-title',D.music_titles[m.music_id]||m.music_id),
        el('p','small',`本镜 ${fmt(a-shot.start)}—${fmt(b-shot.start)} · 原曲 ${fmt(source)}—${fmt(source+b-a)}`),
        el('p','small',m.editorial_note),btn('▶ 试听本镜音乐原段',button=>listen(asset(m.path),button,source,source+b-a)),
        el('p','small',`原曲试听未套混音增益；基线 ${m.nominal_gain_db} dB，对白另压 ${m.dialogue_duck_additional_db} dB。`));root.append(box);
    }
    for(const s of D.silences.filter(s=>s.timeline_start<shot.end && s.timeline_end>shot.start))root.append(el('p','warning',`停乐 ${fmt(Math.max(shot.start,s.timeline_start)-shot.start)}—${fmt(Math.min(shot.end,s.timeline_end)-shot.start)}：${s.reason}。环境与拟音另做。`));
    if(!music.length)root.append(el('p','small','本镜没有BGM。'));
    for(const p of batch.rhythm?.points||[]){if(p.anchor_shot!==shot.id && !(p.film_time>=shot.start && p.film_time<shot.end))continue;root.append(el('div','point',`${fmt(p.film_time)} · ${p.action_zh}\n${p.music_intent}${Number.isFinite(p.source_seconds)?`（原曲 ${fmt(p.source_seconds)}）`:''}`));}
  }
  function drawStaging(shot){
    const root=$('staging');root.replaceChildren();
    const row=shot.generation_row;
    for(const [label,text] of [['动作',row.action],['摄影与构图',row.camera],['衔接',row.transition],['环境与拟音（待制作）',row.effects]]){
      const box=el('div','detail-block');box.append(el('span','detail-label',label),el('p','',text));root.append(box);
    }
    const affected=shot.cue_ids.map(id=>cueById.get(id)).filter(c=>c.revision);
    if(affected.length){const box=el('div','proposal');box.append(el('strong','small','改词后的表演 / 切镜候选（优先供本轮审阅）'));for(const c of affected)box.append(el('p','small',c.role+'：'+c.revision.direction));box.append(el('p','warning','上方原动作中的旧词和旧精确时码仅作基线；新录音完成后同步更新。'));root.append(box);}
  }
  function drawGeneration(shot,batch){
    const root=$('generation');root.replaceChildren();
    root.append(el('strong','small',`第${batch.number}批 · ${batch.title} · ${batch.shot_ids.length}镜同批`),
      el('p','small',`原请求15秒 / 正片${batch.used_seconds.toFixed(2)}秒 / 余量${batch.handle_seconds.toFixed(2)}秒。暂用旧分批，待新语音与时长定稿后再冻结。`),
      el('p','warning','完整提示词是旧版输入基线，尚未按本轮选择重排。不可直接作为本轮提交稿。'));
    const r=shot.generation_row;
    const focused=details('本镜提示词要点',el('div','prompt',[`${shot.display_name}：${shot.title}`,`参考：图片${r.slot}`,`起始：${r.entry}`,`画内：${r.visible.join('、')}`,`摄影：${r.camera}`,`动作：${r.action}`,`结束：${r.exit}`,`衔接：${r.transition}`].join('\n')));focused.open=true;root.append(focused);
    if(batch.revision_ids.length){const patch=el('div','proposal');patch.append(el('strong','small','这批需要同步的台词修订'));for(const id of batch.revision_ids){const c=cueById.get(id);patch.append(el('p','small',`${c.role}：${c.zh} → ${c.revision.zh}`));}patch.append(el('p','warning','新词、表演与声音窗口需整体展开；不把新词机械替换进旧时码。'));root.append(patch);}
    const prompt=el('div','prompt'), tabs=el('div','model-tabs');
    const setModel=(key)=>{prompt.textContent=batch.prompts[key];for(const b of tabs.children)b.classList.toggle('active',b.dataset.model===key);};
    for(const [key,name] of [['minimax-h3','H3 基线'],['seedance25','Seedance 基线']]){const b=btn(name,()=>setModel(key));b.dataset.model=key;tabs.append(b);}
    root.append(details('本批完整提示词 · 旧稿对照',tabs,prompt));setModel(batch.selected_model||'minimax-h3');
    const refs=el('div','refs');for(const ref of batch.references){const fig=el('figure','ref'),a=el('a'),im=el('img');a.href=asset(ref.path);a.target='_blank';a.rel='noopener';im.src=asset(ref.path);im.loading='lazy';im.alt='图片'+ref.slot+' · '+ref.purpose;a.append(im);fig.append(a,el('figcaption','',`图片${ref.slot} · ${ref.purpose}${ref.limits?' · '+ref.limits:''}`));refs.append(fig);}
    root.append(details(`本批上传参考顺序 · ${batch.references.length}张`,refs),details('历史关联与追溯',el('p','small',`稳定镜号 ${shot.id} · 批次ID ${batch.id} · 不随界面命名更换；旧稿、原图与录音均保留。`)));
  }
  function render(t){
    if(!D)return;
    const i=Math.max(0,D.shots.findIndex(s=>t>=s.start && t<s.end));
    const actual=t>=D.duration?D.shots.length-1:i;
    if(actual!==index){
      stopSample();index=actual;const s=D.shots[index],batch=D.batches[s.batch_number-1];
      $('shot-name').textContent=s.display_name+' · '+s.title;$('shot-duration').textContent=`${fmt(s.start)}—${fmt(s.end)} · 基线`;
      $('batch').value=String(s.batch_number);$('shot').replaceChildren(...batch.shot_ids.map(id=>{const x=D.shots.find(s=>s.id===id),o=el('option','',`第${x.batch_shot_number}镜 · ${x.title}`);o.value=x.id;return o;}));$('shot').value=s.id;
      $('prev').disabled=index===0;$('next').disabled=index===D.shots.length-1;
      const strip=$('batch-strip');strip.replaceChildren(...batch.shot_ids.map(id=>{const x=D.shots.find(s=>s.id===id),b=btn('',()=>seek(x.start),'thumb'+(id===s.id?' active':'')),im=el('img');im.src=x.image;im.alt=x.title;b.append(im,el('span','',`第${x.batch_shot_number}镜 · ${x.title}`));return b;}));
      drawDialogue();drawMusic(s,batch);drawStaging(s);drawGeneration(s,batch);
    }
    const s=D.shots[index],state=[...s.states].reverse().find(v=>t>=v.time),img=state?.image||s.image;
    if($('picture').getAttribute('src')!==img){$('picture').src=img;$('picture').alt=s.display_name+' · '+s.title;}
    $('state-label').textContent=state?.label||'';
    const active=D.cues.filter(c=>t>=c.start && t<c.end);
    const caption=$('caption');caption.replaceChildren();
    if(mode==='historical_mix'){
      caption.append(el('span','old-sub','旧混音对照 · 未应用本轮配音选择或新词'));
      for(const c of active)caption.append(el('div','',c.role+'：'+c.ja+' / '+c.zh));
    }else{
      caption.append(el('span','',active.length?'此处仅播放 BGM · 下方查看台词与配音':'此刻留给画面与声音的呼吸 · 当前无对白播放'));
    }
    $('time').textContent=fmt(t)+' / '+fmt(D.duration);$('seek').value=t;
  }
  function seek(time){
    const t=Math.min(Math.max(0,time),D.duration);pendingTime=t;stopSample();
    if(A.readyState)A.currentTime=t;
    render(t);history.replaceState(null,'','#t='+t.toFixed(2));
  }
  function fromHash(){
    const p=new URLSearchParams(location.hash.slice(1));const s=D.shots.find(s=>s.id===p.get('shot'));
    const raw=Number(p.get('t')||0);seek(s?s.start:Number.isFinite(raw)?raw:0);
  }
  $('play').onclick=async()=>{if(!D)return;if(!A.paused){A.pause();return;}stopSample();try{await A.play();}catch(e){status('整片音频加载失败：'+e.message);}};
  A.addEventListener('play',()=>{stopSample();$('play').textContent='Ⅱ 暂停';});
  A.addEventListener('pause',()=>{$('play').textContent=mode==='bgm'?'▶ 播放画面 + BGM':'▶ 播放旧混音对照';});
  A.addEventListener('timeupdate',()=>render(A.currentTime));
  A.addEventListener('loadedmetadata',()=>{A.currentTime=pendingTime;});
  A.addEventListener('error',()=>status('整片音轨无法读取；镜头和逐句试听仍可检查。'));
  $('play-mode').onchange=()=>{pendingTime=A.currentTime;A.pause();stopSample();mode=$('play-mode').value;A.src=D.audio[mode];$('play-note').textContent=mode==='bgm'?'BGM沿用v021剪辑。逐句试听在下方；本轮选择尚未合成整片。':'正在对照历史v021混音：包含你已拒用的旧声音，不代表当前采用。';$('play').textContent=mode==='bgm'?'▶ 播放画面 + BGM':'▶ 播放旧混音对照';render(pendingTime);};
  $('seek').oninput=()=>seek(Number($('seek').value));
  $('prev').onclick=()=>seek(D.shots[Math.max(0,index-1)].start);
  $('next').onclick=()=>seek(D.shots[Math.min(D.shots.length-1,index+1)].start);
  $('batch').onchange=()=>seek(D.shots.find(s=>s.id===D.batches[Number($('batch').value)-1].shot_ids[0]).start);
  $('shot').onchange=()=>seek(D.shots.find(s=>s.id===$('shot').value).start);
  function nextMatch(predicate){const list=D.cues.filter(predicate);if(!list.length){status('没有符合条件的句子。');return;}const c=list.find(c=>D.shots.find(s=>s.id===c.shot).start>D.shots[index].start+.01)||list[0];seek(D.shots.find(s=>s.id===c.shot).start);}
  $('next-rejected').onclick=()=>nextMatch(c=>!selectedOption(c)||(newOptions(c).length && selectedOption(c)?.delivery_version!=='v005'));
  $('next-revision').onclick=()=>nextMatch(c=>c.revision);
  document.addEventListener('keydown',e=>{if(!D||e.altKey||e.ctrlKey||e.metaKey||/INPUT|SELECT|TEXTAREA|BUTTON|SUMMARY/.test(e.target.tagName))return;if(e.code==='Space'){e.preventDefault();$('play').click();}else if(e.key==='ArrowLeft'){e.preventDefault();$('prev').click();}else if(e.key==='ArrowRight'){e.preventDefault();$('next').click();}});
  window.addEventListener('hashchange',()=>{if(D)fromHash();});
  async function init(){
    const r=await fetch('工作台数据.json');if(!r.ok)throw new Error('工作台资料无法读取');D=await r.json();
    const q=await fetch(D.choice_api);if(!q.ok)throw new Error('作者选择记录无法读取，未启用默认回填');choices=await q.json();
    if(!choices.cue_choices || !choices.group_choices)throw new Error('作者选择数据格式不正确');
    for(const c of D.cues)cueById.set(c.id,c);
    await verifyChoices();
    $('batch').replaceChildren(...D.batches.map(b=>{const o=el('option','',`第${b.number}批 · ${b.title}`);o.value=b.number;return o;}));
    $('seek').max=D.duration;A.src=D.audio.bgm;fromHash();drawSummary();
    const stale=D.cues.filter(c=>choices.cue_choices[c.id] && !selectedOption(c)).length;
    status(stale?`${stale}条作者选择文件需核验，请查看对应镜头；原记录未修改。`:'作者选择已读取并校验。新台词为候选；配音选择更改会自动保存。');
  }
  init().catch(e=>{status(e.message);$('overview').textContent='加载失败，请检查项目预览服务';});
})();
