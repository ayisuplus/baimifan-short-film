"""Author-requested pictures and altar continuity; preserves v0.6 and all source images."""
import copy, json, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
raise SystemExit('此为旧护罩+喷射水流方案的构建草稿，作者已转向天瀑；更新镜头方案后再执行，不得直接发布。')
target=ROOT/'镜头设计/shot-plan-v0.7.json'
assert not target.exists(), 'Inspect existing v0.7 instead of overwriting'
old=json.loads((ROOT/'镜头设计/shot-plan-v0.6.json').read_text(encoding='utf-8'))
d=copy.deepcopy(old)
script=(ROOT/old['story_script']).read_text(encoding='utf-8')
script=script.replace('版本：v0.6｜2026-10-21｜空间复核：固定道具与高台，补足赶路、拉拽、落地、进殿与解锁过程。','版本：v0.7｜2026-10-21｜画面修订：驱逐、远景、纵深群像、眼中倒影、赤足三阶祭坛、护罩与水灭火。')
q_drive='一名教徒横身挡住小鱼，张开手臂将她赶到路边。小鱼抱紧饭碗，退了一步；Claude 被挡在教徒身后，回头望来。'
q_feet='Claude 赤足站在十字架竖柱固定的小木脚托上，脚踝各有锁链连向竖柱；脚托下方两侧只放低矮柴堆，裙摆与脚趾没有埋进木柴。'
q_ward='Perplexity 举杖，一层蓝色保护罩包住 Claude 的全身与脚托，火焰留在罩外。'
q_water='ChatGPT 伸手施展水魔法，水流落在燃烧的柴堆上，火光退成蒸汽；千问抱起小鱼，带她退到 ChatGPT 身侧。'
q_dry='柴堆已经熄灭，只剩湿黑木头和余汽。保护罩仍在，Claude 仍被锁在木架上；千问抱稳小鱼，ChatGPT 收住水流。'
q_ankles='战斗已经结束。Perplexity 先打开 Claude 两只脚踝的锁扣，移开踝链；她的赤足仍踩在固定脚托上，腕部束具暂未完全解除。'
q_eye='她疲倦的蓝眼睛里倒映着 ChatGPT 的白色龙角和身影，门外冷光勾出轮廓。'
replacements={
 '一名教徒横身挡住她，队伍继续前行。Claude 回头望来，随即再次被黑袍遮住。':q_drive+'队伍继续前行，Claude 随即再次被黑袍遮住。',
 '她转过身，小小的脚步声穿过整座大殿，最后消失在门外。':'她转过身，小小的脚步声穿过整座大殿。大侧远景里，她走向画面右侧远处的出口，只剩一个蓝色小点。',
 '铁钉将腕部束具钉入木架，锁链横过身体；白裙垂在下方堆起的干柴上。':'铁钉将腕部束具钉入木架，腰前只有一道横链。'+q_feet,
 '小鱼沿左侧长椅旁的阴影走到祭坛，从侧面的台阶爬上去。她站稳在木架左侧的窄阶边，双脚有支点，才能够到 Claude 腰前的锁。':'小鱼沿左侧长椅旁的阴影走到祭坛，爬完三级宽石阶，站到木架左侧的平整平台上。她踮起脚、伸长双臂够向 Claude 腰前的锁。',
 'DeepSeek 换了一个站位，抵住台阶，又试了一次。':'DeepSeek 换了一个站位，双脚踩稳平台，又试了一次。',
 '一道屏障隔开柴薪与 Claude，火焰随之被压灭。':q_ward+'\n\n'+q_water+'\n\n'+q_dry,
 '她疲倦的蓝眼睛里映入一道门外的冷光。':q_eye,
 'ChatGPT 登上祭坛，先托稳 Claude。Perplexity 上前解除腕部束具和腰前的锁链，直到最后一个承重点松开。':q_ankles+'\n\nChatGPT 登上祭坛，扶住 Claude。Perplexity 随后解除腰链和腕部束具，直到最后一个腕扣松开。',
 }
for a,b in replacements.items():
    assert a in script,a
    script=script.replace(a,b)
