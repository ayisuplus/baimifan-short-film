"""One-time v0.31 migration: approved storm incantation and scoped storyboard edits."""
import copy, hashlib, json, shutil
from pathlib import Path
from PIL import Image

R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/苍龙雷渊-v031'
IMG='镜头设计/图像/苍龙雷渊-v031'
if (R/'镜头设计/shot-plan-v0.31.json').exists():
    raise SystemExit('v0.31 exists; do not replay migration')
def read(p): return (R/p).read_text(encoding='utf-8-sig')
def write(p,t): (R/p).write_text(t,encoding='utf-8')
def save(p,o): write(p,json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
old=json.loads(read('镜头设计/shot-plan-v0.30.json')); d=copy.deepcopy(old)
by={s['id']:s for s in d['shots']}; oldby={s['id']:s for s in old['shots']}
cache=Path('C:/Users/36322/.codex/generated_images/01a162c1-6e38-7a10-aee7-5c8371c4830c')
outputs=[('CY024A6',1,'exec-33a71205-7ac5-4042-a48d-ad8f917b5834.png'),('CY024A8',1,'exec-8fa3c131-643e-43fa-be4c-5acb7e2164ce.png'),('CY024A8',2,'exec-e31c893a-6a95-45bd-9972-080a4ccd9815.png'),('CY024A8',3,'exec-43891500-ec41-4c7e-8799-81caca98c9fa.png'),('CY024B',1,'exec-82e0670a-509e-45d3-ba5c-9f3b0c0dd5b3.png')]
(R/IMG).mkdir(parents=True,exist_ok=True)
records=[]
for sid,attempt,fn in outputs:
    dest=f'{IMG}/{sid}-v031-r{attempt}.png'; shutil.copy2(cache/fn,R/dest)
    req=f'{REC}/{sid}-请求-v{attempt:03}.json'; args=json.loads(read(req))
    records.append(dict(shot_id=sid,attempt=attempt,original=str(cache/fn),destination=dest,sha256=sha(R/dest),request=req,request_sha256=sha(R/req),inputs=[dict(path=p,sha256=sha(p)) for p in args['referenced_image_paths']],status='superseded_preserved' if sid=='CY024A8' and attempt<3 else 'candidate_pending_author_review'))

lines=[
'盘踞于苍穹尽头，','统御深流与雷鸣的古老意志啊。','循吾之声，自漫长的沉眠中苏醒。',
'将散落尘世的万千水息，','汇作悬于群星之下的无岸之海。','以重云为冠，以紫电为爪，','让汝的咆哮震彻这寂静的长夜。',
'此刻，洞开天穹，倒悬沧海！','令灼烧无辜的烈焰，在奔流中止息；','令阻挡吾行的高墙，在雷鸣中崩裂！',
'水与雷的执掌者啊，','听我号令——','苍龙雷渊！']
seq=['CY024A','CY024A1','CY024A2','CY024A3','CY024A6','CY024A7','CY024A4','CY024A8','CY024A5']
by['CY024A7']=copy.deepcopy(by['CY024A6']);by['CY024A7']['id']='CY024A7'
by['CY024A8']=copy.deepcopy(by['CY024A4']);by['CY024A8']['id']='CY024A8'
def cue(text,offset,duration,speaker='ChatGPT'): return dict(speaker=speaker,text=text,offset=offset,duration=duration)
specs={
'CY024A':(4,[cue('抱紧我。',0,1.1,'千问'),cue(lines[0],1.2,2.7)]),
'CY024A1':(4,[cue(lines[1],0,3.9)]),
'CY024A2':(4,[cue(lines[2],0,3.9)]),
'CY024A3':(5.5,[cue(lines[3],0,2.4),cue(lines[4],2.4,3.0)]),
'CY024A6':(6,[cue(lines[5],0,2.6),cue(lines[6],2.6,3.3)]),
'CY024A7':(3.5,[cue(lines[7],0,3.4)]),
'CY024A4':(4,[cue(lines[8],0,3.9)]),
'CY024A8':(4,[cue(lines[9],0,3.9)]),
'CY024A5':(7,[cue(lines[10],0,2.3),cue(lines[11],2.4,1.6),cue(lines[12],4.8,2.1)])}

texts={}
for sid,idx in [('CY024A',0),('CY024A1',1),('CY024A2',2)]:
    text=oldby[sid]['source_quote']; oldline=oldby[sid]['subtitle_cues'][-1]['text']
    texts[sid]=text.replace(oldline,lines[idx])
texts['CY024A2']=texts['CY024A2'].replace('先隔开逼近的火舌与热浪。','先隔开逼近的火舌与热浪。弧盾同时排开后续魔法雷支流，底部通道只允许失去魔法电弧的清水进入灭火，不把雷引向她的金属束具。')
texts['CY024A3']='''切到教堂屋顶上方空气中的水珠特写。一颗较大的透明水珠轻轻颤动，被向上的力量拉长，又回弹；两三颗小水珠靠近、融入，接触处形成细小液桥。它晃动一下继续上升，背景更多微小水珠朝同一方向聚拢。水珠由高处水雾凝成，不从殿内地面抽水，也不是向下落的雨。月光与教堂尖塔在液面形成微小折射，云影逐渐遮住月色；此镜还未出现紫电。

**ChatGPT（画外）：**
将散落尘世的万千水息，
汇作悬于群星之下的无岸之海。'''
texts['CY024A6']='''切到教堂外低处台阶旁，从地面陡仰拍中殿上空。尖塔、飞扶壁和完整屋顶轮廓压在画面下缘及两侧，一朵巨大的深蓝黑色乌云占据大部分天空。层层云壁向中心旋卷，上浮水珠融入云腹；紫色闪电第一次从云层深处间歇亮起，照出盘旋的体积与深度。雷光只在云内游走，尚未向屋顶放电；云与电的形态隐约呼应冠与爪，不出现实体龙、龙脸或另一只生物。云心正对中殿，后殿不在落水破坏区。

**ChatGPT（画外）：**
以重云为冠，以紫电为爪，
让汝的咆哮震彻这寂静的长夜。'''
texts['CY024A7']='''切入同一仰视方向的云心近景。厚重云壁向纵深旋卷，暗色中心缓缓张开，紫电分支在云褶之间闪过；积聚的水雾与细流仍被托在云内。这里的“洞开天穹”表现云心张开，不让教堂屋顶提前破裂，不画明亮传送门。水仍未落下，雷声和音乐抬升。

**ChatGPT（画外）：**
此刻，洞开天穹，倒悬沧海！'''
texts['CY024A4']='''切回Claude脚边的低柴与弧盾下缘局部：火焰仍在盾外翻动，裙边、赤足和脚踝束具在上方可辨；蓝色护盾下缘与石台之间的水流通道保持敞开。她仍受缚，头纱与衣料干燥，火焰尚未熄灭。借这个局部，把天空中的威势接回等待获救的人。

**ChatGPT（画外）：**
令灼烧无辜的烈焰，在奔流中止息；'''
texts['CY024A8']='''教主在长阶下段中央缓台听见闷雷，缓缓抬起下巴，目光转向画外完整的穹顶，紧绷的眉眼第一次露出警觉。他看不到屋顶外的云心；一瞬微弱紫光仅由高处彩窗与敞开的门传入，脸侧仍有原有火盆的暖光。衣袍干燥，脚步未动，暗金护罩尚未展开。

**ChatGPT（画外）：**
令阻挡吾行的高墙，在雷鸣中崩裂！'''
texts['CY024A5']='''切回ChatGPT。她抬眼，确认青蓝弧盾和侧柱白银护光都已就位；自己仍在靠入口、主落水柱前方的安全位置，施法水纹将靠近的侧浪与雷支流向外引开。

**ChatGPT：**
水与雷的执掌者啊，

她收拢手指，语气从低沉的呼唤转为确定的命令。

**ChatGPT：**
听我号令——

音乐骤收约0.8秒，只留呼吸和远处低雷。她重读招式名，声音坚定而不嘶喊，手掌随最后一个字翻下。

**ChatGPT：**
苍龙雷渊！'''
for sid,(seconds,cues) in specs.items():
    s=by[sid];s.update(seconds=seconds,source_quote=texts[sid],subtitle_cues=cues,dialogue_cues=[],dialogue='\n'.join(c['speaker']+'：'+c['text'] for c in cues),dialogue_timing_status='estimated_budget_pending_actual_readthrough')
    s['cinematic_beats']=[dict(offset=c['offset'],intent=c['text']) for c in cues]
    s['editorial_review']=dict(version='v031',status='candidate_pending_author_review',dynamic_execution='pending')

def describe(sid,**kw): by[sid].update(kw)
describe('CY024A',title='古老意志，起咏',sound='千问先说抱紧我；GPT低声起句，低弦持续音进入，环境声缓慢压低。两人台词不重叠。配音与音乐待制作。')
describe('CY024A1',sound='低弦连贯跨切；杖首细小魔法声低于人声，吟唱语气平稳。配音与音乐待制作。')
describe('CY024A2',sound='弧盾轻响，低弦略增密；吟唱连贯，不在切镜处换句重起。配音与音乐待制作。')
describe('CY024A3',title='水息上浮，合滴回弹',framing='水珠微距／浅景深／随大滴缓慢上移',action='大水珠晃动、拉长回弹，小滴向上靠近并融入；云影逐渐掩月，上浮方向引向下一镜云腹。',purpose='展示魔法聚水来源，用细小反重力变化为巨大云旋蓄势。',entry_state='护盾已经形成，外部水雾凝滴，月光尚能照见液面。',exit_state='小滴融入大滴并继续上升，云影渐浓。',sound='细薄上行弦乐随水珠加入；液桥合并音轻微，无雨声或近雷，保持人声清楚。声音待制作。')
describe('CY024A6',title='仰望螺旋乌云与紫电',framing='教堂外地面陡仰大景／尖塔压边／云旋占主体',action='镜头从完整尖塔微仰至中殿上空巨大的螺旋乌云；水珠融入云腹，少量紫电在厚云内部间歇闪亮。',purpose='以地面视角交代云旋尺度、位置与水雷蓄势，压迫感来自建筑和天空的体量差。',entry_state='外部水滴上浮，屋顶完整。',exit_state='云旋成形，紫电只在云内游走，水与雷均未落下。',sound='切巨大云旋时低鼓及无词合唱进入；紫电闪后接闷雷，吟唱始终前置，不能以雷声盖字。声音待制作。',asset_ids=['ENV-CHURCH'])
describe('CY024A7',title='云心张开，紫电蓄势',framing='同向仰视云心近景／现有云旋图局部视窗',action='云壁向纵深旋卷，暗色中心张开，紫电沿云褶掠过；水仍悬在云中，地面建筑不提前破坏。',purpose='让洞开天穹的命令对应蓄势变化，保留真正释放的延迟。',entry_state='云旋已成形，内部紫电闪动。',exit_state='云心张开但没有向下释放，切回火前受困者。',sound='弦乐、低鼓与合唱共同抬升，闷雷压在对白后；此处不是最终落水重音。声音待制作。',asset_ids=['ENV-CHURCH'])
describe('CY024A4',title='盾外烈焰仍燃',framing='Claude脚边与低柴局部／护盾开底可辨',action='火舌在盾外低柴翻动，上方衣料干燥，赤足仍在固定脚托；镜头把蓄势拉回救人目的。',purpose='让止息烈焰指向具体受困者，同时重申开底灭火与尚未解锁。',entry_state='天空蓄势，尚未落水。',exit_state='低柴仍燃、弧盾稳定，接教主听雷抬头。',sound='音乐保持高位，短露火焰噼啪声，GPT画外继续，不能先做熄火声。声音待制作。')
describe('CY024A8',title='教主听雷抬眼',framing='教主胸上近景／略仰机位／仰望画外完整穹顶',action='教主在原缓台听雷抬头，眉眼绷紧；侧窗间接紫光掠过脸侧，原火盆暖光尚在，未张护罩。',purpose='把天空威压转成人物反应，并为下一镜教主自张护罩提供预备。',entry_state='教主原地站立，衣料干燥，屋顶尚完整。',exit_state='教主已警觉抬头，未移动，切GPT最终命令。',sound='闷雷经殿内回响而来，GPT画外句末崩裂加重但不嘶喊；没有新增教主对白。声音待制作。',asset_ids=['CHAR-PRIEST','ENV-CHURCH'])
describe('CY024A5',title='听我号令——苍龙雷渊',action='GPT确认护人已就位，收拢手指；听我号令后短停，随苍龙雷渊最后的渊字翻掌压下。',entry_state='云旋、水与雷已蓄势，人物防护已就位，屋顶仍完整。',exit_state='翻掌完成，命令落字，下一镜水雷同时倾泻。',sound='0—4秒音乐持续高位；4—4.8秒骤收，留呼吸与远雷；4.8—6.9秒招式名重读不喊破，渊字与下一镜水雷及管弦重音对齐。声音待制作。')
by['CY024A5']['cinematic_beats'] += [dict(offset=4,intent='音乐骤收0.8秒'),dict(offset=6.8,intent='渊字翻掌，切水雷落下')]

# Replace old spell block as a unit, retaining the source passages of every other shot.
t=read(old['story_script']);start=t.index(oldby['CY024A']['source_quote']);end=t.index(oldby['CY024A5']['source_quote'])+len(oldby['CY024A5']['source_quote'])
t=t[:start]+'\n\n'.join(texts[sid] for sid in seq)+t[end:]
flood=oldby['CY024B']['source_quote'].replace('天瀑从夜空轰穿中央中殿的穹顶，','苍龙雷渊应声释放，云中汇聚的水与紫色魔法雷霆一同轰穿中央中殿的穹顶，').replace('主水体向下倾泻，落地激起宽阔水浪。','主水体向下倾泻，少量紫电间歇穿行于水幕内部，水仍是画面主体，落地激起宽阔水浪。')
flood += ' 魔法雷支流在青蓝弧盾、右侧白银护光及教主暗金罩的外缘偏转，远离盾内身体与金属束具；GPT入口侧水纹把侧浪和雷支流导离自身。盾下只通过已失去魔法电弧的清水，不让紫电沿地面蔓延。水幕结束前紫电先收尽，下一镜长椅只受清水余浪冲击。'
t=t.replace(oldby['CY024B']['source_quote'],flood,1);by['CY024B']['source_quote']=flood
by['CY024B'].update(title='苍龙雷渊，水雷倾泻',action='连续水幕覆盖中后景，内部间歇紫电随水落下；三处护罩排开雷支流，盾下清水灭火，入口侧GPT将侧浪导开。',sound='渊字落点接水幕爆响、雷击低频与管弦重音；随后转持续瀑声，紫电只短促爆裂，不能持续电噪。末段紫电先熄再切余浪。声音待制作。')
by['CY024B1']['sound']='紫电已收尽；余浪拍石、木椅滑擦与翻转声，教徒短促失衡声；无人体受伤细节。声音待制作。'
oldret=oldby['CY027']['source_quote'];newret=oldret.replace('天瀑停下，','苍龙雷渊的紫电已收尽，水幕停下；云旋松散，月光重新透下。')
t=t.replace(oldret,newret,1);by['CY027']['source_quote']=newret

# Current narrative uses the new name; historical handover notes and all frozen prompts keep their provenance.
body,notes=t.split('## 制作交接备注',1);body=body.replace('天瀑','苍龙雷渊');t=body+'## 制作交接备注'+notes
tl=t.splitlines();tl[2]='版本：v0.31｜2026-10-23｜作者确认苍龙雷渊长咏唱；仰视螺旋乌云、云心紫电、水滴与人物反应；救护与咏唱共42秒。';t='\n'.join(tl)+'\n'
write('剧本/穿云-场景剧本-v0.31.md',t)
for s in d['shots']+[by['CY024A7'],by['CY024A8']]:
    for field in ['title','purpose','entry_state','action','exit_state','dialogue','sound','next_link','source_quote','lighting','claude_accessory_state']:
        if field in s:s[field]=s[field].replace('天瀑','苍龙雷渊')
    s['invariants']=[x.replace('天瀑','苍龙雷渊') for x in s.get('invariants',[])]

weather_rules=['机位在教堂外地面仰望，不能穿透完整屋顶；尖塔与飞扶壁压边、云旋占主体。','上浮水滴先凝聚，再被厚重螺旋云腹吸收；不再使用俯拍悬空液态水库，不提前落雨。','云内紫电允许在咏唱中间歇闪动，未到最终命令不得向下击穿屋顶。','云心为厚重立体暗云，不是明亮传送门；冠与爪只是形态联想，不提前出现实体龙。','中殿与后殿屋顶直到CY024B前都完整；最终只破中殿，保留后殿和正门。']
for sid in ['CY024A3','CY024A6','CY024A7']:by[sid]['invariants']=weather_rules.copy()
shield='Perplexity在右侧柱后举杖发出青蓝弧盾并维持到战后；弧盾护住Claude头顶、身前与两侧，排开水雷，底部离地只让失去魔法电弧的清水灭低柴。细水花仍可打湿发梢衣料，镣铐不被雷击解开。千问和小鱼由骑士白银护光保护，教主自张暗金罩；GPT入口侧水纹导开侧浪与雷支流。'
for sid in seq+['CY024B']:
    if sid not in ['CY024A3','CY024A6','CY024A7']:by[sid]['invariants']=[shield,'完整屋顶期间紫光只经侧窗或敞门入殿；雷声可听见，云心不可透顶看见。','施法声始终为ChatGPT，教主反应不新增对白。','水雷收势后再对峙，真正龙形仍在后续变身，未提前解锁Claude。']

def set_image(sid,attempt=1):
    s=by[sid];path=f'{IMG}/{sid}-v031-r{attempt}.png';req=f'{REC}/{sid}-请求-v{attempt:03}.json'
    with Image.open(R/path) as im:w,h=im.size
    oldpath=s['presentation']['path']
    s.update(presentation=dict(path=path,role='action',visible=s['action'],status='v0.31新静帧候选，待作者审阅',missing='静帧不能证明云旋、紫电间歇、人物连续反应及水雷受控分流；动作和声音待制作。',show_as_main=True),page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0.,y=0.,w=1.,h=1.),panel_index=0,generation_request=req,visual_prompt=json.loads(read(req))['prompt'],refs=[dict(path=path,role='本轮新静帧候选'),dict(path=req,role='实际冻结输入'),dict(path=oldpath,role='历史参考保留')])
