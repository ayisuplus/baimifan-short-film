"""Versioned, local-only consolidation of the reviewed pre-generation repairs."""
import copy, hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OLD='视频制作/生成板-v012/'
OUT='视频制作/生成板-v014/'
FIX='后期/生成前修正-v014/'
SOURCE='镜头设计/shot-plan-v0.59.json'
SNAPSHOTS=json.loads((ROOT/FIX/'输入快照.json').read_text('utf-8'))
def load(p):
    key=str(p).replace('\\','/')
    if key in SNAPSHOTS:
        record=SNAPSHOTS[key];p=record['snapshot'];assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==record['sha256'],p
    return json.loads((ROOT/p).read_text('utf-8-sig'))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def write(p,d):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def replace_terms(d):
    if isinstance(d,dict):return {k:replace_terms(v) for k,v in d.items()}
    if isinstance(d,list):return [replace_terms(v) for v in d]
    if isinstance(d,str) and not re.search(r'\.(wav|mp3|png|json|md|html)\b',d):return d.replace('沧海天倾','沧龙出海').replace('そうかいてんけい','そうりゅうしゅつかい')
    return d
def shift(d):
    for key in ('timeline_start','timeline_end','film_start','film_end'):
        if isinstance(d.get(key),(float,int)) and d[key]>=53:d[key]=round(d[key]+13.5,6)

