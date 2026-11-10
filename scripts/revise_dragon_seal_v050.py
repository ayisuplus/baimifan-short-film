"""Apply the author's coiled dragon / hand-seal revision without changing music IDs."""
import copy, hashlib, json, shutil
from pathlib import Path
from PIL import Image

R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/结印盘龙-v050'
OUT='镜头设计/shot-plan-v0.50.json'
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def save(p,v):
    out=R/p;out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

base=load('镜头设计/shot-plan-v0.49.json');p=copy.deepcopy(base)
old={s['id']:s for s in base['shots']};by={s['id']:s for s in p['shots']}
script=(R/base['story_script']).read_text(encoding='utf-8-sig')
chant=['盘踞于苍穹尽头，','统御万千深流的水之灵啊，','请将散落尘世的万千水息，','汇作悬于群星之下的无岸之海。','以重云为岸，以长风为引，','令沉睡的潮汐翻卷，奔涌而来。','此刻，洞开天穹，倒悬沧海；','令灼烧无辜的烈焰，在奔流中止息；','将阻挡吾行的高墙，淹没于万顷狂澜！','请降下你的救赎——','沧海天倾！']

def cue(sid,rows,full=None):
    s=by[sid];s['subtitle_cues']=[dict(speaker='ChatGPT',text=t,offset=o,duration=d) for t,o,d in rows]
    s['dialogue']='ChatGPT（画外）：'+(full or ''.join(r[0] for r in rows))
    s['dialogue_timing_status']='字幕时长预算；正式配音及逐字听审待制作'

for sid in ['CY024A9','CY024A10','CY024A11','CY024A12']:
    cue(sid,[('统御万千深流的',0,by[sid]['seconds'])],chant[1]+'（跨镜连续句，本镜前半句，不重复起句）')
cue('CY024A1',[('水之灵啊，',0,2.9)],chant[1]+'（接前半句完成）')
cue('CY024A2',[(chant[2],0,3.9)])
cue('CY024A3',[(chant[3],0,5.4)])
cue('CY024A6',[(chant[4],0,2.6),(chant[5],2.6,3.3)])
cue('CY024A7',[(chant[6],0,3.4)])
cue('CY024A8',[(chant[8],0,3.9)])
cue('CY024A5',[(chant[9],2.4,2.6),(chant[10],5.8,2.1)])
by['CY024A5']['dialogue']='ChatGPT：请降下你的救赎——沧海天倾！'

