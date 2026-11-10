"""Version the approved mathematical palace decoration direction, preserving story and sound."""
import copy,hashlib,json,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
SRC='镜头设计/shot-plan-v0.56.json';OLD='镜头设计/shot-plan-v0.55.json'
REC='镜头设计/生成记录/数学宫殿-v056';IMG='镜头设计/图像/数学宫殿-v056';OUT='视频制作/生成板-v006'
if (R/SRC).exists():raise SystemExit('v0.56 exists; will not overwrite. Use build scripts to render.')
def load(f):return json.loads((R/f).read_text('utf-8-sig'))
def save(f,d):
 p=R/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
def sha(f):return hashlib.sha256((R/f).read_bytes()).hexdigest()
def rep(v,a,b):
 if isinstance(v,str):return v.replace(a,b)
 if isinstance(v,list):return [rep(x,a,b) for x in v]
 if isinstance(v,dict):return {k:rep(x,a,b) for k,x in v.items()}
 return v
base=load(OLD);p=copy.deepcopy(base);by={s['id']:s for s in p['shots']}
ids=['CY005','CY006','CY007','CY008','CY009','CY009A']
decor='殿内两侧灯具为金色正十二面体骨架包乳白柔光芯，骨架不发光；高处少量倾斜椭圆金环吊灯。正面看卧榻，头端左侧小几放几何手稿、圆规、透明多面体压纸、茶杯和莫比乌斯带状小灯，脚端右侧摆环仪与多面体。墙面局部交圆及对称纹样，主龙徽保留。所有摆件在侧边，中央通道和台阶留空，白金淡紫本色及柔和暮光保持。反向过肩时王座、小几在机后画外；近景不强行塞入画外摆件。'
for sid in ids:
 s=by[sid];old=s['presentation']['path'];new=f'{IMG}/{sid}.png';assert (R/new).is_file()
 s['previous_presentation_v055']=copy.deepcopy(s['presentation'])
 s['presentation'].update(path=new,status='数学宫殿方向作者认可；本轮新静帧待作者审阅')
 s['presentation']['visible']+=' 背景按数学宫殿版本呈现几何柔光灯及画幅内摆件。'
 s['refs'].insert(0,{'path':new,'role':'当前数学宫殿构图/状态参考；人物身份仍用四视图'})
 for ref in s['refs'][1:]:
  if ref['path']==old:ref['role']='历史宫殿装饰版本，保留，不作为当前灯具参考'
 s['invariants'].append(decor)
 s['generation_request']=REC+'/实际请求.json'
 s['editorial_review']={'version':'v056','status':'pending_author_review','dynamic_execution':'pending'}
 s['final_static_review']={'version':'v056','status':'pending_author_review'}
 w,h=Image.open(R/new).size;s['page_size']=[w,h];s['panel_rect_pixels']=[0,0,w,h]
 p['scenes']=rep(p['scenes'],old,new);p['page_layouts']=rep(p['page_layouts'],old,new)
oldquote=by['CY005']['source_quote']
addition=' 卧榻头端的小几上摆着翻开的几何手稿、圆规、透明多面体压纸和茶杯，旁边一盏扭转带状小灯泛着柔光；另一端的环仪与多面体安静陈列。殿内两侧的十二面体灯罩包着乳白灯芯，高处悬着少量倾斜椭圆金环，墙面交圆纹样与原有龙徽并存。中央长廊与台阶仍然畅通。'
script=(R/base['story_script']).read_text('utf-8-sig');assert oldquote in script
by['CY005']['source_quote']=oldquote+addition;script=script.replace(oldquote,oldquote+addition,1)
script=script.replace('版本：v0.55｜2026-10-26｜宫殿对称卧榻、慵懒侧躺与起身目送；既定对白和后段救援保持。','版本：v0.56｜2026-10-26｜数学宫殿灯具与生活摆件；躺姿、搓手、过肩目送及既定对白保持。')
p.update(version='v0.56',title='《白米饭》带图分镜 v0.56 · 数学宫殿',subtitle='132镜 · 435.5秒 · 几何柔光灯、数学手稿与慵懒龙',source_manifest=OLD,story_script='剧本/白米饭-场景剧本-v0.56.md',picture_revision='v056',report_revision='v056',audio_arrangement='后期/数学宫殿-v056/预演编排.json',music_adoption='后期/数学宫殿-v056/作者确认选曲.json',review_intro='宫殿六镜更新数学灯具与生活摆件；搓手特写、人物动作、对白与选曲保持。',review_focus='十二面体灯、头端小几与脚端环仪的跨镜位置；近景及反向过肩仅显示实际取景范围。')
p['continuity']['mathematical_palace']=decor
(R/p['story_script']).write_text(script,'utf-8');save(SRC,p)
oldhash=sha(OLD);newhash=sha(SRC)
for name in ['预演编排.json','作者确认选曲.json']:
 d=load('后期/宫殿躺姿-v055/'+name)
 for a,b in [(OLD,SRC),(oldhash,newhash),('后期/宫殿躺姿-v055','后期/数学宫殿-v056')]:d=rep(d,a,b)
 d['version']='v056';d['previous']='后期/宫殿躺姿-v055/'+name;save('后期/数学宫殿-v056/'+name,d)
for name in ['批次计划.json','人物核对.json','声音核对.json','动态审查.json']:
 d=load('视频制作/生成板-v005/'+name)
 for a,b in [('视频制作/生成板-v005',OUT),(OLD,SRC),(oldhash,newhash)]:d=rep(d,a,b)
 if 'version' in d:d['version']='v006'
 if name=='批次计划.json':
  d['navigation']['review']=REC+'/审查与交付.md'
  for sid in ids:d['shot_notes'][sid]=d.get('shot_notes',{}).get(sid,'')+' 当前背景采用数学宫殿灯具；按本镜实际视野显示，不挪摆件、不新增人物。'
 save(OUT+'/'+name,d)
