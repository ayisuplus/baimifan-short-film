"""Apply the approved repair scope; preserve originals and stable dialogue IDs."""
import copy, hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'视频制作/生成板-v012'
FIX=ROOT/'后期/收尾修复-v001'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def write(p,d):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    OUT.mkdir(exist_ok=True)
    timing=load('后期/收尾修复-v001/配音对位方案.json')
    old=load('视频制作/生成板-v011/展开数据.json')
    plan=load('视频制作/生成板-v011/批次计划.json')
    source=load(plan['source']);assert sha(plan['source'])==timing['source_sha256']
    oldsm={s['id']:copy.deepcopy(s) for s in source['shots']}
    sm={s['id']:s for s in source['shots']};tm={s['shot_id']:s for s in timing['shots']}
    oldpairs=[(b,c) for b in old['batches'] for c in b['dialogue']]
    oldaudio=load('视频制作/生成板-v011/日语音频映射.json')
    oldaudit=load('视频制作/生成板-v011/对白复核.json')
    assert len(oldpairs)==len(timing['cues'])==61
    cmap={c['id']:c for c in timing['cues']}
    ordered=[cmap[a['cue_id']] for a in oldaudio['cues']]
    updates=load('后期/收尾修复-v001/镜头动态修正.json') if (FIX/'镜头动态修正.json').exists() else {'shots':{}}
    plan.setdefault('shot_notes',{}).update(updates.get('plan_note_replacements',{}).get('shot_notes',{}))
    for s in source['shots']:
        t=tm[s['id']];s.update(seconds=t['new_seconds'],start_second=t['new_start'],end_second=t['new_end'],subtitle_cues=[])
        s['dialogue_cues']=[]
        s['timing_revision']={'previous_seconds':t['old_seconds'],'direction':t['direction'],'audio_rate':1}
        s.update(updates['shots'].get(s['id'],{}).get('source_overrides',{}))
    for (_,oldcue),c in zip(oldpairs,ordered):
        sid=c['shot_id'];cue=dict(speaker=oldcue['speaker'],text=oldcue['source_text'],offset=c['shot_relative_start'],duration=round(c['timeline_end']-c['timeline_start'],6),cue_id=c['id'],cross_shot_offscreen=c['cross_shot_offscreen'],visual_shots=c['visual_shots'])
        sm[sid]['subtitle_cues'].append(cue)
    bridge=source['music_direction']['incantation_bridge']
    bridge['seconds']=cmap['VO-CY024A9-01']['file_out']
    bridge['rule']='自然速度连续母版跨五镜，只说一次；各镜重新分配画面时长，不重起、不加速。'
    source.update(version='v0.57',revision='v057',total_seconds=timing['new_duration'],previous_source=plan['source'],audio_repair_plan='后期/收尾修复-v001/配音对位方案.json')
    source['subtitle']='132镜 · 450.9秒 · 日语原声自然速度对位与实际配乐剪辑'
    source['previous_revision_notes']=source.get('revision_notes',{})
    source['revision_notes']={'previous_manifest':plan['source'],'boundary':'保留132镜顺序、采用图片、中文原意及日语回交原词；按原速音频重排至450.9秒，七首采用曲不变。'}
    source.update(roughcut_preview='后期/收尾修复-v001/全片声音预览.html',roughcut_preview_label='日语原声与实际BGM静帧预览',review_intro='61句日语完整原速对位，画面与音乐按实际时间连看。',review_focus='发音与表演、音乐乐句、保留四秒显形/六秒打断；环境与拟音另验。')
    for scene in source['scenes']:scene['seconds']=round(sum(sm[i]['seconds'] for i in scene['shot_ids']),6)
    for s in source['shots']:
        s['sound']=s['sound'].replace(' 新配音未制作；字幕仅为阅读暂排，实际说话与动作节奏待声音预演。',' 日语原声已回交，按自然速度时间对位。')
    sm['CY028A2']['sound']='本镜前2秒GPT在画外完整回答，宝宝无词反应，不跟随对嘴；滴水与安静呼吸，保持祭坛方向与距离感，不新增台词。'
    sm['CY028A2']['dialogue']='ChatGPT（画外）：她没事，在下面等你。'
    sm['CY034']['sound']='尾乐在本镜前3秒内收尽；最后4秒（成片446.9–450.9秒）BGM静音，只留街市声与两人呼吸。'
    md=source['music_direction'];md.update(status='audio_timing_rendered_pending_listening',voice_timing='full_master_natural_speed',estimated_spell_sequence_seconds=round(sum(sm[i]['seconds'] for i in md['sequence']),6),estimated_gpt_incantation_seconds=53.0,pre_release_sequence_seconds=round(sm['CY024A5B']['start_second']-sm['CY024A0']['start_second'],6))
    md['rule']=md['rule'].replace('正式配音、音效和乐句混合待制作。','原速日语配音与BGM已做实际预览；音效待制作，乐句听感待听审。')
    star=source['star_incantation'];star.update(seconds=round(sum(sm[i]['seconds'] for i in star['sequence']),6),sequence_elapsed_seconds=28.91,status='原全文日语母版完整对位，六秒父亲停顿保留；待听审',music='父亲呼唤与六秒停顿停乐；继续咏唱时返乐。完整术名后，下一镜才送出火种。')
    write('镜头设计/shot-plan-v0.57.json',source)
    sourcepath='镜头设计/shot-plan-v0.57.json';sourcehash=sha(sourcepath)

    # Cross-shot voices and the continuous invocation are indivisible generation units.
    joined=set()
    ids=list(sm)
    for c in ordered:
        positions=[ids.index(s) for s in c['visual_shots']]
        for i in range(min(positions),max(positions)):joined.add((ids[i],ids[i+1]))
    dirs={}
    for p in plan['direction_reviews']:dirs.update(load(p)['batches'])
    newb=[];newdirs={};parent={}
    for b in plan['batches']:
        units=[]
        for sid in b['shot_ids']:
            if units and (units[-1][-1],sid) in joined:units[-1].append(sid)
            else:units.append([sid])
        groups=[];group=[];duration=0
        for unit in units:
            length=sum(sm[i]['seconds'] for i in unit);assert length<=15+1e-8,(b['id'],unit,length)
            if group and duration+length>15+1e-8:groups.append(group);group=[];duration=0
            group+=unit;duration+=length
        if group:groups.append(group)
        for index,group in enumerate(groups):
            nb=copy.deepcopy(b);bid=b['id'] if len(groups)==1 else b['id']+'-'+str(index+1)
            nb.update(id=bid,shot_ids=group,parent_batch=b['id'],status='timing_repaired_not_submitted')
            if len(groups)>1:nb.update(title='、'.join(sm[s]['title'] for s in group),group_reason='以完整对白和连续动作为最小单元，按自然原声重新合批。',handle_reason='15秒内保留原速对白，剩余尾部供剪辑去除。')
            nd=copy.deepcopy(dirs[b['id']]);nd['shots']={s:nd['shots'][s] for s in group}
            if len(groups)>1:
                nd.update(arc_zh='；'.join(sm[s]['title'] for s in group),arc_en='Continue the actions below in their listed order, without restarting ongoing motion or speech.',entry_bridge_zh=nd['shots'][group[0]]['transition_zh'],exit_bridge_zh=sm[group[-1]]['exit_state'])
            for sid in group:
                u=updates['shots'].get(sid,{})
                nd['shots'][sid].update(u.get('direction_override',{}))
                if u.get('source_overrides',{}).get('sound'):nd['shots'][sid]['effects_zh_override']=u['source_overrides']['sound']
                if sid in ('CY028A2','CY028','CY034'):nd['shots'][sid]['effects_zh_override']=sm[sid]['sound']
                if sid=='CY028A2':nd['shots'][sid].update(transition_zh='沿Claude俯视方向切小鱼，在本镜前2秒听GPT画外完整回答；宝宝无词反应不对嘴，保持祭坛方向。',transition_en="Follow Claude's downward eyeline to the child's silent response. GPT delivers the full offscreen answer during this shot's first two seconds; the child does not mouth it.")
                if u.get('execution_note'):plan.setdefault('execution_notes',{})[sid]=u['execution_note']
                if u.get('action_override'):plan.setdefault('action_overrides',{})[sid]=u['action_override']
            newb.append(nb);newdirs[bid]=nd;parent[bid]=b['id']
    byshot={sid:b for b in newb for sid in b['shot_ids']}
    for c in ordered:assert len({byshot[s]['id'] for s in c['visual_shots']})==1,('Cross-batch speech',c['id'])
    for b in newb:
        b['group_reason']='完整对白和动作保持连续；按当前自然原声时长合批。'
        b['handle_reason']='生成15秒；超过本批有效内容的尾部只保持终态，后期剪除。'
    write(OUT/'动态审查.json',{'source_sha256':sourcehash,'batches':newdirs})
    cast=load(plan['cast_review']);cast['source_sha256']=sourcehash;write(OUT/'人物核对.json',cast)
    sound=load(plan['sound_review']);write(OUT/'声音核对.json',sound)
    loc=load(plan['audio_execution']['localization']);loc.update(source_sha256=sourcehash,status='returned_japanese_natural_speed_timed_pending_listening',timing_reviews={},note='回交日语原词原速对位；逐字发音、表演与成片口型仍待听审。')
    write(OUT/'日语译配.json',loc)
    audit=copy.deepcopy(oldaudit);audit.update(source=sourcepath,source_sha256=sourcehash,version='v012',migration='natural_speed_retime',status='natural_speed_timing_applied_pending_listening',localization_sha256=sha(OUT/'日语译配.json'),summary='61条日语原声原词原速完整对位；跨镜母版连续，实际BGM剪辑另附。听审与动态口型未验收。',cues=[],batches=[],batch_notes={},issues=[])
    audio=copy.deepcopy(oldaudio);audio['cues']=[];counter={b['id']:0 for b in newb}
    for (_,oc),c,a,review in zip(oldpairs,ordered,oldaudio['cues'],oldaudit['cues']):
        bid=byshot[c['shot_id']]['id'];ci=counter[bid];counter[bid]+=1
        b=byshot[c['shot_id']];start=sm[b['shot_ids'][0]]['start_second']
        note='完整原声自然速度；连续母版只混入一次。' if c['mix_source']=='master_reference_only' else '完整干声自然速度；保留原始词首、词尾及余白。'
        if c['cross_shot_offscreen']:note+=' 跨镜连续，画内其他人物不得代说。'
        a.update(batch_id=bid,cue_index=ci,budget_seconds=round(c['timeline_end']-c['timeline_start'],6),state='natural_speed_timed_pending_listening',note=note,timeline_start=c['timeline_start'],timeline_end=c['timeline_end'],visual_shots=c['visual_shots'],mix_source=c['mix_source'])
        audio['cues'].append(a)
        review.update(batch_id=bid,cue_index=ci,start=round(c['timeline_start']-start,6),end=round(c['timeline_end']-start,6),duration=round(c['timeline_end']-c['timeline_start'],6),film_start=c['timeline_start'],film_end=c['timeline_end'],offscreen=review['offscreen'] or c['cross_shot_offscreen'],notes=[note],issue_ids=[])
        audit['cues'].append(review)
    for b in newb:audit['batches'].append(dict(batch_id=b['id'],title=b['title'],context=newdirs[b['id']]['arc_zh'],has_dialogue=bool(counter[b['id']]),cue_count=counter[b['id']]))
    audit['counts']['batches']=len(newb)
    write(OUT/'对白复核.json',audit);write(OUT/'日语音频映射.json',audio)
    # Keep action anchors stable; real source timings are filled from the rendered edit.
    rhythm=load(plan['audio_execution']['rhythm']);oldb={b['id']:b for b in old['batches']}
    nr={'source_sha256':sourcehash,'status':'actual_edit_candidate_pending_listening','method':'稳定镜号动作锚对位；原曲时码来自实际BGM剪辑，不把所有动作点称为重拍。','batches':{b['id']:{'status':'actual_edit_candidate_pending_listening','note':'动作点与实际配乐剪辑关联；停乐处用拟音，不生成BGM。','points':[]} for b in newb}}
    for bid,br in rhythm['batches'].items():
        for p in br['points']:
            t=oldb[bid]['film_start']+p['time']
            s=next(s for s in oldsm.values() if s['start_second']<=t<s['end_second'])
            sid=s['id'];nt=sm[sid]['start_second']+(t-s['start_second'])*sm[sid]['seconds']/s['seconds']
            # Prayer gap and spell entry follow audio, not proportional visual scaling.
            if sid=='CY024A5' and abs(t-s['start_second']-5)<.01:nt=cmap['VO-CY024A5-01']['timeline_end']
            if sid=='CY024A5' and abs(t-s['start_second']-5.8)<.01:nt=cmap['VO-CY024A5-02']['timeline_start']
            nb=byshot[sid];q=copy.deepcopy(p);q.update(time=round(nt-sm[nb['shot_ids'][0]]['start_second'],6),anchor_shot=sid,source_seconds=None)
            nr['batches'][nb['id']]['points'].append(q)
    write(OUT/'配乐卡点方案.json',nr)
    plan.update(version='v012',source=sourcepath,output='视频制作/生成板-v012',batches=newb,cast_review='视频制作/生成板-v012/人物核对.json',sound_review='视频制作/生成板-v012/声音核对.json',direction_reviews=['视频制作/生成板-v012/动态审查.json'],dialogue_review='视频制作/生成板-v012/对白复核.json',pilot_batch=None)
    plan['navigation'].update(previs='后期/收尾修复-v001/全片声音预览.html',review='后期/收尾修复-v001/修复交接.md')
    plan['audio_execution'].update(localization='视频制作/生成板-v012/日语译配.json',rhythm='视频制作/生成板-v012/配乐卡点方案.json',display_note='61条日语原声已按自然速度完整对位。仅上传图片，不上传配音或BGM；实际声音预览可连看。逐字听审、口型与教主四视图仍需验收。',replacement_note='后期按实际配音对位方案使用39条独立干声与3条连续母版，不重复叠加22条参考切片；不加速不截字。动态口型仍须逐镜检查。')
    plan['sound_policy']='有词对白全部使用指定日语，只说一次。画外与跨镜咏唱保持连续，在画人物不代说。只上传图片；不上传配音或BGM，不生成BGM。对白窗口以本批新时间为准，后期按自然原速母版替换并检查口型。'
    plan['mix_notes']=['七首采用曲不变；原曲剪入剪出、淡变和留白见实际BGM剪辑。','配音使用46个实际混入事件；61条逐句参考不重复叠加。','无词吟唱、示警、喘息、接触声与环境底按逐镜声音要求生成或后期补齐，预览未伪造完成。']
    plan['global_gaps']=['教主缺合格四视图，不以现有概念立绘冒充身份参考。','逐字发音、表演与动态口型待听审；文件完整和时间对位不等于听审通过。','无词声音与拟音尚无独立完成证据，预览只包含回交对白及配乐。']
    write(OUT/'批次计划.json',plan)
    print(json.dumps({'source':sourcepath,'seconds':source['total_seconds'],'batches':len(newb),'cues':len(audio['cues'])},ensure_ascii=False))

if __name__=='__main__':main()
