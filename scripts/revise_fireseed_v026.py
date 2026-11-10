"""Revise fire action into release, slow flight, and autonomous ignition."""
import copy,hashlib,json,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];REC='镜头设计/生成记录/火种慢镜-v026';IMG='镜头设计/图像/火种慢镜-v026'
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,s):(R/p).write_text(s,encoding='utf-8')
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
old=json.loads(read('镜头设计/shot-plan-v0.25.json'));d=copy.deepcopy(old);lookup={s['id']:s for s in d['shots']}
release='Claude移开看向父亲的目光，望向空十字架。切指尖特写：她抬手凝起一小团橙金火种，指尖轻轻一送，火种离手；火种与手指之间留出清楚的空气间隙。手指随即放松，不再持续输出火焰。此刻头纱与衣料已经干燥，空刑架尚未起火。'
flight='切火种飞行特写。镜头沿同一侧贴着火种短距离跟随，火种从画面右侧飞向左侧空刑架，尾后仅有短促余烬，没有连接手指的火流。飞行短暂放慢，远处Claude虚化，近处木纹与空镣铐逐渐清楚。火种触木的瞬间恢复正常速度，木纹上先亮起一个小点。'
burn='切回低位大火镜：着火点沿木纹骤然窜开，厚实火焰沿立柱与横木翻卷上冲，空十字架和锁链仍从火隙中显露。Claude已经放下施法的手，刑架自行燃烧；她与刑架之间没有火流。ChatGPT守在她身侧。火势止于空刑架，没有扑向人物或点燃建筑，普通灯具仍熄灭。短促腾燃声打破飞行时的安静，随后转为持续燃烧声。'
collapse='火焰已经攀上空木架。Claude的施法手已经放下，力量耗尽，膝盖一软，身体向右侧倾去。她仍有意识，没有摔到地上。'
script=read(old['story_script']);lines=script.splitlines();lines[2]='版本：v0.26｜2026-10-22｜焚架改为指尖释放火种、飞行慢镜、触木后骤燃；大火镜已收手，无持续火流。对白保持，三张本轮画面候选待审。';script='\n'.join(lines)+'\n'
assert lookup['CY029B']['source_quote'] in script
script=script.replace(lookup['CY029B']['source_quote'],release+'\n\n'+flight+'\n\n'+burn,1).replace(lookup['CY029C']['source_quote'],collapse,1)
write('剧本/穿云-场景剧本-v0.26.md',script)
d.update(version='v0.26',revision='v026',title='《穿云》带图分镜 v0.26 · 火种慢镜与骤燃',subtitle='离手火种→短暂慢速飞行→触木骤燃；无持续喷火',story_script='剧本/穿云-场景剧本-v0.26.md',origin_manifest='镜头设计/shot-plan-v0.25.json',source_manifest='镜头设计/生成记录/生成索引-v026.json')
d['review_intro']='作者确认火种镜头方案：新增CY029B1释放特写和CY029B2飞行慢镜，原CY029B改成收手后的自主燃烧。三张新图待审，慢动作、跟焦、触木骤燃及声音均为分镜执行说明，未制作动态视频。'
d['review_focus']='教主呼唤→Claude放出火种→火种短暂慢速飞行→触木恢复正常速度→空架骤燃且Claude已收手→脱力接抱。'
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.25.json',previous_html='镜头设计/带图分镜-v0.25.html',added_ids=['CY029B1','CY029B2'],modified_ids=['CY029B','CY029C'],boundary='新增两镜各2秒；原94镜时长、对白和其余93张图保持，只替换CY029B。当前96镜308秒。')
base=copy.deepcopy(lookup['CY029B'])
def frame(s,id,title,quote,framing,purpose,entry,exit,next_link,seconds):
 s.update(id=id,title=title,source_quote=quote,action=quote,framing=framing,purpose=purpose,entry_state=entry,exit_state=exit,next_link=next_link,seconds=seconds,dialogue='无对白',dialogue_cues=[])
 s.pop('subtitle_cues',None);s.pop('cinematic_beats',None)
 s['invariants']=['面向画面，Claude在右、空架在左；火种只从右向左，避免镜间反向。','只有一枚脱离手指的小火种；不画光束、长尾火流或持续喷火。','人物头纱/衣料已经蒸干；火种触木前刑架不燃，普通灯具保持熄灭。','刑架无人，镣铐为空；火种飞向木料，不冲向Claude、GPT或其他角色。']
 s['presentation']=dict(path=IMG+'/'+id+'-v026-r1.png',role='action',visible=quote,status='v0.26修订候选，待作者审阅',missing='静帧只表达代表状态；离手、运动方向、慢速跟拍/跟焦、触木与骤燃仍待动态验证。',show_as_main=True)
 s['generation_request']=REC+'/'+id+'-请求-v001.json';s['visual_prompt']=json.loads(read(s['generation_request']))['prompt'];s['refs']=[dict(path=s['presentation']['path'],role='本轮候选'),dict(path=s['generation_request'],role='实际冻结输入')]
 s['editorial_review']=dict(version='v026',status='candidate_pending_author_review',dynamic_execution='pending')
 with Image.open(R/s['presentation']['path']) as im:w,h=im.size
 s['page_size']=[w,h];s['panel_rect_pixels']=[0,0,w,h];s['panel_region']=dict(x=0.0,y=0.0,w=1.0,h=1.0);s['panel_index']=0
 return s
