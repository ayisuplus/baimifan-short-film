"""Versioned edit: fire-seed first-person approach, preserving previous editions."""
import copy,hashlib,json,shutil,re
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
REC='镜头设计/生成记录/火种主观-v027'
IMG='镜头设计/图像/火种主观-v027/CY029B2-v027-r1.png'
REQ=REC+'/CY029B2-请求-v001.json'
SRC=Path(r'C:\Users\36322\.codex\generated_images\01a162c1-6e38-7a10-aee7-5c8371c4830c\exec-76c8046a-bd1c-49ee-86e6-00200b1c4f64.png')
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,s):(R/p).write_text(s,encoding='utf-8')
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
(R/IMG).parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(SRC,R/IMG)
old=json.loads(read('镜头设计/shot-plan-v0.26.json'));d=copy.deepcopy(old)
shots={s['id']:s for s in d['shots']};s=shots['CY029B2'];previous=s['presentation']['path']
flight='切入火种的主观视角。空十字架位于正前方，镜头沿火种飞行方向缓缓逼近立柱与横木交接处铁箍下方的裸露木纹；木纹与空镣铐逐渐放大。画面中央不出现火种本体，仅边缘掠过少量虚焦橙金火舌与轻微热扰动，中心落点始终清楚。镜头平稳前行，仅有轻微漂移，不翻滚、不绕行。最后一小段提速，触及木料时局部闪亮，随即切回外部视角，接空刑架骤燃。'
script=read(old['story_script']).replace(s['source_quote'],flight,1)
lines=script.splitlines();lines[2]='版本：v0.27｜2026-10-22｜CY029B2改为火种主观逼近、末段提速触木；释放与大火镜、对白和时长保持。新静帧候选待审。'
write('剧本/穿云-场景剧本-v0.27.md','\n'.join(lines)+'\n')
d.update(version='v0.27',revision='v027',title='《穿云》带图分镜 v0.27 · 火种主观飞行',subtitle='指尖释放→火种主观逼近→触木骤燃；对白与时长保持',story_script='剧本/穿云-场景剧本-v0.27.md',origin_manifest='镜头设计/shot-plan-v0.26.json',source_manifest='镜头设计/生成记录/生成索引-v027.json')
d['review_intro']='作者确认CY029B2改为火种第一视角：正前方空架缓缓逼近，边缘少量虚焦火舌，末段提速触木后切外部大火。新图是临近触木的代表帧，待作者审阅；动态运镜、变速、接点与声音尚未制作。'
d['review_focus']='指尖火种离手→顺飞行方向切主观，空架正前方→逼近裸露木纹→末段提速触木→切回外部空架骤燃且Claude已收手。'
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.26.json',previous_html='镜头设计/带图分镜-v0.26.html',added_ids=[],modified_ids=['CY029B1','CY029B2'],boundary='只替换CY029B2静帧与主观飞行设计，CY029B1更新转场说明；96镜308秒，全部对白和时长、其余95张画面保持。')
s.update(title='火种主观逼近空架',source_quote=flight,action=flight,framing='火种第一视角／平稳前移／短暂慢速，末段提速',purpose='让观众随火种接近曾束缚Claude的空架，以安静逼近蓄势，触木后释放火势。',entry_state='单枚火种已离手；切入顺其运动方向的主观视角，空架在正前方、尚未燃烧。',exit_state='末段提速触及铁箍下方裸露木纹，局部闪亮，切外部大火。',next_link='接CY029B：从主观触木切回原外部轴线，空架在左骤燃，Claude在右且手已放下。',asset_ids=['ENV-CHURCH'])
s['invariants']=['主观镜头沿既有火种飞向空架的空间方向进入，目标在正前方；外部镜仍保持Claude右、空架左。不可把主观居中误作空间换位。','镜头即火种视点，中心不出现火种本体、手、人物、HUD或长尾火流；只在边缘保留少量虚焦火舌与轻微热扰动。','空架无人，镣铐为空；目标是交接处铁箍下方裸露木料，触木前不燃，不撞向人物或金属扣。','慢速平稳逼近、仅轻微漂移；不翻滚、不绕行。末段提速触木后立即切外部骤燃。','天瀑后普通灯具保持熄灭；暖色来自火种近场光与水面反射，不能让烛台或火盆复燃。']
s['sound']='环境声短暂压低，留轻微贴近视点的火焰掠过声；末段提速、触木后由下一镜腾燃声骤起。无新对白，实际声音未制作。'
s['cinematic_beats']=[dict(offset=0,intent='由离手外部特写切入沿飞行方向的主观视角，空架正前方，中心清楚'),dict(offset=0.2,intent='平稳慢速逼近，木纹与空镣铐逐渐放大，边缘少量虚焦火舌'),dict(offset=1.6,intent='最后一小段提速，瞄准交接铁箍下方裸露木纹'),dict(offset=1.9,intent='触木局部闪亮，立即切CY029B外部大火')]
s['presentation'].update(path=IMG,visible='临近触木的火种主观代表帧：正前方空木架及空镣铐清楚，中央无火球，边缘有虚焦火光；尚未点燃。',status='v0.27修订候选，待作者审阅',missing='此静帧表示逼近末段；慢速飞行、末段加速、触木闪亮及切回大火须动态验证。')
s['generation_request']=REQ;s['visual_prompt']=json.loads(read(REQ))['prompt']
s['refs']=[dict(path=IMG,role='本轮主观镜候选'),dict(path=REQ,role='实际冻结输入'),dict(path=previous,role='保留的侧面跟拍旧版')]
s['editorial_review']=dict(version='v027',status='candidate_pending_author_review',dynamic_execution='pending')
with Image.open(R/IMG) as im:w,h=im.size
s['page_size']=[w,h];s['panel_rect_pixels']=[0,0,w,h]
shots['CY029B1']['next_link']='接CY029B2：火种离手后顺其运动方向切主观视角，空架位于正前方，保持同一落点。'
d['continuity']['cross_fire']='CY029B1外部特写火种离手→CY029B2沿火种方向切主观，空架正前方，缓缓逼近裸露木纹、末段提速触木→CY029B切回原外部轴线，空架自主骤燃且Claude已收手→CY029C直接脱力。主观中央不画火种，边缘火舌不能遮挡落点。火止于空架，普通灯具不复燃。'
for sc in d['scenes']:
 ss=[x for x in d['shots'] if x['scene']==sc['id']];sc['pages']=list(dict.fromkeys(x['presentation']['path'] for x in ss));sc['path']=sc['pages'][0]
