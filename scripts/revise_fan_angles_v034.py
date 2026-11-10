"""Versioned local revision: upward projectile and distinct impact camera; no media editing."""
import argparse, copy, hashlib, json, shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/扇叶上行与换机位-v034'
IMG='镜头设计/图像/扇叶上行与换机位-v034'
def read(p): return (R/p).read_text(encoding='utf-8-sig')
def write(p,s): (R/p).write_text(s,encoding='utf-8')
def save(p,d): write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=argparse.ArgumentParser();a.add_argument('--flight',required=True);a.add_argument('--impact',required=True);args=a.parse_args()
assert not (R/'镜头设计/shot-plan-v0.34.json').exists(), 'One-time revision already applied'
old=json.loads(read('镜头设计/shot-plan-v0.33.json'));d=copy.deepcopy(old);by={s['id']:s for s in d['shots']}
script=read(old['story_script']).replace('版本：v0.33｜2026-10-23｜GPT展翼升空、千问单片扇叶阻击与子弹时间、斜俯拍水雷、退水降落及全片漏翼修订。','版本：v0.34｜2026-10-23｜修正扇叶地面向上飞行方向，飞行极特写与侧面仰拍撞击采用不同机位。')
fly='切单枚扇叶独立飞行的极特写。扇叶自地面千问的右手斜向上射出，飞往高于站立人头顶的拦截点。摄影机位于刃尖侧前方、略低于飞行路径，朝后看叶身：锐利尖端靠近镜头、位于画面右上，方形叶尾退向左下，薄刃与花纹有明显透视缩短。扇叶始终由左下向右上爬升，柱线保持竖直，不靠歪斜镜头伪造上升。背景教堂高度虚化，只有细金边随轻微轴向翻转掠过反光。镜内只留这一枚实体扇叶，没有敌方术光、人脸或碰撞火花。子弹时间只慢放画面，GPT咏唱自然连续。'
hit='随后切到拦截点侧面更低的仰拍机位，较上一镜绕开约70度且不越动作轴线，景别由极特写拉开为撞击近景。完整扇叶以侧面轮廓出现，画面占比明显缩小；虚化柱廊和高处横向石檐交代撞击发生在半空。扇叶继续从左下斜向右上，叶尾低、刃尖高；教主术光从右下朝左上射向空中ChatGPT，两条向上的路径在半空交汇。接触瞬间恢复常速，只爆开一小点白金亮光和清脆裂响。术光随后断成两股，偏向无人空处消散；扇叶在碰撞失速之后才斜落空侧廊，绝不在接触前向下扎。千问在画外合拢余扇收回胸侧，左臂始终未松开小鱼。\n\n教主收回被震偏的手，发现两侧骑士已经封住接近路线。掩护仍在画外持续，Kimi继续施法；教主转向判断头顶雷声，逐步改为自保，而不是原地等待。'
for sid, passage in [('CY024A11',fly),('CY024A12',hit)]:
    prev=by[sid]['source_quote'];assert script.count(prev)==1
    script=script.replace(prev,passage,1);by[sid]['source_quote']=passage
opening=by['CY024A10'];prev=opening['source_quote'];assert prev in script
opening['source_quote']=prev+' 出叶前右腕向上挑，发射口指向头顶以上的拦截点；千问双脚仍在地面，左臂继续托抱小鱼。'
script=script.replace(prev,opening['source_quote'],1)
opening['action']+=' 出叶前右腕上挑、发射方向斜向上；左臂托抱不变。'
opening['exit_state']='单叶自右手向上弹出，母扇仍在手中，接同方向上行极特写。'
opening['next_link']='接CY024A11：右腕上挑发射，保持地面至高处的上行方向。'
for beat in opening.get('cinematic_beats',[]):
    if beat['offset']==1.7:beat['intent']='右腕上挑，单叶向上弹脱，切上行飞行'