one=frame(copy.deepcopy(base),'CY029B1','放出一枚火种',release,'手部侧面特写／正常速度','把告别落实为轻轻一送的决定，明确火种离手。','父亲呼唤已落下，Claude回望空架。','火种脱离手指向左，手不再输出。','接CY029B2：同向切火种飞行，空架在左。',2)
one['sound']='父亲呼唤尾音散去，衣袖轻动，保留微弱火焰声。无新对白；声音未制作。'
one['cinematic_beats']=[dict(offset=0,intent='接移开父亲目光与抬手，进入指尖特写'),dict(offset=0.7,intent='轻送一枚火种，明确离手间隙'),dict(offset=1.5,intent='手指松开，不维持喷火')]
two=frame(copy.deepcopy(base),'CY029B2','火种飞向空架',flight,'火种近景／同侧短距离跟拍／短暂慢动作与焦点转移','以短暂安静的飞行衬托触木骤燃，明确火种落点。','单枚火种已经脱手，木架未燃。','火种触木，恢复正常速度，局部亮起一点。','接CY029B：同一着火点骤然沿木纹扩散，切大火。',2)
two['sound']='短暂压低环境声，留下轻微火焰掠过声；触木恢复正常速度，腾燃声由下一镜接入。无持续喷火声，声音未制作。'
two['cinematic_beats']=[dict(offset=0,intent='右向左跟随单枚火种，短暂放慢'),dict(offset=1.2,intent='焦点由火种过渡至近处木纹，人物留虚化背景'),dict(offset=1.8,intent='触木时恢复正常速度，局部亮点接下一镜')]
idx=d['shots'].index(lookup['CY029B']);d['shots'][idx:idx]=[one,two]
oldpath=lookup['CY029B']['presentation']['path']
fire=frame(lookup['CY029B'],'CY029B','触木后骤然燃起',burn,'低位中远景／正常速度／空架腾燃高峰','用大火骤起回应小火种的安静，避免重复施法。','火种已触木，Claude完成释放。','Claude手已放下，刑架持续燃烧；下一镜直接脱力。','接CY029C：不再重复收手，直接膝软向GPT一侧倾去。',3)
fire['sound']='短促腾燃声骤起，随后木料燃烧与锁链声；无新对白，实际音效未制作。'
fire['cinematic_beats']=[dict(offset=0,intent='切正常速度，着火点沿木纹迅速窜开'),dict(offset=0.5,intent='空架火势上冲，Claude手已离开施法姿态'),dict(offset=2.3,intent='转持续燃烧，接膝软脱力')]
fire['refs'].append(dict(path=oldpath,role='保留的持续火流旧版，不用于本次动作'))
lookup['CY029C'].update(source_quote=collapse,action=collapse,entry_state='空刑架自主燃烧，Claude已收手。');lookup['CY029C']['presentation']['visible']=collapse
lookup['CY029E']['exit_state']='呼唤尾音散去，Claude转向空刑架，接指尖释放火种。';lookup['CY029E']['next_link']='接CY029B1：Claude不答父亲，移开目光，抬手轻送火种。'
d['continuity']['cross_fire']='CY029B1单枚火种离手→CY029B2右向左慢速飞行、触木恢复正常速→CY029B空架自主骤燃且Claude已收手→CY029C直接脱力。不再使用连接手指的持续火流。火止于空架，普通灯具不复燃。'
elapsed=0
for s in d['shots']:s['start_second']=elapsed;elapsed+=s['seconds'];s['end_second']=elapsed
d['total_seconds']=elapsed
for sc in d['scenes']:
 ss=[s for s in d['shots'] if s['scene']==sc['id']];sc.update(shot_ids=[s['id'] for s in ss],seconds=sum(s['seconds'] for s in ss),pages=list(dict.fromkeys(s['presentation']['path'] for s in ss)));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=s['presentation']['path'],rows=1,cols=1) for s in d['shots']]
