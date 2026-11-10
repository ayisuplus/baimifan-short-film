"""One-time scoped revision: charging gesture, single torrent, heavier surge."""
import copy, hashlib, json, shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
def read(p): return (R/p).read_text(encoding='utf-8-sig')
def write(p,s): (R/p).write_text(s,encoding='utf-8')
def save(p,d): write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert not (R/'镜头设计/shot-plan-v0.38.json').exists()
o=json.loads(read('镜头设计/shot-plan-v0.37.json'));d=copy.deepcopy(o)
by={s['id']:s for s in d['shots']}; script=read(o['story_script'])
rec='镜头设计/生成记录/蓄力与水雷-v038'
sources={'CY024A5':'exec-4d8a2435-7b46-4852-b04d-7ac58c0c3c5f.png','CY024B':'exec-f5aa9b05-54db-4e19-a4d6-d964873ae54a.png','CY024B1':'exec-ed702e6c-2fa8-43d5-a3eb-39a27e596dc8.png'}
a=by['CY024A5'];old=a['source_quote']
a['source_quote']=old.replace('面部和施法手占主体，肩后可见缓慢扇动的膜翼','面部、高举的施法手与掌上凝聚的水雷光团占主体，肩后可见缓慢扇动的膜翼').replace('她垂眼，确认','她短暂垂眼，确认').replace('她收拢手指，语气从低沉的呼唤转为坚定的祈愿；','她将右臂举过头顶，掌心向上，另一只手在胸前稳定术式。上浮水珠在高举的掌心上方收拢成紧密旋转的水团，紫电藏在水层内部明灭；手臂与肩背绷住，双翼持续维持悬停。她抬眼注视聚能处，力量仍在压缩，没有提前下放。语气从低沉的呼唤转为坚定的祈愿；').replace('手掌随最后一个字翻下','高举的手掌直到最后一个“渊”字才翻转压下，将蓄积引向主落点；掌上光团是控制与聚能的节点，巨型水柱仍来自屋顶上空的螺旋乌云，并非从掌心直接喷出')
assert old in script;script=script.replace(old,a['source_quote'],1)
a.update(framing='空中侧前方中近景／面部、高举聚能手掌与肩后膜翼',action='GPT振翼悬停，右手举过头顶、掌心向上汇聚紧密旋转的水雷光团，另一手在胸前稳定术式；肩臂绷紧持续蓄力，最后一个“渊”字才翻掌压下。',exit_state='聚能保持至招式名末字，压掌触发云中单根粗水雷柱；切高位斜俯拍。',next_link='接CY024B：压掌落点接单柱撞罩；GPT留在主水柱侧前方安全区。')
a['invariants'].append('本镜主图为蓄力保持状态：右手高举掌心向上，左手在胸前稳术；报招末字才压掌，不提前释放。掌上水团控制云中聚水，不作为巨型水柱的出水口。')
a['cinematic_beats']=[dict(offset=0,intent='短暂确认保护，右臂上举，掌上聚水'),dict(offset=2.4,intent='高举掌心持续凝聚水雷，肩臂绷住，祈愿'),dict(offset=5,intent='音乐骤收0.8秒，保持蓄力'),dict(offset=5.8,intent='报招，最后渊字才翻掌压下接云中水雷')]
b=by['CY024B'];old=b['source_quote']
b['source_quote']=old.replace('厚重连续的银白水幕覆盖中后景，主水体向下倾泻，主水体旋卷成相互缠绕的液流，紫电沿液流内部的涡旋螺旋穿行；','一根粗壮、连续、直径明显大于教主护罩的银白水柱占据中后景，正对下段中央缓台的暗金护罩倾泻。撞罩之前只有一个完整水体，不并列分叉；柱心直接压到罩顶，水体随后顺罩面摊开，炸出宽阔的环状浪冠并沿两侧与台阶奔流。主水体持续向下，紫电沿柱内涡旋盘绕向上；').replace('水仍是画面主体，落地激起宽阔水浪。','水仍是画面主体，撞罩分流后形成厚重的地面洪浪。')
assert old in script;script=script.replace(old,b['source_quote'],1)
b.update(title='单柱水雷，撞罩分流',purpose='用单根粗柱压向暗金罩、撞击后才分流的因果，读出水雷体量与教主承压。',action='一根粗水雷柱从上方直压教主暗金罩；紫电沿柱内涡旋盘绕，与向下的液流交织。柱心撞上罩顶才炸成环状浪冠，沿罩面与台阶向外分流；GPT在左侧高空引流，末段紫电先收。',exit_state='主落水停止，魔法紫电先收尽；撞罩后的厚重清水余浪继续扑向最高祭坛后墙左侧。',next_link='接CY024B1：失去紫电的厚浪掀走左后墙长椅，所有普通灯火已灭。')
b['invariants'].append('只设一根宽于暗金护罩的连续水柱；罩顶接触前不分成两柱，接触后才环状炸开并向侧面分流。水向下、紫电沿柱内涡旋盘绕向上，二者同处一水体。')
b['cinematic_beats']=[dict(offset=0,intent='渊字接单根水雷柱破顶重音'),dict(offset=1,intent='俯拍单柱撞暗金罩，罩顶才分流，GPT在左侧安全区'),dict(offset=3.8,intent='紫电先收，主落水终止，厚重清水余浪接长椅')]
c=by['CY024B1'];old=c['source_quote']
c['source_quote']=old.replace('水浪沿平台扑来，撞上此前靠墙摆放的深色木长椅。','撞罩后奔向此处的清水余浪沿平台扑来，浪身厚重、浪冠高过椅背，连续水体挤满中后景，撞上此前靠墙摆放的深色木长椅。').replace('椅脚先滑过湿石，一端被掀离原位，椅身转向平台前缘；','厚浪淹过椅脚与部分座面，椅脚先滑过湿石，一端被掀离原位，椅身转向平台前缘；').replace('被水带向同一方向。','腰腹被厚水遮住，被水带向同一方向，兜帽头部与抓空的手仍清楚可见。宽厚水层持续从石台边缘翻下。')
assert old in script;script=script.replace(old,c['source_quote'],1)
c.update(action='厚重清水浪冠高过椅背，淹没椅脚与部分座面，将原款长椅掀起、推向平台前缘；教徒腰腹被水遮住，抓空的手与头部仍可见。整片水层从台阶边缘翻下，壁烛熄灭。',entry_state='单柱撞罩分流形成的厚重清水余浪已冲上最高祭坛左后墙；紫电收尽。',exit_state='厚浪带偏长椅与教徒，流出台阶边缘；接水源停止后的退水镜。')
c['invariants'].append('浪身与浪冠同时加厚，保留椅背、人物头手、平台边缘作为尺度；不放大家具、不增加杂物，不延续紫电。后殿和平台结构完整。')
records=[]
for id,filename in sources.items():
 s=by[id];old_image=s['presentation']['path'];dest=f'镜头设计/图像/蓄力与水雷-v038/{id}-v038-r1.png'
 src=Path('C:/Users/36322/.codex/generated_images/01a162c1-6e38-7a10-aee7-5c8371c4830c')/filename
 (R/dest).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,R/dest)
 req=f'{rec}/{id}-请求-v001.json';spec=json.loads(read(req));w,h=Image.open(R/dest).size
 s.update(generation_request=req,visual_prompt=spec['prompt'],page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0.,y=0.,w=1.,h=1.),editorial_review=dict(version='v038',status='candidate_pending_author_review',dynamic_execution='pending'))
 visible={'CY024A5':'GPT高举掌心托起紧密旋转的水雷光团，另一手在胸前稳术，两片膜翼保持展开；此静帧尚未压掌。','CY024B':'一根连续的粗水雷柱撞击暗金罩顶部，柱内紫电旋卷，罩边炸出分流浪冠；GPT位于左侧高空。','CY024B1':'高过椅背的厚重浪头推动原款木椅，教徒抓空，水层越过平台边缘；画面无紫电。'}[id]
 s['presentation']=dict(path=dest,role='action',visible=visible,status='v0.38新静帧候选，待作者审阅',missing='静帧已查看；蓄力至压掌、柱内电流方向、撞罩分流及冲椅退水的连续运动待动态制作。',show_as_main=True)
 s['refs']=[dict(path=dest,role='本轮新静帧候选'),dict(path=req,role='冻结实际输入'),dict(path=old_image,role='保留的上一版画面')]+[r for r in s['refs'] if r['path']!=old_image]
 records.append(dict(shot_id=id,original=str(src),destination=dest,sha256=sha(R/dest),request=req,request_sha256=sha(R/req),inputs=[dict(path=p,sha256=sha(p)) for p in spec['referenced_image_paths']],status='candidate_pending_author_review'))
