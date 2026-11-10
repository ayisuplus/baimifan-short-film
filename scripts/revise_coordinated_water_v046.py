"""Version the coordinated water rescue without changing music choices or dialogue."""
import copy,hashlib,json,re,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
PLAN='镜头设计/shot-plan-v0.46.json';REC='镜头设计/生成记录/控水协作-v046';IMG='镜头设计/图像/控水协作-v046'
def read(p):return (R/p).read_text('utf-8-sig')
def load(p):return json.loads(read(p))
def write(p,s):
 (R/p).parent.mkdir(parents=True,exist_ok=True);(R/p).write_text(s,encoding='utf-8')
def save(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
assert not (R/PLAN).exists(),'Preserve existing revision'
old=load('镜头设计/shot-plan-v0.45.json');d=copy.deepcopy(old);script=read(old['story_script'])
ct=copy.deepcopy(d['continuity'])
ct.update(
 claude_shield='Kimi循明刃瞬移震开柴堆后，祭坛两侧教徒转身施法。她以右暗刃闭合完全不透明的深靛暗月罩，包住两人、刑架和脚托，挡住教徒的琥珀色攻击法术及外侧残焰。先交代攻击来源，再拍法术撞罩碎散。罩施放后持续存在，双刃可收回后腰，Kimi空手照顾Claude。GPT主动控制水雷避开祭坛中央，水在接触暗罩前分成两路，留出罩外净空间隔；暗罩不抵抗友方水流。外景看不见罩内人物，内景只见平静暗膜；Kimi抱托安抚，不撑壁承压。确认安全后撤罩接钥匙。',
 kimi_fx='月下剪影→明刃破中央彩窗→钉外缘柴木→循刃瞬移回收明刃并爆气震柴→两侧教徒举手施法→右暗刃闭合暗月罩，琥珀色敌方法术在外壳碎散。罩面只在敌法命中处闪短促火星，内侧保持平静。GPT的银蓝水流在碰罩之前主动转向侧道，不撞罩、不压凹、不触发应力纹。罩内两刃收好，抱托、拭汗、查踝链；水声经过时轻扶后脑安抚。',
 water_impact_insert='主水雷扑灭罩外残柴与普通灯火。Kimi先震散木头并隔绝教徒攻击，GPT再控制侧流绕开暗罩；CY024B1拍同一批围攻教徒被厚重清水冲散、失足滑下侧阶，法杖脱手。长椅留作固定背景参照，不再掀走。历史CY024B2不接入镜序。',
 water_curtain='单根连续粗水雷柱正面撞击敌方教主暗金罩，撞击之前不分叉，紫电在水体内部盘绕。撞敌罩后形成侧流，GPT在水抵达友方暗月罩之前主动引向两侧通道，中央祭坛留出清楚净空；两种罩的受击关系不能混用。紫电先收尽，清水余浪冲散攻击暗罩的教徒。',
 water_volume='CY024A5高举掌心聚能，最后渊字才压掌；CY024B单柱重水攻击教主暗金罩。GPT控制后续巨量侧流提前避让暗月罩，水量与速度落在外侧教徒和燃木上。CY024B3两条厚水道与安稳中央祭坛同框；B3A罩内安抚；B1水没过教徒腰腹、冲断阵形并沿侧阶下行。不是细小水流，也不让人物飞天翻滚。',
 storm_release='GPT控制紫电只作用于主水柱及敌方教主暗金罩附近，不接触祭坛暗月罩、Claude束具或同伴。主动将侧流引向外围，给Kimi和Claude留出安全区；紫电先收尽，接清水冲散教徒、退水、对峙与变身。',
 support_roles='Kimi负责明刃定位瞬移、震柴、暗刃阻挡教徒法术、罩内照顾及战后钥匙解锁；GPT负责精确控制水雷，打击教主并让侧流提前绕开暗罩、冲散围攻教徒和灭掉外缘残柴。Perplexity警戒，千问抱护小鱼并保持原扇叶阻击。')
ct['wet_state']=ct['wet_state'].replace('暗月罩隔绝洪水与魔法雷','GPT主动将洪水与魔法雷引离祭坛中央安全区，暗月罩隔绝教徒法术及外侧残焰')
ct['claude_accessories']=ct['claude_accessories'].replace('暗月罩隔绝天瀑直冲','GPT主动留出祭坛中央安全区，水雷不冲向暗罩')
ct['claude_damage']=ct['claude_damage'].replace('暗月罩隔绝后续火焰、水雷伤害','暗月罩隔绝敌方法术与残焰，GPT控水雷避开两人')
repls={old['continuity'][k]:v for k,v in ct.items() if v!=old['continuity'][k]}
repls.update({'撞罩分流及冲椅退水':'撞击敌方金罩、侧流避开暗月及冲散教徒后退水','暗月罩隔绝天瀑直冲':'GPT主动留出祭坛中央安全区，水雷不冲向暗罩','覆盖Kimi与Claude的银白结界':'覆盖Kimi与Claude的不透明暗月罩','准备在落水后将靠近的侧浪与雷支流向外引开':'预先划出祭坛中央安全区，准备在侧浪抵达暗罩之前主动将水流引向两侧，雷支流也避开同伴'})
def rewrite(v):
 if isinstance(v,str):
  for a,b in repls.items():v=v.replace(a,b)
  return v
 if isinstance(v,list):return [rewrite(x) for x in v]
 if isinstance(v,dict):return {k:rewrite(x) for k,x in v.items()}
 return v
d=rewrite(d);script=rewrite(script);by={s['id']:s for s in d['shots']}
spec={
'CY024K3':dict(title='暗月闭合，截住教徒法术',framing='罩外低机位中远景，教徒施法源与命中点同框',action='祭坛两侧教徒已经举手施法，琥珀色光束朝Kimi与Claude逼近。Kimi退到Claude身前，右手暗刃向上划弧，深靛暗月罩迅速闭合，完整包住两人、刑架和脚托。关键帧停在敌方法术撞上外壳、碎成短促火星的一刻，画面两侧仍看得到教徒的施法手和法杖，攻击方向明确。暗罩完全不透明，外面看不到人物或十字架。所有燃木留在罩外，罩面完整；罩施放后持续存在，Kimi可以收刃照顾Claude。此时GPT尚未释放水雷。',entry_state='震柴惊动两侧教徒，他们抬手聚起法术，Kimi转身护住Claude。',exit_state='教徒第一轮攻击被暗罩截住，接罩内试镣；外侧仍有间歇攻击。',sound='教徒聚能尖鸣→两道破空法术→暗壳上的短促碎裂声；切入罩内后压成遥远闷响'),
'CY024B':dict(title='水雷清场，主动留出祭坛',framing='GPT侧后高位斜俯拍，敌方金罩主落点与远处友方安全区同框',action='镜头从空中ChatGPT侧后上方斜俯拍，近景膜翼、中景巨柱、远处祭坛构成纵深。苍龙雷渊轰穿中央中殿穹顶，一根连续、粗壮、直径大于教主护罩的银蓝水柱正面压向下段中央缓台的敌方暗金罩。主水柱撞敌罩前不分叉；紫电在厚水内部盘绕、被泡沫遮断并折射，主撞击炸开宽阔浪冠。GPT保持入口侧高空悬停，压掌之后微转手腕引流：奔向最高祭坛的侧流在抵达深靛暗月罩之前便主动分成左右两路，沿外围台阶奔涌，罩与水之间留出清楚的净空石面。暗罩安稳，没有被水顶开或压凹；罩外看不到两人与刑架。厚水扑灭外缘燃木、火盆、吊灯、壁烛及火把，并切断围攻教徒的站位。千问抱着小鱼留在右侧柱边的同伴安全位置。后殿拱顶完整，中央高窗破口保留，侧窗完整。镜末紫电先收尽，接两侧清水绕行与教徒被冲散；镜内不飞舞长椅、杂物或人物。',entry_state='GPT已确认暗罩阻住敌法，并预留祭坛中央安全区。',exit_state='敌方金罩承受主水柱，友方暗罩外围的水流已提前转向两侧，紫电收尽。',sound='主水柱撞击敌方金罩的轰鸣、巨量侧水奔流；友方暗罩处没有撞击或绷裂声'),
'CY024B3':dict(title='洪流分两侧，暗月安稳',framing='祭坛前方略高广角，两条水道与中央净空区同框',action='从祭坛前方看，GPT引导的厚重清水在暗月罩前方尚有明显距离时就分向左右，沿两侧石阶形成汹涌水道。中央通道和罩体周边留出完整净空石面，观众能连续看见水的转向位置、间隔和安稳的深靛暗罩。罩面不被水接触，没有压痕、银色应力纹或罩顶瀑布，紫电已经收尽。外围散柴被浇灭带向下方，水流转向刚才施法的教徒；中央破窗保留，侧窗完整，所有普通灯火熄灭。',entry_state='GPT已主动引流，主水柱紫电收尽，厚水进入祭坛两侧。',exit_state='水经过外围，中央安稳，切罩内安抚，再接外侧教徒失足。',sound='左右两侧持续重水奔流；中央没有冲罩音，切罩内时轰鸣自然变闷'),
'CY024B3A':dict(title='外面水声经过，里面靠肩安抚',framing='罩内双人中近景，扶后脑、靠肩与腕扣同框',action='罩内只传来隔远的水声。Claude听见外面轰鸣，疲惫地靠近Kimi；Kimi一只空手轻扶她的后脑，另一臂托住肩背与上臂，额侧贴近，以安稳的神情让她慢慢松下紧张。Claude仍直立受缚，双腕固定在横木，双踝与脚托没有变化；双刃都已收在Kimi后腰。暗膜内侧平静、不透明，没有水压凹痕、应力闪光或外景。Kimi不用手撑墙，也没有对抗GPT法术的吃力表情。',entry_state='GPT让水流绕过祭坛，Kimi已从踝链旁起身靠回Claude。',exit_state='Claude靠肩缓下来，接罩外同一批教徒被清水冲散。',sound='隔膜后的低沉水声、轻柔衣料与呼吸；不出现撑膜、碎裂或吃力喘息'),
'CY024B1':dict(title='洪流冲散围攻教徒',framing='外侧台阶低机位，近景教徒失足、远景暗罩安稳',action='镜头落到祭坛外侧台阶，刚才围攻暗罩的黑金袍教徒察觉水流转来，仓促转身抬手防御，持续攻击被迫中断。厚重清水撞散阵形，淹过腰腹，脚下失去支点；前排一人伸手抓石沿却滑开，后排数人随水沿侧阶向下滑走，一根法杖脱手落在水面。人物有重量，部分身体被厚水遮住，不飞天翻滚，不表现撞伤细节。远景暗月罩稳立中央净空平台，水从两侧经过，罩与水保持间隔。后墙的小长椅仍落在原位作为固定参照，中央彩窗破口保留，侧窗完整，壁烛已灭；这股清水没有魔法雷。',entry_state='GPT引导清水沿祭坛侧道逼近原先施法的教徒，紫电已收尽。',exit_state='围攻阵形瓦解、教徒沿外阶被冲散，接水源停止后的退水与GPT降落。',sound='敌方法术戛然而止、教徒短促惊呼、厚水拍石、法杖落水及衣袍拖水声；不再突出木椅翻转')
}
for sid,changes in spec.items():
 s=by[sid];before=s['source_quote'];assert before in script,sid
 script=script.replace(before,changes['action']).replace(s['title'],changes['title'])
 s.update(changes,source_quote=changes['action'],purpose='明确'+changes['title']+'，体现GPT清场与Kimi守护的分工。',cinematic_beats=[dict(offset=0,intent=changes['action'].split('。')[0])])
 s['presentation']['visible']=s['action'];s.pop('final_static_review',None)
n=copy.deepcopy(by['CY024K3']);n.update(id='CY024K2A',title='震柴惊动教徒，转身施法',seconds=2,dialogue='无对白',dialogue_cues=[],entry_state='Kimi循刃震开柴堆，两侧教徒仍在祭坛边。',exit_state='教徒攻击即将发出，Kimi抬起右暗刃，接闭罩拦截。',framing='侧前低机位，黑袍教徒前景夹住后方Kimi与Claude',purpose='先展示敌人和施法方向，为暗罩的用途建立因果。')
n['action']='柴堆被震开，祭坛两侧的黑金袍教徒转身围向中央。近景有人抬起空手，有人举杖，琥珀色火星在掌心和杖端收拢，攻击方向朝向后方Kimi与Claude。Kimi尚未闭罩，压低重心转向攻击者，右暗刃抬起，左明刃保持在身体外侧；Claude直立受缚，腕踝锁扣和固定脚托不变。人物分处散柴外侧通道与中央净空区，互不穿过火堆。'
n['sound']='重柴滚落尾音、黑袍急转脚步、教徒掌心与杖端聚能；不新增对白';n['source_quote']=n['action'];n['cinematic_beats']=[dict(offset=0,intent='教徒转身，抬手聚能'),dict(offset=1,intent='Kimi察觉，抬暗刃')]
for k in ['subtitle_cues','dialogue_timing_status','final_static_review']:n.pop(k,None)
i=d['shots'].index(by['CY024K2']);d['shots'].insert(i+1,n);by[n['id']]=n
script=script.replace(by['CY024K2']['source_quote'],by['CY024K2']['source_quote']+'\n\n'+n['source_quote'])
# Carry the enemy assault into the quiet interior through sound; existing dialogue is unchanged.
s=by['CY024A1'];before=s['source_quote'];s['action']=s['action'].replace('Kimi听向罩外雷声','Kimi听向罩外教徒法术的闷响与远处雷声');s['source_quote']=before.replace('Kimi听向罩外雷声','Kimi听向罩外教徒法术的闷响与远处雷声');script=script.replace(before,s['source_quote']);s['presentation']['visible']=s['action'];s['sound']='承前GPT咏唱、衣料与缓慢呼吸；教徒法术撞罩声隔远成闷响，远处雷声逐渐增强'
# Bind the six edited/new images, retain every old candidate.
requests=load(REC+'/实际请求-r1.json');fix=load(REC+'/中央破窗修正-r2.json');requests.append(fix)
selected={x['id']:x for x in requests};images=[]
for sid,row in selected.items():
 s=by[sid];prior=s['presentation']['path'];path=f'{IMG}/{sid}-v046-r{row["rev"]}.png';req=REC+('/中央破窗修正-r2.json' if row['rev']==2 else '/实际请求-r1.json')
 s['presentation'].update(path=path,visible=s['action'],status='v0.46协作救援修订候选，待作者画面审阅',missing='静帧已查看；敌法轨迹、控水提前绕行、人体随水失衡和跨镜动作仍待动态验证。')
 s['refs']=[dict(path=path,role='本轮修订候选'),dict(path=req,role='实际生成请求')]+([] if sid=='CY024K2A' else [dict(path=prior,role='历史画面保留')])
 s.update(visual_prompt=row['prompt'],generation_request=req,editorial_review=dict(version='v046',status='candidate_pending_author_review',dynamic_execution='pending'))
 with Image.open(R/path) as im:w,h=im.size
 s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0,y=0,w=1,h=1),panel_index=0)
 images.append(dict(id=sid,path=path,sha256=sha(path),size=[w,h],request=req,request_sha256=sha(req),inputs=[dict(path=p,sha256=sha(p)) for p in row['refs']]))
