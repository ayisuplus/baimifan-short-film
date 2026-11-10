"""Preserve old shot IDs while integrating reaction, complete Kimi chant and local color fixes."""
import copy,hashlib,json,re,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/目光与入场-v048'
IMG='镜头设计/图像/目光与入场-v048'
PLAN='镜头设计/shot-plan-v0.48.json'
def read(p):return (R/p).read_text('utf-8-sig')
def load(p):return json.loads(read(p))
def write(p,t):
 (R/p).parent.mkdir(parents=True,exist_ok=True);(R/p).write_text(t,'utf-8')
def save(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
assert not (R/PLAN).exists()
old=load('镜头设计/shot-plan-v0.47.json');d=copy.deepcopy(old);script=read(old['story_script']);by={s['id']:s for s in d['shots']}
def update(sid,**fields):
 global script
 s=by[sid];before=s['source_quote'];s.update(fields)
 s['source_quote']=s['action']+('' if s['dialogue']=='无对白' else '\n\n**Kimi（画外）：**\n'+s['dialogue'].split('：',1)[1])
 assert before in script,sid
 script=script.replace(before,s['source_quote'])
 s['presentation']['visible']=s['action'];s.pop('final_static_review',None)
update('CY022A1',action='背后低机位沿长阶中轴望向Claude。教主右手握着同一支火把，头、肩、骨盆及双脚都朝向最高祭坛，背对镜头一步一步上阶；不回头，不侧身偏向画面右侧。前脚踩上高一级石阶，后脚跟进，披风顺背向下拖曳。高处Claude直立受缚，腰腹以下仍陷在黑木堆里，小鱼留在下端。',framing='背后低机位，教主后脑、背部与Claude共用登阶方向',exit_state='教主正对Claude登到柴堆前，右手火把准备下压点火。',cinematic_beats=[dict(offset=0,intent='正背面沿中央阶梯登向Claude'),dict(offset=2,intent='迈上一级，保持身体朝向')])
n=copy.deepcopy(by['CY024K0'])
n.update(id='CY024R',title='教主回身，注意力转向正门',seconds=3.5,framing='教主胸上三分之二侧面，附近教徒在后景',purpose='接住援军入场的敌方反应，为后窗突入制造注意力空隙，并先闻Kimi咏唱。',
 action='接GPT说完“护住她们”。教主在长阶下段缓台停住，头肩转向正门，平视画外入场者，眉眼绷紧；附近黑袍教徒也被门口动静吸引。注意力留在正门，没有提前仰看后窗或云层。画外渐入Kimi的呼唤，先让观众听见声音，再切中央高窗揭示她的位置；教主不因此抢先发现后窗的人。',
 dialogue='Kimi（画外）：隐于月背的暗影啊，',
 sound='承前脚步和门口甲片尾响，教徒转身衣料声；0.6秒起Kimi画外呼唤，观众听点先行，随后切窗外。正式配音未制作。',
 entry_state='GPT带同伴进入正门，命令护住她们。',exit_state='教主与邻近教徒仍盯正门，Kimi呼唤收尾，切后窗暗影。',
 asset_ids=['CHAR-PRIEST','CHAR-CULTIST','ENV-CHURCH','MULKZI2WMFNJE'],dialogue_cues=[],
 subtitle_cues=[dict(speaker='Kimi（画外）',text='隐于月背的暗影啊，',offset=.6,duration=2.8)],
 cinematic_beats=[dict(offset=0,intent='教主转向入口，附近教徒跟随'),dict(offset=.6,intent='先闻画外呼唤，画面仍留在敌方反应')])
n['source_quote']=n['action']+'\n\n**Kimi（画外）：**\n隐于月背的暗影啊，'
n['invariants']=[d['continuity']['church'],'此时尚未破窗、闭罩、落水；教主目光朝正门，不提前发现Kimi。']
n.pop('final_static_review',None);by[n['id']]=n
i=d['shots'].index(by['CY024']);d['shots'].insert(i+1,n)
script=script.replace(by['CY024']['source_quote'],by['CY024']['source_quote']+'\n\n'+n['source_quote'])
update('CY024K0',title='窗外举刃，暗影开门',seconds=6,
 action='十字架正后中央高窗仍然完整。承接画外呼唤，月光中浮现Kimi模糊的头肩与长发剪影，隔着蓝色彩玻璃看不清面容。她说出法术请求，左手将小尺寸明刃举到肩旁；刃缘透过完整玻璃只显出一线微亮，握持关系可辨，右暗刃低垂在画外。镜末请求句收住，短停半拍后左臂甩刃；左右窗没有破损，也没有护罩、阵纹或额外月环。',
 dialogue='Kimi（画外）：请循此刃的银辉，为我开启通往彼端的门扉——',
 sound='承前呼唤，0.1—5.5秒说出请求，末尾留约半秒；殿内火声压低，下一镜玻璃爆裂独占声音重音。正式配音未制作。',
 entry_state='敌方视线被正门牵住，呼唤已传入；中央彩窗完整。',
 exit_state='请求句收尾，左臂甩出明刃，接力量破窗。',
 subtitle_cues=[dict(speaker='Kimi（画外）',text='请循此刃的银辉，',offset=.1,duration=2),dict(speaker='Kimi（画外）',text='为我开启通往彼端的门扉——',offset=2.2,duration=3.3)],
 cinematic_beats=[dict(offset=0,intent='剪影接请求前半句'),dict(offset=2.2,intent='左手举明刃，建立法术方向'),dict(offset=5.5,intent='请求句后短停，蓄甩刃动作')])
update('CY024K1A',seconds=2,
 action='明刃下尖钉入柴堆前侧外缘的一根乌烬木，木纤维裂开。接触点的银光短促亮起，刀已稳稳留在木上，Kimi才从画外报出术名“月影渡”。镜末银光收拢，接她沿坐标瞬移现身；刀不插地、不展开护罩，高柴仍燃烧。画面此刻还没有Kimi实体。',
 dialogue='Kimi（画外）：月影渡！',
 sound='0—0.5秒刀尖入木与纤维裂响，玻璃尾声降下；0.6—1.8秒术名清晰落定，最后一个字接短促瞬移低鸣，下一镜爆气震柴。',
 entry_state='明刃已穿过中央彩窗，飞向柴堆外缘。',exit_state='明刃成为固定坐标，术名落定，接Kimi循刃瞬移。',
 subtitle_cues=[dict(speaker='Kimi（画外）',text='月影渡！',offset=.6,duration=1.2)],
 cinematic_beats=[dict(offset=0,intent='刀尖入木，坐标亮起'),dict(offset=.6,intent='报术名，末字接瞬移')])
s=by['CY024K1'];s['sound']='咏唱在此暂停；一记硬脆撞击→密集玻璃爆裂→刀锋掠过镜头→碎片坠地尾响，避免盖住下一镜术名。';s['entry_state']='Kimi说完请求后甩出左手明刃，彩窗仍完整到刀锋接触。'
s=by['CY024K2'];s['entry_state']='月影渡术名落定，明刃已钉稳柴木成为坐标。';s['sound']='承术名尾音的瞬移低鸣→低频爆气→重木刮石翻落；不重复念咒，不延长成漂浮碎片。'
ct=d['continuity'];old_kimi=ct['kimi_fx'];new_kimi=old_kimi.replace('月下剪影→明刃破中央彩窗','教主转向正门时先闻呼唤→月下剪影举明刃并说出请求→留白，明刃破中央彩窗').replace('钉外缘柴木→循刃瞬移','钉外缘柴木后报“月影渡”→循刃瞬移')
old_branch=next((v for k,v in ct.items() if 'Kimi与GPT稍早约定分路' in v),None)
repls={old_kimi:new_kimi}
if old_branch:repls[old_branch]=old_branch.replace('月光中显现剪影，画外短咏','月光中显现剪影；呼唤、法术请求、术名构成完整咏唱').replace('K1明刃力量破窗特写→K1A钉入柴堆外缘→K2','K1明刃力量破窗特写（咏唱暂停）→K1A钉入柴堆外缘，报“月影渡”→K2')
def rewrite(v):
 if isinstance(v,str):
  for a,b in repls.items():v=v.replace(a,b)
  return v
 if isinstance(v,list):return [rewrite(x) for x in v]
 if isinstance(v,dict):return {k:rewrite(x) for k,x in v.items()}
 return v
d=rewrite(d);script=rewrite(script);by={s['id']:s for s in d['shots']}
d['continuity']['kimi_chant']='作者确认完整咏唱：“隐于月背的暗影啊，请循此刃的银辉，为我开启通往彼端的门扉——月影渡！”CY024R先闻呼唤，K0窗外举刃说请求，K1破窗暂停说话，K1A钉稳后报术名，K2瞬移回应。时长为字幕预演预算，正式配音与口型尚未制作。暗刃护罩为随后的独立动作，不把瞬移术名误指成护罩名称。'
d['continuity']['face_color']='眼白保持自然，去除无光源依据的整片红眼睑和腮红；保留泪水、污痕、疲惫及有依据的火侧轮廓光。GPT淡紫、Kimi紫、Claude橙金、DeepSeek蓝；各援军沿用母本，Gemini天生一粉紫一金的异色瞳保留，不能把本来眼色当成红眼异常。'
selected={};images=[]
for req in sorted((R/REC).glob('0[1-6]-*.json')):
 for row in json.loads(req.read_text('utf-8-sig')):selected[row['id']]=(row,str(req.relative_to(R)).replace('\\','/'))
for sid,(row,req) in selected.items():
 s=by[sid];prior=s['presentation']['path'];path=f'{IMG}/{sid}-v048-r{row["rev"]}.png'
 s['presentation'].update(path=path,visible=s['action'],status='v0.48朝向、反应、咏唱及局部色偏修订候选，待作者画面审阅',missing='静帧已查看；动态朝向、咏唱时长与逐拍执行待视频和正式声音验证。')
 s['refs']=[dict(path=path,role='本轮修订候选'),dict(path=req,role='冻结实际生成请求')]+([] if sid=='CY024R' else [dict(path=prior,role='历史画面保留')])
 s.update(visual_prompt=row['prompt'],generation_request=req,editorial_review=dict(version='v048',status='candidate_pending_author_review',dynamic_execution='pending'))
 s.pop('final_static_review',None)
 with Image.open(R/path) as im:w,h=im.size
 s.update(page_size=[w,h],panel_rect_pixels=[0,0,w,h],panel_region=dict(x=0,y=0,w=1,h=1),panel_index=0)
 images.append(dict(id=sid,path=path,sha256=sha(path),size=[w,h],request=req,request_sha256=sha(req),inputs=[dict(path=p,sha256=sha(p)) for p in row['refs']]))
elapsed=0
for i,s in enumerate(d['shots']):
 s.update(start_second=elapsed,end_second=elapsed+s['seconds']);elapsed+=s['seconds']
 if i+1<len(d['shots']):s['next_link']='接 '+d['shots'][i+1]['id']+'：'+d['shots'][i+1]['entry_state']
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']]
 sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)),path=ss[0]['presentation']['path'])