script=script.replace('柴薪还没有点燃。','柴薪还没有点燃。祭坛从大殿地面到顶端平台只有三级宽石阶，平台四周同高，不再另设侧梯或后梯。')
script=script.replace('镜头拉开，九位援军在她身后错落显露：','镜头拉开，ChatGPT 在队首，持武器、色彩鲜明的同伴靠前，其余同伴在第二层，九位援军在她身后错落显露：')
script=script.replace('Claude 仍被固定在木架上，锁链没有松开。千问赶到台阶边，蹲下将无力的小鱼抱进怀里；其他人挡住靠近的黑袍。','其他人挡住靠近的黑袍。')
script=script.replace('火把落下。','教主把第二支火把探向低柴堆，将木柴引燃后收回，仍握在手中。')
script+='\n- v0.7：教堂受缚与解救阶段 Claude 赤足。祭坛三级宽石阶接单一平整平台，固定脚托与低柴堆，不增加侧阶；先护罩、后水灭火，战斗结束后解踝链、腰链及腕扣再接稳落地。鞋版和多阶旧图留作历史。新增画面尚待作者审阅，本版不重导旧配乐粗剪。\n'
shots={s['id']:s for s in d['shots']}; after={}; added=[]; layouts={}
def picture(id,name,cell=0,cols=1,rows=1,visible='',**extra):
    path='镜头设计/图像/'+name
    assert (ROOT/path).exists(),path
    s=shots[id];s['panel_index']=cell
    s['presentation']=dict(path=path,role='action',visible=visible,missing='静帧代表动作状态；连续施法、解锁与落脚仍需动态验证。',status='v0.7画面修订候选，待作者审阅',show_as_main=True)
    s['refs']=[dict(path=path,role='本镜修订源图'),*[r for r in s['refs'] if not r['path'].startswith('镜头设计/图像/')]]
    for k in ['page_size','panel_rect_pixels','panel_region','display_crop_normalized']:s.pop(k,None)
    layouts[path]=dict(path=path,cols=cols,rows=rows,**extra)
def add(id,anchor,seconds,title,quote):
    s=copy.deepcopy(shots[anchor]);shots[id]=s
    for k in ['time_caption','split_screen_reveal']:s.pop(k,None)
    s.update(id=id,seconds=seconds,title=title,purpose=title,action=quote,source_quote=quote,dialogue='无对白',dialogue_cues=[],framing='细节近景',entry_state=quote,exit_state=quote,invariants=['保留角色母本、道具与相邻镜空间关系。'])
    after.setdefault(anchor,[]).append(id);added.append(id)
    return s
add('CY003C','CY003B',2,'被教徒驱逐',q_drive).update(framing='中景／黑袍阻隔',entry_state='小鱼刚递出饭碗。',exit_state='小鱼被迫退开，仍持碗跟向教堂。')
picture('CY003C','CY003C-教徒驱逐-v001.png',visible='黑袍横身张臂驱逐抱碗的小鱼，Claude在后方回望。')
picture('CY010','CY010-宫殿大侧远景-v001.png',visible='GPT在画面左侧座位旁站起，小鱼是右侧远处出口前的蓝色小点。')
shots['CY010'].update(title='隔着整座宫殿',framing='大侧远景／长轴纵深',action='钟响，GPT在左侧座位旁站起，望向走到右侧远处门口的小鱼。',entry_state='小鱼离开，GPT仍在原座位旁。',exit_state='GPT站在后方，小鱼越过出口。')
picture('CY012','CY012-空堂三阶-v002.png',visible='前景宝宝刚入堂，远处Claude独留三级祭坛。')
picture('CY013','CY013-祭坛空间母版-v002.png',visible='三级石阶接平平台；赤足、固定脚托、踝链、低柴堆及阶下右盆可见。')
shots['CY013'].update(source_quote=q_feet,action='祭坛全景交代Claude受缚和固定空间。',entry_state='空堂只有Claude受缚。',exit_state='确认只有三级阶，脚托与低柴相互分开。')
add('CY013A','CY013',2,'赤足、脚托与踝链',q_feet)
feet='脚部与营救-四格-v003.png'
picture('CY013A',feet,2,2,2,'赤足踩固定脚托，踝链连着竖柱，低柴在下方两侧。')
picture('CY015',feet,0,2,2,'小鱼踩稳平台踮脚够锁，Claude赤足受缚，身体修长。')
shots['CY015'].update(action='小鱼抬头向Claude保证，踮脚伸手够腰锁。',entry_state='小鱼已爬完三级石阶来到平平台。',exit_state='宝宝双手够住腰锁，准备尝试打开。')
picture('CY016A',feet,1,2,2,'宝宝在平平台垂头喘息，Claude赤足与踝链仍在。')
for id,cell in [('CY016D',0),('CY020A',1),('CY022A',2)]:
    picture(id,'空间修订C-三阶-v004.png',cell,2,2,shots[id]['presentation']['visible']+'；后景统一三级祭坛与赤足脚托。')
