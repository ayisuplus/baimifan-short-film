"""Version the three deliberate pointing gestures and cloud-fed water targets."""
import copy, hashlib, json, re, shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
PLAN='镜头设计/shot-plan-v0.47.json'
REC='镜头设计/生成记录/三点定流-v047'
IMG='镜头设计/图像/三点定流-v047'
def read(p): return (R/p).read_text('utf-8-sig')
def load(p): return json.loads(read(p))
def write(p,s):
 (R/p).parent.mkdir(parents=True,exist_ok=True)
 (R/p).write_text(s,encoding='utf-8')
def save(p,v): write(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256((R/p).read_bytes()).hexdigest()
assert not (R/PLAN).exists(), 'Preserve existing revision'
old=load('镜头设计/shot-plan-v0.46.json')
d=copy.deepcopy(old); script=read(old['story_script'])
ct=copy.deepcopy(old['continuity'])
ct.update(
 water_curtain='同一片云层供给三股互相分离的银蓝水雷柱：中央主柱较粗，正面压向教主暗金罩；左右两股辅柱分别压入围攻教徒所在的外侧通道。三柱均从中央中殿上方落下，不从指尖发射，不由一根柱中途分叉。GPT用右食指依次点选中央、左侧、右侧；每次指向对应一处落水重音。三处落点及后续径流都避开最高祭坛暗月罩与同伴，保留中央净空石面。三柱紫电统一先收尽，再接清水余浪冲散教徒。',
 water_volume='CY024A5保留八秒咏唱与前段掌上聚能，最后渊字右前臂落至肩前、伸出食指首点教主；CY024A5A再点左侧，CY024A5B再点右侧，各1.5秒。CY024B呈现一主两辅三股厚重水柱，辅柱虽较细仍明显宽于人身，不能变细小水线。三柱向外侧泄流，中央祭坛始终有净空。CY024B3两条厚水道与安稳暗罩同框；B3A罩内安抚；B1清水没过教徒腰腹，冲断阵形并沿侧阶下行。',
 storm_release='GPT以右食指依次指定教主、左翼教徒、右翼教徒，水雷从云层落向三处敌方区域。紫电局限于三股水体和敌方落点，不接触祭坛暗月罩、Claude束具或同伴。镜末三柱紫电先收尽、上方供水停止，已落下的清水沿外侧通道冲散教徒，再退水、对峙与变身。',
 water_impact_insert='三股水雷打击中央敌方金罩及两翼围攻区域，清水余浪扑灭罩外残柴与普通灯火。Kimi先震散木头并隔绝教徒攻击；GPT用三次瞄准留出祭坛安全区，左右辅柱及主柱外泄水汇成外侧水道。CY024B1拍同一批教徒被厚重清水冲散、失足滑下侧阶、法杖脱手。长椅留作固定背景，历史CY024B2不接入镜序。',
 support_roles='Kimi负责明刃定位瞬移、震柴、暗刃阻挡教徒法术、罩内照顾及战后钥匙解锁；GPT负责指向三处目标、控制一主两辅云中水雷，打击教主与两翼围攻教徒，同时让水流避开暗罩并扑灭残柴。Perplexity警戒，千问抱护小鱼并保持原扇叶阻击。')
repls={old['continuity'][k]:v for k,v in ct.items() if v!=old['continuity'][k]}
repls.update({
 '本镜主图为蓄力保持状态：右手高举掌心向上，左手在胸前稳术；报招末字才压掌，不提前释放。掌上水团控制云中聚水，不作为巨型水柱的出水口。':'本镜主图是八秒咏唱末尾的首点结束帧，不能把这张首点图当成全八秒的蓄力姿势。前段仍高举掌心聚能；末字右食指点向教主，左手在胸前稳术。指尖只指定目标，不是出水口。',
 '蓄力至压掌':'蓄力至首点及左右选点',
 '最后一个“渊”字才翻掌压下':'最后一个“渊”字才伸出右食指点向教主'
})
def rewrite(v):
 if isinstance(v,str):
  for a,b in repls.items(): v=v.replace(a,b)
  return v
 if isinstance(v,list): return [rewrite(x) for x in v]
 if isinstance(v,dict): return {k:rewrite(x) for k,x in v.items()}
 return v
d=rewrite(d);script=rewrite(script);by={s['id']:s for s in d['shots']}
s=by['CY024A5'];before=s['source_quote']
s.update(framing='空中侧前方中近景，末字首点时眼神与右食指同框',
 action='GPT振翼悬停，前段右掌高举凝聚水雷，左手在胸前稳术。念到最后一个“渊”字，掌上光团收拢消散，右前臂落至肩前，食指伸出、其余手指自然收拢，目光沿指向锁定下方教主。中央主水柱应声从云层落下；指尖只留一粒水光，不喷水。本镜采用咏唱末尾的首点结束帧。',
 exit_state='首点教主，第一股云中主柱落下；保持同一侧摄影轴，接右手转指左翼。',
 purpose='完整保留咏唱，以末字首点明确施法手势与中央落点的因果。',
 sound=s['sound']+' 首点中央接第一声低沉落水重音；后两次选点分镜各接一声，不重复咏唱。')
s['source_quote']=before.replace('高举的手掌直到最后一个“渊”字才翻转压下，将蓄积引向主落点；掌上光团是控制与聚能的节点，巨型水柱仍来自屋顶上空的螺旋乌云，并非从掌心直接喷出。','高举的右掌直到最后一个“渊”字才收拢光团、落至肩前，食指伸出，其余手指自然收拢。她目光沿指向锁定下方教主，第一股主水柱应声落向暗金罩。指尖只留一粒水光作为选点提示；水柱来自屋顶上空的螺旋乌云，并非从手指喷出。')
assert s['source_quote']!=before
script=script.replace(before,s['source_quote'])
s['cinematic_beats']=[dict(offset=0,intent='确认安全区，右掌上举聚能'),dict(offset=2.4,intent='掌心持续蓄力，坚定祈愿'),dict(offset=5,intent='音乐骤收，留呼吸'),dict(offset=5.8,intent='报招；末字收光团，右食指首点教主，云中第一柱落下')]
s.pop('final_static_review',None)
new_specs=[
 ('CY024A5A','第二点，锁定左翼','GPT保持同一高度悬停，左手仍在胸前稳定术式。她先将视线转向左翼教徒，右肩带动同一条右臂向画面左侧展开，食指点向左下方外侧通道；右肩、肘、腕衔接清楚，不交换施法手。第二股较细但厚重的云中水柱落向左翼围攻区域，第一股主柱仍在远处虚焦背景中持续。指尖水光只闪一下，不射出水线。','第一股主柱已压住教主，右手完成首点。','左翼辅柱落下，右臂准备横向移指右翼。','第二次短促选点水鸣，接左侧重水落地；中央主柱轰鸣持续。'),
 ('CY024A5B','第三点，锁定右翼','GPT的目光先扫向右翼教徒，身体保持悬停，右前臂随之横移到画面右侧，伸直的食指指向右下方外侧通道，动作比首点更向外展开；左手始终在胸前稳术。第三股辅柱从云层落向右翼围攻区域，前两股水柱在虚焦背景中持续。三次选点都避开最高祭坛与同伴，手指没有喷射水流。镜末接高位斜俯全景确认三处落点。','左侧辅柱已落下，主柱持续；右手由左翼横移。','第三股水柱命中右翼，接一主两辅全景。','第三次选点水鸣接右侧重水落地，三股轰鸣汇合后切大景。')]
new=[]
for sid,title,action,entry,exit_,sound in new_specs:
 n=copy.deepcopy(s)
 n.update(id=sid,title=title,seconds=1.5,dialogue='无对白',dialogue_cues=[],source_quote=action,action=action,entry_state=entry,exit_state=exit_,sound=sound,purpose='用明确的眼神与右食指方向对应一处云中落水目标。',framing='同侧摄影轴的空中中近景，面部与完整右手同框',cinematic_beats=[dict(offset=0,intent='目光先锁定目标，右臂移指'),dict(offset=0.7,intent='食指停定，下一股云中水柱应声落下')])
 for key in ['subtitle_cues','dialogue_timing_status','final_static_review']: n.pop(key,None)
 n['invariants']=[v for v in n['invariants'] if not v.startswith('本镜主图是八秒')]
 n['invariants'].append('始终以右食指选点，左手留在胸前稳术；前一股云中水柱持续，当前手势只增开对应目标，不从指尖出水。')
 new.append(n);by[sid]=n
i=d['shots'].index(s);d['shots'][i+1:i+1]=new
script=script.replace(s['source_quote'],s['source_quote']+'\n\n'+'\n\n'.join(n['source_quote'] for n in new))
b=by['CY024B'];before=b['source_quote'];old_title=b['title']
b.update(title='三点定流，一主两辅清场',framing='GPT侧后高位斜俯大景，三柱落点与远处安全祭坛同框',
 action='从空中ChatGPT侧后上方斜俯拍，近景膜翼、中景三股水雷、远处安全祭坛构成纵深。她右食指仍指向第三处右翼目标，左手维持胸前稳术。中央中殿上方同一云层降下三股互相分离的银蓝水柱：较粗主柱压向下段中央缓台的教主暗金罩；左右辅柱分别压入两翼围攻教徒的外侧通道。每股都厚重、连续，辅柱明显宽于人身，不从主柱分叉，也不从指尖射出。紫电在三股水体内盘绕，教徒穿黑金兜帽长袍，散落于两翼落点附近。最高祭坛不透明暗月罩与中央通道保持净空，三处落点和径流都主动避开友方；暗罩不受水压，外景看不见两人与刑架。水沿外围石阶奔涌、扑灭残柴与普通灯火，打断教徒施法。千问与小鱼仍在柱边同伴安全位置、可出画。中央高窗破口保留，左右侧窗与后殿拱顶完整。镜末三柱紫电先收尽，上方供水停止，已落下的清水向外侧台阶汇流。',
 entry_state='GPT已连续点选中央教主、左翼及右翼教徒，三股云中水柱先后落下。',
 exit_state='三处目标被压制，三柱紫电收尽、供水停止；清水余浪沿两侧通道下行，祭坛中央保持净空。',
 sound='承接第三次命中，三股重水轰鸣形成空间层次；中央撞金罩、左右拍石与教徒惊呼，友方暗罩没有受水撞击声。',
 purpose='一次交代三次瞄准的结果，兼顾力量规模、目标关系和友方安全区。',
 cinematic_beats=[dict(offset=0,intent='第三柱落定，一主两辅与安全祭坛同框'),dict(offset=3.5,intent='三柱紫电收尽，停止供水，余浪沿两侧下行')])
b['source_quote']=b['action'];script=script.replace(before,b['source_quote']).replace(old_title,b['title'])
for sid in ['CY024B3','CY024B1']:
 t=by[sid];before=t['source_quote']
 if sid=='CY024B3':
  t['action']=t['action'].replace('GPT引导的厚重清水在暗月罩前方尚有明显距离时就分向左右，沿两侧石阶形成汹涌水道。','左右辅柱已经停止供水，落点积水与主柱外泄清水汇成两条厚重水道，沿祭坛外侧石阶下行。GPT预先选定的落点远离暗月罩，水路从一开始就绕开中央。')
  t['entry_state']='三股水柱均已收雷停水，左右落点的清水与主柱外泄水沿外侧石阶汇流。'
 else:
  t['entry_state']='左右辅柱及主柱外泄清水沿祭坛侧道冲向刚才围攻的教徒，三柱紫电已全部收尽。'
 t['source_quote']=t['action'];script=script.replace(before,t['source_quote'])
selected={}
for req in ['01-首点与三柱大景.json','02-左右瞄准与大景修正.json','03-左点头饰修正.json']:
 for row in load(REC+'/'+req): selected[row['id']]=(row,REC+'/'+req)
images=[]
for sid,(row,req) in selected.items():
 t=by[sid];prior=t['presentation']['path'];path=f'{IMG}/{sid}-v047-r{row["rev"]}.png'
 t['presentation'].update(path=path,visible=t['action'],status='v0.47三点定流修订候选，待作者画面审阅',missing='静帧已查看；三次转指与逐柱响应、收雷停水接续待动态制作。')
 t['refs']=[dict(path=path,role='本轮修订候选'),dict(path=req,role='冻结实际生成请求')]+([] if sid in ['CY024A5A','CY024A5B'] else [dict(path=prior,role='历史画面保留')])
 t.update(visual_prompt=row['prompt'],generation_request=req,editorial_review=dict(version='v047',status='candidate_pending_author_review',dynamic_execution='pending'))
 t.pop('final_static_review',None)
 with Image.open(R/path) as im: w,h=im.size
 t.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0,y=0,w=1,h=1),panel_index=0)
 images.append(dict(id=sid,path=path,sha256=sha(path),size=[w,h],request=req,request_sha256=sha(req),inputs=[dict(path=p,sha256=sha(p)) for p in row['refs']]))