actions={
'CY024A6':'切到教堂外低处，从地面仰拍中殿上空。完整尖塔与屋顶轮廓压在下缘，层层深蓝云壁向中心旋卷，上浮水珠融入云腹；云褶之间托住连续的深蓝水面，银色月光沿涟漪流动，仿佛整片海悬于夜空。水只在高空汇聚，没有闪电或发光法环。云心正对中央中殿，后殿不在破坏区。镜末水面向中心收拢，为下一镜水龙下行蓄势。',
'CY024A7':'摄影机切到教堂上方，以陡俯视角随水龙从云腹向下。近处是水龙向下弯折的厚重长颈与龙首背面，远处尖塔、长条中殿屋脊和后殿构成高度参照。单一深蓝水龙从前景上方斜冲中央中殿屋顶，体躯有明显透视缩短，龙首先至、长身随后。镜末吻部撞上中殿指定位置，石瓦开裂形成第一处缺口；后殿屋顶与左右侧窗完整。水龙没有从手或地面生出。',
'CY024A5A':'紧接上一镜同一处撞点，切入殿内从侧下方仰拍穹顶破裂的特写。水龙头颈以同一向下斜冲方向穿入，石板和拱肋碎块沿缺口向下、向外翻开，重块慢于水首，粉尘与水雾被气流推开。厚重水腹掠过断面后开始弯转，避开吊灯、GPT及同伴所在位置；碎块落向无人侧廊。只扩大中央中殿的这一处破口，不炸后殿，不新增第二处天窗。镜末水龙已入殿，接两处反应切镜，跨切完成回卷盘身。',
'CY024A8':'教主仍在下段中央缓台，听到破顶巨响，抬眼追踪已经入殿的水龙；眉眼绷紧，另一只手抬起准备护身。画外龙身经过高处投下流动的银蓝反光，脸侧仍有尚未扑灭的火盆暖光。这个近景不显示屋顶；中殿已破，后殿完整，教主衣袍仍干，暗金护罩尚未展开。GPT在反应切镜期间持续结印，水龙沿她身后外侧回卷。',
'CY024A5':'切回正面略低的中远景。GPT悬空直立在构图中央，双翼舒展，双手在胸前结印：两手相扣、食指并拢竖起，手腕与肘部自然，面部与手势完整可见。水龙已经在她周围盘成宽松立体的一圈，后段高过翼背，近处前段低于膝部，体躯前粗后细、有透视缩短，不勒住人物。龙首停在画面右侧肩旁，三分之二侧面朝向前下方敌人，深蓝水腹有眉骨、吻部、下颌与转颈的体积，浪鬃沿脊背流动；不是实体冰龙或平面圆环。她不伸手抚龙，不反复指点。镜头缓慢靠近，完成祈愿与报术名；救赎后音乐收声半拍。术名最后一字只完成蓄势，双手仍未解印，水龙仍盘在身边，没有提前攻击。',
'CY024A5B':'同侧动作轴切近至膝上，承接上一镜仍相扣的双手。GPT先抬眼锁定画外前下方的教主，双手分开，左手留在胸前，右肩带动右臂向前下方一次指出，食指伸出，其他手指自然收拢。指尖不喷水。水龙先转首响应，长颈随之扭转，后高前低的盘势舒展开，整条水龙向画面右前下方冲去。先有人物指令，后有水首响应；本镜只启动俯冲，不提前出现撞盾水花。',
'CY024B':'从GPT侧后上方斜俯拍。近景她仍保持一次前指的收势，白色人身与水龙清楚分离；中景同一条深蓝水龙沿有体积的弧线俯冲，龙首先压中下段中央缓台的教主暗金罩，眉骨、吻部和长颈在接触前仍保持可辨轮廓，接触后吻部才崩开为厚重白浪。后随水身继续压入，余水向左右外侧通道分流，冲断黑金袍教徒的阵形，扑灭外围残柴与普通灯火。只有一个龙首，不再增加左右两条龙或三股直柱。最高祭坛不透明暗月罩与中央上层石阶保持干燥净空，没有被水撞击，罩内人物不可见；千问与小鱼仍在柱边友方安全位置。中央后窗保持原破口，后殿拱顶和侧窗完整。镜末GPT收势，上方水源停止补给，龙形随冲击化散，余水继续沿两侧石阶下行。',
}

meta={
'CY024A6':('云腹聚水，倒悬之海','外景低处仰拍，全景交代天空与完整教堂','水珠上浮，屋顶完整。','云腹水海成形，接高空俯冲。','高空长风与深沉潮鸣，压低于咏唱；没有雷电声。'),
'CY024A7':('俯冲，水龙直下穹顶','教堂外高空陡俯视，随龙首向下','云海已聚起水龙，中央中殿屋顶尚完整。','龙首触顶，石瓦开裂；接同一撞点特写。','长风骤急、下坠水鸣，镜末接第一下石瓦裂响。'),
'CY024A5A':('破顶，水首贯入','殿内侧下方仰拍撞点特写','龙首已撞开中央中殿同一位置。','单一破口张开，水龙入殿转弯；反应切镜期间盘到GPT身边。','一记沉重破石声、石屑与短促水啸；此镜无咏唱，给撞击留声音空间。'),
'CY024A8':('教主追视入殿水龙','沿用面部近景，屋顶保持画外','中殿已破，水龙已入殿；教主仍在缓台。','教主准备护盾，水龙在反应切镜期间盘稳。','破顶声尾音衰减，厚重水身回卷的低鸣与衣料声。'),
'CY024A5':('居中结印，水龙盘身','正面略低中远景，人物居中完整，缓慢靠近','水龙已在跨切期间回卷，GPT双手结印，水龙盘势已建立。','术名念完，双手仍结印；下一镜解印前指才发起攻击。','0—2.4秒盘水低鸣；2.4—5秒救赎祈愿；5—5.8秒音乐骤收；5.8—7.9秒术名坚定落下，不提前放撞盾重音。'),
'CY024A5B':('解印，一指出击','同侧动作轴膝上景，手与龙首同框','双手仍相扣，水龙仍盘在她身边。','右臂一次前指，水龙响应并启动俯冲，尚未命中。','解印衣袖轻响，前指后水啸加速；撞盾声留到下一镜。'),
'CY024B':('水龙冲击，后浪清场','GPT侧后高位斜俯大景，敌方金罩与远处安全祭坛同框','水龙已响应前指，龙首沿弧线冲向教主。','龙首撞散为浪，供水停止；余水冲向两侧，最高祭坛净空。','水首撞金罩的低沉重音，随后厚浪拍石、教徒惊呼；无雷电声，无友方罩体受水声。')}