d['continuity']['water_volume']='CY024A5高举掌心聚能，最后渊字才压掌；CY024B云中单根粗水柱直压暗金罩，紫电在柱内盘绕，撞罩后才炸开分流；末段紫电先收，CY024B1厚重清水余浪高过椅背并翻下台阶，后续沿原镜头退水。'
d['continuity']['water_curtain']='单根连续粗水雷柱占中后景，不出现并排双柱或撞罩前分叉；碰到教主暗金罩顶才摊开分流。水体内紫电被水膜折射、泡沫遮断，不是表面贴线。GPT留在侧前方高空，右柱与Claude保护沿原设定；主水停止、紫电先收后才接清水冲椅。'
d.update(version='v0.38',revision='v038',title='《穿云》带图分镜 v0.38 · 蓄力与单柱水雷',subtitle='高举聚能 · 单柱撞罩 · 厚浪掀椅',story_script='剧本/穿云-场景剧本-v0.38.md',source_manifest='镜头设计/生成记录/生成索引-v038.json',review_intro='仅修CY024A5蓄力手势、CY024B单根粗水雷柱及CY024B1厚浪冲椅。115镜381秒、对白字幕与音乐预算保持；三张新静帧待作者审阅。',review_focus='先高举聚能再压掌；单柱撞罩才分流；厚浪推动原款长椅，紫电先收。',revision_notes=dict(previous_manifest='镜头设计/shot-plan-v0.37.json',previous_html='镜头设计/带图分镜-v0.37.html',modified_ids=list(sources),boundary='仅三镜画面和对应动作；其余112镜资料、全片时长及声音保持。'))
lines=script.splitlines();lines[2]='版本：v0.38｜2026-10-23｜高举聚能、单柱水雷撞罩分流、厚浪掀椅。';write(d['story_script'],'\n'.join(lines)+'\n')
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']];sc['pages']=list(dict.fromkeys(s['presentation']['path'] for s in ss));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
save('镜头设计/shot-plan-v0.38.json',d)
save(d['source_manifest'],dict(version='v038',engine='built-in image_gen',previous_index=o['source_manifest'],records=records))
shutil.copy2(R/'镜头设计/带图分镜.html',R/'镜头设计/带图分镜-v0.37.html')
p='scripts/build_storyboard.py';s=read(p).replace('shot-plan-v0.37.json','shot-plan-v0.38.json').replace('"v037")','"v037", "v038")').replace("'v037')","'v037','v038')").replace('data.get("revision")=="v037"','data.get("revision") in ("v037","v038")');write(p,s)
p='00_打开项目.html';write(p,read(p).replace('v0.37','v0.38'))
p='制作进度.md';s=read(p);pos=s.index('## 2026-10-23：');note='## 2026-10-23：蓄力与单柱水雷（v0.38）\n\n作者要求GPT施法前明显蓄力、双水柱合并加粗、撞教主护罩后分流并增强冲椅浪势。仅修CY024A5/A5对应剧本、CY024B和CY024B1：高举掌心聚能至渊字压掌，单柱内紫电螺旋与水融合，撞罩后炸开，清水厚浪高过椅背。内置imagegen生成三张新候选并实际查看；旧图保留。\n\n同步[剧本v0.38](剧本/穿云-场景剧本-v0.38.md)与[带图分镜](镜头设计/带图分镜.html)。115镜381秒，全部对白、字幕时点、音频引用、音乐预算保持；其余112镜资料未改。静帧不证明连续运动，未生成音视频。见[复核记录](镜头设计/生成记录/蓄力与水雷-v038/复核记录.md)。\n\n';write(p,s[:pos]+note+s[pos:])
print('v038 written: 3 revised images, 115 shots, 381 sec')