def main():
    source=replace_terms(load('镜头设计/shot-plan-v0.58.json'))
    plan=replace_terms(load(OLD+'批次计划.json'))
    inner=load('镜头设计/王宫内心戏-已采用增补-v001.json')
    sm={s['id']:s for s in source['shots']}
    baseline_hashes={p:sha(p) for p in ['镜头设计/shot-plan-v0.58.json','镜头设计/王宫内心戏-已采用增补-v001.json',OLD+'日语译配.json',OLD+'日语音频映射.json','后期/收尾修复-v001/配音对位方案.json']}
    for s in source['shots']:
        if s['start_second']>=53:
            s['start_second']=round(s['start_second']+13.5,6);s['end_second']=round(s['end_second']+13.5,6)
    for job in load('镜头设计/生成记录/生成前修正-v059/请求.json'):
        if job['id'] not in sm or job.get('selected_for_v014') is False:continue
        s=sm[job['id']];s['previous_presentation_v058']=copy.deepcopy(s['presentation'])
        s['presentation'].update(path=job['project_output'],status='生成前修正候选，待作者审阅',missing='仍需动态验证；未自动认定作者采用')
        s['generation_request']='镜头设计/生成记录/生成前修正-v059/请求.json'
        s['refs'].insert(0,dict(path=job['project_output'],role='当前修正候选；旧图保留溯源'))
        s['final_static_review']={'version':'v059','status':'repair_candidate_pending_author_review'}
        if job['id'] in ['CY024A7','CY024A5A','CY024A5','CY024A5B','CY024B']:s['invariants'].append('水龙是流体法术：眼窝为深蓝折射与水流暗部，无实体眼球、虹膜、瞳孔、固定亮点；不影响GPT本人眼睛。')
    base=inner['reference_images'][2]['path'];states=inner['state_sequence']
    s=dict(id='CY008M',scene='S02',scene_title='宫殿求助',title='协议与怜悯：内心争执',seconds=13.5,start_second=53,end_second=66.5,
        framing='王座反应近景，固定机位',purpose=inner['shot_design']['purpose'],entry_state='本体侧躺于卧榻；分身尚未出现。',
        action='0–0.6秒本体与背景定格虚化，前景两只Q版分身显现。0.6–4.18秒左侧恶魔抱臂慢悠悠提醒，天使闭口听；4.18–4.53秒停顿。4.53–12.33秒右侧天使先心疼看向小鱼画外位置，再焦急转向本体反驳，恶魔闭口听。12.33–13.5秒两只分身闭口抬眼等待，本体不回答、不点头。',
        exit_state='分身等待，争执不判胜负；下一批小鱼完整原声画外起句打断，随即切回现实。',dialogue='；'.join(c['speaker']+'：'+c['source_text'] for c in inner['cues']),
        sound='内心段配乐与现实空间声收低；仅当前分身开口，另一只和本体闭口；不添加叹词或胜负结论。',next_link='接CY009：小鱼原句一次，恢复现实。',
        invariants=[inner['visual'],inner['devil_color_direction'],'本体和背景复用同一张王座底图；禁止背景游动或让本体参与分身动作。'],asset_ids=['CHAR-GPT-ANGEL-CHIBI','CHAR-GPT-DEVIL-CHIBI'],
        presentation=dict(path=base,role='frozen_background',visible='本体侧躺的固定背景底板，分身另按状态进入',status='既有王座底图',show_as_main=True,missing='合成冻结与分身动态需视频验证'),
        refs=copy.deepcopy(inner['reference_images']),subtitle_cues=[],dialogue_cues=[],priority='normal',
        state_references=[dict(path=base,offset=0,label='王座定格底板',label_en='Frozen throne plate'),dict(path=states[0]['path'],offset=.6,label='恶魔提醒',label_en='Devil speaks; angel listens'),dict(path=states[2]['path'],offset=12.33,label='闭口等待',label_en='Both wait silently')],
        review_state_sequence=[dict(path=states[i]['path'],offset=t,label=states[i]['label']) for i,t in enumerate([.6,4.53,12.33])])
    for c,t in zip(inner['cues'],[.6,4.53]):
        s['subtitle_cues'].append(dict(speaker=c['speaker'],text=c['source_text'],offset=t,duration=c['duration_seconds'],cue_id=c['id'],cross_shot_offscreen=False,visual_shots=['CY008M']))
    source['shots'].insert(next(i for i,x in enumerate(source['shots']) if x['id']=='CY009'),s);sm[s['id']]=s
    sm['CY008']['next_link']='接CY008M：王座本体定格，内心分身出现。'
    sm['CY009']['subtitle_cues'][0].update(offset=0)
    sm['CY009']['action']='小鱼完整原句从画外起声打断内心争执；在起句的切点回到现实小鱼近景，然后转身离开。原句只播放一次，不由GPT或分身代说。'+sm['CY009']['action']
    sm['CY009']['entry_state']='内心分身尚在等待；小鱼起句打断，切回现实，分身消失。'
    sm['CY024A5']['subtitle_cues'][-1].update(text='沧龙出海！',duration=2.03)
    sm['CY024A5']['action']+=' 术名在本镜8.57秒说完，之后闭口保持手印至12秒镜尾，不重复、不拉长发声；下一镜才解印出击。'
    sm['CY024A5']['sound']='0–5.74秒完整救赎祈愿；5.74–6.54秒保留0.8秒语音空窗并收音乐；6.54–8.57秒完整新术名，8.57–12秒闭口蓄势留白。水龙与双手持续蓄势，全镜无攻击、撞盾或提前重音。'
    sm['CY034']['sound']=sm['CY034']['sound'].replace('446.9–450.9','460.4–464.4')
    for scene in source['scenes']:
        if 'CY008' in scene['shot_ids']:scene['shot_ids'].insert(scene['shot_ids'].index('CY008')+1,'CY008M')
        scene['seconds']=round(sum(sm[i]['seconds'] for i in scene['shot_ids']),6)
    marks=load(source['music_adoption']);marks['marks']['CY008M']=marks['marks']['CY007'];marks['version']='v059';write(FIX+'作者确认选曲.json',marks)
    source.update(version='v0.59',revision='v059',previous_source='镜头设计/shot-plan-v0.58.json',total_seconds=464.4,subtitle='133镜 · 464.4秒 · 63句日语 · 41批生成修正版',music_adoption=FIX+'作者确认选曲.json',audio_repair_plan=FIX+'配音对位方案.json',roughcut_preview=FIX+'全片声音预览.html')
    source['revision_notes']={'scope':'已授权生成前修正：统一内心戏、术名、图片、实际音频时码；历史输入保留。','baseline_hashes':baseline_hashes}
    source['music_direction']['estimated_gpt_incantation_seconds']=49.57
    write(SOURCE,source);h=sha(SOURCE)
    timing=replace_terms(load('后期/收尾修复-v001/配音对位方案.json'))
    timing.update(source=SOURCE,source_sha256=h,old_duration=450.9,new_duration=464.4,duration_delta=13.5,status='v014_natural_speed_retimed_pending_audition')
    timing['shots']=[dict(shot_id=x['id'],old_start=x['start_second']-(13.5 if x['start_second']>=66.5 else 0),old_seconds=0 if x['id']=='CY008M' else x['seconds'],new_start=x['start_second'],new_end=x['end_second'],new_seconds=x['seconds'],delta_seconds=13.5 if x['id']=='CY008M' else 0,direction='新增完整内心戏；下游整体顺延，原速音频。') for x in source['shots']]
    for c in timing['cues']:shift(c)
    for e in timing['mix_events']:shift(e)
    for m in timing['masters']:
        for seg in m['segments']:shift(seg)
        if m['id']=='GPT':
            retired=m['segments'].pop();m['retired_segments']=[dict(**retired,reason='作者改术名，旧词原件保留而不混入v014；以独立沧龙出海v002替换')]
    timing['protected_beats']['claude_pause']=[round(t+13.5,6) for t in timing['protected_beats']['claude_pause']]
    tc={c['id']:c for c in timing['cues']}
    c=tc['VO-CY009-01'];c.update(timeline_start=66.5,timeline_end=68.2,shot_relative_start=0,shot_relative_end=1.7,cross_shot_offscreen=False,offscreen_entry=True)
    e=next(e for e in timing['mix_events'] if e['id']=='VO-CY009-01');e.update(timeline_start=66.5,timeline_end=68.2)
    aud=replace_terms(load(OLD+'日语音频映射.json'));am={c['cue_id']:c for c in aud['cues']};a=am['VO-CY024A5-02']
    c=tc['VO-CY024A5-02'];c.update(file=a['path'],sha256=sha(a['path']),file_in=0,file_out=2.03,text_ja='そうりゅうしゅつかい！',timeline_end=round(c['timeline_start']+2.03,6),shot_relative_end=8.57,mix_source='dry_file',estimated_word_boundaries=False)
    c['replaced_master_provenance']={k:c.pop(k) for k in list(c) if k.startswith('master_')}
    e=next(e for e in timing['mix_events'] if e['id']=='MASTER-GPT-3');e.update(file=c['file'],file_in=0,file_out=2.03,timeline_start=c['timeline_start'],timeline_end=c['timeline_end'],replacement_of='GPT master 47.54–53s retired by author spell revision')
    for ic,t in zip(inner['cues'],[53.6,57.53]):
        c=dict(id=ic['id'],role=ic['speaker'],shot_id='CY008M',text_ja=ic['ja_draft'],file=ic['audio_path'],sha256=sha(ic['audio_path']),file_in=0,file_out=ic['duration_seconds'],rate=1,timeline_start=t,timeline_end=round(t+ic['duration_seconds'],6),shot_relative_start=round(t-53,6),shot_relative_end=round(t-53+ic['duration_seconds'],6),visual_shots=['CY008M'],cross_shot_offscreen=False,mix_source='dry_file',estimated_word_boundaries=False)
        timing['cues'].append(c);timing['mix_events'].append({k:c[k] for k in ['id','file','file_in','file_out','rate','timeline_start','timeline_end']})
    timing['cues'].sort(key=lambda c:c['timeline_start']);timing['mix_events'].sort(key=lambda c:c['timeline_start'])
    timing['music_duck_regions']=[dict(id='inner-world',start=53,end=66.5,gain_db=-7,attack_seconds=.2,release_seconds=.2,reason='整段内心戏持续压低配乐，句间不弹回；与对白duck取较低值，不重复叠加')]
    timing['policy']['spell_revision']='旧GPT母版最后5.46秒已明确退役；以完整2.03秒新术名替换，原母版前47.54秒仍仅用一次。' if isinstance(timing.get('policy'),dict) else None
    write(FIX+'配音对位方案.json',timing)
    write(FIX+'BGM剪辑方案.json',load('后期/收尾修复-v001/BGM剪辑方案.json'))
    # Independent review sources are copied forward; original boards remain immutable.
    dirs=replace_terms(load(OLD+'动态审查.json'));cast=load(OLD+'人物核对.json');sound=replace_terms(load(OLD+'声音核对.json'));loc=load(OLD+'日语译配.json');audit=replace_terms(load(OLD+'对白复核.json'));rhythm=load(OLD+'配乐卡点方案.json')
    ib=dict(id='GB004M',title='协议与怜悯：内心争执',shot_ids=['CY008M'],group_reason='完整两句11.38秒，加显现、换气和等待，共13.5秒。',handle_reason='末尾1.5秒只延续等待，后期剪除。',status='repair_candidate_not_submitted')
    plan['batches'].insert(4,ib)
    dirs['batches']['GB004M']=dict(arc_zh=s['purpose'],arc_en='A frozen adult GPT is torn between her devil and angel avatars; neither wins.',entry_bridge_zh=s['entry_state'],exit_bridge_zh=s['exit_state'],shots={'CY008M':dict(camera_zh=s['framing'],camera_en='Locked camera; one frozen blurred adult/background plate.',transition_zh=inner['shot_design']['entry'],transition_en='Cut to the adult reaction, freeze and defocus the plate, then reveal the two avatars.',action_en='Devil speaks from 0.6 to 4.18s; angel replies from 4.53 to 12.33s. Both wait silently to 13.5s; adult never moves or answers. Neither wins.',effects_en='Inner-world air; only the current avatar speaks; no added words.',action_zh_override=s['action'],effects_zh_override=s['sound'])})
    dirs['batches']['GB005']['shots']['CY009'].update(action_zh_override=sm['CY009']['action'],transition_zh='小鱼原句从画外起声，随即切回现实小鱼近景并转身离开；不重复起句。',transition_en='The child begins offscreen, interrupting the inner world; immediately cut to her and follow her departure. The line occurs once.')
    dirs['batches']['GB022-1']['shots']['CY024A5']['action_zh_override']=sm['CY024A5']['action']
    dirs['batches']['GB022-1']['shots']['CY024A5']['action_en']+=' Finish the spell name at 8.57s, close the mouth and hold the seal until 12s; release only in the following shot.'
    dirs['batches']['GB022-1']['shots']['CY024A5']['effects_zh_override']=sm['CY024A5']['sound']
    dirs['batches']['GB022-1']['shots']['CY024A5']['effects_en']='Prayer 0–5.74s; vocal and music gap 5.74–6.54s; complete new spell name 6.54–8.57s; closed mouth and held seal 8.57–12s. No attack or shield impact.'
    sound['CY024A5']['effects']=sm['CY024A5']['sound']
    dirs['batches']['GB033']['shots']['CY034']['effects_zh_override']=sm['CY034']['sound']
    fan='0.1秒扇轴短咔；0.2–0.9秒扇骨依次展开；1.15秒单叶卡扣响；1.35秒弹脱破空。声音轻脆，避让跨镜咏唱，下一镜接同一扇叶飞行。'
    sound['CY024A10']['effects']=fan
    dirs['batches']['GB019']['shots']['CY024A10'].update(effects_zh_override=fan,effects_en='Fan axle at 0.1s, unfolding 0.2–0.9s, leaf latch 1.15s, release 1.35s. Next shot continues the same leaf flight; keep chant audible.')
    plan['execution_notes']['CY029']='本镜4秒＋下一镜CY029E两秒＝完整6秒停顿；父亲4.18秒原声从本镜0.3秒开始、跨至下一镜0.48秒结束；Claude在6秒满后才续咏。'
    plan['execution_notes']['CY029E3']='保留3秒手部凝种镜；同一句后段在本镜1.33秒已画外进入，下一镜小鱼反应继续承接，不能重复起句。'
    for sid in ['CY024A7','CY024A5A','CY024A5','CY024A5B','CY024B']:
        rv=next(d['shots'][sid] for d in dirs['batches'].values() if sid in d['shots'])
        rv['action_zh_override']=rv.get('action_zh_override',sm[sid]['action'])+' 水龙眼窝为流体折射暗部，无实体眼球、虹膜、瞳孔或固定亮点。'
        rv['action_en']+=' Water-dragon eyes are dark fluid refraction, without solid eyeballs, iris, pupils or fixed glints.'
    cast['shots']['CY008M']=dict(visible=['恶魔GPT','天使GPT','定格GPT底板'],offscreen=['DeepSeek'],reflection=[],note='成人本体已烘焙在冻结底板中，只复用像素、不重生成人身份；两只分身按各自四视图独立表演。',basis='作者采用内心戏及实际录音')
    for who,asset,name in [('恶魔GPT','CHAR-GPT-DEVIL-CHIBI','Devil GPT'),('天使GPT','CHAR-GPT-ANGEL-CHIBI','Angel GPT')]:
        cast['identities'][who]=dict(aliases=[],anchor='已采用v003分身四视图，比例配色保持',master_asset_id=asset)
        plan['identity_inputs'][who]=dict(name_en=name,asset_id=asset,kind='four_view')
    cast['identities']['定格GPT底板']=dict(aliases=[],anchor='同一已冻结王座底图中的成人GPT，不参与生成表演')
    plan['identity_inputs']['定格GPT底板']=dict(name_en='frozen adult GPT plate',asset_id=None,kind='background')
    plan['identity_inputs']['教主']=dict(name_en='the High Priest',asset_id='CHAR-PRIEST',kind='four_view')
    assets=load('资产/assets.json');a=next(a for a in assets['assets'] if a['id']=='CHAR-PRIEST')
    if a['path']!='资产/图像/四视图/CHAR-PRIEST-TURN-v001.png':a.setdefault('previous_versions',[]).append(dict(path=a['path'],status=a['status'],role='历史概念立绘，保留溯源'))
    a.update(path='资产/图像/四视图/CHAR-PRIEST-TURN-v001.png',status='生成前修正候选，待作者审阅',limits='四幅全身正、朝左、背、朝右；侧背结构为基于原立绘的合理补全，待作者确认。',generation_record='镜头设计/生成记录/生成前修正-v059/请求.json')
    a['version']='v001四视图修正候选'
    for path,role in [('资产/图像/CHAR-PRIEST-v001.png','原概念立绘，保留设计溯源'),('资产/图像/四视图/CHAR-PRIEST-TURN-v001-views-r2/01_front-full.png','修正候选：正面全身'),('资产/图像/四视图/CHAR-PRIEST-TURN-v001-views-r2/02_facing-left.png','修正候选：朝画面左侧全身'),('资产/图像/四视图/CHAR-PRIEST-TURN-v001-views-r2/03_back.png','修正候选：正背全身'),('资产/图像/四视图/CHAR-PRIEST-TURN-v001-views-r2/04_facing-right.png','修正候选：朝画面右侧全身')]:
        if not any(x['path']==path for x in a.setdefault('related',[])):a['related'].append(dict(path=path,role=role))
    write('资产/assets.json',assets)
    # Freeze the same candidate asset manifest for this board, without claiming author adoption.
    write(OUT+'资产输入快照.json',assets);plan['assets']=OUT+'资产输入快照.json'
    sound['CY008M']=dict(effects=s['sound'],action_override=s['action'])
    for ic in inner['cues']:loc['translations'][ic['source_text']]=ic['ja_draft']
    loc['delivery_csv_sha256']=sha('后期/日语配音交接-v001/台词与回交表.csv')
    for d in [dirs,cast,loc,rhythm]:d['source_sha256']=h
    cast.update(source=SOURCE,scope='133镜人物核对，补教主四视图和已采用分身身份；修正图待作者审阅')
    write(OUT+'日语译配.json',loc)
    newam={};tc={c['id']:c for c in timing['cues']}
    reviewmap={(c['batch_id'],c['cue_index']):c for c in audit['cues']}
    for a in aud['cues']:
        c=tc[a['cue_id']];review=reviewmap[(a['batch_id'],a['cue_index'])];bs=next(sm[b['shot_ids'][0]]['start_second'] for b in plan['batches'] if b['id']==a['batch_id'])
        a.update(text=c['text_ja'],timeline_start=c['timeline_start'],timeline_end=c['timeline_end'],budget_seconds=round(c['timeline_end']-c['timeline_start'],6),mix_source=c['mix_source'])
        review.update(start=round(c['timeline_start']-bs,6),end=round(c['timeline_end']-bs,6),duration=a['budget_seconds'],film_start=c['timeline_start'],film_end=c['timeline_end'],current_text=c['text_ja'])
        if c['id']=='VO-CY009-01':review.update(offscreen=False,offscreen_entry=True,notes=['仅起声画外打断，随即切回小鱼本人对嘴说完，不重说。'])
        if c['id']=='VO-CY024A5-02':
            a.update(master=None,mix_source='dry_file',file_seconds=2.03,note='作者新版术名完整2.03秒原速；旧母版尾段不混入。',sha256=c['sha256']);review.update(source_text='沧龙出海！',notes=[a['note']])
    for ci,ic in enumerate(inner['cues']):
        c=tc[ic['id']];a=dict(cue_id=c['id'],batch_id='GB004M',cue_index=ci,shot_id='CY008M',speaker=ic['speaker'],text=c['text_ja'],path=c['file'],sha256=c['sha256'],file_seconds=c['file_out'],speech_start=0,speech_end=c['file_out'],speech_seconds=c['file_out'],budget_seconds=c['file_out'],state='natural_speed_timed_pending_listening',note='完整新配音原速；无需加速或截字，待听审。',master=None,delivery_status='recorded',transcript_verified=False,timeline_start=c['timeline_start'],timeline_end=c['timeline_end'],visual_shots=['CY008M'],mix_source='dry_file')
        aud['cues'].append(a)
        audit['cues'].append(dict(batch_id='GB004M',cue_index=ci,shot_id='CY008M',speaker=ic['speaker'],listener='另一分身与GPT本体',source_text=ic['source_text'],current_text=ic['ja_draft'],language='Japanese',intention=ic['delivery'],delivery=ic['delivery'],start=c['shot_relative_start'],end=c['shot_relative_end'],duration=c['file_out'],film_start=c['timeline_start'],film_end=c['timeline_end'],offscreen=False,notes=[a['note']],issue_ids=[]))
    aud['cues'].sort(key=lambda c:c['timeline_start']);audit['cues'].sort(key=lambda c:c['film_start'])
    audit.update(version='v014',source=SOURCE,source_sha256=h,localization_sha256=sha(OUT+'日语译配.json'),summary='63句原速对位；已并入内心戏和新术名；文件与时间验证不代表听审。')
    audit['batches'].insert(4,dict(batch_id='GB004M',title=ib['title'],context=s['purpose'],has_dialogue=True,cue_count=2))
    audit['counts'].update(batches=41,dialogue_cues=63,unique_source_texts=len({c['source_text'] for c in audit['cues']}),speaking_roles=len({c['speaker'] for c in audit['cues']}))
    rhythm['batches']['GB004M']=dict(status='actual_edit_candidate_pending_listening',note='同一王宫曲连续，整段内心戏压低7dB，句间不弹回。',points=[])
    for v in rhythm['batches'].values():
        for p in v['points']:
            if p.get('film_time',0)>=53:p['film_time']=round(p['film_time']+13.5,6)
    for file,d in [('人物核对.json',cast),('声音核对.json',sound),('动态审查.json',dirs),('对白复核.json',audit),('日语音频映射.json',aud),('配乐卡点方案.json',rhythm)]:write(OUT+file,d)
    plan.update(version='v014',source=SOURCE,output=OUT.rstrip('/'),cast_review=OUT+'人物核对.json',sound_review=OUT+'声音核对.json',direction_reviews=[OUT+'动态审查.json'],dialogue_review=OUT+'对白复核.json',pilot_batch=None)
    plan['navigation'].update(previs=FIX+'全片声音预览.html',review=FIX+'修正交接.html')
    plan['audio_execution'].update(localization=OUT+'日语译配.json',rhythm=OUT+'配乐卡点方案.json',display_note='63句自然原速对位；只上传图片，声音后期替换；修正候选待作者视听审阅。',replacement_note='41条独立干声（含新增2句）与保留的连续母版，加独立新版术名；母版旧术名尾段退役，参考切片不叠加。')
    plan['speech_modes'].pop('CY009',None)
    plan['shot_notes']['CY020B']='当前修正候选已统一为短柄黑铁笼式仪式火把，点火近景为道具母版；后续不变成长权杖。'
    plan['shot_notes']['CY024A0']='当前修正候选为左臂抱小鱼、右手持扇；后续镜头保持同一手位，不整体镜像。'
    plan.get('action_overrides',{}).pop('CY009',None);plan.get('action_overrides',{}).pop('CY024A5',None)
    plan['model_contracts']['minimax-h3']['max_chars']=2000
    plan['model_contracts']['verified']='2026-10-26 LibTV实时接口，证据：后期/生成准入审查-20261026/实时模型接口.json；H3 2000字符/9图，Seedance 30图。'
    plan['mix_notes']=['七首采用曲保持；13.5秒内心戏并入原曲，后续时码整体顺延。','63句原速，48个实际混音事件；旧术名不再使用，连续母版切片不叠加。','音效与动态口型需视频后验证。']
    plan['global_gaps']=['新修正画面和教主四视图已接入候选输入，待作者审阅。','逐字发音、表演与音乐乐句待作者试听；动态口型和背景冻结效果需视频验证。','环境与拟音已有要求，尚无独立成品；声音预览只含对白及BGM。']
    plan['reference_reductions']=[dict(batch='GB004M',removed=states[1]['path'],reason='中间反驳状态留在预览；身份、起点、终点足够，动作由明确时码描述。'),dict(batch='GB019',removed_shot='CY024A2',reuse_shot='CY024A1',reason='擦汗动作接同组罩内双人构图，不再重复上传单独构图，原图保留预览。')]
    write(OUT+'批次计划.json',plan);write(FIX+'输入来源.json',baseline_hashes)
    print('Prepared v014: 133 shots, 63 cues, 41 batches, 464.4 seconds')

if __name__=='__main__':main()