for sid,action in actions.items():
    s=by[sid];title,framing,entry,exit_,sound=meta[sid]
    s.update(title=title,framing=framing,entry_state=entry,exit_state=exit_,sound=sound,action=action,purpose='交代'+title+'，保持水龙与施法者的因果和空间关系。')
    # Store one source passage, with actual spoken text only once in the screenplay.
    spoken='\n'.join(c['text'] for c in s.get('subtitle_cues',[]))
    s['source_quote']=action+ ('\n\n**ChatGPT'+('（画外）' if sid not in ['CY024A5'] else '')+'：**\n'+spoken if spoken else '')
    s['cinematic_beats']=[dict(offset=0,intent=entry),dict(offset=min(.7,s['seconds']/2),intent=title)]
by['CY024A5']['cinematic_beats']=[dict(offset=0,intent='中心结印，立体盘势已经形成'),dict(offset=2.4,intent='请降下你的救赎，手印保持'),dict(offset=5,intent='收声0.8秒，水龙停势'),dict(offset=5.8,intent='术名完成蓄势；尚不解印、不冲击')]
by['CY024A5B']['cinematic_beats']=[dict(offset=0,intent='先锁定教主，双手解印'),dict(offset=.5,intent='右臂一次指出，水首随后转向'),dict(offset=1,intent='龙身展开启动俯冲，切命中大景')]
by['CY024B']['cinematic_beats']=[dict(offset=0,intent='龙首压中敌方金罩，接触后才化浪'),dict(offset=2,intent='后随水身冲入，余水分两侧清场'),dict(offset=4,intent='收势停供水，余水继续下行')]

# Replace new spoken lines in their unchanged earlier inserts.
line_pairs=[('统御深流与雷鸣的古老意志啊。',chant[1]),('循吾之声，自漫长的沉眠中苏醒。',chant[2]),('将散落尘世的万千水息，\n汇作悬于群星之下的无岸之海。',chant[3]),('苍龙雷渊','沧海天倾'),('水雷','水流'),('头顶雷声','头顶潮声'),('远处雷声','远处潮声'),('此镜还未出现紫电','云腹尚未释放水龙'),('洪水与魔法雷','洪流'),('主落水柱','水龙下行路径'),('主水柱','水龙下行路径'),('不延续紫电','保持纯水质感'),('这股清水没有魔法雷','这股清水已不再保持龙形')]
line_pairs.extend([
 ('完整屋顶期间紫光只经侧窗或敞门入殿；雷声可听见，云心不可透顶看见。','完整屋顶期间月光和水光只经侧窗或敞门入殿，云海不可透顶看见；中段潮鸣先到，A7/A5A才破开中央中殿。'),
 ('教主听雷转防御','教主循潮声与破顶动静转为防御'),
])
def words(t):
    for a,b in line_pairs:t=t.replace(a,b)
    return t

# Change script quotes before general wording, then move the breach close-up as a whole.
for sid in actions:
    assert old[sid]['source_quote'] in script,sid
    script=script.replace(old[sid]['source_quote'],by[sid]['source_quote'],1)
