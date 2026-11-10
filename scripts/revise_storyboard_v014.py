"""Build v0.14 from immutable v0.13 and reviewed independent image edits."""
import json, shutil, hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def read(p):return json.loads((root/p).read_text(encoding='utf-8'))
def write(p,d):(root/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
d=read('镜头设计/shot-plan-v0.13.json')
script=(root/d['story_script']).read_text(encoding='utf-8')
space='祭坛中央彩窗、十字架与多段宽长阶共用中轴。长阶经缓台通往最高平整平台，Claude固定于顶端刑架；以CY012-v014-r5母版为准。固定建筑和灯具左右对称，下、中、上各一对低铜火盆共六只；中殿圣灯左右一对、同高度同进深；下段左右对应石座各一支蜡烛。人物行动与战损不要求镜像。'
light='天瀑前六火盆、两圣灯和两蜡烛提供暖光，蓝紫彩窗月光勾勒Claude；顶部刑架低柴到CY022才点燃。CY024B后全部普通灯火及低柴彻底熄灭，无红炭、无暖色灯点，照明来自中殿破顶、彩窗和门口冷月光。后殿拱顶完整。护罩、变身和战斗仅提供局部魔法光；CY028B起Claude掌火，CY029B起空刑架剧情火焰可提供暖光，普通灯具直到离殿不复燃。'
route='宝宝登顶尝试开锁，随后冲下长阶，在下段地面阻拦教徒与教主。第一火把落在面向祭坛的下段右火盆。教主接第二火把登顶点柴，然后返回下段缓台；天瀑与对峙期间站位不变。GPT在下层中殿、千问抱宝宝在侧柱边。战后GPT与Perplexity登顶解锁，Claude施法脱力后被公主抱；省略下阶过程后，十二位核心角色于下层中殿汇合离开。'
repl=[
('版本：v0.13','版本：v0.14'),
('低台祭坛上','高处祭坛上'),
('祭坛从大殿地面到顶端平台只有三级宽石阶，平台四周同高，不再另设侧梯或后梯。','中央长阶经缓台通向高处祭坛，Claude与刑架位于顶端平整平台；阶梯、缓台和栏杆沿用当前母版。'),
('两个相同的铜火盆对称放在祭坛最下一级台阶外的左右地面，中央通道留空。','长阶下、中、上各设一对低铜火盆，共六只；每对同高度、同进深、左右对称，中央通道留空。中殿圣灯左右等高对称悬挂一对；下段两侧对应石座各一支蜡烛。'),
('小鱼沿左侧长椅旁的阴影走到祭坛，爬完三级宽石阶','小鱼沿左侧阴影走到长阶，省略途中登阶'),
('急切地沿三级石阶冲下','急切地沿多段长阶冲到最下段'),
('持火者继续走向柴薪。','持火者在长阶下段右侧准备登阶。'),
('四周的蜡烛也仍然燃着','三对火盆、对称圣灯与两支蜡烛仍然燃着'),
('DeepSeek 乘机跑回 Claude 身前，张开双臂。','DeepSeek 转到长阶下端中央，张开双臂挡住通往 Claude 的路，没有再次登顶。'),
('教主接过火把后走向柴薪，继续迈步','教主接过火把后踏上长阶，继续迈步'),
('教主把第二支火把探向低柴堆，将木柴引燃后收回，仍握在手中。','省略途中攀登，教主已到顶部平台，把第二支火把探向低柴堆，将木柴引燃后收回。小鱼仍远在长阶下端。镜尾教主转身开始下阶。'),
('千问从她身侧跑向阶下的小鱼，Perplexity 在右侧举杖，蓝光先到祭坛','千问跑向长阶下端的小鱼，Perplexity 在右侧举杖，蓝光先到高处祭坛'),
('教主在她前方、祭坛下的中央地面','教主已返回她前方长阶下段的中央缓台'),
('远处才是三级低台祭坛。','远处多段长阶通向高祭坛，Claude仍在最高平台。'),
('众人确认阻碍解除，才走向后殿祭坛。','确认阻碍解除，GPT与Perplexity走向中央长阶并踏上首阶。'),
('战斗已经结束。Perplexity 先打开','省略登阶过程，GPT与Perplexity已经来到顶部祭坛。Perplexity 先打开'),
('ChatGPT 登上祭坛，扶住 Claude。','已在顶部平台的ChatGPT扶稳Claude。'),
('抱着她转向出口，没有再将她放下。','在顶部平台抱着她转向下行长阶，始终没有将她放下。'),
('众人护着她们走向门外。','省略下阶过程，GPT抱着Claude来到下层中殿，与千问抱宝宝的队伍汇合，众人护着她们走向门外。'),
('一滴烛泪沿旧蜡痕缓缓滑落','下段左侧石座上那支蜡烛，一滴烛泪沿旧蜡痕缓缓滑落'),
('三级低宽石阶接一个平平台','多段宽长阶经缓台通向高处平平台'),
('三级低台祭坛','长阶顶端高祭坛'),
('三级石阶','多段长阶'),
('三级宽石阶','多段宽长阶'),
('跑下三阶','跑下长阶'),
('冲下三阶','冲下长阶'),
('两只火盆及殿内全部蜡烛与火把','三对铜火盆、两盏圣灯、两支蜡烛及殿内火把'),
('双火盆','三对火盆'),
('两只火盆','三对火盆'),
('两盆','六只火盆'),
('右侧火盆','长阶下段右侧火盆'),
('右侧炭火盆','长阶下段右侧炭火盆'),
('祭坛右侧火盆','长阶下段右侧火盆'),
]
def tx(v):
 if isinstance(v,str):
  for a,b in repl:v=v.replace(a,b)
  return v
 if isinstance(v,list):return [tx(x) for x in v]
 if isinstance(v,dict):return {k:tx(x) for k,x in v.items()}
 return v
original_notes=script.split('## 制作交接备注',1)[1]
repl += [('赤足三阶祭坛','赤足高祭坛与多段长阶'),('低柴与两火盆全灭','顶部低柴及六火盆、两圣灯、两蜡烛等普通灯火全部熄灭'),('火盆在阶下左右','火盆沿长阶下、中、上三对对称布置'),('持火者向柴薪靠近','持火者在长阶下段右侧准备登阶'),('持火者奔向柴薪','持火者在长阶下段右侧准备登阶'),('持火者由祭坛右侧靠近低柴','持火者在长阶下段右侧准备登阶')]
space=space.replace('Claude固定于顶端刑架','刑架固定于顶端平台，解救前Claude受缚于刑架')
script=tx(script)
script=script.split('## 制作交接备注',1)[0]+'## 制作交接备注'+original_notes+'\n\n- v0.14 当前决定：多段长阶替代旧低台，三对火盆、一对等高悬灯与两支蜡烛全部对称；天瀑后普通灯火全灭。上文版本条目保留历史事实，不覆盖本版正文及空间规则。\n'
d=tx(d)
script=script.replace('## S01｜','## 教堂空间与光源 · v0.14\n\n'+space+'\n\n'+light+'\n\n'+route+'\n\n## S01｜',1)
(root/'剧本/穿云-场景剧本-v0.14.md').write_text(script,encoding='utf-8')
d.update(title='《穿云》带图分镜 v0.14',version='v0.14',revision='v014',created='2026-10-22',story_script='剧本/穿云-场景剧本-v0.14.md',origin_manifest='镜头设计/shot-plan-v0.13.json',subtitle='对称长阶圣殿、天瀑熄灯与上下阶连续性')
d['continuity'].update(church=space,lighting=light,magic=light+' 教主固定在GPT前方下段缓台撑暗金护罩。',obstruction=route,torches='第一支火把固定落在面向祭坛时长阶下段右侧铜火盆中；教主接第二支火把后登顶，点燃刑架低柴，再返回下段缓台。')
d['continuity']['doors']=d['continuity']['doors'].replace('CY017队尾关门落闩','CY016D—CY017期间正门已经落闩')
d['review_intro']='教堂固定为对称多级长阶、三对火盆、一对等高圣灯与两支对称蜡烛；天瀑后普通灯火全灭。高处Claude、下层阻拦、登顶解锁与抱持离殿路线统一。'
d['review_focus']='重点连看CY012—022上下阶、CY024B—027A天瀑与对峙、CY027F—030登顶解锁及离开。近景画外光不代表灯具移到人物身后；静帧不能证明连续动作已经完成。'
d['roughcut_preview_label']='旧版静帧配乐v002（69镜239秒，未包含v0.14改图；Victory决定保留）'
records=read('镜头设计/生成记录/天瀑空间-v014/结果映射.json')
choices=read('镜头设计/生成记录/天瀑空间-v014/采用映射.json')
selected={r['id']:r for r in records if choices.get(r['id'])==r['take']}
assert len(selected)==len(choices)
d['masters']=[m for m in d['masters'] if not m['id'].startswith('M-ALTAR')]
d['masters'].append({'id':'M-ALTAR-v014','title':'对称多级长阶与光源母版','path':selected['CY012']['destination'],'role':space,'status':'本轮采用母版，待作者整片审阅','limits':light+' 旧低台母版保留于历史图册，不再用于当前镜头。'})
d['masters'].append({'id':'M-ALTAR-POST-v014','title':'天瀑后破顶与全灭照明','path':selected['CY027']['destination'],'role':light,'status':'本轮战后参考','limits':'只采用破顶范围、熄灯状态和站位关系，动态水流及退水待视频制作。'})
actions={
'CY012':'宝宝在下层抬头看见长阶顶端受缚的Claude，沿左侧阴影靠近中央长阶，镜尾开始登阶。',
'CY016A':'宝宝在顶部平台暂时垂下双手、低头喘气；用她疲惫的近景表现多次尝试后的消耗，Claude在画外。',
'CY016A1':'面向祭坛时下段左侧石座的单支蜡烛，烛泪沿旧痕滑落；背景不再有烛阵。',
'CY016C':'从顶部祭坛向下望过长阶与中殿，提灯教徒由远处正门返回，沿下层中央通道走向长阶下端。',
'CY016D':'宝宝松开未打开的锁，沿中央长阶冲下，镜内表现末段下行，奔向下段右侧持火者。',
'CY017':'宝宝在长阶下端短暂半跪后撑起；持火者仍在下段右侧准备登阶；正门已经落闩。',
'CY018':'宝宝撞偏持火者手臂，第一支火把跌入长阶下段右铜盆的炭块间，迸出火星。',
'CY019':'宝宝转到长阶下端中央张臂挡路，Claude仍远在最高平台；宝宝没有重新登顶。',
'CY020A':'宝宝被推倒在长阶下端同一片地面，无力再次起身。',
'CY021':'宝宝在长阶下端撑地失败，望向身旁教主的袍尾。',
'CY021A':'教主在长阶下端接牢第二支火把，迈向上行阶梯；第一火把留在下段右盆。',
'CY022A':'教主踏上长阶，袍尾从宝宝指间滑脱；宝宝留在下端，省略攀登接顶部点柴。',
'CY022':'教主已登到顶部平台，用第二支火把点燃刑架低柴；宝宝远在下端、在本镜画外。镜尾教主转身下阶。',
'CY024B':'天瀑轰穿中殿穹顶，水墙扑灭全部普通灯火和顶部低柴，冲散教徒。教主已回到GPT前方下段中央缓台，开暗金护罩原地抵挡；千问抱宝宝在右侧柱边。',
'CY027':'水流排出，GPT在下层中殿走近；教主留在中央下段缓台，双方隔低处短阶对峙，Claude仍远在最高平台。',
'CY027A':'GPT在左侧近处，教主正前方下段缓台拦路；两人在破碎穹顶下对话，保持天瀑镜的前后关系。',
'CY027F':'战后教主与教徒全倒地，九位同伴齐全，千问抱宝宝；GPT恢复人形，和Perplexity踏上长阶，准备登顶解锁。',
'CY029A':'Claude主动搭肩；GPT保持托背、托膝，在顶部平台抱着她转向下行长阶，始终不放下。',
'CY030':'省略下阶，GPT抱Claude已到下层中殿，与千问抱宝宝的队伍汇合，十二位核心角色沿通道离开；骑士留守。',
}
for s in d['shots']:
 sid=s['id']
 if sid in actions:s['action']=actions[sid]
 if s['scene'] in ('S03','S04','S05') and not sid.startswith('CY026'):
  s['invariants']=[v for v in s['invariants'] if not any(w in v for w in ('祭坛只有','铜火盆','天瀑后殿内全部','两只铜','三级','三阶'))]
  s['invariants']+= [space,light,route]
 if sid=='CY015':s['entry_state']='省略登阶，小鱼已到顶部平整平台，站在木架左侧。'
 if sid=='CY016A':s['framing']='宝宝疲惫的上半身近景';s['exit_state']='宝宝缓口气，仍未打开锁，接听到门外脚步。'
 if sid=='CY016D':s['purpose']='交代主动下阶拦截，非被拖下或跌落。'
 if sid=='CY018':s['framing']='长阶下段右侧中景／持火者与炭火盆同框'
 if sid=='CY021':s['purpose']='表现宝宝无力起身，转而抓住身旁教主的袍尾。'
 if sid=='CY021B':s['sound']='攥紧衣料的摩擦声与宝宝喘息；没有穿云信号。'
 if sid=='CY027':s['purpose']='建立GPT在下层、教主在下段缓台、Claude在最高平台的关系。'
 if sid=='CY022':s['entry_state']='省略途中登阶，教主已到顶部平台，宝宝仍留在下端。';s['exit_state']='低柴已燃，教主转身开始下阶；Claude仍受缚。'
 if sid=='CY027A':s['exit_state']='双方保持破顶下对峙，接GPT回应。'
 if sid=='CY027F':s['exit_state']='GPT与Perplexity踏上首阶，省略途中登顶，接解踝链。'
 if sid=='CY027F1':s['entry_state']='GPT与Perplexity已登到顶部祭坛，Claude仍受束，先解踝链。'
 if sid=='CY030':s['entry_state']='省略下阶，GPT仍抱Claude，与下层同伴汇合。'
 if sid in selected:
  r=selected[sid];previous=s['presentation']['path']
  s['presentation']={'path':r['destination'],'role':'action','visible':s['action'],'status':'v0.14空间与照明修订，待作者整片审阅','missing':'静帧表达代表状态；连续运动、灯火熄灭过程与正式声音待动态制作。','show_as_main':True}
  s['visual_prompt']=r['input']['prompt'];s['generation_request']=r['request']
  s['refs']=[{'path':r['destination'],'role':'本轮独立镜头修订'},{'path':r['request'],'role':'冻结实际输入'},{'path':previous,'role':'保留的上一版'}]
  s['editorial_review']={'version':'v014','status':'candidate_static_review','dynamic_execution':'pending'}
  s['panel_index']=0;s.pop('display_crop_normalized',None)
 s['presentation']['visible']=s['action']
for i,s in enumerate(d['shots']):
 s['next_link']='接 '+d['shots'][i+1]['id']+'：'+s['exit_state']+' → '+d['shots'][i+1]['entry_state'] if i+1<len(d['shots']) else '结束。'
for sc in d['scenes']:
 group=[s for s in d['shots'] if s['scene']==sc['id']]
 sc['pages']=list(dict.fromkeys(s['presentation']['path'] for s in group));sc['path']=sc['pages'][0]
d['page_layouts']=[{'path':s['presentation']['path'],'rows':1,'cols':1} for s in d['shots']]
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.13.json',previous_html='镜头设计/带图分镜-v0.13.html',added_ids=[],repurposed_ids=['CY016A'],boundary=f'{len(selected)}镜独立改图，89镜286秒不变。多级长阶替代旧低台；对称灯具，天瀑后全灭。旧配乐粗剪未重导；原件、历史候选及冻结输入保留。')
assert len(d['shots'])==89 and sum(s['seconds'] for s in d['shots'])==286
missing=[s['id'] for s in d['shots'] if s['source_quote'] not in script]
assert not missing,missing
archive=root/'镜头设计/带图分镜-v0.13.html'
if not archive.exists():shutil.copy2(root/'镜头设计/带图分镜.html',archive)
write('镜头设计/shot-plan-v0.14.json',d)
assets=read('资产/assets.json')
snap=root/'资产/assets-v0.13.json'
if not snap.exists():shutil.copy2(root/'资产/assets.json',snap)
for a in assets['assets']:
 if a['id']=='ENV-CHURCH':
  a['previous_path']=next(x['path'] for x in read('资产/assets-v0.13.json')['assets'] if x['id']=='ENV-CHURCH');a['path']=selected['CY012']['destination'];a['name']='教堂 · 对称多级长阶与光源母版'
  a['role']=space+' '+light
  a['limits']='空间与灯具参考含剧情人物；战后参考CY027-v014。侧反机位按透视与遮挡，不硬塞全部灯具。旧低台资产仅历史参考。'
write('资产/assets.json',assets)
audit=[]
for r in records:
 p=root/r['destination'];original=Path(r['original'])
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 assert digest==hashlib.sha256(original.read_bytes()).hexdigest()
 audit.append({'id':r['id'],'take':r['take'],'path':r['destination'],'original':r['original'],'sha256':digest,'status':'current-candidate' if choices.get(r['id'])==r['take'] else 'superseded-preserved'})
write('镜头设计/生成记录/天瀑空间-v014/归档校验.json',audit)
print(f'v014: {len(selected)} images selected; {len(audit)} originals verified; 89 shots, 286 seconds')