set_image('CY024A6');set_image('CY024A8',3);set_image('CY024B')
# Cloud-core is an editorial window from the same cloud master, not a second generated image.
cloud=by['CY024A6'];core=by['CY024A7']
for key in ['presentation','page_size','generation_request','visual_prompt','refs']:core[key]=copy.deepcopy(cloud[key])
core['presentation'].update(visible='同一仰拍云旋图的云心与紫电局部视窗。',missing='局部视窗仅验证构图，云心向纵深张开的运动待动态。')
core['panel_region']=dict(x=.30,y=.015,w=.44,h=.44)
w,h=core['page_size'];core['panel_rect_pixels']=[round(.30*w),round(.015*h),round(.44*w),round(.44*h)]
core['refs'].append(dict(path=f'{IMG}/CY024A6-v031-r1.png',role='共用云旋母图，局部展示不修改原图'))
fire=by['CY024A4'];fire['panel_region']=dict(x=.21,y=.40,w=.58,h=.58)
w,h=fire['page_size'];fire['panel_rect_pixels']=[round(.21*w),round(.40*h),round(.58*w),round(.58*h)]
fire['presentation'].update(visible='复用护盾图的下半身、脚托、弧盾下缘与低柴局部视窗。',missing='原图局部构图预演，火舌和护盾持续运动待动态。')
by['CY024A3']['presentation']['visible']='沿用v0.30大水珠合滴代表帧；本轮延长为5.5秒，动态上浮和回弹待制作。'
by['CY024A3']['presentation']['missing']='向上漂浮、晃动、合滴与云影掩月需动态实现，现图只表达代表状态。'
ids=[s['id'] for s in d['shots']];first=ids.index('CY024A');last=ids.index('CY024A5')
d['shots']=d['shots'][:first]+[by[sid] for sid in seq]+d['shots'][last+1:]
for a,b in zip(seq,seq[1:]+['CY024B']):by[a]['next_link']='接'+b+'：'+by[b]['entry_state']+' GPT吟唱与音乐连续跨切。'
d.update(version='v0.31',revision='v031',created='2026-10-23',title='《穿云》带图分镜 v0.31 · 苍龙雷渊',subtitle='地面仰拍螺旋乌云 · 水滴上浮 · 紫电水幕 · 长咏唱',story_script='剧本/穿云-场景剧本-v0.31.md',origin_manifest='镜头设计/shot-plan-v0.30.json',source_manifest='镜头设计/生成记录/生成索引-v031.json')
d['review_intro']='作者确认苍龙雷渊原创长咒语、仰拍云旋、紫电与水滴。护人及咏唱9镜42秒，其中千问起句1.2秒，GPT咏唱预算约40.8秒；全片105镜348秒。三张新图候选、水滴旧图复用、云心与火前局部视窗已接入同一预演。配音、BGM与动态尚未制作。'
d['review_focus']='水滴上浮→地面仰拍云旋→云心蓄势→盾外低柴→教主听雷抬眼→GPT命令→紫电水幕；云内可闪电但不提前破顶，雷支流避开盾内人物，开底清水灭火，长椅下一镜才掀起。'
d['revision_notes']=dict(previous_manifest='镜头设计/shot-plan-v0.30.json',previous_html='镜头设计/带图分镜-v0.30.html',added_ids=['CY024A7','CY024A8'],modified_ids=seq+['CY024B','CY024B1','CY027'],repurposed_ids=['CY024A6','CY024A4'],boundary='当前天瀑改名苍龙雷渊，保留原封版及历史输入。24秒施法段扩为42秒，增加云心和教主反应2镜；除本段外时长、对白、图片保持。')
d['music_direction']=dict(status='design_only_not_rendered',sequence=seq+['CY024B','CY024B1'],rule='同一BGM连续：起咏低弦→护盾轻声铺底→水滴上行细弦→仰拍云旋低鼓/无词合唱进入→云心与雷声抬升→火前/教主反应保持威压→命令后骤收0.8秒→苍龙雷渊最后渊字接水雷管弦重音→紫电先收尽只余水声。人声居前，前半低沉从容、后半坚定、不嘶喊。旧Victory粗剪不代表本轮完成。',estimated_spell_sequence_seconds=42,estimated_gpt_incantation_seconds=40.8,voice_timing='subtitle_budget_only_pending_actual_readthrough',approved_incantation=lines)
for k,v in d['continuity'].items():
    if isinstance(v,str):d['continuity'][k]=v.replace('天瀑','苍龙雷渊')
