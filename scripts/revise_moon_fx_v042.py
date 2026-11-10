"""Version the grounded lunar VFX sequence; preserve old shots and music choices."""
import copy, hashlib, json, shutil
from pathlib import Path
from PIL import Image

R=Path(__file__).resolve().parents[1]
PLAN='镜头设计/shot-plan-v0.42.json'
REC='镜头设计/生成记录/月相阵纹-v042'
IMG='镜头设计/图像/月相阵纹-v042'
def read(p):return (R/p).read_text('utf-8-sig')
def load(p):return json.loads(read(p))
def write(p,t):
 (R/p).parent.mkdir(parents=True,exist_ok=True)
 (R/p).write_text(t,encoding='utf-8')
def save(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
assert not (R/PLAN).exists(),'One-time migration: v042 already exists.'
d=load('镜头设计/shot-plan-v0.41.json');old=copy.deepcopy(d)
by={s['id']:s for s in d['shots']}
script=read(d['story_script'])
changes={
'CY024K0':('刑架背后偏左高窗仍然完整，实月的冷光透过蓝玻璃和浮尘落入殿内。人没有露面，一句低声咏唱从窗外传来。此时没有阵纹或护盾抢先亮起。','窗外短咏，殿内火声保持；无魔法启动重音'),
'CY024K1':('彩窗破开的瞬间，真实月光勾出Kimi轮廓。她双持一暗一明的小圆月刃，从刑架背后偏左彩窗上部斜向下扑向最高祭坛左侧空石地。碎玻璃沿墙侧落下，避开Claude；高柴仍燃，尚未劈动。刃缘只留短促反光，空中不出现阵纹或护盾；镜末前脚即将触地。','清脆破窗、玻璃沿墙侧坠落、衣摆破风；落地重音留给下一镜'),
'CY024K2':('落脚月阵的两端沿石面伸向刑架。Kimi屈膝稳住重心，举起左手明月刃；细光从Claude衣料与外侧高柴之间向上展开，与Kimi身周合拢，先把两人和固定脚托护住。护罩刚闭合时上缘一闪，随即转为近透明，只在贴近黑焰处出现局部折射和亮边。脚下只有一枚贴地弯月阵纹，光被鞋底遮住、被石缝打断，并照亮附近靴边与裙褶。右手暗刃暂不挥动；高柴仍堆到Claude腰腹，全部留在罩外。','落脚低频余音延续，细光上行，闭合时一声短促低鸣，随即压低'),
'CY024K3':('护罩已经闭合，脚下弯月阵纹降至低亮。Kimi压低重心、转胯，左手明刃维持保护，右手暗刃实体切进乌烬木接缝；刃口触木的一瞬才闪出短促暗银弧光。切开的木段沿月牙内缘被勾向两侧外下方，沉重地落地，避开刑架、脚托和束具，不做漫天漂浮碎片。Claude直立的裙摆、锁着的双踝和脚下固定窄脚托逐渐露出。残柴仍燃紫黑火，全部在罩外；透明罩面保持安静，不与劈柴抢亮。','刀刃触木短响→木纤维裂开→重木落石；无持续激光声'),
'CY024K4':('Kimi用右手暗刃轻试Claude腕镣的接缝。护罩处于低亮透明维持态，画面只在腕扣细小符纹上突然亮紫光；Claude痛得闭眼缩肩。Kimi立刻收回刀锋，继续守住她；腕镣没有断开，左手明刃持续护持。镜头不露地面，不另画一枚悬浮月阵。','轻触金属、腕镣短促刺鸣、立刻收刀；护罩底声压低'),
'CY024A1':('切最高祭坛左侧的Kimi。她停下试镣，左手明刃贴近胸前维持保护，右手暗刃低垂戒备，侧耳听向中殿雷声。脚下同一枚弯月阵纹低亮，护罩只剩边缘微弱折射，罩面不铺星月图案。Claude仍直立在刑架上，双腕双踝受缚、赤足踩固定窄脚托，残柴只在罩外低处燃烧。\n\n第二句咏唱从前面的阻击连续接来，至本镜念完；不重复起句。','GPT承前咏唱、远处雷声；月阵维持低鸣，不新增启动声'),
'CY024A2':('透过近透明护罩看Claude苍白汗湿的脸。她仍直立，双腕固定横木；黑焰只从画面外侧映出紫边。护罩边缘仅在画面一侧造成微弱烛光折射，不用花纹光带横穿脸和胸口。她缓回一口气，焦损袖边和头纱没有恢复；月阵在画外持续，不在特写里另生符号。','咏唱连续、Claude轻缓呼吸、罩外低火声'),
'CY024A4':('切固定脚托、踝链与裙边局部。Claude双腿自然垂直、双踝仍锁着，赤足踩十字架立柱上的窄脚托。中央柴已经让开，画外Kimi月阵延出的低亮地面弧线从左下掠过石缝；它只是共用结界的一段边缘，不围着Claude另起完整光环或小护罩。紫黑火只留两侧罩外散柴，外裙焦损保留，内层衣料完整。','承接咏唱、罩外低火声；不重复阵纹点亮音'),
'CY024B3':('水雷侧浪从左侧抵达最高祭坛。Kimi前膝压低、后脚抵地，双臂交架，把右暗左明的小圆月刃扣在胸前顶住冲击。脚下同一枚贴地弯月短暂增亮；透明护罩迎水面被压扁，只有接触区骤亮并沿弧面传出两三道迅速衰减的涟漪。厚水堆起后沿罩外绕开，背向冲击的一侧仍暗而清透。Claude在她身后直立受缚，腕踝锁扣与固定脚托完整。散柴已熄灭，魔法雷只在罩外偏转；紫电先收尽，再接清水余浪。','重水撞罩一记低沉冲击，短促绷紧声随涟漪衰减，再剩绕流轰鸣'),
'CY027F2':('省略登阶过程，GPT来到最高祭坛，与一直守在Claude左侧的Kimi会合。确认危险解除，Kimi撤去共用护罩，脚下弯月阵纹同时熄灭；她将双月刃扣入后腰固定环，腾出双手。GPT把从教主处取来的黑铁钥匙交到她掌心；Claude此时仍直立，双腕与双踝都锁着。','护罩与地阵低鸣一同收尽、收刃卡扣、钥匙落掌')}
for sid,(action,sound) in changes.items():
 s=by[sid];before=s['source_quote'];assert s['action'] in before,sid
 after=before.replace(s['action'],action)
 assert before in script,sid
 script=script.replace(before,after)
 s.update(action=action,source_quote=after,sound=sound)
 s['presentation']['visible']=action
 # Remove inherited action beats that referred to an unrelated old shot.
 s['cinematic_beats']=[dict(offset=0,intent=action.split('。')[0])]

insert=copy.deepcopy(by['CY024K2'])
insert.update(id='CY024K1A',title='落脚，弯月沿石面点亮',seconds=1.5,
 framing='贴地低机位脚部特写，鞋底接触与月阵透视同框',
 purpose='把动作接触、月阵起源和护罩成形分成可读的先后。',
 entry_state='Kimi从后窗下落，前脚即将落在最高祭坛左侧空石面；尚未撑盾。',
 action='Kimi前脚压实石地，屈膝卸力，尘粒被震向两侧。一枚银白弯月阵纹从鞋底接触点沿石面勾亮，先近弧、后两尖，月尖朝向刑架。阵纹紧贴石面，在透视中压成弧形，鞋底遮住光、石缝切断细纹，局部反光托亮靴边与裙底；没有悬浮光盘，护罩还未升起。',
 exit_state='脚步落稳，地面弯月已点亮，接明刃撑盾。',dialogue='无对白',
 sound='一记结实的落脚低音、石面尘粒擦响，银光短促上扬；没有第二句咏唱',
 dialogue_cues=[],asset_ids=['MULKZI2WMFNJE','ENV-CHURCH'])
for key in ['subtitle_cues','time_caption','split_screen_reveal','dialogue_timing_status']:
 insert.pop(key,None)
insert['source_quote']=insert['action']
insert['cinematic_beats']=[dict(offset=0,intent='前脚压实石地，尘粒外扩'),dict(offset=0.35,intent='近弧亮起，沿地面走向两尖'),dict(offset=1.1,intent='阵纹连通，接明刃撑盾')]
script=script.replace(by['CY024K2']['source_quote'],insert['source_quote']+'\n\n'+by['CY024K2']['source_quote'])
i=d['shots'].index(by['CY024K1']);d['shots'].insert(i+1,insert);by[insert['id']]=insert
by['CY024K1']['exit_state']='前脚即将触地，月阵与护罩尚未出现。'
by['CY024K2']['entry_state']='Kimi落脚，贴地弯月刚点亮；高柴仍围住Claude腰腹。'
by['CY024K2']['exit_state']='双人护罩已经闭合，高柴未劈；接暗刃触木。'
by['CY027F2']['exit_state']='护罩与地阵均熄灭，双刃收好，Kimi拿到钥匙。'
beats={
 'CY024K0':[(0,'实月透窗，画外短咏；无魔法阵')],
 'CY024K1':[(0,'破窗逆光'),(1,'双刃护身斜向下落'),(2.6,'前脚将触地，接落脚特写')],
 'CY024K2':[(0,'弯月阵纹沿地延向刑架'),(.6,'左明刃抬起，罩缘从内侧上行'),(1.8,'双人罩闭合、上缘一闪'),(2.5,'转低亮维持，高柴仍未劈')],
 'CY024K3':[(0,'低重心转胯，暗刃实体入木'),(.7,'接触处短闪，木段裂开'),(1.8,'向外下方勾拨，木头落地'),(3.2,'中央净空，腕踝与脚托露出')],
 'CY024K4':[(0,'轻试腕扣'),(.7,'符纹亮，Claude吃痛'),(1.1,'立刻收刃，护罩持续')],
 'CY024A1':[(0,'护罩低亮，Kimi听向雷声；GPT承前念完古老意志啊')],
 'CY024B3':[(0,'侧浪抵达，双刃交架'),(.4,'接触区骤亮、迎水面压扁'),(1.4,'涟漪衰减，水向两侧绕流'),(2.6,'紫电收尽，接清水余浪')]
}
for sid,rows in beats.items():by[sid]['cinematic_beats']=[dict(offset=t,intent=v) for t,v in rows]
fx='月阵只在Kimi落脚后出现：K0实月与画外短咏→K1破窗下落→K1A脚底点亮单枚贴地弯月→K2明刃引光上行并闭合双人罩→K3暗刃实体触木才闪短弧→K4腕镣反噬局部亮→A1/A2/A4低亮维持→B3水撞处局部骤亮→F2撤罩时地阵同步熄灭。阵纹受地面透视、鞋底遮挡、石缝和局部反光约束；罩面不印星月图案，体积来自折射、边缘与受力变形。衣服、实体武器的原有星月装饰保持。'
prev=d['continuity']['kimi_dark_moon'];nxt=prev.replace('K2明刃先护两人','K1A落脚月阵→K2明刃先护两人')
d['continuity']['kimi_dark_moon']=nxt
d['continuity']['kimi_fx']=fx
d['continuity']['magic']=d['continuity']['magic'].replace('两侧与脚下散柴','罩外两侧散柴')
script=script.replace(prev,nxt)
for s in d['shots']:
 s['invariants']=[x.replace(prev,nxt) for x in s['invariants']]
 if s['id'] in changes or s['id'] in ['CY024K1A','CY024B','CY027D']:
  s['invariants'].append(fx)
script=script.replace('版本：v0.41｜2026-10-24｜小圆月双刃、后窗突入、先护后劈、双刃承压与钥匙解锁。新动作画面待作者审阅。','版本：v0.42｜2026-10-24｜落脚月阵、先护后劈、低亮维持与局部承压。新特效画面待作者审阅。\n\n## 月相特效连续性 · v0.42\n\n'+fx)

requests={}
for f in (R/REC).glob('*.json'):
 rows=load(f.relative_to(R));rows=rows if isinstance(rows,list) else [rows]
 for row in rows:
  if isinstance(row,dict) and 'prompt' in row:requests[(row['id'],row['rev'])]=(f.relative_to(R).as_posix(),row)
updates={'CY024K1A':1,'CY024K2':2,'CY024K3':2,'CY024K4':1,'CY024A1':1,'CY024A2':1,'CY024A4':2,'CY024B3':1}
generated=[]
for sid,rev in updates.items():
 s=by[sid];path=f'{IMG}/{sid}-v042-r{rev}.png';req,row=requests[(sid,rev)]
 prior=s['presentation']['path']
 s['presentation'].update(path=path,visible=s['action'],status='v0.42特效修订候选，待作者审阅',missing='静帧已查看；月阵展开、刀木接触、水流绕盾及跨镜动态未制作。')
 s['refs']=[dict(path=path,role='本轮特效候选'),dict(path=req,role='实际生成请求')]+([] if sid=='CY024K1A' else [dict(path=prior,role='历史画面保留')])
 s.update(generation_request=req,visual_prompt=row['prompt'],editorial_review=dict(version='v042',status='candidate_pending_author_review',dynamic_execution='pending'))
 with Image.open(R/path) as im:w,h=im.size
 s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0,y=0,w=1,h=1),panel_index=0)
 generated.append(dict(id=sid,path=path,sha256=sha(path),size=[w,h],request=req,inputs=[dict(path=q,sha256=sha(q)) for q in row['refs']]))
