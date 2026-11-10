"""Two camera revisions only; keep timing, dialogue and adopted music unchanged."""
import copy, hashlib, json, shutil
from pathlib import Path
from PIL import Image

R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/冲击机位-v051'
def load(p): return json.loads((R/p).read_text(encoding='utf-8-sig'))
def save(p,v):
    q=R/p;q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=load('镜头设计/shot-plan-v0.50.json');p=copy.deepcopy(base)
old={s['id']:s for s in base['shots']};by={s['id']:s for s in p['shots']}
script=(R/base['story_script']).read_text(encoding='utf-8')
changes={
 'CY024A5A':dict(
  title='贴近破口，水首掠镜',framing='18mm超广角贴近破口下沿仰拍，轻微倾斜，龙首强透视冲向近前景',
  action='承接俯视镜末的同一撞点，机位藏在中殿穹顶破口下沿，偏离水龙轴线，以超广角向上迎拍。龙首从左上远处猛冲向右下近处，鼻吻和下颌迅速放大并掠出画边，长颈缩向同一破口，保留龙眉与一只眼的清晰体积。近前景一块断拱石擦过画边，后层小碎石与粉尘沿冲势飞落，形成明确的近大远小；运动模糊集中于碎石边缘与背景，水首关键轮廓仍清楚。先听石材断裂，后见厚重水腹掠过机位；摄影机只在擦过瞬间短促受震，不持续乱抖。水龙进入中殿后转向GPT外侧，碎块落往无人侧廊，避开吊灯和友方。始终只有中央中殿同一个破口，后殿不受损；接Kimi与教主反应切镜，跨切完成回卷盘身。',
  purpose='用贴近破口的迎面透视表现俯冲速度与石材重量，不再完整陈列龙首。',
  sound='近处一记干脆石裂接低频破顶重击，碎石擦过声由近到远，水啸快速掠过；无对白和雷电声。',
  beats=[dict(offset=0,intent='切入同一破口下沿，龙首由远逼近'),dict(offset=.45,intent='鼻吻迅速放大，断拱石擦过画边'),dict(offset=1.05,intent='水腹掠镜，一次短震后切入反应镜')]),
 'CY024B':dict(
  title='低机位撞盾，水首压境',framing='24mm膝高侧后近景，教主前景右侧，水龙从左上压向右下接触点',
  action='承接GPT一次前指，切到教主侧后方、护罩外的膝高低机位，保持水龙从左上冲向右下的屏幕方向。教主在右侧近前景以错步屈膝站稳，双臂上举撑住已经成形的暗金罩，仰头迎着压来的龙首；没有跪下或转身逃跑。巨大龙首从高处压入金罩左上弧面，鼻吻在直接接触处才碎成厚重白浪，眉骨、眼和后颈仍可辨，不留空隙、不张口吐水。金罩在同一接触点局部压平，金色纹路沿罩面扩开，放射水幕从接触区向画边掀出；教主外袍向后翻起，身体承压后移但尚未跌倒。后随水身继续冲入，画面下缘的余水沿两侧石阶冲散边缘教徒并扑灭残柴。GPT和最高祭坛此镜均在画外；友方暗月罩与中央上层石阶仍保持干燥净空，后续B3再交代整体安全空间。镜末水首完全散成浪，画外GPT收势停止补水，余水继续下行；不新增破口、不破侧窗，不让友方护罩承受水流。',
  purpose='把观看位置移到受击者附近，以人物撑盾、龙首尺度和接触变形表现压力；安全区由后续镜头交代。',
  sound='龙首贴盾的一记低沉撞击，接短促罩面共振；厚水拍石与衣袍急响随后展开，教徒惊呼退到两侧。无雷电与友方罩受击声。',
  beats=[dict(offset=0,intent='金罩已经成立，教主撑盾，龙首直接压入'),dict(offset=.8,intent='罩面局部压平，吻部化浪，袍摆后掀'),dict(offset=2.2,intent='后随水身涌入，两侧教徒失衡'),dict(offset=4,intent='画外收势停供水，余浪向外侧石阶下行')])}

