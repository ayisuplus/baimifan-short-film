"""Apply author's raised-blade readability correction without changing timings/music."""
import hashlib,json
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text('utf-8-sig'))
def save(p,d):(R/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
p='镜头设计/shot-plan-v0.42.json';d=load(p)
s=next(s for s in d['shots'] if s['id']=='CY024K4')
req='镜头设计/生成记录/月相阵纹-v042/试镣左臂连接修正请求.json';row=load(req)
image='镜头设计/图像/月相阵纹-v042/CY024K4-v042-r5.png'
before=s['source_quote']
action='Kimi从侧下方用右手暗刃轻试金属腕镣接缝，不高举刀、不朝向Claude身体。腕扣细小符纹突然亮紫光，Claude吃痛；Kimi立刻把暗刃收回自己外侧髋边，刀口朝外下方，与Claude留出清晰空隙，担忧地看向锁扣。关键帧选择已经收刀的一刻，只在金属腕扣上保留将熄的紫纹，刀和皮肤不发紫光。左手明刃贴近自己胸前继续维持共用护罩，腕镣完整；护罩边界在此近景画外，不另画发光月环，不把试锁画成挥刀攻击。'
script=(R/d['story_script']).read_text('utf-8-sig')
assert before in script
script=script.replace(before,action)
(R/d['story_script']).write_text(script,encoding='utf-8')
s.update(action=action,source_quote=action,framing='两人近中景，暗刃已退至外侧髋边，刀与Claude之间清楚留空',exit_state='暗刃收至外侧，锁扣完整，Kimi意识到不能暴力解锁。',visual_prompt=row['prompt'],generation_request=req)
s['presentation'].update(path=image,visible='反噬发生后：暗刃已经退至Kimi外侧髋边、刃口朝外下方；腕扣残余紫纹，Kimi担忧看锁扣，左明刃继续护持。左肘在自身左肋旁（画面右侧），前臂从右下向左上接到握柄；护罩边界在画外，无额外月环。',status='v0.42-r5：收刀、去除歧义月环并重构左臂连接，待作者审阅')
s['refs']=[dict(path=image,role='作者反馈后修订候选'),dict(path='镜头设计/图像/月相阵纹-v042/CY024K4-v042-r1.png',role='作者指出举刀姿态像攻击，历史保留'),dict(path='镜头设计/图像/月相阵纹-v042/CY024K4-v042-r2.png',role='作者指出左侧月环意义不明，历史保留'),dict(path='镜头设计/图像/月相阵纹-v042/CY024K4-v042-r3.png',role='作者指出手臂人体逻辑异常，历史保留'),dict(path='镜头设计/图像/月相阵纹-v042/CY024K4-v042-r4.png',role='左臂接向错侧，独立复核拒绝'),dict(path=req,role='实际生成请求')]
s['cinematic_beats']=[dict(offset=0,intent='侧下轻试金属接缝，不高举或挥砍'),dict(offset=.5,intent='腕扣反噬，立即收刀'),dict(offset=1,intent='暗刃退至外侧髋边，留清晰空隙；关键帧与后半停顿')]
with Image.open(R/image) as im:w,h=im.size
s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h])
for i,x in enumerate(d['shots'][:-1]):x['next_link']='接 '+d['shots'][i+1]['id']+'：'+d['shots'][i+1]['entry_state']
for sc in d['scenes']:sc['pages']=list(dict.fromkeys(x['presentation']['path'] for x in d['shots'] if x['scene']==sc['id']))
d['page_layouts']=[dict(path=x['presentation']['path'],rows=1,cols=1) for x in d['shots']]
save(p,d)
a=load(d['audio_arrangement']);a['shot_plan_sha256']=sha(p);save(d['audio_arrangement'],a)
ix=load(d['source_manifest']);item=next(x for x in ix['images'] if x['id']=='CY024K4')
item.update(path=image,sha256=sha(image),size=[w,h],request=req,inputs=[dict(path=q,sha256=sha(q)) for q in row['refs']])
note='K4r1高举刀像攻击，r2退刀但边缘月环歧义，r3去环但手臂逻辑被指出，r4左臂仍接错侧；r5重构左肩肘腕连接'
if note not in ix['not_used']:ix['not_used'].append(note)
save(d['source_manifest'],ix)
rows=[];selected={x['path'] for x in ix['images']}
for f in sorted((R/'镜头设计/图像/月相阵纹-v042').glob('*.png')):
 q=f.relative_to(R).as_posix()
 with Image.open(f) as im:size=list(im.size)
 rows.append(dict(path=q,bytes=f.stat().st_size,sha256=sha(q),size=size,status='current_candidate_pending_author_review' if q in selected else 'superseded_preserved'))
save('镜头设计/生成记录/月相阵纹-v042/文件核验.json',rows)
check=load('镜头设计/生成记录/月相阵纹-v042/核验.json');check.update(stored_images=len(rows),author_feedback_k4='r1 attacking read; r2 extra moon ring; r3/r4 arm connection rejected; r5 rebuilt left shoulder-elbow-wrist chain, pending author review');save('镜头设计/生成记录/月相阵纹-v042/核验.json',check)
print('K4 r5 bound, source and audio hash synchronized.')