by['CY024A11'].update(title='扇叶上行，刃尖侧前极特写',framing='刃尖侧前方略低机位朝后拍／强透视缩短／左下至右上爬升',entry_state='单枚扇叶由地面千问右手向上发射，方形叶尾低于刃尖。',action='刃尖右上近镜、叶尾左下后退，持续斜向上伴飞，微旋反光；画面仅一枚实体扇叶。',exit_state='沿上行轨迹接近高处拦截点；接触前不向下转向。',next_link='接CY024A12：切同轴侧面低机位并拉开景别，继续左下至右上的运动，碰撞时恢复常速。')
by['CY024A12'].update(title='侧面仰拍，半空截击',framing='与飞行镜相差约70度的侧面低机位仰拍／撞击近景／叶身侧面与柱廊高度参照',entry_state='两条由低处射向高处的轨迹将交汇；扇叶仍在上行。',action='扇叶从左下向右上击中右下朝左上的暗金术光；小亮点后残光偏散，碰撞失速后叶片才开始落向空侧廊。',exit_state='高处截击完成，千问始终站地护人，GPT空中咏唱继续。')
rule='千问地面发射→单叶上行→半空接触→失速后落向无人侧廊。A11刃尖侧前极特写、强透视缩短；A12绕同轴约70度至侧面低机位、景别拉开、扇叶侧面轮廓。两镜保持叶尾左下/刃尖右上及向上运动，柱线竖直；接触前不得下坠。飞行镜无术光，碰撞镜才出现敌方术光。'
d['continuity']['bullet_time']=rule+' 咏唱跨切自然连续，声音不随子弹时间变调。'
for sid in ['CY024A10','CY024A11','CY024A12']:
    by[sid]['invariants']=list(dict.fromkeys(by[sid]['invariants']+[rule]))
    by[sid]['editorial_review']=dict(version='v034',status='candidate_pending_author_review',dynamic_execution='pending')
d.update(title='《穿云》带图分镜 v0.34 · 扇叶上行与换机位',subtitle='地面发射 · 上行极特写 · 侧面仰拍截击',version='v0.34',revision='v034',story_script='剧本/穿云-场景剧本-v0.34.md',source_manifest='镜头设计/生成记录/生成索引-v034.json')
d['review_intro']='修正单枚扇叶从地面斜向上飞行的方向；飞行用刃尖侧前极特写，撞击改侧面低机位并拉开景别。两镜延续上行轨迹，接触失速后才下落。既有升空、水雷、龙翼、对白及总时长保持。新图待作者审阅，动态与声音未制作。'
d['revision_notes']=dict(previous_manifest='镜头设计/shot-plan-v0.33.json',previous_html='镜头设计/带图分镜-v0.33.html',added_ids=[],modified_ids=['CY024A10','CY024A11','CY024A12'],boundary='仅重做A11/A12两张画面，A10补向上发射动作说明；109镜359秒不变。旧图、旧剧本、旧分镜与冻结请求保留。')
(R/IMG).mkdir(parents=True,exist_ok=True)
records=[]
for sid,src in [('CY024A11',args.flight),('CY024A12',args.impact)]:
    n=3 if sid=='CY024A11' else 1
    source=Path(src).resolve();dest=f'{IMG}/{sid}-v034-r{n}.png';req=f'{REC}/{sid}-请求-v{n:03}.json'
    shutil.copy2(source,R/dest);q=by[sid];spec=json.loads(read(req));w,h=Image.open(R/dest).size
    prev=q['presentation']['path']
    visible='单枚扇叶刃尖朝右上、叶尾左下，前端近镜、叶身透视后退，背景虚化且无敌方术光。' if sid=='CY024A11' else '低机位侧面观察上行扇叶与暗金术光的半空接触，小亮点及柱廊高度参照；景别较飞行镜拉开。'
    q.update(presentation=dict(path=dest,role='action',visible=visible,status='v0.34新静帧候选，待作者审阅',missing='上行伴飞、跨切运动匹配、撞击失速及声音待动态制作验证。',show_as_main=True),page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0.,y=0.,w=1.,h=1.),generation_request=req,visual_prompt=spec['prompt'],refs=[dict(path=dest,role='本轮上行与换机位候选'),dict(path=req,role='冻结实际输入'),dict(path=prev,role='作者否定的下指刃尖与重复角度历史稿')])
    records.append(dict(shot_id=sid,attempt=n,original=str(source),destination=dest,sha256=sha(R/dest),request=req,request_sha256=sha(R/req),inputs=[dict(path=x,sha256=sha(x)) for x in spec['referenced_image_paths']],status='candidate_pending_author_review'))