close=by['CY024A5A']['source_quote']
assert script.count(close)==1
script=script.replace(close+'\n\n','',1)
script=script.replace(by['CY024A7']['source_quote'],by['CY024A7']['source_quote']+'\n\n'+close,1)
script=words(script)

skip={'path','refs','visual_prompt','generation_request','page_layouts','source_manifest','origin_manifest'}
def rewrite(v):
    if isinstance(v,str):return words(v)
    if isinstance(v,list):return [rewrite(x) for x in v]
    if isinstance(v,dict):return {k:(x if k in skip or k.startswith('previous_') else rewrite(x)) for k,x in v.items()}
    return v
p=rewrite(p);by={s['id']:s for s in p['shots']}

water='云海聚水→高空俯冲触顶→同一撞点近景破开中央中殿→跨Kimi与教主反应镜回卷盘身→GPT居中双手结印完成救赎祈愿及术名→下一镜解印、右臂只向前指一次→水龙随后俯冲撞金罩，接触后化浪，后随水身冲两翼。无魔法雷电。Kimi暗月罩隔绝敌法，水流从始至终远离最高祭坛和同伴。'
ct=copy.deepcopy(p['continuity'])
ct.update(water_curtain=water,storm_release=water,water_gathering='外景水珠向上汇入云海，A6云海完整；A7从上向下俯冲、镜末首次触顶，A5A破顶特写。A4/A8时中殿已破，水龙跨切盘身。后殿完整，Kimi中央后窗破口不变。',water_volume='水龙具有单一龙首、眉骨吻部与下颌、转颈和粗细变化；纯蓝透明水腹，背脊浪鬃，前低后高立体盘势。GPT悬空站立居中，双手胸前结印8秒，面部和手完整可见；后接1.5秒解印前指。不是盘坐或反复指点，也不是平面圆环、均匀水管。',water_impact_insert='单一水龙撞教主金罩，龙首接触后才化浪，后随水身和余水分到两翼冲散教徒、灭残柴及普通灯火。B3两侧退水，B3A罩内安抚，B1教徒失足。后墙长椅固定。',support_roles='Kimi定位瞬移、震柴、暗罩挡教徒魔法，照顾Claude并战后解锁；GPT结印控水龙，一次前指清场灭火；千问抱护小鱼和扇叶阻击保持。',gpt_flight='GPT先升至完整中殿穹顶下，避开中央吊灯；水龙从她外侧的指定破口入殿，反应切镜期间回卷盘身。GPT悬空直立居中结印，前指后水龙离身攻击，退水后落地；人物不是水龙本体，后段真正变身另外发生。')
old_to_new={p['continuity'][k]:v for k,v in ct.items() if p['continuity'].get(k)!=v}
p['continuity']=ct
for s in p['shots']:
    inv=[]
    for v in s['invariants']:
        v=old_to_new.get(v,v)
        if any(x in v for x in ['右食指选点','云内紫电','三股独立水柱','三点定流','前段仍高举掌心','云中水柱','首点落柱前']):v=water
        if v not in inv:inv.append(v)
    s['invariants']=inv

# Update retreat and ambient wording only in the water sequence; later storm remains.
retreat_pairs=[('三股水柱均已收雷停水，左右落点的清水与主柱外泄水沿外侧石阶汇流。','水龙已撞盾化浪，上方停止供水，余水沿两侧石阶下行。'),('左右辅柱已经停止供水，落点积水与主柱外泄清水汇成两条厚重水道','水龙的后随水身化散后，余水汇成两条厚重水道'),('，紫电已经收尽','，不再保留龙形'),('左右辅柱及主柱外泄清水沿祭坛侧道冲向刚才围攻的教徒，三柱紫电已全部收尽。','水龙化散的余水沿祭坛侧道冲向刚才围攻的教徒。'),('沧海天倾的紫电已收尽，水幕停下','沧海天倾已经收势，龙形化散，上方供水停下'),('紫电与水幕结束','水龙化散、上方供水结束')]
for a,b in retreat_pairs:
    script=script.replace(a,b)
    for s in p['shots']:
        for k in ['action','entry_state','exit_state','source_quote','next_link','sound']:
            if isinstance(s.get(k),str):s[k]=s[k].replace(a,b)
        s['presentation']['visible']=s['presentation']['visible'].replace(a,b)