d.update(version='v0.48',revision='v048',picture_revision='v048',title='《穿云》带图分镜 v0.48 · 敌方反应与月影渡',subtitle=f'{len(d["shots"])}镜 · {elapsed}秒 · 新图待作者审阅',total_seconds=elapsed,story_script='剧本/穿云-场景剧本-v0.48.md',source_manifest='镜头设计/生成记录/生成索引-v048.json',origin_manifest='镜头设计/shot-plan-v0.47.json',audio_arrangement='后期/目光与入场-v048/预演编排.json',review_intro='教主正向Claude登阶；援军入场后先接敌方反应，再以完整月影渡咏唱引出后窗救援。后段眼色与肤色局部修正。',review_focus='检查登阶方向、正门吸引敌方注意与后窗声画衔接，以及呼唤—请求—术名的完整咏唱。修正色偏时保留角色眼色、情绪与伤后状态。',revision_notes=dict(previous_manifest='镜头设计/shot-plan-v0.47.json',added_ids=['CY024R'],modified_image_ids=list(selected),boundary='新反应3.5秒、K0延长2秒、K1A延长0.5秒；Kimi咏唱按作者确认替换，其余旧镜时长和对白保留；BGM标记不改。'))
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
script=re.sub(r'版本：v0\.47[^\n]*','版本：v0.48｜2026-10-24｜敌方反应、完整月影渡咏唱及局部眼肤色修正。',script,1)
script=script.replace('## 三点定流与控水协作 · v0.47','## 敌方反应与完整月影渡 · v0.48')
script+='\n\n## 月影渡与脸部色彩连续性 · v0.48\n\n'+d['continuity']['kimi_chant']+'\n\n'+d['continuity']['face_color']+'\n'
assert len(d['shots'])==131 and elapsed==431.5
assert all(s['source_quote'] in script for s in d['shots'])
save(PLAN,d);write(d['story_script'],script)
save(d['source_manifest'],dict(version='v048',previous_index=old['source_manifest'],engine='built-in image_gen',mode='reference edit',transparent_background=False,images=images))
a=load(old['audio_arrangement']);a.update(version='v048-picture-sync',previous=old['audio_arrangement'],shot_plan=PLAN,shot_plan_sha256=sha(PLAN))
a['shot_overrides']['CY024R']=copy.deepcopy(a['shot_overrides']['CY024K0'])
for sid in ['CY024R','CY024K0','CY024K1','CY024K1A','CY024K2']:a['effects'][sid]=by[sid]['sound']
for sid in ['CY024R','CY024K0','CY024K1A']:
 a['shot_overrides'][sid]['note']='音乐候选保持；'+by[sid]['title']
 a['shot_overrides'][sid]['audition_question']='比较音乐是否让开Kimi的呼唤、请求与术名；破窗留出独立重音。'
