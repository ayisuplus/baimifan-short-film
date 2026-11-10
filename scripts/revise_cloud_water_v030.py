"""Add upward water-drop and rooftop reservoir shots; revise incantation."""
import copy,json,hashlib,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];REC='镜头设计/生成记录/水珠与云顶-v030';IMG='镜头设计/图像/水珠与云顶-v030'
if (R/'镜头设计/shot-plan-v0.30.json').exists():raise SystemExit('v0.30 already exists; edit current files directly instead of replaying migration.')
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,t):(R/p).write_text(t,encoding='utf-8')
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
cache=Path('C:/Users/36322/.codex/generated_images/01a162c1-6e38-7a10-aee7-5c8371c4830c')
originals={'CY024A3':cache/'exec-269dc38f-2c0c-4938-9ab9-b4bc2818c22d.png','CY024A6':cache/'exec-326cc181-6cf7-44ed-ad75-62e13c4e888e.png'}
(R/IMG).mkdir(parents=True,exist_ok=True)
for id,p in originals.items():shutil.copy2(p,R/IMG/(id+'-v030-r1.png'))
old=json.loads(read('镜头设计/shot-plan-v0.29.json'));d=copy.deepcopy(old);by={s['id']:s for s in d['shots']}
drop='''切到教堂屋顶上方空气中的水珠特写。一颗较大的透明水珠轻轻颤动，被向上的力量拉长，又回弹；两三颗小水珠靠近、融入，接触处形成细小液桥。它晃动一下继续上升，背景更多微小水珠朝同一方向聚拢。水珠由高处水雾凝成，不从殿内地面抽水，也不是向下落的雨。月光与远处教堂在液面形成微小折射。

**ChatGPT（画外）：**
在此展开倾天之势。'''
reservoir='''切教堂外高位斜俯视。乌云作为背景缓缓卷动，云层下方的水珠和细流汇入中殿正上方的厚重悬空水体。水体轮廓不规则，表面波动，下缘坠出起伏的鼓包，又被力量托住；不是圆球、冰块或一团乌云。下方中殿屋顶和后殿拱顶均完整，屋顶与水体之间留有清楚的空气间隙。水尚未下落，不加闪电；蓄水中心对准中殿，后续落水不扩成整座教堂被压毁。

**ChatGPT（画外）：**
让高悬的洪门洞开，'''
release='''切回ChatGPT。她抬眼，确认保护已就位。

**ChatGPT：**
云海之水，

她收拢手指。

**ChatGPT：**
听我号令——

音乐骤收，留出短暂空隙；手掌随最后的法术名翻下。

**ChatGPT：**
天瀑。'''
t=read(old['story_script']);t=t.replace(by['CY024A3']['source_quote'],drop+'\n\n'+reservoir,1).replace(by['CY024A5']['source_quote'],release,1)
# Preserve the knights' evacuation action after replacing the old GPT hold shot.
needle='护盾下缘悬在石台之上，低柴堆留在盾外，底部保留水流通道；不是包住整座祭坛的封闭球。Claude抬眼看向来光，腕镣、腰链、踝链与固定脚托都未解除。'
replacement=needle+' 与此同时骑士退入两翼厚石柱后，中央落水区净空；ChatGPT仍在中殿入口方向抬掌蓄势。'
assert needle in t;t=t.replace(needle,replacement,1)
lines=t.splitlines();lines[2]='版本：v0.30｜2026-10-23｜补水珠上浮特写与穹顶聚水大景；收尾改“云海之水，听我号令——天瀑”；施法段仍24秒。';t='\n'.join(lines)+'\n'
write('剧本/穿云-场景剧本-v0.30.md',t)
d.update(version='v0.30',revision='v030',created='2026-10-23',title='《穿云》带图分镜 v0.30 · 水珠与云海之水',subtitle='上浮水珠→穹顶聚水→云海之水，听我号令；施法仍24秒',story_script='剧本/穿云-场景剧本-v0.30.md',origin_manifest='镜头设计/shot-plan-v0.29.json',source_manifest='镜头设计/生成记录/生成索引-v030.json')
d['review_intro']='作者确认两个聚水画面及收尾“云海之水，听我号令——天瀑”。原6秒GPT蓄势镜改为水珠3秒与穹顶聚水4秒；两处护盾镜各收1秒，最终命令加1秒，整段仍24秒。新增两张静帧待审，真实上浮/合滴/积水及声音尚未制作。'
d['review_focus']='看护盾成形→小水珠上浮合并→中殿屋顶上方巨大水体→Claude→GPT云海之水/听我号令/天瀑；水珠方向向上、屋顶直到落水才破，吟唱与音乐连续跨切。'
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.29.json',previous_html='镜头设计/带图分镜-v0.29.html',added_ids=['CY024A6'],modified_ids=['CY024A1','CY024A2','CY024A3','CY024A4','CY024A5'],repurposed_ids=['CY024A3'],boundary='原CY024A3六秒GPT蓄势改为水珠三秒，新增CY024A6四秒云顶聚水；A1/A2各4→3秒，A5由3→4秒。103镜330秒，施法段仍24秒；其余对白与图片保持。')
def cue(text,offset,duration):return dict(speaker='ChatGPT',text=text,offset=offset,duration=duration)
by['CY024A1'].update(seconds=3,subtitle_cues=[cue('沉眠于云海的无尽潮汐。',0,2.95)])
by['CY024A2'].update(seconds=3,source_quote=by['CY024A2']['source_quote'].replace(needle,replacement),subtitle_cues=[cue('循我的声音汇聚，',0,2.85)])
by['CY024A2']['action']+=' 骑士同时退入两翼柱后，中央落水区净空。'
by['CY024A2']['sound']='护盾展开声克制，低弦连续铺底；为下一镜细薄的水珠上行弦乐留空间，不提前满编合唱。GPT画外吟唱清楚，实际声音未制作。'
by['CY024A2']['exit_state']='弧盾已成形，低柴在外，骑士净空；GPT吟唱继续，切屋顶上空水珠。'
by['CY024A2']['next_link']='接CY024A3：由护盾细光过渡到银蓝水珠，GPT声音跨切到教堂外。'
oldshot=copy.deepcopy(by['CY024A3']);s=by['CY024A3']
s.update(title='向上汇聚的水珠',seconds=3,framing='屋顶上空水珠微距／浅景深／随水珠缓缓上移',action='大水珠颤动、拉长回弹，小水珠靠近并融合；水珠从高处水雾凝成，继续向上汇聚。',source_quote=drop,purpose='以小尺度上浮聚水建立天瀑的来源和反重力蓄势。',entry_state='Claude护盾已成形，水尚未落下；切教堂屋顶上方空气中的水珠。',exit_state='小水珠融合，较大水珠继续向上，接同一聚水过程的大尺度。',next_link='接CY024A6：从水珠上浮切到其汇入中殿上方的巨大悬空水体。',dialogue='ChatGPT：在此展开倾天之势。',subtitle_cues=[cue('在此展开倾天之势。',0,2.85)],dialogue_cues=[],sound='GPT画外吟唱不断，细薄上行弦乐保持，轻微液体合并音；不提前加入强鼓、雷声或落雨声。音乐与音效未制作。',asset_ids=['ENV-CHURCH'])
s['cinematic_beats']=[dict(offset=0,intent='微距锁定轻颤大水珠，背景小滴上浮'),dict(offset=.6,intent='小滴接近、液桥合并，大滴拉长再回弹'),dict(offset=1.7,intent='大滴继续上升，视线引向下一镜悬空水体')]
wide=copy.deepcopy(s);wide.update(id='CY024A6',title='穹顶上方的悬空水体',seconds=4,framing='教堂外高位斜俯大景／完整屋顶与悬水同框',action='乌云作背景，水珠与细流汇入中殿正上方的不规则厚重水体；下缘起伏悬而未落，完整屋顶与水体间的空隙可见。',source_quote=reservoir,purpose='将微小水珠汇聚的结果放大，交代天瀑蓄水位置、体量和即将落向中殿的方向。',entry_state='上浮水珠正汇入高处，中殿屋顶完整。',exit_state='水体悬于中殿上方，尚未下落；切回盾中Claude，再回GPT下令。',next_link='接CY024A4：外部积水尚悬空，切Claude在弧盾中抬眼，仍干燥受束。',dialogue='ChatGPT：让高悬的洪门洞开，',subtitle_cues=[cue('让高悬的洪门洞开，',0.1,3.2)],sound='由微距切到巨大水体时，低鼓与无词合唱加入，弦乐延续；低沉水体共鸣蓄势但无落水爆响。吟唱清楚居前，实际音乐/音效未制作。')
wide['cinematic_beats']=[dict(offset=0,intent='大景交代水体和完整中殿屋顶之间的距离'),dict(offset=1,intent='边缘水珠汇入，厚水体下缘鼓动但不释放'),dict(offset=3.2,intent='保持重量和压迫感，接Claude反应')]
rules=['此处在教堂屋顶上方空气中，水雾凝水、运动向上；不从殿内地面抽水，不提前下雨。','乌云作背景，实际汇聚的是液态水；不是水晶球、冰块、圆盘或仅乌云翻滚。','水体悬于中殿上方且与屋顶分离；中殿与后殿屋顶此刻都完整。','没有闪电、战斗爆闪、飞石或落水；实际天瀑在最终命令后才冲破中殿。','与小水珠镜连续，最终水体向中殿落下，不能将后殿或全城一起摧毁。']
records=[]
for shot in [s,wide]:
 id=shot['id'];path=IMG+'/'+id+'-v030-r1.png';req=REC+'/'+id+'-请求-v001.json'
 shot['invariants']=rules;shot['presentation']=dict(path=path,role='action',visible=shot['action'],status='v0.30新静帧候选，待作者审阅',missing='单张静帧不能证明水珠向上运动、合并回弹或水体悬停变化；运动方向与速度须动态验证。',show_as_main=True)
 shot['generation_request']=req;shot['visual_prompt']=json.loads(read(req))['prompt']
 shot['refs']=[dict(path=path,role='本轮新静帧候选'),dict(path=req,role='实际冻结输入')]
 with Image.open(R/path) as im:w,h=im.size
 shot.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0.,y=0.,w=1.,h=1.),panel_index=0,editorial_review=dict(version='v030',status='candidate_pending_author_review',dynamic_execution='pending'),dialogue_timing_status='estimated_budget_pending_actual_readthrough')
 request=json.loads(read(req));records.append(dict(shot_id=id,attempt=1,original=str(originals[id]),destination=path,sha256=sha(R/path),request=req,request_sha256=sha(R/req),inputs=[dict(path=p,sha256=sha(p)) for p in request['referenced_image_paths']],status='candidate_pending_author_review'))