for sid,sound in {'CY024A1':'承前咏唱，衣料与呼吸；罩外敌法闷响及高空潮鸣。','CY024A3':'水滴液桥合并轻响，高空长风；无落雨或电流音。','CY024A4':'罩外破顶余响逐渐变闷，锁链轻响与呼吸；水龙在画外回卷，最高祭坛没有受水撞击。'}.items():by[sid]['sound']=sound
by['CY024A4']['entry_state']='水龙已破中央中殿顶，暗月罩仍平静，双刃已收好；Claude双踝未解。'
by['CY024A8']['presentation']['missing']='沿用反应近景；屋顶保持画外，动态补水龙经过的银蓝反光，非新生成画面。'
for sid in actions:by[sid]['presentation']['visible']=by[sid]['action']

# Reorder stable IDs and derive all absolute times. No new IDs or music selections.
moved=by['CY024A5A'];p['shots'].remove(moved);at=p['shots'].index(by['CY024A7']);p['shots'].insert(at+1,moved)
elapsed=0
for i,s in enumerate(p['shots']):
    s.update(start_second=elapsed,end_second=elapsed+s['seconds']);elapsed+=s['seconds']
    if i+1<len(p['shots']):s['next_link']='接 '+p['shots'][i+1]['id']+'：'+p['shots'][i+1]['entry_state']

# Freeze and apply reviewed image candidates, preserve every previous presentation.
rows=load(REC+'/实际请求.json')
image_changes=[]
for row in rows:
    sid=row['id'];s=by[sid];dest=R/f'镜头设计/图像/结印盘龙-v050/{sid}-v050-r{row.get("rev",1)}.png'
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(row['source'],dest)
    with Image.open(dest) as im:w,h=im.size;im.verify()
    rel=dest.relative_to(R).as_posix();req=REC+'/'+sid+'.json'
    record=dict(row,output=rel,sha256=sha(dest),dimensions=[w,h],engine='built-in image_gen',status='revised_storyboard_candidate_pending_author_visual_review')
    save(req,record)
    s['previous_presentation_v049']=old[sid]['presentation'];s['previous_generation_request_v049']=old[sid]['generation_request']
    s['presentation'].update(path=rel,visible=s['action'],status='v0.50结印盘龙修订，待作者视觉审阅',missing='静帧代表动作关键状态，破顶运动、盘绕路径、手印解开及水首响应仍待动态制作。')
    s['refs'].append(dict(path=rel,role='v0.50修订主图；旧版原图保留'))
    s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0,y=0,w=1,h=1),panel_index=0,visual_prompt=row['input']['prompt'],generation_request=req,editorial_review=dict(version='v050',status='pending_author_review',dynamic_execution='pending'))
    s['final_static_review']=dict(version='v050',status='pending_author_visual_review')
    image_changes.append(dict(id=sid,before=old[sid]['presentation']['path'],after=rel,sha256=sha(dest)))
for sc in p['scenes']:
    group=[s for s in p['shots'] if s['scene']==sc['id']]
    sc.update(shot_ids=[s['id'] for s in group],seconds=sum(s['seconds'] for s in group),pages=list(dict.fromkeys(s['presentation']['path'] for s in group)))