elapsed=0
for i,t in enumerate(d['shots']):
 t.update(start_second=elapsed,end_second=elapsed+t['seconds']);elapsed+=t['seconds']
 if i+1<len(d['shots']): t['next_link']='接 '+d['shots'][i+1]['id']+'：'+d['shots'][i+1]['entry_state']
 if t['id'] in ['CY024A5','CY024A5A','CY024A5B','CY024B','CY024B3','CY024B1']: t['presentation']['visible']=t['action']
for sc in d['scenes']:
 ss=[t for t in d['shots'] if t['scene']==sc['id']]
 sc.update(shot_ids=[t['id'] for t in ss],seconds=sum(t['seconds'] for t in ss),pages=list(dict.fromkeys(t['presentation']['path'] for t in ss)),path=ss[0]['presentation']['path'])
d.update(version='v0.47',revision='v047',picture_revision='v047',title='《穿云》带图分镜 v0.47 · 三次瞄准与三柱清场',subtitle=f'{len(d["shots"])}镜 · {elapsed}秒 · 新图待作者审阅',total_seconds=elapsed,story_script='剧本/穿云-场景剧本-v0.47.md',source_manifest='镜头设计/生成记录/生成索引-v047.json',origin_manifest='镜头设计/shot-plan-v0.46.json',audio_arrangement='后期/三点定流-v047/预演编排.json',review_intro='GPT右食指依次点选教主、左翼、右翼；云中水柱逐一响应，三股清场水流都避开中央暗月罩。',review_focus='检查三次指向与一主两辅落点的对应，首点与后两点的节奏，以及清水余浪沿两侧接冲散教徒。新静帧待审，动态与正式音效未制作。',revision_notes=dict(previous_manifest='镜头设计/shot-plan-v0.46.json',added_ids=['CY024A5A','CY024A5B'],modified_image_ids=list(selected),boundary='A5原八秒及所有旧镜对白、时长和BGM候选保持；增两个1.5秒选点镜头，替换三柱大景，保留历史稿。'))
d['page_layouts']=[dict(path=t['presentation']['path'],rows=1,cols=1) for t in d['shots']]
script=re.sub(r'版本：v0\.46[^\n]*','版本：v0.47｜2026-10-24｜三次瞄准、一主两辅水雷与祭坛安全区，新图待审。',script,1).replace('## 暗月阻敌与控水协作 · v0.46','## 三点定流与控水协作 · v0.47')
assert len(d['shots'])==130 and elapsed==425.5
assert all(t['source_quote'] in script for t in d['shots'])
save(PLAN,d);write(d['story_script'],script)
save(d['source_manifest'],dict(version='v047',previous_index=old['source_manifest'],engine='built-in image_gen',mode='reference edit',transparent_background=False,images=images,discarded=[dict(path=IMG+'/CY024B-v047-r1.png',reason='大景手掌未收为食指且教徒近似列队，保留但不接入'),dict(path=IMG+'/CY024A5A-v047-r1.png',reason='头饰换侧，r2局部修正')]))
a=load(old['audio_arrangement']);a.update(version='v047-picture-sync',previous=old['audio_arrangement'],shot_plan=PLAN,shot_plan_sha256=sha(PLAN))
# Section endpoints automatically include the two inserted shots; no author marks are changed.
for sid in ['CY024A5','CY024A5A','CY024A5B','CY024B','CY024B3','CY024B1']: a['effects'][sid]=by[sid]['sound']
a['author_feedback']='原128镜BGM候选和作者标记保留；新增两个1.5秒选点镜沿用所属M09音乐段。首点、左点、右点分别接落水重音，仅声音设计，未自动替作者选曲。'
save(d['audio_arrangement'],a)
snapshot=R/'镜头设计/带图分镜-控水协作-v046.html';assert not snapshot.exists()
shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
t=read('scripts/build_storyboard.py').replace('shot-plan-v0.46.json','shot-plan-v0.47.json').replace('"v046")','"v046", "v047")').replace("'v046')","'v046','v047')")
t=t.replace('data.get("revision")=="v046"','data.get("revision") in ("v046","v047")')
write('scripts/build_storyboard.py',t)
e=read('00_打开项目.html').replace('v0.46','v0.47').replace('128镜422.5秒；6张协作救援修订候选待审','130镜425.5秒；4张三点定流修订候选待审').replace('128 镜 · 7 分 02.5 秒','130 镜 · 7 分 05.5 秒').replace('暗月阻敌与控水清场','三次瞄准与三柱清场')
write('00_打开项目.html',e)
progress='''## 2026-10-24：三次瞄准与三柱清场（v0.47，新图待审）

作者确认多股水柱配合ChatGPT手指逐点瞄准。A5保留原8秒咏唱，末字改右食指首点教主；新增A5A、A5B各1.5秒，右手依次转指左翼、右翼；B改一主两辅三股云中水雷。水来自云层，手指只指定目标，友方暗月罩与中央祭坛留有净空。三柱先收雷停水，外侧余浪接B3安全区、B3A罩内安抚、B1冲散教徒。后续原图可复用。

当前130镜425.5秒，4张当前修订图，6张生成结果含一张未采用大景和一张头饰修正旧稿。旧128镜时长、对白及音乐候选保留，新增两镜沿用相邻音乐段，不代替作者标记。v046页面、计划和原图完整保留。静帧待作者审阅；连续指向、逐柱响应与正式音效尚未制作。

'''
p=read('制作进度.md');pos=p.index('## 2026-10-24：');write('制作进度.md',p[:pos]+progress+p[pos:])
print(json.dumps(dict(shots=len(d['shots']),seconds=elapsed,images=len(images)),ensure_ascii=False))