s['refs'].append(dict(path=oldshot['presentation']['path'],role='保留原GPT蓄势代表帧；本镜已改水珠'))
idx=d['shots'].index(s);d['shots'].insert(idx+1,wide)
a5=by['CY024A5'];a5.update(seconds=4,source_quote=release,action='GPT抬眼说“云海之水”，收拢手指说“听我号令”；音乐骤收、短停，翻掌说“天瀑”，接水幕轰落。',dialogue='ChatGPT：云海之水，听我号令——\nChatGPT：天瀑。',subtitle_cues=[cue('云海之水，',0,1.25),cue('听我号令——',1.3,1.2),cue('天瀑。',3.2,.75)],sound='云海之水时合唱保持高点，听我号令后骤收，约0.7秒留白，再由天瀑落字接下一镜管弦与水墙重音。实际配音和音乐尚未制作。')
a5['cinematic_beats']=[dict(offset=0,intent='云海之水，抬眼'),dict(offset=1.3,intent='听我号令，手指收拢'),dict(offset=2.5,intent='音乐骤收，短停'),dict(offset=3.2,intent='天瀑，翻掌；下一镜水幕释放')]
seq=['CY024A','CY024A1','CY024A2','CY024A3','CY024A6','CY024A4','CY024A5']
d['music_direction'].update(sequence=seq+['CY024B'],rule='连续同一段BGM跨切：GPT起句低弦→护盾轻声铺底→水珠细薄上行弦乐→穹顶巨大水体时低鼓/无词合唱进入→Claude反应保持高点→云海之水，听我号令后骤收→天瀑落水重音。未绑定或改动旧Victory粗剪。')
d['continuity']['water_gathering']='护盾先成形→屋顶上方空气中水珠上浮、融合→中殿上方厚重水体悬停；乌云作背景，完整屋顶和悬水间留空隙。云海之水/听我号令/天瀑之后才落水破中殿，后殿完整。不提前下雨或闪电。'
elapsed=0
for shot in d['shots']:shot['start_second']=elapsed;elapsed+=shot['seconds'];shot['end_second']=elapsed
d['total_seconds']=elapsed
for sc in d['scenes']:
 ss=[x for x in d['shots'] if x['scene']==sc['id']];sc.update(shot_ids=[x['id'] for x in ss],seconds=sum(x['seconds'] for x in ss),pages=list(dict.fromkeys(x['presentation']['path'] for x in ss)));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=x['presentation']['path'],rows=1,cols=1) for x in d['shots']]