records=load(REC+'/实际请求.json');assert {r['id'] for r in records}==set(changes)
for row in records:
    sid=row['id'];s=by[sid];v=changes[sid]
    s.update({k:v[k] for k in ['title','framing','action','purpose','sound']})
    s['cinematic_beats']=v['beats'];s['source_quote']=s['action']
    assert old[sid]['source_quote'] in script
    script=script.replace(old[sid]['source_quote'],s['source_quote'],1)
    dest=R/f'镜头设计/图像/冲击机位-v051/{sid}-v051-r1.png';dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(row['source'],dest)
    with Image.open(dest) as im:w,h=im.size;im.verify()
    rel=dest.relative_to(R).as_posix();req=REC+'/'+sid+'.json'
    save(req,dict(row,output=rel,sha256=sha(dest),dimensions=[w,h],engine='built-in image_gen',status='pending_author_visual_review'))
    s['previous_presentation_v050']=copy.deepcopy(old[sid]['presentation'])
    s['previous_generation_request_v050']=old[sid]['generation_request']
    s['presentation'].update(path=rel,visible=s['action'],status='v0.51机位修订，待作者视觉审阅',missing='静帧表现关键冲击状态；贴镜掠过、护罩形变与反应节奏待动态制作。')
    s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],visual_prompt=row['input']['prompt'],generation_request=req,editorial_review=dict(version='v051',status='pending_author_review',dynamic_execution='pending'),final_static_review=dict(version='v051',status='pending_author_visual_review'))
    s['refs'].append(dict(path=rel,role='v0.51机位修订候选，保留旧图'))
for sc in p['scenes']:
    sc['pages']=list(dict.fromkeys(s['presentation']['path'] for s in p['shots'] if s['scene']==sc['id']))
p['page_layouts']=[dict(path=path,rows=1,cols=1) for path in dict.fromkeys(s['presentation']['path'] for s in p['shots'])]
p.update(version='v0.51',picture_revision='v051',report_revision='v051',title='《穿云》带图分镜 v0.51 · 贴镜破顶与低机位撞盾',source_manifest='镜头设计/shot-plan-v0.50.json',story_script='剧本/穿云-场景剧本-v0.51.md',audio_arrangement='后期/冲击机位-v051/预演编排.json')
p['review_intro']='破顶特写改为超广角贴近破口迎拍；撞盾改为教主侧后低机位，集中表现龙首压盾、罩面变形与后浪。结印盘龙、一次前指、七首BGM和全部时点保持。'
p['review_focus']='比较两镜的近远尺度、接触点和受击压力。新图待作者视觉确认，动态和声音制作尚未完成。'
p['revision_notes']=dict(previous_manifest=p['source_manifest'],modified_image_ids=list(changes),added_ids=[],moved_ids=[],boundary='只重构两镜机位、可见动作及音效说明；131镜431.5秒、全部对白字幕及BGM归属保持。')
script=script.replace('版本：v0.50','版本：v0.51',1)
(R/p['story_script']).write_text(script,encoding='utf-8')
out='镜头设计/shot-plan-v0.51.json';save(out,p)
audio=load(base['audio_arrangement'])
for sid in changes:audio['effects'][sid]=by[sid]['sound']
audio.update(version='v051-impact-camera-seven-tracks',shot_plan=out,shot_plan_sha256=sha(R/out),previous=base['audio_arrangement'])
save(p['audio_arrangement'],audio)
assert p['music_adoption']==base['music_adoption']
assert audio['adopted_music']==load(base['audio_arrangement'])['adopted_music']
assert [s['id'] for s in p['shots']]==[s['id'] for s in base['shots']]
for s in p['shots']:
    for k in ['seconds','start_second','end_second','dialogue','dialogue_cues','subtitle_cues']:
        assert s.get(k)==old[s['id']].get(k),(s['id'],k)
    assert s['source_quote'] in script,s['id']
    if s['id'] not in changes:assert s==old[s['id']],s['id']
snapshot=R/'镜头设计/带图分镜-结印盘龙-v050.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
save(REC+'/变更核验.json',dict(shots=131,seconds=431.5,changed_shots=list(changes),unchanged_shots=129,timing='unchanged',dialogue='unchanged',music='seven_author_tracks_unchanged',source_passages='131_matched',dynamic_validation='pending'))
print(out)
