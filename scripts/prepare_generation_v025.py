"""Reconcile current Japanese dry audio, shot clocks, music anchors and batch inputs."""
from pathlib import Path
import copy, json, hashlib, subprocess, math, re

ROOT=Path(__file__).resolve().parents[1]
OLD='视频制作/生成板-v021'; OUT='视频制作/生成板-v025'
OLDFIX='后期/语音节奏定版-v021'; FIX='后期/生成收口-v025'
BASE='镜头设计/shot-plan-v0.64.json'; SOURCE='镜头设计/shot-plan-v0.65.json'
def load(p):return json.loads((ROOT/p).read_text('utf-8-sig'))
def write(p,x):
 p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n','utf-8')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def remap(x):
 if isinstance(x,dict):return {k:remap(v) for k,v in x.items()}
 if isinstance(x,list):return [remap(v) for v in x]
 if isinstance(x,str):return x.replace(OLD,OUT).replace(OLDFIX,FIX).replace(BASE,SOURCE).replace('沧龙出海','沧龙天倾').replace('そうりゅうしゅつかい','そうりゅうてんけい')
 return x
def n(t):return f'{t:.3f}'.rstrip('0').rstrip('.')
def main():
 baseline=load(BASE);src=copy.deepcopy(baseline);sm={s['id']:s for s in src['shots']};oldsm={s['id']:s for s in baseline['shots']}
 mapping=remap(load(OLD+'/日语音频映射.json'));am={a['cue_id']:a for a in mapping['cues']}
 # Author choices stay immutable; two v005 files are explicitly authorized for this alignment.
 choices=load('后期/配音挑选-v022/作者选择.json')
 wb=load('后期/制作工作台-v023/工作台数据.json')
 revisions={c['id']:c for c in load('剧本/对白修订-v0.64-候选.json')['cues']}
 wc={c['id']:c for c in wb['cues']}
 alignment_only={'VO-CY026D-02','VO-CY024A5-01'}
 selected=[];text_pairs={}
 for a in mapping['cues']:
  cid=a['cue_id']; cue=wc[cid]; choice=choices['cue_choices'][cid]
  opt=next(o for o in cue['options'] if o['id']==choice['option_id'])
  if cid in alignment_only:
   opt=next(o for o in cue['options'] if o.get('delivery_version')=='v005' and not o['raw'])
  assert sha(opt['path'])==opt['sha256']
  for key in ['speech_start','speech_end','speech_seconds','transcript_verified','delivery_status']:
   a.pop(key,None)
  a.update(path=opt['path'],sha256=opt['sha256'],text=revisions.get(cid,{}).get('ja',a['text']),
           author_selection=choice,alignment_only=cid in alignment_only,
           delivery_status='作者授权v005用于对位，旧版仅音色参考' if cid in alignment_only else '作者已选版本',transcript_verified=False)
  selected.append(dict(cue_id=cid,path=opt['path'],sha256=opt['sha256'],option_id=opt['id'],alignment_only=cid in alignment_only,original_choice=choice))
  if cid in revisions:
   sub=next(c for s in src['shots'] for c in s.get('subtitle_cues',[]) if c['cue_id']==cid)
   text_pairs[sub['text']]=revisions[cid]['zh'];sub['text']=revisions[cid]['zh']
 for s in src['shots']:
  for key in ['dialogue','action','sound','transition']:
   if isinstance(s.get(key),str):
    for old,new in text_pairs.items():s[key]=s[key].replace(old,new)
    s[key]=s[key].replace('沧龙出海','沧龙天倾').replace('そうりゅうしゅつかい','そうりゅうてんけい')
 write(FIX+'/本轮对位采用.json',dict(choices_source_sha256=sha('后期/配音挑选-v022/作者选择.json'),author_instruction='先用现有 v005 新词录音完成对位',items=selected))

 oldvp=load(OLDFIX+'/配音对位方案.json');oldvc={c['id']:c for c in oldvp['cues']}
 plan=remap(load(OLD+'/批次计划.json'));oldplan=load(OLD+'/批次计划.json')
 for f in (ROOT/OLD).glob('*.json'):
  if f.name not in ['展开数据.json','结构核验.json']:write(OUT+'/'+f.name,remap(load(OLD+'/'+f.name)))
 # Measure exactly what ffmpeg will put in the 48kHz preview. Never trim tails.
 facts=[]
 for a in mapping['cues']:
  raw=subprocess.run(['ffmpeg','-v','error','-i',str(ROOT/a['path']),'-vn','-ac','2','-ar','48000','-f','f32le','pipe:1'],capture_output=True,check=True).stdout
  count=len(raw)//8;a.update(sha256=sha(a['path']),file_seconds=count/48000,budget_seconds=count/48000)
  facts.append(dict(cue_id=a['cue_id'],path=a['path'],sha256=a['sha256'],decoded_frames_48k=count,seconds=count/48000))
 write(FIX+'/音频实测.json',facts)
 byshot={s['id']:[a for a in mapping['cues'] if a['shot_id']==s['id']] for s in src['shots']}
 offsets={};changes=[]
 for s in src['shots']:
  sid=s['id'];aa=byshot[sid]
  if not aa:continue
  aa.sort(key=lambda a:a['timeline_start'])
  oldc={c['cue_id']:c for c in s.get('subtitle_cues',[])}
  cursor=0
  for i,a in enumerate(aa):
   cid=a['cue_id'];lead=max(0,a['timeline_start']-s['start_second']) if i==0 else cursor+.3
   if sid=='CY008M':lead=.25 if i==0 else cursor+.2
   if sid=='CY028A':lead=.1 if i==0 else 2.8 # same shot: step down, then close face at 2.7
   if sid=='CY024A':lead=3.79 # retain lift-off before the full file's natural leading silence
   if sid=='CY024A5':lead=0 if i==0 else cursor+.8
   if sid=='CY024K0':lead=0 if i==0 else cursor # continuous request, existing file silence retained
   if sid in ['CY028B','CY028C','CY029E1','CY029E2','CY029E3','CY029E4','CY029B1']:lead=0
   offsets[cid]=round(lead,6);cursor=lead+a['file_seconds']
  # These two whole phrases deliberately cross multiple visual shots.
  if sid in ['CY021','CY024A9']:continue
  tail=.3 if sid=='CY008M' else (.6 if sid=='CY024K0' else .1)
  need=math.ceil((cursor+tail-1e-8)*100)/100
  if cursor>s['seconds'] or sid in ['CY008M','CY024K0']:s['seconds']=max(s['seconds'],need)
  if sid=='CY028B':s['seconds']=round(cursor+.5,6) # retain the new original clause handoff gap
  if sid=='CY003B':s['seconds']=round(cursor+.04,6) # complete unfinished phrase, cut immediately after its file tail
  if sid=='CY028C':s['seconds']=round(cursor,6) # father window begins at the actual complete file end
 # Inner-world frame remains one <15s shot with complete audio and a short waiting beat.
 assert sm['CY008M']['seconds']<=15
 cursor=0
 for s in src['shots']:
  s['start_second']=round(cursor,6);cursor+=s['seconds'];s['end_second']=round(cursor,6)
  if s['seconds']!=oldsm[s['id']]['seconds']:changes.append(dict(shot_id=s['id'],title=s['title'],old_seconds=oldsm[s['id']]['seconds'],new_seconds=s['seconds'],reason='按新版分句衔接并让真实词尾紧接6秒父亲停顿' if s['id'] in ['CY028B','CY028C'] else '完整新版日语原速＋必要交接/动作留白'))
 total=round(cursor,6)
 # All display cues and actual playback events come from the same full dry file.
 cues=[];events=[]
 alias={'VO-CY024A5-01':'MASTER-GPT-2','VO-CY024A5-02':'MASTER-GPT-3'}
 for s in src['shots']:
  sid=s['id'];oldsubs={c['cue_id']:c for c in s.get('subtitle_cues',[])};subs=[]
  for a in byshot[sid]:
   cid=a['cue_id'];off=offsets[cid];start=round(s['start_second']+off,6);end=round(start+a['file_seconds'],6)
   visible=[x['id'] for x in src['shots'] if x['start_second']<end-1e-6 and x['end_second']>start+1e-6]
   sub=copy.deepcopy(oldsubs[cid]);sub.update(offset=off,duration=round(a['file_seconds'],6),visual_shots=visible,cross_shot_offscreen=len(visible)>1)
   subs.append(sub)
   a.update(timeline_start=start,timeline_end=end,budget_seconds=round(a['file_seconds'],6),visual_shots=visible,mix_source='dry_file',master=None,state='v025_selected_voice_retimed',note='本句完整新版干声仅混入一次；不变速、不截字。镜内剩余时间留给动作、反应与环境声。')
   c=dict(id=cid,role=a['speaker'],shot_id=sid,text_ja=a['text'],file=a['path'],sha256=a['sha256'],file_in=0,file_out=a['file_seconds'],rate=1,timeline_start=start,timeline_end=end,shot_relative_start=off,shot_relative_end=round(off+a['file_seconds'],6),visual_shots=visible,cross_shot_offscreen=len(visible)>1,mix_source='dry_file',estimated_word_boundaries=False,note='整句文件边界实测；文件内停顿原样保留，非逐词对齐。')
   cues.append(c);events.append(dict(id=alias.get(cid,cid),cue_id=cid,file=a['path'],file_in=0,file_out=a['file_seconds'],rate=1,timeline_start=start,timeline_end=end))
  s['subtitle_cues']=subs
 tc={c['id']:c for c in cues}
 # Remove old bridge syllable splitting; retain one uninterrupted cue across the same five shots.
 src['previous_incantation_bridge']=src.get('music_direction',{}).pop('incantation_bridge',None)
 plan['continuous_line_parts']={}
 # Source-owned timing prose. Old narrative/visual actions stay; stale audio budgets are replaced.
 for s in src['shots']:
  aa=byshot[s['id']]
  if not aa:continue
  s['previous_sound_v063']=s['sound']
  clean=s['sound'].replace('按完整文件原速；句内停顿保留，余下闭口表演；跨镜时声音连续，不让画内其他人物代说。','').replace('双方不重叠，尚无人返回。','').replace('全镜无攻击和撞盾。','')
  ambient=re.sub(r'[^。；]*(?:\d|母版|待配音)[^。；]*[。；]?','',clean).strip()
  ambient=re.sub(r'[^。；]*(?:日语|配音|译配|预算|对白|台词|字幕|原声|待录|待补|待制作)[^。；]*[。；]?','',ambient).strip()
  windows='；'.join(f"{a['speaker']}在镜内{n(offsets[a['cue_id']])}–{n(offsets[a['cue_id']]+a['file_seconds'])}秒说完同一句日语" for a in aa)
  s['sound']=ambient+' '+windows+'。按完整文件原速；句内停顿保留，余下闭口表演；跨镜时声音连续，不让画内其他人物代说。'
  s['sound']=re.sub(r'[^。；]*(?:待制作|暂定|待配|待生成)[^。；]*[。；]?','',s['sound'])
 sm['CY016A']['sound']+=' 双方不重叠，尚无人返回。'
 sm['CY024K0']['sound']+=' 两句说完再短停投刃，镜尾明刃已离手；玻璃撞击只在下一镜。'
 sm['CY024K1A']['sound']+=' 刀尖先入木，术名说完仍留坐标低鸣；下一镜才瞬移爆气。'
 sm['CY028A2']['sound']+=' GPT在画外回答，小鱼无词反应；不可提前覆盖Claude前镜的提问。'
 sm['CY029']['sound']+=' 本镜与下一镜合计保持6秒Claude停顿；父亲只在此窗口说一次。'
 sm['CY029E']['sound']='父亲原句已经完整结束，沿倒影切父亲无声伸手反应，只留环境尾声；两镜合计6秒满后，下一镜Claude才续咏。'
 for sid in plan['execution_notes']:
  if sid in sm:plan['execution_notes'][sid]=re.sub(r'镜长[\d.]+秒',f'镜长{n(sm[sid]["seconds"])}秒',plan['execution_notes'][sid])
 for sid in ['CY016A','CY024K0','CY024A','CY024A2','CY024A6','CY028B','CY028C','CY029','CY029E','CY029E1','CY029E2','CY029E3','CY029E4']:
  plan['execution_notes'][sid]=f'镜长{n(sm[sid]["seconds"])}秒。'+sm[sid]['sound']
 plan['execution_notes']['CY024A5A']='保留1.5秒破顶镜，本镜无新语音；下一镜从下一条完整日语干声起，不重复前句。'
 plan['shot_notes']['CY024K0']='Kimi现场完整请求两句，句间沿用原文件自然停顿；两句说完再投刃。显形已在前镜4秒完成。'
 plan['shot_notes']['CY021']='延续唯一一次撑地失败，不再次摔倒；Claude完整4.13秒求情画外连续，跨下一镜约0.33秒，宝宝不代说。维持现有构图与光源。'
 plan['shot_notes']['CY031A']='按下方实测窗口先邀请落座，再完整回应；先坐下、后接勺，双方不重叠。'
 a1,a2=byshot['CY008M'];t1=offsets[a1['cue_id']];e1=t1+a1['file_seconds'];t2=offsets[a2['cue_id']];e2=t2+a2['file_seconds']
 sm['CY008M']['action']=f'0–{n(t1)}秒王座本体与背景定格虚化，两只分身显现。{n(t1)}–{n(e1)}秒恶魔抱臂提醒，天使闭口听；{n(e1)}–{n(t2)}秒交接停顿；{n(t2)}–{n(e2)}秒天使先心疼看向小鱼画外位置，再焦急反驳，恶魔闭口听。余下至{n(sm["CY008M"]["seconds"])}秒两只分身闭口等待，本体不回答、不点头。'
 for states in ['state_references','review_state_sequence']:
  for i,st in enumerate(sm['CY008M'].get(states,[])):
   if states=='state_references':st['offset']=[0,t1,round(e2,6)][i]
   else:st['offset']=[t1,t2,round(e2,6)][i]
 sm['CY024A5']['action']=sm['CY024A5']['action'].split(' 以本版对白窗口')[0].split(' 术名在本镜')[0]+' 以本版对白窗口完成祈愿，完整保留0.8秒空窗，再报术名。词尾结束后闭口蓄势至镜尾；下一镜才解印出击。'
 sm['CY024A5']['sound']+=' 祈愿与术名之间音乐静音0.8秒，保留后期水声；全镜无攻击和撞盾。'
 sm['CY029B1']['action']=sm['CY029B1']['action'].replace('4.36秒完整文件与词尾全部保留','新版完整术名与词尾全部保留，剩余时间闭口凝视同一火种')
 sm['CY034']['sound']='尾乐在本镜前3秒内收尽；最后4秒BGM静音，只留街市声与两人呼吸。'
 sm['CY028A']['invariants']=[re.sub(r'0\.1–2\.6秒GPT、2\.8–6\.08秒Claude原速对白不变。','对白时点以v021实测窗口为准，站稳后收近和2.7秒状态点不变。',x) for x in sm['CY028A']['invariants']]
 for cid,revision in revisions.items():
  sid=am[cid]['shot_id']
  sm[sid]['action']+=' '+revision['direction']
 for shot in src['shots']:
  shot['invariants']=[x.replace('沧龙出海','沧龙天倾').replace('v021实测窗口','v025实测窗口') for x in shot.get('invariants',[])]
 for scene in src['scenes']:scene['seconds']=round(sum(sm[i]['seconds'] for i in scene['shot_ids']),6)
 src.update(version='v0.65',revision='v065',previous_source=BASE,total_seconds=total,title='《白米饭》带图分镜 v0.65 · 新日语语音与音乐同源对位',subtitle=f'133镜 · {n(total)}秒 · 新语音原速对位',audio_repair_plan=FIX+'/配音对位方案.json',roughcut_preview=FIX+'/全片声音预览.html')
 src['story_script']='剧本/白米饭-场景剧本-v0.64.md'
 src['music_direction']['estimated_gpt_incantation_seconds']=round(tc['VO-CY024A5-02']['timeline_end']-tc['VO-CY024A-01']['timeline_start'],6)
 script=(ROOT/'剧本/白米饭-场景剧本-v0.63.md').read_text('utf8')
 for old,new in text_pairs.items():script=script.replace(old,new)
 script=script.replace('沧龙出海','沧龙天倾').replace('そうりゅうしゅつかい','そうりゅうてんけい').replace('水之灵','纯水之主')
 note='# v0.64 新台词与作者选声对位（2026-10-27）\n\n当前镜头源v0.65、工作台v025。下方历史时长以本轮实测窗口为准。七句新台词已同步；两句v005按作者授权用于对位，旧选择仅留音色对照。\n\n'
 for cid,r in revisions.items():note+=f"- {cid}：{r['zh']}／{r['ja']}\n"
 (ROOT/src['story_script']).write_text(note+'\n---\n\n'+script,'utf8')
 src['revision_notes']=dict(scope='保留画面，采用7句修订及61条作者选择、2条授权v005对位音频；完整原速重排，BGM由镜号锚点解析。',audio_facts=FIX+'/音频实测.json')
 write(SOURCE,src);sourcehash=sha(SOURCE)
 # Safe shot-group boundaries: never split an utterance, nor an indivisible visual shot.
 batches=[];parent={};shotbatch={}
 cross_groups=[set(c['visual_shots']) for c in cues if c['cross_shot_offscreen']]
 for old in oldplan['batches']:
  ids=old['shot_ids'];chunks=[];chunk=[]
  for sid in ids:
   if chunk and sum(sm[x]['seconds'] for x in chunk)+sm[sid]['seconds']>15+1e-6:
    assert not any(set(chunk)&g and sid in g for g in cross_groups),'Unsafe voice split'
    chunks.append(chunk);chunk=[]
   chunk.append(sid)
  if chunk:chunks.append(chunk)
  for k,ss in enumerate(chunks):
   b=copy.deepcopy(old);bid=old['id'] if k==0 else old['id']+'R'+str(k+1)
   b.update(id=bid,shot_ids=ss,title=old['title'] if len(chunks)==1 else '、'.join(sm[i]['title'] for i in ss),group_reason='按完整新版语音与动作窗口合批；只在镜间且无连续对白跨越处切开。',handle_reason='15秒请求内未用尾部仅延续末态，剪辑时去除。',status='v025_inputs_prepared_not_submitted')
   assert sum(sm[x]['seconds'] for x in ss)<=15+1e-6
   batches.append(b);parent[bid]=old['id']
   for sid in ss:shotbatch[sid]=bid
 # Regenerate associated reviews from final source and timing.
 dirs=remap(load(OLD+'/动态审查.json'));olddirs=copy.deepcopy(dirs['batches']);dirs['batches']={}
 sounds=remap(load(OLD+'/声音核对.json'));cast=remap(load(OLD+'/人物核对.json'))
 rhythm=remap(load(OLD+'/配乐卡点方案.json'));oldrh=copy.deepcopy(rhythm['batches']);rhythm['batches']={}
 audit=remap(load(OLD+'/对白复核.json'));oldaudit={(x['batch_id'],x['cue_index']):copy.deepcopy(x) for x in audit['cues']};audit['cues']=[];audit['batches']=[]
 for b in batches:
  bid=b['id'];pb=parent[bid];d=copy.deepcopy(olddirs[pb]);d['shots']={sid:d['shots'][sid] for sid in b['shot_ids']}
  if bid!=pb:d['entry_bridge_zh']='接上一批同一场景，延续前镜状态；不重说、不重演。'
  for sid,rv in d['shots'].items():
   if byshot[sid] or sid in ['CY029E','CY034']:
    rv['action_zh_override']=sm[sid]['action'];rv['effects_zh_override']=sm[sid]['sound']
    rv['effects_en']='Use the exact new Japanese dialogue windows below, once at natural speed. Keep ambience and action sounds subdued under speech. Silence between lines is intentional.'
    # English direction previously carried old timing; current source action is authoritative.
    rv['action_en']=sm[sid]['action']
    sounds[sid]['effects']=sm[sid]['sound']
    if 'action_override' in sounds[sid]:sounds[sid]['action_override']=sm[sid]['action']
    plan.get('action_overrides',{}).pop(sid,None)
   if sid=='CY028A':
    plan['execution_notes'][sid]=sm[sid]['sound']+' 保持0秒旧全景空间参考、2.7秒新近景；同一镜不跳切。'
    plan['shot_notes'][sid]='旧宽景只约束起段空间，新近景是站稳后状态。'
   if sid=='CY028A2':rv['transition_zh']='接Claude问孩子，切小鱼反应；GPT在本镜画外完整回答4.07秒，不提前覆盖上一镜。'
   if sid=='CY028B':
    rv['transition_zh']='Claude第一句完整咏唱在本镜结束，保留0.5秒交接空白，再切腕部特写。'
    rv['transition_en']='Finish the complete first Claude line here, hold the half-second handoff, then cut to the wrist close-up.'
   if sid=='CY028C':
    rv['transition_zh']='腕部特写从下一句完整咏唱开始；本句结束即进入父亲插话的6秒窗口。'
    rv['transition_en']='Begin the next complete Claude line on the wrist close-up; its full ending opens the six-second father interruption window.'
   if sid=='CY029E':
    rv['transition_zh']='父亲原声已经完整结束，沿倒影切父亲无声伸手反应，只留环境尾响；6秒插话窗口满后下一镜Claude续咏。'
    rv['transition_en']='The father line has already ended. Cut along the reflection to the father silently reaching out, with ambience only; Claude resumes chanting next shot after the full six-second interruption window.'
   if sid=='CY029E4':
    rv['transition_zh']='从掌心凝种切小鱼攥衣仰望；Claude下一条完整咏唱在本镜开始，前句不重起。'
    rv['transition_en']='Cut from the formed ember to the child looking up; start the next complete Claude line here once.'
  dirs['batches'][bid]=d
  rh=copy.deepcopy(oldrh[pb]);rh['points']=[];rhythm['batches'][bid]=rh
  aa=sorted([a for a in mapping['cues'] if a['shot_id'] in b['shot_ids']],key=lambda a:a['timeline_start'])
  for index,a in enumerate(aa):
   review=copy.deepcopy(oldaudit[(a['batch_id'],a['cue_index'])]);a.update(batch_id=bid,cue_index=index)
   bs=sm[b['shot_ids'][0]]['start_second']
   review.update(batch_id=bid,cue_index=index,start=round(a['timeline_start']-bs,6),end=round(a['timeline_end']-bs,6),duration=round(a['file_seconds'],6),film_start=a['timeline_start'],film_end=a['timeline_end'],current_text=a['text'])
   if a['cue_id'] in revisions:review['source_text']=revisions[a['cue_id']]['zh']
   audit['cues'].append(review)
  audit['batches'].append(dict(batch_id=bid,title=b['title'],context=d['arc_zh'],has_dialogue=bool(aa),cue_count=len(aa)))
 # Existing action anchors remain the editing authority; resolved clocks assigned by builder.
 bgm=remap(load(OLDFIX+'/BGM剪辑方案.json'))
 for p in bgm['action_points']:
  sid=p['anchor']['shot_id'];bid=shotbatch[sid]
  point=next((x for rh in oldrh.values() for x in rh['points'] if x['action_zh']==p['action_zh']),None)
  if point:
   point=copy.deepcopy(point);time=sm[sid]['start_second']+p['anchor'].get('offset_seconds',0)
   point.update(time=round(time-sm[next(b['shot_ids'][0] for b in batches if b['id']==bid)]['start_second'],6),film_time=round(time,6))
   rhythm['batches'][bid]['points'].append(point)
 # Kimi's longer request moves the impact beyond the old music pre-roll. Use an existing later measured candidate.
 m7=next(c for c in bgm['cues'] if c['id']=='M07');oldhit=copy.deepcopy(m7['source_alignment']['evidence'])
 m7['source_alignment']['previous_evidence_v020']=oldhit
 m7['source_alignment']['evidence'].update(source_seconds=27.70141,score=.470958,listening_verified=False)
 m7['retime_note']='新版Kimi完整请求延长，旧22.29116秒瞬态会导致源入点为负；改用已测27.70141秒候选，待乐句听审。'
 prayer=tc['VO-CY024A5-01'];spell=tc['VO-CY024A5-02'];po=prayer['shot_relative_end'];so=spell['shot_relative_start']
 for c in bgm['cues']:
  if c['id']=='M09':c['end_anchor']['offset_seconds']=po
  if c['id']=='M10':c['start_anchor']['offset_seconds']=so
 for z in bgm['silences']:
  if z['id']=='S04':z['start_anchor']['offset_seconds']=po;z['end_anchor']['offset_seconds']=so
 for p in bgm['action_points']:
  if p['action_zh']=='结印镜中咏唱暂停':p['anchor']['offset_seconds']=po
 write(FIX+'/BGM剪辑方案.json',bgm)
 vp=dict(status='v025_selected_audio_aligned_pending_review',source=SOURCE,source_sha256=sourcehash,old_duration=baseline['total_seconds'],new_duration=total,duration_delta=round(total-baseline['total_seconds'],6),policy=dict(mix_instruction='63条完整新版干声各一次；母版只留溯源不叠加。句内原始停顿保留，句间根据镜头留白；禁止变速或截尾。'),masters=[],previous_masters_provenance=oldvp.get('previous_masters_provenance',oldvp.get('masters',[])),cues=cues,mix_events=events,shots=[dict(shot_id=s['id'],old_start=oldsm[s['id']]['start_second'],old_seconds=oldsm[s['id']]['seconds'],new_start=s['start_second'],new_end=s['end_second'],new_seconds=s['seconds'],delta_seconds=round(s['seconds']-oldsm[s['id']]['seconds'],6)) for s in src['shots']],protected_beats=copy.deepcopy(oldvp['protected_beats']),music_duck_regions=[dict(id='inner-world',start=sm['CY008M']['start_second'],end=sm['CY008M']['end_second'],gain_db=-7,attack_seconds=.2,release_seconds=.2,reason='整个内心戏持续压低音乐，句间不弹回')])
 vp['protected_beats']['claude_pause']=[sm['CY029']['start_second'],sm['CY029E']['end_second']]
 write(FIX+'/配音对位方案.json',vp)
 mapping['revision']=dict(version='v025',note='基于最新v020选定路径实测完整文件，更新全部窗口与批次，句内音频无改动。');write(OUT+'/日语音频映射.json',mapping)
 plan.update(version='v025',source=SOURCE,batches=batches,output=OUT+'/生成板.html')
 plan['sound_policy']='63句完整新版日语干声各一次，语音自然原速，镜头迁就长句；短句后的动作/反应留白保留。只上传图片，配音与BGM后期替换。'
 plan['audio_execution']['display_note']='63句新版语音实测窗口与画面、字幕、BGM锚点同源；只上传图片，未提交视频。'
 plan['audio_execution']['replacement_note']='63条完整干声各一次，连续母版保留历史但不叠加；不变速，不截字。'
 plan['audio_revision']=dict(principle='full_dry_audio_voice_first',author_status='61句保留作者已选，2句现有v005获授权用于对位；全片节奏试听待验收。')
 plan['mix_notes']=['七首既有曲目按镜号动作锚点重剪，不整体循环、不拉伸。','63句完整新版干声各一次，字幕与生成窗口同步。','4秒显形、6秒父亲插话窗口、0.8秒祈愿停乐及结尾4秒无BGM保持。']
 for data in [dirs,cast,rhythm,audit]:data.update(source=SOURCE,source_sha256=sourcehash)
 audit['counts']['batches']=len(batches);audit.update(version='v025',summary='63句完整新版干声的实测对位，逐词和动态口型仍另验。')
 loc=remap(load(OLD+'/日语译配.json'));loc['source_sha256']=sourcehash;loc['continuous_line_parts']={}
 for cid,r in revisions.items():
  loc['translations'][r['zh']]=r['ja']
  loc['approved_translations'][r['zh']]=dict(text=r['ja'],status='author_requested_revision_used_for_alignment',date='2026-10-27')
 for old,new in text_pairs.items():
  if old!=new:loc['translations'].pop(old,None)
 loc['pronunciation_drafts'].pop('沧龙出海',None)
 loc['pronunciation_drafts']['沧龙天倾']='蒼龍天傾（そうりゅうてんけい）'

 for name,data in [('批次计划.json',plan),('动态审查.json',dirs),('人物核对.json',cast),('声音核对.json',sounds),('配乐卡点方案.json',rhythm),('对白复核.json',audit),('日语译配.json',loc)]:write(OUT+'/'+name,data)
 audit['localization_sha256']=sha(OUT+'/日语译配.json');write(OUT+'/对白复核.json',audit)
 write(FIX+'/重排明细.json',dict(old_seconds=baseline['total_seconds'],new_seconds=total,changed_shots=changes,old_batches=len(oldplan['batches']),new_batches=len(batches),batch_parents=parent,images_unchanged=True,full_dry_events=63))
 write(FIX+'/输入快照哈希.json',{p:sha(p) for p in [BASE,OLD+'/批次计划.json',OLD+'/日语音频映射.json',OLDFIX+'/配音对位方案.json',OLDFIX+'/BGM剪辑方案.json']})
 print(json.dumps(dict(seconds=total,batches=len(batches),changed_shots=changes),ensure_ascii=False))

if __name__=='__main__':main()