# Clear derived next-links and rebuild every timing and scene index once.
elapsed=0
for i,s in enumerate(d['shots']):
 s.update(start_second=elapsed,end_second=elapsed+s['seconds']);elapsed+=s['seconds']
 if i+1<len(d['shots']):s['next_link']='接 '+d['shots'][i+1]['id']+'：'+d['shots'][i+1]['entry_state']
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']];sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)),path=ss[0]['presentation']['path'])
d.update(version='v0.46',revision='v046',picture_revision='v046',title='《穿云》带图分镜 v0.46 · 暗月阻敌与控水清场',subtitle=f'{len(d["shots"])}镜 · {elapsed}秒 · 新图待作者审阅',total_seconds=elapsed,story_script='剧本/穿云-场景剧本-v0.46.md',source_manifest='镜头设计/生成记录/生成索引-v046.json',origin_manifest='镜头设计/shot-plan-v0.45.json',audio_arrangement='后期/控水协作-v046/预演编排.json',review_intro='教徒施法围攻，暗月罩挡住敌法；GPT控制巨量水流提前绕开暗罩、冲散教徒。罩外清场，罩内靠肩安抚。',review_focus='检查敌方攻击来源、主水柱攻击教主金罩与侧流主动避让暗月的区别，以及教徒被冲散、罩内安抚的接续。新静帧候选待审，动态及正式音效未制作。',revision_notes=dict(previous_manifest='镜头设计/shot-plan-v0.45.json',added_ids=['CY024K2A'],modified_image_ids=list(selected),boundary='替换友方对抗误读；新增两秒攻击来源，旧镜对白时长与BGM候选保留；静帧候选待作者审阅。'))
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
script=re.sub(r'版本：v0\.45[^\n]*','版本：v0.46｜2026-10-24｜暗月阻敌与GPT控水清场，罩内安抚。新图待审。',script,1).replace('## 暗月瞬临连续性 · v0.45','## 暗月阻敌与控水协作 · v0.46')
assert all(s['source_quote'] in script for s in d['shots'])
save(PLAN,d);write(d['story_script'],script)
save(d['source_manifest'],dict(version='v046',previous_index=old['source_manifest'],engine='built-in image_gen',mode='reference edit',transparent_background=False,images=images,discarded=[dict(path=IMG+'/CY024B-v046-r1.png',reason='侧窗误破，r2恢复侧窗并保留中央破口')]))
a=load(old['audio_arrangement']);a.update(version='v046-picture-sync',previous=old['audio_arrangement'],shot_plan=PLAN,shot_plan_sha256=sha(PLAN))
# New two-second enemy reaction inherits exactly the neighboring K3 candidates.
a['shot_overrides']['CY024K2A']=copy.deepcopy(a['shot_overrides']['CY024K3'])
for sid in list(selected)+['CY024A1']:
 a['effects'][sid]=by[sid]['sound']
 if sid in a['shot_overrides']:a['shot_overrides'][sid]['note']='沿用既有候选；当前动作：'+by[sid]['title']
