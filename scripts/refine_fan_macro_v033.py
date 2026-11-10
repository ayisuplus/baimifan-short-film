"""Apply the author's final close-up correction within the uncommitted v033 revision."""
import json,hashlib,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];REC='镜头设计/生成记录/展翼与扇面-v033';IMG='镜头设计/图像/展翼与扇叶-v033'
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,t):(R/p).write_text(t,encoding='utf-8')
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p='镜头设计/shot-plan-v0.33.json';d=json.loads(read(p));by={s['id']:s for s in d['shots']};s=by['CY024A10']
assert not s['presentation']['path'].endswith('-r3.png'),'macro already applied'
old=s['source_quote']
new='''切千问右手与扇轴的极近特写，人脸和抱孩子的左臂留在画外。她拇指轻拨扇轴的小卡扣，发出一声很短的“咔”；手腕一抖，扇骨依次展开，几声细密的金属轻响沿展开动作铺开。蓝白花纹扇叶和细金扇骨占满画面，扇柄仍握在右手，原折扇并未被扔出。

开扇到位，外缘一枚狭长实体扇叶的卡扣再轻响一次，叶片尖端微微抬起。镜头末端只让这单枚扇叶脱离固定处，立即切下一镜伴飞；不在这个特写里再展示千问全身或一整片扇面飞出。她的左臂始终在画外托住小鱼，未交接孩子。'''
t=read(d['story_script']);assert old in t;t=t.replace(old,new,1);write(d['story_script'],t)
s.update(title='开扇咔响，单叶解锁',seconds=2,framing='右手、扇轴与扇骨极近特写／浅景深',purpose='让观众先看清开扇与单叶解锁，再接暗器飞行；机械轻响强化精巧结构。',entry_state='教主术光已射出；千问左臂抱稳小鱼，右手持尚未完全展开的扇子。',action='拇指拨扣，甩腕开扇，扇骨依次展开；外缘单叶卡扣解锁，末端弹离，切伴飞。孩子始终由画外左臂托稳。',exit_state='原扇仍握在右手，只有一枚狭长实体扇叶已离开外缘固定处；接暗器飞行。',source_quote=new,sound='0.15秒扇轴短咔；0.3—1.1秒扇骨依次展开的轻细金属声；1.4秒单叶卡扣轻响，1.7秒弹脱破空接下镜。声音轻而脆，不用枪械上膛、重齿轮或引擎声。GPT画外第二句连续，机械声避开人声。正式音效未制作。',cinematic_beats=[dict(offset=0.15,intent='扇轴卡扣短咔'),dict(offset=0.3,intent='扇骨依次打开'),dict(offset=1.4,intent='外缘单叶卡扣解锁'),dict(offset=1.7,intent='单叶弹脱，切飞行')])
s['subtitle_cues'][0]['duration']=2
by['CY024A1']['seconds']=3;by['CY024A1']['subtitle_cues'][0]['duration']=2.9
source=Path('C:/Users/36322/.codex/generated_images/01a162c1-6e38-7a10-aee7-5c8371c4830c/exec-446b3629-dcdd-4b2d-82e0-cafb725524c5.png')
dest=f'{IMG}/CY024A10-v033-r3.png';req=f'{REC}/CY024A10-请求-v003.json';shutil.copy2(source,R/dest)
args=json.loads(read(req));w,h=Image.open(R/dest).size
s.update(presentation=dict(path=dest,role='action',visible='右手握住扇轴，折扇接近完全展开，外缘单叶仍在扇上待发；金色扇骨和小卡扣可辨。',status='v0.33开扇特写新候选，待作者审阅',missing='静帧代表开扇到位前后，拨扣/展开/单叶弹脱及机械音效尚未制作；左臂抱人保持在画外。',show_as_main=True),page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0.,y=0.,w=1.,h=1.),generation_request=req,visual_prompt=args['prompt'],refs=[dict(path=dest,role='本轮开扇特写候选'),dict(path=req,role='冻结实际输入'),dict(path=f'{IMG}/CY024A10-v033-r2.png',role='作者否定的旧全人像发射构图，保留'),dict(path='资产/图像/四视图复用/C04_Qwen-角色设定卡.png',role='扇子与服饰参考')])
d['music_direction']['incantation_bridge']['rule']='前半句5秒跨教主1秒/开扇2秒/单叶飞行2秒，后半句3秒在Kimi镜收尾，只念一次。'
d['music_direction']['rule']=d['music_direction']['rule'].replace('千问弹叶','千问开扇卡扣与单叶弹脱')
d['review_focus']=d['review_focus'].replace('右手单叶脱扇','右手开扇卡扣特写/单叶脱扇')
d['revision_notes']['boundary']=d['revision_notes']['boundary'].replace('5张中间稿','6张中间稿')+' 作者后续否定A10全人像发射图，改开扇极近特写配机械轻响；A10加1秒、Kimi起护收1秒，全片时长不变。'
d['continuity']['qwen_fan_intercept']+=' CY024A10仅拍右手开扇，左臂抱小鱼在画外延续；两秒含扇轴咔响、扇骨轻响与单叶卡扣解锁。'
elapsed=0
for shot in d['shots']:shot['start_second']=elapsed;elapsed+=shot['seconds'];shot['end_second']=elapsed
assert elapsed==358
for sc in d['scenes']:
 ss=[q for q in d['shots'] if q['scene']==sc['id']];sc.update(seconds=sum(q['seconds'] for q in ss),pages=list(dict.fromkeys(q['presentation']['path'] for q in ss)));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=q['presentation']['path'],rows=1,cols=1) for q in d['shots']]
save(p,d)
idxp='镜头设计/生成记录/生成索引-v033.json';idx=json.loads(read(idxp))
for r in idx['records']:
 if r['shot_id']=='CY024A10' and r['attempt']==2:r['status']='rejected_author_prefers_fan_opening_macro'
idx['records'].append(dict(shot_id='CY024A10',attempt=3,original=str(source),destination=dest,sha256=sha(R/dest),request=req,request_sha256=sha(R/req),inputs=[dict(path=p,sha256=sha(p)) for p in args['referenced_image_paths']],status='candidate_pending_author_review'))
save(idxp,idx)
outp=REC+'/输出映射.json';rows=json.loads(read(outp))
for r in rows:
 if r['id']=='CY024A10' and r['attempt']==2:r['status']='rejected_author_prefers_fan_opening_macro'
rows.append(dict(id='CY024A10',attempt=3,original=str(source),status='candidate_pending_author_review'));save(outp,rows)
p='制作进度.md';x=read(p).replace('CY024A10千问左臂托抱/右手弹出单叶','CY024A10右手开扇与卡扣特写（左臂画外托抱）').replace('共4秒；咏唱第二句','共5秒；Kimi起护由4秒收至3秒，咏唱第二句').replace('5张中间稿保留','6张中间稿保留');write(p,x)
p='00_打开项目.html';write(p,read(p).replace('千问单片实体扇叶 · 子弹时间','开扇特写与机械轻响 · 单片实体扇叶 · 子弹时间'))
print('Final fan macro applied. 108 shots358seconds unchanged;17 current frames,23 attempts.')