elapsed=0
for i,s in enumerate(d['shots']):
 s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
 if i+1<len(d['shots']):s['next_link']='接 '+d['shots'][i+1]['id']+'：'+d['shots'][i+1]['entry_state']
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']]
 sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)),path=ss[0]['presentation']['path'])
d.update(version='v0.42',revision='v042',picture_revision='v042',title='《穿云》带图分镜 v0.42 · 落脚月阵',total_seconds=elapsed,
 subtitle=f'{len(d["shots"])}镜 · {elapsed}秒 · 特效修订待审',story_script='剧本/穿云-场景剧本-v0.42.md',source_manifest='镜头设计/生成记录/生成索引-v042.json',origin_manifest='镜头设计/shot-plan-v0.41.json',audio_arrangement='后期/月相阵纹-v042/预演编排.json',
 review_intro='月光先藏在窗外，落脚才点亮弯月阵纹；先闭合双人护罩，再实体劈柴。护罩低亮维持，水撞处局部骤亮。',review_focus='核对落脚→阵纹→罩闭合→暗刃触木的先后，以及低亮守护与水浪承压的强弱差。Claude直立、腕踝锁扣与固定脚托保持。新图待审，音乐选择保留。',
 revision_notes=dict(previous_manifest='镜头设计/shot-plan-v0.41.json',added_ids=['CY024K1A'],modified_image_ids=list(updates),boundary='本轮特效画面为候选；原武器服装保留，既有对白与BGM不变。'))
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
assert all(s['source_quote'] in script for s in d['shots'])
save(PLAN,d);write(d['story_script'],script)
save(d['source_manifest'],dict(version='v042',previous_index=old['source_manifest'],generated_images=len(generated),images=generated,not_used=['K2r1提前清柴，r2恢复高柴','K3r1漏踝扣，r2补回','A4r1误生局部小护罩，r2改共用罩的局部地面边界']))
a=load(old['audio_arrangement']);a.update(version='v042-picture-sync',previous=old['audio_arrangement'],shot_plan=PLAN,shot_plan_sha256=sha(PLAN))
a['shot_overrides']['CY024K1A']=copy.deepcopy(a['shot_overrides']['CY024K2'])
a['shot_overrides']['CY024K1A'].update(note='落脚与月阵启动插镜，沿用相邻镜候选，未替作者选定。',audition_question='试听落脚重音与月阵启动的短暂停顿。')
for sid in list(changes)+['CY024K1A']:a['effects'][sid]=by[sid]['sound']
a['author_feedback']='原有125镜音乐候选及浏览器选曲标记保留；新增1.5秒落脚镜沿用邻镜候选，未自动标记。新增特效声音为设计说明，未制作音轨。'
save(d['audio_arrangement'],a)
snapshot=R/'镜头设计/带图分镜-月刃救援-v041.html'
if not snapshot.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
t=read('scripts/build_storyboard.py').replace('shot-plan-v0.41.json','shot-plan-v0.42.json')
t=t.replace('"v041")','"v041", "v042")').replace("'v041')","'v041','v042')")
t=t.replace('data.get("revision")=="v041"','data.get("revision") in ("v041","v042")')
t=t.replace('["CY024K0","CY024K1","CY024K2","CY024K3","CY024K4"]','["CY024K0","CY024K1",*(["CY024K1A"] if data.get("revision")=="v042" else []),"CY024K2","CY024K3","CY024K4"]')
t=t.replace("data.get('revision') == 'v041'","data.get('revision') in ('v041','v042')")
write('scripts/build_storyboard.py',t)
write('00_打开项目.html',read('00_打开项目.html').replace('v0.41','v0.42'))
progress='''## 2026-10-24：落脚月阵与特效强弱（v0.42，新图待审）

作者指出Kimi的星月护罩像贴图、张力不足，建议月形阵纹。本轮改成破窗只见实月逆光，落脚插镜点亮贴地弯月，明刃引光闭合双人罩后暗刃才触木；平时低亮透明，水浪只让受压区域骤亮。撤盾时地阵同步熄灭。衣服与实体武器上的原有星月纹饰保留，Claude直立受缚与固定脚托保持。

七张旧特效图修订，并新增1.5秒落脚特写CY024K1A，共126镜418.5秒。剧本、分镜、预演与声音设计同步；原有125镜候选BGM和本机选择保留，新增镜沿用相邻候选而不自动选定。新图待作者审阅，动态与正式特效音尚未制作。实际请求、输入哈希与拒绝中间稿保留在月相阵纹-v042记录中。

'''
p=read('制作进度.md');pos=p.index('## 2026-10-24：');write('制作进度.md',p[:pos]+progress+p[pos:])
print(json.dumps(dict(shots=len(d['shots']),seconds=elapsed,images=len(generated)),ensure_ascii=False))