d['continuity']['water_gathering']='水雾凝滴向上合流→地面仰拍中殿上空的螺旋乌云→紫电在云内间歇游走→云心张开但不破屋顶→最终命令后水雷一起落下，仅破中殿；后殿完整。旧悬空液态水库退出当前版。'
d['continuity']['claude_shield']=shield
d['continuity']['storm_release']='施法雷电受GPT控制，沿护盾外缘偏转，不沿地面导电或击中镣铐。水幕结束前紫电收尽，CY024B1只留清水余浪；CY027云旋松散、月光重新透下，再对峙和真龙变身。'
d['continuity']['water_impact_insert']='CY024B1紧接水雷大景，局部展示最高祭坛后墙左侧长椅刚被余浪掀离原位、教徒抓空；不是侧廊凭空出现的椅子，所有普通灯火已灭。'
for k in ['magic','lighting']:d['continuity'][k]=d['continuity']['altar_lighting_v023']+' 云内紫电间歇闪动，破顶前仅经彩窗或敞门入殿；落水时短暂紫电局部照明，收势后只留既定冷光。'
elapsed=0
for s in d['shots']:s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
d['total_seconds']=elapsed
for sc in d['scenes']:
    ss=[s for s in d['shots'] if s['scene']==sc['id']];sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
save('镜头设计/shot-plan-v0.31.json',d)
save('镜头设计/生成记录/生成索引-v031.json',dict(version='v031',previous_index='镜头设计/生成记录/生成索引-v030.json',records=records,review=REC+'/复核记录.md',reused_water_drop=by['CY024A3']['presentation']['path'],superseded_direction=dict(path=oldby['CY024A6']['presentation']['path'],reason='作者否定俯拍悬空水体方向，改地面仰拍螺旋乌云；历史图保留')))
snap=R/'镜头设计/带图分镜-v0.30.html'
if not snap.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snap)
p='scripts/build_storyboard.py';write(p,read(p).replace('shot-plan-v0.30.json','shot-plan-v0.31.json').replace('"v030")','"v030", "v031")').replace("'v030')","'v030','v031')"))
p='00_打开项目.html';x=read(p).replace('v0.30','v0.31').replace('103 镜','105 镜').replace('5 分 30 秒','5 分 48 秒').replace('长吟唱24秒','护人及长吟唱42秒').replace('云海之水，听我号令——天瀑','听我号令——苍龙雷渊').replace('本轮：水珠上浮与穹顶聚水','本轮：苍龙雷渊 · 仰拍云旋与紫电').replace('两张新图 · 云海之水，听我号令 · 施法仍24秒','水滴→仰拍螺旋乌云→云心紫电→人物反应→水雷倾泻').replace('#CY024A3','#CY024A6',1)
write(p,x)
p='制作进度.md';x=read(p);i=x.index('## ')
write(p,x[:i]+'''## 2026-10-23：苍龙雷渊、仰拍云旋与水雷咏唱（v0.31）

作者确认完整原创长咒语及镜头音乐设计，已同步[剧本v0.31](剧本/穿云-场景剧本-v0.31.md)和[当前带图分镜](镜头设计/带图分镜.html)。原24秒施法段扩为9镜42秒（含千问起句约1.2秒，GPT咏唱预算约40.8秒），新增CY024A7云心局部与CY024A8教主听雷反应；全片105镜348秒（5分48秒）。其他段时长与对白保持。

CY024A6改为教堂外地面仰拍螺旋乌云及云内紫电，CY024A3保留原水滴图并延长晃动合滴到5.5秒；云心与Claude脚边低柴采用现有图局部视窗。CY024B连续水幕加入少量紫电，护盾外缘排开魔法雷支流，底部清水灭火；紫电先收、下一镜余浪才掀左后墙长椅。云旋散开后月光恢复，对峙和真正龙形变身仍在后面。

三张当前新图由内置imagegen制作，均待作者审阅；教主旧资产初版存在年龄/纹样差异，已按当前CY027A修订脸与服饰并清除新增背景灯具，前两次候选保留。旧俯拍悬水方向退出当前版但不删除。低弦→上行细弦→低鼓与无词合唱→命令后收声0.8秒→渊字接水雷重音已写入镜头；正式咏唱、BGM、雷水声及动态未制作，42秒为估算待试读。见[复核记录](镜头设计/生成记录/苍龙雷渊-v031/复核记录.md)。

'''+x[i:])
assert len(d['shots'])==105 and elapsed==348
assert sum(by[sid]['seconds'] for sid in seq)==42
assert ''.join(c['text'] for sid in seq for c in by[sid]['subtitle_cues'] if c['speaker']=='ChatGPT')==''.join(lines)
for s in d['shots']:assert s['source_quote'] in t,s['id']
print('v0.31 prepared:105 shots,348 seconds,42-second spell block;3 current images,2 preserved intermediate images.')