a['author_feedback']='保留原127镜候选BGM及本机选择；新增CY024K2A沿用K3候选，不自动选定。改为敌方法术撞罩、GPT主动引流、教徒失衡落水，声音目前仅设计。';save(d['audio_arrangement'],a)
snapshot=R/'镜头设计/带图分镜-暗月瞬临-v045.html';assert not snapshot.exists();shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
t=read('scripts/build_storyboard.py').replace('shot-plan-v0.45.json','shot-plan-v0.46.json').replace('"v045")','"v045", "v046")').replace("'v045')","'v045','v046')")
t=t.replace('"CY024K2","CY024K3"','"CY024K2",*(["CY024K2A"] if data.get("revision")=="v046" else []),"CY024K3"').replace("data.get('revision') == 'v045'","data.get('revision') in ('v045','v046')")
write('scripts/build_storyboard.py',t)
e=read('00_打开项目.html').replace('v0.45','v0.46').replace('127镜420.5秒；17张修订候选待审','128镜422.5秒；6张协作救援修订候选待审').replace('暗月瞬临与罩内抱护','暗月阻敌与控水清场').replace('127 镜 · 7 分 00.5 秒','128 镜 · 7 分 02.5 秒').replace('巨浪中抱护撑罩','控水绕行时靠肩安抚').replace('暗刃闭合不透明月罩','暗刃闭罩挡敌法').replace('明刃破窗、瞬移震柴、罩内抱护','暗月阻敌、控水避让、洪流冲散教徒');write('00_打开项目.html',e)
assets=read('资产/assets.json').replace('暗月罩隔绝天瀑直冲','GPT主动留出祭坛中央安全区，水雷不冲向暗罩');write('资产/assets.json',assets)
progress='''## 2026-10-24：暗月阻敌与控水清场（v0.46，新图待审）

作者确认护罩主要挡祭坛周围教徒的法术，GPT能精确控制水雷，主动绕开友方暗罩；原冲椅镜改为冲散围攻教徒。新增CY024K2A两秒交代教徒转身施法，K3敌法命中罩面；B保留主水柱攻击教主金罩，侧流提前避开暗月；B3展示两路洪流与中央安全区，B3A改靠肩扶后脑安抚，B1改群体教徒失足沿侧阶被水带走。长椅只作固定背景。原127镜对白、时长及候选BGM保留，新镜沿用相邻候选而不代选。

当前128镜422.5秒，6张当前修订图，7张生成结果含一张侧窗误破的历史稿。主剧本、连续性、动作声音与预演入口同步；v045旧页及原图保留。静帧待作者审阅，未制作连续动态、正式音效或新配音。

'''
p=read('制作进度.md');pos=p.index('## 2026-10-24：');write('制作进度.md',p[:pos]+progress+p[pos:])
print(json.dumps(dict(shots=len(d['shots']),seconds=elapsed,images=len(images)),ensure_ascii=False))