d['page_layouts']=[dict(path=x['presentation']['path'],rows=1,cols=1) for x in d['shots']]
save('镜头设计/shot-plan-v0.27.json',d)
request=json.loads(read(REQ))
record=dict(shot_id='CY029B2',attempt=1,original=str(SRC),destination=IMG,sha256=sha(R/IMG),request=REQ,request_sha256=sha(R/REQ),inputs=[dict(path=p,sha256=sha(p)) for p in request['referenced_image_paths']],status='candidate_pending_author_review')
save('镜头设计/生成记录/生成索引-v027.json',dict(version='v027',previous_index='镜头设计/生成记录/生成索引-v026.json',records=[record],review=REC+'/复核记录.md'))
write(REC+'/复核记录.md','''# CY029B2 火种主观镜头 v0.27

作者确认设计修改。新增一张静帧候选，旧侧跟画面保留，不代表作者已审定新图。

已查看实际生成图：正前方空十字架、空镣铐可读；中央没有火球、人物或HUD；边缘有虚焦暖色火光，主体尚未燃烧。图为逼近末段代表状态，起幅应稍远，触点明确在交接铁箍下方的裸露木纹；画面中的暖色水面亮斑按火种反光处理，不代表普通灯具复燃。两侧边缘火光在动态制作中不可继续增厚遮挡落点。

执行：0–1.6秒平稳缓缓前移，1.6秒后短程提速，约1.9秒触木局部闪亮，切回CY029B外部大火。主观方向由B1离手建立，B2不强行保持外部“架左人右”的画面位置；B镜恢复既有外部轴线。

96镜308秒及所有对白保持，只有CY029B2的主画面替换。前一版本、原画面封版与历史候选均保留。未制作视频、声音；运动、速度变化与剪辑衔接仍待动态验证。
''')
snap=R/'镜头设计/带图分镜-v0.26.html'
if not snap.exists():shutil.copy2(R/'镜头设计/带图分镜.html',snap)
p='scripts/build_storyboard.py';write(p,read(p).replace('shot-plan-v0.26.json','shot-plan-v0.27.json').replace('"v026")','"v026", "v027")').replace("'v026')","'v026','v027')"))
p='00_打开项目.html';write(p,read(p).replace('v0.26','v0.27').replace(previous,IMG).replace('新增：火种飞行特写','修订：火种第一视角').replace('短暂慢动作与触木恢复正常速度 · 静帧候选','正前方缓缓逼近，末段提速触木 · 静帧候选').replace('火种慢镜与触木骤燃；对白保持','火种主观飞行与触木骤燃；对白保持'))
p='制作进度.md';t=read(p);i=t.index('## ')
write(p,t[:i]+'''## 2026-10-22：火种第一视角逼近空架（v0.27）

作者确认CY029B2改为火种主观视角：空架在前方缓缓逼近，画面中心不画火种，仅边缘保留少量虚焦火舌；末段提速触及铁箍下方裸露木纹，切回外部大火。CY029B1释放和CY029B收手后自主燃烧的画面保持。当前96镜308秒（5分08秒），全部对白和时长不变。

[当前分镜](镜头设计/带图分镜.html)与[剧本v0.27](剧本/穿云-场景剧本-v0.27.md)同步。新图是逼近末段代表帧、待作者审阅；旧侧跟镜与历史版本保留。实际飞行、变速、触木、剪辑及声音未制作。见[复核记录](镜头设计/生成记录/火种主观-v027/复核记录.md)。

'''+t[i:])
assert len(d['shots'])==96 and d['total_seconds']==308
assert all(a['id']==b['id'] and a['seconds']==b['seconds'] and a['dialogue']==b['dialogue'] and a.get('dialogue_cues')==b.get('dialogue_cues') for a,b in zip(old['shots'],d['shots']))
assert [b['id'] for a,b in zip(old['shots'],d['shots']) if a['presentation']['path']!=b['presentation']['path']]==['CY029B2']
print('Prepared v0.27: 96 shots, 308 seconds, all dialogue/timing preserved, only CY029B2 image changed.')