save('镜头设计/shot-plan-v0.30.json',d)
save('镜头设计/生成记录/生成索引-v030.json',dict(version='v030',previous_index='镜头设计/生成记录/生成索引-v029.json',records=records,review=REC+'/复核记录.md'))
snap=R/'镜头设计/带图分镜-v0.29.html'
if not snap.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snap)
p='scripts/build_storyboard.py';write(p,read(p).replace('shot-plan-v0.29.json','shot-plan-v0.30.json').replace('"v029")','"v029", "v030")').replace("'v029')","'v029','v030')"))
p='00_打开项目.html';x=read(p).replace('v0.29','v0.30').replace('102 镜','103 镜').replace('汇于苍穹的万流，听我号令——天瀑','云海之水，听我号令——天瀑')
x=x.replace('<a href="镜头设计/带图分镜.html#CY024A1">','<a href="镜头设计/带图分镜.html#CY024A3">本轮：水珠上浮与穹顶聚水<small>两张新图 · 云海之水，听我号令 · 施法仍24秒</small></a>\n<a href="镜头设计/带图分镜.html#CY024A1">',1)
write(p,x)
p='制作进度.md';x=read(p);i=x.index('## ')
write(p,x[:i].replace('更新：2026-10-22','更新：2026-10-23')+'''## 2026-10-23：水珠上浮、穹顶聚水与“云海之水”（v0.30）

作者确认补两处聚水镜头并采用“云海之水，听我号令——天瀑”。原CY024A3六秒GPT蓄势改为三秒水珠近景，新增CY024A6四秒穹顶上方悬水大景；CY024A1/A2各收一秒，CY024A5多留一秒给新词。七镜合计24秒，全片103镜330秒（5分30秒）。[当前分镜](镜头设计/带图分镜.html)与[剧本v0.30](剧本/穿云-场景剧本-v0.30.md)已同步。

水珠由屋顶上方水雾凝成并向上聚拢；乌云作背景，实际形成厚重液态水体，屋顶仍完整，不提前下雨、闪电或落水。水珠镜用细薄上行弦乐，大景加入低鼓与合唱，最终命令后收声再释放。两张内置imagegen新静帧为待审候选，旧图/版本保留。实际漂浮、合滴、回弹、落水及配音/BGM未制作，24秒为字幕和动作预算。见[复核记录](镜头设计/生成记录/水珠与云顶-v030/复核记录.md)。

'''+x[i:])
assert len(d['shots'])==103 and elapsed==330
assert sum(next(s for s in d['shots'] if s['id']==id)['seconds'] for id in seq)==24
for shot in d['shots']:assert shot['source_quote'] in t,shot['id']
print('Prepared v0.30: 103 shots330 seconds; two new images; spell sequence24 seconds.')