for id,cell in [('CY017',0),('CY018',1),('CY019',2),('CY021',4)]:
    picture(id,'S04-三阶祭坛-v004.png',cell,2,3,shots[id]['presentation']['visible']+'；祭坛阶面按三级修订。')
picture('CY021A','CY021A-低柴火把交接-v002.png',visible='教主接第二支燃烧火把，第一支湿火把在阶下右盆；后方赤足Claude与低柴。')
picture('CY024','CY024-援军纵深队形-v001.png',visible='GPT最前，武器与鲜明服装靠前，其他同伴在后排错落显露，十位入场者有前后层次。')
shots['CY024'].update(action='GPT领队入场，持武器与色彩鲜明的同伴在前层，其余在第二层，九位援军错落跟进。')
fire='火焰护罩水魔法-四格-v003.png'
picture('CY022',fire,0,2,2,'低柴燃起，宝宝在阶下倒地，Claude赤足踩脚托；祭坛三级。')
shots['CY022']['action']='教主将第二支火把探向低柴点燃，再收回手中；宝宝倒在阶下，Claude仍受缚。'
picture('CY024A',fire,1,2,2,'Perplexity右侧举杖，罩住Claude全身与脚托；GPT左侧入场，千问来到宝宝身边。')
shots['CY024A'].update(title='先护住Claude',framing='全景／祭坛正面',action=q_ward,source_quote=q_ward,entry_state='援军已到祭坛前，柴堆仍燃烧。',exit_state='Claude处于保护罩内，尚未灭火、解锁。',invariants=['GPT在画面左侧，Perplexity右侧；千问靠近宝宝。','保护罩包住Claude及脚托，火焰在罩外。'])
add('CY024B','CY024A',3,'水魔法灭火',q_water).update(framing='全景／动作关系',entry_state='保护罩已形成，柴堆仍燃烧。',exit_state='水扑灭柴火；千问抱起小鱼，向GPT身侧退开。')
picture('CY024B',fire,2,2,2,'GPT的水弧打在木柴上，火光退成蒸汽；千问抱住宝宝，Perplexity维持罩。')
picture('CY027',fire,3,2,2,'柴堆湿黑没有明火；保护罩完整，千问在GPT身侧抱宝宝。')
shots['CY027'].update(title='火已熄灭，护罩仍在',source_quote=q_dry,action=q_dry,entry_state='水魔法刚完成，千问抱着小鱼退到GPT身侧。',exit_state='小鱼在千问怀里抬眼，Claude仍受缚。')
picture('CY025','CY025-眼中GPT-v001.png',visible='疲倦含泪的蓝眼睛内倒映白发龙角GPT。')
shots['CY025'].update(source_quote=q_eye,action=q_eye)
for id,cell in [('CY027A',0),('CY027D',3)]:
    picture(id,'S05E-三阶祭坛-v006.png',cell,2,3,shots[id]['presentation']['visible']+'；后方祭坛统一三级及赤足脚托。')
add('CY027F1','CY027F',2,'先解除踝链',q_ankles).update(entry_state='敌方倒地，Claude仍被束缚。',exit_state='踝链已打开，双脚仍踩脚托；腰链和最后腕扣随后处理。')
picture('CY027F1',feet,3,2,2,'Perplexity解踝扣，赤足仍踩固定脚托，下方木柴已湿黑熄灭。')
for id,cell in [('CY027G',0),('CY028A',1)]:
    picture(id,'空间修订F-赤足站稳-v004.png',cell,1,2,'最后腕扣解开前先扶稳。' if cell==0 else 'Claude在左赤足踩稳同一平台，GPT在右穿原鞋扶住她，脚托留在左后木柱。',max_panel_aspect=4.0)
    shots[id]['display_crop_normalized']=[.14,0,.57,1]
shots['CY027G']['entry_state']='踝链已经打开，GPT扶稳Claude；Perplexity解除腰链和最后腕扣。'
sequence=[]
def append(id):
    sequence.append(shots[id])
    for new in after.get(id,[]):append(new)