p['page_layouts']=[dict(path=path,rows=1,cols=1) for path in dict.fromkeys(s['presentation']['path'] for s in p['shots'])]
p.update(version='v0.50',picture_revision='v050',report_revision='v050',title='《穿云》带图分镜 v0.50 · 破顶、结印盘龙与一指出击',story_script='剧本/穿云-场景剧本-v0.50.md',source_manifest='镜头设计/shot-plan-v0.49.json',audio_arrangement='后期/结印盘龙-v050/预演编排.json')
p['review_intro']='云海聚水后接高空俯冲与破顶特写；GPT居中悬空结印，水龙立体盘身，最后解印前指一次。纯水咏唱保留救赎，七首BGM与全部镜号保持。'
p['review_focus']='审阅破顶的俯视—特写接续、中央手印与盘龙空间、一次前指驱动冲击。新图待作者确认；正式配音、声音混合与动态尚未制作。'
p['revision_notes']=dict(previous_manifest=p['source_manifest'],modified_image_ids=[x['id'] for x in image_changes],added_ids=[],moved_ids=['CY024A5A'],boundary='131镜431.5秒，A5A前移至A7后，其余相对顺序保持；全部BGM标记与现有语音文件不变。结构revision沿用v048验证分支。')
md=p['music_direction'];md.update(approved_incantation=chant,rule='中段“洞开天穹”接俯冲触顶，A5A破顶重音无对白；A4/A8跨切继续咏唱并完成盘身。A5救赎句后留0.8秒收声，术名只完成蓄势；A5B解印前指后水啸启动，B才撞盾。无魔法雷电声。正式配音、音效和乐句混合待制作。')
md['incantation_bridge']['text']=chant[1]
ids=[s['id'] for s in p['shots']];md['sequence']=ids[ids.index('CY024A0'):ids.index('CY024B1')+1]
md['estimated_spell_sequence_seconds']=sum(by[sid]['seconds'] for sid in md['sequence'])
md['estimated_gpt_incantation_seconds']=round(sum(c['duration'] for sid in md['sequence'] for c in by[sid].get('subtitle_cues',[])),3)
md['pre_release_sequence_seconds']=by['CY024A5B']['start_second']-by['CY024A0']['start_second']
script=script.replace('v0.48r1','v0.50').replace('终极审查说明同步；对白与画面保持。','水龙俯冲破顶、居中结印盘身、一次前指出击；纯水咏唱保留救赎。')
(R/p['story_script']).write_text(script,encoding='utf-8')
save(OUT,p)
audio=load(base['audio_arrangement'])
for s in p['shots']:
    if s['id'].startswith('CY024A') or s['id'] in ['CY024B','CY024B3','CY024B1','CY027']:audio['effects'][s['id']]=s['sound']
def audio_notes(x):
    if isinstance(x,str):return x.replace('长咏唱双候选；04:03–04:03.8收声、04:06水雷重音尚待精剪','纯水咏唱；A5A破顶重音，A5镜内5—5.8秒收声，A5B前指启动，B撞盾。正式乐句精剪待制作')
    if isinstance(x,list):return [audio_notes(v) for v in x]
    if isinstance(x,dict):return {k:audio_notes(v) for k,v in x.items()}
    return x
audio=audio_notes(audio)
audio.update(version='v050-dragon-seal-seven-tracks',shot_plan=OUT,shot_plan_sha256=sha(R/OUT),previous=base['audio_arrangement'])
save(p['audio_arrangement'],audio)
assert set(old)==set(by) and len(p['shots'])==131 and elapsed==431.5
assert p['music_adoption']==base['music_adoption']
assert audio['adopted_music']==load(base['audio_arrangement'])['adopted_music']
for s in p['shots']:
    assert s['source_quote'] in script,s['id']
    assert old[s['id']]['dialogue_cues']==s['dialogue_cues'],s['id']
    for c in s.get('subtitle_cues',[]):assert c['offset']+c['duration']<=s['seconds'],s['id']
assert by['CY024B']['start_second']==old['CY024B']['start_second']
assert not any(x in ''.join(chant) for x in ['绕过','雷','紫电'])
snapshot=R/'镜头设计/带图分镜-连续性修复-v049.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
save(REC+'/变更核验.json',dict(shots=131,seconds=elapsed,images=image_changes,moved_id='CY024A5A',music='seven_author_selections_unchanged',dialogue_audio='existing_clips_unchanged_new_chant_unrecorded',source_quotes='all_matched',subtitles='within_budget_not_actual_voice_review',timeline=[dict(id=s['id'],before=old[s['id']]['start_second'],after=s['start_second']) for s in p['shots'] if old[s['id']]['start_second']!=s['start_second']],dynamic_validation='pending'))
print(OUT)