a['author_feedback']='作者确认完整月影渡咏唱；保留原130镜音乐候选及浏览器本机选曲标记。新增反应沿用相邻K0候选，不代选。字幕仅为预算，正式配音未制作。'
save(d['audio_arrangement'],a)
snapshot=R/'镜头设计/带图分镜-三点定流-v047.html';assert not snapshot.exists();shutil.copy2(R/'镜头设计/带图分镜.html',snapshot)
t=read('scripts/build_storyboard.py').replace('shot-plan-v0.47.json','shot-plan-v0.48.json').replace('"v047")','"v047", "v048")').replace("'v047')","'v047','v048')")
t=t.replace('"CY024",*(','"CY024",*(["CY024R"] if data.get("revision")=="v048" else []),*(')
write('scripts/build_storyboard.py',t)
e=read('00_打开项目.html').replace('v0.47','v0.48').replace('130镜425.5秒；4张三点定流修订候选待审',f'131镜431.5秒；{len(images)}张本轮修订图待审').replace('130 镜 · 7 分 05.5 秒','131 镜 · 7 分 11.5 秒')
e=e.replace('<strong>三次瞄准与三柱清场','<strong>敌方反应与完整月影渡咏唱')
e=e.replace('<a href="镜头设计/带图分镜.html#CY024A5">本轮：','<a href="镜头设计/带图分镜.html#CY024R">本轮：教主反应与月影渡<small>先闻呼唤 → 窗外举刃与请求 → 破窗留白 → 钉柴报术名 → 瞬移</small></a>\n<a href="镜头设计/带图分镜.html#CY024A5">')
write('00_打开项目.html',e)
p=read('制作进度.md');pos=p.index('## 2026-10-24：')
entry=f'''## 2026-10-24：朝向、敌方反应与完整月影渡（v0.48，新图待审）

CY022A1改为教主头肩、身体和脚步正向Claude上阶。CY024后新增CY024R 3.5秒：教主及邻近教徒回身盯向正门，给Kimi后窗突入建立注意力空隙。作者确认“隐于月背的暗影啊，请循此刃的银辉，为我开启通往彼端的门扉——月影渡！”R先闻呼唤、K0窗外举刃说请求（6秒）、K1破窗留白、K1A钉柴报术名（2秒）、K2瞬移。原句保存在v047历史稿。

针对后段异常眼区红染、大片腮红和GPT眼色串为金色逐镜局部修正；保留原定虹膜色、Gemini异色瞳、泪水、污痕、表情和动作。当前131镜431.5秒，{len(images)}张本轮修订图，旧130镜音乐候选与本机标记保留。主剧本、字幕、声音说明和预演台同源更新，v047旧页及图片保留。静帧待作者审阅，完整咏唱尚未制作正式配音，时长为预演预算。

'''
write('制作进度.md',p[:pos]+entry+p[pos:])
print(json.dumps(dict(shots=len(d['shots']),seconds=elapsed,images=len(images)),ensure_ascii=False))