for n,fn in [(1,'exec-672d5a38-cfbf-4f17-8c4c-fff2fb4002f3.png'),(2,'exec-a18d36c2-5cda-4091-9e73-f5347e3b68d7.png')]:
    source=Path('C:/Users/36322/.codex/generated_images/01a162c1-6e38-7a10-aee7-5c8371c4830c')/fn
    dest=f'{IMG}/CY024A11-v034-r{n}.png';req=f'{REC}/CY024A11-请求-v{n:03}.json';spec=json.loads(read(req))
    records.append(dict(shot_id='CY024A11',attempt=n,original=str(source),destination=dest,sha256=sha(R/dest),request=req,request_sha256=sha(R/req),inputs=[dict(path=x,sha256=sha(x)) for x in spec['referenced_image_paths']],status='superseded_camera_too_similar_to_profile'))
for sc in d['scenes']:
    ss=[s for s in d['shots'] if s['scene']==sc['id']]
    sc['pages']=list(dict.fromkeys(s['presentation']['path'] for s in ss));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
save('镜头设计/生成记录/生成索引-v034.json',dict(version='v034',previous_index=old['source_manifest'],records=records,superseded=[dict(shot_id=sid,path=next(s for s in old['shots'] if s['id']==sid)['presentation']['path'],reason='作者否定：刃尖向下、飞行和碰撞角度重复；原件与旧索引保留。') for sid in ['CY024A11','CY024A12']]))
write(d['story_script'],script);save('镜头设计/shot-plan-v0.34.json',d)
assert not (R/'镜头设计/带图分镜-v0.33.html').exists()
shutil.copy2(R/'镜头设计/带图分镜.html',R/'镜头设计/带图分镜-v0.33.html')
p='scripts/build_storyboard.py';s=read(p).replace('shot-plan-v0.33.json','shot-plan-v0.34.json').replace('"v033")','"v033", "v034")').replace("'v033')","'v033','v034')");write(p,s)
p='00_打开项目.html';s=read(p).replace('v0.33','v0.34');write(p,s)
p='制作进度.md';s=read(p);header='## 2026-10-23：扇叶上行与撞击换机位（v0.34）\n\n作者否定上一版刃尖朝下、飞行与撞击机位重复。CY024A10补右腕上挑、从地面向高处发射；CY024A11改刃尖右上、叶尾左下的侧前方极特写；CY024A12换同轴侧面低机位并拉开景别，柱廊交代高度，两条上行轨迹在半空交汇。撞击失速后才下落。\n\n已同步[剧本v0.34](剧本/穿云-场景剧本-v0.34.md)与[带图分镜](镜头设计/带图分镜.html)。本轮仅两张内置imagegen新候选，旧图与v0.33快照保留；109镜359秒、咒语及声音预算不变。静态画面已检查，动态运动和音效未制作。记录与完整提示词见[复核记录](镜头设计/生成记录/扇叶上行与换机位-v034/复核记录.md)。\n\n'
s=s.replace('## 2026-10-23：展翼升空',header+'## 2026-10-23：展翼升空',1);write(p,s)
print('Created v0.34, two image replacements, 109 shots / 359 sec unchanged.')