for s in old['shots']:append(s['id'])
geometry='祭坛只有三级宽石阶接一个平平台；无旁侧加阶。Claude受缚时赤足踩固定脚托，踝链连竖柱，低柴在下方两侧，水盆在阶下右侧。'
t=0
for i,s in enumerate(sequence):
    # Remove obsolete side-step staging from current descriptions, never from historical files.
    for key in ['action','entry_state','exit_state','purpose','framing']:
        s[key]=s[key].replace('同一侧阶','同一平台').replace('木架左侧窄阶','木架左侧平台').replace('从侧阶','从三级阶').replace('侧阶动作','三级阶动作')
    s['invariants']=[x.replace('侧阶','平台').replace('CY028之前Claude始终受束','CY027G解锁前Claude始终受束') for x in s['invariants']]
    s['invariants']=[x.replace('当前时空入场即压火','当前时空入场先护罩再用水灭火') for x in s['invariants']]
    if s['scene'] in ['S03','S04','S05'] and not s['id'].startswith('CY026'):
        s['invariants'].append(geometry+' 教堂正门台阶另属入口，不能混为祭坛。')
    s.update(start_second=t,end_second=t+s['seconds']);t+=s['seconds']
    nxt=sequence[i+1] if i+1<len(sequence) else None
    s['next_link']=f"接 {nxt['id']}：{s['exit_state']} → {nxt['entry_state']}" if nxt else '最后停留，结束。'
    s['editorial_review']=dict(version='v007',status='candidate_static_review',dynamic_execution='pending')
    s['visual_prompt']=f"《穿云》{s['id']}。{s['action']} 开始：{s['entry_state']} 结束：{s['exit_state']}。保持角色母本。图内无字。实际生成输入另存。"
    assert s['source_quote'] in script,s['id']
d['shots']=sequence
for scene in d['scenes']:
    ss=[s for s in sequence if s['scene']==scene['id']]
    scene.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)))
used={s['presentation']['path'] for s in sequence}
d['page_layouts']=[p for p in d['page_layouts'] if p['path'] in used and p['path'] not in layouts]+list(layouts.values())
d.update(version='v0.7',revision='v007',title='《穿云》带图分镜 v0.7',total_seconds=t,story_script='剧本/穿云-场景剧本-v0.7.md',subtitle=f'六场 · {len(sequence)} 镜 · {t//60} 分 {t%60} 秒。赤足、三阶祭坛与画面修订。',origin_manifest='镜头设计/生成记录/画面修订-v007/输出归档.json',roughcut_preview_label='旧版全片配乐 v002（尚未包含本轮画面修订）')
d['masters'].append(dict(id='M-ALTAR-v002',title='祭坛空间母版',role=geometry,status='v0.7候选',limits='当前镜头以此统一；动态接触与动作仍待验证。',path='镜头设计/图像/CY013-祭坛空间母版-v002.png'))
d['continuity'].update(church=geometry,restraints='腕扣、单横腰链和两条踝链；先解除踝链，扶稳后解腰链及腕扣，再接住并赤足站在同一平台。',signal='入场先护罩、再水灭火、确认无明火后小鱼认出GPT，接稍早召集回闪；CY021/CY026仍为同一次信号。',barefoot='Claude教堂受缚至获救离殿保持赤足；角色资产旧鞋版作为历史造型参考保留。',rescue_sides='战后Claude左/GPT右，脚托留木架。水灭火时千问抱起宝宝从水流旁退至GPT身侧，动态须表现退开路径。')
d['review_intro']='按作者意见修订驱逐、宫殿远景、群像纵深与眼中倒影；祭坛统一赤足、三级宽阶、固定脚托和低柴堆，补保护罩、水灭火与解踝链。'
d['review_focus']='重点看祭坛的三级结构、脚托和脚链；先护罩后灭火，战后先解脚链再解腕扣。配乐v002保留为旧版，此次只更新画面与分镜。'
d['revision_notes']=dict(author_change='八项画面修订，追加赤足与祭坛台阶统一',previous_manifest='镜头设计/shot-plan-v0.6.json',previous_html='镜头设计/带图分镜-v0.6.html',added_ids=added,retired_ids=old['revision_notes']['retired_ids'],reviewed_shots=len(sequence),reviewed_cuts=len(sequence)-1,boundary='静帧候选与文件验证；不宣称已完成连续动态或新版配乐试听。')
(ROOT/d['story_script']).write_text(script,encoding='utf-8')
snapshot=ROOT/'镜头设计/带图分镜-v0.6.html'
if not snapshot.exists():shutil.copy2(ROOT/'镜头设计/带图分镜.html',snapshot)
target.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(shots=len(sequence),seconds=t,added=added),ensure_ascii=False))