save('镜头设计/shot-plan-v0.26.json',d)
snap=R/'镜头设计/带图分镜-v0.25.html'
if not snap.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snap)
p='scripts/build_storyboard.py';write(p,read(p).replace('shot-plan-v0.25.json','shot-plan-v0.26.json').replace('"v025")','"v025", "v026")').replace("'v025')","'v025','v026')"))
entry=read('00_打开项目.html').replace('v0.25','v0.26').replace('94 镜 · 5 分 04 秒','96 镜 · 5 分 08 秒').replace('战后对白与小鱼补镜；刑架火势增强','火种慢镜与触木骤燃；对白保持')
entry=entry.replace('镜头设计/图像/战后对白与补镜-v025/CY029B-v025-r1.png',IMG+'/CY029B-v026-r1.png')
entry=entry.replace('<a href="镜头设计/图像/',f'<a href="{IMG}/CY029B1-v026-r1.png">新增：指尖释放火种<small>明确离手，不再持续喷火</small></a>\n<a href="{IMG}/CY029B2-v026-r1.png">新增：火种飞行特写<small>短暂慢动作与触木恢复正常速度 · 静帧候选</small></a>\n<a href="镜头设计/图像/',1)
write('00_打开项目.html',entry)
p='制作进度.md';t=read(p);i=t.index('## ');note='''## 2026-10-22：火种离手、慢速飞行与触木骤燃（v0.26）

作者确认将CY029B的持续火流改为：指尖轻送一枚火种→飞行特写短暂慢速→触木恢复正常速度→刑架骤燃。新增CY029B1、CY029B2各2秒，CY029B去掉连接手指的火流并将Claude施法手放下；CY029C改为直接脱力，不重复收手。对白及原94镜时长保持，当前96镜308秒（5分08秒）。

[当前分镜](镜头设计/带图分镜.html)与[剧本v0.26](剧本/穿云-场景剧本-v0.26.md)同步。三张本轮图像为待审候选，原94镜仅替换CY029B，旧画面、原封版和历史图册保留。实际飞行、跟焦、变速、触木骤燃与声音尚未制作；这里只完成静帧及执行说明，未生成视频。见[复核记录](镜头设计/生成记录/火种慢镜-v026/复核记录.md)。

''';write(p,t[:i]+note+t[i:]);print('v0.26 prepared',len(d['shots']),elapsed)