zh={
 'CY005':'环境：左侧卧榻头端小几放几何手稿、圆规、透明多面体压纸、茶杯与扭转带小灯，右侧脚端陈列环仪；两侧十二面体柔光灯、高处椭圆环吊灯，中央台阶与通道留空。',
 'CY006':'背景沿用同位置的十二面体金色灯罩与乳白柔光芯，花架不变；此近景不显示画外的小几与吊灯。',
 'CY007':'背景灯罩沿用十二面体金色骨架和乳白柔光芯；卧榻与人物姿态不变，画外小几和吊灯不硬塞入近景。',
 'CY008':'后景十二面体灯、花架及软垫边与前一小鱼近景同位置；不出现画外小几和吊灯。',
 'CY009':'延续入殿远景的数学装饰：头端小几在画面左、脚端环仪在右，十二面体柔光灯与高处环灯同款，孩子走动通道留空。',
 'CY009A':'只见沿长廊两侧的十二面体柔光灯与远处高悬椭圆环灯；王座和手稿小几在机后画外，不搬到远门口。'
}
en={
 'CY005':'Environment: a study table at the head end on screen left carries geometry sketches, compass, transparent polyhedron paperweight, tea cup and twisted-ribbon desk lamp; the foot-end ring instrument is on screen right. Gold dodecahedron opal lamps flank the clear aisle, with a few inclined ellipse-ring chandeliers high above. No candles or glowing frames.',
 'CY006':'Keep the background flower stands and matching gold dodecahedron lamps with opal cores at their established positions. The study table and ceiling chandelier are outside this close crop.',
 'CY007':'Background lamps have gold dodecahedral frames and soft opal cores. Keep the throne and pose; do not insert the offscreen study table or ceiling chandelier into this close shot.',
 'CY008':'Match the preceding child close-up: identical background dodecahedron lamp positions, flower stands and blurred cushion edge. No offscreen desk or chandelier enters the crop.',
 'CY009':'Match the arrival shot decor: head-end study table on screen left, foot-end ring instrument on right, gold dodecahedron opal lamps and high ellipse-ring chandelier. Keep the walking route empty.',
 'CY009A':'Only the corridor lamps and distant high ellipse-ring chandelier are visible. Use gold dodecahedron cages with soft opal cores; the throne and study table stay behind camera, never move them to the far door.'
}
d=load(OUT+'/动态审查.json')
for b in d['batches'].values():
 for sid,v in b['shots'].items():
  if sid in ids:
   v['action_zh_override']=v.get('action_zh_override',by[sid]['action'])+' '+zh[sid]
   v['action_en']=v['action_en']+' '+en[sid]
save(OUT+'/动态审查.json',d)
a=load('资产/assets.json');env=next(x for x in a['assets'] if x['id']=='ENV-PALACE');prev=copy.deepcopy(env)
env.update(name='宫殿 · 数学灯具与卧榻书案',version='v056',status='作者认可数学装饰方向；新图待审',path=IMG+'/CY005.png',role=decor,source=REC+'/实际请求.json',limits='S02宫殿环境参考，不替代人物四视图。静帧中的几何设计供美术参考，不是制造图；莫比乌斯带在远景的拓扑未作严格验证。')
env['previous_v055']=prev;env['related']=[{'path':IMG+'/CY009A.png','role':'反向紧过肩与长廊灯具'},{'path':IMG+'/CY007.png','role':'卧榻近景与背景几何灯'},{'path':prev['path'],'role':'历史宫殿装饰与卧榻参考，保留'}]+prev['related']
save('资产/assets.json',a)
jobs=load(REC+'/实际请求.json')
for j in jobs['jobs']:
 j['sha256']=sha(j['output']);j['dimensions']=list(Image.open(R/j['output']).size)
save(REC+'/实际请求.json',jobs)
shutil.copy2(R/'镜头设计/带图分镜.html',R/'镜头设计/带图分镜-v055.html')
for f in ['scripts/build_storyboard.py','scripts/build_generation_board.py','scripts/verify_generation_board.py','00_打开项目.html','AGENTS.md']:
 file=R/f;t=file.read_text('utf-8-sig').replace('shot-plan-v0.55.json','shot-plan-v0.56.json').replace('生成板-v005','生成板-v006').replace('v0.55','v0.56')
 if f=='AGENTS.md':t=t.replace('v003与v004全片旧版保留历史','v003、v004与v005全片旧版保留历史')
 file.write_text(t,'utf-8')
for x,y in zip(base['shots'],p['shots']):
 for k in ['id','seconds','start_second','end_second','action','entry_state','exit_state','dialogue','dialogue_cues','framing']:assert x.get(k)==y.get(k),(y['id'],k)
assert all(s['source_quote'] in script for s in p['shots'])
assert load(base['music_adoption'])['marks']==load(p['music_adoption'])['marks']
save(REC+'/变更核验.json',{'shots':132,'seconds':435.5,'new_images':ids,'reused_hand_closeup':by['CY010']['presentation']['path'],'timing_dialogue_actions_framing_unchanged':True,'music_marks_unchanged':True,'source_quotes_verified':132,'previous_source':OLD,'source':SRC,'source_sha256':newhash,'scope':'静帧与文本；未生成动态视频或重新听审'})
print(json.dumps({'source':SRC,'source_sha256':newhash,'new_images':len(ids)},ensure_ascii=False))
