"""Restore Claude's mother-design accessories without changing the edit."""
import json, shutil, hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def read(p): return json.loads((root/p).read_text(encoding='utf-8'))
def write(p,d): (root/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
archive=root/'镜头设计/带图分镜-v0.12.html'
if not archive.exists(): shutil.copy2(root/'镜头设计/带图分镜.html',archive)
d=read('镜头设计/shot-plan-v0.12.json')
script=(root/'剧本/穿云-场景剧本-v0.12.md').read_text(encoding='utf-8')
rule='Claude全片保留母本的大朵橙色层叠花饰、黑缎带、细金垂饰与象牙白半透明蕾丝头纱。花饰固定在角色自身左鬓（正面画面右侧），不随机镜像、不转移到GPT身上；近景远侧允许被头部遮挡。头纱由头后垂至肩背，不遮眼。天瀑前干燥；天瀑后湿贴发丝肩背；CY028C随衣料蒸干；随后恢复轻盈，公主抱时顺肩背与承托手臂外侧垂落。'
old='温暖火光掠过少女的裙边，水汽轻轻升腾，水分蒸散；衣料完整，她的赤足踩在平整平台上。'
new='温暖火光掠过少女的裙边，水汽轻轻升腾，衣料与头纱的水分一同蒸散；衣料完整，她的赤足踩在平整平台上。头纱随后恢复轻盈，暖流轻轻托起纱尾。'
changes=[('版本：v0.12','版本：v0.13'),(old,new)]
for a,b in changes:
 assert a in script
 script=script.replace(a,b)
script=script.replace('## S01｜街市·日·外','## 角色服饰连续性 · v0.13\n\n'+rule+'\n\n不新增摘纱、掉饰或烘干镜头。CY028C以裙边水汽承接整体烘干，下一镜可见恢复轻盈的头纱。月光、熄烛与空刑架局部火光沿用v0.12。\n\n## S01｜街市·日·外',1)
(root/'剧本/穿云-场景剧本-v0.13.md').write_text(script,encoding='utf-8')
d.update(title='《穿云》带图分镜 v0.13',version='v0.13',revision='v013',created='2026-10-22',story_script='剧本/穿云-场景剧本-v0.13.md',origin_manifest='镜头设计/shot-plan-v0.12.json',subtitle='Claude头纱、花饰与干湿状态连续性')
d['continuity']['claude_accessories']=rule
for m in d['masters']:
 if m['id']=='M-CL': m['role']=rule
d['review_intro']='Claude的橙花、黑缎带与蕾丝头纱全片保留。淋湿、随衣料蒸干、力竭接抱的状态连贯；花饰固定自身左侧，允许自然遮挡。'
d['review_focus']='重点查看CY012—022头纱保留、CY027G—028A湿纱、CY028C后恢复干燥，以及CY029C—030接抱时的左侧花饰与头纱落向。既有熄烛月光连续性继续保持。'
d['roughcut_preview_label']='旧版静帧配乐 v002（69镜239秒，未包含v0.13改图；Victory决定保留）'
records=read('镜头设计/生成记录/头纱连续-v013/结果映射.json')
selected={}
for r in records:
 if r['id'] not in selected or r['take']>selected[r['id']]['take']: selected[r['id']]=r
wet=False
for s in d['shots']:
 for key in ['action','entry_state','exit_state','source_quote','visual_prompt','sound']:
  if key in s:
   for a,b in changes: s[key]=s[key].replace(a,b)
 if s['id']=='CY024B': wet=True
 if s['id']=='CY028C': wet=False
 if 'Claude' in s['action'] or s['id'] in selected or s['id'] in ['CY028B','CY028C']:
  s['invariants'].append(rule)
  s['claude_accessory_state']='湿纱贴发丝肩背，左鬓花饰仍固定' if wet else '干燥轻盈头纱，左鬓花饰固定'
  if s['id']=='CY028C':s['claude_accessory_state']='裙边水汽代表衣料与头纱整体蒸干，后镜接轻盈干纱'
 if s['id'] not in selected:continue
 r=selected[s['id']];previous=s['presentation']['path'];job=read(r['request'])
 s['presentation']={'path':r['destination'],'role':'action','visible':s['action'],'status':'v0.13头纱与花饰修订候选，待作者审阅','missing':'静帧状态已补；纱尾连续运动与正式声音待制作。','show_as_main':True}
 s['visual_prompt']=job['input']['prompt'];s['generation_request']=r['request']
 s['refs']=[{'path':r['destination'],'role':'本轮独立改图候选'},{'path':r['request'],'role':'冻结的实际提示词与输入'},{'path':previous,'role':'保留的上一版'},{'path':'概念参考/01-Claude-母版概念参考.webp','role':'花饰与头纱身份依据'}]
 s['editorial_review']={'version':'v013','status':'candidate_static_review','dynamic_execution':'pending'}
 s['panel_index']=0;s.pop('display_crop_normalized',None)
for i,s in enumerate(d['shots']):
 s['presentation']['visible']=s['action']
 s['next_link']='接 '+d['shots'][i+1]['id']+'：'+s['exit_state']+' → '+d['shots'][i+1]['entry_state'] if i+1<len(d['shots']) else '结束。'
d['revision_notes'].update(previous_manifest='镜头设计/shot-plan-v0.12.json',previous_html='镜头设计/带图分镜-v0.12.html',added_ids=[],repurposed_ids=[],boundary='18镜独立头纱花饰修订，含返修24次请求；89镜286秒不变。四视图复用。旧配乐粗剪未重导。全部原件与冻结输入保留。')
d['page_layouts']=[{'path':s['presentation']['path'],'rows':1,'cols':1} for s in d['shots']]
for sc in d['scenes']:
 group=[s for s in d['shots'] if s['scene']==sc['id']]
 sc['pages']=list(dict.fromkeys(s['presentation']['path'] for s in group));sc['path']=sc['pages'][0]
assert all(s['source_quote'] in script for s in d['shots'])
assert len(d['shots'])==89 and sum(s['seconds'] for s in d['shots'])==286
write('镜头设计/shot-plan-v0.13.json',d)
for r in records:
 r['sha256']=hashlib.sha256((root/r['destination']).read_bytes()).hexdigest()
 assert r['sha256']==hashlib.sha256(Path(r['original']).read_bytes()).hexdigest()
 r['status']='candidate' if r['take']==selected[r['id']]['take'] else 'superseded-preserved'
write('镜头设计/生成记录/头纱连续-v013/归档校验.json',records)
assets=read('资产/assets.json')
for a in assets['assets']:
 if a['id']=='CHAR-CLAUDE':
  a['role']='橙发圣女四向全身参考，母版负责身份与服装。'+rule
  a['limits']='侧背与下裙含补全，不作为精确工程正交图。受缚至离殿采用赤足，四视图鞋仅为日常服装参考。近景不为展示花饰而换侧；不新增另一朵花。'
write('资产/assets.json',assets)
print('v0.13: 89 shots, 286 seconds, 18 accessory edits; 24 original hashes and script quotes passed')

